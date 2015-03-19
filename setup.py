from setuptools import setup
import sys
import os

NAME = 'easyprocess'
URL = 'https://github.com/ponty/easyprocess'
DESCRIPTION = 'Easy to use python subprocess interface.'
PACKAGES = [NAME,
            NAME + '.examples',
            ]

# get __version__
__version__ = None
exec(open(os.path.join(NAME , 'about.py')).read())
VERSION = __version__

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

classifiers = [
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Operating System :: OS Independent",

    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    #    "Programming Language :: Python :: 2.3",
    #    "Programming Language :: Python :: 2.4",
    #"Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    #    "Programming Language :: Python :: 2 :: Only",
    "Programming Language :: Python :: 3",
    #    "Programming Language :: Python :: 3.0",
    "Programming Language :: Python :: 3.1",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
]


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.rst', 'r').read(),
    classifiers=classifiers,
    keywords='subprocess interface',
    author='ponty',
    # author_email='',
    url=URL,
    license='BSD',
    packages=PACKAGES,
    **extra
)
