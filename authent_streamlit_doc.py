import hmac
import streamlit as st

import streamlit as st
import hmac


def login_form():
    """Form with widgets to collect user information"""
    with st.form("login_form"):
        st.text_input("Username", key="login_username")
        st.text_input("Password", type="password", key="login_password")
        st.form_submit_button("Log in", on_click=password_entered)


def password_entered():
    """Checks whether a password entered by the user is correct."""
    if st.session_state["login_username"] in st.secrets[
        "passwords"
    ] and hmac.compare_digest(
        st.session_state["login_password"],
        st.secrets.passwords[st.session_state["login_username"]],
    ):
        st.session_state["password_correct"] = True
        # Update the username in the session state
        # if you want to keep the username
        st.session_state["username"] = st.session_state["login_username"]
        # Don't store the username or password.
        del st.session_state["login_password"]
        del st.session_state["login_username"]
    else:
        st.session_state["password_correct"] = False


def check_password():
    """Returns `True` if the user had a correct password."""
    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False
