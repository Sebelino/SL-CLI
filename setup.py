from setuptools import setup, find_packages

version = '3.1.2'

setup(
    name='SL-CLI',
    version=version,
    description='Command-line interface to APIs used by sl.se.',
    author='Sebelino',
    author_email='sebelino7@gmail.com',
    url='https://github.com/Sebelino/SL-CLI',
    download_url='https://github.com/Sebelino/SL-CLI/tarball/{}'.format(
        version),
    packages=find_packages(),
    package_data={
        'slcli.resources': [
            'locations.xml',
        ],
    },
    entry_points={
        'console_scripts': [
            'sl-cli = slcli.sl_cli:main',
        ],
    },
    license='MIT',
    install_requires=[
        'xmltodict',
    ],
)
