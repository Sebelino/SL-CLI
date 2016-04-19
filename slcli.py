#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from pprint import pprint
import re,argparse

from reseplanerare2 import tripapi, journeydetailapi as japi
from platsuppslag import api as papi
from api import requestURL, API, unquote
from keyreader import read_keys
from collections import OrderedDict

""" :returns: Properties of the trip
    :param origin: Location of the origin
    :param destination: Location of the destination
    :param time: When to depart
    The origin and destination do not need to perfectly match the actual names in the API.
"""
def travel(origin,destination,time):
    apikeys = read_keys()

    def sitedata(searchstring):
        presponse = papi.request({'key':apikeys['platsuppslag'],'searchstring':searchstring})
        topentry = presponse['ResponseData'][0]
        return {'name':topentry['Name'],'id':topentry['SiteId']}

    startpoint = sitedata(origin)
    endpoint = sitedata(destination)

    rresponse = tripapi.request({'key':apikeys['reseplanerare2'],'originId':startpoint['id'],'destId':endpoint['id'],'time':time})
    trips = rresponse['TripList']['Trip']
    toptrip = trips[0]['LegList']['Leg']
    subtrips = []
    for st in toptrip:
        if 'JourneyDetailRef' in st:
            refvalue = unquote(st['JourneyDetailRef']['ref'][6:])
            sstsresponse = japi.request({'key': apikeys['reseplanerare2'],
                                         'ref': refvalue})
            stops = sstsresponse['JourneyDetail']['Stops']['Stop'][1:]
            subsubtrips = [{'arrivalTime': s['arrTime'], 'destination':
                            s['name']} for s in stops]
        else:
            subsubtrips = []
        st = {
            'departureTime': st['Origin']['time'],
            'origin': st['Origin']['name'],
            'trip': subsubtrips,
            'arrivalTime': st['Destination']['time'],
            'destination': st['Destination']['name'],
        }
        subtrips.append(st)
    result = {
        'departureDate': toptrip[0]['Origin']['date'],
        'departureTime': toptrip[0]['Origin']['time'],
        'origin':startpoint['name'],
        'destination':endpoint['name'],
        'trip' : subtrips,
    }
    return result


""" Pretty-printing.
"""
def printtrip(trip):
    header = "%s %s %s - %s:"% (trip['departureTime'],trip['departureDate'],trip['origin'],trip['destination'])
    print(header)
    for subtrip in trip['trip']:
        originstr = u'{}....{}'.format(subtrip['departureTime'],
                                      subtrip['origin'])
        print(originstr)
        for subsubtrip in subtrip['trip']:
            t = subsubtrip['arrivalTime']
            d = subsubtrip['destination']
            intermediatestr = t+u'.'*8+d
            print(intermediatestr)
        destinationstr = u'{}....{}'.format(subtrip['arrivalTime'],
                                           subtrip['destination'])
        print(destinationstr)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('origin',metavar='from',help="Varifrån ska du resa?")
    parser.add_argument('to',help="Vart ska du?")
    parser.add_argument('at',help="När ska du bege dig?")
    args = parser.parse_args()
    results = travel(args.origin,args.to,args.at)
    printtrip(results)
