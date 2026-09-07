import streamlit as st
from api.auth_api import create_user, get_all_users, update_user, delete_user, get_users_by_role


ALLOWED_ROLES = ["student", "admin", "principal", "vice principal"]

ROLE_CREATION_MATRIX = {
    "vice principal": ["principal", "admin", "student"],
    "principal": ["admin", "student"],
    "admin": ["student"],
}


def get_allowed_roles_for_user():
    auth_user = st.session_state.get("auth_user") or {}
    user_role = str(auth_user.get("role", "")).lower()
    return ROLE_CREATION_MATRIX.get(user_role, ALLOWED_ROLES)


@st.dialog("Create New User")
def show_create_user_dialog(token=None):
    allowed_options = get_allowed_roles_for_user()
    with st.form("create_user_modal_form", clear_on_submit=True):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password", placeholder="Minimum 8 characters")
        role = st.selectbox("Role", options=allowed_options, index=0)

        submitted = st.form_submit_button("Create", type="primary")

        if submitted:
            if not full_name or not email or not password:
                st.error("Please fill out all fields.")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long.")
            else:
                res = create_user(full_name, email, password, role, token=token)
                if res and res.status_code in [200, 201]:
                    st.toast("User created successfully!", icon="✅")
                    st.rerun()
                else:
                    try:
                        err_data = res.json()
                        detail = err_data.get("detail", "Server error")
                        if isinstance(detail, list):
                            detail = "; ".join([d.get("msg", str(d)) for d in detail])
                    except Exception:
                        detail = "Server error"
                    st.error(f"Failed to create user: {detail}")


@st.dialog("Update User")
def show_update_user_dialog(user, token):
    with st.form("update_user_modal_form"):
        st.write(f"Editing User **ID: {user['id']}**")
        new_name = st.text_input("Full Name", value=user.get("name", ""))
        new_email = st.text_input("Email Address", value=user.get("email", ""))
        
        allowed_options = get_allowed_roles_for_user()
        current_role = user.get("role", "student").lower()
        role_index = allowed_options.index(current_role) if current_role in allowed_options else 0
        new_role = st.selectbox("Role", options=allowed_options, index=role_index)

        submitted = st.form_submit_button("Save Changes", type="primary")

        if submitted:
            if not new_name or not new_email:
                st.error("Full Name and Email cannot be empty.")
            else:
                res = update_user(user["id"], new_name, new_email, token, new_role)
                if res and res.status_code == 200:
                    if user.get("email") == st.session_state.auth_user.get("email"):
                        st.session_state.auth_user["email"] = new_email
                        st.session_state.auth_user["name"] = new_name
                    st.toast("User updated successfully!", icon="✅")
                    st.rerun()
                else:
                    detail = res.json().get("detail") if res else "Failed to update user"
                    st.error(f"Error updating user: {detail}")


@st.dialog("Confirm Delete User")
def show_delete_user_dialog(user, token):
    st.warning(f"Are you sure you want to delete **{user.get('name')}** ({user.get('email')})?")
    st.caption("This action cannot be undone.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("🗑️ Yes, Delete", type="primary", use_container_width=True):
            res = delete_user(user["id"], token)
            if res and res.status_code in [200, 204]:
                if user.get("email") == st.session_state.auth_user.get("email"):
                    st.session_state.auth_user = None
                    st.rerun()
                else:
                    st.toast("User deleted successfully!", icon="🗑️")
                    st.rerun()
            else:
                detail = res.json().get("detail") if res else "Failed to delete user"
                st.error(f"Error deleting user: {detail}")


def show_dashboard():
    st.title("User Dashboard")

    if st.session_state.auth_user:
        token = st.session_state.auth_user.get("token")
        user_name = st.session_state.auth_user.get("name", "User")
        user_role = str(st.session_state.auth_user.get("role", "student")).title()

        st.info(f"👋 **Hello, {user_name}!** You are signed in as **{user_role}**.")

        # Action Bar with Create User Button
        col1, col2 = st.columns([4, 1])
        with col1:
            st.subheader("System Users")
        with col2:
            if st.button("➕ Create User", type="primary", use_container_width=True):
                show_create_user_dialog(token)

        st.divider()

        # ---------------- ROLE FILTER SECTION ----------------
        filter_col1, _ = st.columns([2, 2])
        with filter_col1:
            selected_role = st.selectbox(
                "Filter by Role:",
                options=["All users"] + get_allowed_roles_for_user(),
                index=0
            )

        # Fetch Data based on filter condition
        if selected_role == "All users":
            response = get_all_users(token)
            target_role = ""
        else:
            response = get_users_by_role(selected_role, token)
            target_role = selected_role

        st.divider()

        # ---------------- TABLE DISPLAY SECTION ----------------
        if response and response.status_code == 200:
            users_data = response.json()
            if users_data:
                if target_role:
                    st.caption(f"Showing results for Role: **{target_role}** ({len(users_data)} users found)")

                # Table Header
                h_id, h_name, h_email, h_role, h_actions = st.columns([1, 3, 3, 2, 3])
                with h_id:
                    st.markdown("**ID**")
                with h_name:
                    st.markdown("**Name**")
                with h_email:
                    st.markdown("**Email**")
                with h_role:
                    st.markdown("**Role**")
                with h_actions:
                    st.markdown("**Actions**")

                st.divider()

                # Table Rows with Edit & Delete Buttons
                for user in users_data:
                    c_id, c_name, c_email, c_role, c_actions = st.columns([1, 3, 3, 2, 3])
                    with c_id:
                        st.write(user.get("id"))
                    with c_name:
                        st.write(user.get("name"))
                    with c_email:
                        st.write(user.get("email"))
                    with c_role:
                        st.write(user.get("role", "user"))
                    with c_actions:
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            if st.button("✏️ Edit", key=f"edit_{user['id']}", use_container_width=True):
                                show_update_user_dialog(user, token)
                        with btn_col2:
                            if st.button("🗑️ Delete", key=f"del_{user['id']}", use_container_width=True):
                                show_delete_user_dialog(user, token)
            else:
                st.info(f"No users found with role '{target_role}'.")
        elif response and response.status_code == 404:
            st.info(f"No users found matching role: '{target_role}'")
        elif response and response.status_code == 401:
            st.error("Session expired or unauthorized. Please sign in again.")
        else:
            st.error("Could not load users from backend.")
    else:
        st.warning("Please sign in to access the dashboard.")
        if st.button("Go to Sign In"):
            st.switch_page("views/sign_in.py")


show_dashboard()