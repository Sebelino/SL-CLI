#!/usr/bin/env python

from nose.tools import assert_equal, assert_less_equal, assert_greater_equal
from slcli.sl_cli import travel, trip2str, main
from datetime import datetime, timedelta
import sys
import re
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
        s2line = "".join(s if s == single_char else p for s, p in zip(sline, pline))
        assert_equal(s2line, pline)


def dag_paths(dag):
    """ :return A frozenset containing every path (v1,v2,...,vn) such that each vi is nested within @dag and
    is a direct element of at most one set.
    :param @dag A nested structure of elements where each element is a string, a tuple or a frozenset. """
    if dag == ():
        return {()}
    elif isinstance(dag[0], str):
        return frozenset([(dag[0],) + t for t in dag_paths(dag[1:])])
    elif isinstance(dag[0], tuple):
        return dag_paths(dag[0] + dag[1:])
    elif isinstance(dag[0], frozenset):
        setofsets = frozenset([dag_paths((e,) + dag[1:]) for e in dag[0]])
        return frozenset([x for y in setofsets for x in y])
    else:
        raise TypeError("Unexpected type: {}".format(type(dag[0])))


def assert_matches_dag(string, dag, single_char, lines_char):
    """ :raise AssertionError if there is no path through the directed acyclic graph @dag such that
    @string matches the pattern given by the path.
    :param @dag A nested structure of elements where each element is a string, a tuple or a frozenset. The
    structure is isomorphic to a (transitively reduced) DAG in which every vertex is a string. The
    concatenation of the vertices along any path in the DAG becomes a pattern which @string is
    matched against. """
    paths = dag_paths(dag)
    patterns = {'\n'.join(v.strip() for v in p) for p in paths}
    for pattern in patterns:
        try:
            assert_matches(string, pattern, single_char, lines_char)
            break
        except AssertionError:
            pass
    else:  # If no match:
        raise AssertionError("--- Output: ---\n{}\n--- did not match any of the following {} patterns: ---\n{}".format(string, len(patterns), '\n\n'.join(patterns)))


def assert_matches_regex(string, pattern):
    r = re.compile(pattern)
    assert r.fullmatch(string), "--- Returned output: ---\n{}\n--- does not match regex ---\n{}".format(string, pattern)


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
        #assert_equal(ret, 3)  # General case
        assert_greater_equal(ret, 3)  # Vårsta -> Tumba -> T-Centralen -> Tekniska högskolan [-> ...]
        assert_less_equal(ret, 7)  # Not even SL could break this assertion

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
        # Should take well below 2 hours (hopefully):
        assert_less_equal(delta.total_seconds()/60, 120)


class TestMain:
    def setup(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.mystdout = StringIO()

    def test_varsta_to_teknisk(self):
        main(Namespace(origin="vårsta", to="teknisk", at="12:00",
                       verbose=False))
        returned = self.mystdout.getvalue()
        sys.stdout = self.old_stdout
        expected_regex = ("""
1\d:\d\d 20\d\d-\d\d-\d\d Vårsta centrum \(Botkyrka\) - Tekniska högskolan \(Stockholm\):
1\d:\d\d\.{4}Vårsta centrum
1\d:\d\d\.{4}\.{4}Malmtorp
1\d:\d\d\.{4}\.{4}Bergudden
1\d:\d\d\.{4}\.{4}Kassmyra
.*
1\d:\d\d\.{4}Tumba station
1\d:\d\d\.{4}Tumba
1\d:\d\d\.{4}\.{4}Tullinge
1\d:\d\d\.{4}\.{4}Flemingsberg
1\d:\d\d\.{4}\.{4}Huddinge
1\d:\d\d\.{4}\.{4}Stuvsta
1\d:\d\d\.{4}\.{4}Älvsjö
1\d:\d\d\.{4}\.{4}Årstaberg
1\d:\d\d\.{4}\.{4}Stockholms södra
(
        """.strip() + """
1\d:\d\d\.{4}Stockholm City
1\d:\d\d\.{4}T-Centralen
1\d:\d\d\.{4}\.{4}Östermalmstorg
1\d:\d\d\.{4}\.{4}Stadion
1\d:\d\d\.{4}Tekniska högskolan
        """.strip() + "|" + """
1\d:\d\d\.{4}\.{4}Stockholm City
1\d:\d\d\.{4}Stockholm Odenplan
1\d:\d\d\.{4}Odenplan
1\d:\d\d\.{4}\.{4}Stadsbiblioteket
1\d:\d\d\.{4}\.{4}Roslagsgatan
1\d:\d\d\.{4}\.{4}Valhallavägen
1\d:\d\d\.{4}Östra station
        """.strip() + """
)""".strip())
        #assert_matches_regex(returned, expected_regex)  # Screw regex; too hard to debug!

        expected_dag = (
            """
12:´´ 20´´-´´-´´ Vårsta centrum (Botkyrka) - Tekniska högskolan (Stockholm):
12:´´....Vårsta centrum
1´:´´........Malmtorp
1´:´´........Bergudden
1´:´´........Kassmyra
            """, frozenset({  # Long route: bus 716; short route: 717/727/279
                """
1´:´´........Skäcklinge
1´:´´........Skäcklinge gårdsväg
1´:´´........Lövholmenvägen
1´:´´........Toppvägen
1´:´´........Hålvägen
1´:´´........Passvägen
                """,
                """
1´:´´........Skrävstavägen
1´:´´........Solbo
                """,
            }),
            """
1´:´´....Tumba station
1´:´´....Tumba
1´:´´........Tullinge
1´:´´........Flemingsberg
1´:´´........Huddinge
1´:´´........Stuvsta
1´:´´........Älvsjö
1´:´´........Årstaberg
1´:´´........Stockholms södra
            """, frozenset({  # Usual route; other routes are exceptional
                """
1´:´´....Stockholm City
1´:´´....T-Centralen
1´:´´........Östermalmstorg
1´:´´........Stadion
1´:´´....Tekniska högskolan
                """,
                """
1´:´´........Stockholm City
1´:´´....Stockholm Odenplan
1´:´´....Odenplan
1´:´´........Stadsbiblioteket
1´:´´........Roslagsgatan
1´:´´........Valhallavägen
1´:´´....Östra station
                """,
                """
1´:´´....Stockholm City
1´:´´....T-Centralen
1´:´´........Östermalmstorg
1´:´´....Karlaplan
1´:´´....Värtavägen
1´:´´........Jungfrugatan
1´:´´........Musikhögskolan
1´:´´........Stadion (på Valhallavägen)
1´:´´....Östra station
                """,
            }),

        )
        assert_matches_dag(returned, expected_dag, "´", "*")


    def test_varsta_to_tumba(self):
        main(Namespace(origin="vårsta", to="tumba", at="23:00",
                       verbose=False))
        returned = self.mystdout.getvalue()
        sys.stdout = self.old_stdout
        # Long route: bus 716; short route: 717/727/279
        expected = """
23:´´ 20´´-´´-´´ Vårsta centrum (Botkyrka) - Tumba (Botkyrka):
23:´´....Vårsta centrum
´´:´´........Malmtorp
´´:´´........Bergudden
´´:´´........Kassmyra
*
´´:´´....Tumba station
        """
        assert_matches(returned, expected, "´", "*")

    def teardown(self):
        sys.stdout = self.old_stdout
