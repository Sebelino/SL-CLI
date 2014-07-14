#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import argparse,sys,os
import xml.etree.ElementTree as ET

def read_keys():
    xmlfile = 'sensitive.xml'
    if not os.path.isfile(xmlfile):
        raise Exception("Filen %s saknas."% xmlfile)
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    return dict([(key.attrib['name'],key.text) for key in root.iter('key')])

if __name__ == '__main__':
    keys = read_keys()
    parser = argparse.ArgumentParser()
    parser.add_argument('api',choices=list(keys))
    args = parser.parse_args()
    print keys[args.api]
