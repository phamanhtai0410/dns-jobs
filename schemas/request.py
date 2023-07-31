# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate


class RequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    page = fields.Integer(default=1, validate=validate.Range(min=1))
    page_size = fields.Integer(default=10, validate=validate.Range(min=1))
    search = fields.String(allow_none=True)

