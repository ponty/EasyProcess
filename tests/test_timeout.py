from easyprocess import EasyProcess
from nose.tools import eq_, timed
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
    
    @timed(2)
    def test_time_cli1(self):
        p=EasyProcess(['python', '-c', "import logging;logging.basicConfig(level=logging.DEBUG);from easyprocess import EasyProcess;EasyProcess('sleep 15').start()"])
        p.call()
        eq_(p.return_code,0)

    @timed(2)
    def test_time_cli2(self):
        p=EasyProcess(['python', '-c', "import logging;logging.basicConfig(level=logging.DEBUG);from easyprocess import EasyProcess;EasyProcess('sleep 15').call(timeout=0.5)"])
        p.call()
        eq_(p.return_code,0)
    
    @timed(1.2)
    def test_time2(self):
        EasyProcess('sleep 5').call(timeout=1)
        
    @timed(0.3)
    def test_time3(self):
        EasyProcess('sleep 5').start()
