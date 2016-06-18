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

    def test_empty_json(self):
        branch = "devel"
        url = ("https://github.com/Sebelino/SL-CLI/tree/{}/slcli/test/assets/js"
               "on/empty.json").format(branch)
        returned = requestURL(url)
        expected = {}
        assert_equal(returned, expected)

    def test_nontrivial_json(self):
        assert False

    def test_non_json(self):
        assert False

    @raises(Exception)
    def test_closed_socket(self):
        socket.socket = self.guard
        requestURL(self.url)

    def teardown(self):
        """ Restore internet connection in case it was blocked """
        socket.socket = self.oldsocket
