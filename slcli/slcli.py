#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import os.path
from pprint import pformat
from time import time
from shutil import copyfile
from urllib.parse import unquote

from .apis.reseplanerare2 import tripapi, journeydetailapi as japi
from .apis.platsuppslag import api as papi
from .keyreader import get_keys
from .keyreader import KeysNotFoundError


def travel(origin, destination, time):
    """
    :returns: Properties of the trip
    :param origin: Location of the origin
    :param destination: Location of the destination
    :param time: When to depart
    The origin and destination do not need to perfectly match the actual names
    in the API.
    """
    apikeys = get_keys()

    def sitedata(searchstring):
        presponse = papi.request({'key': apikeys['platsuppslag'],
                                  'searchstring': searchstring})
        topentry = presponse['ResponseData'][0]
        return {'name': topentry['Name'], 'id': topentry['SiteId']}

    startpoint = sitedata(origin)
    endpoint = sitedata(destination)

    rresponse = tripapi.request({'key': apikeys['reseplanerare2'], 'originId':
                                 startpoint['id'], 'destId': endpoint['id'],
                                 'time': time})
    trips = rresponse['TripList']['Trip']
    toptrip = trips[0]['LegList']['Leg']
    subtrips = []
    for st in toptrip:
        if st['type'] == 'WALK':  # Skip information about walking
            continue
        if 'JourneyDetailRef' in st:
            refvalue = unquote(st['JourneyDetailRef']['ref'][6:])
            sstsresponse = japi.request({'key': apikeys['reseplanerare2'],
                                         'ref': refvalue})
            allstops = sstsresponse['JourneyDetail']['Stops']['Stop']
            oid = st['Origin']['id']
            did = st['Destination']['id']
            sameid = [s['id'] in {oid, did} for s in allstops]
            (oindex, dindex) = [i for i, e in enumerate(sameid) if e]
            stops = allstops[oindex+1:dindex]
            subsubtrips = [{'arrivalTime': s['arrTime'], 'stop':
                            s['name']} for s in stops]
        else:
            subsubtrips = []
        subtrip = {
            'departureTime': st['Origin']['time'],
            'origin': st['Origin']['name'],
            'trip': subsubtrips,
            'arrivalTime': st['Destination']['time'],
            'destination': st['Destination']['name'],
        }
        subtrips.append(subtrip)
    result = {
        'departureDate': toptrip[0]['Origin']['date'],
        'departureTime': toptrip[0]['Origin']['time'],
        'origin': startpoint['name'],
        'destination': endpoint['name'],
        'trip': subtrips,
    }
    return result


def trip2str(trip):
    """ Pretty-printing. """
    header = "{} {} {} - {}:".format(trip['departureTime'],
                                     trip['departureDate'], trip['origin'],
                                     trip['destination'])
    output = [header]
    for subtrip in trip['trip']:
        originstr = u'{}....{}'.format(subtrip['departureTime'],
                                       subtrip['origin'])
        output.append(originstr)
        for subsubtrip in subtrip['trip']:
            t = subsubtrip['arrivalTime']
            d = subsubtrip['stop']
            intermediatestr = t+u'.'*8+d
            output.append(intermediatestr)
        destinationstr = u'{}....{}'.format(subtrip['arrivalTime'],
                                            subtrip['destination'])
        output.append(destinationstr)
    return "\n".join(output)


def check_keys_installed():
    try:
        get_keys()
    except KeysNotFoundError as e:
        print("Dina API-nycklar är inte installerade.")
        srcpath = "./sensitive.xml"
        print("Ange sökvägen till dina nycklar [{}]:".format(srcpath))
        answer = input("> ")
        if answer.strip():
            srcpath = answer
        if not os.path.isfile(srcpath):
            raise KeysNotFoundError([srcpath])
        for dstpath in e.paths:
            print("Kopiera {} till {}? (y/n) [n]:".format(srcpath, dstpath))
            answer = input("> ")
            if answer.lower().strip() == 'y':
                print("Skapar kataloger...")
                os.makedirs(os.path.dirname(dstpath))
                print("Kopierar {} -> {}".format(srcpath, dstpath))
                copyfile(srcpath, dstpath)


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('origin', metavar='from', help="Varifrån ska du resa?")
    parser.add_argument('to', help="Vart ska du?")
    parser.add_argument('at', help="När ska du bege dig?")
    parser.add_argument('--verbose', '-v', action='store_true',
                        help="Skriv ut debuggutskrifter")
    check_keys_installed()
    args = args if args else parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        starttime = time()
    results = travel(args.origin, args.to, args.at)
    if args.verbose:
        logging.debug(pformat(results))
        elapsedtime = time()-starttime
        logging.debug("Elapsed request time: %f seconds", elapsedtime)
    print(trip2str(results))

if __name__ == '__main__':
    main()
