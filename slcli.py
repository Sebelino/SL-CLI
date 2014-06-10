#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from urllib2 import urlopen
from sys import exit

try:
    import sensitive
except ImportError:
    print "Det verkar inte finnas en sensitive.py i din katalog. Läs installationsinstruktionerna."
    exit(1)

time = '9:15'
start = 9506
stop = 9526
urltemplate = r'https://api.trafiklab.se/sl/reseplanerare.json?key=%s&S=%s&Z=%s&time=%s'
url = urltemplate % (sensitive.apikey,start,stop,time)

print url
jsonresponse = urlopen(url).read()
print jsonresponse

