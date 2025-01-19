from marshmallow import Schema, fields, post_dump

class BusinessSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    items_sold = fields.Dict(keys=fields.Str(), values=fields.Float(), allow_none=True)  # JSON for items and prices
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    status = fields.Boolean(required=True)
    region = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump
    def remove_none_values(self, data, **kwargs):
        """Remove None values from serialized output."""
        return {key: value for key, value in data.items() if value is not None}