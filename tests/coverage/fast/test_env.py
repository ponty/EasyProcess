from easyprocess import EasyProcess
from nose.tools import eq_, ok_
import sys

python = sys.executable


def pass_env(e):
    return EasyProcess(
        [python, '-c', 'import os;print(dict(os.environ))'], env=e).call().stdout


def test_env():
    ok_(len(pass_env(None)))
    eq_(pass_env({}), '{}')
    eq_(pass_env(dict(x='2')), "{'x': '2'}")
