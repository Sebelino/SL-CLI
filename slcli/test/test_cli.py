#!/usr/bin/env python

from nose.tools import assert_equal, assert_less_equal
from ..slcli import travel, trip2str, main
from datetime import datetime, timedelta
import sys
from io import StringIO
from argparse import Namespace


def assert_matches(string, pattern, single_char, lines_char):
    """ Raises AssertionError if the string does not match the pattern """
    slines = string.strip().split("\n")
    paragraphs = pattern.split(lines_char)
    plines = [p.strip().split("\n") for p in paragraphs]
    delta = len(slines)-sum(len(lines) for lines in plines)
    missing = slines[len(plines[0]):len(plines[0])+delta]
    plines[1:1] = [missing]
    plines = [line for lines in plines for line in lines]
    for sline, pline in zip(slines, plines):
        if len(sline) != len(pline):
            assert_equal(sline, pline)
        s2line = "".join(s if s == "´" else p for s, p in zip(sline, pline))
        assert_equal(s2line, pline)


def test_trip2str():
    sample_trip = {
        'departureTime': '12:21',
        'trip': [
            {
                'departureTime': '12:21',
                'trip': [
                    {
                        'stop': 'Malmtorp',
                        'arrivalTime': '12:22'
                    }, {
                        'stop': 'Bergudden',
                        'arrivalTime': '12:23'
                    }, {
                        'stop': 'Kassmyra',
                        'arrivalTime': '12:25'
                    }, {
                        'stop': 'Skäcklinge',
                        'arrivalTime': '12:27'
                    }, {
                        'stop': 'Skäcklinge gårdsväg',
                        'arrivalTime': '12:28'
                    }, {
                        'stop': 'Lövholmenvägen',
                        'arrivalTime': '12:30'
                    }, {
                        'stop': 'Toppvägen',
                        'arrivalTime': '12:31'
                    }, {
                        'stop': 'Hålvägen',
                        'arrivalTime': '12:33'
                    }, {
                        'stop': 'Passvägen',
                        'arrivalTime': '12:34'
                    }
                ],
                'origin': 'Vårsta centrum',
                'destination': 'Tumba station',
                'arrivalTime': '12:38'
            }, {
                'departureTime': '12:48',
                'trip': [
                    {
                        'stop': 'Tullinge',
                        'arrivalTime': '12:52'
                    }, {
                        'stop': 'Flemingsberg',
                        'arrivalTime': '12:55'
                    }, {
                        'stop': 'Huddinge',
                        'arrivalTime': '12:58'
                    }, {
                        'stop': 'Stuvsta',
                        'arrivalTime': '13:01'
                    }, {
                        'stop': 'Älvsjö',
                        'arrivalTime': '13:04'
                    }, {
                        'stop': 'Årstaberg',
                        'arrivalTime': '13:07'
                    }, {
                        'stop': 'Stockholms södra',
                        'arrivalTime': '13:10'
                    }
                ],
                'origin': 'Tumba',
                'destination': 'Stockholms central',
                'arrivalTime': '13:14'
            }, {
                'departureTime': '13:22',
                'trip': [
                    {
                        'stop': 'Östermalmstorg',
                        'arrivalTime': '13:25'
                    }, {
                        'stop': 'Stadion',
                        'arrivalTime': '13:26'
                    }
                ],
                'origin': 'T-Centralen',
                'destination': 'Tekniska högskolan',
                'arrivalTime': '13:28'
            }
        ],
        'origin': 'Vårsta centrum (Botkyrka)',
        'destination': 'Tekniska högskolan (Stockholm)',
        'departureDate': '2016-06-13'
    }
    returned = trip2str(sample_trip)
    returned = returned.strip()
    expected = """
12:21 2016-06-13 Vårsta centrum (Botkyrka) - Tekniska högskolan (Stockholm):
12:21....Vårsta centrum
12:22........Malmtorp
12:23........Bergudden
12:25........Kassmyra
12:27........Skäcklinge
12:28........Skäcklinge gårdsväg
12:30........Lövholmenvägen
12:31........Toppvägen
12:33........Hålvägen
12:34........Passvägen
12:38....Tumba station
12:48....Tumba
12:52........Tullinge
12:55........Flemingsberg
12:58........Huddinge
13:01........Stuvsta
13:04........Älvsjö
13:07........Årstaberg
13:10........Stockholms södra
13:14....Stockholms central
13:22....T-Centralen
13:25........Östermalmstorg
13:26........Stadion
13:28....Tekniska högskolan
    """.strip()
    for rline, eline in zip(returned.split("\n"), expected.split("\n")):
        assert_equal(rline, eline)
    assert_equal(returned, expected)


class TestTravelToKTH:
    @classmethod
    def setup_class(cls):
        cls.params = ["vårsta", "teknisk", "12:00"]
        cls.returned = travel(*cls.params)

    def test_origin(self):
        ret = self.returned["origin"]
        assert_equal(ret, "Vårsta centrum (Botkyrka)")

    def test_destination(self):
        ret = self.returned["destination"]
        assert_equal(ret, "Tekniska högskolan (Stockholm)")

    def test_trip_length(self):
        ret = len(self.returned["trip"])
        assert_equal(ret, 3)

    def test_time(self):
        astr = self.returned["departureTime"]
        bstr = self.returned["trip"][-1]["arrivalTime"]
        a = datetime.strptime(astr, "%H:%M")
        b = datetime.strptime(bstr, "%H:%M")
        delta = b-a
        if delta.days < 0:
            delta = delta+timedelta(days=1)
        # We do not yet have the technology to make it below 30 minutes:
        assert_less_equal(30, delta.total_seconds()/60)
        # Should take well below 2 hours:
        assert_less_equal(delta.total_seconds()/60, 120)


class TestMain:
    def setup(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.mystdout = StringIO()

    def test_main(self):
        main(Namespace(origin="vårsta", to="teknisk", at="12:00",
                       verbose=False))
        returned = self.mystdout.getvalue()
        sys.stdout = self.old_stdout
        # There are two possibile routes here:
        expected = """
12:´´ 20´´-´´-´´ Vårsta centrum (Botkyrka) - Tekniska högskolan (Stockholm):
12:´´....Vårsta centrum
1´:´´........Malmtorp
1´:´´........Bergudden
1´:´´........Kassmyra
*
1´:´´....Tumba station
1´:´´....Tumba
1´:´´........Tullinge
1´:´´........Flemingsberg
1´:´´........Huddinge
1´:´´........Stuvsta
1´:´´........Älvsjö
1´:´´........Årstaberg
1´:´´........Stockholms södra
1´:´´....Stockholms central
1´:´´....T-Centralen
1´:´´........Östermalmstorg
1´:´´........Stadion
1´:´´....Tekniska högskolan
        """
        assert_matches(returned, expected, "´", "*")

    def teardown(self):
        sys.stdout = self.old_stdout
