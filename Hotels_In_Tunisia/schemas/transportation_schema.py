from marshmallow import fields
from .base_schema import BaseSchema

class TransportationSchema(BaseSchema):
    from_location = fields.Str(required=True)
    to_location = fields.Str(required=True)
    means = fields.Str(required=True)
    duration = fields.Int(allow_none=True)
    price = fields.Float(allow_none=True)
    schedule = fields.Dict(allow_none=True)
    stops = fields.List(fields.Str(), allow_none=True)
    route_map = fields.Dict(allow_none=True)
