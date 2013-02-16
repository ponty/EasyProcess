from easyprocess import EasyProcess
from nose.tools import timed, eq_
from pyvirtualdisplay.display import Display
import os.path
import sys

python = sys.executable

VISIBLE = 0

# deadlock in 0.0.0
# popen.communicate() hangs
# no deadlock with temp_files


@timed(4)
def test_deadlock():
    with Display(visible=VISIBLE, size=(600, 400)):
        p = EasyProcess([python, '-c', 'import Image;Image.new("RGB",(99, 99)).show()'])
        p.start()
        p.sleep(1)
        # hangs with pipes
        p.stop()

