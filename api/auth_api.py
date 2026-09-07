import requests
import streamlit as st

BASE_URL = st.secrets["api"]["BASE_URL"]

def create_user(full_name: str, email: str, password: str, role: str = "student", token: str = None):
    """Sends registration details to FastAPI backend at /create-users."""
    url = f"{BASE_URL}/create-users"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    payload = {"name": full_name, "email": email, "password": password, "role": role}
    try:
        return requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException:
        return None

def sign_in(email: str, password: str):
    """Sends login credentials to FastAPI backend at /sign-in using form data."""
    url = f"{BASE_URL}/sign-in"
    # FastAPI SimpleOAuth2PasswordRequestForm expects form-encoded data with username & password
    data = {"username": email, "password": password}
    try:
        return requests.post(url, data=data, timeout=5)
    except requests.exceptions.RequestException:
        return None

def sign_out(token: str):
    """Invalidates active session token at FastAPI backend at /sign-out."""
    url = f"{BASE_URL}/sign-out"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        return requests.post(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException:
        return None

def forgot_password(email: str):
    """Requests password reset code from FastAPI backend at /forgot-password."""
    url = f"{BASE_URL}/forgot-password"
    payload = {"email": email}
    try:
        return requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException:
        return None

def reset_password(token: str, new_password: str):
    """Submits new password and verification code to FastAPI backend at /reset-password."""
    url = f"{BASE_URL}/reset-password"
    payload = {"token": token, "new_password": new_password}
    try:
        return requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException:
        return None

# Getting all users from the backend
def get_all_users(token: str = None):
    url = f"{BASE_URL}/get-users"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        return response
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)
        return None

def update_user(user_id: int, name: str, email: str, token: str = None, role: str = "student"):
    """Updates user details via PUT /update-users/{user_id}."""
    url = f"{BASE_URL}/update-users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    payload = {"name": name, "email": email, "role": role}
    try:
        return requests.put(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException:
        return None

def delete_user(user_id: int, token: str = None):
    """Deletes a user via DELETE /delete-users/{user_id}."""
    url = f"{BASE_URL}/delete-users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        return requests.delete(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException:
        return None


def get_users_by_role(role: str, token: str = None):
    """Fetch all users matching a specific role using query parameters."""
    url = f"{BASE_URL}/get-users-by-role"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    params = {"role": role}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        return response
    except requests.exceptions.RequestException:
        return None