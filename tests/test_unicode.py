from easyprocess import EasyProcess
from nose.tools import eq_
from unittest import TestCase


class Test(TestCase):
    def test_str(self):
        eq_(EasyProcess(unicode('ls -la')).call().return_code, 0)
    def test_ls(self):
        eq_(EasyProcess([unicode('ls'), unicode('-la')]).call().return_code, 0)
    
    def test_parse(self):
        eq_(EasyProcess(unicode('ls -la')).cmd, ['ls', '-la'])
        eq_(EasyProcess(unicode('ls "abc"')).cmd, ['ls', 'abc'])
        eq_(EasyProcess(unicode('ls "ab c"')).cmd, ['ls', 'ab c'])
