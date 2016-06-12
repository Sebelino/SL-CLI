import os
import xml.etree.ElementTree as ET
from setuptools import setup, find_packages
from os.path import (isfile, dirname, realpath, join, basename, expandvars,
                     expanduser)

sensitive_path = join(dirname(realpath(__file__)), 'sensitive.xml')
config_path = join(dirname(realpath(__file__)), 'config.xml')
locations_path = join(dirname(realpath(__file__)), 'locations.xml')

if not isfile(sensitive_path):
    raise Exception("File not found: {}".format(sensitive_path))
if not isfile(config_path):
    raise Exception("File not found: {}".format(config_path))


def resolvepath(path):
    return expanduser(expandvars(path))


def write_locations(paths):
    root = ET.Element("root")
    pathtags = [ET.SubElement(root, "path") for _ in paths]
    for i in range(len(paths)):
        pathtags[i].text = paths[i]
    tree = ET.ElementTree(root)
    tree.write(locations_path)


def config_paths():
    tree = ET.ElementTree(file=config_path)
    root = tree.getroot()
    children = [c for c in root if c.tag == 'setup']
    children = [c for c in children if 'os' not in c.attrib
                                       or c.attrib['os'] == os.name]
    setuptag = children[0]
    installpaths = [p.text for p in setuptag.find("install") if p.tag == "path"]
    deploypaths = [p.text for p in setuptag.find("deploy") if p.tag == "path"]
    if not installpaths and not deploypaths:
        installpaths = [p for p in setuptag if p.tag == "path"]
        deploypaths = [p for p in setuptag if p.tag == "path"]
    paths = {
        "install": installpaths,
        "deploy": deploypaths,
    }
    return paths


def data_files(paths):
    dat = [(resolvepath(dirname(p)), [basename(p)]) for p in paths]
    dat.append(('slcli/resources', ['locations.xml']))
    return dat

paths = config_paths()
write_locations(paths["deploy"])

setup(
    name='SLCLI',
    version='3.0.dev0',
    url='https://github.com/Sebelino/SL-CLI',
    packages=find_packages(),
    package_data={
        'slcli.resources': [
            'locations.xml',
            'sensitive.example.xml',
        ],
    },
    data_files=data_files(paths["install"]),
    entry_points={
        'console_scripts': [
            'sl-cli = slcli.slcli:main',
        ],
    },
    license=open('LICENSE').read(),
    long_description=open('README.md').read(),
)
