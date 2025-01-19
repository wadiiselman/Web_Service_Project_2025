from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB  # Import JSONB from PostgreSQL dialect

class Preferences(db.Model):
    __tablename__ = 'preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    cuisine_types = db.Column(JSONB, default=[], nullable=True)  # JSONB for PostgreSQL
    preferred_regions = db.Column(JSONB, default=[], nullable=True)
    activity_types = db.Column(JSONB, default=[], nullable=True)
    budget_range = db.Column(db.String(20))
    transportation_means = db.Column(JSONB, default=[], nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='preferences')

    def __init__(self, user_id, cuisine_types, preferred_regions, activity_types, budget_range, transportation_means):
        self.user_id = user_id
        self.cuisine_types = cuisine_types
        self.preferred_regions = preferred_regions
        self.activity_types = activity_types
        self.budget_range = budget_range
        self.transportation_means = transportation_means

    def __repr__(self):
        return f'<Preferences(user_id={self.user_id}, cuisine_types={self.cuisine_types})>'
