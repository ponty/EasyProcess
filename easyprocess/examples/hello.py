from easyprocess import EasyProcess
import sys
python = sys.executable
s = EasyProcess([python, '-c', 'print "hello"']).call().stdout
print(s)
