import sys

from easyprocess import EasyProcess

python = sys.executable
s = EasyProcess([python, "-c", 'print "hello"']).call().stdout
print(s)
