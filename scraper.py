import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env")
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def clean_stipend(raw_stipend):
    """Converts raw stipend strings (e.g. '₹35000/month') into an integer."""
    if pd.isna(raw_stipend) or not raw_stipend:
        return 0
    stipend_str = str(raw_stipend).replace('₹', '').replace('/month', '').replace(',', '').strip()
    try:
        return int(float(stipend_str))
    except (ValueError, TypeError):
        return 0

def generate_apply_link(internship_id):
    """Generates direct PM Internship Scheme application URL."""
    clean_id = str(internship_id).strip()
    return f"https://pminternship.mca.gov.in/internship/{clean_id}"

def parse_unstructured_html(html_content):
    """
    Parses unstructured HTML string or webpage content and converts it 
    into clean structured dictionary records.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    structured_records = []
    
    # Target internship cards or rows
    cards = soup.find_all(['div', 'article'], class_=re.compile(r'(internship|job|card)', re.I))
    
    for idx, card in enumerate(cards):
        title = card.find(['h2', 'h3', 'h4'])
        company = card.find(class_=re.compile(r'(company|employer|org)', re.I))
        skills = card.find(class_=re.compile(r'(skill|tag|requirement)', re.I))
        location = card.find(class_=re.compile(r'(location|city|place)', re.I))
        stipend = card.find(class_=re.compile(r'(stipend|salary|pay)', re.I))
        link = card.find('a', href=True)
        
        record = {
            "internship_id": f"INT-SCRAPED-{idx+1:03d}",
            "company_name": company.get_text(strip=True) if company else "Featured Enterprise",
            "title": title.get_text(strip=True) if title else "Internship Opportunity",
            "sector": "Information Technology",
            "required_skills": skills.get_text(strip=True) if skills else "Python, Communication",
            "required_education": "Pursuing B.Tech / Graduation",
            "location": location.get_text(strip=True) if location else "Pan India",
            "stipend": clean_stipend(stipend.get_text(strip=True) if stipend else "15000"),
            "apply_link": link['href'] if link else "https://pminternship.mca.gov.in/login/"
        }
        structured_records.append(record)
        
    return structured_records

def load_and_structure_csv(csv_path="data/internship.csv"):
    """Reads existing CSV dataset, cleans it, and ensures all structured fields exist."""
    df = pd.read_csv(csv_path)
    
    # Ensure apply_link column exists
    if 'apply_link' not in df.columns:
        df['apply_link'] = df['internship_id'].apply(generate_apply_link)
        
    structured_records = []
    for _, row in df.iterrows():
        record = {
            "internship_id": str(row.get('internship_id', '')).strip(),
            "company_name": str(row.get('company_name', '')).strip(),
            "title": str(row.get('title', '')).strip(),
            "sector": str(row.get('sector', '')).strip(),
            "required_skills": str(row.get('required_skills', '')).strip(),
            "required_education": str(row.get('required_education', '')).strip(),
            "location": str(row.get('location', '')).strip(),
            "stipend": clean_stipend(row.get('stipend', 0)),
            "apply_link": str(row.get('apply_link', generate_apply_link(row.get('internship_id')))).strip()
        }
        structured_records.append(record)
        
    # Save back updated dataset to CSV
    updated_df = pd.DataFrame(structured_records)
    updated_df.to_csv(csv_path, index=False)
    print(f"[SUCCESS] Local CSV updated with structured data ({len(structured_records)} records).")
    return structured_records

def sync_to_supabase(records):
    """Upserts structured internship records into Supabase 'internships' table."""
    try:
        supabase = get_supabase_client()
        print(f"[SYNC] Syncing {len(records)} structured records to Supabase...")
        
        # Batch upsert in chunks of 50 to avoid request size payload limits
        chunk_size = 50
        for i in range(0, len(records), chunk_size):
            chunk = records[i:i + chunk_size]
            response = supabase.table("internships").upsert(chunk, on_conflict="internship_id").execute()
            
        print("[SUCCESS] Successfully populated Supabase database table 'internships'!")
        return True
    except Exception as e:
        print(f"[NOTE] Supabase Sync check: {e}")
        print("Ensure you have run 'supabase_schema.sql' in your Supabase SQL Editor to create the 'internships' table!")
        return False

def run_pipeline():
    print("=== Web Scraper & Supabase Data Structuring Engine ===")
    records = load_and_structure_csv()
    sync_to_supabase(records)
    print("=== Pipeline Complete ===")

if __name__ == "__main__":
    run_pipeline()
