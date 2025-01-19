from .base import BaseModel, db

class Transportation(BaseModel):
    __tablename__ = 'transportation'

    from_location = db.Column(db.String(100), nullable=False)
    to_location = db.Column(db.String(100), nullable=False)
    means = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer)  # Duration in minutes
    price = db.Column(db.Float)  # Price in local currency
    schedule = db.Column(db.JSON, default=lambda: {})
    stops = db.Column(db.JSON, default=lambda: [])
    route_map = db.Column(db.JSON, default=lambda: {})
    latitude = db.Column(db.Float)  # For geospatial queries
    longitude = db.Column(db.Float)  # For geospatial queries

    def __init__(self, **kwargs):
        super(Transportation, self).__init__(**kwargs)
        self.schedule = self.schedule or {}
        self.stops = self.stops or []
        self.route_map = self.route_map or {}

    def to_dict(self):
        return {
            'id': self.id,
            'from_location': self.from_location,
            'to_location': self.to_location,
            'means': self.means,
            'duration': self.duration,
            'price': self.price,
            'schedule': self.schedule,
            'stops': self.stops,
            'route_map': self.route_map,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Transportation {self.from_location} to {self.to_location}>'