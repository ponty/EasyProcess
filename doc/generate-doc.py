import glob
import logging
import os

from entrypoint2 import entrypoint

from easyprocess import EasyProcess

commands = [
    "python3 -m easyprocess.examples.hello",
    "python3 -m easyprocess.examples.cmd",
    "python3 -m easyprocess.examples.timeout",
    "python3 -m easyprocess.examples.with",
]


def empty_dir(dir):
    files = glob.glob(os.path.join(dir, "*"))
    for f in files:
        os.remove(f)


@entrypoint
def main():
    gendir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen")
    logging.info("gendir: %s", gendir)
    os.makedirs(gendir, exist_ok=True)
    empty_dir(gendir)
    pls = []
    try:
        os.chdir("gen")
        for cmd in commands:
            logging.info("cmd: %s", cmd)
            fname_base = cmd.replace(" ", "_")
            fname = fname_base + ".txt"
            logging.info("cmd: %s", cmd)
            print("file name: %s" % fname)
            with open(fname, "w") as f:
                f.write("$ " + cmd + "\n")
                p = EasyProcess(cmd).call()
                f.write(p.stdout)
                f.write(p.stderr)
                pls += [p]
    finally:
        os.chdir("..")
        for p in pls:
            p.stop()
    embedme = EasyProcess(["embedme", "../README.md"])
    embedme.call()
    print(embedme.stdout)
    assert embedme.return_code == 0
    assert "but file does not exist" not in embedme.stdout
