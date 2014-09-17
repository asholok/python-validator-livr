from distutils.core import setup

with open('README.txt') as readme:
    setup(
        name = 'LIVR',
        version = '0.4',
        author = 'Viktor Turstkiy, Ihor Kolosha',
        packages = ['LIVR', 'LIVR.test', 'LIVR.Rules'],
        license='look into README',
        description='LIVR validator.',
        long_description=readme.read(),
    )