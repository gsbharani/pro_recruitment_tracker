import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("NEON_DB_URL")

def get_conn():
    return psycopg2.connect(DB_URL)

def execute_query(query, params=None, fetch=False):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params or ())
    if fetch:
        result = cur.fetchall()
    else:
        result = None
    conn.commit()
    cur.close()
    conn.close()
    return result
