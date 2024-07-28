
# # conda activate  cvenv309
# streamlit run Z_generate_pdffile_student.py
from authent_streamlit_individual import check_password
from logout_button import logout_button
import hmac
import streamlit as st
import pandas as pd
import numpy as np
import json
import random
# import mysqlclient  # pip install mysqlclient (hard to work with this pacakge)
# import PIL
from PIL import Image
# import pymysql  # pip install pymysql
import io
from io import BytesIO
import base64
from datetime import date
import pdfkit  # pip install pdfkit
# pip install Jinja2
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader, DictLoader
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
# from fn_drawables import process_canvas
from fn_fileupload import process_image
from menu import menu_with_redirect
import sqlalchemy.exc

# Load the .csv file
# df = pd.read_csv(r'C:/Users/aembaye/OneDrive - University of Arkansas/C2-embaye/Teaching/00_AllCourses/Ec_4743/Grades/_92_Sp2024/pse04_submission/_submission_metadata.csv')
df = pd.read_csv(r'C:/Users/aembaye/OneDrive - University of Arkansas/C2-embaye/Teaching/00_AllCourses/Ec_3333_PubEcon/Grades/_96_Sp2024/Pset04/submissions/_submission_metadata.csv')

df.fillna('--', inplace=True)

# Path to wkhtmltopdf
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Folder to save the PDF files
folder = r'C:/Users/aembaye/OneDrive - University of Arkansas/C2-embaye/Teaching/00_AllCourses/Ec_3333_PubEcon/Grades/_96_Sp2024/Pset04/submissions'

# Simple HTML template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <style>
        .response {
            border: 1px solid black;
            padding: 10px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <h1>{{ full_name }}</h1>
    {% for name, response in responses.items() %}
        <div class="response">
            <h2>{{ name }}</h2>
            <p>{{ response }}</p>
        </div>
    {% endfor %}
</body>
</html>
"""

# Set up the Jinja2 environment
env = Environment(loader=DictLoader(
    {'template.html': html_template}), autoescape=select_autoescape())

# Load the HTML template
template = env.get_template('template.html')

# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    # For each column that ends with 'Response', put its value in an HTML template variable
    html_variables = {column: row[column]
                      for column in df.columns if column.endswith('Response') or column == 'fullname'}

    # Store the idnumber in the session state
    st.session_state.student_id_number = row['fullname']

    # Render the HTML template with the variables
    html = template.render(responses=html_variables)

    # # Save the HTML to a file
    # with open(f"{folder}\\{st.session_state.student_id_number}_Pset04_completed.html", 'w', encoding='utf-8') as f:
    #     f.write(html)

    # st.write(f"Generated HTML for {st.session_state.student_id_number}")
    # Generate the PDF
    pdfkit.from_string(
        html, f"{folder}\\{st.session_state.student_id_number}_Pset04_completed.pdf", configuration=config)
    st.write(f"Generated PDF for {st.session_state.student_id_number}")

    # # conda activate  cvenv309
# streamlit run Z_generate_pdffile_student.py
