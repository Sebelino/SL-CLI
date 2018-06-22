#!/usr/bin/env python

from nose.tools import assert_equal
import os
from os.path import dirname, realpath, join
from ..keyreader import read_keys


class TestReadKeys:
    @classmethod
    def setup_class(cls):
        xmlcontents = """
<?xml version='1.0' encoding='utf-8'?>
<root>
    <key name="platsuppslag"  >abcdef</key>
    <key name="reseplanerare3">123456789</key>
</root>
        """.strip()
        cls.path = join(dirname(realpath(__file__)), "test.xml")
        outfile = open(cls.path, 'w')
        outfile.write(xmlcontents)

    def test_read_keys(self):
        returned = read_keys(self.path)
        assert_equal(returned["platsuppslag"], "abcdef")
        assert_equal(returned["reseplanerare3"], "123456789")

    @classmethod
    def teardown_class(cls):
        os.remove(cls.path)
        cls.path
