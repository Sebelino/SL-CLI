#!/usr/bin/env python

from nose.tools import raises, assert_equal
from ..apis.api import request_url
from random import randint
from urllib.error import URLError


class TestRequestURL:
    @staticmethod
    def guard(*args, **kwargs):
        raise Exception("Internet access intentionally blocked.")

    def request_url(self, filename, expected):
        baseurl = ("https://raw.githubusercontent.com/Sebelino/SL-CLI/devel/slc"
                   "li/test/assets/json/")
        url = baseurl+filename
        returned = request_url(url, 5)
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

    @raises(URLError)
    def test_inaccessible_url(self):
        randomstr = str(randint(10**5, 10**6))
        self.request_url(randomstr, dict())
