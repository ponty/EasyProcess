from easyprocess import EasyProcess

v = EasyProcess('python --version').call().stderr
print 'your python version:', v

