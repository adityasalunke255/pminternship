import pandas as pd
import requests
import concurrent.futures

def check_link(row_tuple):
    index, row = row_tuple
    link = row['apply_link']
    try:
        # Use a realistic User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Only fetch headers to be faster
        response = requests.head(link, headers=headers, allow_redirects=True, timeout=5)
        
        # If head fails or returns 404, try GET just in case HEAD is blocked
        if response.status_code == 404 or response.status_code == 405:
            response = requests.get(link, headers=headers, timeout=5)
            
        if response.status_code == 200:
            return index, True
        else:
            return index, False
    except requests.RequestException:
        return index, False

def validate_csv(file_path):
    print(f"Reading {file_path}...")
    df = pd.read_csv(file_path)
    
    # Ensure apply_link exists
    if 'apply_link' not in df.columns:
        df['apply_link'] = df['internship_id'].apply(lambda x: f"https://pminternship.mca.gov.in/internship/{x}")
        
    print(f"Checking {len(df)} links...")
    
    valid_indices = []
    
    # Use ThreadPoolExecutor for concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(check_link, df.iterrows()))
        
    for index, is_valid in results:
        if is_valid:
            valid_indices.append(index)
            
    print(f"Found {len(valid_indices)} working links.")
    print(f"Found {len(df) - len(valid_indices)} broken links.")
    
    # Filter the dataframe to only keep valid links
    valid_df = df.loc[valid_indices].copy()
    
    # Let's add some guaranteed working data so the system isn't empty
    new_data = [
        {
            'internship_id': 'INT-TEST-001',
            'company_name': 'Tech Mahindra (Demo)',
            'title': 'Software Engineer Intern',
            'sector': 'Information Technology',
            'required_skills': 'Python, Java, HTML, CSS',
            'required_education': 'B.Tech',
            'location': 'Maharashtra',
            'stipend': 15000,
            'apply_link': 'https://pminternship.mca.gov.in/login/'
        },
        {
            'internship_id': 'INT-TEST-002',
            'company_name': 'TCS (Demo)',
            'title': 'Data Analyst Intern',
            'sector': 'Data Science & Analytics',
            'required_skills': 'SQL, Excel, Python',
            'required_education': 'B.Sc',
            'location': 'Delhi',
            'stipend': 20000,
            'apply_link': 'https://pminternship.mca.gov.in/login/'
        },
        {
            'internship_id': 'INT-TEST-003',
            'company_name': 'Reliance Retail (Demo)',
            'title': 'Marketing Intern',
            'sector': 'Marketing & Advertising',
            'required_skills': 'Communication, Social Media, SEO',
            'required_education': 'BBA',
            'location': 'Gujarat',
            'stipend': 12000,
            'apply_link': 'https://pminternship.mca.gov.in/login/'
        }
    ]
    
    # Append the guaranteed data
    new_df = pd.DataFrame(new_data)
    final_df = pd.concat([valid_df, new_df], ignore_index=True)
    
    print(f"Saving final dataset with {len(final_df)} rows...")
    final_df.to_csv(file_path, index=False)
    print("Done!")

if __name__ == "__main__":
    validate_csv("data/internship.csv")
