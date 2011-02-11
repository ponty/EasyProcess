EasyProcess is an easy to use python subprocess interface.

home: https://github.com/ponty/EasyProcess

documentation: http://ponty.github.com/EasyProcess

Advantages:
 - easy interface
 - command can be list or string
 - logging

Basic usage
============

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

