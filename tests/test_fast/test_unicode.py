import sys

from easyprocess import EasyProcess
from easyprocess.unicodeutil import split_command

OMEGA = "\u03A9"

python = sys.executable


def test_str():
    assert EasyProcess("ls -la").call().return_code == 0


def test_ls():
    assert EasyProcess(["ls", "-la"]).call().return_code == 0


def test_parse():
    assert EasyProcess("ls -la").cmd == ["ls", "-la"]
    assert EasyProcess('ls "abc"').cmd == ["ls", "abc"]
    assert EasyProcess('ls "ab c"').cmd == ["ls", "ab c"]


def test_split():
    # list -> list
    assert split_command([str("x"), str("y")]) == ["x", "y"]
    assert split_command([str("x"), "y"]) == ["x", "y"]
    assert split_command([str("x"), OMEGA]) == ["x", OMEGA]

    # str -> list
    assert split_command(str("x y")) == ["x", "y"]
    assert split_command("x y") == ["x", "y"]
    assert split_command("x " + OMEGA) == ["x", OMEGA]

    # split windows paths #12
    assert split_command("c:\\temp\\a.exe someArg", posix=False) == [
        "c:\\temp\\a.exe",
        "someArg",
    ]


def test_echo():
    assert EasyProcess("echo hi").call().stdout == "hi"
    assert EasyProcess("echo " + OMEGA).call().stdout == OMEGA
    assert EasyProcess(["echo", OMEGA]).call().stdout == OMEGA


def test_invalid_stdout():
    """invalid utf-8 byte in stdout."""
    # https://en.wikipedia.org/wiki/UTF-8#Codepage_layout

    # 0x92  continuation byte
    cmd = [python, "-c", "import sys;sys.stdout.buffer.write(b'\\x92')"]
    p = EasyProcess(cmd).call()
    assert p.return_code == 0
    assert p.stdout == ""

    # 0xFF must never appear in a valid UTF-8 sequence
    cmd = [python, "-c", "import sys;sys.stdout.buffer.write(b'\\xFF')"]
    p = EasyProcess(cmd).call()
    assert p.return_code == 0
    assert p.stdout == ""
