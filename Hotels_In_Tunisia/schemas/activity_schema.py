
from marshmallow import Schema, fields
from .base_schema import BaseSchema

class ActivitySchema(BaseSchema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    activity_type = fields.Str(required=True)
    price = fields.Float(required=True)
    duration = fields.Str(required=True)
    region = fields.Str(required=True)
    provider_id = fields.Int(dump_only=True)
    schedule = fields.Raw(load_default={}, dump_default={})
    images = fields.Raw(load_default=[], dump_default=[])
    equipment_provided = fields.Raw(load_default={}, dump_default={})
    working_hours = fields.Raw(load_default={}, dump_default={})
    is_open = fields.Bool(missing=False)
    rating = fields.Float(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
