from unittest import TestCase


from easyprocess import EasyProcess, EasyProcessError


class Test(TestCase):
    def test_is_started(self):
        assert EasyProcess("ls -la").is_started is False
        assert EasyProcess("ls -la").start().is_started
        assert EasyProcess("ls -la").call().is_started
        assert EasyProcess("ls -la").start().wait().is_started
        assert EasyProcess("ls -la").start().stop().is_started

    def test_raise(self):
        self.assertRaises(
            EasyProcessError, lambda: EasyProcess("ls -la").start().start()
        )
        self.assertRaises(EasyProcessError, lambda: EasyProcess("ls -la").stop())
        self.assertRaises(EasyProcessError, lambda: EasyProcess("ls -la").sendstop())
        # self.assertRaises(EasyProcessError, lambda : EasyProcess('ls
        # -la').start().stop().stop())
        self.assertRaises(
            EasyProcessError, EasyProcess("ls -la").start().wrap(lambda: None)
        )
        EasyProcess("ls -la").wrap(lambda: None)()
