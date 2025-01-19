from marshmallow import Schema, fields, validate, post_dump

class LocationSchema(Schema):
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)

class HotelSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    price_range = fields.Str(required=True)
    amenities = fields.Dict(allow_none=True)
    images = fields.List(fields.Str(), allow_none=True)
    region = fields.Str(required=True)
    rating = fields.Float(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many, **kwargs):
        return data

class RestaurantSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    cuisine_type = fields.Str(required=True)
    price_range = fields.Str(required=True)
    menu = fields.Dict(allow_none=True)
    images = fields.List(fields.Str(), allow_none=True)
    region = fields.Str(required=True)
    rating = fields.Float(allow_none=True)
    working_hours = fields.Dict(allow_none=True)
    is_open = fields.Bool(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class ActivitySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    activity_type = fields.Str(required=True)
    price = fields.Float(required=True)
    duration = fields.Str(required=True)
    schedule = fields.Dict(allow_none=True)
    images = fields.List(fields.Str(), allow_none=True)
    region = fields.Str(required=True)
    rating = fields.Float(allow_none=True)
    capacity = fields.Int(allow_none=True)
    min_age = fields.Int(allow_none=True)
    difficulty_level = fields.Str(allow_none=True)
    equipment_provided = fields.Dict(allow_none=True)
    working_hours = fields.Dict(allow_none=True)
    is_open = fields.Bool(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class TransportationSchema(Schema):
    id = fields.Int(dump_only=True)
    from_location = fields.Str(required=True)
    to_location = fields.Str(required=True)
    means = fields.Str(required=True)
    duration = fields.Int(allow_none=True)
    price = fields.Float(allow_none=True)
    schedule = fields.Dict(allow_none=True)
    stops = fields.List(fields.Str(), allow_none=True)
    route_map = fields.Dict(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)