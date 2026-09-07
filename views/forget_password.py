import streamlit as st
from api.auth_api import forgot_password

def show_forgot_password():
    st.title("Forgot Password")
    st.caption("Enter your email address to receive a password reset code.")

    with st.form(key="forgot_form"):
        email = st.text_input("Registered Email Address", placeholder="name@example.com")
        submit_forgot = st.form_submit_button("Send Reset Code")

        if submit_forgot:
            email_clean = email.strip().lower()

            if not email_clean:
                st.error("Please enter your email address.")
            else:
                response = forgot_password(email_clean)

                if response is None:
                    st.error("Cannot connect to FastAPI server. Check terminal.")
                elif response.status_code == 200:
                    st.success("If an account exists, a reset code has been sent to your email!")
                    st.info("Check your inbox and click below to enter your code on the Reset Password page.")
                else:
                    try:
                        error_msg = response.json().get("detail", "Request failed.")
                    except Exception:
                        error_msg = "Request failed."
                    st.error(f"Error: {error_msg}")

    st.divider()
    if st.button("Have a reset code? Go to Reset Password Page"):
        st.switch_page("views/reset_password.py")

show_forgot_password()