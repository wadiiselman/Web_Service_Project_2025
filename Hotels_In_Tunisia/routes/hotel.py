from flask import Blueprint as FlaskBlueprint, render_template
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas import HotelSchema
from models import Hotel, Activity, Restaurant
from app import db
from utils import role_required, calculate_distance
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Web routes blueprint
web_blp = FlaskBlueprint("hotels", __name__, url_prefix="/hotels")

# API routes blueprint
api_blp = Blueprint(
    "Hotels", "hotels_api",
    description="Operations on hotels",
    url_prefix="/api/hotels"
)

@api_blp.route("/<region>")
class HotelList(MethodView):
    @api_blp.response(200, HotelSchema(many=True))
    def get(self, region):
        """Get all hotels in a specific region"""
        try:
            logger.debug(f"Fetching hotels for region: {region}")
            hotels = Hotel.query.filter_by(region=region.lower()).all()
            logger.debug(f"Found {len(hotels)} hotels")
            # Convert the hotels to dictionaries before serialization
            hotels_dict = [hotel.to_dict() for hotel in hotels]
            return hotels_dict
        except Exception as e:
            logger.error(f"Error fetching hotels: {str(e)}")
            abort(500, message=str(e))

    @api_blp.arguments(HotelSchema)
    @api_blp.response(201, HotelSchema)
    def post(self, hotel_data, region):
        """Create a new hotel in a region"""
        try:
            hotel_data["region"] = region.lower()
            hotel_data["admin_id"] = 1  # Set default admin_id
            new_hotel = Hotel(**hotel_data)
            db.session.add(new_hotel)
            db.session.commit()
            logger.info(f"Created new hotel: {new_hotel.name} in {region}")
            return new_hotel.to_dict()
        except Exception as e:
            logger.error(f"Error creating hotel: {str(e)}")
            db.session.rollback()
            abort(500, message=str(e))


@web_blp.route("/<int:hotel_id>/nearby-restaurants")
def show_nearby_restaurants(hotel_id):
    """Render the nearby restaurants page."""
    try:
        # Fetch the hotel by ID
        hotel = Hotel.query.get_or_404(hotel_id)
        max_distance = 5.0  # Default distance in km

        # Fetch all restaurants and calculate distance
        restaurants = Restaurant.query.all()
        nearby_restaurants = []

        for restaurant in restaurants:
            distance = calculate_distance(
                hotel.latitude, hotel.longitude,
                restaurant.latitude, restaurant.longitude
            )
            if distance <= max_distance:
                # Ensure working_hours is handled if not present
                working_hours = getattr(restaurant, 'working_hours', None)

                # Safely construct restaurant_data
                restaurant_data = {
                    'id': restaurant.id,
                    'name': restaurant.name,
                    'description': restaurant.description,
                    'price_range': restaurant.price_range,
                    'cuisine_type': restaurant.cuisine_type,
                    'menu': restaurant.menu,
                    'is_open': restaurant.is_open,
                    'owner_id': restaurant.owner_id,
                    'images': restaurant.images,
                    'rating': restaurant.rating,
                    'distance': round(distance, 2),
                    'working_hours': working_hours if working_hours else 'Not available'
                }
                nearby_restaurants.append(restaurant_data)

        # Sort restaurants by distance
        nearby_restaurants.sort(key=lambda x: x['distance'])

        return render_template(
            "nearby_restaurants.html",
            hotel=hotel,
            nearby_restaurants=nearby_restaurants
        )
    except Exception as e:
        logger.error(f"Error rendering nearby restaurants: {str(e)}")
        abort(500, description="An error occurred while fetching nearby restaurants.")


@api_blp.route("/<int:hotel_id>/nearby/restaurants")
class NearbyRestaurants(MethodView):
    def get(self, hotel_id):
        """Get nearby restaurants for a specific hotel"""
        try:
            hotel = Hotel.query.get_or_404(hotel_id)
            max_distance = float(request.args.get('radius', 5.0))  # Default 5km radius

            restaurants = Restaurant.query.all()
            nearby_restaurants = []

            for restaurant in restaurants:
                distance = calculate_distance(
                    hotel.latitude, hotel.longitude,
                    restaurant.latitude, restaurant.longitude
                )
                if distance <= max_distance:
                    restaurant_data = {
                        'id': restaurant.id,
                        'name': restaurant.name,
                        'cuisine_type': restaurant.cuisine_type,
                        'description': restaurant.description,
                        'price_range': restaurant.price_range,
                        'menu': restaurant.menu,
                        'distance': round(distance, 2),
                        'latitude': restaurant.latitude,
                        'longitude': restaurant.longitude
                    }
                    nearby_restaurants.append(restaurant_data)

            nearby_restaurants.sort(key=lambda x: x['distance'])
            return {"nearby_restaurants": nearby_restaurants}
        except Exception as e:
            logger.error(f"Error finding nearby restaurants: {str(e)}")
            abort(500, message=str(e))


@api_blp.route("/<int:hotel_id>/nearby/activities")
class NearbyActivities(MethodView):
    def get(self, hotel_id):
        """Get nearby activities for a specific hotel"""
        try:
            hotel = Hotel.query.get_or_404(hotel_id)
            max_distance = float(request.args.get('radius', 5.0))  # Default 5km radius

            activities = Activity.query.all()
            nearby_activities = []

            for activity in activities:
                distance = calculate_distance(
                    hotel.latitude, hotel.longitude,
                    activity.latitude, activity.longitude
                )
                if distance <= max_distance:
                    activity_data = {
                        'id': activity.id,
                        'name': activity.name,
                        'type': activity.activity_type,
                        'description': activity.description,
                        'price': activity.price,
                        'distance': round(distance, 2),
                        'latitude': activity.latitude,
                        'longitude': activity.longitude
                    }
                    nearby_activities.append(activity_data)

            nearby_activities.sort(key=lambda x: x['distance'])
            return {"nearby_activities": nearby_activities}
        except Exception as e:
            logger.error(f"Error finding nearby activities: {str(e)}")
            abort(500, message=str(e))

@api_blp.route("/<int:hotel_id>")
class HotelDetail(MethodView):
    def get(self, hotel_id):
        """Get hotel details"""
        try:
            hotel = Hotel.query.get_or_404(hotel_id)
            return hotel.to_dict()
        except Exception as e:
            logger.error(f"Error getting hotel details: {str(e)}")
            abort(500, message=str(e))

@api_blp.route("/<int:hotel_id>/nearby/restaurants")
class NearbyRestaurants(MethodView):
    def get(self, hotel_id):
        """Get nearby restaurants for a specific hotel"""
        try:
            hotel = Hotel.query.get_or_404(hotel_id)
            max_distance = float(request.args.get('radius', 5.0))  # Default 5km radius

            restaurants = Restaurant.query.all()
            nearby_restaurants = []

            for restaurant in restaurants:
                distance = calculate_distance(
                    hotel.latitude, hotel.longitude,
                    restaurant.latitude, restaurant.longitude
                )
                if distance <= max_distance:
                    restaurant_data = {
                        'id': restaurant.id,
                        'name': restaurant.name,
                        'cuisine_type': restaurant.cuisine_type,
                        'description': restaurant.description,
                        'price_range': restaurant.price_range,
                        'menu': restaurant.menu,
                        'distance': round(distance, 2),
                        'latitude': restaurant.latitude,
                        'longitude': restaurant.longitude
                    }
                    nearby_restaurants.append(restaurant_data)

            nearby_restaurants.sort(key=lambda x: x['distance'])
            return {"nearby_restaurants": nearby_restaurants}
        except Exception as e:
            logger.error(f"Error finding nearby restaurants: {str(e)}")
            abort(500, message=str(e))

@api_blp.route("/<int:hotel_id>")
class HotelResource(MethodView):
    @api_blp.response(200, HotelSchema)
    def get(self, hotel_id):
        """Get a specific hotel's details"""
        try:
            hotel = Hotel.query.get_or_404(hotel_id)
            return hotel.to_dict()
        except Exception as e:
            logger.error(f"Error fetching hotel {hotel_id}: {str(e)}")
            abort(500, message=str(e))

    @api_blp.arguments(HotelSchema)
    @api_blp.response(200, HotelSchema)
    def put(self, hotel_data, hotel_id):
        """Update a hotel's details"""
        try:
            hotel = Hotel.query.get_or_404(hotel_id)

            for key, value in hotel_data.items():
                setattr(hotel, key, value)

            db.session.commit()
            logger.info(f"Updated hotel: {hotel.name}")
            return hotel.to_dict()
        except Exception as e:
            logger.error(f"Error updating hotel {hotel_id}: {str(e)}")
            db.session.rollback()
            abort(500, message=str(e))