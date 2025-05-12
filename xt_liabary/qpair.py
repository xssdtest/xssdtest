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
from xt_platform import xt_interface as xt
class QueuePair(object):
    """
    Manages I/O queue pairs for a device.

    This class is responsible for creating, deleting, and managing I/O queues associated with a device.
    It provides methods to create, destroy, reinitialize queues, and configure timeouts.

    Attributes:
        device (object): Reference to the device instance.
        logger (Logger): Logger instance inherited from the device for logging purposes.
        max_ioqueue_entry (int): Maximum supported I/O queue depth.
        io_cmds_timeout (int): Timeout value for I/O commands.
        qpairs (list): List of initialized I/O queue pair objects.
    """

    def __init__(self, device):
        """
        Initialize a new QueuePair instance.

        Parameters:
            device (object): Device instance used to derive configuration values such as logger,
                             maximum queue depth, and timeout settings.
        """
        self.device = device
        self.logger = self.device.logger
        self.max_ioqueue_entry = self.device.max_ioqueue_entry
        self.io_cmds_timeout = self.device.io_cmds_timeout
        # Use the default I/O queue pair from the device as the initial queue
        self.qpairs = [self.device.device_inst.default_io_qpair]

    def get_qpairs(self):
        """
        Get all managed I/O queue pairs.

        Returns:
            list: A list containing all current I/O queue pair objects.
        """
        return self.qpairs

    def create_io_queues(self, qdepth=None):
        """
        Create a new I/O queue pair with the specified depth.

        If no depth is provided and the driver is 'uio' or 'vfio', it uses a capped value of 1024
        if the device's maximum queue depth exceeds this limit.

        Parameters:
            qdepth (int): Optional. The depth of the new I/O queue. If None, defaults to
                          `self.max_ioqueue_entry` capped at 1024.

        Returns:
            object: The newly created I/O queue pair.
        """
        if "uio" in self.device.driver or "vfio" in self.device.driver:
            if qdepth is None:
                qdepth = self.max_ioqueue_entry if self.max_ioqueue_entry < 1024 else 1024
        qpair = xt.XT_IO_QPAIR(self.device.device_inst, qdepth=qdepth, timeout=self.io_cmds_timeout, logger=self.logger)
        self.qpairs.append(qpair)
        return qpair

    def delete_io_queues(self, qpair=None):
        """
        Release resources for one or all I/O queues.

        Calls `qpair_free()` on each queue to clean up resources.

        Parameters:
            qpair (object): Optional. A specific queue pair to delete. If None, deletes all queues.
        """
        if qpair is None:
            for qp in self.qpairs:
                qp.qpair_free()
        else:
            qpair.qpair_free()

    def destroy_io_qpairs(self, qpair=None):
        """
        Destroy one or all I/O queue pairs.

        Calls `qpair_destroy()` on the queue(s) to completely destroy them.

        Parameters:
            qpair (object): Optional. A specific queue pair to destroy. If None, destroys all queues.
        """
        if qpair is None:
            for qp in self.qpairs:
                qp.qpair_destroy()
        else:
            qpair.qpair_destroy()

    def reinit_io_queues(self, qprio=0):
        """
        Re-initialize all I/O queues with the same depth but updated priority.

        Parameters:
            qprio (int): New priority level for the queues. Default is 0.
        """
        for qpair in self.qpairs:
            qdepth = qpair.get_qdepth()
            qpair.qpair_create(qdepth, qprio=qprio, timeout=self.io_cmds_timeout)

    def set_io_timeout(self, timeout=None):
        """
        Set the timeout for I/O commands across all queues.

        Parameters:
            timeout (int): Optional. The new timeout value. If not provided, defaults to
                           `self.io_cmds_timeout`.
        """
        timeout = self.io_cmds_timeout if timeout is None else timeout
        if timeout != self.io_cmds_timeout:
            for qpair in self.qpairs:
                qpair.set_timeout(timeout)
            self.io_cmds_timeout = timeout

    def get_qpair_status(self, qpair):
        """
        Retrieve the status of a specific I/O queue pair.

        Parameters:
            qpair (object): The queue pair to query.

        Returns:
            varies: Status information returned by the underlying implementation.
        """
        return qpair.get_qpair_status()

