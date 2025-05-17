from flask import Flask, render_template, request, redirect, url_for, flash
from parser import extract_text
from matcher import get_match_score_and_explanation
from excel_handler import append_to_excel
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # for flashing messages

# Store current JD text globally (simple approach)
current_jd_text = None
current_jd_filename = None

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_jd_text, current_jd_filename
    if request.method == 'POST':
        if 'jd_file' in request.files:
            jd_file = request.files['jd_file']
            if jd_file and allowed_file(jd_file.filename):
                jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_file.filename)
                jd_file.save(jd_path)
                try:
                    current_jd_text = extract_text(jd_path)
                    current_jd_filename = jd_file.filename
                    flash(f"Job Description '{jd_file.filename}' uploaded successfully.", "success")
                except Exception as e:
                    flash(f"Failed to process JD: {e}", "danger")
            else:
                flash("Invalid JD file. Please upload a PDF or DOCX.", "danger")
        return redirect(url_for('index'))
    return render_template('index.html', jd_filename=current_jd_filename)

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    global current_jd_text, current_jd_filename
    if current_jd_text is None:
        flash("Please upload a Job Description file first.", "warning")
        return redirect(url_for('index'))

    if 'resume_file' not in request.files:
        flash("No resume file part", "danger")
        return redirect(url_for('index'))

    resume_file = request.files['resume_file']
    if resume_file.filename == '':
        flash("No selected file", "danger")
        return redirect(url_for('index'))

    if resume_file and allowed_file(resume_file.filename):
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
        resume_file.save(resume_path)
        try:
            resume_text = extract_text(resume_path)
            score, explanation = get_match_score_and_explanation(resume_text, current_jd_text)
            if score is None:
                flash("Failed to parse score from OpenAI response. See logs.", "warning")
                score = 0
                explanation = "Could not extract structured score from AI response."
            append_to_excel({
                'Resume': resume_file.filename,
                'Job Description': current_jd_filename or "Uploaded JD",
                'Score': score,
                'Explanation': explanation
            })
            return render_template('result.html',
                                   score=score,
                                   explanation=explanation,
                                   resume_filename=resume_file.filename,
                                   jd_filename=current_jd_filename)
        except Exception as e:
            flash(f"Error processing resume: {e}", "danger")
            return redirect(url_for('index'))
    else:
        flash("Invalid resume file type. Only PDF and DOCX are allowed.", "danger")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

