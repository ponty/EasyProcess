import json
import sys

from easyprocess import EasyProcess

python = sys.executable


def pass_env(e):
    """
    Pass in the environment and return a json object.

    Args:
        e: (todo): write your description
    """
    prog = "import os,json;print(json.dumps(dict(os.environ)))"
    s = EasyProcess([python, "-c", prog], env=e).call().stdout
    return json.loads(s)


def test_env():
    """
    Test if the current environment.

    Args:
    """
    assert len(pass_env(None)) > 0
    e = pass_env(None)
    assert pass_env(e).get("FOO") is None
    e["FOO"] = "2"
    assert pass_env(e).get("FOO") == "2"
