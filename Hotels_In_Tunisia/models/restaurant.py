
from .base import BaseModel, db

class Restaurant(BaseModel):
    __tablename__ = 'restaurant'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    cuisine_type = db.Column(db.String(50), nullable=False)
    price_range = db.Column(db.String(20), nullable=False)
    menu = db.Column(db.JSON, nullable=False)
    region = db.Column(db.String(50), nullable=False)
    working_hours = db.Column(db.JSON, nullable=False)
    is_open = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    images = db.Column(db.JSON, default=list, nullable=False)
    rating = db.Column(db.Float, default=0.0)

    def __init__(self, **kwargs):
        super(Restaurant, self).__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'cuisine_type': self.cuisine_type,
            'price_range': self.price_range,
            'menu': self.menu,
            'region': self.region,
            'working_hours': self.working_hours,
            'is_open': self.is_open
        }
