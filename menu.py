import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    # st.sidebar.page_link("Login.py", label="Switch accounts")
    # st.sidebar.page_link("pages/user.py", label="Your profile")
    #if st.session_state.course == "Econ3333" and st.session_state.username != None:
    if st.session_state.username != None:
        st.sidebar.page_link("pages/Econ3333-pset03_edit.py", label="Econ3333-pset03_edit",
                             disabled=st.session_state.course != "Econ3333")
        # st.sidebar.page_link("pages/Econ3333-pset04x_withoutdb.py", label="Econ3333-pset04x_withoutdb",
        #                      disabled=st.session_state.course != "Econ3333")
        # st.sidebar.page_link("pages/Econ3333-pset04.py", label="Econ3333-pset04",
        #                      disabled=st.session_state.course != "Econ3333")
        # st.sidebar.page_link("pages/Econ3333-regression.py", label="Econ3333-regression",
        #                      disabled=st.session_state.course != "Econ3333")
        # st.sidebar.page_link("pages/Econ3333-pset03.py", label="Econ3333-pset03",
        #                      disabled=st.session_state.course != "Econ3333")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("Entry_code.py", label="Login")


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
        st.switch_page("Entry_code.py")
    menu()
