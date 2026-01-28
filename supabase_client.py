# supabase_client.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("NEON_DB_URL")

conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
cursor = conn.cursor()

def execute_query(query, params=None):
    cursor.execute(query, params)
    if query.strip().lower().startswith("select"):
        return cursor.fetchall()
    else:
        conn.commit()
        return cursor.rowcount
