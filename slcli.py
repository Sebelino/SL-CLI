#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from pprint import pprint
import re,argparse

from reseplanerare import api as rapi
from platsuppslag import api as papi
from api import requestURL,API
from keyreader import read_keys

""" :returns: Properties of the trip
    :param origin: Location of the origin
    :param destination: Location of the destination
    :param time: When to depart
    The origin and destination do not need to perfectly match the actual names in the API.
"""
def travel(origin,destination,time):
    slapi = API('http://xml.reseplanerare.sl.se:8080/bin/query.exe/sn',{
        'ident' : {'required':True},
        'seqnr' : {'required':True},
        'L' : {'required':True},
        'getIntermediateStops' : {'required':True},
    })

    apikeys = read_keys()

    def sitedata(searchstring):
        presponse = papi.request({'key':apikeys['platsuppslag'],'searchstring':searchstring})
        topentry = presponse['ResponseData'][0]
        return {'name':topentry['Name'],'id':topentry['SiteId']}

    startpoint = sitedata(origin)
    endpoint = sitedata(destination)

    rresponse = rapi.request({'key':apikeys['reseplanerare'],'s':startpoint['id'],'z':endpoint['id'],'time':time})
    trips = rresponse['HafasResponse']['Trip']
    toptrip = trips[0]
    result = {
        'Origin':startpoint['name'],
        'Destination':endpoint['name'],
        'DepartureTime':toptrip['Summary']['DepartureTime']['#text'],
        'DepartureDate':toptrip['Summary']['DepartureDate'],
        'trip' : [],
    }
    for subtrip in toptrip['SubTrip']:
        st = {
            'Origin':subtrip['Origin']['#text'],
            'Destination':subtrip['Destination']['#text'],
            'DepartureTime':subtrip['DepartureTime']['#text'],
            'DepartureDate':subtrip['DepartureDate'],
            'ArrivalTime':subtrip['ArrivalTime']['#text'],
            'ArrivalDate':subtrip['ArrivalDate'],
            'trip':[],
        }
        intermediateurl = subtrip['IntermediateStopsQuery']

        """ Rad 1 nedanför konformerar till dokumentationen; rad 2 konformerar till det faktiska beteendet. """
        #matchings = re.search(r'intermediate/([^/]*)/([^/]*)/([^.]*).json',intermediateurl,re.I|re.U)
        matchings = re.search(r'intermediate/([^/]*)/([^/]*)/[^/]*(C[^.]*).json',intermediateurl,re.I|re.U)

        (a,b,c) = [matchings.group(i) for i in (1,2,3)]
        resp = slapi.request({'ident':a,'seqnr':b,'L':'vs_xml','getIntermediateStops':c})
        indices = ['Name','ArrivalDate','ArrivalTime','DepartureDate','DepartureTime']
        for subsubtrip in resp['HafasResponse']['IntermediateStops']['IntermediateStop']:
            insertion = dict()
            for i in indices:
                if isinstance(subsubtrip[i],basestring):
                    insertion[i] = subsubtrip[i]
                else:
                    insertion[i] = subsubtrip[i]['#text']
            st['trip'].append(insertion)
        result['trip'].append(st)
    return result

""" Pretty-printing.
"""
def printtrip(trip):
    header = "%s %s %s - %s"% (trip['DepartureTime'],trip['DepartureDate'],trip['Origin'],trip['Destination'])
    print header.encode('cp1252')
    maxlength = 0
    for subtrip in trip['trip']:
        for subsubtrip in subtrip['trip']:
            maxlength = max(maxlength,len(subsubtrip['Name']))
    for subtrip in trip['trip']:
        print "%s....%s"% (subtrip['DepartureTime'],subtrip['Origin'])
        for subsubtrip in subtrip['trip']:
            n = subsubtrip['Name']+' '*(maxlength-len(subsubtrip['Name']))
            dt = subsubtrip['DepartureTime']
            dd = subsubtrip['DepartureDate']
            at = subsubtrip['ArrivalTime']
            ad = subsubtrip['ArrivalDate']
            print "%s........%s"% (dt,n)
        print "%s....%s"% (subtrip['ArrivalTime'],subtrip['Destination'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('origin',metavar='from',help="Varifrån ska du resa?")
    parser.add_argument('to',help="Vart ska du?")
    parser.add_argument('at',help="När ska du bege dig?")
    args = parser.parse_args()
    results = travel(args.origin,args.to,args.at)
    printtrip(results)

