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
    
   Use only information explicitly provided by the user. Never invent experience, education, dates, companies, skills, or achievements. If information is missing, use empty strings or empty arrays instead of making it up.
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
          else:
              raise ValueError("AI did not return valid resume JSON.")
            
        return resume_data
    except Exception as e:
    print(f"Error generating resume: {str(e)}")
    raise ValueError("Unable to generate resume. Please try again.")

def extract_resume_data_fallback(description):
    """
    Extract only information available in the user's description.
    Do not generate fictional personal or professional details.
    """
    data = {
        "fullName": "",
        "email": "",
        "phone": "",
        "location": "",
        "summary": description[:200] + "..." if len(description) > 200 else description,
        "experience": [],
        "education": [],
        "skills": [],
        "projects": [],
        "languages": [],
        "interests": []
    }

    name_match = re.search(
        r'(?:my name is|I am|name|i am:)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        description,
        re.IGNORECASE
    )
    if name_match:
        data["fullName"] = name_match.group(1)

    email_match = re.search(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        description
    )
    if email_match:
        data["email"] = email_match.group(0)

    phone_match = re.search(r'\+?[\d\s().-]{10,}', description)
    if phone_match:
        data["phone"] = phone_match.group(0).strip()

    linkedin_match = re.search(
        r'(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9-]+',
        description
    )
    if linkedin_match:
        data["linkedin"] = linkedin_match.group(0)
        if not data["linkedin"].startswith("http"):
            data["linkedin"] = "https://" + data["linkedin"]

    github_match = re.search(
        r'(https?://)?(www\.)?github\.com/[a-zA-Z0-9-]+',
        description
    )
    if github_match:
        data["github"] = github_match.group(0)
        if not data["github"].startswith("http"):
            data["github"] = "https://" + data["github"]

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
