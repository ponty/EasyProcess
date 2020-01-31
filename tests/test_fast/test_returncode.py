from nose.tools import eq_, ok_

from easyprocess import EasyProcess


def test_return_code():
    # process has finished but no stop() or wait() was called
    eq_(EasyProcess("echo hello").start().sleep(0.5).return_code, None)

    # wait()
    eq_(EasyProcess("echo hello").start().wait().return_code, 0)

    # stop() after process has finished
    eq_(EasyProcess("echo hello").start().sleep(0.5).stop().return_code, 0)

    # stop() before process has finished
    ok_(EasyProcess("sleep 2").start().stop().return_code != 0)

    # same as start().wait().stop()
    eq_(EasyProcess("echo hello").call().return_code, 0)


def test_is_alive1():
    # early exit
    p = EasyProcess("echo hello").start().sleep(0.5)

    eq_(p.return_code, None)
    eq_(p.stdout, None)
    eq_(p.stderr, None)

    eq_(p.is_alive(), False)  # is_alive collects ouputs if proc stopped

    eq_(p.return_code, 0)
    eq_(p.stdout, "hello")
    eq_(p.stderr, "")

    eq_(p.is_alive(), False)
    eq_(p.is_alive(), False)


def test_is_alive2():
    # no exit
    p = EasyProcess("sleep 10").start()

    eq_(p.return_code, None)
    eq_(p.stdout, None)
    eq_(p.stderr, None)

    eq_(p.is_alive(), True)  # is_alive collects ouputs if proc stopped

    eq_(p.return_code, None)
    eq_(p.stdout, None)
    eq_(p.stderr, None)

    eq_(p.is_alive(), True)
    eq_(p.is_alive(), True)
