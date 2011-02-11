'''
Easy to use python subprocess interface.
'''

import logging
import platform
import shlex
import subprocess
import tempfile
import time

__version__ = '0.0.2'

log = logging.getLogger(__name__)
#log=logging

log.debug('EasyProcess version ' + __version__)

# deadlock test fails if USE_FILES=0
USE_FILES = 1

class EasyProcessCheckError(Exception):
    """This exception is raised when a process run by check() returns
    a non-zero exit status or OSError is raised.  
    """
    def __init__(self, easy_process):
        self.easy_process = easy_process
    def __str__(self):
        msg = 'EasyProcess check failed! \n OSError:{detail} \n cmd:{cmd} \n return code:{return_code} \n stderr:{stderr}'.format(
                            cmd=self.easy_process.cmd,
                            detail=self.easy_process.detail,
                            return_code=self.easy_process.return_code,
                            stderr=self.easy_process.stderr,
                            )
        return msg

template = '''cmd:{cmd}
OSError:{detail}  
Program install error! '''
class EasyProcessCheckInstalledError(Exception):
    """This exception is raised when a process run by check() returns
    a non-zero exit status or OSError is raised.  
    """
    def __init__(self, easy_process):
        self.easy_process = easy_process
    def __str__(self):
        msg = template.format(cmd=self.easy_process.cmd,
                          detail=self.easy_process.detail,
                          )
        if self.easy_process.url:
            msg += '\nhome page: ' + self.easy_process.url
        if platform.dist()[0].lower() == 'ubuntu':
            if self.easy_process.ubuntu_package:
                msg += '\nYou can install it in terminal:\n'
                msg += 'sudo apt-get install %s' % self.easy_process.ubuntu_package
        return msg

class EasyProcess():
    '''
    simple interface for :mod:`subprocess` 

    shell is not supported (shell=False)
    
    '''
    
    def __init__(self, cmd, ubuntu_package=None, url=None):
        '''
        :param cmd: string ('ls -l') or list of strings (['ls','-l']) 
        '''
        self.popen = None
        self.stdout = None
        self.stderr = None
        self._stdout_file = None
        self._stderr_file = None
        self.url = url
        self.ubuntu_package = ubuntu_package

        if hasattr(cmd, '__iter__'):
            # cmd is string list
            self.cmd = cmd
            self.cmd_as_string = ' '.join(cmd) # TODO: not perfect
        else:
            # cmd is string 
            self.cmd = shlex.split(cmd)
            self.cmd_as_string = cmd
        log.debug('command: %s (%s)' % (str(self.cmd), self.cmd_as_string))

        
    @property
    def pid(self):
        '''
        PID (subprocess.Popen.pid)

        :rtype: int
        '''
        if self.popen:
            return self.popen.pid
        
    @property
    def return_code(self):
        '''
        returncode (``subprocess.Popen.returncode``)

        :rtype: int
        '''
        if self.popen:
            return self.popen.returncode

    def check(self, return_code=0):
        '''
        Run command with arguments. Wait for command to complete.
        If the exit code was as expected and there is no exception then return, 
        otherwise raise EasyProcessCheckError.
        
        :param return_code: int, expected return code
        :rtype: self
        '''
        self.detail = None
        try:
            ret = self.call().return_code
            ok = ret == return_code
        except OSError as detail:
            log.debug('OSError exception')
            ok = False
            self.detail = detail
        if not ok:
            raise EasyProcessCheckError(self)
        return self

    def check_installed(self):
        '''
        Used for testing if program is installed.
        
        Run command with arguments. Wait for command to complete.
        If OSError raised, then raise :class:`EasyProcessCheckInstalledError`
        with information about program installation
        
        :param return_code: int, expected return code
        :rtype: self
        '''
        self.detail = None
        try:
            self.call()
        except OSError as detail:
            log.debug('OSError exception')
            self.detail = detail
            raise EasyProcessCheckInstalledError(self)
        return self
    
    def call(self):
        '''
        Run command with arguments. Wait for command to complete.
        Same as x.start().wait()
        
        :rtype: self
        '''
        return self.start().wait()

    def start(self):
        '''
        start command in background and does not wait for it
        
        :rtype: self
        '''
        if USE_FILES:
            self._stdout_file = tempfile.NamedTemporaryFile(prefix='stdout')
            self._stderr_file = tempfile.NamedTemporaryFile(prefix='stderr')
            #self._stdout_file = open('/tmp/stdout','w+')
            #self._stderr_file = open('/tmp/stderr','w+')
            
            self.popen = subprocess.Popen(self.cmd,
                                  stdout=self._stdout_file,
                                  stderr=self._stderr_file,
                                  #shell=1,
                                  )
        else:
            self.popen = subprocess.Popen(self.cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  #shell=1,
                                  )
        log.debug('process was started (pid:%s)' % (str(self.pid),))
        return self


    def is_alive(self):
        '''
        poll process (:func:`subprocess.Popen.poll`)
        
        :rtype: bool
        '''
        if self.popen:
            return self.popen.poll() is None
        else:
            return False
        
    def wait(self):
        '''
        Wait for command to complete.
        
        :rtype: self
        '''
        def remove_ending_lf(s):
            if s.endswith('\n'):
                return s[:-1]
            else:
                return s
        if self.popen:

            if USE_FILES:    
                self.popen.wait()
                self._stdout_file.seek(0)            
                self._stderr_file.seek(0)            
                self.stdout=self._stdout_file.read()
                self.stderr=self._stderr_file.read()
            else:
                # This will deadlock when using stdout=PIPE and/or stderr=PIPE 
                # and the child process generates enough output to a pipe such 
                # that it blocks waiting for the OS pipe buffer to accept more data. 
                # Use communicate() to avoid that.
                #self.popen.wait()
                #self.stdout = self.popen.stdout.read()
                #self.stderr = self.popen.stderr.read()
                (self.stdout, self.stderr) = self.popen.communicate()
            log.debug('process has ended')
            self.stdout = remove_ending_lf(self.stdout)
            self.stderr = remove_ending_lf(self.stderr)
            
            log.debug('return code=' + str(self.return_code))
            log.debug('stdout=' + self.stdout)
            log.debug('stderr=' + self.stderr)
        return self
            
    def stop(self):
        '''
        Kill process by sending SIGTERM.
        and wait for command to complete.
        
        same as ``sendstop().wait()``
        
        :rtype: self
        '''
        return self.sendstop().wait()

    def sendstop(self):
        '''
        Kill process by sending SIGTERM.
        Do not wait for command to complete.
        
        :rtype: self
        '''
        log.debug('stopping process (pid:%s cmd:"%s")' % (str(self.pid), self.cmd))
        if self.popen:
            if self.is_alive():
                log.debug('process is active -> sending SIGTERM')

                #os.kill(self.popen.pid, signal.SIGKILL)
                self.popen.terminate()
            else:
                log.debug('process was already stopped')
        else:
            log.debug('process was not started')

        return self
    
    def sleep(self, sec):
        '''
        sleeping (same as :func:`time.sleep`)

        :rtype: self
        '''
        time.sleep(sec)

        return self

    def wrap(self, callable, delay=0):
        '''
        
        :rtype: 
        '''
        def wrapped():
            self.start()   
            if delay:
                self.sleep(delay)     
            x = callable()
            self.stop()
            return x
        return wrapped
