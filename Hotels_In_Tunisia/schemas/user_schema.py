from marshmallow import fields, validate
from .base_schema import BaseSchema

class UserSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(required=True, validate=validate.OneOf(
        ['visitor', 'hotel_admin', 'restaurant_owner', 'activity_provider']
    ))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)