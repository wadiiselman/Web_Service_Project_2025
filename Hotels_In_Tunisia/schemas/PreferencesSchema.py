from marshmallow import Schema, fields

class PreferencesSchema(Schema):
    user_id = fields.Int(required=True)  # Required field
    cuisine_types = fields.List(fields.String(), default=[])
    preferred_regions = fields.List(fields.String(), default=[])
    activity_types = fields.List(fields.String(), default=[])
    budget_range = fields.String()
    transportation_means = fields.List(fields.String(), default=[])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
