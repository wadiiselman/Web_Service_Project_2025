from .base import BaseModel, db
from datetime import datetime

class Hotel(BaseModel):
    __tablename__ = 'hotel'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    price_range = db.Column(db.String(20))
    amenities = db.Column(db.JSON)
    images = db.Column(db.JSON)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, default=0.0)

    def __init__(self, **kwargs):
        # Handle amenities and images before initialization
        if 'amenities' in kwargs:
            kwargs['amenities'] = kwargs['amenities'] if isinstance(kwargs['amenities'], dict) else {}
        else:
            kwargs['amenities'] = {}

        if 'images' in kwargs:
            kwargs['images'] = kwargs['images'] if isinstance(kwargs['images'], list) else []
        else:
            kwargs['images'] = []

        super(Hotel, self).__init__(**kwargs)

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'price_range': self.price_range,
            'amenities': self.amenities if isinstance(self.amenities, dict) else {},
            'images': self.images if isinstance(self.images, list) else [],
            'region': self.region,
            'rating': self.rating,
            'admin_id': self.admin_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f'<Hotel {self.name}>'