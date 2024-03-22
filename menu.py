import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    # st.sidebar.page_link("Login.py", label="Switch accounts")
    # st.sidebar.page_link("pages/user.py", label="Your profile")
    if st.session_state.course == "Econ3333" and st.session_state.username != None:
        st.sidebar.page_link("pages/Econ3333-pset03.py", label="Econ3333-pset03",
                             disabled=st.session_state.course != "Econ3333")
    elif st.session_state.course == "Econ4743" and st.session_state.username != None:
        st.sidebar.page_link("pages/Econ4743-pset03.py", label="Econ4743-pset03",
                             disabled=st.session_state.course != "Econ4743")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("Login.py", label="Login")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "course" not in st.session_state or st.session_state.course is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "course" not in st.session_state or st.session_state.course is None:
        st.switch_page("Login.py")
    menu()
