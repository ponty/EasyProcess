from easyprocess import EasyProcess
from nose.tools import eq_
from nose.tools import timed
from pyvirtualdisplay.display import Display
import sys

python = sys.executable

VISIBLE = 0

# deadlock in 0.0.0
# popen.communicate() hangs
# no deadlock with temp_files


@timed(100)
def test_deadlock():
    d = Display(visible=VISIBLE, size=(600, 400))
    d.start()

    p = EasyProcess(
        [python, '-c', 'import Image;Image.new("RGB",(99, 99)).show()'])
    p.start()
    p.sleep(1)
    # hangs with pipes
    p.stop()

    d.stop()
