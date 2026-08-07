from flask import request, jsonify, g
from . import v2_bp
from .middleware import validate_and_sanitize, generate_jwt
from .database import save_analysis_result, get_user_history_from_db, get_or_create_user, get_missing_skills_for_analysis
import uuid

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
    # Expecting FormData
    resume_file = request.files.get('resume')
    job_description = request.form.get('job_description')
    target_branch = request.form.get('target_branch')

    # TODO: Implement resume parsing, TF-IDF scoring, gap analysis, and roadmap generation

    # For now, we use mock output but save it properly to the database
    analysis_id = str(uuid.uuid4())
    # Retrieve user_id from the validated JWT token in the Flask g context, fallback to mock if bypassed
    user_id = getattr(g, 'user_id', "default-test-user-id")

    analysis_data = {
        "analysis_id": analysis_id,
        "overall_score": 85.5,
        "skills_found": ["Python", "Flask", "Machine Learning"],
        "skills_missing": ["Docker", "Kubernetes", "Redis"],
        "roadmap": {
            "Docker": "https://example.com/course/docker",
            "Kubernetes": "https://example.com/course/k8s",
            "Redis": "https://example.com/course/redis"
        }
    }
    
    # Persist to database
    save_analysis_result(user_id, analysis_data)

    return jsonify(analysis_data), 200

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
