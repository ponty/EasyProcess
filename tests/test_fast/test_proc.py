from __future__ import with_statement

import sys
import time

import pytest

from easyprocess import EasyProcess

python = sys.executable


def test_call():
    """
    Returns the test code.

    Args:
    """
    assert EasyProcess("ls -la").call().return_code == 0
    assert EasyProcess(["ls", "-la"]).call().return_code == 0


def test_start():
    """
    Waits the test starts.

    Args:
    """
    p = EasyProcess("ls -la").start()
    time.sleep(0.2)
    assert p.stop().return_code == 0


def test_start2():
    """
    Test if the test starts.

    Args:
    """
    p = EasyProcess("echo hi").start()
    time.sleep(0.2)
    # no wait() -> no results
    assert p.return_code is None
    assert p.stdout is None


@pytest.mark.timeout(1)
def test_start3():
    """
    Returns the start3 code for the given test code.

    Args:
    """
    p = EasyProcess("sleep 10").start()
    assert p.return_code is None


def test_alive():
    """
    This function is alive is alive.

    Args:
    """
    assert EasyProcess("ping 127.0.0.1 -c 2").is_alive() is False
    assert EasyProcess("ping 127.0.0.1 -c 2").start().is_alive()
    assert EasyProcess("ping 127.0.0.1 -c 2").start().stop().is_alive() is False
    assert EasyProcess("ping 127.0.0.1 -c 2").call().is_alive() is False


def test_std():
    """
    Run the test test.

    Args:
    """
    assert EasyProcess("echo hello").call().stdout == "hello"
    assert EasyProcess([python, "-c", "print(42)"]).call().stdout == "42"


def test_wait():
    """
    Waits for a command to complete.

    Args:
    """
    assert EasyProcess("echo hello").wait().return_code is None
    assert EasyProcess("echo hello").wait().stdout is None

    assert EasyProcess("echo hello").start().wait().return_code == 0
    assert EasyProcess("echo hello").start().wait().stdout == "hello"


#     def test_xephyr():
#         EasyProcess('Xephyr -help').check(return_code=1)


def test_wrap():
    """
    Decorator to convert a test.

    Args:
    """
    def f():
        """
        Return the number of the process.

        Args:
        """
        return EasyProcess("echo hi").call().stdout

    assert EasyProcess("ping 127.0.0.1").wrap(f)() == "hi"


def test_with():
    """
    Returns true if a test.

    Args:
    """
    with EasyProcess("ping 127.0.0.1") as x:
        assert x.is_alive()
    assert x.return_code != 0
    assert not x.is_alive()


def test_parse():
    """
    Check to see if the test test.

    Args:
    """
    assert EasyProcess("ls -la").cmd == ["ls", "-la"]
    assert EasyProcess('ls "abc"').cmd == ["ls", "abc"]
    assert EasyProcess('ls "ab c"').cmd == ["ls", "ab c"]


def test_stop():
    """
    Waits for a code to complete.

    Args:
    """
    p = EasyProcess("ls -la").start()
    time.sleep(0.2)
    assert p.stop().return_code == 0
    assert p.stop().return_code == 0
    assert p.stop().return_code == 0
