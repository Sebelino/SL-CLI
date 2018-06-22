#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import os.path
import errno
import xml.etree.ElementTree as ET
from pkg_resources import resource_stream

# XML file storing one or more paths to the XML file containing the API keys
locations_filename = 'locations.xml'
locations_file = resource_stream('slcli.resources', locations_filename)
locations_xml = locations_file.read().decode('utf8')


class KeysNotFoundError(IOError):
    def __init__(self, paths):
        self.message = 'Could not find the API keys in any of these locations:'
        self.message = self.message+'\n'+'\n'.join(paths)
        self.paths = paths
        super(KeysNotFoundError, self).__init__(self.message)


def get_keys():
    keys = dict()
    keys["platsuppslag"] = os.environ.get("PLATSUPPSLAG")
    keys["reseplanerare3"] = os.environ.get("RESEPLANERARE")
    if all(k is None for k in keys.values()):
        return find_keys()
    else:
        return keys


def find_keys():
    """ Reads API keys from the XML files referenced in the param xml """
    root = ET.fromstring(locations_xml)
    paths = [c for c in root if 'os' not in c.attrib or
             c.attrib['os'] == os.name]
    paths = [c.text for c in paths if c.tag == 'path']
    resolvpaths = [os.path.expanduser(os.path.expandvars(p)) for p in paths]
    for rpath in resolvpaths:
        try:
            dirpath = os.path.dirname(locations_filename)
            fullpath = os.path.join(dirpath, rpath)
            return read_keys(fullpath)
        except OSError as e:
            if e.errno == errno.ENOENT:
                continue
            else:
                raise
    raise KeysNotFoundError(resolvpaths)


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
