from .base import BaseModel, db

class Activity(BaseModel):
    __tablename__ = 'activity'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    activity_type = db.Column(db.String(50))
    price = db.Column(db.Float)
    duration = db.Column(db.String(50))
    schedule = db.Column(db.JSON, default=lambda: {})
    images = db.Column(db.JSON, default=lambda: [])
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, default=0.0)
    capacity = db.Column(db.Integer)
    min_age = db.Column(db.Integer)
    difficulty_level = db.Column(db.String(20))
    equipment_provided = db.Column(db.JSON, default=lambda: {})
    working_hours = db.Column(db.JSON, default=lambda: {})
    is_open = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.schedule = kwargs.get('schedule', {})
        self.images = kwargs.get('images', [])
        self.equipment_provided = kwargs.get('equipment_provided', {})
        self.working_hours = kwargs.get('working_hours', {})

    def __repr__(self):
        return f'<Activity {self.name}>'