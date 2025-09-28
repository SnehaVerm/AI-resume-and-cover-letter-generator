from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os
import json
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_resume_from_description(description):
    """
    Use OpenAI to generate a structured resume from a description
    """
    prompt = f"""
    Based on the following professional description, generate a complete resume in JSON format with these fields:
    - fullName
    - email
    - phone
    - location
    - linkedin (optional)
    - github (optional)
    - portfolio (optional)
    - summary (professional summary)
    - experience (array of objects with title, company, duration, and description)
    - education (array of objects with degree, school, duration, and description)
    - skills (array of objects with name and level)
    - projects (array of objects with name, description, technologies, and link if available)
    - languages (array of objects with name and proficiency)
    - interests (array of strings)
    
    Here's the description:
    {description}
    
    For experience and education, include realistic durations and detailed descriptions.
    Return ONLY the JSON object, no additional text or explanation.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful resume assistant that generates structured resume data in JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # Extract the JSON from the response
        content = response.choices[0].message.content
        # Clean the response to extract only JSON
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            resume_data = json.loads(json_match.group())
        else:
            # If no JSON found, use fallback
            resume_data = extract_resume_data_fallback(description)
            
        return resume_data
    except Exception as e:
        print(f"Error generating resume: {str(e)}")
        # Fallback to simple parsing if OpenAI fails
        return extract_resume_data_fallback(description)

def extract_resume_data_fallback(description):
    """
    Fallback method to extract resume data if OpenAI API fails
    """
    # Simple parsing to extract information from the description
    data = {
        "fullName": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "location": "San Francisco, CA",
        "summary": description[:200] + "..." if len(description) > 200 else description,
        "experience": [],
        "education": [],
        "skills": [],
        "projects": [],
        "languages": [{"name": "English", "proficiency": "Fluent"}],
        "interests": ["Technology", "Software Development", "Learning"]
    }
    
    # Extract name
    name_match = re.search(r'(?:my name is|I am|name|i am:)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', description, re.IGNORECASE)
    if name_match:
        data["fullName"] = name_match.group(1)
    
    # Extract phone number
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4})', description)
    if phone_match:
        data["phone"] = phone_match.group(1)
    
    # Extract location
    location_match = re.search(r'(?:from|based in|located in|location:)\s+([A-Za-z\s]+(?:,\s*[A-Za-z\s]*)*)', description, re.IGNORECASE)
    if location_match:
        data["location"] = location_match.group(1).strip()
    
    # Extract LinkedIn URL
    linkedin_match = re.search(r'(https?://)?(www\.)?linkedin\.com/(in|company)/[a-zA-Z0-9-]+', description)
    if linkedin_match:
        data["linkedin"] = linkedin_match.group(0)
        if not data["linkedin"].startswith('http'):
            data["linkedin"] = 'https://' + data["linkedin"]
    
    # Extract GitHub URL
    github_match = re.search(r'(https?://)?(www\.)?github\.com/[a-zA-Z0-9-]+', description)
    if github_match:
        data["github"] = github_match.group(0)
        if not data["github"].startswith('http'):
            data["github"] = 'https://' + data["github"]
    
    # Extract portfolio URL
    portfolio_match = re.search(r'\b(?:portfolio|website):?\s*(https?://[^\s]+)', description, re.IGNORECASE)
    if not portfolio_match:
        portfolio_match = re.search(r'(https?://)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?', description)
        if portfolio_match and "linkedin" not in portfolio_match.group(0) and "github" not in portfolio_match.group(0):
            data["portfolio"] = portfolio_match.group(0)
            if not data["portfolio"].startswith('http'):
                data["portfolio"] = 'https://' + data["portfolio"]
    else:
        data["portfolio"] = portfolio_match.group(1)
    
    # Extract email
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', description)
    if email_match:
        data["email"] = email_match.group(0)
    
    # Extract skills based on common keywords
    skill_keywords = ["Java", "Spring Boot", "Microservices", "MySQL", "PostgreSQL", "MongoDB", 
                     "AWS", "Docker", "JavaScript", "Python", "React", "Node.js", "HTML", "CSS",
                     "Git", "REST API", "SQL", "NoSQL", "Cloud", "DevOps", "Agile", "Kubernetes",
                     "TensorFlow", "PyTorch", "Machine Learning", "AI", "Data Science", "Big Data",
                     "Spark", "Hadoop", "Kafka", "Redis", "Jenkins", "CI/CD", "Terraform", "Ansible"]
    
    for skill in skill_keywords:
        if skill.lower() in description.lower():
            data["skills"].append({"name": skill, "level": "Proficient"})
    
    # Extract experience information
    exp_years_match = re.search(r"(\d+)\s+years?\s+of\s+experience", description, re.IGNORECASE)
    years = exp_years_match.group(1) if exp_years_match else "3"
    
    # Generate experience based on description
    if any(word in description.lower() for word in ["software", "developer", "engineer", "programming"]):
        data["experience"].append({
            "title": "Software Engineer",
            "company": "Tech Solutions Inc.",
            "duration": f"Jan 202{int(years)-1} - Present",
            "description": "Developed and maintained software applications using modern technologies. Collaborated with cross-functional teams to deliver high-quality products."
        })
    
    if any(word in description.lower() for word in ["senior", "lead", "manager"]):
        data["experience"].append({
            "title": "Senior Developer",
            "company": "Previous Company",
            "duration": f"Mar 202{int(years)-3} - Dec 202{int(years)-1}",
            "description": "Led development teams and mentored junior developers. Designed system architecture and implemented best practices."
        })
    
    # Add default experience if none detected
    if not data["experience"]:
        data["experience"].append({
            "title": "Professional Role",
            "company": "Various Companies",
            "duration": f"2019 - Present",
            "description": "Gained valuable experience in relevant field. Developed key skills and contributed to various projects."
        })
    
    # Extract education information
    if any(word in description.lower() for word in ["master", "ms", "masters"]):
        data["education"].append({
            "degree": "Master of Science in Computer Science",
            "school": "University of Technology",
            "duration": "Sep 2019 - May 2021",
            "description": "Specialized in Advanced Computing. Thesis on innovative software solutions."
        })
    
    if any(word in description.lower() for word in ["bachelor", "bs", "ba", "undergraduate"]):
        data["education"].append({
            "degree": "Bachelor of Science in Computer Science",
            "school": "State University",
            "duration": "Aug 2015 - May 2019",
            "description": "Focused on software development fundamentals. Relevant coursework in algorithms and data structures."
        })
    
    # Add default education if none detected
    if not data["education"]:
        data["education"].append({
            "degree": "Bachelor's Degree in Relevant Field",
            "school": "University Name",
            "duration": "2015 - 2019",
            "description": "Completed comprehensive program with focus on practical applications."
        })
    
    # Extract potential job titles
    title_match = re.search(r"(?:am|is|as|role:?)\s+(a\s+|an\s+)?([A-Za-z\s]+)(?:developer|engineer|specialist|analyst|manager)", description, re.IGNORECASE)
    if title_match:
        title = title_match.group(2).strip()
        if not data["fullName"] or data["fullName"] == "John Doe":
            data["fullName"] = "John " + title  # Using a placeholder name
    
    # Add some default projects based on the description
    if any(word in description.lower() for word in ["management", "system", "application"]):
        data["projects"].append({
            "name": "Management System",
            "description": "Developed a comprehensive management system application",
            "technologies": "Java, Spring Boot, React",
            "link": ""
        })
    
    if any(word in description.lower() for word in ["web", "site", "portal"]):
        data["projects"].append({
            "name": "Web Application",
            "description": "Built a responsive web application with modern UI",
            "technologies": "JavaScript, HTML, CSS",
            "link": ""
        })
    
    if any(word in description.lower() for word in ["mobile", "app", "ios", "android"]):
        data["projects"].append({
            "name": "Mobile Application",
            "description": "Developed a cross-platform mobile application",
            "technologies": "React Native, Flutter, Kotlin",
            "link": ""
        })
    
    return data

def generate_cover_letter(data):
    """
    Use OpenAI to generate a professional cover letter based on the provided data
    """
    prompt = f"""
    Generate a professional cover letter based on the following information:
    
    Applicant Information:
    - Name: {data.get('fullName', '')}
    - Email: {data.get('email', '')}
    - Phone: {data.get('phone', '')}
    - Location: {data.get('location', '')}
    - LinkedIn: {data.get('linkedin', '')}
    
    Job Information:
    - Company: {data.get('companyName', '')}
    - Job Title: {data.get('jobTitle', '')}
    - Hiring Manager: {data.get('hiringManager', 'Hiring Manager')}
    - Key Skills/Requirements: {data.get('jobSkills', '')}
    
    Applicant's Strengths: {data.get('strengths', '')}
    Why Interested: {data.get('interest', '')}
    
    Please generate a professional, tailored cover letter that:
    1. Addresses the hiring manager appropriately
    2. Highlights the applicant's relevant skills and experience
    3. Explains why the applicant is interested in this specific role and company
    4. Is concise but compelling (around 3-4 paragraphs)
    5. Ends with a professional closing and signature
    
    Return ONLY the cover letter content, no additional text or explanation.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional career advisor that creates compelling, tailored cover letters."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating cover letter: {str(e)}")
        # Fallback to a simple cover letter template
        return generate_fallback_cover_letter(data)

def generate_fallback_cover_letter(data):
    """
    Fallback method to generate a cover letter if OpenAI API fails
    """
    salutation = f"Dear {data.get('hiringManager', 'Hiring Manager')},"
    
    cover_letter = f"""{salutation}

I am writing to express my enthusiastic interest in the {data.get('jobTitle', '')} position at {data.get('companyName', '')}, which I discovered through your company's website. 
With my background and proven track record of success, 
I am confident that I possess the skills and experience necessary to excel in this role and contribute significantly to your team.

{data.get('strengths', 'I have developed a strong skill set that aligns well with your requirements.')}

I have been following {data.get('companyName', 'your company')}'s progress in the industry, and I'm impressed by your innovative approach and market leadership. {data.get('interest', 'Your company values align perfectly with my professional philosophy.')}

I would welcome the opportunity to discuss how my experience and skills can benefit {data.get('companyName', 'your company')}. Thank you for considering my application. I have attached my resume for your review and look forward to the possibility of interviewing with you.

Sincerely,
{data.get('fullName', '')}
{data.get('email', '')} | {data.get('phone', '')} {data.get('linkedin', '')}
{data.get('location', '')}
"""
    
    return cover_letter

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    try:
        data = request.get_json()
        description = data.get('description')
        
        if not description:
            return jsonify({"error": "Description is required"}), 400
            
        resume_data = generate_resume_from_description(description)
        
        return jsonify(resume_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter_route():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['fullName', 'email', 'companyName', 'jobTitle']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400
                
        cover_letter = generate_cover_letter(data)
        
        return jsonify({"coverLetter": cover_letter})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Serve the resume generator page
@app.route('/resume-generator')
def serve_resume_generator():
    return send_from_directory('.', 'resume-generator.html')

# Serve the resume form page
@app.route('/resume-form')
def serve_resume_form():
    return send_from_directory('.', 'resume-form.html')

# Serve the cover letter page
@app.route('/coverletter')
def serve_cover_letter():
    return send_from_directory('.', 'coverletter.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
