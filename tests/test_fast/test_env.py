import json
import sys

from nose.tools import eq_, ok_

from easyprocess import EasyProcess

python = sys.executable


def pass_env(e):
    prog = "import os,json;print(json.dumps(dict(os.environ)))"
    s = EasyProcess([python, "-c", prog], env=e).call().stdout
    return json.loads(s)


def test_env():
    ok_(len(pass_env(None)))
    e = pass_env(None)
    eq_(pass_env(e).get("FOO"), None)
    e["FOO"] = "2"
    eq_(pass_env(e).get("FOO"), "2")
