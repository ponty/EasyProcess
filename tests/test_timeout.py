from easyprocess import EasyProcess
from nose.tools import eq_
from unittest import TestCase


class Test(TestCase):
    def test_timeout(self):
        p = EasyProcess('sleep 1').start()
        p.wait(0.2)
        eq_(p.is_alive(), True)
        p.wait(0.2)
        eq_(p.is_alive(), True)
        p.wait(2)
        eq_(p.is_alive(), False)
        
        eq_(EasyProcess('sleep 0.3').call().return_code==0, True)
        eq_(EasyProcess('sleep 0.3').call(timeout=0.1).return_code==0, False)
        eq_(EasyProcess('sleep 0.3').call(timeout=1).return_code==0, True)
    