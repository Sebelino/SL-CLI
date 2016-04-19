#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from api import API, cli

api = API(r'https://api.sl.se/api2/TravelplannerV2/trip.json', {
    'key': {'required': True, 'description': "Din API-nyckel."},
    'originId': {'required': True,
                 'description': "Namn eller ID för startpunkten."},
    'destId': {'required': True, 'domain': bool,
               'description': "Namn eller ID för destinationen."},
    'time': {'required': True, 'domain': str, 'description': "Tidpunkt."},
    'lang': {'required': False, 'domain': set(["sv", "en"]), 'default': "sv",
             'description': "Språket som resultaten presenteras i."},
})

if __name__ == '__main__':
    cli(api)
