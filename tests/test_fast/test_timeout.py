import sys
from unittest import TestCase
import pytest

from easyprocess import EasyProcess

python = sys.executable


class Test(TestCase):
    def test_timeout(self):
        p = EasyProcess("sleep 1").start()
        p.wait(0.2)
        assert p.is_alive()
        p.wait(0.2)
        assert p.is_alive()
        p.wait(2)
        assert not p.is_alive()

        assert EasyProcess("sleep 0.3").call().return_code == 0
        assert EasyProcess("sleep 0.3").call(timeout=0.1).return_code != 0
        assert EasyProcess("sleep 0.3").call(timeout=1).return_code == 0

        assert EasyProcess("sleep 0.3").call().timeout_happened is False
        assert EasyProcess("sleep 0.3").call(timeout=0.1).timeout_happened
        assert EasyProcess("sleep 0.3").call(timeout=1).timeout_happened is False

    @pytest.mark.timeout(3)
    def test_time_cli1(self):
        p = EasyProcess(
            [
                python,
                "-c",
                "import logging;logging.basicConfig(level=logging.DEBUG);from easyprocess import EasyProcess;EasyProcess('sleep 5').start()",
            ]
        )
        p.call()
        assert p.return_code == 0

    @pytest.mark.timeout(3)
    def test_time_cli2(self):
        p = EasyProcess(
            [
                python,
                "-c",
                "import logging;logging.basicConfig(level=logging.DEBUG);from easyprocess import EasyProcess;EasyProcess('sleep 5').call(timeout=0.5)",
            ]
        )
        p.call()
        assert p.return_code == 0

    @pytest.mark.timeout(3)
    def test_time2(self):
        p = EasyProcess("sleep 5").call(timeout=1)
        assert p.is_alive() is False
        assert p.timeout_happened
        assert p.return_code != 0
        assert p.stdout == ""

    @pytest.mark.timeout(3)
    def test_timeout_out(self):
        p = EasyProcess(
            [python, "-c", "import time;print( 'start');time.sleep(5);print( 'end')"]
        ).call(timeout=1)
        assert p.is_alive() is False
        assert p.timeout_happened
        assert p.return_code != 0
        assert p.stdout == ""

    @pytest.mark.timeout(0.3)
    def test_time3(self):
        EasyProcess("sleep 5").start()
