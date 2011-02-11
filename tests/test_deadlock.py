from easyprocess import EasyProcess, EasyProcessCheckError, \
    EasyProcessCheckInstalledError
from nose.tools import eq_, timed
from unittest import TestCase
import time


class Test(TestCase):
    @timed(1)
    def test_stop(self):
        # deadlock in 0.0.0
        EasyProcess('python deadlock.py').start().sleep(0.5).stop()


