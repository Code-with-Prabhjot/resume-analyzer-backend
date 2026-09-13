from flask import request, jsonify, g
from . import v2_bp
from .middleware import validate_and_sanitize, generate_jwt
from .database import save_analysis_result, get_user_history_from_db, get_or_create_user, get_missing_skills_for_analysis
import uuid

# -----------------------------------------------------------------------------
# 0. Healthcheck / Ping
# -----------------------------------------------------------------------------
@v2_bp.route('/ping', methods=['GET'])
def ping():
    """
    Simple unauthenticated endpoint to wake up the Render free tier.
    """
    return jsonify({"status": "awake"}), 200

# -----------------------------------------------------------------------------
# Phase 4: In-Memory Caching
# -----------------------------------------------------------------------------
JD_CACHE = {}

# -----------------------------------------------------------------------------
# 1. Authentication & User Provisioning
# -----------------------------------------------------------------------------
@v2_bp.route('/users/auth', methods=['POST'])
@validate_and_sanitize()
def auth_user():
    """
    Validates OAuth token and provisions a new user or logs in an existing user.
    """
    data = request.get_json() or {}
    provider = data.get('provider')
    token = data.get('token')
    
    if not provider or not token:
        return jsonify({"error": "provider and token are required"}), 400

    user_id = get_or_create_user(provider, token)
    session_jwt = generate_jwt(user_id)

    return jsonify({
        "user_id": user_id,
        "session_jwt": session_jwt
    }), 200

# -----------------------------------------------------------------------------
# 2. Standardized Resume Analysis (Authenticated)
# -----------------------------------------------------------------------------
@v2_bp.route('/analyze', methods=['POST'])
@validate_and_sanitize()
def analyze_resume():
    """
    Ingests the resume and JD, scores it, generates the roadmap, and now automatically saves the result to the user's history.
    """
    import re
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    from app import (
        extract_text, 
        preprocess, 
        extract_skills, 
        calculate_score
    )
    from .roadmap import generate_hardened_roadmap

    if 'resume' not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({"error": "No file selected!"}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Invalid format. Please upload a .pdf file!"}), 400

    job_desc = request.form.get('job_description', '')
    if len(job_desc) > 15000:
        return jsonify({"error": "Job description exceeds maximum allowed length of 15,000 characters."}), 400

    target_branch = request.form.get('target_branch', '')

    try:
        job_desc = job_desc.replace('\n', ',')
        job_desc = re.sub(r'(?i)version control systems', 'version control', job_desc)
        
        resume_text = extract_text(file)
    
        if not resume_text:
            return jsonify({
                "error": "UNREADABLE_PDF",
                "message": "We could not read text from this PDF, even after OCR."
            }), 400
    
        cache_key = job_desc.strip().lower()
    
        if cache_key in JD_CACHE:
            cached_data = JD_CACHE[cache_key]
            jd_skills = list(cached_data['jd_skills'])
            vectorizer = cached_data['vectorizer']
            jd_vector = cached_data['jd_vector']
        else:
            clean_jd = preprocess(job_desc.lower())
            jd_skills = extract_skills(clean_jd)
    
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
    
            if ',' in job_desc and '.' not in job_desc:
                raw_jd_list = [s.strip().lower() for s in job_desc.split(',') if s.strip()]
                for custom_skill in raw_jd_list:
                    if len(custom_skill.split()) <= 3 and custom_skill not in NOISE_WORDS:
                        jd_skills.append(custom_skill)
            else:
                custom_tech = re.findall(r'\b[A-Z]{2,}(?:/[A-Z]{2,})?\b|\b[a-zA-Z]+[+#]+', job_desc)
                for tech in custom_tech:
                    tech_lower = tech.lower()
                    if tech_lower not in NOISE_WORDS:
                        jd_skills.append(tech_lower)
    
            jd_skills = [s for s in list(set(jd_skills)) if s.lower() not in NOISE_WORDS]
            
            vectorizer = TfidfVectorizer(stop_words='english')
            jd_vector = vectorizer.fit_transform([clean_jd])
            
            JD_CACHE[cache_key] = {
                'jd_skills': list(jd_skills),
                'vectorizer': vectorizer,
                'jd_vector': jd_vector
            }
    
        clean_resume = preprocess(resume_text)
        resume_skills = extract_skills(clean_resume)
    
        # Re-declare NOISE_WORDS to filter resume skills
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
        resume_skills = [s for s in list(set(resume_skills)) if s.lower() not in NOISE_WORDS]
    
        for skill in jd_skills:
            if skill not in resume_skills and skill in clean_resume:
                resume_skills.append(skill)
    
        matched_skills = list(set(resume_skills) & set(jd_skills))
        missing_skills = list(set(jd_skills) - set(resume_skills))
    
        # Compute similarity using the cached JD vectorizer
        if not clean_resume.strip():
            similarity = 0.0
        else:
            resume_vector = vectorizer.transform([clean_resume])
            score_sim = cosine_similarity(resume_vector, jd_vector)[0][0]
            similarity = round(score_sim * 100, 2)
    
        score = calculate_score(similarity, matched_skills, len(jd_skills))
        roadmap = generate_hardened_roadmap(missing_skills)
    
        analysis_id = str(uuid.uuid4())
        user_id = getattr(g, 'user_id', "default-test-user-id")
    
        analysis_data = {
            "analysis_id": analysis_id,
            "overall_score": score,
            "skills_found": matched_skills,
            "skills_missing": missing_skills,
            "roadmap": roadmap
        }
        
        save_analysis_result(user_id, analysis_data)
    
        return jsonify(analysis_data), 200

    except Exception as e:
        return jsonify({"error": "Resume analysis encountered an error.", "details": str(e)}), 500

# -----------------------------------------------------------------------------
# 3. Fetch User History
# -----------------------------------------------------------------------------
@v2_bp.route('/users/<user_id>/history', methods=['GET'])
@validate_and_sanitize()
def get_user_history(user_id):
    """
    Retrieves a chronological list of a user's past resume analyses for the frontend dashboard.
    """
    # Authorization header is checked in middleware

    history_records = get_user_history_from_db(user_id)
    
    # Calculate a simple trend delta (last score minus previous score) if enough data
    trend_delta = 0.0
    if len(history_records) >= 2:
        # Since they are ordered DESC by timestamp (newest first)
        trend_delta = history_records[0]['overall_score'] - history_records[1]['overall_score']

    return jsonify({
        "history": history_records,
        "trend_delta": round(trend_delta, 2)
    }), 200

# -----------------------------------------------------------------------------
# 4. AI Mock Interview Generator
# -----------------------------------------------------------------------------
@v2_bp.route('/interview/generate', methods=['POST'])
@validate_and_sanitize()
def generate_interview():
    """
    Takes the skills_missing array from a previous analysis and generates targeted interview practice questions.
    """
    data = request.get_json() or {}
    analysis_id = data.get('analysis_id')
    difficulty = data.get('difficulty', 'Beginner')

    if not analysis_id:
        return jsonify({"error": "analysis_id is required"}), 400

    skills_missing = get_missing_skills_for_analysis(analysis_id)
    if not skills_missing:
        # Default fallback for testing if no analysis exists
        skills_missing = ["Docker", "Kubernetes"]

    questions = []
    answers = []

    # Dynamically generate questions based on missing skills and difficulty
    for skill in skills_missing:
        if difficulty == "Hard":
            questions.append(f"Explain the most complex edge case you've encountered with {skill} and how you architected a solution.")
            answers.append(f"Focus on deep architectural tradeoffs, performance tuning, or multi-threading context in {skill}.")
        elif difficulty == "Intermediate":
            questions.append(f"How do you typically implement best practices for {skill} in a production environment?")
            answers.append(f"Discuss standard production setups, logging, and error handling for {skill}.")
        else:
            questions.append(f"What is {skill} and what primary problem does it solve in modern software development?")
            answers.append(f"Define {skill} and provide a basic use-case example.")
            
        if len(questions) >= 5:
            break
            
    # Pad if we have fewer than 5 questions
    while len(questions) < 5:
        questions.append("General: How do you approach learning a new technology related to your tech stack?")
        answers.append("Discuss reading documentation, building POCs, and reviewing source code.")
        
    return jsonify({
        "questions": questions[:5],
        "suggested_answers": answers[:5]
    }), 200
