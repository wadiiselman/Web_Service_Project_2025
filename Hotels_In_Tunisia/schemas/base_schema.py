from marshmallow import Schema, fields, validate, post_dump

class BaseSchema(Schema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many, **kwargs):
        return data
