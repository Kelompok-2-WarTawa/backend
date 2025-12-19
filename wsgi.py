import os
from dotenv import load_dotenv
from src.app import init_app

load_dotenv()

DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise RuntimeError("DB_URL is not set")

settings = {
    "sqlalchemy.url": DB_URL
}

application = init_app(settings)
