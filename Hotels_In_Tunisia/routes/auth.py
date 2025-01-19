from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask import render_template, redirect, url_for, request, flash, Blueprint as FlaskBlueprint
from schemas import UserSchema
from models import User
from app import db  # Import db from app instead of models

# Web routes blueprint
web_blp = FlaskBlueprint("auth", __name__, url_prefix="/auth")

# API routes blueprint
api_blp = Blueprint(
    "Auth", "auth_api",
    description="Authentication operations",
    url_prefix="/api/auth"
)

@web_blp.route("/login", methods=['GET', 'POST'])
def login():
    """Handle web login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            if user.role == 'visitor':
                return redirect(url_for('main.index'))
            return redirect(url_for('dashboard.dashboard'))

        flash('Please check your login details and try again.')
    return render_template('auth/login.html')

@web_blp.route("/register", methods=['GET', 'POST'])
def register():
    """Handle web registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        if User.query.filter_by(email=email).first():
            flash('Email address already exists')
            return redirect(url_for('auth.register'))

        new_user = User(
            email=email,
            username=username,
            role=role
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@web_blp.route("/logout")
@login_required
def logout():
    """Handle web logout"""
    logout_user()
    return redirect(url_for('main.index'))

# API Routes
@api_blp.route("/login")
class LoginAPI(MethodView):
    @api_blp.arguments(UserSchema(only=['email', 'password']))
    @api_blp.response(200)
    def post(self, user_data):
        """API login endpoint"""
        user = User.query.filter_by(email=user_data['email']).first()

        if user and user.check_password(user_data['password']):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': UserSchema().dump(user)
            }
        abort(401, message="Invalid credentials")

@api_blp.route("/register")
class RegisterAPI(MethodView):
    @api_blp.arguments(UserSchema)
    @api_blp.response(201, UserSchema)
    def post(self, user_data):
        """API registration endpoint"""
        if User.query.filter_by(email=user_data['email']).first():
            abort(400, message="Email address already exists")
            
        if User.query.filter_by(username=user_data['username']).first():
            abort(400, message="Username already exists")

        try:
            new_user = User(
                email=user_data['email'],
                username=user_data['username'],
                role=user_data.get('role', 'visitor')
            )
            new_user.set_password(user_data['password'])

            db.session.add(new_user)
            db.session.commit()

            access_token = create_access_token(identity=new_user.id)
            refresh_token = create_refresh_token(identity=new_user.id)

            return {
                'message': 'User registered successfully',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': UserSchema().dump(new_user)
            }
        except Exception as e:
            db.session.rollback()
            abort(400, message=str(e))

        return {
            'message': 'User registered successfully',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': UserSchema().dump(new_user)
        }

@api_blp.route("/token/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    @api_blp.response(200)
    def post(self):
        """Refresh access token"""
        current_user_id = get_jwt_identity()
        access_token = create_access_token(identity=current_user_id)
        return {'access_token': access_token}