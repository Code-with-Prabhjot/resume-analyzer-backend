from flask import Blueprint

v2_bp = Blueprint('api_v2', __name__, url_prefix='/api/v2')

# Import routes to register them with the blueprint
from . import routes
