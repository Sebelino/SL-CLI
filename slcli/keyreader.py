#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import os.path
import errno
import xml.etree.ElementTree as ET
from pkg_resources import resource_stream

# XML file storing one or more paths to the XML file containing the API keys
LOCATOR_FILE = resource_stream('slcli.resources', 'locations.xml')


def get_keys():
    keys = dict()
    keys["platsuppslag"] = os.environ.get("PLATSUPPSLAG")
    keys["reseplanerare2"] = os.environ.get("RESEPLANERARE")
    if all(k is None for k in keys.values()):
        return find_keys()
    else:
        print("Found keys in environment variables. Using those...")
        return keys


def find_keys():
    """ Reads API keys from the XML files referenced in the param xml """
    locator_xml = LOCATOR_FILE.read().decode('utf8')
    root = ET.fromstring(locator_xml)
    for child in root:
        if child.tag == 'path':
            try:
                path = child.text
                dirpath = os.path.dirname(LOCATOR_FILE.name)
                fullpath = os.path.join(dirpath, path)
                return read_keys(fullpath)
            except OSError as e:
                if e.errno == errno.ENOENT:
                    continue
                else:
                    raise
    exceptionfmt = 'None of the files referenced by {} were found.'
    raise Exception(exceptionfmt.format(LOCATOR_FILE.name))


def read_keys(path):
    """ Reads API keys from the XML file specified by param path """
    tree = ET.parse(path)
    root = tree.getroot()
    return dict([(key.attrib['name'], key.text) for key in root.iter('key')])

if __name__ == '__main__':
    keys = get_keys()
    parser = argparse.ArgumentParser()
    parser.add_argument('api', choices=list(keys))
    args = parser.parse_args()
    print(keys[args.api])
