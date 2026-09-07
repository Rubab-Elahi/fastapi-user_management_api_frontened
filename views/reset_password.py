"""
Reset Password Page Component

Communicates with the FastAPI backend service to verify reset token
and update the user's password.
"""

import time
import streamlit as st
from api.auth_api import reset_password

def show_reset_password():
    st.title("Reset Password")

    # Check if password was just successfully reset
    if st.session_state.get("password_reset_success", False):
        st.success("Your password has been successfully reset! Please sign in again.")
        if st.button("Sign In Again"):
            st.session_state.password_reset_success = False
            st.switch_page("views/sign_in.py")
        return

    # Automatically extract token from query parameters (URL)
    token_from_url = st.query_params.get("token", "")
    if token_from_url:
        st.session_state["reset_token"] = token_from_url

    reset_token = st.session_state.get("reset_token", token_from_url)

    if not reset_token:
        st.warning("⚠️ No password reset token found. Please click the reset link sent to your email address.")
        if st.button("Go to Forgot Password Page"):
            st.switch_page("views/forget_password.py")
        return

    st.caption("Enter your new password below to update your account credentials.")

    # Form to capture only new password and confirmation (Token processed behind the scenes)
    with st.form(key="reset_form"):
        new_password = st.text_input(
            "New Password",
            type="password",
            placeholder="Minimum 8 characters",
            key="reset_new_password",
        )
        confirm_new_password = st.text_input(
            "Confirm New Password",
            type="password",
            placeholder="Re-enter new password",
            key="reset_confirm_password",
        )

        submit_reset = st.form_submit_button("Reset Password")

        # Password reset processing logic
        if submit_reset:
            # Rule 1: Check for incomplete fields
            if not new_password or not confirm_new_password:
                st.error("Please fill in both password fields.")
            # Rule 2: Verify new password matching
            elif new_password != confirm_new_password:
                st.error("New passwords do not match.")
            # Rule 3: Password length check (min 8 characters to match FastAPI schema)
            elif len(new_password) < 8:
                st.error("Password must be at least 8 characters long.")
            else:
                response = reset_password(reset_token.strip(), new_password)

                if response is None:
                    st.error("Cannot connect to FastAPI server. Check terminal.")
                elif response.status_code == 200:
                    st.session_state.password_reset_success = True
                    st.success("Password successfully reset! Redirecting to sign in...")
                    time.sleep(1.5)
                    st.switch_page("views/sign_in.py")
                else:
                    try:
                        error_msg = response.json().get("detail", "Invalid or expired reset token.")
                    except Exception:
                        error_msg = "Invalid or expired reset token."
                    st.error(f"Error: {error_msg}")

show_reset_password()
