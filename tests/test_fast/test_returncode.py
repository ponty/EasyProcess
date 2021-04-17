from easyprocess import EasyProcess


def test_return_code():
    # process has finished but no stop() or wait() was called
    assert EasyProcess("echo hello").start().sleep(0.5).return_code is None

    # wait()
    assert EasyProcess("echo hello").start().wait().return_code == 0

    # stop() after process has finished
    assert EasyProcess("echo hello").start().sleep(0.5).stop().return_code == 0

    # stop() before process has finished
    assert EasyProcess("sleep 2").start().stop().return_code != 0

    # same as start().wait().stop()
    assert EasyProcess("echo hello").call().return_code == 0


def test_is_alive1():
    # early exit
    p = EasyProcess("echo hello").start().sleep(0.5)

    assert p.return_code is None
    assert p.stdout is None
    assert p.stderr is None

    assert p.is_alive() is False  # is_alive collects ouputs if proc stopped

    assert p.return_code == 0
    assert p.stdout == "hello"
    assert p.stderr == ""


def test_is_alive2():
    # no exit
    p = EasyProcess("sleep 10").start()

    assert p.return_code is None
    assert p.stdout is None
    assert p.stderr is None

    assert p.is_alive()  # is_alive collects ouputs if proc stopped

    assert p.return_code is None
    assert p.stdout is None
    assert p.stderr is None
