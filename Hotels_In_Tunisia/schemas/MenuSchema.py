from marshmallow import Schema, fields


class MenuSchema(Schema):
    menu = fields.Dict(required=True)