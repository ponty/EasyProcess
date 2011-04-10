from easyprocess import EasyProcess
from nose.tools import eq_
from unittest import TestCase


class Test(TestCase):
    def test_max_size(self):
        eq_(EasyProcess('echo 123456', max_bytes_to_log=2).call().stdout, '1..6')
        eq_(EasyProcess('echo 123456', max_bytes_to_log=3).call().stdout, '12..56')
        eq_(EasyProcess('echo 123456', max_bytes_to_log=4).call().stdout, '12..56')
        eq_(EasyProcess('echo 123456', max_bytes_to_log=5).call().stdout, '123456')
        eq_(EasyProcess('echo 123456', max_bytes_to_log=6).call().stdout, '123456')
        eq_(EasyProcess('echo 123456', max_bytes_to_log=8).call().stdout, '123456')

        eq_(EasyProcess('echo 12345', max_bytes_to_log=2).call().stdout, '1..5')
        eq_(EasyProcess('echo 12345', max_bytes_to_log=3).call().stdout, '12..45')
        eq_(EasyProcess('echo 12345', max_bytes_to_log=4).call().stdout, '12..45')
        eq_(EasyProcess('echo 12345', max_bytes_to_log=5).call().stdout, '12345')
        eq_(EasyProcess('echo 12345', max_bytes_to_log=6).call().stdout, '12345')
        eq_(EasyProcess('echo 12345', max_bytes_to_log=8).call().stdout, '12345')
