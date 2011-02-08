import logging
import shlex
import subprocess
import time

__version__='0.0.0'

log = logging.getLogger(__name__)
#log=logging

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

class EasyProcess():
    '''
    :mod:`subprocess` wrapper

    shell is not supported (shell=False)
    stdout is in self.stdout
    stderr is in self.stderr
    '''
    
    def __init__(self, cmd):
        '''
        :param cmd: string ('ls -l') or list of strings (['ls','-l']) 
        '''
        self.popen = None
        self.stdout = None
        self.stderr = None

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
        if self.popen:
            return self.popen.pid
        
    @property
    def return_code(self):
        if self.popen:
            return self.popen.returncode

    def _log_output(self):
        log.debug('return code=' + str(self.return_code))
        log.debug('stdout:\n' + self.stdout)
        log.debug('stderr:\n' + self.stderr)
    
    def check(self):
        '''
        Run command with arguments. Wait for command to complete.
        If the exit code was zero and there is no exception then return, 
        otherwise raise CalledProcessError.
        
        :rtype: bool
        '''
        self.detail = None
        try:
            ret = self.call().return_code
            ok = ret == 0
        except OSError as detail:
            log.debug('OSError exception')
            ok = False
            self.detail = detail
        if not ok:
            raise EasyProcessCheckError(self)
        return ok
    
    def call(self):
        '''
        Run command with arguments. Wait for command to complete.

        :rtype: self
        '''
        return self.start().wait()

    def start(self):
        '''
        start command in background and does not wait for it
        
        :rtype: self
        '''
        self.popen = subprocess.Popen(self.cmd,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              #shell=1,
                              )
        log.debug('process was started (pid:%s)' % (str(self.pid),))
        return self


    def is_alive(self):
        if self.popen:
            return self.popen.poll() is None
        else:
            return False
        
    def wait(self):
        '''
        :rtype: self
        '''
        def remove_ending_lf(s):
            if s.endswith('\n'):
                return s[:-1]
            else:
                return s
        if self.popen:
            self.popen.wait()
            log.debug('process has ended')
            self.stdout = remove_ending_lf(self.popen.stdout.read())
            self.stderr = remove_ending_lf(self.popen.stderr.read())
            self._log_output()
        return self
            
    def stop(self):
        '''
        kill process by sending SIGTERM

        :rtype: self
        '''
        log.debug('stopping process (pid:%s cmd:"%s")' % (str(self.pid), self.cmd))
        if self.popen:
            if self.is_alive():
                log.debug('process is active -> sending SIGTERM')
                #os.kill(self.popen.pid, signal.SIGKILL)
                
                #does not work with shell=True
                self.popen.terminate()
            else:
                log.debug('process was already stopped')
            self.wait()
        else:
            log.debug('process was not started')

        return self
    
    def sleep(self, sec):
        '''
        sleeping

        :rtype: self
        '''
        time.sleep(sec)

        return self
