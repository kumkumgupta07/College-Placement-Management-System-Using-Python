import os
import uuid
import gridfs
from datetime import datetime
from utils.database import get_db  # Ensure get_db() returns the DB, not client

ALLOWED_EXTENSIONS = ["pdf"]

# Generate unique filename
def generate_filename(original_name):
    ext = os.path.splitext(original_name)[-1]
    return f"{uuid.uuid4()}{ext}"

# Validate file type
def is_valid_file(uploaded_file):
    return uploaded_file.name.split('.')[-1].lower() in ALLOWED_EXTENSIONS

# Create logs
def create_log_entry(user_id, action):
    return {
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.utcnow()
    }

# Save uploaded file to MongoDB GridFS
def save_file_to_mongodb(uploaded_file, folder="resumes", metadata=None):
    db = get_db()
    fs = gridfs.GridFS(db, collection=folder)

    file_id = fs.put(
        uploaded_file.read(),
        filename=uploaded_file.name,
        content_type=uploaded_file.type,
        metadata=metadata or {},
        upload_date=datetime.utcnow()
    )
    return file_id
import json

def save_analysis_to_json(data, filename="ats_results.json"):
    try:
        with open(filename, "r") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing_data = []

    existing_data.append(data)

    with open(filename, "w") as f:
        json.dump(existing_data, f, indent=4)
