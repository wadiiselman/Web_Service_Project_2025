import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_cors import CORS
from sqlalchemy.orm import DeclarativeBase
from datetime import timedelta
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

# Base model class
class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.update(
        SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', 'dev-key-change-in-production'),
        SQLALCHEMY_DATABASE_URI='postgresql://postgres:wadiiwadii@localhost:5432/HotelApi',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ENGINE_OPTIONS={
            "pool_recycle": 300,
            "pool_pre_ping": True,
        },
        API_SPEC_OPTIONS={
            'security': [{"bearerAuth": []}],
            'components': {
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            }
        },
        # JWT Configuration
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production'),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),
        JWT_ALGORITHM="HS256",
        JWT_DECODE_ALGORITHMS=["HS256"],
        # API Documentation
        API_TITLE="Tunisia Tourism API",
        API_VERSION="v1",
        OPENAPI_VERSION="3.0.2",
        OPENAPI_JSON_PATH="/api-spec",
        OPENAPI_URL_PREFIX="/",
        OPENAPI_SWAGGER_UI_PATH="/api/docs",
        OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        # Enable CORS for development
        CORS_ORIGINS="*"
    )

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Initialize Flask-Smorest API
    api = Api(app)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        from models import User
        return User.query.get(int(id))

    with app.app_context():
        # Import models to ensure they are registered
        from models import User, Hotel, Restaurant, Activity, Transportation, Business

        # Import blueprints
        from routes.main import blp as main_blp
        from routes.auth import web_blp as auth_web_blp, api_blp as auth_api
        from routes.hotel import web_blp as hotel_web_blp, api_blp as hotel_api
        from routes.restaurant import blp as restaurant_api
        from routes.activity import blp as activity_api
        from routes.transportation import blp as transportation_api
        from routes.business import blp as business_api

        # Register web blueprints
        app.register_blueprint(main_blp)
        app.register_blueprint(auth_web_blp)
        app.register_blueprint(hotel_web_blp)

        # Register API blueprints
        api.register_blueprint(auth_api)
        api.register_blueprint(hotel_api)
        api.register_blueprint(restaurant_api)
        api.register_blueprint(activity_api)
        api.register_blueprint(transportation_api)
        api.register_blueprint(business_api)

        # Create tables if not existing
        db.create_all()

    return app