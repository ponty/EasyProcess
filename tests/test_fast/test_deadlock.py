import sys

from nose.tools import timed
from pyvirtualdisplay.display import Display

from easyprocess import EasyProcess

python = sys.executable

VISIBLE = 0

# deadlock in 0.0.0
# popen.communicate() hangs
# no deadlock with temp_files


@timed(100)
def test_deadlock():
    # skip these tests for Windows/Mac
    if not sys.platform.startswith("linux"):
        return
    d = Display(visible=VISIBLE, size=(600, 400))
    d.start()

    p = EasyProcess([python, "-c", 'import Image;Image.new("RGB",(99, 99)).show()'])
    p.start()
    p.sleep(1)
    # hangs with pipes
    p.stop()

    d.stop()
