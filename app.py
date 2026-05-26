from flask import Flask, jsonify, request
from flask_cors import CORS
import spacy
import fitz
import pytesseract
from pdf2image import convert_from_bytes
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from datetime import datetime
from utils import SKILLS_DB, normalize_skill

app = Flask(__name__)
CORS(app, origins=[
    "https://resume-analyzer-frontend-gold.vercel.app", 
    "http://localhost:3000",
    "http://localhost:5173" 
])

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Windows Tesseract path
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

try:
    with open('career_database.json', 'r') as db_file:
        CAREER_DB = json.load(db_file)
        print("SUCCESS: Career Database loaded into memory!")
except Exception as e:
    print("WARNING: Could not load career_database.json (Create this file if you haven't yet!)")

nlp = spacy.load("en_core_web_sm")


def extract_text(file):
    try:
        file_bytes = file.read()

        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""

        for page in doc:
            text += page.get_text()

        if text.strip():
            print("✅ Normal PDF text extraction successful")
            return text.lower()

        print("⚠️ No selectable text found. Starting OCR fallback...")

        images = convert_from_bytes(file_bytes)

        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img)

        if ocr_text.strip():
            print("✅ OCR extraction successful")
            return ocr_text.lower()

        print("❌ OCR also failed. PDF may be blank or unreadable.")
        return ""

    except Exception as e:
        print(f"🚨 PDF EXTRACTION CRASHED: {str(e)}")
        return ""

def preprocess(text):
    text = text.replace('/', ' / ')
    doc = nlp(text.lower())
    
    cleaned = [
        token.text for token in doc
        if not token.is_stop and token.text not in ['\n', ',', ':']
    ]
    return " ".join(cleaned)

def extract_skills(text):
    doc = nlp(text)
    
    tokens = set([token.text.lower().strip('-.,') for token in doc])
    
    found = set()
    normalized_tokens = set([normalize_skill(token) for token in tokens])

    for skill in SKILLS_DB:
        skill_tokens = skill.lower().split()
        if len(skill_tokens) > 1:
            if skill in text:
                found.add(skill)
        else:
            if skill in tokens or skill in normalized_tokens:
                found.add(skill)
    return list(found)

def compute_similarity(resume, jd):
    if not resume.strip() or not jd.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume, jd])
    score = cosine_similarity(vectors)[0][1]
    return round(score * 100, 2)

def calculate_score(similarity, matched, total_required):
    if total_required == 0:
        return round(similarity, 2)
        
    skill_ratio = len(matched) / total_required
    
    # 1. Use highly tuned weights (85% Skills / 15% Text Context)
    base_score = (0.15 * similarity) + (0.85 * skill_ratio * 100)
    
    # 2. ANTI-CHEAT LOGIC: Detect plain text keyword stuffing
    # If they match skills but text similarity is under 10%, they are cheating
    if skill_ratio > 0.70 and similarity < 10.0:
        # Apply a flat 25 point penalty for lack of context/experience
        final_score = base_score - 25.0
        print("🚨 ANTI-CHEAT: Keyword stuffing detected (Low similarity relative to high skills). Penalty applied.")
    else:
        final_score = base_score
        
    # Ensure the score stays within human bounds (0 to 100)
    final_score = max(0.0, min(100.0, final_score))
    
    return round(final_score, 2)

def generate_roadmap(missing_skills):
    phases = [
        # --- PHASE 1 HEADING UPDATED HERE ---
        {"phase": "Phase 1: Basics", "skills": []},
        {"phase": "Phase 2: Intermediate", "skills": []},
        {"phase": "Phase 3: Advanced", "skills": []},
        {"phase": "Phase 4: Project & Practice", "skills": []}
    ]

    for i, skill in enumerate(missing_skills):
        phase_index = i % 4
        phases[phase_index]["skills"].append(skill)

    roadmap = []
    for phase in phases:
        phase_tasks = []
        
        for skill in phase["skills"]:
            links = {
                "youtube": "https://www.youtube.com/results?search_query=" + skill.replace(" ", "+"),
                "course": "https://www.coursera.org/search?query=" + skill.replace(" ", "+"),
                "reading": "https://www.google.com/search?q=" + skill.replace(" ", "+")
            }
            
            for branch, branch_skills in CAREER_DB.items():
                if skill in branch_skills:
                    links["youtube"] = branch_skills[skill].get("youtube", links["youtube"])
                    links["course"] = branch_skills[skill].get("course", links["course"])
                    links["reading"] = branch_skills[skill].get("reading", links["reading"])
                    break 
            
            phase_tasks.append({
                "skill_name": f"Learn {skill.title()}",
                "links": links
            })

        roadmap.append({
            "phase": phase["phase"],
            "tasks": [f"Learn {skill.title()}" for skill in phase["skills"]],
            "resources": "YouTube / Official Docs / Practice Platforms",
            "detailed_tasks": phase_tasks 
        })
        
    return roadmap

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        if 'resume' not in request.files:
            return jsonify({"error": "No resume uploaded"}), 400

        file = request.files['resume']

        if file.filename == '':
            return jsonify({"error": "No file selected!"}), 400

        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Invalid format. Please upload a .pdf file!"}), 400

        job_desc = request.form.get('jobDescription', '')
        resume_text = extract_text(file)

        if not resume_text:
            print("🛡️ BOUNCER: Blocked unreadable/image-based PDF.")
            return jsonify({
                "error": "UNREADABLE_PDF",
                "message": "We could not read text from this PDF, even after OCR. Please upload a clearer PDF or a text-based PDF."
            }), 400

        clean_resume = preprocess(resume_text)
        clean_jd = preprocess(job_desc.lower())

        resume_skills = extract_skills(clean_resume)
        jd_skills = extract_skills(clean_jd)

        matched_skills = list(set(resume_skills) & set(jd_skills))
        missing_skills = list(set(jd_skills) - set(resume_skills))

        similarity = compute_similarity(clean_resume, clean_jd)
        score = calculate_score(similarity, matched_skills, len(jd_skills))
        roadmap = generate_roadmap(missing_skills)

        try:
            with open("server_logs.txt", "a") as log_file:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{current_time}] Resume Processed | Score: {score}%\n")
            print(f"📊 Analytics: Successfully logged {score}% to server_logs.txt")
        except Exception as log_error:
            print("Warning: Could not write to log file -", log_error)

        return jsonify({
            "score": score,
            "matchedSkills": matched_skills,
            "missingSkills": missing_skills,
            "roadmap": roadmap
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Something went wrong"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)