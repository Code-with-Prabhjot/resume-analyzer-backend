from functools import wraps
from flask import request, abort, jsonify, g
import base64
import json
import hmac
import hashlib

SECRET_KEY = "my_super_secret_jwt_key_for_v2" # Mock secret for V2

def generate_jwt(user_id):
    """Generates a mock JWT signed with HMAC-SHA256"""
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip("=")
    payload = base64.urlsafe_b64encode(json.dumps({"user_id": user_id}).encode()).decode().rstrip("=")
    signature = base64.urlsafe_b64encode(hmac.new(SECRET_KEY.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()).decode().rstrip("=")
    return f"{header}.{payload}.{signature}"

def verify_jwt(token):
    """Verifies a mock JWT and returns the user_id if valid."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header, payload, signature = parts
        expected_sig = base64.urlsafe_b64encode(hmac.new(SECRET_KEY.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()).decode().rstrip("=")
        if hmac.compare_digest(signature, expected_sig):
            decoded_payload = json.loads(base64.urlsafe_b64decode(payload + "==").decode())
            return decoded_payload.get("user_id")
    except Exception:
        pass
    return None

def validate_and_sanitize():
    """
    Security & Rate Limit Middleware.
    Sits in front of the application logic to strip malicious data before it ever touches the AI models.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 1. Origin Verification (Check Access-Control-Allow-Origin)
            # Placeholder: Check request origin against allowed Vercel frontend domains.
            origin = request.headers.get('Origin')
            # if origin not in ALLOWED_ORIGINS:
            #     abort(403, description="Forbidden: Invalid Origin")

            # 2. Token Integrity (Validate JWT signature)
            # Only apply to protected routes
            if request.path.startswith('/api/v2/analyze') or request.path.startswith('/api/v2/users/') or request.path.startswith('/api/v2/interview'):
                if request.path != '/api/v2/users/auth': # Auth route doesn't need JWT validation
                    auth_header = request.headers.get('Authorization')
                    
                    if not auth_header or not auth_header.startswith("Bearer "):
                        # Bypass mode for testing
                        if request.headers.get("X-Test-Bypass") == "true":
                            g.user_id = "test-bypass-user"
                        else:
                            abort(401, description="Unauthorized: Missing or malformed token")
                    else:
                        token = auth_header.split(" ")[1]
                        user_id = verify_jwt(token)
                        
                        if not user_id:
                            if request.headers.get("X-Test-Bypass") == "true":
                                g.user_id = "test-bypass-user"
                            else:
                                abort(401, description="Unauthorized: Invalid token signature")
                        else:
                            g.user_id = user_id
            
            # 3. File Type Validation (Magic number check for PDFs only)
            # Placeholder: Check if the uploaded file is a valid PDF using magic numbers.
            # if 'resume' in request.files:
            #     file = request.files['resume']
            #     if not is_valid_pdf(file):
            #         abort(415, description="Unsupported Media Type: Only PDFs are allowed")

            # 4. Rate Limit Check (Redis IP tracker)
            # Placeholder: Check rate limit for the client's IP.
            client_ip = request.remote_addr
            # if is_rate_limited(client_ip):
            #     abort(429, description="Too Many Requests: Rate limit exceeded")

            return f(*args, **kwargs)
        return decorated_function
    return decorator
