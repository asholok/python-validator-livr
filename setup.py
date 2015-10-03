from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='LIVR',
    version='0.4.31',
    author='Ihor Kolosha, Viktor Turstkiy',
    packages=find_packages(),
    license='look into README',
    description='LIVR validator.',
    long_description=long_description,
    url='https://github.com/asholok/python-validator-livr',
)