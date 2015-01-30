EasyProcess is an easy to use python subprocess interface.

Links:
 * home: https://github.com/ponty/EasyProcess
 * documentation: http://ponty.github.com/EasyProcess

.. image:: https://pypip.in/version/EasyProcess/badge.svg
    :target: https://pypi.python.org/pypi/EasyProcess/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/EasyProcess/badge.svg
    :target: https://pypi.python.org/pypi/EasyProcess/
    :alt: Supported Python versions

.. image:: https://pypip.in/license/EasyProcess/badge.svg
    :target: https://pypi.python.org/pypi/EasyProcess/
    :alt: License
            
.. image:: https://pypip.in/download/EasyProcess/badge.svg
    :target: https://pypi.python.org/pypi/EasyProcess/
    :alt: Downloads
    
.. image:: https://pypip.in/download/EasyProcess/badge.svg
    :target: https://pypi.python.org/pypi/EasyProcess/
    :alt: Build
    
.. image:: https://pypip.in/download/EasyProcess/badge.svg
    :target: https://pypi.python.org/pypi/EasyProcess/
    :alt: Coverage

Features:
 - layer on top of subprocess_ module
 - easy to start, stop programs
 - easy to get standard output/error, return code of programs
 - command can be list or string
 - logging
 - timeout
 - unit-tests
 - cross-platform, development on linux
 - global config file with program aliases 
 - shell is not supported
 - pipes are not supported
 - stdout/stderr is set only after the subprocess has finished
 - stop() does not kill whole subprocess tree 
 - unicode support
 - supported python versions: 2.6, 2.7, 3.2, 3.3, 3.4
 
Known problems:
 - none

Similar projects:
 * execute (http://pypi.python.org/pypi/execute)
 * commandwrapper (http://pypi.python.org/pypi/commandwrapper)
 * extcmd (http://pypi.python.org/pypi/extcmd)
 * sh (https://github.com/amoffat/sh)
 * envoy (https://github.com/kennethreitz/envoy)
 * plumbum (https://github.com/tomerfiliba/plumbum)
 
Basic usage
===========

    >>> from easyprocess import EasyProcess
    >>> EasyProcess('python --version').call().stderr
    u'Python 2.6.6'

Installation
============

General
-------

 * install pip_
 * install the program::

    # as root
    pip install EasyProcess

Ubuntu
------
::

    sudo apt-get install python-pip
    sudo pip install EasyProcess

Uninstall
---------
::

    # as root
    pip uninstall EasyProcess


.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pip: http://pip.openplans.org/
.. _subprocess: http://docs.python.org/library/subprocess.html
