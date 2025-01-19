from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import Restaurant, db
from utils import role_required
from math import radians, sin, cos, sqrt, atan2

restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/api/restaurants')

def calculate_distance(lat1, lng1, lat2, lng2):
    R = 6371  # Earth's radius in kilometers
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

@restaurant_bp.route('/')
def get_restaurants():
    try:
        category = request.args.get('category')
        query = Restaurant.query
        
        if category:
            query = query.filter_by(price_range=category)
            
        restaurants = query.all()
        return jsonify([{
            'id': restaurant.id,
            'name': restaurant.name,
            'description': restaurant.description,
            'latitude': restaurant.latitude,
            'longitude': restaurant.longitude,
            'cuisine_type': restaurant.cuisine_type,
            'price_range': restaurant.price_range,
            'menu': restaurant.menu,
            'images': restaurant.images,
            'region': restaurant.region
        } for restaurant in restaurants])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@restaurant_bp.route('/nearby')
def get_nearby_restaurants():
    try:
        latitude = float(request.args.get('lat'))
        longitude = float(request.args.get('lng'))
        max_distance = float(request.args.get('radius', 5.0))  # Default 5km radius

        restaurants = Restaurant.query.all()
        nearby = []

        for restaurant in restaurants:
            distance = calculate_distance(
                latitude, longitude,
                restaurant.latitude, restaurant.longitude
            )
            if distance <= max_distance:
                nearby.append({
                    'id': restaurant.id,
                    'name': restaurant.name,
                    'description': restaurant.description,
                    'latitude': restaurant.latitude,
                    'longitude': restaurant.longitude,
                    'cuisine_type': restaurant.cuisine_type,
                    'price_range': restaurant.price_range,
                    'menu': restaurant.menu,
                    'images': restaurant.images,
                    'region': restaurant.region,
                    'distance': distance
                })

        # Sort by distance
        nearby.sort(key=lambda x: x['distance'])
        return jsonify(nearby)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@restaurant_bp.route('/<int:restaurant_id>/menu')
def get_restaurant_menu(restaurant_id):
    try:
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        return jsonify({
            'menu': restaurant.menu,
            'last_updated': restaurant.last_updated
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@restaurant_bp.route('/<int:restaurant_id>/menu', methods=['PUT'])
@login_required
@role_required('restaurant_owner')
def update_menu(restaurant_id):
    try:
        restaurant = Restaurant.query.get_or_404(restaurant_id)

        if restaurant.owner_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()
        restaurant.menu = data['menu']
        restaurant.last_updated = db.func.now()

        db.session.commit()
        return jsonify({
            'message': 'Menu updated successfully',
            'menu': restaurant.menu,
            'last_updated': restaurant.last_updated
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@restaurant_bp.route('/<int:restaurant_id>', methods=['PUT'])
@login_required
@role_required('restaurant_owner')
def update_restaurant(restaurant_id):
    try:
        restaurant = Restaurant.query.get_or_404(restaurant_id)

        if restaurant.owner_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()
        for key, value in data.items():
            if hasattr(restaurant, key):
                setattr(restaurant, key, value)

        db.session.commit()
        return jsonify({
            'id': restaurant.id,
            'name': restaurant.name,
            'description': restaurant.description,
            'cuisine_type': restaurant.cuisine_type,
            'price_range': restaurant.price_range,
            'menu': restaurant.menu,
            'images': restaurant.images
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@restaurant_bp.route('/register', methods=['POST'])
@login_required
@role_required('restaurant_owner')
def register_restaurant():
    try:
        data = request.get_json()
        new_restaurant = Restaurant(
            name=data['name'],
            description=data['description'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            cuisine_type=data['cuisine_type'],
            price_range=data['price_range'],
            menu=data.get('menu', []),
            images=data.get('images', []),
            owner_id=current_user.id,
            region=data['region']
        )
        
        db.session.add(new_restaurant)
        db.session.commit()
        
        return jsonify({
            'id': new_restaurant.id,
            'name': new_restaurant.name,
            'message': 'Restaurant registered successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500