from flask import Blueprint, jsonify, request
from models import Hotel, Business, Activity, Restaurant, db
from math import radians, sin, cos, sqrt, atan2
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

hotel_bp = Blueprint('hotel', __name__, url_prefix='/api/hotels')

def calculate_distance(lat1, lng1, lat2, lng2):
    R = 6371  # Earth's radius in kilometers
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

@hotel_bp.route('/<region>')
def get_hotels_by_region(region):
    """Get hotels in a specific region"""
    try:
        # Get user's location from request parameters
        user_lat = float(request.args.get('lat', 0))
        user_lng = float(request.args.get('lng', 0))

        # Get all hotels in the region
        hotels = Hotel.query.filter_by(region=region.lower()).all()

        # Calculate distances and sort hotels
        hotel_list = [{
            'id': hotel.id,
            'name': hotel.name,
            'description': hotel.description,
            'latitude': hotel.latitude,
            'longitude': hotel.longitude,
            'price_range': hotel.price_range,
            'amenities': hotel.amenities,
            'images': hotel.images,
            'region': hotel.region,
            'distance': calculate_distance(user_lat, user_lng, hotel.latitude, hotel.longitude)
        } for hotel in hotels]

        # Sort by distance
        hotel_list.sort(key=lambda x: x['distance'])

        return jsonify(hotel_list)
    except Exception as e:
        logger.error(f"Error fetching hotels by region: {str(e)}")
        return jsonify({'error': str(e)}), 500

@hotel_bp.route('/<int:hotel_id>')
def get_hotel_details(hotel_id):
    """Get details of a specific hotel"""
    try:
        hotel = Hotel.query.get_or_404(hotel_id)
        return jsonify({
            'id': hotel.id,
            'name': hotel.name,
            'description': hotel.description,
            'latitude': hotel.latitude,
            'longitude': hotel.longitude,
            'price_range': hotel.price_range,
            'amenities': hotel.amenities,
            'images': hotel.images,
            'region': hotel.region
        })
    except Exception as e:
        logger.error(f"Error fetching hotel {hotel_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@hotel_bp.route('/<int:hotel_id>/nearby/businesses')
def get_nearest_businesses(hotel_id):
    """Get nearest businesses (restaurants, activities, etc.) to a hotel"""
    try:
        hotel = Hotel.query.get_or_404(hotel_id)
        max_distance = float(request.args.get('radius', 5.0))  # Default 5km radius

        # Get all businesses (restaurants, supermarkets, etc.)
        businesses = Business.query.all()

        nearby_businesses = []
        for business in businesses:
            distance = calculate_distance(hotel.latitude, hotel.longitude, business.latitude, business.longitude)
            if distance <= max_distance:
                nearby_businesses.append({
                    'id': business.id,
                    'name': business.name,
                    'description': business.description,
                    'latitude': business.latitude,
                    'longitude': business.longitude,
                    'distance': round(distance, 2)  # Round to 2 decimal places
                })

        # Sort businesses by distance
        nearby_businesses.sort(key=lambda x: x['distance'])

        return jsonify({
            'nearby_businesses': nearby_businesses
        })
    except Exception as e:
        logger.error(f"Error fetching nearest businesses: {str(e)}")
        return jsonify({'error': str(e)}), 500

@hotel_bp.route('/<int:hotel_id>/nearby/activities')
def get_nearby_activities(hotel_id):
    """Get nearby activities for a specific hotel"""
    try:
        hotel = Hotel.query.get_or_404(hotel_id)
        max_distance = float(request.args.get('radius', 5.0))  # Default 5km radius

        # Get all activities
        activities = Activity.query.all()

        nearby_activities = [
            {
                'id': activity.id,
                'name': activity.name,
                'type': activity.activity_type,
                'description': activity.description,
                'price': activity.price,
                'distance': calculate_distance(
                    hotel.latitude, hotel.longitude,
                    activity.latitude, activity.longitude
                )
            }
            for activity in activities
            if calculate_distance(
                hotel.latitude, hotel.longitude,
                activity.latitude, activity.longitude
            ) <= max_distance
        ]

        # Sort by distance
        nearby_activities.sort(key=lambda x: x['distance'])

        return jsonify({
            'nearby_activities': nearby_activities
        })
    except Exception as e:
        logger.error(f"Error fetching nearby activities: {str(e)}")
        return jsonify({'error': str(e)}), 500

@hotel_bp.route('/<int:hotel_id>/nearby/restaurants')
def get_nearby_restaurants(hotel_id):
    """Get nearby restaurants for a specific hotel"""
    try:
        hotel = Hotel.query.get_or_404(hotel_id)
        max_distance = float(request.args.get('radius', 5.0))  # Default 5km radius

        # Get all restaurants
        restaurants = Restaurant.query.all()

        nearby_restaurants = [
            {
                'id': restaurant.id,
                'name': restaurant.name,
                'cuisine_type': restaurant.cuisine_type,
                'price_range': restaurant.price_range,
                'menu': restaurant.menu,
                'distance': calculate_distance(
                    hotel.latitude, hotel.longitude,
                    restaurant.latitude, restaurant.longitude
                )
            }
            for restaurant in restaurants
            if calculate_distance(
                hotel.latitude, hotel.longitude,
                restaurant.latitude, restaurant.longitude
            ) <= max_distance
        ]

        # Sort by distance
        nearby_activities.sort(key=lambda x: x['distance'])
        nearby_restaurants.sort(key=lambda x: x['distance'])

        return jsonify({
            'nearby_restaurants': nearby_restaurants
        })
    except Exception as e:
        logger.error(f"Error fetching nearby restaurants: {str(e)}")
        return jsonify({'error': str(e)}), 500