from functools import wraps
from flask import request, abort, jsonify, g
import jwt
import base64
import json
import hmac
import hashlib
import time
import os

SECRET_KEY = "my_super_secret_jwt_key_for_v2" # Mock secret for V2

# -----------------------------------------------------------------------------
# Rate Limiting State
# -----------------------------------------------------------------------------
IP_REQUESTS = {}

def is_rate_limited(ip):
    now = time.time()
    if ip not in IP_REQUESTS:
        IP_REQUESTS[ip] = []
    
    IP_REQUESTS[ip] = [t for t in IP_REQUESTS[ip] if now - t < 60]
    
    if len(IP_REQUESTS[ip]) >= 5:
        return True
    
    IP_REQUESTS[ip].append(now)
    return False

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
                    
                    if auth_header and auth_header.startswith("Bearer "):
                        token = auth_header.split(" ")[1]
                        secret = os.environ.get("SUPABASE_JWT_SECRET")
                        try:
                            header = jwt.get_unverified_header(token)
                            token_alg = header.get("alg", "HS256")
                            
                            if secret:
                                decoded_token = jwt.decode(token, key=secret, algorithms=[token_alg], options={"verify_aud": False})
                            else:
                                decoded_token = jwt.decode(token, algorithms=[token_alg], options={"verify_signature": False, "verify_aud": False})
                                
                            user_id = decoded_token.get("sub")
                            if not user_id:
                                return jsonify({"error": "Unauthorized", "message": "Missing 'sub' in token"}), 401
                            g.user_id = user_id
                        except Exception as e:
                            return jsonify({"error": "Unauthorized", "message": f"JWT Decode Error: {str(e)}"}), 401
                    else:
                        # Bypass mode for testing
                        if request.headers.get("X-Test-Bypass") == "true":
                            g.user_id = "test-bypass-user"
                        else:
                            return jsonify({"error": "Unauthorized", "message": "Missing or malformed token"}), 401
            
            # 3. File Type Validation (Magic number check for PDFs only)
            if 'resume' in request.files:
                file = request.files['resume']
                
                # 5MB Limit check
                file.seek(0, os.SEEK_END)
                size = file.tell()
                file.seek(0)
                if size > 5 * 1024 * 1024:
                    abort(413, description="Payload Too Large: File exceeds 5MB")
                
                # Magic bytes check for %PDF
                magic = file.read(4)
                file.seek(0)
                if magic != b'%PDF':
                    abort(415, description="Unsupported Media Type: Only PDFs are allowed")

            # 4. Rate Limit Check (In-memory IP tracker)
            if request.path == '/api/v2/analyze':
                client_ip = request.remote_addr or "unknown"
                if is_rate_limited(client_ip):
                    abort(429, description="Too Many Requests: Rate limit exceeded")

            return f(*args, **kwargs)
        return decorated_function
    return decorator
