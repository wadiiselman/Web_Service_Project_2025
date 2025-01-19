from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from utils import role_required
from models import Hotel, Restaurant, Activity
from app import db
import os
from werkzeug.utils import secure_filename

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@dashboard_bp.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        image_url = url_for('static', filename=f'uploads/{filename}')
        
        if current_user.role == 'restaurant_owner':
            restaurant = Restaurant.query.filter_by(owner_id=current_user.id).first()
            if restaurant:
                if not restaurant.images:
                    restaurant.images = []
                restaurant.images.append(image_url)
                db.session.commit()
        elif current_user.role == 'activity_provider':
            activity = Activity.query.filter_by(provider_id=current_user.id).first()
            if activity:
                if not activity.images:
                    activity.images = []
                activity.images.append(image_url)
                db.session.commit()
                
        flash('Image uploaded successfully')
        return redirect(url_for('dashboard.dashboard'))
    flash('Invalid file type')
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if current_user.role == 'visitor':
        return redirect(url_for('main.index'))
        
    if current_user.role not in ['hotel_admin', 'restaurant_owner', 'activity_provider']:
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.index'))

    stats = {
        'dates': [],
        'view_counts': [],
        'views': 0,
        'bookings': 0,
        'revenue': 0
    }

    if current_user.role == 'hotel_admin':
        hotels = Hotel.query.filter_by(admin_id=current_user.id).all()
        return render_template('dashboard/hotel.html', hotel=hotels[0] if hotels else None, stats=stats)
    elif current_user.role == 'restaurant_owner':
        restaurants = Restaurant.query.filter_by(owner_id=current_user.id).all()
        return render_template('dashboard/restaurant.html', restaurant=restaurants[0] if restaurants else None, stats=stats)
    elif current_user.role == 'activity_provider':
        activities = Activity.query.filter_by(provider_id=current_user.id).all()
        return render_template('dashboard/activity.html', activity=activities[0] if activities else None, stats=stats)
    if request.method == 'POST':
        try:
            if current_user.role == 'restaurant_owner':
                restaurant = Restaurant.query.filter_by(owner_id=current_user.id).first()
                
                menu_items = request.form.getlist('menu_items[]')
                menu_prices = request.form.getlist('menu_prices[]')
                menu_data = [{'item': item, 'price': float(price)} 
                            for item, price in zip(menu_items, menu_prices) 
                            if item and price]

                data = {
                    'name': request.form.get('name'),
                    'description': request.form.get('description'),
                    'latitude': float(request.form.get('latitude', 0)),
                    'longitude': float(request.form.get('longitude', 0)),
                    'cuisine_type': request.form.get('cuisine_type'),
                    'price_range': request.form.get('price_range'),
                    'region': request.form.get('region', 'default'),
                    'menu': menu_data,
                    'owner_id': current_user.id
                }

                if restaurant:
                    for key, value in data.items():
                        setattr(restaurant, key, value)
                    db.session.commit()
                    flash('Restaurant updated successfully', 'success')
                else:
                    new_restaurant = Restaurant(**data)
                    db.session.add(new_restaurant)
                    db.session.commit()
                    restaurant = new_restaurant
                    flash('Restaurant created successfully', 'success')
                
                return render_template('dashboard/restaurant.html', 
                                    restaurant=restaurant,
                                    stats=stats)

            elif current_user.role == 'activity_provider':
                activity = Activity.query.filter_by(provider_id=current_user.id).first()
                if activity:
                    activity.name = request.form.get('name')
                    activity.description = request.form.get('description')
                    activity.latitude = float(request.form.get('latitude', 0))
                    activity.longitude = float(request.form.get('longitude', 0))
                    activity.activity_type = request.form.get('activity_type')
                    activity.region = request.form.get('region', 'default')
                    db.session.commit()
                    flash('Activity updated successfully', 'success')
            elif current_user.role == 'activity_provider':
                activity = Activity.query.filter_by(provider_id=current_user.id).first()
                if activity:
                    activity.name = request.form.get('name')
                    activity.description = request.form.get('description')
                    activity.price = float(request.form.get('price', 0))
                    activity.activity_type = request.form.get('activity_type')
                    activity.region = request.form.get('region', 'default')
                    activity.latitude = float(request.form.get('latitude', 0))
                    activity.longitude = float(request.form.get('longitude', 0))
                    db.session.commit()
                    flash('Profile updated successfully', 'success')
                else:
                    new_activity = Activity(
                        name=request.form.get('name'),
                        description=request.form.get('description'),
                        price=float(request.form.get('price', 0)),
                        activity_type=request.form.get('activity_type'),
                        region=request.form.get('region', 'default'),
                        latitude=float(request.form.get('latitude', 0)),
                        longitude=float(request.form.get('longitude', 0)),
                        provider_id=current_user.id
                    )
                    db.session.add(new_activity)
                    db.session.commit()
                    flash('Activity added successfully', 'success')
            return redirect(url_for('dashboard.dashboard'))
        except Exception as e:
            flash(f'Error updating profile: {str(e)}', 'error')
            db.session.rollback()
            return redirect(url_for('dashboard.dashboard'))
    
    return redirect(url_for('main.index'))

@dashboard_bp.route('/add_hotel', methods=['POST'])
@login_required
def add_hotel():
    if current_user.role != 'hotel_admin':
        flash('You do not have permission to add hotels.')
        return redirect(url_for('main.index'))
    try:
        data = request.form
        new_hotel = Hotel(
            name=data['name'],
            description=data['description'],
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            price_range=data['price_range'],
            amenities=data.get('amenities', {}),
            region=data['region'],
            admin_id=current_user.id
        )
        db.session.add(new_hotel)
        db.session.commit()
        return redirect(url_for('dashboard.dashboard'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/delete_hotel/<int:hotel_id>', methods=['POST'])
@login_required
@role_required('hotel_admin')
def delete_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    if hotel.admin_id != current_user.id:
        abort(403)
    db.session.delete(hotel)
    db.session.commit()
    return redirect(url_for('dashboard.dashboard'))
