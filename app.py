from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import datetime  # Needed for today's date
from dotenv import load_dotenv  # ✅ Add this
import os  

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

load_dotenv()  # Load variables from .env file

API_KEY = os.getenv("API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ✅ CORRECT: Single definition of generate_ai_response()
def generate_ai_response(prompt):
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error from API: {response.text}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"

# 🎯 ROUTE: /generate-resume
@app.route("/generate-resume", methods=["POST"])
def generate_resume():
    data = request.json

    # Get form values
    name = data.get('name', '')
    email = data.get('email', '')
    phone = data.get('phone', '')
    location = data.get('location', '')
    dob = data.get('dob', '')
    summary = data.get('summary', '')
    education = data.get('education', '')
    qualification = data.get('qualification', '')
    skills = data.get('skills', '')
    hobbies = data.get('hobbies', '')

    # Build prompt
    prompt = (
        f"Create a detailed, professional resume for the following individual:\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"Location: {location}\n"
        f"Date of Birth: {dob}\n\n"
        f"Professional Summary:\n{summary}\n\n"
        f"Education:\n{education}\n\n"
        f"Qualification:\n{qualification}\n\n"
        f"Skills:\n{skills}\n\n"
        f"Hobbies:\n{hobbies}\n\n"
        f"Please format it like a modern resume with clear sections and bullet points."
    )

    result = generate_ai_response(prompt)
    return jsonify({"resume": result})


# 🎯 ROUTE: /generate-cover
@app.route("/generate-cover", methods=["POST"])
def generate_cover():
    data = request.json

    name = data.get('name', '')
    email = data.get('email', '')
    company = data.get('company', '')
    position = data.get('position', '')
    manager = data.get('manager', 'Hiring Manager')
    description = data.get('description', '')
    date = data.get('date', datetime.datetime.today().strftime('%B %d, %Y'))

    # Build prompt
    prompt = f"""
You are an AI that writes professional cover letters.

Generate a cover letter in a formal, structured format, including:
- Name & Email at the top
- Current date
- Hiring manager's name
- Company name
- Addressing with 'Dear Mr./Ms.'
- A clear 3-paragraph body: introduction, skills/experience, enthusiasm for the company
- A professional closing and signature

Use the following applicant details:

Name: {name}  
Email: {email}  
Date: {date}  
Hiring Manager: {manager}  
Company: {company}  
Position: {position}  
Job Description: {description}

Write only the cover letter. Keep it formal, concise, and professional.
"""

    result = generate_ai_response(prompt)
    return jsonify({"cover_letter": result})


# ✅ Start server
if __name__ == "__main__":
    app.run(debug=True)
