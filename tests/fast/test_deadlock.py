from easyprocess import EasyProcess
from nose.tools import timed

# deadlock in 0.0.0
# popen.communicate() hangs
# no deadlock with temp_files

@timed(1)
def test_stop():
    EasyProcess('python deadlock.py').start().sleep(0.5).stop()
    
