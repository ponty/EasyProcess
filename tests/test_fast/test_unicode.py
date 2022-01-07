import sys

from easyprocess import EasyProcess
from easyprocess.unicodeutil import split_command

OMEGA = "\u03A9"

python = sys.executable


def platform_is_win():
    return sys.platform == "win32"


def py_minor():
    return sys.version_info[1]


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
    if not platform_is_win():
        assert EasyProcess("echo " + OMEGA).call().stdout == OMEGA
        assert EasyProcess(["echo", OMEGA]).call().stdout == OMEGA


def test_argv():
    assert (
        EasyProcess([python, "-c", r"import sys;assert sys.argv[1]=='123'", "123"])
        .call()
        .return_code
        == 0
    )
    assert (
        EasyProcess([python, "-c", r"import sys;assert sys.argv[1]=='\u03a9'", OMEGA])
        .call()
        .return_code
        == 0
    )


if py_minor() > 6:  # sys.stdout.reconfigure from py3.7

    def test_py_print():
        assert (
            EasyProcess(
                [
                    python,
                    "-c",
                    r"import sys;sys.stdout.reconfigure(encoding='utf-8');print('\u03a9')",
                ]
            )
            .call()
            .stdout
            == OMEGA
        )

        assert (
            EasyProcess(
                [
                    python,
                    "-c",
                    r"import sys;sys.stdout.reconfigure(encoding='utf-8');print(sys.argv[1])",
                    OMEGA,
                ]
            )
            .call()
            .stdout
            == OMEGA
        )


def test_py_stdout_write():
    assert (
        EasyProcess(
            [
                python,
                "-c",
                r"import sys;sys.stdout.buffer.write('\u03a9'.encode('utf-8'))",
            ]
        )
        .call()
        .stdout
        == OMEGA
    )


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
