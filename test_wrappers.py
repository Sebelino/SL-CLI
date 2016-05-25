#!/usr/bin/env python

from nose.tools import assert_equals
from keyreader import read_keys
from platsuppslag import api as pu_api


class TestPlatsuppslag:
    @classmethod
    def setup_class(cls):
        cls.api = pu_api
        cls.key = read_keys()['platsuppslag']

    def setup(self):
        pass

    def test_tekniska_hogskolan(self):
        response = self.api.request({'key': self.key,
                                     'searchstring': 'teknisk'})
        returned = response['ResponseData'][0]['Name']
        expected = "Tekniska högskolan (Stockholm)"
        assert_equals(returned, expected)

    def teardown(self):
        pass
