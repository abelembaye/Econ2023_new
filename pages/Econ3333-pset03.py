
import streamlit as st
import pandas as pd
import numpy as np
import json
import random
# import mysqlclient  # pip install mysqlclient (hard to work with this pacakge)
# import PIL
from PIL import Image
import pymysql  # pip install pymysql
import io
from io import BytesIO
import base64
from datetime import date
import pdfkit  # pip install pdfkit
# pip install Jinja2
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import time
from time import sleep
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import mysql.connector  # pip install mysql-connector-python
from mysql.connector import FieldType  # pip install mysql-connector-python
from sqlalchemy.sql import text  # pip install SQLAlchemy
import sys
import os
import toml
# from streamlit_drawable_canvas import st_canvas
# from fn_drawables import process_canvas
from fn_fileupload import process_image

from menu import menu_with_redirect

# Redirect to Login.py if not logged in, otherwise show the navigation menu
menu_with_redirect()


hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

authenticator = st.session_state.authenticator

if st.session_state["authentication_status"]:
    authenticator.logout("Logout", "sidebar")
# ---------------------------------------------------------------------------------------------------------------# Initialize st.session_state.course to None


if "username" not in st.session_state or st.session_state.username == '' or st.session_state.username == None:
    st.warning("You haven't logged in; Please login.")

elif "course" not in st.session_state or st.session_state.course == '' or st.session_state.course == None or st.session_state.course != "Econ3333":
    st.warning(
        "You are not allowed to access this courese with the credentials you submitted.")

else:
    st.title("Econ 3333 Problem Set 3")

    conn = st.connection('mysql', type='sql', ttl=60)
    query = f"SELECT * from Econ3333pset03c WHERE username = '{st.session_state.username}';"
    hw_df = conn.query(query)
    # st.write(f" hw_df datatype: \n \n {type(hw_df)}")

    # Get column names and types
    hw_column_names = hw_df.columns[2:].tolist()
    hw_column_types = hw_df.dtypes[2:].tolist()

    hw_column_types = [4, 4, 252, 4, 252, 252]

    # st.write( f"hw_column_names:  \n \n {hw_column_names};  \n \n hw_column_types:  \n \n {hw_column_types}")

    # sys.exit()

    user_row = hw_df  # [hw_df['username'] == st.session_state.username]
    # Get the user_row from the database
    # Use a dictionary to store the default values
    default_vals = {}

    # Get the default values from the user_row of the database to a dictionary
    for col in hw_column_names:
        # Check if the user_row is not empty
        if not user_row.empty:
            # If not empty, get the value from the user_row
            default_vals[col] = user_row[col].values[0]
        else:
            # If empty, set the value to None
            default_vals[col] = 0  # None
    # st.write(default_vals)
    # ------------------------------------------------- New User input prompt starts here  -------------------------------
    user_inputs = {}
    # Create a dictionary to store the variables
    uploads = {}

    # replace with your actual text column names
    # text_columns = ['q6', 'q16', 'q19']
    text_columns = ["q1"]

    # ---------------Questions and fetching of default values of questions starts here ---------------------------
    for i in range(len(hw_column_names)):
        if hw_column_types[i] == FieldType.FLOAT:
            user_inputs[hw_column_names[i]] = st.number_input(hw_column_names[i], min_value=None, value=float(
                default_vals[hw_column_names[i]]), key=hw_column_names[i])
        elif hw_column_types[i] == FieldType.VAR_STRING:
            user_inputs[hw_column_names[i]] = st.text_input(
                hw_column_names[i], value=default_vals[hw_column_names[i]], key=hw_column_names[i])
        elif hw_column_types[i] == FieldType.BLOB and hw_column_names[i] in text_columns:
            user_inputs[hw_column_names[i]] = st.text_area(
                hw_column_names[i], value=default_vals[hw_column_names[i]], key=hw_column_names[i])
        elif hw_column_types[i] == FieldType.BLOB:
            upload2db, upload2templ = process_image(
                hw_df, hw_column_names[i])
            user_inputs[hw_column_names[i]] = upload2db
            # uploads[f'q{i+1}'] = upload2templ
            uploads[hw_column_names[i]] = upload2templ

    # sys.exit()

    with st.form(key="fields_form2"):
        submit_button = st.form_submit_button(label="save your work")
        if submit_button:
            # st.write(f"username inside submit button: {username}")
            with conn.session as s:
                sql = text('UPDATE Econ3333pset03c SET ' + ', '.join(
                    [f'{q}=:{q}' for q in hw_column_names]) + ' WHERE username=:username;')

                params = {
                    **{q: user_inputs[q] for q in hw_column_names}, 'username': st.session_state.username}
                s.execute(sql, params)
                s.commit()
            st.write(
                " Your work has been submitted successfully to database, but download a pdf file below for gradescope submission! 👍")

        # df_new = conn.query(query, ttl=0)
        # st.write(df_new)

    submit = st.button("Generate PDF, don't forget to save your work before!")

    # Load HTML template
    env = Environment(loader=FileSystemLoader(
        "."), autoescape=select_autoescape())

    # here the template is in a separate .html file
    template = env.get_template("template-Econ3333-ps03.html")

    # Add the student_name to the user_inputs dictionary
    user_inputs["student_name"] = st.session_state.username
    # Merge user_inputs and uploads dictionaries
    merged_inputs = {**user_inputs, **uploads}

    # st.write(f'uploads: {uploads}')
    if submit:
        # Start the progress bar
        progress = st.progress(0)

        # Render the HTML template

        # Render the template with the user_inputs dictionary
        html = template.render(**merged_inputs)

        # Update the progress bar
        progress.text('Rendering HTML template...')
        progress.progress(25)

        # Update the progress bar
        progress.text('Generating PDF...')
        progress.progress(50)

        incloud = True  # False  #

        if incloud:
            pdf = pdfkit.from_string(html, False)  # when in cloud deployment

        # if local development:
        else:
            # must be comments in deployment in cloud
            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

            # must be commented in deployment in cloud
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            pdf = pdfkit.from_string(html,  configuration=config)
            # pdf = pdfkit.from_string(
            #     html, f"{st.session_state.username}_Pset03_completed.pdf", configuration=config)
        # Update the progress bar
        progress.text('Saving PDF...')
        progress.progress(75)

        # Finish the progress bar
        progress.text('Done!')
        progress.progress(100)
        st.success(
            "🎉 Your PDF file has been generated! Download it below and submit it in gradescope!")

        st.download_button(
            # "⬇️ Download HTML",
            "⬇️ Download pdf",
            # data=html,
            data=pdf,
            # file_name=f"{st.session_state.username}_Pset03_completed.html",
            file_name=f"{st.session_state.username}_Pset03.pdf",
            # mime="text/html",
            mime="application/octet-stream",
        )
