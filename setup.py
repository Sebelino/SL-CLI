from setuptools import setup, find_packages

setup(
    name='SL-CLI',
    version='3.0dev1',
    description='Command-line interface to APIs used by sl.se.',
    author='Sebelino',
    author_email='sebelino7@gmail.com',
    url='https://github.com/Sebelino/SL-CLI',
    download_url='https://github.com/Sebelino/SL-CLI/tarball/3.0dev1',
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
)
