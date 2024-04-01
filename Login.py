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
import hmac
from logout_button import logout_button
from authent_streamlit_doc import check_password


st.set_page_config(layout="wide")

# Initialize st.session_state.incloud to None
if "incloud" not in st.session_state:
    # change this to True to enable cloud deployment
    st.session_state["incloud"] = True  # False

hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# db = False  # True # False

# Initialize st.session_state.username to None
if "username" not in st.session_state:
    st.session_state["username"] = None

if "authenticator" not in st.session_state:
    st.session_state["authenticator"] = None

if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None


st.write("incloud: ", st.session_state.incloud)
# ------------------------------------------------------------------------------------------
conn = st.connection('mysql', type='sql', ttl=60)

# rosters_df = conn.query('SELECT * from rosters')


@st.cache_data
def get_rosters():
    return conn.query('SELECT * from rosters')


rosters_df = get_rosters()


# Initialize st.session_state.course to None
if "course" not in st.session_state:
    st.session_state.course = None

# Retrieve the course from Session State to initialize the widget
st.session_state._course = st.session_state.get('course', None)


def set_course():
    # Callback function to save the course selection to Session State
    st.session_state.course = st.session_state._course


# Create a placeholder for the selection widget
selection_placeholder = st.empty()

# Selectbox to choose course
selection = selection_placeholder.selectbox(
    "Please select your course and then wait few seconds for login form to appear:",
    [None, "Econ2013", "Econ4743", "Econ3333"],
    key="_course",
    on_change=set_course,
)

# Create a placeholder for the info message
info_message = st.empty()

if selection:
    # Clear the selection widget
    selection_placeholder.empty()

    if not check_password():
        st.stop()

    else:
        st.write(
            f"Hi @{st.session_state.username}, you are sucessfully logged in and now select the folder in your course to navigate to.")

logout_button()

menu()

# sys.exit()

# conda activate  cvenv309
# streamlit run Login.py
