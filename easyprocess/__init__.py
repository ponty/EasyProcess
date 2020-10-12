"""Easy to use python subprocess interface."""

import logging
import os.path
import signal
import subprocess
import tempfile
import threading
import time

from easyprocess.about import __version__
from easyprocess.unicodeutil import split_command, unidecode, uniencode

log = logging.getLogger(__name__)

log.debug("version=%s", __version__)

POLL_TIME = 0.1
USE_POLL = 0


class EasyProcessError(Exception):
    def __init__(self, easy_process, msg=""):
        self.easy_process = easy_process
        self.msg = msg

    def __str__(self):
        return self.msg + " " + repr(self.easy_process)


template = """cmd=%s
OSError=%s
Program install error! """


class EasyProcess(object):

    """
    .. module:: easyprocess

    simple interface for :mod:`subprocess`

    shell is not supported (shell=False)

    .. warning::

      unicode is supported only for string list command (Python2.x)
      (check :mod:`shlex` for more information)

    :param cmd: string ('ls -l') or list of strings (['ls','-l'])
    :param cwd: working directory
    :param use_temp_files: use temp files instead of pipes for
                           stdout and stderr,
                           pipes can cause deadlock in some cases
                           (see unit tests)

    :param env: If *env* is not ``None``, it must be a mapping that defines the environment
                   variables for the new process; these are used instead of inheriting the current
                   process' environment, which is the default behavior.
                   (check :mod:`subprocess`  for more information)
    """

    def __init__(
        self, cmd, cwd=None, use_temp_files=True, env=None,
    ):
        self.use_temp_files = use_temp_files
        self._outputs_processed = False

        self.env = env
        self.popen = None
        self.stdout = None
        self.stderr = None
        self._stdout_file = None
        self._stderr_file = None
        self.is_started = False
        self.oserror = None
        self.cmd_param = cmd
        self._thread = None
        self.timeout_happened = False
        self.cwd = cwd
        cmd = split_command(cmd)
        self.cmd = cmd
        # self.cmd_as_string = " ".join(self.cmd)
        self.enable_stdout_log = True
        self.enable_stderr_log = True

        # log.debug('param: "%s" ', self.cmd_param)
        log.debug("command: %s", self.cmd)
        # log.debug('joined command: %s', self.cmd_as_string)

        if not len(cmd):
            raise EasyProcessError(self, "empty command!")

    def __repr__(self):
        msg = (
            '<%s cmd_param=%s cmd=%s oserror=%s return_code=%s stdout="%s" stderr="%s" timeout_happened=%s>'
            % (
                self.__class__.__name__,
                self.cmd_param,
                self.cmd,
                self.oserror,
                self.return_code,
                self.stdout,
                self.stderr,
                self.timeout_happened,
            )
        )
        return msg

    @property
    def pid(self):
        """
        PID (:attr:`subprocess.Popen.pid`)

        :rtype: int
        """
        if self.popen:
            return self.popen.pid

    @property
    def return_code(self):
        """
        returncode (:attr:`subprocess.Popen.returncode`)

        :rtype: int
        """
        if self.popen:
            return self.popen.returncode

    def call(self, timeout=None, kill_after=None):
        """Run command with arguments. Wait for command to complete.

        same as:
         1. :meth:`start`
         2. :meth:`wait`
         3. :meth:`stop`

        :rtype: self

        """
        self.start().wait(timeout=timeout)
        if self.is_alive():
            self.stop(kill_after=kill_after)
        return self

    def start(self):
        """start command in background and does not wait for it.

        :rtype: self

        """
        if self.is_started:
            raise EasyProcessError(self, "process was started twice!")

        if self.use_temp_files:
            self._stdout_file = tempfile.TemporaryFile(prefix="stdout_")
            self._stderr_file = tempfile.TemporaryFile(prefix="stderr_")
            stdout = self._stdout_file
            stderr = self._stderr_file

        else:
            stdout = subprocess.PIPE
            stderr = subprocess.PIPE

        cmd = list(map(uniencode, self.cmd))

        try:
            self.popen = subprocess.Popen(
                cmd, stdout=stdout, stderr=stderr, cwd=self.cwd, env=self.env,
            )
        except OSError as oserror:
            log.debug("OSError exception: %s", oserror)
            self.oserror = oserror
            raise EasyProcessError(self, "start error")
        self.is_started = True
        log.debug("process was started (pid=%s)", self.pid)
        return self

    def is_alive(self):
        """
        poll process using :meth:`subprocess.Popen.poll`
        It updates stdout/stderr/return_code if process has stopped earlier.
        
        :rtype: bool
        """
        if self.popen:
            alive = self.popen.poll() is None

            if not alive:
                # collect stdout/stderr/return_code if proc stopped
                self._wait4process()

            return alive
        else:
            return False

    def wait(self, timeout=None):
        """Wait for command to complete.

        Timeout:
         - discussion: http://stackoverflow.com/questions/1191374/subprocess-with-timeout
         - implementation: threading

        :rtype: self

        """

        if timeout is not None:
            if not self._thread:
                self._thread = threading.Thread(target=self._wait4process)
                self._thread.daemon = 1
                self._thread.start()

        if self._thread:
            self._thread.join(timeout=timeout)
            self.timeout_happened = self.timeout_happened or self._thread.is_alive()
        else:
            # no timeout and no existing thread
            self._wait4process()

        return self

    def _wait4process(self):
        if self._outputs_processed:
            return

        def remove_ending_lf(s):
            if s.endswith("\n"):
                s = s[:-1]
            if s.endswith("\r"):
                s = s[:-1]
            return s

        if self.popen:
            if self.use_temp_files:
                if USE_POLL:
                    while True:
                        if self.popen.poll() is not None:
                            break
                        # if self._stop_thread:
                        #     return
                        time.sleep(POLL_TIME)

                else:
                    # wait() blocks process, timeout not possible
                    self.popen.wait()

                self._stdout_file.seek(0)
                self._stderr_file.seek(0)
                self.stdout = self._stdout_file.read()
                self.stderr = self._stderr_file.read()

                self._stdout_file.close()
                self._stderr_file.close()
            else:
                # This will deadlock when using stdout=PIPE and/or stderr=PIPE
                # and the child process generates enough output to a pipe such
                # that it blocks waiting for the OS pipe buffer to accept more data.
                # Use communicate() to avoid that.
                # self.popen.wait()
                # self.stdout = self.popen.stdout.read()
                # self.stderr = self.popen.stderr.read()

                # communicate() blocks process, timeout not possible
                (self.stdout, self.stderr) = self.popen.communicate()
            log.debug("process has ended, return code=%s", self.return_code)
            self.stdout = remove_ending_lf(unidecode(self.stdout))
            self.stderr = remove_ending_lf(unidecode(self.stderr))
            self._outputs_processed = True

            #            def limit_str(s):
            #                if len(s) > self.max_bytes_to_log:
            #                    warn = '[middle of output was removed, max_bytes_to_log=%s]'%(self.max_bytes_to_log)
            #                    s = s[:self.max_bytes_to_log / 2] + warn + s[-self.max_bytes_to_log / 2:]
            #                return s
            if self.enable_stdout_log:
                log.debug("stdout=%s", self.stdout)
            if self.enable_stderr_log:
                log.debug("stderr=%s", self.stderr)

    def stop(self, kill_after=None):
        """Kill process and wait for command to complete.

        same as:
         1. :meth:`sendstop`
         2. :meth:`wait`

        :rtype: self

        """
        self.sendstop().wait(timeout=kill_after)
        if self.is_alive() and kill_after is not None:
            self.sendstop(kill=True).wait()
        return self

    def sendstop(self, kill=False):
        """
        Kill process (:meth:`subprocess.Popen.terminate`).
        Do not wait for command to complete.

        :rtype: self
        """
        if not self.is_started:
            raise EasyProcessError(self, "process was not started!")

        log.debug('stopping process (pid=%s cmd="%s")', self.pid, self.cmd)
        if self.popen:
            if self.is_alive():
                signame = "SIGKILL" if kill else "SIGTERM"
                log.debug("process is active -> sending " + signame)

                try:
                    try:
                        if kill:
                            self.popen.kill()
                        else:
                            self.popen.terminate()
                    except AttributeError:
                        os.kill(self.popen.pid, signal.SIGKILL)
                except OSError as oserror:
                    log.debug("exception in terminate:%s", oserror)

            else:
                log.debug("process was already stopped")
        else:
            log.debug("process was not started")

        return self

    def sleep(self, sec):
        """
        sleeping (same as :func:`time.sleep`)

        :rtype: self
        """
        time.sleep(sec)

        return self

    def wrap(self, func, delay=0):
        """
        returns a function which:
         1. start process
         2. call func, save result
         3. stop process
         4. returns result

        similar to :keyword:`with` statement

        :rtype:
        """

        def wrapped():
            self.start()
            if delay:
                self.sleep(delay)
            x = None
            try:
                x = func()
            except OSError as oserror:
                log.debug("OSError exception:%s", oserror)
                self.oserror = oserror
                raise EasyProcessError(self, "wrap error!")
            finally:
                self.stop()
            return x

        return wrapped

    def __enter__(self):
        """used by the :keyword:`with` statement"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """used by the :keyword:`with` statement"""
        self.stop()
