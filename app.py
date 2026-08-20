import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def load_internships_data():
    """
    Attempts to fetch live structured data from Supabase DB.
    Falls back gracefully to local data/internship.csv if DB table isn't ready.
    """
    # 1. Try loading from Supabase if credentials exist
    if SUPABASE_URL and SUPABASE_ANON_KEY:
        try:
            from supabase import create_client
            supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
            response = supabase.table("internships").select("*").execute()
            if response.data and len(response.data) > 0:
                df = pd.DataFrame(response.data)
                print(f"[SUPABASE] Loaded {len(df)} active internships directly from Supabase DB.")
                return prepare_dataframe(df)
        except Exception as e:
            print(f"[NOTE] Supabase fetch fallback to CSV: {e}")

    # 2. Local CSV fallback
    try:
        df = pd.read_csv('data/internship.csv')
        print(f"[CSV] Loaded {len(df)} internships from local CSV.")
        return prepare_dataframe(df)
    except FileNotFoundError:
        print("Error: 'internship.csv' not found.")
        return pd.DataFrame()

def prepare_dataframe(df):
    """Clean and standardize columns."""
    if 'stipend' in df.columns:
        df['stipend'] = df['stipend'].astype(str).str.replace('₹', '').str.replace('/month', '').str.replace(',', '').str.strip()
        df['stipend'] = pd.to_numeric(df['stipend'], errors='coerce').fillna(0).astype(int)
    
    if 'apply_link' not in df.columns:
        df['apply_link'] = df['internship_id'].apply(lambda x: f"https://pminternship.mca.gov.in/internship/{x}")
        
    df.dropna(subset=['required_skills'], inplace=True)
    df.fillna('', inplace=True)
    return df

# Initialize data and skills
internships_df = load_internships_data()

all_skills = set()
if not internships_df.empty and 'required_skills' in internships_df.columns:
    for skills_list in internships_df['required_skills'].astype(str).str.lower().str.split(','):
        if isinstance(skills_list, list):
            for skill in skills_list:
                if skill.strip():
                    all_skills.add(skill.strip())

# --- Scoring Weights for Accuracy ---
WEIGHT_SKILL = 15
WEIGHT_LOCATION = 10
WEIGHT_SECTOR = 5
WEIGHT_SKILL_PERCENTAGE = 10 

# --- Flexible Education Hierarchy ---
EDUCATION_LEVELS = {
    '10th pass': 0, '12th pass': 1, 'diploma': 2,
    'ba': 3, 'b.sc': 3, 'b.com': 3, 'bba': 3, 'b.tech': 3, 'b.design': 3, 'b.pharma': 3,
    'ma': 4, 'm.sc': 4, 'mba': 4, 'm.tech': 4, 'm.pharma': 4
}

@app.route('/')
def home():
    """Serves your main HTML page and passes the list of skills."""
    return render_template('index.html', all_skills=sorted(list(all_skills)))

@app.route('/recommend', methods=['POST'])
def recommend():
    """
    API endpoint that receives candidate data and returns recommendations.
    """
    # Dynamic reload to ensure up-to-date data without server restarts
    current_df = load_internships_data()
    if current_df.empty:
        return jsonify([])

    data = request.get_json() or {}
    
    # Extract candidate details
    user_qualification = data.get('qualification', '').lower()
    user_skills_str = data.get('skills', '').lower()
    user_sector = data.get('sector_interested', '').lower()
    user_location = data.get('location_interested', '').lower()
    
    # Filter user skills to only include skills that exist in our master list
    user_skills_list = [skill.strip() for skill in user_skills_str.split(',') if skill.strip()]
    valid_user_skills = set(skill for skill in user_skills_list if skill in all_skills)
    
    user_education_level = EDUCATION_LEVELS.get(user_qualification, -1)

    scored_internships = []

    for index, internship in current_df.iterrows():
        
        required_skills = set(skill.strip() for skill in str(internship['required_skills']).lower().split(',') if skill.strip())

        # If the user typed skills, but none of their valid skills match this internship, skip it.
        if user_skills_str and not valid_user_skills.intersection(required_skills):
            continue

        # Education Check
        required_education = str(internship.get('required_education', '')).lower()
        required_education_level = EDUCATION_LEVELS.get(required_education, 0)
        
        if user_education_level < required_education_level:
            continue

        current_score = 0
        
        # Location match score
        if user_location and user_location in str(internship.get('location', '')).lower():
            current_score += WEIGHT_LOCATION

        # Sector match score
        if user_sector and user_sector in str(internship.get('sector', '')).lower():
            current_score += WEIGHT_SECTOR
        
        # Skill match score
        if required_skills and valid_user_skills:
            matching_skills_count = len(valid_user_skills.intersection(required_skills))
            if matching_skills_count > 0:
                current_score += matching_skills_count * WEIGHT_SKILL
                skill_match_ratio = matching_skills_count / len(required_skills)
                current_score += skill_match_ratio * WEIGHT_SKILL_PERCENTAGE

        max_possible_score = 0
        if user_location:
            max_possible_score += WEIGHT_LOCATION
        if user_sector:
            max_possible_score += WEIGHT_SECTOR
        if len(required_skills) > 0:
            max_possible_score += (len(required_skills) * WEIGHT_SKILL) + WEIGHT_SKILL_PERCENTAGE
            
        # Avoid division by zero
        max_possible_score = max(max_possible_score, 1)

        if current_score > 0:
            internship_data = internship.to_dict()
            internship_data['score'] = current_score
            match_percentage = (current_score / max_possible_score) * 100
            
            # Cap at 100 just in case
            internship_data['match_percentage'] = min(round(match_percentage), 100)
            
            # Ensure apply_link fallback
            if not internship_data.get('apply_link'):
                internship_data['apply_link'] = f"https://pminternship.mca.gov.in/internship/{internship_data.get('internship_id')}"
            scored_internships.append(internship_data)

    # Rank
    sorted_internships = sorted(scored_internships, key=lambda x: x['match_percentage'], reverse=True)
    
    tier_1 = []
    tier_2 = []
    tier_3 = []
    
    for req in sorted_internships:
        if req['match_percentage'] >= 80:
            tier_1.append(req)
        elif req['match_percentage'] >= 45:
            tier_2.append(req)
        else:
            tier_3.append(req)

    return jsonify({
        "tier_1": tier_1[:10], # Top 10 perfect matches
        "tier_2": tier_2[:10], # Top 10 close matches
        "tier_3": tier_3[:10]  # Top 10 other options
    })

if __name__ == '__main__':
    app.run(debug=True)
