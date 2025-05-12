#! /usr/bin/python3
###############################################################################
 #    BSD LICENSE
 #
 #    Copyright (c) Saul Han <2573789168@qq.com>
 #
 #    Redistribution and use in source and binary forms, with or without
 #    modification, are permitted provided that the following conditions
 #    are met:
 #
 #       Redistributions of source code must retain the above copyright
 #        notice, this list of conditions and the following disclaimer.
 #       Redistributions in binary form must reproduce the above copyright
 #        notice, this list of conditions and the following disclaimer in
 #        the documentation and/or other materials provided with the
 #        distribution.
 #
 #    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 #    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 #    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 #    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 #    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 #    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 #    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 #    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 #    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 #    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 #    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################
import time
import subprocess
class SystemCmd(object):
    def __init__(self, logger=None):
        if logger is None:
            class Logger(object):
                def __init__(self, cb_log=print):
                    self.critical = lambda x: cb_log("%s CRITICAL: %s" % (time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()), x))
                    self.debug = lambda x: cb_log("%s DEBUG: %s" % (time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()), x))
                    self.error = lambda x: cb_log("%s ERROR: %s" % (time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()), x))
                    self.info = lambda x: cb_log("%s INFO: %s" % (time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()), x))
                    self.warning = lambda x: cb_log("%s WARNING: %s" % (time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()), x))
            self.logger = Logger()
        else:
            self.logger = logger

    def check_return_code(self, cmdline, check_pass, check_code, ret, readline=None, raise_flag=True, cb_log=print):
        """
        Check if the return code of a command matches the expected value.

        Parameters:
        - cmdline (str): The command line string that was executed.
        - check_pass (bool): Indicates whether to check for successful execution.
        - check_code (int/str): The expected return code or a string expected in the output.
        - ret (int): The actual return code from the command execution.
        - readline (str, optional): The output from the command execution.
        - raise_flag (bool, optional): Whether to raise an exception, defaults to True.
        - cb_log (function, optional): Logging function, defaults to print.

        Returns:
        None. This function may raise an exception or log messages based on the checks.
        """
        # Check for successful execution scenario
        if check_pass:
            # If raise_flag is True and the actual return code is non-zero, raise an exception
            assert not(raise_flag and ret), cb_log("cmdline is %s. Return miscompare! ReturnCode: expected 0x%x, actual 0x%x, readline is %s" % (cmdline, 0, ret, readline))
        else:
            # Perform different validations based on the type of check_code (integer or string)
            if isinstance(check_code, int):
                # When the expected return code is 0 and the actual return code is also 0, validate raise_flag
                if check_code == 0 and ret == 0:
                    assert raise_flag, cb_log("cmdline is %s. Return miscompare! ReturnCode: expected False, actual 0x%x" % (cmdline, ret))
                # When the expected return code is non-zero and does not match the actual return code, validate raise_flag
                elif check_code != 0 and ret != check_code:
                    assert raise_flag, cb_log("cmdline is %s. Return miscompare! ReturnCode: expected False, expected return code %s, actual 0x%x" % (cmdline, check_code, ret))
                # When the expected return code is non-zero and matches the actual return code, log that it meets expectations
                elif check_code != 0 and ret == check_code:
                    cb_log("cmdline is %s. Return expected! expected return code %s, actual 0x%x" % (cmdline, check_code, ret))
                # For other cases where the expected return code is non-zero but the actual return code is 0, log that it meets expectations
                else:
                    cb_log("cmdline is %s. Return expected! not to check return code %s, actual 0x%x" % (cmdline, check_code, ret))
            # When the expected result is a string, check if the command output contains this string
            elif isinstance(check_code, str):
                if check_code not in readline:
                    assert raise_flag, cb_log(f"cmdline is {cmdline}. Return miscompare! expect return {check_code}")


    def send_cmd(self, cmdline=None, check_ret=True, check_pass=True, check_code=0, show_log=True, stdout=False, input=None, cb_log=print, raise_flag=True, get_status_output=False,
                 disable_repeat_info=False):
        """
        Executes a system command and handles its output and errors.

        Parameters:
        - cmdline: The command line string to execute.
        - check_ret: Whether to check the return code of the command execution.
        - check_pass: Whether to check if the command executed successfully.
        - check_code: Expected return code.
        - show_log: Whether to display the command's output log.
        - stdout: Whether to return the command's output instead of the return code.
        - input: Data to be input into the command.
        - cb_log: Callback function for logging, defaults to print.
        - raise_flag: Whether to raise an exception if the command fails.
        - get_status_output: Whether to return both the return code and the output of the command.
        - disable_repeat_info: Whether to disable repeated information output.

        Returns:
        - If get_status_output is True, returns a tuple of the command's return code and output.
        - If stdout is True, returns the command's output.
        - Otherwise, returns the command's return code.
        """
        # Execute the command, depending on whether input data is provided
        if input:
            p = subprocess.run(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, input=input)
        else:
            p = subprocess.run(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # Retrieve the command's return code and output
        ret = p.returncode
        readline = p.stdout.decode(errors='ignore')

        # Handle and log the command's output based on disable_repeat_info parameter
        if not disable_repeat_info:
            # Log command execution information using logger or cb_log
            if hasattr(self.logger, 'info'):
                self.logger.info("the system cmd is '%s' and return %d" % (cmdline, ret))
            else:
                cb_log("the system cmd is '%s' and return %d" % (cmdline, ret))

            # Display the command's output log based on show_log and check_pass parameters
            if show_log or (check_pass and ret):
                cb_log("the command print log \n %s" % readline)

        # Check the command's return code based on check_ret parameter
        if check_ret:
            self.check_return_code(cmdline=cmdline, check_pass=check_pass, check_code=check_code, ret=ret, readline=readline, raise_flag=raise_flag, cb_log=cb_log)

        # Determine the return value based on get_status_output parameter
        if get_status_output:
            return ret, readline
        return readline if stdout else ret
