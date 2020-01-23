import sys

from nose.tools import eq_

from easyprocess import EasyProcess


def test():
    # skip these tests for Windows/Mac
    if not sys.platform.startswith("linux"):
        return
    eq_(
        EasyProcess([sys.executable, "-m", "easyprocess.examples.ver"])
        .call()
        .return_code,
        0,
    )
    eq_(
        EasyProcess([sys.executable, "-m", "easyprocess.examples.log"])
        .call()
        .return_code,
        0,
    )
    eq_(
        EasyProcess([sys.executable, "-m", "easyprocess.examples.cmd"])
        .call()
        .return_code,
        0,
    )
    eq_(
        EasyProcess([sys.executable, "-m", "easyprocess.examples.hello"])
        .call()
        .return_code,
        0,
    )
    eq_(
        EasyProcess([sys.executable, "-m", "easyprocess.examples.timeout"])
        .call()
        .return_code,
        0,
    )
