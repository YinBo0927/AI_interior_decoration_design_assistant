import yaml
import base64
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.exceptions import (CredentialsError,
                                                          ForgotError,
                                                          LoginError,
                                                          RegisterError,
                                                          ResetError,
                                                          UpdateError) 
from app2 import main


def main_bg(main_bg):
    main_bg_ext = "png"
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


def login():
    
    # main_bg('bg.jpg')

    # Load config file
    with open('config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Create the authenticator object
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )

    # Initialize session state if not already initialized
    if 'page' not in st.session_state:
        st.session_state.page = 'Login'

    # Navigation function
    def navigate_to(page):
        st.session_state.page = page

    # Define actions for each page
    if st.session_state.page == 'Login':
        try:
            authenticator.login()
        except LoginError as e:
            st.error(e)

        if st.session_state["authentication_status"]:
            main() 
        elif st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button('Register', on_click=lambda: navigate_to('Register'))
            with col2:
                st.button('Forgot Password', on_click=lambda: navigate_to('Forgot Password'))
            with col3:
                st.button('Forgot Username', on_click=lambda: navigate_to('Forgot Username'))
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button('Register', on_click=lambda: navigate_to('Register'))
            with col2:
                st.button('Forgot Password', on_click=lambda: navigate_to('Forgot Password'))
            with col3:
                st.button('Forgot Username', on_click=lambda: navigate_to('Forgot Username'))

    elif st.session_state.page == 'Register':
        try:
            (email_of_registered_user,
            username_of_registered_user,
            name_of_registered_user) = authenticator.register_user(pre_authorization=False)
            if email_of_registered_user:
                st.success('User registered successfully')
        except RegisterError as e:
            st.error(e)

        st.button('Back to Login', on_click=lambda: navigate_to('Login'))

    elif st.session_state.page == 'Forgot Password':
        try:
            (username_of_forgotten_password,
            email_of_forgotten_password,
            new_random_password) = authenticator.forgot_password()
            if username_of_forgotten_password:
                st.success('New password sent securely')
                # Random password to be transferred to the user securely
            elif not username_of_forgotten_password:
                st.error('Username not found')
        except ForgotError as e:
            st.error(e)

        st.button('Back to Login', on_click=lambda: navigate_to('Login'))

    elif st.session_state.page == 'Forgot Username':
        try:
            (username_of_forgotten_username,
            email_of_forgotten_username) = authenticator.forgot_username()
            if username_of_forgotten_username:
                st.success('Username sent securely')
                # Username to be transferred to the user securely
            elif not username_of_forgotten_username:
                st.error('Email not found')
        except ForgotError as e:
            st.error(e)

        st.button('Back to Login', on_click=lambda: navigate_to('Login'))

    elif st.session_state.page == 'Reset Password':
        if st.session_state["authentication_status"]:
            try:
                if authenticator.reset_password(st.session_state["username"]):
                    st.success('Password modified successfully')
            except ResetError as e:
                st.error(e)
            except CredentialsError as e:
                st.error(e)
        else:
            st.warning('Please log in to reset your password.')

        st.button('Back to Login', on_click=lambda: navigate_to('Login'))

    elif st.session_state.page == 'Update User Details':
        if st.session_state["authentication_status"]:
            try:
                if authenticator.update_user_details(st.session_state["username"]):
                    st.success('Entries updated successfully')
            except UpdateError as e:
                st.error(e)
        else:
            st.warning('Please log in to update your details.')

        st.button('Back to Login', on_click=lambda: navigate_to('Login'))

    # CSS to position the logout button in the sidebar's bottom left
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .sidebar .sidebar-content .logout-button {
            text-align: left;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Position the logout button at the bottom-left corner of the sidebar
    if st.session_state["authentication_status"]:
        with st.sidebar:
            authenticator.logout('Logout', 'sidebar')

    # Save config file
    with open('config.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(config, file, default_flow_style=False)

if __name__ == '__main__':
    login()