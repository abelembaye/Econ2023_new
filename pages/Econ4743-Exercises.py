
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
# import pdfkit  # pip install pdfkit
# pip install Jinja2
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import time
from time import sleep
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import mysql.connector  # pip install mysql-connector-python
# from mysql.connector import FieldType  # pip install mysql-connector-python
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
import matplotlib.pyplot as plt # pip install matplotlib
from sklearn.linear_model import LinearRegression  # pip install scikit-learn


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

elif "course" not in st.session_state or st.session_state.course == '' or st.session_state.course == None or st.session_state.course != "Econ4743":
    st.warning(
        "You are not allowed to access this courese with the given credentials.")
# ---------------------------------------------------------------------------------------------------------------#
else:
    # st.title("Econ 4743 Exercises")
    st.markdown("<h1 style='text-align: center; color: Black;'>Econ 4743 Notes</h1>",
                unsafe_allow_html=True)
    st.markdown("# Centeral Limit Theorem")

    # Generate a population of 1000 observations
    n = 10000  # population size
    nsample = 1500  # sample size
    rep = 100
    np.random.seed(0)
    # x = np.random.uniform(0, 1, n)
    x = np.random.normal(0, 1, n)
    y = 2 + 3*x + np.random.normal(0, 1, n)
    st.write(f'Suppose in the population of 10,000 ordered pairs the relationship between Y and X is given by \n \n Y= 2 + 3X+ u  \n \n where u ~ N(0,1)')

    data = pd.DataFrame({'x': x, 'y': y})

    # Initialize an empty list to store the slope coefficients
    coefficients = []

    # Run the loop 50 times
    for _ in range(rep):
        # Randomly sample 100 observations from the population
        sample = data.sample(nsample)

        # Fit a simple linear regression model to the sample
        model = LinearRegression()
        model.fit(sample[['x']], sample['y'])

        # Extract the slope coefficient and append it to the list
        coefficients.append(model.coef_[0])

    # Calculate the average of the slope coefficients
    average_coefficient = np.mean(coefficients)

    # Use streamlit to display the results
    st.write(f'True slope coefficient: 3')
    st.write(
        f'Estimates from the {rep} samples of each {nsample} size: \n \n {[round(coef, 3) for coef in coefficients]}')
    st.write(f'Average slope coefficient: {round(average_coefficient,3) }')
    # Plot a histogram of the slope coefficients
    # fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.hist(coefficients, bins=20)
    st.pyplot(fig)
