from easyprocess import EasyProcess
from nose.tools import eq_, ok_
import sys

python = sys.executable


def pass_env(e):
    # py37 creates "LC_CTYPE" automatically
    prog = 'import os;d=dict(os.environ);d.pop("LC_CTYPE",None);print(d)'
    return EasyProcess([python, '-c', prog], env=e).call().stdout


def test_env():
    ok_(len(pass_env(None)))
    eq_(pass_env({}), '{}')
    eq_(pass_env(dict(x='2')), "{'x': '2'}")
