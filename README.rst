============
EasyProcess
============

Easy to use python subprocess interface.

home: https://github.com/ponty/easyprocess

Usage
------------
::

    >>> from easyprocess import EasyProcess
    >>> EasyProcess('echo hello').call().stdout
    'hello'
    >>> EasyProcess(['echo','hello']).call().stdout
    'hello'
    >>> EasyProcess('python --version').call().stderr
    'Python 2.6.6'
    >>> EasyProcess('python --version').call().return_code
    0
    >>> EasyProcess('ping localhost').start().sleep(1).stop().stdout
    'PING localhost.localdomain (127.0.0.1) 56(84) bytes of data.\n64 bytes from localhost.localdomain (127.0.0.1): icmp_req=1 ttl=64 time=0.026 ms'
    >>> EasyProcess('ls').check()
    True
    >>> EasyProcess('bad_command').check()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "easyprocess.py", line 84, in check
        raise EasyProcessCheckError(self)
    easyprocess.EasyProcessCheckError: EasyProcess check failed!
     OSError:[Errno 2] No such file or directory
     cmd:['bad_command']
     return code:None
     stderr:None
    >>> EasyProcess('sh -c bad_command').check()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "easyprocess.py", line 84, in check
        raise EasyProcessCheckError(self)
    easyprocess.EasyProcessCheckError: EasyProcess check failed!
     OSError:None
     cmd:['sh', '-c', 'bad_command']
     return code:127
     stderr:sh: bad_command: not found

Advantages
----------

- easy interface
- command can be list or string
- logging


Installation
------------

The easiest way to get is if you have setuptools_ installed::

    easy_install easyprocess

or if you have pip_ installed::

    pip install easyprocess

Uninstall::

    pip uninstall easyprocess


.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pip: http://pip.openplans.org/

