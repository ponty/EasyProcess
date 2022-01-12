EasyProcess is an easy to use python subprocess interface.

Links:
 * home: https://github.com/ponty/EasyProcess
 * PYPI: https://pypi.python.org/pypi/EasyProcess

![workflow](https://github.com/ponty/EasyProcess/actions/workflows/main.yml/badge.svg)

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
 - supported python versions: 3.7, 3.8, 3.9, 3.10
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
with EasyProcess(["ping", "127.0.0.1"]) as proc: # start()
    # communicate with proc
    pass
# stopped
```

Equivalent:
    
```python
from easyprocess import EasyProcess
proc = EasyProcess(["ping", "127.0.0.1"]).start()
try:
    # communicate with proc
    pass
finally:
    proc.stop()
```

Full example:
```py
# easyprocess/examples/with.py

import os
import sys
import urllib.request
from os.path import abspath, dirname
from time import sleep

from easyprocess import EasyProcess

webserver_code = """
from http.server import HTTPServer, CGIHTTPRequestHandler
srv = HTTPServer(server_address=("", 8080), RequestHandlerClass=CGIHTTPRequestHandler)
srv.serve_forever()
"""
os.chdir(dirname(abspath(__file__)))
with EasyProcess([sys.executable, "-c", webserver_code]):
    sleep(2)  # wait for server
    html = urllib.request.urlopen("http://localhost:8080").read().decode("utf-8")
print(html)

```

Output:

<!-- embedme doc/gen/python3_-m_easyprocess.examples.with.txt -->

```console
$ python3 -m easyprocess.examples.with
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Directory listing for /</title>
</head>
<body>
<h1>Directory listing for /</h1>
<hr>
<ul>
<li><a href="__init__.py">__init__.py</a></li>
<li><a href="__pycache__/">__pycache__/</a></li>
<li><a href="cmd.py">cmd.py</a></li>
<li><a href="hello.py">hello.py</a></li>
<li><a href="log.py">log.py</a></li>
<li><a href="timeout.py">timeout.py</a></li>
<li><a href="ver.py">ver.py</a></li>
<li><a href="with.py">with.py</a></li>
</ul>
<hr>
</body>
</html>

```

Timeout
-------

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