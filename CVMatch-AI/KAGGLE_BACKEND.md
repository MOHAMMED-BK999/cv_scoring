# Run Backend On Kaggle, Frontend Locally

## 1. Upload the backend to Kaggle

Add this project folder to Kaggle as a Dataset, or clone/copy it into `/kaggle/working/CVMatch-AI`.

## 2. Add your ngrok token safely

In Kaggle, add a Secret named:

```text
NGROK_AUTHTOKEN
```

Do not hardcode the token in the notebook.

## 3. Add your Neon database safely

Use Neon PostgreSQL for all application data and vector storage. In Kaggle, add
a Secret named:

```text
DATABASE_URL
```

Example Neon format:

```text
postgresql://USER:PASSWORD@HOST/DB_NAME?sslmode=require
```

Do not hardcode the real database password in the notebook.

## 4. Start the backend in a Kaggle notebook

If your project is in `/kaggle/working/CVMatch-AI`, run:

```python
%cd /kaggle/working/CVMatch-AI/backend
!pip install -q -r requirements-kaggle.txt

import os
from kaggle_secrets import UserSecretsClient

os.environ["DATABASE_URL"] = UserSecretsClient().get_secret("DATABASE_URL")
os.environ["AUTO_CREATE_TABLES"] = "1"

import psycopg2

conn = psycopg2.connect(os.environ["DATABASE_URL"])
conn.autocommit = True
with conn.cursor() as cur:
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
conn.close()

!alembic upgrade head
!python seed_db.py
!python kaggle_runner.py
```

With Neon configured, all tables are stored in Neon, including these pgvector columns:

```text
job_descriptions.embedding_vector vector(768)
candidate_profiles.embedding_vector vector(768)
```

The runner prints a public URL and a line like:

```text
VITE_API_BASE_URL=https://xxxx.ngrok-free.app
```

## 5. Point the local frontend to Kaggle

On your local machine, edit:

```text
frontend/.env.local
```

Put the URL from Kaggle:

```text
VITE_API_BASE_URL=https://xxxx.ngrok-free.app
```

Then restart the local frontend:

```powershell
cd C:\Users\DELL\OneDrive\Desktop\test\CVMatch-AI
npm --prefix frontend run dev
```

Open the local frontend at:

```text
http://127.0.0.1:5173
```

## Optional: enable Ollama LLM scoring on Kaggle

The backend works without Ollama by using local fallback extraction and scoring. For full LLM parsing/scoring, run this before `!python kaggle_runner.py`:

```python
import os
import subprocess
import time

os.environ["OLLAMA_MODEL"] = "llama3:8b"
!curl -fsSL https://ollama.com/install.sh | sh
subprocess.Popen(["ollama", "serve"])
time.sleep(10)
!ollama pull llama3:8b
```

Keep the Kaggle notebook cell running while your local frontend is using the API.

## Optional: enable Docling document parsing

The Kaggle requirements are intentionally light to avoid dependency conflicts with Kaggle's preinstalled packages. PDF parsing still works through PyMuPDF. If you need Docling/DOCX parsing, install it separately:

```python
!pip install -q docling pymupdf4llm
```
