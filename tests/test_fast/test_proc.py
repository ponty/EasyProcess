from __future__ import with_statement

import sys
import time

import pytest

from easyprocess import EasyProcess

python = sys.executable


def test_call():
    assert EasyProcess("ls -la").call().return_code == 0
    assert EasyProcess(["ls", "-la"]).call().return_code == 0


def test_start():
    p = EasyProcess("ls -la").start()
    time.sleep(0.2)
    assert p.stop().return_code == 0


def test_start2():
    p = EasyProcess("echo hi").start()
    time.sleep(0.2)
    # no wait() -> no results
    assert p.return_code is None
    assert p.stdout is None


@pytest.mark.timeout(1)
def test_start3():
    p = EasyProcess("sleep 10").start()
    assert p.return_code is None


def test_alive():
    assert EasyProcess("ping 127.0.0.1 -c 2").is_alive() is False
    assert EasyProcess("ping 127.0.0.1 -c 2").start().is_alive()
    assert EasyProcess("ping 127.0.0.1 -c 2").start().stop().is_alive() is False
    assert EasyProcess("ping 127.0.0.1 -c 2").call().is_alive() is False


def test_std():
    assert EasyProcess("echo hello").call().stdout == "hello"
    assert EasyProcess([python, "-c", "print(42)"]).call().stdout == "42"


def test_wait():
    assert EasyProcess("echo hello").wait().return_code is None
    assert EasyProcess("echo hello").wait().stdout is None

    assert EasyProcess("echo hello").start().wait().return_code == 0
    assert EasyProcess("echo hello").start().wait().stdout == "hello"


#     def test_xephyr():
#         EasyProcess('Xephyr -help').check(return_code=1)


def test_wrap():
    def f():
        return EasyProcess("echo hi").call().stdout

    assert EasyProcess("ping 127.0.0.1").wrap(f)() == "hi"


def test_with():
    with EasyProcess("ping 127.0.0.1") as x:
        assert x.is_alive()
    assert x.return_code != 0
    assert not x.is_alive()


def test_parse():
    assert EasyProcess("ls -la").cmd == ["ls", "-la"]
    assert EasyProcess('ls "abc"').cmd == ["ls", "abc"]
    assert EasyProcess('ls "ab c"').cmd == ["ls", "ab c"]


def test_stop():
    p = EasyProcess("ls -la").start()
    time.sleep(0.2)
    assert p.stop().return_code == 0
    assert p.stop().return_code == 0
    assert p.stop().return_code == 0
