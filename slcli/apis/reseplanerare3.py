#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slcli.apis.api import API, cli

tripapi = API(r'https://api.sl.se/api2/TravelplannerV3/trip.json', {
    'key': {'required': True, 'description': "Din API-nyckel.", 'position': 1},
    'originId': {'required': True,
                 'description': "ID för startpunkten.",
                 'position': 2},
    'destId': {'required': True, 'domain': bool,
               'description': "ID för destinationen.",
               'position': 3},
    'time': {'required': True, 'domain': str, 'description': "Tidpunkt, format: HH:MM",
             'position': 4},
    'lang': {'required': False, 'domain': {"de", "sv", "en"}, 'default': "de",
             'description': "Språket som resultaten presenteras i."},
})

journeydetailapi = \
    API(r'https://api.sl.se/api2/TravelplannerV3/journeydetail.json', {
        'key': {'required': True, 'description': "Din API-nyckel.",
                'position': 1},
        'id': {'required': True, 'description': "Referensparameter erhållen "
                "från tidigare trip-sökning.", 'position': 2},
    })

if __name__ == '__main__':
    cli(tripapi)
