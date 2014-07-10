#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import argparse,sys,urllib,urllib2,json
from copy import deepcopy

""" URL -> dict """
""" Returns None if the site could not be accessed. """
def requestURL(url):
    print "Requesting URL: %s"% url
    try:
        jsonresponse = urllib2.urlopen(url).read().decode('iso-8859-1')
    except urllib2.URLError:
        print 'Kunde inte öppna URL. Är din internetuppkoppling nere?'
        return None
    dictresponse = json.loads(jsonresponse)
    return dictresponse

def cli(api):
    parser = argparse.ArgumentParser()
    for (a,b) in api.interface():
        optionalprefix = '' if b['required'] else '--'
        parser.add_argument('%s%s'% (optionalprefix,a),default=b['default'] if 'default' in b else '',help=b['description'])
    args = parser.parse_args()
    response = api.request(vars(args))
    if not response:
        sys.exit()
    print response

class API:

    """
        param: baseurl
    """
    def __init__(self,baseurl,interface):
        self._baseurl = baseurl
        self._interface = interface

    """
        returns: An URL with the parameters and its respecive parameters added.
        Example: https://api.sl.se/api2/typeahead.json?key=123abc&searchstring=Vårsta
    """
    def context(self,values):
        filteredvals = dict((k,v) for k,v in values.items() if v)
        for key,_ in filteredvals.iteritems():
            if key not in self._interface:
                raise Exception("Parameter %s not in this API."% key)
        s = self._baseurl+'?'+urllib.urlencode(filteredvals)
        return s

    def __str__(self):
        s = 'Baseurl: %s\n'% self._baseurl
        for param,helpstr in self._interface.iteritems():
            s += '%s : %s\n'% (param,helpstr)
        s = s.rstrip()
        return s

    def interface(self):
        return self._interface.iteritems()

    def request(self,values):
        return requestURL(self.context(values))

if __name__ == '__main__':
    print "Sample API instance:"
    testapi = API('https://api.sl.se/api2/typeahead.json',{
        'key' : "API-nyckel",
        'searchstring' : "Söksträng för platsen",
    })
    print str(testapi)
    vals = {'key':'1234abcd','searchstring':"Vårsta"}
    print "\nSample URL with %s:"% vals
    print testapi.context(vals)
    print "Iterating over the API parameters:"
    for (a,b) in testapi.interface():
        print '%s -> %s'% (a,b)

