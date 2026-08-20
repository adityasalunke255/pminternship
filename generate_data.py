import pandas as pd
import random

# Core options matching app.py / index.html exact definitions
EDUCATION_LEVELS = [
    '10th Pass', '12th Pass', 'Diploma', 'B.Tech', 'M.Tech', 'BBA', 'MBA', 
    'B.Pharma', 'M.Pharma', 'B.Design', 'B.Sc', 'M.Sc', 'B.Com', 'BA', 'MA'
]

SECTORS = [
    'Information Technology', 'FinTech', 'Marketing & Advertising', 
    'Data Science & Analytics', 'Human Resources', 'E-commerce', 
    'EdTech', 'Healthcare', 'Design', 'Finance'
]

LOCATIONS = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 
    'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Delhi'
]

SKILLS_POOL = {
    'Information Technology': ['Python', 'Java', 'HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'SQL', 'Git', 'AWS', 'Docker'],
    'FinTech': ['Python', 'SQL', 'Excel', 'Financial Modeling', 'Data Analysis', 'Risk Management', 'Power BI'],
    'Marketing & Advertising': ['SEO', 'SEM', 'Google Analytics', 'Social Media Marketing', 'Content Creation', 'Facebook Ads', 'Canva'],
    'Data Science & Analytics': ['Python', 'R', 'SQL', 'Machine Learning', 'Pandas', 'NumPy', 'TensorFlow', 'Tableau'],
    'Human Resources': ['Recruitment', 'Employee Engagement', 'MS Office Suite', 'Interviewing', 'Communication', 'Sourcing'],
    'E-commerce': ['Inventory Management', 'Logistics', 'Excel', 'SQL', 'Market Research', 'CRM'],
    'EdTech': ['Content Writing', 'Curriculum Design', 'Video Editing', 'Communication', 'Subject Matter Expertise'],
    'Healthcare': ['Hospital Operations', 'Patient Care Coordination', 'MS Excel', 'Data Entry', 'Healthcare Management'],
    'Design': ['Figma', 'Adobe XD', 'User Research', 'Wireframing', 'Adobe Photoshop', 'Illustrator', 'Typography'],
    'Finance': ['Valuation', 'DCF', 'Mergers & Acquisitions', 'PowerPoint', 'Excel', 'Accounting', 'Tally']
}

COMPANIES = [
    "Nexus Technologies", "Capital Crest Finance", "BrandBoosters Inc.", "DataWeave Analytics", 
    "TalentSphere Consulting", "QuickCart Retail", "LearnWell EdTech", "CureFast Health", 
    "PixelPerfect Studios", "InvestRight Partners", "CodeGenius Labs", "PeopleFirst Corp",
    "GlobalBasket", "Innovate IO", "AdVantage Media", "QuantumLeap AI", "Tech Mahindra", 
    "TCS", "Infosys", "Wipro", "HDFC Bank", "ICICI Bank", "Reliance Retail", "Aditya Birla Group"
]

TITLES = {
    'Information Technology': ['Software Engineer Intern', 'Frontend Developer Intern', 'Backend Developer Intern', 'Cloud Computing Intern', 'Cybersecurity Intern'],
    'FinTech': ['Financial Analyst Intern', 'Risk Management Intern', 'Fintech Research Intern'],
    'Marketing & Advertising': ['Digital Marketing Intern', 'Social Media Intern', 'Graphic Design Intern', 'SEO Intern'],
    'Data Science & Analytics': ['Data Science Intern', 'Machine Learning Intern', 'Data Analyst Intern', 'AI Research Intern'],
    'Human Resources': ['Human Resources Intern', 'Talent Acquisition Intern', 'HR Operations Intern'],
    'E-commerce': ['Supply Chain Intern', 'Business Development Intern', 'E-commerce Operations Intern'],
    'EdTech': ['Content Development Intern', 'Instructional Design Intern', 'EdTech Strategy Intern'],
    'Healthcare': ['Healthcare Management Intern', 'Clinical Operations Intern', 'Health Informatics Intern'],
    'Design': ['UI/UX Design Intern', 'Product Design Intern', 'Visual Designer Intern'],
    'Finance': ['Investment Banking Intern', 'Finance Intern', 'Equity Research Intern']
}

data = []
for i in range(1, 151):
    sector = random.choice(SECTORS)
    title = random.choice(TITLES[sector])
    company = random.choice(COMPANIES)
    
    # Pick 3-5 random skills from that sector
    req_skills = random.sample(SKILLS_POOL[sector], random.randint(3, 5))
    
    # Assign appropriate education based on role loosely
    if 'Engineer' in title or 'Developer' in title:
        ed = random.choice(['B.Tech', 'M.Tech', 'Diploma', 'BCA'])
        if ed == 'BCA': ed = 'B.Sc' # map to exact dropdown
    elif 'Data' in title or 'AI' in title or 'Machine' in title:
        ed = random.choice(['B.Tech', 'M.Tech', 'B.Sc', 'M.Sc'])
    elif 'Finance' in title or 'Financial' in title or 'Banking' in title:
        ed = random.choice(['B.Com', 'MBA', 'BBA'])
    elif 'Design' in title:
        ed = random.choice(['B.Design', 'BA', 'Diploma'])
    else:
        ed = random.choice(EDUCATION_LEVELS)

    internship = {
        'internship_id': f"INT-{sector[:3].upper()}-25-{i:03d}",
        'company_name': company,
        'title': title,
        'sector': sector,
        'required_skills': ", ".join(req_skills),
        'required_education': ed,
        'location': random.choice(LOCATIONS),
        'stipend': random.randint(15000, 50000),
        'apply_link': 'https://pminternship.mca.gov.in/login/'
    }
    data.append(internship)

df = pd.DataFrame(data)
df.to_csv('data/internship.csv', index=False)
print(f"Successfully generated {len(df)} realistic internships with working links!")
