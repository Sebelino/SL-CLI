#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from pprint import pprint
import re,argparse

from reseplanerare import api as rapi
from platsuppslag import api as papi
from api import requestURL,API
from keyreader import read_keys

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
    time = '20:15'

    rresponse = rapi.request({'key':apikeys['reseplanerare'],'s':startpoint['id'],'z':endpoint['id'],'time':time})
    trip = {'Origin':startpoint['name'],'Destination':endpoint['name'],'trip' : []}
    for subtrip in rresponse['HafasResponse']['Trip'][0]['SubTrip']:
        st = {'Origin':subtrip['Origin']['#text'],'Destination':subtrip['Destination']['#text'],'trip':[]}
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
        trip['trip'].append(st)
    return trip

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('origin',metavar='from',help="Varifrån ska du resa?")
    parser.add_argument('to',help="Vart ska du?")
    parser.add_argument('at',help="När ska du bege dig?")
    args = parser.parse_args()
    results = travel(args.origin,args.to,args.at)
    pprint(results)

