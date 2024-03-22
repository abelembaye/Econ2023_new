# conda activate  cvenv309
# streamlit run Login.py

import streamlit as st
import pandas as pd
import json
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from sqlalchemy.sql import text  # pip install SQLAlchemy
import sys
import os
import time
from menu import menu

st.set_page_config(layout="wide")


# Initialize st.session_state.username to None
if "username" not in st.session_state:
    st.session_state["username"] = None

if "authenticator" not in st.session_state:
    st.session_state["authenticator"] = None

if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None


hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# ----------------------------------------------------------------------------------------------------------
conn = st.connection('mysql', type='sql', ttl=60)

# rosters_df = conn.query('SELECT * from rosters')


@st.cache_data
def get_rosters():
    return conn.query('SELECT * from rosters')


rosters_df = get_rosters()

# st.write(rosters_df)
# query = f"SELECT * from Econ3333pset03b WHERE username = 'asau';"
# hw_df = conn.query(query)
# st.write(hw_df)
# sys.exit()

# ----------------------------------------------------------------------------------------------------------

# Initialize st.session_state.username to None
if "username" not in st.session_state:
    st.session_state["username"] = None

# Initialize st.session_state.course to None
if "course" not in st.session_state:
    st.session_state.course = None

# Retrieve the course from Session State to initialize the widget
st.session_state._course = st.session_state.course


def set_course():
    # Callback function to save the course selection to Session State
    st.session_state.course = st.session_state._course


# Selectbox to choose course
selection = st.selectbox(
    "Please select your course and then wait few seconds for login form to appear:",
    [None, "Econ2013", "Econ4743", "Econ3333"],
    key="_course",
    on_change=set_course,
)


# Create a placeholder for the info message
info_message = st.empty()

if selection:
    info_message.info("Please wait a moment while we load your course...")

# This is authentication file fetch from db based on the course selected.
if st.session_state.course is not None:
    st.session_state.course = st.session_state.course
    info = rosters_df.loc[rosters_df['id'] ==
                          st.session_state.course, 'info'].values[0]
else:
    st.stop()

# If info is not None and not an empty string, otherwise change it to dictionary
if pd.notnull(info) and info != '':
    config = json.loads(info)  # loads the string to dictionary

# st.write(f"config file: {config}")

# sys.exit()


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

if "authenticator" not in st.session_state or st.session_state.authenticator is None:
    st.session_state.authenticator = authenticator

# # # uncomment this if you want to use the login widget and especially in cloud deployment
authenticator.login()

# Clear the info message
info_message.empty()


if st.session_state.get("authentication_status") is None:
    st.warning('Please enter your username and password')

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"]:
    authenticator.logout("Logout", "sidebar")
    st.write(f"You are logged in and you can now access the homework or assignment pertaining to your course")
    menu()


# conda activate  cvenv309
# streamlit run Login.py
