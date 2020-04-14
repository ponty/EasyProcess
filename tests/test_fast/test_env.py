import json
import sys

from easyprocess import EasyProcess

python = sys.executable


def pass_env(e):
    prog = "import os,json;print(json.dumps(dict(os.environ)))"
    s = EasyProcess([python, "-c", prog], env=e).call().stdout
    return json.loads(s)


def test_env():
    assert len(pass_env(None)) > 0
    e = pass_env(None)
    assert pass_env(e).get("FOO") is None
    e["FOO"] = "2"
    assert pass_env(e).get("FOO") == "2"
