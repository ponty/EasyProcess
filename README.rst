EasyProcess is an easy to use python subprocess interface.

home: https://github.com/ponty/EasyProcess

html documentation: http://ponty.github.com/EasyProcess

pdf documentation: https://github.com/ponty/EasyProcess/raw/master/docs/_build/latex/EasyProcess.pdf


Features:
 - layer on top of subprocess module
 - easy to start, stop programs
 - easy to get standard output/error, return code of programs
 - command can be list or string
 - logging
 - timeout
 - unittests
 - shell is not supported
 - crossplatform but development on linux
 
Basic usage
============

    >>> from easyprocess import EasyProcess
    >>> EasyProcess('echo hello').call().stdout
    'hello'


Installation
============

General
--------

 * install setuptools_ or pip_
 * install the program:

if you have setuptools_ installed::

    # as root
    easy_install EasyProcess

if you have pip_ installed::

    # as root
    pip install EasyProcess

Ubuntu
----------
::

    sudo apt-get install python-setuptools
    sudo easy_install EasyProcess

Uninstall
----------
::

    # as root
    pip uninstall EasyProcess


.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pip: http://pip.openplans.org/

