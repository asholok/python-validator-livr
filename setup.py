from distutils.core import setup

setup(
    name = 'LIVR',
    version = '0.4',
    author = 'Viktor Turstkiy, Ihor Kolosha',
    packages = ['LIVR', 'LIVR.test'],
    license='LICENSE.txt',
    description='LIVR validator.',
    long_description=open('README.md').read(),
)