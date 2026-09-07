"""
Sign In Page Component

Handles user authentication forms, validating credentials against
the FastAPI backend server and managing logged-in session state.
"""

import time
import streamlit as st
from api.auth_api import sign_in, sign_out

def show_sign_in():
    st.title("Sign In")
    st.caption("Enter your email address and password to access your account.")

    # If user is already logged in, show status & Sign Out button
    if st.session_state.auth_user:
        st.success(
            f"Logged in as **{st.session_state.auth_user['name']}** ({st.session_state.auth_user['email']})"
        )
        if st.button("Go to Dashboard"):
            st.switch_page("views/dashboard.py")
        if st.button("Sign Out"):
            if st.session_state.auth_user.get("token"):
                sign_out(st.session_state.auth_user["token"])
            st.session_state.auth_user = None
            st.rerun()
    else:
        # Wrap inputs inside a Streamlit form to batch user inputs until submit
        with st.form(key="login_form"):
            email = st.text_input(
                "Email Address",
                placeholder="name@example.com",
                key="login_email",
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password",
                key="login_password",
            )
            submit_login = st.form_submit_button("Sign In")

            # Form submission handler logic
            if submit_login:
                email_clean = email.strip().lower()
                
                # Check for empty fields
                if not email_clean or not password:
                    st.error("Please fill in both Email Address and Password.")
                else:
                    response = sign_in(email_clean, password)
                    if response is None:
                        st.error("Cannot connect to FastAPI server. Check terminal.")
                    elif response.status_code == 200:
                        try:
                            data = response.json()
                            user_name = data.get("name", data.get("full_name", email_clean.split('@')[0].capitalize()))
                            user_role = data.get("role", "student")
                            token = data.get("access_token")
                        except Exception:
                            user_name = email_clean.split('@')[0].capitalize()
                            token = None
                            user_role = "student"

                        st.session_state.auth_user = {
                            "email": email_clean,
                            "name": user_name,
                            "token": token,
                            "role": user_role,
                        }
                        st.success("Login successful!")
                        time.sleep(0.5)
                        st.switch_page("views/dashboard.py")
                    else:
                        try:
                            error_msg = response.json().get("detail", "Invalid email address or password.")
                        except Exception:
                            error_msg = "Invalid email address or password."
                        st.error(f"Error: {error_msg}")

show_sign_in()
