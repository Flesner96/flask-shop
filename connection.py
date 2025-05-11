from psycopg2 import connect, OperationalError
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Settings from environment variables
settings = {
    'host': 'localhost',
    'database': 'flask_shop',
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': '5432'
}

def connect_to_db():
    try:
        connection = connect(**settings)
        print("✅ Connected to database.")
        return connection
    except OperationalError as e:
        print("❌ Connection failed:", e)
        return None
