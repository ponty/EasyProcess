from easyprocess import EasyProcess, EasyProcessCheckError, \
    EasyProcessCheckInstalledError
from nose.tools import eq_, timed
from unittest import TestCase
import time


class Test(TestCase):
    def test_call(self):
        eq_(EasyProcess('ls -la').call().return_code, 0)
        eq_(EasyProcess(['ls', '-la']).call().return_code, 0)
    
    def test_check(self):
        eq_(EasyProcess('ls -la').check().return_code, 0)
        eq_(EasyProcess(['ls', '-la']).check().return_code, 0)
        
        self.assertRaises(EasyProcessCheckError, lambda :  EasyProcess('xxxxx').check())
        self.assertRaises(EasyProcessCheckError, lambda :  EasyProcess('sh -c xxxxx').check())


    def test_start(self):
        p = EasyProcess('ls -la').start()
        time.sleep(0.2)
        eq_(p.stop().return_code, 0)
    
    def test_alive(self):
        eq_(EasyProcess('ping 127.0.0.1 -c 2').is_alive(), False)
        eq_(EasyProcess('ping 127.0.0.1 -c 2').start().is_alive(), True)
        eq_(EasyProcess('ping 127.0.0.1 -c 2').start().stop().is_alive(), False)
        eq_(EasyProcess('ping 127.0.0.1 -c 2').call().is_alive(), False)
        
    def test_std(self):
        eq_(EasyProcess('echo hello').call().stdout, 'hello')
        
    def test_wait(self):
        eq_(EasyProcess('echo hello').wait().return_code, None)
        eq_(EasyProcess('echo hello').wait().stdout, None)
        
        eq_(EasyProcess('echo hello').start().wait().return_code, 0)
        eq_(EasyProcess('echo hello').start().wait().stdout, 'hello')
        
    def test_xephyr(self):
        EasyProcess('Xephyr -help').check(return_code=1)
        
    def test_wrap(self):
        def f():
            return EasyProcess('echo hi').call().stdout
        eq_(EasyProcess('ping 127.0.0.1').wrap(f)(), 'hi')
        
    def test_install(self):
        EasyProcess('echo hello').check_installed()
        self.assertRaises(EasyProcessCheckInstalledError, 
                          lambda :  EasyProcess('xecho', 
                                                url='http://xecho',
                                                ubuntu_package='xecho').check_installed())
        
        EasyProcess('echo', 
                                                url='http://xecho',
                                                ubuntu_package='xecho').check_installed()


