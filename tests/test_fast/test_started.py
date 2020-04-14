import pytest

from easyprocess import EasyProcess, EasyProcessError


def test_is_started():
    assert EasyProcess("ls -la").is_started is False
    assert EasyProcess("ls -la").start().is_started
    assert EasyProcess("ls -la").call().is_started
    assert EasyProcess("ls -la").start().wait().is_started
    assert EasyProcess("ls -la").start().stop().is_started


def test_raise():
    with pytest.raises(EasyProcessError):
        EasyProcess("ls -la").start().start()
    with pytest.raises(EasyProcessError):
        EasyProcess("ls -la").stop()
    with pytest.raises(EasyProcessError):
        EasyProcess("ls -la").sendstop()
    # .assertRaises(EasyProcessError, lambda : EasyProcess('ls
    # -la').start().stop().stop())
    with pytest.raises(EasyProcessError):
        EasyProcess("ls -la").start().wrap(lambda: None)()
    EasyProcess("ls -la").wrap(lambda: None)()
