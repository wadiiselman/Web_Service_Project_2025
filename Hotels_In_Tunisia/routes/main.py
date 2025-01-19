from flask import Blueprint, render_template, abort, jsonify, redirect, url_for
from flask_login import current_user
from models import Hotel, Restaurant, Activity
from schemas import HotelSchema, RestaurantSchema, ActivitySchema
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a regular Flask blueprint for web routes
blp = Blueprint('main', __name__)

@blp.route('/')
def index():
    """Render home page"""
    try:
        if current_user.is_authenticated and current_user.role != 'visitor':
            return redirect(url_for('dashboard.dashboard'))
        hotels = Hotel.query.limit(3).all()
        restaurants = Restaurant.query.limit(3).all()
        activities = Activity.query.limit(3).all()
        return render_template('index.html',
                           hotels=hotels,
                           restaurants=restaurants,
                           activities=activities)
    except Exception as e:
        logger.error(f"Error rendering index page: {str(e)}")
        abort(500)

@blp.route('/restaurant/le-mediterranee')
def restaurant_details():
    return render_template('restaurant_details.html')

@blp.route('/activity/medina-tour')
def activity_details():
    return render_template('activity_details.html')

@blp.route('/explore')
def explore():
    """Render explore page"""
    try:
        hotels = Hotel.query.all()
        restaurants = Restaurant.query.all()
        activities = Activity.query.all()

        # Pass the model objects directly to the template
        hotels_dict = hotels
        restaurants_dict = restaurants
        activities_dict = activities

        logger.debug(f"Serialized {len(hotels_dict)} hotels, {len(restaurants_dict)} restaurants, {len(activities_dict)} activities")

        return render_template('explore.html',
                            hotels=hotels_dict,
                            restaurants=restaurants_dict,
                            activities=activities_dict)
    except Exception as e:
        logger.error(f"Error in explore route: {str(e)}")
        abort(500)

@blp.route('/hotels/<string:region>')
def hotels_by_region(region):
    """Render region-specific hotels page"""
    try:
        hotels = Hotel.query.filter_by(region=region.lower()).all()

        # Convert models to dictionaries
        hotels_dict = [hotel.to_dict() for hotel in hotels]

        logger.debug(f"Hotels data for region {region}: {hotels_dict}")

        return render_template('hotels_region.html',
                           region=region,
                           hotels=hotels_dict)
    except Exception as e:
        logger.error(f"Error in hotels_by_region route: {str(e)}")
        logger.exception(e)  # This will log the full stack trace
        abort(500)

# Error handlers
@blp.errorhandler(500)
def handle_500(error):
    return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

@blp.errorhandler(404)
def handle_404(error):
    return jsonify({"error": "Not Found", "message": str(error)}), 404