#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import argparse,sys,urllib,urllib2,json

""" URL -> dict """
""" Returns None if the site could not be accessed. """
def request(url):
    print "Requesting URL: %s"% url
    try:
        jsonresponse = urllib2.urlopen(url).read().decode('iso-8859-1')
    except urllib2.URLError:
        print 'Kunde inte öppna URL. Är din internetuppkoppling nere?'
        return None
    dictresponse = json.loads(jsonresponse)
    return dictresponse

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
        for key,value in values.iteritems():
            if key not in self._interface:
                raise Exception("Parameter %s not in this API."% key)
        s = self._baseurl+'?'+urllib.urlencode(values)
        return s

    def __str__(self):
        s = 'Baseurl: %s\n'% self._baseurl
        for param,helpstr in self._interface.iteritems():
            s += '%s : %s\n'% (param,helpstr)
        s = s.rstrip()
        return s

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

