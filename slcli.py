#!/usr/bin/python2.7

from urllib2 import urlopen
import sensitive

time = '9:15'
start = 9506
stop = 9526
urltemplate = r'https://api.trafiklab.se/sl/reseplanerare.json?key=%s&S=%s&Z=%s&time=%s'
url = urltemplate % (sensitive.apikey,start,stop,time)

print url
jsonresponse = urlopen(url).read()
print jsonresponse

