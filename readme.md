# 💼 AI Doc Designer

AI Doc Designer is a smart web application designed to help users generate professional resumes and personalized cover letters using AI. Built using **Flask** for the backend and **HTML/CSS/JavaScript** for the frontend, this project simplifies the job application process by allowing users to input details via intuitive forms and receive polished, AI-generated documents.

---

## 📸 Screenshots

### 🧾 Resume Builder (Empty State)
![Resume Builder Interface](./screenshots/screenshot5.png)

### 🧾 Resume Builder (Filled Form)
![Filled Resume Form](./screenshots/screenshot4.png)

### 💌 Cover Letter Generator (Empty State)
![Cover Letter Empty Form](./screenshots/screenshot3.png)

### 💌 Cover Letter Generator (Filled Form)
![Cover Letter Filled Form](./screenshots/screenshot2.png)

### 📄 Generated Cover Letter Output
![Cover Letter Output](./screenshots/screenshot1.png)

---

## ✨ Features

- 📄 AI-generated **professional resume** with dynamic form inputs
- 💌 Personalized **cover letter** generator with a 3-paragraph formal structure
- ⏱ One-click **date fill** using a 'Set Today' button
- 🔄 **Tab-based** interface to switch between Resume and Cover Letter
- 🎯 **Live preview** of generated content on the same page

---

## 🛠 Tech Stack

| Frontend        | Backend        | AI/Services Used              |
|-----------------|----------------|-------------------------------|
| HTML, CSS, JS   | Python (Flask) | OpenRouter (GPT-3.5)          |
| Vanilla JS      | Flask-CORS     | `.env` for API key security   |
| Responsive UI   | RESTful APIs   | Requests, Python-Dotenv       |

---

## 📂 Project Structure

ai-doc-designer/
├── static/
│ └── style.css
├── templates/
│ └── Resume.html
├── app.py
├── .env
├── .gitignore
├── README.md
└── screenshots/
├── screenshot1.png (Generated Cover Letter)
├── screenshot2.png (Cover Letter Form Filled)
├── screenshot3.png (Cover Letter Form Empty)
├── screenshot4.png (Filled Resume Form)
└── screenshot5.png (Resume Builder Interface)

yaml
Copy
Edit

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-doc-designer.git
cd ai-doc-designer
2. Install Dependencies
bash
Copy
Edit
pip install flask flask-cors requests python-dotenv
3. Configure API Key
Create a .env file in the root directory:

env
Copy
Edit
API_KEY=your_openrouter_api_key_here
4. Run the Application
bash
Copy
Edit
python app.py
Then visit: http://127.0.0.1:5000

📤 API Endpoints
🔹 POST /generate-resume
Generates a professional resume from form inputs.

Example Request JSON:

json
Copy
Edit
{
  "name": "Sneha Verma",
  "email": "example@gmail.com",
  "phone": "1234567890",
  "location": "XYZ colony Prayagraj",
  "dob": "01/01/2001",
  "education": "B.Tech in CSE",
  "qualification": "12th UP board",
  "skills": "C, Java, HTML, CSS",
  "hobbies": "playing games",
  "summary": "Motivated and passionate about technology."
}
🔹 POST /generate-cover
Creates a cover letter using user inputs and GPT-3.5.

Example Request JSON:

json
Copy
Edit
{
  "name": "Sneha Verma",
  "email": "example@gmail.com",
  "company": "Microsoft",
  "position": "Software Engineer",
  "manager": "Rakesh",
  "description": "Excited to work in tech. 5 years of experience.",
  "date": "August 1, 2025"
}
🔮 Future Enhancements
📄 Export Resume and Cover Letter as PDF

🌐 Add multi-language support

🧠 Intelligent AI suggestions for sections

✏ Editable content with live preview refinements

🧪 Notes
Ensure your OpenRouter API key is active and secured in .env.

All data is processed locally via your own Flask backend.

Prompt customization for GPT is done in app.py.

🤝 Contributing
Pull requests are welcome!
For any major changes, open an issue first to discuss improvements.

📄 License
This project is licensed under the MIT License.

🙌 Acknowledgements
OpenRouter API

OpenAI GPT-3.5 Turbo

Flask

Inspired by modern AI-powered job application tools