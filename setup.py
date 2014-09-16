from distutils.core import setup

with open('README.rst') as readme:
    setup(
        name = 'LIVR',
        version = '0.4',
        author = 'Viktor Turstkiy, Ihor Kolosha',
        packages = ['LIVR', 'LIVR.test'],
        license='LICENSE.txt',
        description='LIVR validator.',
        long_description=readme.read(),
    )