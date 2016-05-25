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

    def lookup(self, sstring, expected):
        response = self.api.request({'key': self.key, 'searchstring': sstring})
        returned = response['ResponseData'][0]['Name']
        assert_equals(returned, expected)

    def test_tekniska_hogskolan(self):
        self.lookup("teknisk", "Tekniska högskolan (Stockholm)")

    def test_varsta(self):
        self.lookup("vårsta", "Vårsta centrum (Botkyrka)")

    def teardown(self):
        pass
