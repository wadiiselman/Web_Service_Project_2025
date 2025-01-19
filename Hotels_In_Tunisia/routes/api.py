from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import Hotel, Restaurant, Activity, Transportation, db
from functools import wraps
from routes.hotel_routes import hotel_bp
from routes.restaurant_routes import restaurant_bp
from routes.activity_routes import activity_bp
from routes.transportation_routes import transport_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                return jsonify({'error': 'Unauthorized'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Register all API route blueprints
api_bp.register_blueprint(hotel_bp)
api_bp.register_blueprint(restaurant_bp)
api_bp.register_blueprint(activity_bp)
api_bp.register_blueprint(transport_bp)