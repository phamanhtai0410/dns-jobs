# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from flask import request
from schemas.hello import HelloSchema
from connect import security
from lib.logger import debug

class HelloWorld(Resource):

    @security.http(
        # login_required=True
    )
    def get(self):
        debug(request.headers)
        return {'hello': 'world'}

    @security.http(
        form_data=HelloSchema(),  # form_data
        params=HelloSchema(),  # params
        login_required=True  # user
    )
    def post(self, form_data, params, user):

        return {}
