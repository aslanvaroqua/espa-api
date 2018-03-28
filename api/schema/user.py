""" Defines JSON validation de-/serialization """
import datetime

from marshmallow import Schema, fields, pre_load, validate, ValidationError


class UserEntrySchema(Schema):
    """ Critical information saved in the database """
    id = fields.Int(load_only=True, missing=0)
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    contactid = fields.Str(required=True)
    last_login = fields.DateTime(missing=lambda: str(datetime.datetime.utcnow()))
    date_joined = fields.DateTime(missing=lambda: str(datetime.datetime.utcnow()))


class UserResponseSchema(Schema):
    """ Object about a user, fit for return to the user """
    id = fields.Int(load_only=True, missing=0)
    email = fields.Str(required=True, validate=validate.Email())
    username = fields.Str(required=True)
    roles = fields.List(fields.String(), missing=[])
