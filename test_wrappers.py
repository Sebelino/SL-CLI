#!/usr/bin/env python

from nose.tools import assert_equal
from keyreader import get_keys
from platsuppslag import api as pu_api


class TestPlatsuppslag:
    @classmethod
    def setup_class(cls):
        cls.api = pu_api
        cls.key = get_keys()['platsuppslag']

    def test_lookup(self):
        params = {
            "teknisk": "Tekniska högskolan (Stockholm)",
            "vårsta": "Vårsta centrum (Botkyrka)",
        }
        for sstring in params:
            expected = params[sstring]
            d = {'key': self.key, 'searchstring': sstring}
            response = self.api.request(d)
            returned = response['ResponseData'][0]['Name']
            yield assert_equal, returned, expected


