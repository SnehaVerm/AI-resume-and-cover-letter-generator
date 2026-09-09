ResumeAI Generator

ResumeAI Generator is a full-stack web application that uses AI to generate professional resumes and cover letters from user-provided information. The project combines a Flask backend with a responsive HTML, CSS, and JavaScript frontend.

✨ Features

🤖 AI-powered resume generation

📝 AI-generated cover letters

📄 Structured resume output

🖨️ Resume preview and PDF export

🎨 Responsive and clean user interface

🌙 Light/Dark theme support

⚡ REST API powered by Flask

🔐 Environment-variable based API key configuration

📱 Works across desktop and mobile screens

🛠️ Tech Stack

Frontend

HTML5

CSS3

JavaScript (ES6)

jsPDF

html-to-image

Backend

Python

Flask

Flask-CORS

OpenAI API

python-dotenv

📁 Project Structure

ResumeAI-Generator/
│
├── Flask_App/
│   ├── app.py
│   ├── .env
│   └── requirements.txt
│
├── Frontend/
│   ├── resume-generator.html
│   ├── style.css
│   └── script.js
│
├── README.md
└── .gitignore

File and folder names may be different in your repository. Update the structure above if your actual project uses different names.

⚙️ How It Works

User enters resume details
          ↓
Frontend sends request to Flask API
          ↓
Flask processes the request
          ↓
OpenAI API generates resume/cover letter content
          ↓
Generated data is returned to frontend
          ↓
User previews the resume
          ↓
User can export the resume as PDF

🚀 Getting Started

1. Clone the repository

git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name

2. Create a virtual environment

python -m venv venv

Activate it:

Windows

venv\Scripts\activate

macOS/Linux

source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

If requirements.txt is inside Flask_App, run:

cd Flask_App
pip install -r requirements.txt

4. Configure the OpenAI API key

Create a .env file in the backend directory:

OPENAI_API_KEY=your_openai_api_key

Never commit your API key to GitHub.

Add this to .gitignore:

.env
venv/
__pycache__/
*.pyc

5. Run the Flask server

python app.py

The backend will normally run at:

http://127.0.0.1:5000

6. Open the frontend

Open the frontend HTML file in your browser, or serve the frontend through a local development server.

Make sure the frontend API URL matches the URL where your Flask backend is running.

🔌 API Endpoints

Generate Resume

POST /generate-resume

Generates structured resume content using the user's information.

Generate Cover Letter

POST /generate-cover-letter

Generates a personalized cover letter based on the provided information.

📄 Resume PDF Export

The frontend uses:

jsPDF for PDF creation

html-to-image for converting the resume preview into an image

This allows users to download their generated resume as a PDF.

🔒 Security

Store API keys in environment variables.

Do not upload .env files to GitHub.

Add .env to .gitignore.

Do not expose the OpenAI API key in frontend JavaScript.

Keep API requests that require the secret key on the backend.

🌐 Deployment

The application can be deployed using platforms that support Python/Flask applications.

For deployment:

Push the project to GitHub.

Create a web service on your preferred hosting platform.

Set the required environment variable:

OPENAI_API_KEY

Install dependencies using requirements.txt.

Start the Flask application using an appropriate production server.

Example:

gunicorn app:app

The exact start command depends on the location and name of your Flask application file.

🎯 Use Cases

ResumeAI Generator can help:

Students create professional resumes

Freshers prepare resumes for placements

Job seekers generate customized cover letters

Developers quickly create resume drafts

Applicants tailor their resume content for different job roles

🔮 Future Improvements

Multiple professional resume templates

ATS score checker

Resume keyword optimization

Job-description based resume customization

User authentication

Resume history and saved versions

More PDF customization options

Improved AI-generated formatting

Cloud database integration

👩‍💻 Author

Sneha Verma

B.Tech Computer Science & Engineering

⭐ Contributing

Contributions are welcome.

Fork the repository.

Create a new branch.

Make your changes.

Commit your changes.

Push the branch.

Open a Pull Request.

📜 License

This project is available for educational and personal use. Add a specific open-source license such as MIT if you intend to distribute the project under an open-source license.
