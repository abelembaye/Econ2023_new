import streamlit as st


def logout_button():
    if st.sidebar.button('Logout'):
        # Clear the session state
        st.session_state.clear()

        # Rerun the app to go back to the login page
        st.rerun()
