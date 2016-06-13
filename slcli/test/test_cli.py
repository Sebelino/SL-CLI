#!/usr/bin/env python

from nose.tools import assert_equal
from ..slcli import trip2str


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
