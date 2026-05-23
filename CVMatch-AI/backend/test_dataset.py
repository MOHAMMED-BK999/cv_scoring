import os
import glob
import requests
from pathlib import Path
import time

BASE_URL = "http://localhost:8000/api/v1"
DATASET_DIR = Path("data/dataset")

def create_dummy_job():
    print("1. Creating a test job...")
    job_data = {
        "title": "Software Engineer (AI/Backend)",
        "department": "Engineering",
        "description": "We are looking for a Software Engineer experienced with Python, FastAPI, and Machine Learning (NLP, LLMs). You should have a minimum of 2 years of experience and be able to build robust APIs."
    }
    response = requests.post(f"{BASE_URL}/jobs", json=job_data)
    response.raise_for_status()
    job_id = response.json().get("id")
    print(f"   -> Job created with ID: {job_id}")
    return job_id

def create_job_from_category(category_name):
    print(f"Creating job for category: {category_name}...")
    job_data = {
        "title": category_name.replace("-", " ").title(),
        "department": "Various",
        "description": f"We are looking for a professional {category_name.replace('-', ' ').title()}. Must have relevant experience and skills matching the role."
    }
    response = requests.post(f"{BASE_URL}/jobs", json=job_data)
    response.raise_for_status()
    job_id = response.json().get("id")
    print(f"   -> Job created with ID: {job_id}")
    return job_id

def process_dataset():
    if not DATASET_DIR.exists():
        print(f"Directory {DATASET_DIR} does not exist. Creating it...")
        DATASET_DIR.mkdir(parents=True, exist_ok=True)
        print("Please put some PDF or DOCX files in 'backend/data/dataset' and run the script again.")
        return

    # Check for subdirectories (Kaggle dataset style)
    subdirs = [d for d in DATASET_DIR.iterdir() if d.is_dir()]
    
    if subdirs:
        print(f"Found {len(subdirs)} categories. Processing each category...")
        for subdir in subdirs:
            category_name = subdir.name
            job_id = create_job_from_category(category_name)
            
            files = []
            files.extend(subdir.glob("*.pdf"))
            files.extend(subdir.glob("*.docx"))
            
            if not files:
                print(f"   -> No CVs found in {category_name}.")
                continue
                
            print(f"   -> Found {len(files)} CVs in {category_name}. Uploading...")
            upload_cvs(job_id, files)
            get_job_scores(job_id)
    else:
        # Fallback to dummy job if it's just a flat folder
        job_id = create_dummy_job()
        files = []
        files.extend(DATASET_DIR.glob("*.pdf"))
        files.extend(DATASET_DIR.glob("*.docx"))

        if not files:
            print(f"No CVs found in {DATASET_DIR}. Please add some PDFs or DOCXs.")
            return

        print(f"2. Found {len(files)} CVs. Starting processing...")
        upload_cvs(job_id, files)
        get_job_scores(job_id)

def upload_cvs(job_id, files):
    for file_path in files[:5]: # Limiting to 5 per category for testing
        print(f"\nProcessing {file_path.name}...")
        with open(file_path, "rb") as f:
            files_payload = {"file": (file_path.name, f, "application/pdf" if file_path.suffix == ".pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            start_time = time.time()
            try:
                response = requests.post(f"{BASE_URL}/jobs/{job_id}/cvs/upload", files=files_payload)
                response.raise_for_status()
                duration = time.time() - start_time
                print(f"   -> Success! (Took {duration:.2f}s)")
            except requests.exceptions.RequestException as e:
                print(f"   -> Failed: {e}")
                if response is not None:
                    print(f"      Details: {response.text}")

def get_job_scores(job_id):
    print(f"\n3. Fetching final leaderboard for Job {job_id}...")
    response = requests.get(f"{BASE_URL}/jobs/{job_id}/scores")
    if response.status_code == 200:
        scores = response.json()
        print(f"\n--- LEADERBOARD (Top Candidates) ---")
        for i, score in enumerate(scores):
            print(f"{i+1}. Score ID {score.get('id')} | Global Score: {score.get('global_score')}/100 | Details: {score}")
    else:
        print(f"Failed to fetch scores: {response.text}")

if __name__ == "__main__":
    try:
        requests.get(f"{BASE_URL}/health")
    except requests.exceptions.ConnectionError:
        print("API is down! Please start FastAPI with: uvicorn app.main:app --reload")
        exit(1)
        
    process_dataset()
