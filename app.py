import streamlit as st
from api.auth_api import sign_out

# Page Configuration Settings
st.set_page_config(
    page_title="Streamlit Forms",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom UI Styling
st.markdown(
    """
<style>
    header, footer { visibility: hidden; }
    
    .stButton > button {
        width: 100%;
        border-radius: 6px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize Session State Variables

# Simulated in-memory database for users
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "user@example.com": {
            "name": "Alex Morgan",
            "password": "Password123!",
            "reset_token": None,
        }
    }

# Tracks logged in user payload (None if guest)
if "auth_user" not in st.session_state:
    st.session_state.auth_user = None

# Define Streamlit Pages using script file paths
page_sign_in = st.Page(
    "views/sign_in.py",
    title="Sign In",
    icon="🔑",
    url_path="login",
    default=True,
)

page_sign_up = st.Page(
    "views/sign_up.py",
    title="Sign Up",
    icon="📝",
    url_path="signup",
)

page_forgot_password = st.Page(
    "views/forget_password.py",
    title="Forgot Password",
    icon="❓",
    url_path="forgot-password",
)

page_reset_password = st.Page(
    "views/reset_password.py",
    title="Reset Password",
    icon="🔒",
    url_path="reset-password",
)

page_dashboard = st.Page(
    "views/dashboard.py",
    title="Dashboard",
    icon="📊",
    url_path="dashboard",
)

# Group pages dynamically for st.navigation
if st.session_state.auth_user:
    nav_sections = {
        "Main": [page_dashboard],
        "Account": [
            page_sign_in,
            page_sign_up,
            page_forgot_password,
            page_reset_password,
        ],
    }
else:
    nav_sections = {
        "Authentication": [
            page_sign_in,
            page_sign_up,
            page_forgot_password,
            page_reset_password,
        ],
        "Main": [page_dashboard],
    }

# Sidebar Profile Status Section
with st.sidebar:
    st.title("Navigation Menu")
    if st.session_state.auth_user:
        st.success(f"Logged in as **{st.session_state.auth_user['name']}**")
        if st.button("Sign Out", key="sidebar_logout_btn"):
            if st.session_state.auth_user.get("token"):
                sign_out(st.session_state.auth_user["token"])
            st.session_state.auth_user = None
            st.switch_page("views/sign_in.py")
    st.divider()

# Execute Streamlit Navigation
pg = st.navigation(nav_sections)
pg.run()