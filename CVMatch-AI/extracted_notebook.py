!apt-get update -y
!apt-get install -y zstd


# --- CELL ---

!curl -fsSL https://ollama.com/install.sh | sh


# --- CELL ---

import subprocess
import time

ollama_process = subprocess.Popen(["ollama", "serve"])
time.sleep(10)


# --- CELL ---

# llama3:8b is stronger but heavier. If Kaggle RAM is limited, use tinyllama instead.
!ollama pull llama3:8b


# --- CELL ---

import os
os.environ["OLLAMA_MODEL"] = "llama3:8b"

!ollama run llama3:8b "Say hello"


# --- CELL ---

!cp -r /kaggle/input/datasets/mohammedbarik/backend-final-v1/backend/kaggle/working
%cd /kaggle/input/datasets/mohammedbarik/backend-final-v1/backend/requirements-kaggle.txt
!pip install -q -r requirements-kaggle.txt


# --- CELL ---

# Use Neon PostgreSQL from Kaggle Secrets.
# In Kaggle: Add-ons > Secrets > add DATABASE_URL with your Neon URL:
# postgresql://neondb_owner:...@ep-calm-base-ap5dy0o7-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
#
# Do not hardcode the database password directly in this notebook.
import os
from kaggle_secrets import UserSecretsClient

os.environ["DATABASE_URL"] = UserSecretsClient().get_secret("DATABASE_URL")
print("DATABASE_URL loaded from Kaggle Secrets")
db_url = os.environ["DATABASE_URL"]
print(db_url[:25])
print(db_url.startswith("postgresql://"))
print(len(db_url))

# --- CELL ---

# Optional Supabase format, only if you decide not to use Neon.
# Replace [YOUR-PASSWORD] in Supabase, then save it as DATABASE_URL in Kaggle Secrets.
# postgresql://postgres:[YOUR-PASSWORD]@db.qnclrgszwhytysrwsput.supabase.co:5432/postgres?sslmode=require


# --- CELL ---

import os
import psycopg2

conn = psycopg2.connect(os.environ["DATABASE_URL"])
conn.autocommit = True

with conn.cursor() as cur:
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

conn.close()
print("pgvector extension enabled")


# --- CELL ---

# Fix existing Neon scoring columns if they were created by an older migration.
# This is safe to run multiple times.
import os
import psycopg2

conn = psycopg2.connect(os.environ["DATABASE_URL"])
conn.autocommit = True

with conn.cursor() as cur:
    cur.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_name = 'scoring_results'
            ) THEN
                ALTER TABLE scoring_results
                ALTER COLUMN semantic_score TYPE NUMERIC(5,2),
                ALTER COLUMN skills_score TYPE NUMERIC(5,2),
                ALTER COLUMN experience_score TYPE NUMERIC(5,2),
                ALTER COLUMN education_score TYPE NUMERIC(5,2);
            END IF;
        END $$;
    """)

conn.close()
print("Score columns ready")


# --- CELL ---

%cd /kaggle/working/backend
!alembic upgrade head
!python seed_db.py
!python kaggle_runner.py
