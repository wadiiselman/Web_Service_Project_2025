from app import db  # Import `db` from `app.py`
from .user import User
from .hotel import Hotel
from .restaurant import Restaurant
from .activity import Activity
from .transportation import Transportation
from .business import Business  # Import Business

__all__ = [
    'db',  # Make `db` accessible
    'User',
    'Hotel',
    'Restaurant',
    'Activity',
    'Transportation',
    'Business',
]