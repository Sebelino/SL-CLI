#!/usr/bin/env python

from nose.tools import assert_equal
from ..keyreader import get_keys
from ..apis.platsuppslag import api as pu_api
from ..apis.reseplanerare3 import tripapi as trip_api
from ..apis.reseplanerare3 import journeydetailapi as jd_api


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


class TestReseplanerare3:
    @classmethod
    def setup_class(cls):
        cls.trip_api = trip_api
        cls.jd_api = jd_api
        cls.key = get_keys()['reseplanerare3']

    def test_trip_suggestions_count(self):
        params = [
            (7305, 9204, '08:00'),
        ]
        for a, b, t in params:
            d = {'key': self.key, 'originId': a, 'destId': b, 'time': t}
            response = self.trip_api.request(d)
            tripcount = len(response['Trip'])
            expected = 5
            yield assert_equal, tripcount, expected
