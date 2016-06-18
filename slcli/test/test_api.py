#!/usr/bin/env python

from nose.tools import raises, assert_equal
from ..apis.api import requestURL
import socket


class TestRequestURL:
    @classmethod
    def setup_class(cls):
        cls.oldsocket = socket.socket

    @staticmethod
    def guard(*args, **kwargs):
        raise Exception("Internet access intentionally blocked.")

    def request_url(self, filename, expected):
        baseurl = ("https://raw.githubusercontent.com/Sebelino/SL-CLI/devel/slc"
                   "li/test/assets/json/")
        url = baseurl+filename
        returned = requestURL(url)
        assert_equal(returned, expected)

    def test_empty_json(self):
        self.request_url("empty.json", dict())

    def test_nontrivial_json(self):
        expected = {
            "glossary": {
                "title": "example glossary",
                "GlossDiv": {
                    "title": "S",
                    "GlossList": {
                        "GlossEntry": {
                            "ID": "SGML",
                            "SortAs": "SGML",
                            "GlossTerm": "Standard Generalized Markup Language",
                            "Acronym": "SGML",
                            "Abbrev": "ISO 8879:1986",
                            "GlossDef": {
                                "para": ("A meta-markup language, used to creat"
                                         "e markup languages such as DocBook."),
                                "GlossSeeAlso": ["GML", "XML"]
                            },
                            "GlossSee": "markup"
                        }
                    }
                }
            }
        }
        self.request_url("nontrivial.json", expected)

    @raises(ValueError)
    def test_non_json(self):
        self.request_url("nonjson.txt", dict())

    @raises(Exception)
    def test_closed_socket(self):
        socket.socket = self.guard
        requestURL(self.url)

    def teardown(self):
        """ Restore internet connection in case it was blocked """
        socket.socket = self.oldsocket
