EasyProcess is an easy to use python subprocess interface.

Links:
 * home: https://github.com/ponty/EasyProcess
 * PYPI: https://pypi.python.org/pypi/EasyProcess

[![Build Status](https://travis-ci.org/ponty/EasyProcess.svg?branch=master)](https://travis-ci.org/ponty/EasyProcess)

Features:
 - layer on top of [subprocess](https://docs.python.org/library/subprocess.html) module
 - easy to start, stop programs
 - easy to get standard output/error, return code of programs
 - command can be list (preferred) or string (command string is converted to list using shlex.split)
 - logging
 - timeout
 - shell is not supported
 - pipes are not supported
 - stdout/stderr is set only after the subprocess has finished
 - stop() does not kill whole subprocess tree
 - unicode support
 - supported python versions: 3.6, 3.7, 3.8, 3.9
 - [Method chaining](https://en.wikipedia.org/wiki/Method_chaining)
 
Installation:

```console
$ python3 -m pip install EasyProcess
```

Usage
=====

Examples:
```py
# easyprocess/examples/hello.py

from easyprocess import EasyProcess

cmd = ["echo", "hello"]
s = EasyProcess(cmd).call().stdout
print(s)

```

Output:
<!-- embedme doc/gen/python3_-m_easyprocess.examples.hello.txt -->

```console
$ python3 -m easyprocess.examples.hello
hello
```


```py
# easyprocess/examples/cmd.py

import sys

from easyprocess import EasyProcess

python = sys.executable

print("-- Run program, wait for it to complete, get stdout:")
s = EasyProcess([python, "-c", "print(3)"]).call().stdout
print(s)

print("-- Run program, wait for it to complete, get stderr:")
s = EasyProcess([python, "-c", "import sys;sys.stderr.write('4\\n')"]).call().stderr
print(s)

print("-- Run program, wait for it to complete, get return code:")
s = EasyProcess([python, "--version"]).call().return_code
print(s)

print("-- Run program, wait 1.5 second, stop it, get stdout:")
prog = """
import time
for i in range(10):
    print(i, flush=True)
    time.sleep(1)
"""
s = EasyProcess([python, "-c", prog]).start().sleep(1.5).stop().stdout
print(s)

```

Output:
<!-- embedme doc/gen/python3_-m_easyprocess.examples.cmd.txt -->

```console
$ python3 -m easyprocess.examples.cmd
-- Run program, wait for it to complete, get stdout:
3
-- Run program, wait for it to complete, get stderr:
4
-- Run program, wait for it to complete, get return code:
0
-- Run program, wait 1.5 second, stop it, get stdout:
0
1
```

Shell commands
--------------

Shell commands are not supported.

``echo`` is a shell command on Windows (there is no echo.exe),
but it is a program on Linux.

return_code
-----------

`EasyProcess.return_code` is None until
`EasyProcess.stop` or `EasyProcess.wait` is called.

With
----

By using `with` statement the process is started
and stopped automatically:
    
```python
from easyprocess import EasyProcess
with EasyProcess('ping 127.0.0.1') as proc: # start()
    # communicate with proc
    pass
# stopped
```

Equivalent with:
    
```python
from easyprocess import EasyProcess
proc = EasyProcess('ping 127.0.0.1').start()
try:
    # communicate with proc
    pass
finally:
    proc.stop()
```

Timeout
-------

This was implemented with "daemon thread".

"The entire Python program exits when only daemon threads are left."
https://docs.python.org/library/threading.html

```py
# easyprocess/examples/timeout.py

import sys

from easyprocess import EasyProcess

python = sys.executable

prog = """
import time
for i in range(3):
    print(i, flush=True)
    time.sleep(1)
"""

print("-- no timeout")
stdout = EasyProcess([python, "-c", prog]).call().stdout
print(stdout)

print("-- timeout=1.5s")
stdout = EasyProcess([python, "-c", prog]).call(timeout=1.5).stdout
print(stdout)

print("-- timeout=50s")
stdout = EasyProcess([python, "-c", prog]).call(timeout=50).stdout
print(stdout)

```

Output:

<!-- embedme doc/gen/python3_-m_easyprocess.examples.timeout.txt -->

```console
$ python3 -m easyprocess.examples.timeout
-- no timeout
0
1
2
-- timeout=1.5s
0
1
-- timeout=50s
0
1
2
```