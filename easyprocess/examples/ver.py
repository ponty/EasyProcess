from easyprocess import EasyProcess
import sys
python = sys.executable
v = EasyProcess([python, '--version']).call().stderr
print('your python version:%s' % v)
