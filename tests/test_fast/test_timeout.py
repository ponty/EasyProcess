import sys
import time

import pytest

from easyprocess import EasyProcess

python = sys.executable


def test_timeout():
    """
    Waits for the process to complete.

    Args:
    """
    p = EasyProcess("sleep 1").start()
    p.wait(0.2)
    assert p.is_alive()
    p.wait(0.2)
    assert p.is_alive()
    p.wait(2)
    assert not p.is_alive()

    assert EasyProcess("sleep 0.3").call().return_code == 0
    assert EasyProcess("sleep 0.3").call(timeout=0.1).return_code != 0
    assert EasyProcess("sleep 0.3").call(timeout=1).return_code == 0

    assert EasyProcess("sleep 0.3").call().timeout_happened is False
    assert EasyProcess("sleep 0.3").call(timeout=0.1).timeout_happened
    assert EasyProcess("sleep 0.3").call(timeout=1).timeout_happened is False


@pytest.mark.timeout(3)
def test_time_cli1():
    """
    Returns the number of the python 2.

    Args:
    """
    p = EasyProcess(
        [
            python,
            "-c",
            "import logging;logging.basicConfig(level=logging.DEBUG);from easyprocess import EasyProcess;EasyProcess('sleep 5').start()",
        ]
    )
    p.call()
    assert p.return_code == 0


@pytest.mark.timeout(3)
def test_time_cli2():
    """
    The test for the test.

    Args:
    """
    p = EasyProcess(
        [
            python,
            "-c",
            "import logging;logging.basicConfig(level=logging.DEBUG);from easyprocess import EasyProcess;EasyProcess('sleep 5').call(timeout=0.5)",
        ]
    )
    p.call()
    assert p.return_code == 0


@pytest.mark.timeout(3)
def test_time2():
    """
    Test if the test time in seconds

    Args:
    """
    p = EasyProcess("sleep 5").call(timeout=1)
    assert p.is_alive() is False
    assert p.timeout_happened
    assert p.return_code != 0
    assert p.stdout == ""


@pytest.mark.timeout(3)
def test_timeout_out():
    """
    Waits for a command to be executed.

    Args:
    """
    p = EasyProcess(
        [python, "-c", "import time;print( 'start');time.sleep(5);print( 'end')"]
    ).call(timeout=1)
    assert p.is_alive() is False
    assert p.timeout_happened
    assert p.return_code != 0
    assert p.stdout == ""


@pytest.mark.timeout(0.3)
def test_time3():
    """
    Test if the test test time.

    Args:
    """
    EasyProcess("sleep 5").start()


ignore_term = """
import signal;
import time;
signal.signal(signal.SIGTERM, lambda *args: None);
while True:
    time.sleep(0.5);
"""


@pytest.mark.timeout(3)
def test_force_timeout():
    """
    Executes a command and returns the result.

    Args:
    """
    proc = EasyProcess([python, "-c", ignore_term]).start()
    # Calling stop() right away actually stops python before it
    # has a change to actually compile and run the input code,
    # meaning the signal handlers aren't registered yet. Give it
    # a moment to setup
    time.sleep(1)
    proc.stop(kill_after=1)
    assert proc.is_alive() is False
    assert proc.return_code != 0


@pytest.mark.timeout(2)
def test_force_0_timeout():
    """
    Waits a command and waits for the result.

    Args:
    """
    proc = EasyProcess([python, "-c", ignore_term]).start()
    time.sleep(1)
    proc.stop(kill_after=0)
    assert proc.is_alive() is False
    assert proc.return_code != 0


@pytest.mark.timeout(3)
def test_force_timeout2():
    """
    Test if the timeout of a timeout.

    Args:
    """
    proc = EasyProcess([python, "-c", ignore_term]).call(timeout=1, kill_after=1)
    assert proc.is_alive() is False
    assert proc.return_code != 0


@pytest.mark.timeout(4)
def test_stop_wait():
    """
    Waits for a command to stop.

    Args:
    """
    proc = EasyProcess([python, "-c", ignore_term]).start()
    time.sleep(1)
    proc.sendstop().wait(timeout=1)
    # On windows, Popen.terminate actually behaves like kill,
    # so don't check that our hanging process code is actually hanging.
    # The end result is still what we want. On other platforms, leave
    # this assertion to make sure we are correctly testing the ability
    # to stop a hung process
    if not sys.platform.startswith("win"):
        assert proc.is_alive() is True
    proc.stop(kill_after=1)
    assert proc.is_alive() is False
    assert proc.return_code != 0
