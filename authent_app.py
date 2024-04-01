
# # conda activate  cvenv309
# streamlit run authent_app.py

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

if not check_password():
    st.stop()

logout_button()

# Main Streamlit app starts here
st.write("Here goes your normal Streamlit app...")
st.button("Click me")


# # Compare to this authentication method:

# # Initialize st.session_state.username to None
# if "username" not in st.session_state:
#     st.session_state["username"] = None

# if "authenticator" not in st.session_state:
#     st.session_state["authenticator"] = None

# if "authentication_status" not in st.session_state:
#     st.session_state["authentication_status"] = None

# # ------------------------------------------------------------------------------------------
# conn = st.connection('mysql', type='sql', ttl=60)

# # rosters_df = conn.query('SELECT * from rosters')


# @st.cache_data
# def get_rosters():
#     return conn.query('SELECT * from rosters')


# rosters_df = get_rosters()
# # st.write(rosters_df)
# info = rosters_df.loc[rosters_df['id'] == 'Econ3333', 'info'].values[0]

# # If info is not None and not an empty string, otherwise change it to dictionary
# if pd.notnull(info) and info != '':
#     config = json.loads(info)  # loads the string to dictionary


# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )

# if "authenticator" not in st.session_state or st.session_state.authenticator is None:
#     st.session_state.authenticator = authenticator

# # # # uncomment this if you want to use the login widget and especially in cloud deployment
# authenticator.login()

# if st.session_state.get("authentication_status") is None:
#     st.warning('Please enter your username and password')

# elif st.session_state["authentication_status"] is False:
#     st.error('Username/password is incorrect')

# elif st.session_state["authentication_status"]:
#     authenticator.logout("Logout", "sidebar")
#     st.write(f"You are logged in and you can now access the homework or assignment pertaining to your course")
