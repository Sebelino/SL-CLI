from setuptools import setup, find_packages

setup(
    name='SLCLI',
    version='3.0.dev0',
    url='https://github.com/Sebelino/SL-CLI',
    packages=find_packages(),
    package_data={
        'slcli.resources': [
            'locations.xml',
        ],
    },
    entry_points={
        'console_scripts': [
            'sl-cli = slcli.slcli:main',
        ],
    },
    license=open('LICENSE').read(),
    long_description=open('README.md').read(),
)
