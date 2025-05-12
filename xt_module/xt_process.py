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
import multiprocessing
import traceback
class XTProcess(multiprocessing.Process): # The XTProcess class is derived from the class threading.Thread
    def __init__(self,  target=None, name=None, args=(), kwargs=None, *, daemon=None):
        """
        Process objects represent activity that is run in a separate process
        The class is analogous to `threading.Thread`
        """
        multiprocessing.Process.__init__(self, name=name, daemon=daemon)
        if kwargs is None:
            kwargs = {}
        self._target = target
        if type(args) is tuple:
            self._args = args
        else:
            self._args = (args,)
        self._kwargs = kwargs
        self._name = "%s_process%s"%(self._target, self._name)
        self.exception = None
        self.exc_traceback = ''

    def run(self):
        """
        Overwrite the run() method to specify what the thread should execute.
        This method is responsible for executing the target function and handling any exceptions that occur.
        """
        try:
            # Record the start time
            self._stime = time.time()
            # Execute the target function and store the result
            self._return = self._target(*(self._args), **self._kwargs)
        except Exception as e:
            # Capture and record the exception information
            self.exception = e
            # Print the detailed exception information
            print(''.join(traceback.format_exception(*sys.exc_info())))
            # Exit the program in case of an exception
            exit(1)
        finally:
            # Calculate and record the runtime
            self._runtime = time.time() - self._stime

    @property
    def runtime(self):
        """
        Get the thread runtime.

        This property checks if the thread has started (i.e., the instance has an `_stime` attribute).
        If the thread has started, it returns the runtime. If the `_runtime` attribute is not set,
        it calculates the runtime by subtracting the start time from the current time.
        If the thread has not started, it prints a message and returns None.

        Returns:
            float or None: The runtime of the thread in seconds as a float if it has started, otherwise None.
        """
        # Check if the thread has started by verifying the presence of _stime attribute
        if hasattr(self, '_stime'):
            # Check if the runtime has already been calculated and stored in _runtime attribute
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
    def returnvalue(self):
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
