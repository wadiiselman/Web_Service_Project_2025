from marshmallow import Schema, fields, validate, post_dump
from .base_schema import BaseSchema

class HotelSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    price_range = fields.Str(required=True)
    amenities = fields.Raw(allow_none=True)  # Changed to Raw to handle any JSON structure
    images = fields.List(fields.Str(), allow_none=True)
    region = fields.Str(required=True)
    rating = fields.Float(allow_none=True)
    admin_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump
    def remove_none_values(self, data, **kwargs):
        """Remove None values from the serialized output"""
        return {
            key: value for key, value in data.items()
            if value is not None
        }