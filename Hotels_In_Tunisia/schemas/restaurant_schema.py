
from marshmallow import Schema, fields
from .base_schema import BaseSchema

class RestaurantSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    cuisine_type = fields.Str(required=True)
    price_range = fields.Str(required=True)
    menu = fields.Dict(keys=fields.Str(), values=fields.Raw(), missing={})
    region = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    working_hours = fields.Dict(keys=fields.Str(), values=fields.Raw(), missing={})
    is_open = fields.Bool(missing=False)
    images = fields.List(fields.Str(), missing=[])
    rating = fields.Float(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


