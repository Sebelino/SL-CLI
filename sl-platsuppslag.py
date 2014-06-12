#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from urllib2 import urlopen
from sys import exit
import json
from pprint import pprint

try:
    import sensitive
except ImportError:
    print "Det verkar inte finnas en sensitive.py i din katalog. Läs installationsinstruktionerna."
    exit(1)

searchstring = 'vårsta'
urltemplate = r'https://api.sl.se/api2/typeahead.json?key=%s&searchstring=%s'
url = urltemplate % (sensitive.sl_platsuppslag,searchstring)

print url
jsonresponse = urlopen(url).read().decode('iso-8859-1')
dictresponse = json.loads(jsonresponse)
pprint(dictresponse)

