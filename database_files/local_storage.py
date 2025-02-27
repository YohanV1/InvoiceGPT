import os
import shutil
import streamlit as st
from pathlib import Path

UPLOAD_DIR = "uploaded_invoices"

def ensure_upload_directory(user_email):
    """Ensure user-specific upload directory exists"""
    user_dir = os.path.join(UPLOAD_DIR, user_email)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def upload_file(file_object, filename, user_email):
    """Upload file to local storage"""
    try:
        user_dir = ensure_upload_directory(user_email)
        file_path = os.path.join(user_dir, filename)
        
        # Save the file
        with open(file_path, 'wb') as f:
            f.write(file_object.read() if isinstance(file_object, bytes) else file_object.getvalue())
        
        return f"{user_email}/{filename}"
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

def get_file(file_path):
    """Get file from local storage"""
    try:
        full_path = os.path.join(UPLOAD_DIR, file_path)
        with open(full_path, 'rb') as f:
            return f.read()
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

def delete_file(file_path):
    """Delete file from local storage"""
    try:
        full_path = os.path.join(UPLOAD_DIR, file_path)
        os.remove(full_path)
        return True
    except Exception as e:
        st.error(f"Error deleting file: {e}")
        return False

def list_user_files(user_email):
    """List all files for a user"""
    user_dir = os.path.join(UPLOAD_DIR, user_email)
    if not os.path.exists(user_dir):
        return []
    
    files = []
    for filename in os.listdir(user_dir):
        file_path = os.path.join(user_dir, filename)
        files.append({
            'Key': f"{user_email}/{filename}",
            'LastModified': os.path.getmtime(file_path)
        })
    return files

def remove_user_files(user_email):
    """Remove all files for a user"""
    user_dir = os.path.join(UPLOAD_DIR, user_email)
    if os.path.exists(user_dir):
        shutil.rmtree(user_dir)
