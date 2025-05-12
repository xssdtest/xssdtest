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
import os
import signal
import sys
import traceback
RAISEFLAG = 0
class CatchException(object):
    """
    A decorator class for catching exceptions during function execution and logging or printing error information.

    This class is primarily used to wrap functions for test case execution. If an exception occurs,
    it logs the exception using a provided logger, or prints it if no logger is available.
    It also sets a global flag (`RAISEFLAG`) to indicate that a failure occurred and raises
    an exception to terminate the current test case.

    Attributes:
        func (function): The wrapped function to be executed with exception handling.
        logger (object): Optional. Logger instance from the decorated method's owner.
    """

    def __init__(self, func):
        """
        Initialize the decorator with the target function.

        Parameters:
            func (function): The function to be wrapped by this decorator.
        """
        self.func = func

    def __call__(self, *args, **kwargs):
        """
        Executes the wrapped function and catches any raised exceptions.

        Parameters:
            *args: Positional arguments passed to the wrapped function.
            **kwargs: Keyword arguments passed to the wrapped function.

        Behavior:
            - Tries to execute the decorated function.
            - On exception:
              - Captures the full traceback.
              - Logs the error using `logger.error()` if a valid logger is provided.
              - Otherwise, prints the error trace to stdout.
              - Sets RAISEFLAG to 1.
              - Re-raises a generic Exception indicating test case failure.
        """
        try:
            self.func(*args, **kwargs)
        except Exception as e:
            call_trace = ''.join(traceback.format_exception(*sys.exc_info()))
            logger = kwargs.get('logger') if kwargs.get('logger') else None
            if hasattr(logger, 'error'):
                call_trace = ''.join(traceback.format_exception(*sys.exc_info()))
                logger.error('%s \n Raise info\n %s' % (call_trace, e))
                logger.error("The script raise a error and exit 1")
            else:
                print('%s \n Raise info\n %s' % (call_trace, e))
                print("The script raise a error and exit 1")
            RAISEFLAG = 1
            raise Exception("This case failed")

    def __get__(self, instance, owner):
        """
        Descriptor method to support wrapping instance methods with exception handling.

        Parameters:
            instance (object): The object instance owning the method being wrapped.
            owner (type): The type of the instance.

        Behavior:
            - Attempts to execute the wrapped method.
            - Catches any exceptions and logs them if a logger is available.
            - Always performs a filesystem sync in the `finally` block.
        """
        if hasattr(instance, "logger"):
            self.logger = instance.logger
        else:
            self.logger = None
        try:
            self.func(instance)
        except Exception as e:
            if self.logger:
                call_trace = ''.join(traceback.format_exception(*sys.exc_info()))
                self.logger.error('%s \n Raise info\n %s' % (call_trace, e))
                self.logger.error("The script raise a error and exit 1")
            else:
                call_trace = ''.join(traceback.format_exception(*sys.exc_info()))
                print('%s \n Raise info\n %s' % (call_trace, e))
                print("The script raise a error and exit 1")
            RAISEFLAG = 1
        finally:
            os.system('sync')

    @staticmethod
    def set_timeout(num):
        """
        Static method that returns a decorator to enforce a timeout on function execution.

        Parameters:
            num (int): Timeout duration in seconds.

        Returns:
            function: A decorator that wraps a function to add timeout behavior.

        Wrapped Function Behavior:
            - Uses SIGALRM to monitor execution time.
            - Raises a RuntimeError if the function does not complete within the specified time.
            - Exits with status 1 if a previous error was already raised (`RAISEFLAG == 1`).
        """
        def wrap(func):
            def handle(signum, frame): raise RuntimeError
            def to_do(*args, **kwargs):
                try:
                    signal.signal(signal.SIGALRM, handle)
                    signal.alarm(num)
                    r = func(*args, **kwargs)
                    signal.alarm(0)
                    return r
                except RuntimeError as e:
                    if RAISEFLAG == 1:
                        exit(1)
            return to_do
        return wrap


