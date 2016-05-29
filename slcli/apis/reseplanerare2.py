#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .api import API, cli

tripapi = API(r'http://api.sl.se/api2/TravelplannerV2/trip.json', {
    'key': {'required': True, 'description': "Din API-nyckel.", 'position': 1},
    'originId': {'required': True,
                 'description': "Namn eller ID för startpunkten.",
                 'position': 2},
    'destId': {'required': True, 'domain': bool,
               'description': "Namn eller ID för destinationen.",
               'position': 3},
    'time': {'required': True, 'domain': str, 'description': "Tidpunkt.",
             'position': 4},
    'lang': {'required': False, 'domain': {"sv", "en"}, 'default': "sv",
             'description': "Språket som resultaten presenteras i."},
})

journeydetailapi = \
    API(r'http://api.sl.se/api2/TravelplannerV2/journeydetail.json', {
        'key': {'required': True, 'description': "Din API-nyckel.",
                'position': 1},
        'ref': {'required': True, 'description': "Referensparameter erhållen "
                "från tidigare trip-sökning.", 'position': 2},
    })

if __name__ == '__main__':
    cli(tripapi)
