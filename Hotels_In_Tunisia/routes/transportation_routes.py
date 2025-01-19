from flask import Blueprint, jsonify, request
from models import Transportation, db

transport_bp = Blueprint('transportation', __name__, url_prefix='/api/transportation')

@transport_bp.route('/')
def get_transportation_options():
    try:
        from_location = request.args.get('from')
        to_location = request.args.get('to')
        
        query = Transportation.query
        if from_location:
            query = query.filter_by(from_location=from_location)
        if to_location:
            query = query.filter_by(to_location=to_location)
            
        options = query.all()
        return jsonify([{
            'id': option.id,
            'from_location': option.from_location,
            'to_location': option.to_location,
            'means': option.means,
            'duration': option.duration,
            'price': option.price,
            'schedule': option.schedule,
            'stops': option.stops,
            'route_map': option.route_map
        } for option in options])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transport_bp.route('/nearest')
def get_nearest_transportation():
    try:
        latitude = float(request.args.get('lat'))
        longitude = float(request.args.get('lng'))
        
        # In a real application, you would implement proper geospatial queries
        # For now, we'll return all options and calculate distance in Python
        all_options = Transportation.query.all()
        
        # Simple distance calculation (this should be done in the database)
        def calculate_distance(lat1, lng1, lat2, lng2):
            from math import radians, sin, cos, sqrt, atan2
            
            R = 6371  # Earth's radius in kilometers
            
            lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
            
            dlat = lat2 - lat1
            dlng = lng2 - lng1
            
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            
            return R * c
        
        nearest_options = sorted(all_options, 
            key=lambda x: calculate_distance(latitude, longitude, 
                                          float(x.latitude), float(x.longitude)))[:5]
        
        return jsonify([{
            'id': option.id,
            'from_location': option.from_location,
            'to_location': option.to_location,
            'means': option.means,
            'duration': option.duration,
            'price': option.price,
            'schedule': option.schedule,
            'stops': option.stops
        } for option in nearest_options])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
