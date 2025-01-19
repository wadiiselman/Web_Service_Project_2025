from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import Restaurant
from app import db
from schemas import RestaurantSchema

blp = Blueprint("Restaurants", "restaurants", url_prefix="/api/restaurants")

@blp.route("/")
class RestaurantList(MethodView):
    @blp.response(200, RestaurantSchema(many=True))
    def get(self):
        """Get all restaurants"""
        try:
            # Add sample restaurants if none exist
            if not Restaurant.query.first():
                sample_restaurants = [
                    {
                        "name": "Le Méditerranée",
                        "description": "Upscale Mediterranean restaurant with sea view",
                        "latitude": 35.8248,
                        "longitude": 10.6349,
                        "cuisine_type": "Mediterranean",
                        "price_range": "upscale",
                        "region": "sousse",
                        "owner_id": 1,
                        "images": ["restaurant1.jpg", "menu1.jpg"],
                        "menu": {
                            "Starters": [
                                {"name": "Mediterranean Mezze Platter", "price": 25.00},
                                {"name": "Fresh Seafood Soup", "price": 18.00}
                            ],
                            "Main Courses": [
                                {"name": "Grilled Sea Bass", "price": 45.00},
                                {"name": "Lamb Couscous", "price": 38.00}
                            ],
                            "Desserts": [
                                {"name": "Baklava Selection", "price": 15.00}
                            ]
                        },
                        "working_hours": {"open": "12:00", "close": "23:00"},
                        "is_open": True
                    },
                    {
                        "name": "Café Medina",
                        "description": "Traditional Tunisian café in the heart of Sousse",
                        "latitude": 35.8252,
                        "longitude": 10.6348,
                        "cuisine_type": "Tunisian",
                        "price_range": "moderate",
                        "region": "sousse",
                        "owner_id": 1,
                        "images": ["cafe1.jpg", "menu2.jpg"],
                        "menu": {
                            "Breakfast": [
                                {"name": "Traditional Tunisian Breakfast", "price": 15.00}
                            ],
                            "Main Dishes": [
                                {"name": "Shakshuka", "price": 12.00},
                                {"name": "Tunisian Tajine", "price": 18.00}
                            ],
                            "Beverages": [
                                {"name": "Mint Tea", "price": 4.00}
                            ]
                        },
                        "working_hours": {"open": "08:00", "close": "22:00"},
                        "is_open": True
                    }
                ]
                
                for restaurant_data in sample_restaurants:
                    new_restaurant = Restaurant(**restaurant_data)
                    db.session.add(new_restaurant)
                db.session.commit()
            
            restaurants = Restaurant.query.all()
            return restaurants
        except Exception as e:
            abort(500, message=str(e))

    @blp.arguments(RestaurantSchema)
    @blp.response(201, RestaurantSchema)
    def post(self, restaurant_data):
        """Create a new restaurant"""
        try:
            new_restaurant = Restaurant(**restaurant_data)
            db.session.add(new_restaurant)
            db.session.commit()
            return new_restaurant
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

@blp.route("/<int:restaurant_id>")
class RestaurantResource(MethodView):
    @blp.response(200, RestaurantSchema)
    def get(self, restaurant_id):
        """Get restaurant details"""
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        return restaurant

    @blp.arguments(RestaurantSchema)
    @blp.response(200, RestaurantSchema)
    def put(self, restaurant_data, restaurant_id):
        """Update restaurant details"""
        try:
            restaurant = Restaurant.query.get_or_404(restaurant_id)
            for key, value in restaurant_data.items():
                setattr(restaurant, key, value)
            db.session.commit()
            return restaurant
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

    def delete(self, restaurant_id):
        """Delete restaurant"""
        try:
            restaurant = Restaurant.query.get_or_404(restaurant_id)
            db.session.delete(restaurant)
            db.session.commit()
            return {"message": "Restaurant deleted successfully"}
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

@blp.route("/<int:restaurant_id>/menu")
class RestaurantMenu(MethodView):
    @blp.response(200, RestaurantSchema)
    def get(self, restaurant_id):
        """Get restaurant menu"""
        try:
            restaurant = Restaurant.query.get_or_404(restaurant_id)
            return restaurant
        except Exception as e:
            abort(500, message=str(e))

    @blp.arguments(RestaurantSchema(only=["menu"]))  # Accept only the menu field in the request body
    @blp.response(200, RestaurantSchema)
    def put(self, restaurant_data, restaurant_id):
        """Update restaurant menu"""
        try:
            restaurant = Restaurant.query.get_or_404(restaurant_id)

            # Only update the 'menu' field if it's present in the request
            if 'menu' in restaurant_data:
                restaurant.menu = restaurant_data['menu']
                restaurant.updated_at = db.func.now()  # Optionally update the timestamp for the last update

                # Commit the changes to the database
                db.session.commit()

            return restaurant  # Return the updated restaurant object with the new menu
        except Exception as e:
            db.session.rollback()  # Rollback if there's an error
            abort(500, message=str(e))
