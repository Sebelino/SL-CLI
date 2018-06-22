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

from slcli.apis.reseplanerare3 import tripapi, journeydetailapi as japi
from slcli.apis.platsuppslag import api as papi
from slcli.keyreader import get_keys
from slcli.keyreader import KeysNotFoundError


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

    rresponse = tripapi.request({'key': apikeys['reseplanerare3'], 'originId':
                                 startpoint['id'], 'destId': endpoint['id'],
                                 'time': time, 'lang': 'sv'})
    trips = rresponse['Trip']
    toptrip = trips[0]['LegList']['Leg']
    subtrips = []
    if isinstance(toptrip, dict):
        received_subtrips = [toptrip]
    elif isinstance(toptrip, list):
        received_subtrips = toptrip
    else:
        errmsg = "Expected top trip to be list or dict; received type: {}"
        raise RuntimeError(errmsg.format(type(toptrip)))
    for st in received_subtrips:
        if st['type'] == 'WALK':  # Skip information about walking
            continue
        if 'JourneyDetailRef' in st:
            refvalue = unquote(st['JourneyDetailRef']['ref'])
            sstsresponse = japi.request({'key': apikeys['reseplanerare3'],
                                         'id': refvalue})
            try:
                allstops = sstsresponse['Stops']['Stop']
            except KeyError:
                raise  # In rare cases, key 'Stops' is not found for some reason
            oid = st['Origin']['id']
            did = st['Destination']['id']
            sameid = [s['id'] in {oid, did} for s in allstops]
            (oindex, dindex) = [i for i, e in enumerate(sameid) if e]
            stops = allstops[oindex+1:dindex]
            subsubtrips = [{'arrivalTime': truncate_time(s['arrTime']), 'stop':
                            s['name']} for s in stops]
        else:
            subsubtrips = []
        subtrip = {
            'departureTime': truncate_time(st['Origin']['time']),
            'origin': st['Origin']['name'],
            'trip': subsubtrips,
            'arrivalTime': truncate_time(st['Destination']['time']),
            'destination': st['Destination']['name'],
        }
        subtrips.append(subtrip)
    result = {
        'departureDate': received_subtrips[0]['Origin']['date'],
        'departureTime': truncate_time(received_subtrips[0]['Origin']['time']),
        'origin': startpoint['name'],
        'destination': endpoint['name'],
        'trip': subtrips,
    }
    return result


def truncate_time(time_string: str):
    """ HH:MM:SS -> HH:MM """
    return ':'.join(time_string.split(':')[:2])


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
                os.makedirs(os.path.dirname(dstpath), exist_ok=True)
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
