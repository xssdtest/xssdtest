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
import sys
import time
import threading
import traceback
class XTThread(threading.Thread):  # The XTThread class is derived from the class threading.Thread
    def __init__(self, target=None, name = None, args = (), kwargs = None, *, daemon=True):
        """This constructor should always be called with keyword arguments. Arguments are:

        *target* is the callable object to be invoked by the run()
        method. Defaults to None, meaning nothing is called.

        *name* is the thread name. By default, a unique name is constructed of
        the form "Thread-N" where N is a small decimal number.

        *args* is the argument tuple for the target invocation. Defaults to ().

        *kwargs* is a dictionary of keyword arguments for the target
        invocation. Defaults to {}.

        If a subclass overrides the constructor, it must make sure to invoke
        the base class constructor (Thread.__init__()) before doing anything
        else to the thread.

        """
        threading.Thread.__init__(self, name=name, daemon=daemon)
        if kwargs is None:
            kwargs = {}
        self._target = target
        if type(args) is tuple:
            self._args = args
        else:
            self._args = (args,)
        self._kwargs = kwargs
        self._name = "%s_thread%s"%(self._target.__name__, self._name)
        self.exitcode = None
        self.exception = None
        self.exc_traceback = ''

    def run(self):
        """
        Overwrite the run() method to specify what the thread should execute.
        This method is responsible for executing the target function and handling any exceptions that occur.
        """
        try:
            # Record the start time of the thread execution
            self._stime = time.time()
            # Execute the target function with the provided arguments and keyword arguments
            self._return = self._target(*(self._args), **self._kwargs)
        except Exception as e:
            # If an exception occurs during the execution of the target function, set the exit code to 1
            self.exitcode = 1
            # Save the exception information for potential error handling or logging
            self.exception = e
            # Capture the exception traceback and store it as a string
            self.exc_traceback = ''.join(traceback.format_exception(*sys.exc_info()))
            # Print the exception traceback
            print(self.exc_traceback)
        else:
            # If the target function executes successfully, set the exit code to 0
            self.exitcode = 0
        finally:
            # Calculate and store the runtime of the thread
            self._runtime = time.time() - self._stime
            # Delete the thread's arguments and keyword arguments to free up memory
            del self._args, self._kwargs

    @property
    def runtime(self):
        """
        Get the thread's runtime.

        If the thread has started (i.e., the instance has the `_stime` attribute), this method returns the thread's runtime.
        If the `_runtime` attribute does not exist, it calculates the runtime by subtracting the start time from the current time.
        If the thread has not started (i.e., the instance does not have the `_stime` attribute), it prints a message and returns None.

        Returns:
            float or None: The thread's runtime in seconds as a float if it has started; otherwise, None.
        """
        # Check if the thread has started by verifying the existence of the _stime attribute
        if hasattr(self, '_stime'):
            # Check if the runtime has already been calculated and stored in _runtime
            if hasattr(self, '_runtime'):
                return self._runtime
            else:
                # Calculate the runtime by subtracting the start time from the current time
                return time.time() - self._stime
        else:
            # Print a message indicating the thread has not started and return None
            print("The thread not call start function")
            return None

    @property
    def return_value(self):
        """
        Get the return value attribute.

        If the '_return' attribute of the object is set, it returns the value of this attribute;
        otherwise, it returns None. This method provides a safe way to access the '_return' attribute,
        avoiding errors that may occur from directly accessing an attribute that might not exist.

        Returns:
            The value of the '_return' attribute if it is set; otherwise, None.
        """
        if hasattr(self, '_return'):
            return self._return
        else:
            return None
