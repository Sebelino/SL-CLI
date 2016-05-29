#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import urllib.parse
import json
import xmltodict
import logging


def requestURL(url, retries=10):
    """ URL -> dict.
        :raises: Exception if the site could not be accessed """
    logging.debug("Requesting URL: {}".format(url))
    try:
        responsebytes = urllib.request.urlopen(url).read()
        response = responsebytes.decode('utf8')
    except urllib.error.URLError:
        return requestURL(url, retries-1)
        raise Exception("Kunde inte öppna URL. Felaktig URL, eller så är din"
                        " internetuppkoppling nere.")
        return None
    try:
        dictresponse = json.loads(response)
    except ValueError:
        dictresponse = xmltodict.parse(response)
    return dictresponse


def unquote(ustr):
    return urllib.parse.unquote(ustr)


def cli(api):
    """ Enables the user to specify command-line arguments. """
    parser = argparse.ArgumentParser()
    interface = api.interface()
    positions = [(interface[k]['position'], k) for k in interface
                 if 'position' in interface[k]]
    positions.sort(key=lambda pair: pair[0])
    unpositioned = [k for k in interface if interface[k]['required']
                    and k not in {f for (_, f) in positions}]
    fields = [k for (n, k) in positions]+unpositioned
    for k in fields:
        props = interface[k]
        optionalprefix = '' if props['required'] else '--'
        parser.add_argument('{}{}'.format(optionalprefix, k),
                            default=props['default']
                            if 'default' in props else '',
                            help=props['description'])
    args = parser.parse_args()
    argdict = vars(args)
    argdict = dict([(arg, val) for arg, val in argdict.items() if 'default' not
                    in interface[arg]])
    response = api.request(argdict)
    if not response:
        sys.exit()
    print(json.dumps(response))


class API:
    """ Any API associated with trafiklab.se. """

    def __init__(self, baseurl, interface):
        """
        :param baseurl: Entry point URL for the API
        :param interface: Properties of the query parameters
        """
        self._baseurl = baseurl
        self._interface = interface

    def context(self, values):
        """
        :returns: An URL with the parameters and its respecive parameters added.
        Example:
        https://api.sl.se/api2/typeahead.json?key=123abc&searchstring=Vårsta
        """
        for key, _ in values.items():
            if key not in self._interface:
                raise Exception("Parameter {} not in this API.".format(key))
        s = self._baseurl+'?'+urllib.parse.urlencode(values)
        return s

    def __str__(self):
        s = 'Baseurl: {}\n'.format(self._baseurl)
        for param, helpstr in self._interface.items():
            s += '{} : {}\n'.format(param, helpstr)
        s = s.rstrip()
        return s

    def interface(self):
        return self._interface

    def request(self, values):
        return requestURL(self.context(values))

if __name__ == '__main__':
    print("Sample API instance:")
    testapi = API('https://api.sl.se/api2/typeahead.json', {
        'key': "API-nyckel",
        'searchstring': "Söksträng för platsen",
    })
    print(str(testapi))
    vals = {'key': '1234abcd', 'searchstring': "Vårsta"}
    print("\nSample URL with {}:".format(vals))
    print(testapi.context(vals))
    print("Iterating over the API parameters:")
    for (a, b) in testapi.interface().items():
        print('{} -> {}'.format(a, b))
