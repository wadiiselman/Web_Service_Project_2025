from app import db  # Ensure db is imported from your main app module
from datetime import datetime

class Business(db.Model):
    __tablename__ = 'businesses'  # Ensure the table name matches the database

    # Columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(255), nullable=False)  # Business name
    description = db.Column(db.Text, nullable=True)  # Business description
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User (owner)
    category = db.Column(db.String(255), nullable=False)  # Business category (e.g., Supermarket, Boutique)
    latitude = db.Column(db.Float, nullable=True)  # Latitude for the location (optional)
    longitude = db.Column(db.Float, nullable=True)  # Longitude for the location (optional)
    status = db.Column(db.Boolean, default=True)  # Business status (open/closed)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for last update

    # Relationship to User (owner)
    owner = db.relationship("User", back_populates="businesses")

    def __repr__(self):
        return f"<Business {self.name}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'category': self.category,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }