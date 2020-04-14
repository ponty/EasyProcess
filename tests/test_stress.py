from easyprocess import EasyProcess


def test_call():
    for x in range(1000):
        # test for:
        # OSError exception:[Errno 24] Too many open files
        print("index=", x)
        assert EasyProcess("echo hi").call().return_code == 0


#    def test_start(self):
#        for x in range(1000):
#            print('index=', x)
#            EasyProcess('echo hi').start()
