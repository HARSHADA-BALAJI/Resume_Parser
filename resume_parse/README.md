# 📄 Resume Matcher – AI-Powered Web App

This web application uses OpenAI’s GPT model to **match resumes against job descriptions**, generating:

- A **match score** (0–100)
- A detailed **natural language explanation**  
- Automatically updates a central **Excel sheet** for tracking

## 📁 Project Structure
resume_matcher_webapp/
│
├── app.py # Flask web backend
├── parser.py # File parsing (PDF/DOCX to text)
├── matcher.py # AI scoring logic (OpenAI)
├── excel_handler.py # Append results to Excel
├── config.py # Your OpenAI API key
│
├── templates/
│ ├── index.html # Homepage with upload forms
│ └── result.html # Match result display
│
├── static/
│ └── styles.css # Simple responsive CSS
│
├── uploads/ # Folder where uploaded files are stored
│
├── requirements.txt # All Python dependencies
└── README.md

### 1. Clone the Repo

```bash
git clone <your-repo-url>
cd resume_matcher_webapp

### 2. Install dependencies

pip install -r requirements.txt

### 3. Update API key on config.py 

OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"

### 4. Run using 
python app.py
Visit http://127.0.0.1:5000/ in your browser.

