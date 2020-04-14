import sys
from unittest import TestCase

import six

from easyprocess import EasyProcess
from easyprocess.unicodeutil import EasyProcessUnicodeError, split_command

u = six.u
OMEGA = u("\u03A9")

python = sys.executable


class Test(TestCase):
    def test_str(self):
        assert EasyProcess(u("ls -la")).call().return_code == 0

    def test_ls(self):
        assert EasyProcess([u("ls"), u("-la")]).call().return_code == 0

    def test_parse(self):
        assert EasyProcess(u("ls -la")).cmd == ["ls", "-la"]
        assert EasyProcess(u('ls "abc"')).cmd == ["ls", "abc"]
        assert EasyProcess(u('ls "ab c"')).cmd == ["ls", "ab c"]

    def test_split(self):
        # list -> list
        assert split_command([str("x"), str("y")]) == ["x", "y"]
        assert split_command([str("x"), u("y")]) == ["x", "y"]
        assert split_command([str("x"), OMEGA]) == ["x", OMEGA]

        # str -> list
        assert split_command(str("x y")) == ["x", "y"]
        assert split_command(u("x y")) == ["x", "y"]
        if six.PY3:
            assert split_command(u("x ") + OMEGA) == ["x", OMEGA]
        else:
            self.assertRaises(
                EasyProcessUnicodeError, lambda: split_command(u("x ") + OMEGA)
            )

        # split windows paths #12
        assert (
            split_command("c:\\temp\\a.exe someArg", posix=False)
            == ["c:\\temp\\a.exe", "someArg"],
        )

    def test_echo(self):
        assert EasyProcess(u("echo hi")).call().stdout == "hi"

        if six.PY3:
            assert EasyProcess(u("echo ") + OMEGA).call().stdout == OMEGA
        else:
            # unicode is not supported
            self.assertRaises(
                EasyProcessUnicodeError,
                lambda: EasyProcess(u("echo ") + OMEGA).call().stdout,
            )

        assert EasyProcess(["echo", OMEGA]).call().stdout == OMEGA

    def test_invalid_stdout(self):
        """invalid utf-8 byte in stdout."""
        # https://en.wikipedia.org/wiki/UTF-8#Codepage_layout

        # 0x92  continuation byte
        if six.PY3:
            cmd = [python, "-c", "import sys;sys.stdout.buffer.write(b'\\x92')"]
        else:
            cmd = [python, "-c", "import sys;sys.stdout.write(b'\\x92')"]
        p = EasyProcess(cmd).call()
        assert p.return_code == 0
        assert p.stdout == ""

        # 0xFF must never appear in a valid UTF-8 sequence
        if six.PY3:
            cmd = [python, "-c", "import sys;sys.stdout.buffer.write(b'\\xFF')"]
        else:
            cmd = [python, "-c", "import sys;sys.stdout.write(b'\\xFF')"]
        p = EasyProcess(cmd).call()
        assert p.return_code == 0
        assert p.stdout == ""
