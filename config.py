# config.py
# Loads secrets from environment (.env) so nothing sensitive is in code.

import os
from dotenv import load_dotenv

load_dotenv()  # reads .env in project root

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI is not set. Create a .env file in the project root with:\n"
        "MONGO_URI=mongodb+srv://<username>:<password>@<cluster-host>/<db>?retryWrites=true&w=majority&appName=<app>"
    )
