import os
from supabase import create_client

URL = os.getenv("SUPABASE_URL", "").strip()
ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "").strip()
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()

def _client(key):
    if not URL or not key:
        raise RuntimeError("Supabase environment variables are not configured.")
    return create_client(URL, key)

def sign_up(email, password, username):
    return _client(ANON_KEY).auth.sign_up({"email": email, "password": password, "options": {"data": {"username": username}}})

def sign_in(email, password):
    return _client(ANON_KEY).auth.sign_in_with_password({"email": email, "password": password})

def admin_create_user(email, password, username, role):
    return _client(SERVICE_ROLE_KEY).auth.admin.create_user({"email": email, "password": password, "email_confirm": True, "user_metadata": {"username": username, "role": role}})

def admin_update_user(auth_user_id, attrs):
    return _client(SERVICE_ROLE_KEY).auth.admin.update_user_by_id(str(auth_user_id), attrs)

def admin_delete_user(auth_user_id):
    if auth_user_id:
        return _client(SERVICE_ROLE_KEY).auth.admin.delete_user(str(auth_user_id))
