from flask_smorest import Blueprint
from flask import jsonify
from models import Business  # Import the Business model

# Define the blueprint
blp = Blueprint(
    "business",
    __name__,
    url_prefix="/business",
    description="Operations related to businesses"
)

@blp.route("/", methods=["GET"])
def get_all_businesses():
    """
    Get a list of all businesses.
    """
    businesses = Business.query.all()
    return jsonify([
        {
            'id': business.id,
            'name': business.name,
            'description': business.description,
            'latitude': business.latitude,
            'longitude': business.longitude,
            'status': business.status  # Change to status
        }
        for business in businesses
    ]), 200


@blp.route("/<int:id>", methods=["GET"])
def get_business(id):
    """
    Get details of a single business by ID.
    """
    business = Business.query.get(id)
    if business is None:
        return jsonify({'error': 'Business not found'}), 404

    return jsonify({
        'id': business.id,
        'name': business.name,
        'description': business.description,
        'latitude': business.latitude,
        'longitude': business.longitude,
        'status': business.status  # Change to status
    }), 200