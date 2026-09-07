"""
Sign Up Page Component

Handles new user registration by validating inputs and
sending user details to the FastAPI backend API.
"""

import time
import streamlit as st
from api.auth_api import create_user

def show_sign_up():
    st.title("Create Account")
    st.caption("Fill in your details to create a new account.")

    # Form component to group registration input fields
    with st.form(key="signup_form"):
        full_name = st.text_input(
            "Full Name", placeholder="Alex Morgan", key="signup_name"
        )
        email = st.text_input(
            "Email Address", placeholder="name@example.com", key="signup_email"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimum 8 characters",
            key="signup_password",
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter password",
            key="signup_confirm_password",
        )
        role = st.selectbox(
            "Role",
            options=["student", "admin", "principal", "vice principal"],
            key="signup_role",
        )
        accept_terms = st.checkbox(
            "I accept the Terms of Service"
        )

        submit_signup = st.form_submit_button("Create Account")

        # Form submission validation & account registration logic
        if submit_signup:
            email_clean = email.strip().lower()

            # Rule 1: Ensure all fields are filled
            if (
                not full_name
                or not email_clean
                or not password
                or not confirm_password
            ):
                st.error("All fields are required.")
            # Rule 2: Basic email format validation
            elif "@" not in email_clean or "." not in email_clean:
                st.error("Please enter a valid email address.")
            # Rule 3: Passwords match check
            elif password != confirm_password:
                st.error("Passwords do not match.")
            # Rule 4: Password length constraint
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long.")
            # Rule 5: Terms of service acceptance check
            elif not accept_terms:
                st.warning("Please agree to the Terms of Service to proceed.")
            else:
                response = create_user(full_name, email_clean, password, role)

                if response is None:
                    st.error("Cannot connect to FastAPI server. Check terminal.")
                elif response.status_code in (200, 201):
                    st.success(f"Hello! Account created successfully as **{role.title()}**! You can now sign in.")
                    time.sleep(1)
                    st.switch_page("views/sign_in.py")
                else:
                    try:
                        error_msg = response.json().get("detail", "Failed to create account.")
                    except Exception:
                        error_msg = "Failed to create account."
                    st.error(f"Error: {error_msg}")

show_sign_up()
