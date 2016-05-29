from distutils.core import setup
from setuptools import find_packages

setup(
    name='SL-CLI',
    version='3.0dev',
    packages=find_packages(),
    license=open('LICENSE').read(),
    long_description=open('README.md').read(),
)
