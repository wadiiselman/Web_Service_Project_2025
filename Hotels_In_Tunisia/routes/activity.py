from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas import ActivitySchema
from models import Activity, User
from app import db
from utils import role_required
from math import radians, sin, cos, sqrt, atan2
from flask import request

blp = Blueprint(
    "Activities", "activities",
    description="Operations on activities",
    url_prefix="/api/activities"
)

def calculate_distance(lat1, lng1, lat2, lng2):
    R = 6371  # Earth's radius in kilometers
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

@blp.route("/")
class ActivityList(MethodView):
    """Operations for activities list"""
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, ActivitySchema(many=True))
    def get(self):
        """List all activities (Public endpoint)"""
        try:
            # Add sample activities if none exist
            if not Activity.query.first():
                sample_activities = [
                    {
                        "name": "Guided Medina Tour",
                        "description": "Explore the historic Medina of Sousse with expert guides. Visit ancient markets, historical sites and learn about local culture.",
                        "latitude": 35.8250,
                        "longitude": 10.6350,
                        "activity_type": "Cultural Tour",
                        "price": 45.00,
                        "duration": "3 hours",
                        "region": "sousse",
                        "images": ["medina_tour1.jpg", "medina_tour2.jpg"],
                        "provider_id": 1
                    },
                    {
                        "name": "Beach Water Sports",
                        "description": "Exciting water sports package including jet skiing, parasailing, and banana boat rides.",
                        "latitude": 35.8260,
                        "longitude": 10.6340,
                        "activity_type": "Water Sports",
                        "price": 75.00,
                        "duration": "2 hours",
                        "region": "sousse",
                        "images": ["watersports1.jpg", "watersports2.jpg"],
                        "provider_id": 1
                    }
                ]
                
                for activity_data in sample_activities:
                    new_activity = Activity(**activity_data)
                    db.session.add(new_activity)
                db.session.commit()
            
            activities = Activity.query.all()
            return activities
        except Exception as e:
            abort(500, message=str(e))

    @blp.arguments(ActivitySchema)
    @blp.response(201, ActivitySchema)
    def post(self, activity_data):
        """Create a new activity (Public endpoint)"""
        try:
            # Set a default provider_id for testing
            activity_dict = {
                "name": activity_data["name"],
                "description": activity_data["description"],
                "latitude": float(activity_data["latitude"]),
                "longitude": float(activity_data["longitude"]),
                "activity_type": activity_data["activity_type"],
                "price": float(activity_data["price"]),
                "duration": activity_data["duration"],
                "region": activity_data["region"],
                "provider_id": 1,  # Using a default provider_id
                "schedule": activity_data.get("schedule", {}),
                "images": activity_data.get("images", []),
                "equipment_provided": activity_data.get("equipment_provided", {}),
                "working_hours": activity_data.get("working_hours", {}),
                "is_open": activity_data.get("is_open", False),
                "rating": float(activity_data.get("rating", 0))
            }

            new_activity = Activity(**activity_dict)
            
            db.session.add(new_activity)
            db.session.commit()
            return new_activity
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

@blp.route("/<int:activity_id>")
class ActivityResource(MethodView):
    @blp.response(200, ActivitySchema)
    def get(self, activity_id):
        """Get a specific activity's details (Public endpoint)"""
        activity = Activity.query.get_or_404(activity_id)
        return activity

    @blp.arguments(ActivitySchema)
    @blp.response(200, ActivitySchema)
    def put(self, activity_data, activity_id):
        """Update an activity's details (Public endpoint)"""
        try:
            activity = Activity.query.get_or_404(activity_id)
            for key, value in activity_data.items():
                setattr(activity, key, value)
            db.session.commit()
            return activity
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

    def delete(self, activity_id):
        """Delete an activity (Public endpoint)"""
        try:
            activity = Activity.query.get_or_404(activity_id)
            db.session.delete(activity)
            db.session.commit()
            return {"message": "Activity deleted successfully"}
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))



@blp.route("/region/<region>")
class RegionActivities(MethodView):
    @blp.response(200, ActivitySchema(many=True))
    def get(self, region):
        """Get all activities in a specific region (Public endpoint)"""
        try:
            activities = Activity.query.filter_by(region=region.lower()).all()
            return activities
        except Exception as e:
            abort(500, message=str(e))