# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json

register_domain_event_type = None
with open("blockchain/event_type/RegisterDomain.json") as file:
    register_domain_event_type = json.load(file)  # load contract info as JSON