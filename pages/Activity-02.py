
# from authent_streamlit_doc import check_password
# import hmac
from logout_button import logout_button
import streamlit as st
import pandas as pd
import numpy as np
import json
import random
# import mysqlclient  # pip install mysqlclient (hard to work with this pacakge)
# import PIL
from PIL import Image, UnidentifiedImageError
# import pymysql  # pip install pymysql
import io
from io import BytesIO
import base64
from datetime import date
import pdfkit  # pip install pdfkit
# pip install Jinja2
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader  # pip install
import time
from time import sleep
# import streamlit_authenticator as stauth  # pip install streamlit-authenticator
# import mysql.connector  # pip install mysql-connector-python
# from mysql.connector import FieldType  # pip install mysql-connector-python
from sqlalchemy.sql import text  # pip install SQLAlchemy
import sqlite3  # pip install db-sqlite3
import sys
import os
# import toml
# from streamlit_drawable_canvas import st_canvas
from fn_drawables import process_canvas
from fn_fileupload import process_image
# from menu import menu_with_redirect
import sqlalchemy.exc
from collections import OrderedDict
from helper_fn import start_quiz, next_question, previous_question, finish_quiz, base64_to_image, serialize_data


# Redirect to Login.py if not logged in, otherwise show the navigation menu
# menu_with_redirect()

hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}

            footer {visibility: hidden;}

            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Function to convert base64 string to PIL Image

# if "username" not in st.session_state or st.session_state.username == '' or st.session_state.username == None:
#     st.warning("You haven't logged in; Please login.")
if "username" not in st.session_state:
    st.session_state.username = "you"

st.title("Class Activity")

home_directory = st.text_input(
    "Enter the full path of a folder to save your work, for example C:/Users/aembaye ")

# Load the questions from the JSON file
with open('questions_act02.json', 'r') as file:
    questions = json.load(file)

try:
    # Get the user's home directory
    # home_directory = os.path.expanduser("~")
    # Define the path to the file in the home directory
    file_path = os.path.join(home_directory, "default_user_inputs.json")

    with open(file_path, "r") as json_file:
        default_vals = json.load(json_file)
except FileNotFoundError:
    print(f"{file_path} file not found. Setting default_vals to an empty dictionary.")
    default_vals = {}  # Correctly initialize as an empty dictionary
except json.JSONDecodeError:
    print(
        f"Error decoding JSON from {file_path}. Setting default_vals to an empty dictionary.")
    default_vals = {}  # Correctly initialize as an empty dictionary

# st.write(f"default_values looks like: {default_vals}")
# sys.exit()
# if True:
# user_inputs = {}  # eventually to the database or local storage
# Initialize user_inputs in st.session_state if it doesn't exist
if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = {}
# inputs4template = {}  # for the html template; all the user inputs can be used from user_inputs dict; but, for image upload, we cannot do that and we have to create for it
if 'inputs4template' not in st.session_state:
    st.session_state.inputs4template = {}

# Initialize session state variables
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = -1
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if not st.session_state.quiz_started:
    st.button("Start", on_click=start_quiz)

else:
    # st.write(
    #     f"st.session_state.current_question_index= {st.session_state.current_question_index} and its type: {type(st.session_state.current_question_index)}")
    question = questions[st.session_state.current_question_index]
    question_key = f"q{st.session_state.current_question_index+1}"
    thequestion = f"Question {st.session_state.current_question_index+1}: {question['label']}"
    # Use st.radio to display options as radio buttons
    st.write(thequestion)
    if question["qtype"] == "mc_quest":
        # Display the image if the "img" key exists and handle errors
        if "img" in question:
            try:
                # st.image("img15-4.png")
                st.image(question["img"])
            except Exception as e:
                st.error(f"Error loading image: {e}")

        previous_option_value = default_vals.get(question_key, "")

        # Initialize a variable to hold the index of the previously selected option
        previous_option_index = None  # Default to 0 or any other default index

        # Check if the previously selected option is in the current options list
        if previous_option_value in question["options"]:
            # Find the index of the previously selected option
            previous_option_index = question["options"].index(
                previous_option_value)
        st.session_state.user_inputs[question_key] = st.radio(
            label=thequestion, options=question["options"],  index=previous_option_index, label_visibility="hidden",  key=question_key)
    elif question["qtype"] == "float_num":
        st.session_state.user_inputs[question_key] = st.number_input(
            label=thequestion, min_value=None, value=float(default_vals.get(question_key, 0)),  label_visibility="hidden", key=question_key)
    elif question["qtype"] == "oneline_text":
        st.session_state.user_inputs[question_key] = st.text_input(
            label=thequestion, value=default_vals.get(question_key, ""),  label_visibility="hidden", key=question_key)
    elif question["qtype"] == "manyline_text":
        st.session_state.user_inputs[question_key] = st.text_area(label=thequestion,
                                                                  value=default_vals.get(question_key, ""), label_visibility="hidden",  key=question_key)
    elif question["qtype"] == "upload_quest":
        default_image_data = default_vals.get(question_key, "")
        # st.write(default_image_data)
        st.session_state.user_inputs[question_key], st.session_state.inputs4template[question_key] = process_image(default_image_data,
                                                                                                                   question_key)
    elif question["qtype"] == "drawing_quest":
        default_drawing_data = default_vals.get(question_key, "")
        st.session_state.user_inputs[question_key] = process_canvas(
            default_drawing_data)
        # Convert the default_value to an image and display it
        default_img = base64_to_image(default_drawing_data)
        if default_img:
            st.image(default_img, caption="Your previous drawing", width=150)

    col1, col2, col3 = st.columns([2, 8, 2])  # Adjust the ratio as needed

    if st.session_state.current_question_index > 0:
        with col1:
            st.button("Previous", on_click=previous_question)

    if st.session_state.current_question_index < len(questions) - 1:
        with col3:
            st.button("Next", on_click=next_question)
    else:
        with col3:
            st.button("Finish", on_click=finish_quiz)
# st.write(f"user_inputs: {st.session_state.user_inputs}")

# Serialize user_inputs excluding or converting non-serializable data
serializable_user_inputs = serialize_data(st.session_state.user_inputs)

# # save user entry in .json file
# save_button = st.button(label="save your work", key="save_button")

# if save_button:

#     # Serialize and save user_inputs to default_user_inputs.json
#     with open(file_path, "w") as json_file:
#         json.dump(serializable_user_inputs, json_file)

#     # Inform the user of the full path where the file is saved
#     st.write(f"User input saved as .json file at {file_path}")

submit = st.button(
    "Generate PDF", key="generate_button")

# Load HTML template
env = Environment(loader=FileSystemLoader(
    "."), autoescape=select_autoescape())

template = """
<!DOCTYPE html>
<html>
<head>
<title>Report</title>
<style>
    .page-break {
        page-break-before: always;
    }
</style>
</head>
<body>
<h1>Chapter 4 Quiz Report</h1>
"""

for index, (key, value) in enumerate(st.session_state.user_inputs.items()):
    qtype = questions[index]["qtype"] if index < len(
        questions) else "Unknown"
    question_number = index + 1  # Human-friendly question numbering
    if qtype == "mc_quest":
        template += f"""<h2>Question {question_number}</h2><div style="width:100px; height:20px; padding:20px; text-align:left; border: 1px solid #787878">
    {value}
</div>\n <br> <br>  """
    elif qtype == "float_num":
        template += f"""<h2>Question {question_number}</h2><div style="width:50px; height:20px; padding:20px; text-align:left; border: 1px solid #787878">
    {value}
    </div>\n  <br> <br> """
    elif qtype == "oneline_text":
        template += f"""<h2>Question {question_number}</h2><div style="width:700px; height:20px; padding:20px; text-align:left; border: 1px solid #787878">
    {value}
    </div>\n  <br> <br> """
    elif qtype == "manyline_text":
        template += f"""<h2>Question {question_number}</h2><div style="width:800px; height:200px; padding:20px; text-align:left; border: 1px solid #787878">    {value}</div >\n  <br> <br> """
    elif qtype == "upload_quest":
        processed_value = st.session_state.inputs4template[f"q{index+1}"]
        template += f"""<h2> Question {question_number}</h2><div style="width:700px; height:500px; padding:20px; text-align:center; border: 1px solid #787878">
    <img src="data:image/png;base64,{processed_value}" style="max-width:75%; max-height:75%; object-fit: contain;" />
    </div>\n  <br> <br>   """
    elif qtype == "drawing_quest":
        processed_value = value
        template += f"""<h2>Question {question_number}</h2><div style="width:700px; height:500px; padding:20px; text-align:center; border: 1px solid #787878"> 
    <img src="data:image/png;base64, {processed_value}" style="max-width:75%; max-height:75%; object-fit: contain;" />
    </div>\n  <br> <br>   """
    else:
        # Handle other question types
        pass

template += """
</body>
</html>
"""

# sys.exit()
# if True:
# st.write(f'uploads: {uploads}')
if submit:
    # Render the template with the user_inputs dictionary
    # html = template.render(**user_inputs)
    html = template

    # Check if the wkhtmltopdf executable exists in the local path
    local_wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    is_local = os.path.exists(local_wkhtmltopdf_path)

    if is_local:
        # Local development
        config = pdfkit.configuration(wkhtmltopdf=local_wkhtmltopdf_path)
        pdf = pdfkit.from_string(html, configuration=config)
    else:
        # Cloud deployment
        pdf = pdfkit.from_string(html, False)

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