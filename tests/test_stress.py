from easyprocess import EasyProcess
from easyprocess import EasyProcessError
from nose.tools import eq_


def test_call():
    for x in range(1000):
        # test for:
        # OSError exception:[Errno 24] Too many open files
        print('index=', x)
        eq_(EasyProcess('echo hi').call().return_code, 0)

#    def test_start(self):
#        for x in range(1000):
#            print('index=', x)
#            EasyProcess('echo hi').start()
