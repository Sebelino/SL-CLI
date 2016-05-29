#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .api import API, cli

api = API(r'https://api.sl.se/api2/typeahead.json', {
    'key': {'required': True, 'description': "Din API-nyckel.", 'position': 1},
    'searchstring': {'required': True, 'position': 2,
                     'description': "Söksträngen."},
    'stationsonly': {'required': False, 'domain': bool, 'default': True,
                     'description':
                     "Om \"True\" returneras endast hållplatser."},
    'maxresults': {'required': False, 'domain': range(50+1), 'default': 10,
                   'description': "Maximalt antal resultat som önskas."},
})

if __name__ == '__main__':
    cli(api)
