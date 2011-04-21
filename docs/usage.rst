Usage
==================

.. runblock:: pycon
    
    >>> from easyprocess import EasyProcess
    >>> # Run program, wait for it to complete, get stdout (command is string):
    >>> EasyProcess('echo hello').call().stdout
    >>> # Run program, wait for it to complete, get stdout (command is list):
    >>> EasyProcess(['echo','hello']).call().stdout
    >>> # Run program, wait for it to complete, get stderr:
    >>> EasyProcess('python --version').call().stderr
    >>> # Run program, wait for it to complete, get return code:
    >>> EasyProcess('python --version').call().return_code
    >>> # Run program, wait 1 second, stop it, get stdout:
    >>> print EasyProcess('ping localhost').start().sleep(1).stop().stdout
    >>> # Run program, wait for it to complete, check for errors:
    >>> EasyProcess('ls').check()

Exceptions in check::

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

Timeout
--------

.. runblock:: pycon

    >>> from easyprocess import EasyProcess
    >>> # Run ping with  timeout
    >>> print EasyProcess('ping localhost').call(timeout=1).stdout

Logging
=========

Example program:

.. literalinclude:: ../easyprocess/examples/log.py

Output:

.. program-output:: python -m easyprocess.examples.log
    :prompt:

Alias
======

You can define an alias for EasyProcess calls 
by editing your config file ($HOME/.easyprocess.cfg)
This can be used for:

 * testing different version of the same program
 * redirect calls
 * program path can be defined here. (Installed programs are not in $PATH on Windows) 

start python and print python version::

	>>> from easyprocess import EasyProcess
	>>> EasyProcess('python --version').call().stderr
	'Python 2.6.6'

edit the config file: $HOME/.easyprocess.cfg::

	[link]
	python=/usr/bin/python2.7

restart python and print python version again::

	>>> from easyprocess import EasyProcess
	>>> EasyProcess('python --version').call().stderr
	'Python 2.7.0+'


Replacing existing functions
====================================

Replacing os.system::

    retcode = os.system("ls -l")
    ==>
    p = EasyProcess("ls -l").call()
    retcode = p.return_code
    print p.stdout

Replacing subprocess.call::

    retcode = subprocess.call(["ls", "-l"])
    ==>
    p = EasyProcess(["ls", "-l"]).call()
    retcode = p.return_code
    print p.stdout
