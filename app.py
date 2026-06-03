from flask import Flask, jsonify, request
from flask_cors import CORS
import spacy
import fitz
import pytesseract
import re
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
    text_lower = text.lower() # FIX 1: Create a lowercase version of the full text
    doc = nlp(text)
    
    # FIX 2: Added brackets and quotes to the strip to catch skills hidden in parentheses
    tokens = set([token.text.lower().strip('-.,()[]{}"\'') for token in doc])
    
    found = set()
    normalized_tokens = set([normalize_skill(token) for token in tokens])

    for skill in SKILLS_DB:
        skill_lower = skill.lower() # Ensure database skill is perfectly lowercase
        skill_tokens = skill_lower.split()
        
        if len(skill_tokens) > 1:
            # FIX 3: Check against text_lower, NOT the original case-sensitive text!
            if skill_lower in text_lower:
                found.add(skill)
        else:
            if skill_lower in tokens or skill_lower in normalized_tokens:
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
    
    # 1. NEW WEIGHTS: 95% Skills / 5% Text Context
    # This guarantees a 100% skill match will score at least a 95%
    base_score = (0.05 * similarity) + (0.95 * skill_ratio * 100)
    
    # 2. ANTI-CHEAT LOGIC: Tweaked threshold
    # Lowered to 2.0 so short resumes survive, but pure copy-paste keyword dumps fail.
    if skill_ratio > 0.70 and similarity < 2.0:
        # Apply a flat 25 point penalty for pure keyword stuffing
        final_score = base_score - 25.0
        print("🚨 ANTI-CHEAT: Keyword stuffing detected (Low similarity relative to high skills). Penalty applied.")
    else:
        final_score = base_score
        
    # Ensure the score stays within human bounds (0 to 100)
    final_score = max(0.0, min(100.0, final_score))
    
    return round(final_score, 2)

def generate_roadmap(missing_skills):
    # 1. THE PERFECT MATCH CHECK
    # Return an empty dictionary instead of a list
    if not missing_skills:
        return {} 

    phases = [
        {"phase": "Phase 1: Basics", "skills": []},
        {"phase": "Phase 2: Intermediate", "skills": []},
        {"phase": "Phase 3: Advanced", "skills": []},
        {"phase": "Phase 4: Project & Practice", "skills": []}
    ]

    for i, skill in enumerate(missing_skills):
        phase_index = i % 4
        phases[phase_index]["skills"].append(skill)

    game_plan = {} # <-- Changed to a dictionary to match frontend expectations
    
    for phase in phases:
        # 2. THE EMPTY PHASE FILTER
        if not phase["skills"]:
            continue 

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

        # Save directly to the dictionary using the Phase name as the key
        game_plan[phase["phase"]] = phase_tasks 
        
    return game_plan

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
        
        # 💥 THE NEWLINE FIX
        job_desc = job_desc.replace('\n', ',')
        # 💥 THE COLLISION FIX: Uses Regex to safely replace without destroying capital letters for AWS/GCP
        job_desc = re.sub(r'(?i)version control systems', 'version control', job_desc)
        
        resume_text = extract_text(file)

        if not resume_text:
            return jsonify({
                "error": "UNREADABLE_PDF",
                "message": "We could not read text from this PDF, even after OCR."
            }), 400

        clean_resume = preprocess(resume_text)
        clean_jd = preprocess(job_desc.lower())

        # 1. Base Extraction from your Master Database
        resume_skills = extract_skills(clean_resume)
        jd_skills = extract_skills(clean_jd)

        # 💥 THE CURATED NOISE FILTER 💥
        NOISE_WORDS = {
            'developing', 'maintainability', 'testing', 'designers', 'scalable', 
            'dynamic', 'functional', 'debug', 'efficient', 'test', 'read', 
            'software engineering', 'experience', 'knowledge', 'understanding', 
            'ability', 'responsible', 'required', 'preferred', 'strong', 
            'excellent', 'proven', 'innovative', 'complex', 'solutions', 
            'fast-paced', 'environment', 'track record', 'demonstrated', 
            'working', 'skills', 'cross-functional', 'highly', 'motivated', 
            'seeking', 'join', 'team', 'lifecycle', 'practices'
        }

        # 💥 THE BULLETPROOF JD ADAPTER 💥
        # SCENARIO A: User typed a comma-separated list or vertical list (No sentences)
        if ',' in job_desc and '.' not in job_desc:
            raw_jd_list = [s.strip().lower() for s in job_desc.split(',')]
            for custom_skill in raw_jd_list:
                if len(custom_skill.split()) <= 3 and custom_skill not in NOISE_WORDS:
                    jd_skills.append(custom_skill)
                    
        # SCENARIO B: User pasted a full paragraph (Contains sentences)
        else:
            # We ignore commas so we don't catch adjectives. 
            # We use Regex to hunt for Tech Acronyms (e.g., AWS, GCP, CI/CD) and Tech Symbols (C++, C#)
            custom_tech = re.findall(r'\b[A-Z]{2,}(?:/[A-Z]{2,})?\b|\b[a-zA-Z]+[+#]+', job_desc)
            for tech in custom_tech:
                tech_lower = tech.lower()
                if tech_lower not in NOISE_WORDS:
                    jd_skills.append(tech_lower)

        # Clean duplicates and scrub noise words
        resume_skills = [s for s in list(set(resume_skills)) if s.lower() not in NOISE_WORDS]
        jd_skills = [s for s in list(set(jd_skills)) if s.lower() not in NOISE_WORDS]

        # 🛡️ THE SAFETY NET: Give the candidate credit!
        # If the adapter forced a custom skill into the JD, check if it exists in the resume text
        for skill in jd_skills:
            if skill not in resume_skills and skill in clean_resume:
                resume_skills.append(skill)

        # Calculate Matches
        matched_skills = list(set(resume_skills) & set(jd_skills))
        missing_skills = list(set(jd_skills) - set(resume_skills))

        similarity = compute_similarity(clean_resume, clean_jd)
        score = calculate_score(similarity, matched_skills, len(jd_skills))
        roadmap = generate_roadmap(missing_skills)
        
        is_perfect = len(missing_skills) == 0

        try:
            with open("server_logs.txt", "a") as log_file:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{current_time}] Resume Processed | Score: {score}%\n")
            print(f"📊 Analytics: Successfully logged {score}% to server_logs.txt")
        except Exception as log_error:
            print("Warning: Could not write to log file -", log_error)

        return jsonify({
            "match_score": score,
            "nailed_skills": matched_skills,
            "needs_work": missing_skills,
            "is_perfect_match": is_perfect,
            "game_plan": roadmap
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Something went wrong"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)