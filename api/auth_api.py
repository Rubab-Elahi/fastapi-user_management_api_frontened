import logging
import requests
import streamlit as st

logger = logging.getLogger(__name__)

BASE_URL = st.secrets["api"]["BASE_URL"]

def create_user(full_name: str, email: str, password: str, role: str = "student", token: str = None):
    """Sends registration details to FastAPI backend at /create-users."""
    url = f"{BASE_URL}/create-users"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    payload = {"name": full_name, "email": email, "password": password, "role": role}
    logger.info("Creating user for email: %s with role: %s", email, role)
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        logger.info("create_user request completed with status code: %s", response.status_code)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Error creating user (%s): %s", email, e)
        return None

def sign_in(email: str, password: str):
    """Sends login credentials to FastAPI backend at /sign-in using form data."""
    url = f"{BASE_URL}/sign-in"
    # FastAPI SimpleOAuth2PasswordRequestForm expects form-encoded data with username & password
    data = {"username": email, "password": password}
    logger.info("Attempting sign_in for user: %s", email)
    try:
        response = requests.post(url, data=data, timeout=5)
        logger.info("sign_in request completed with status code: %s", response.status_code)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Error signing in user (%s): %s", email, e)
        return None

def sign_out(token: str):
    """Invalidates active session token at FastAPI backend at /sign-out."""
    url = f"{BASE_URL}/sign-out"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    logger.info("Attempting sign_out request")
    try:
        response = requests.post(url, headers=headers, timeout=5)
        logger.info("sign_out request completed with status code: %s", response.status_code)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Error during sign_out: %s", e)
        return None

def forgot_password(email: str):
    """Requests password reset code from FastAPI backend at /forgot-password."""
    url = f"{BASE_URL}/forgot-password"
    payload = {"email": email}
    logger.info("Requesting forgot_password for email: %s", email)
    try:
        response = requests.post(url, json=payload, timeout=5)
        logger.info("forgot_password request completed with status code: %s", response.status_code)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Error in forgot_password for email (%s): %s", email, e)
        return None

def reset_password(token: str, new_password: str):
    """Submits new password and verification code to FastAPI backend at /reset-password."""
    url = f"{BASE_URL}/reset-password"
    payload = {"token": token, "new_password": new_password}
    logger.info("Attempting reset_password with token")
    try:
        response = requests.post(url, json=payload, timeout=5)
        logger.info("reset_password request completed with status code: %s", response.status_code)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Error resetting password: %s", e)
        return None

# Getting all users from the backend
def get_all_users(token: str = None):
    url = f"{BASE_URL}/get-users"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    logger.info("Fetching all users")
    try:
        response = requests.get(url, headers=headers, timeout=5)
        logger.info("get_all_users request completed with status code: %s", response.status_code)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Connection error in get_all_users: %s", e)
        return None

def update_user(user_id: int, name: str, email: str, token: str = None, role: str = "student"):
    """Updates user details via PUT /update-users/{user_id}."""
    url = f"{BASE_URL}/update-users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    payload = {"name": name, "email": email, "role": role}
    logger.info("Updating user ID: %s (email: %s, role: %s)", user_id, email, role)
    try:
        response = requests.put(url, json=payload, headers=headers, timeout=5)
        logger.info("update_user request completed with status code: %s", response.status_code)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Error updating user ID %s: %s", user_id, e)
        return None

def delete_user(user_id: int, token: str = None):
    """Deletes a user via DELETE /delete-users/{user_id}."""
    url = f"{BASE_URL}/delete-users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    logger.info("Deleting user ID: %s", user_id)
    try:
        response = requests.delete(url, headers=headers, timeout=5)
        logger.info("delete_user request completed with status code: %s", response.status_code)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Error deleting user ID %s: %s", user_id, e)
        return None

def get_users_by_role(role: str, token: str = None):
    """Fetch all users matching a specific role using query parameters."""
    url = f"{BASE_URL}/get-users-by-role"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    params = {"role": role}
    logger.info("Fetching users by role: %s", role)
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        logger.info("get_users_by_role request completed with status code: %s", response.status_code)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching users by role (%s): %s", role, e)
        return None