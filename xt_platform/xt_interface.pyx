# cython: language_level=3
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
from __future__ import print_function

import os
import sys
import logging
import logging.config
import os.path
import datetime,time
import zlib
import threading
import random
import subprocess
import psutil
sys.path.append("../")
from libc.stdlib cimport malloc, free
from array import array
from libc.stdlib cimport srand, rand
from libc.string cimport memcpy, memset, memcmp
from .xt_random import *
from cython.operator cimport dereference as deref
from libc.string cimport strncpy, strlen
import multiprocessing
import copy
cimport xt_interface as interf
cdef int XT_INIT_WRITE_BUFFER_COUNT = 512
cdef int XT_TOTAL_WRITE_BUFFER_COUNT = XT_INIT_WRITE_BUFFER_COUNT * 64
cdef int XT_WRITE_BUFFER_INDEX = 0
cdef list WRITE_BUFFER_LIST = []
cdef interf.xt_buffer ** WRITE_BUFFER_INSTANCES_LIST = <interf.xt_buffer **> interf.xt_allocate_aligned_memory(sizeof(interf.xt_buffer *) * XT_TOTAL_WRITE_BUFFER_COUNT,
                                                                                                               sizeof(void *))
cdef int XT_ADMIN_DEPTH = 0x400
cdef int XT_PCIE_NAME_SIZE = 64
cdef int XT_MAX_NSID = 511
cdef list engine_names = []

def get_init_write_buffer_list():
    return WRITE_BUFFER_LIST

def get_engine_names_list():
    """
    Retrieve a list of engine names.

    This function collects all available engine names by calling the interf.get_engine_names() function,
    and returns them as a list of strings. Each engine name appears only once in the list.

    Returns:
        list: A list containing all available engine names.
    """
    # Declare a C-type pointer variable to store the address of the engine name
    cdef char * engine_name

    # Initialize the engine name pointer, obtaining the address of the first engine name
    engine_name = interf.get_engine_names()

    # Iterate through all engine names until the returned pointer is NULL
    while engine_name != NULL:
        # Decode the C-style character array to a Python string and assign it to _engine_name
        _engine_name = "%s" % engine_name.decode("utf-8")

        # Check if the current engine name is already in the list, if not, add it
        if _engine_name not in engine_names:
            engine_names.append(_engine_name)

        # Continue to obtain the address of the next engine name
        engine_name = interf.get_engine_names()

    # Return the collected list of engine names
    return engine_names

get_engine_names_list()
def xt_project_path():
    """
    Get the root path of the xssdtest project.

    This function starts from the directory of the current file and traverses upwards
    through the directory structure until it finds a directory named 'xssdtest',
    returning the path to this directory. This is used to locate the project root
    directory, allowing for relative file access from any location within the project.

    Returns:
        str: The root path of the xssdtest project.
    """
    path_list = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)
    # Reverse the path list to traverse upwards from the current directory
    path_list.reverse()
    # Initialize the index to the length of the path list to record the position of the project root directory
    index = len(path_list)
    # Traverse the reversed path list to find a directory named 'xssdtest'
    for directory in path_list:
        if 'xt_platform' == directory:
            # Project xt_platform root directory found, stop traversal
            break
        # Project root directory not found, decrement index and continue searching upwards
        index -= 1
    # Reverse the path list again to restore the original order
    path_list.reverse()
    # Join the path list up to the index with the path separator and return as a string
    return os.path.sep.join(path_list[:index-1])

class Logger(object):
    """
    The Logger class is used to initialize and manage log files. It allows users to specify the log file's path, name, format, and output method.

    Args:
        filename (str, optional): The name of the log file. If not provided, it will be generated based on the current script name and timestamp.
        log_path (str, optional): The path where the log file will be saved. If not provided, it defaults to "/home/xt_log/".
        process_trace (bool, optional): If True, the log format will include process and thread information.
        disable_logger (bool, optional): If True, logging will be disabled, and logs will be output to /dev/null.
        pci_info (str, optional): If provided, this information will be included in the log file name.
    """
    def __init__(self, filename=None, log_path=None, process_trace=None, disable_logger=False, pci_info=None):
        # Get the current timestamp for generating the log file name
        time_stamp = self.get_time_stamp()

        # Set the log format based on whether process trace information is needed
        log_formatter = '%(asctime)s %(levelname)s %(process)s %(thread)s %(message)s' if process_trace else '%(asctime)s %(levelname)s %(message)s'

        # Check if logging is disabled
        if not disable_logger :
            # If no filename is provided, default to saving in /home/xt_log/
            if filename is None:
                log_path = "/home/xt_log/" if log_path is None else log_path
                # Generate the log file name based on whether pci_info is provided
                self.log_file_name = log_path + os.path.basename(sys.argv[0])+ "_" + time_stamp + ".log" if pci_info is None else log_path + os.path.basename(sys.argv[0])+ "_%s_"%pci_info + time_stamp + ".log"
            else:
                # If a filename is provided, use it directly
                self.log_file_name = filename
        else:
            # If logging is disabled, output logs to /dev/null
            self.log_file_name = '/dev/null'

        # Ensure the log file directory exists; if not, create it
        if not os.path.exists(os.path.dirname(self.log_file_name)):
            os.mkdir(os.path.dirname(self.log_file_name))
            # Set permissions for the log directory
            chmod_cmd = "sudo chmod 777 " + os.path.dirname(self.log_file_name)
            os.system(chmod_cmd)

        # Initialize the logger
        self.log = logging.getLogger(self.log_file_name)
        self.log.setLevel(logging.INFO)

        # Configure the log output format and handlers
        if not self.log.handlers:
            # Configure the info log output
            info_handler = logging.FileHandler(self.log_file_name)
            info_formater = logging.Formatter(log_formatter)
            info_handler.setFormatter(info_formater)
            self.log.addHandler(info_handler)

            # Configure the error log output
            error_handler = logging.StreamHandler(sys.stdout)
            error_formater = logging.Formatter(log_formatter)
            error_handler.setFormatter(error_formater)
            self.log.addHandler(error_handler)


    def get_name(self):
        return self.log_file_name

    def get_time_stamp(self):
        """
        Get the current time_stamp.

        This method returns a formatted string of the current time, used for recording or displaying time information.
        The time format is "year-month-day_hour-minute-second", which is easy to read and sort.

        Returns:
            str: A formatted time_stamp string.
        """
        return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())


    def info(self,msg, *args, **kwargs):
        """
        Log an information-level message.

        This method wraps the underlying logging object's info method, allowing for
        logging of messages at the INFO level. It accepts a message format string and
        optional arguments to populate the message with variable data.

        Parameters:
        - msg (str): The message format string to log.
        - *args: Variable positional arguments to substitute into the message format string.
        - **kwargs: Variable keyword arguments, typically used for structured logging data.
        """
        self.log.info(msg, *args, **kwargs)

    def debug(self,msg, *args, **kwargs):
        """
        Log a debug-level message.

        This method wraps the underlying logging object's debug method, intended for
        logging detailed debug information. It accepts a message format string and
        optional arguments to populate the message with variable data.

        Parameters:
        - msg (str): The message format string to log.
        - *args: Variable positional arguments to substitute into the message format string.
        - **kwargs: Variable keyword arguments, typically used for structured logging data.
        """
        self.log.debug(msg, *args, **kwargs)

    def warning(self,msg, *args, **kwargs):
        """
        Log a warning-level message.

        This method wraps the underlying logging object's warning method, used for
        logging potential issues that are not immediate errors. It accepts a message
        format string and optional arguments to populate the message with variable data.

        Parameters:
        - msg (str): The message format string to log.
        - *args: Variable positional arguments to substitute into the message format string.
        - **kwargs: Variable keyword arguments, typically used for structured logging data.
        """
        self.log.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Log an error-level message.

        This method wraps the underlying logging object's error method, intended for
        logging errors that occur during execution. It accepts a message format string
        and optional arguments to populate the message with variable data.

        Parameters:
        - msg (str): The message format string to log.
        - *args: Variable positional arguments to substitute into the message format string.
        - **kwargs: Variable keyword arguments, typically used for structured logging data.
        """
        self.log.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        Log a critical-level message.

        This method wraps the underlying logging object's critical method, used for
        logging critical errors that may cause the program to exit or functionality to
        degrade significantly. It accepts a message format string and optional arguments
        to populate the message with variable data.

        Parameters:
        - msg (str): The message format string to log.
        - *args: Variable positional arguments to substitute into the message format string.
        - **kwargs: Variable keyword arguments, typically used for structured logging data.
        """
        self.log.critical(msg, *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        """
        Log a fatal-level message.

        This method wraps the underlying logging object's fatal method, used for
        logging errors that are severe enough to cause the program to terminate.
        It accepts a message format string and optional arguments to populate the
        message with variable data.

        Parameters:
        - msg (str): The message format string to log.
        - *args: Variable positional arguments to substitute into the message format string.
        - **kwargs: Variable keyword arguments, typically used for structured logging data.
        """
        self.log.fatal(msg, *args, **kwargs)

    def set_logger_level(self, level):
        """
        Set the logging level for the logger.

        This method accepts a parameter representing the log level, which can be either a string or an integer.
        If it's a string, it will be converted to the corresponding log level value;
        if it's an integer, it will be directly set as the log level.

        Parameters:
        - level: The log level, which can be a string ('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', etc.) or an integer value.

        Returns:
        None
        """
        # Dictionary mapping log level strings to their corresponding numeric values
        level_dic = {'CRITICAL': 50, 'FATAL': 50, 'ERROR': 40, 'WARNING': 30, 'WARN': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}

        # Check the type of the input log level
        if type(level) is str:
            # Convert the string to uppercase and get the corresponding log level value
            level = level.upper()
            level = level_dic[level]

        # Set the logger's level
        self.log.setLevel(level)

    def set_xt_logger_level(self, int level):
        """
        Sets the xt logger's log level.

        This function sets the log level by accepting an integer parameter `level`.
        The valid range for `level` is from -1 to 4, corresponding to different log levels.
        If the value of `level` is not within this range, it defaults to 4 (XT_LOG_DEBUG).

        Parameters:
        - level (int): Log level, ranging from -1 to 4.

        Returns:
        None
        """
        # Define a dictionary mapping integer levels to log level strings
        level_dic = {-1: "XT_LOG_DISABLED", 0: "XT_LOG_ERROR", 1: "XT_LOG_WARN", 2: "XT_LOG_NOTICE", 3: "XT_LOG_INFO", 4: "XT_LOG_DEBUG"}

        # Define the default log level
        DEFAULT_LOG_LEVEL = 4

        level = level if -1 <= level <= 4 else DEFAULT_LOG_LEVEL

        # Log the current log level being set using a safer format method
        self.info("set xssdtest platform log level: {}".format(level_dic[level]))

        # Call the underlying interface to set the log level
        interf.xt_log_set_print_level(level)



cdef class XT_BUFFER(object):
    cdef unsigned char *m_raw
    cdef interf.xt_buffer _buffer_instance
    cdef unsigned int m_length
    cdef unsigned int buf_type
    cdef object logger
    cdef object pattern
    cdef list alloc_buf_list
    cdef XT_DEVICES device
    def __cinit__(self, unsigned int buf_length, unsigned int buf_align=512, buf_type=0, alloc_type=None, pi_type=0,  logger=None, unsigned int mem_init=0, XT_DEVICES device=None):
        """
        :param buf:
        :param logger:
        :param bufalignment:
        :param driverType:
        :param buf_type: 0 is admin-buffer; 1 is write-buffer with metadata or without metadata; 2 is read-buffer
        :return:
        """
        self.logger = logger
        self.m_length = buf_length
        buf_length = buf_length + 4096 if pi_type else buf_length
        if buf_type:
            if alloc_type is None:
                alloc_type = 1 if device is None else 2 if 'spdk_nvme' in device.driver.engine_opt_name else 1
            else:
                alloc_type = alloc_type
        else:
            alloc_type = 1
        interf.xt_buffer_init(&self._buffer_instance, buf_length, buf_align, alloc_type, mem_init)
        self.m_raw = < unsigned char *>interf.get_xt_buffer(&self._buffer_instance)
        self.buf_type = buf_type
        self.pattern = None
        self.alloc_buf_list = []
        if buf_type == 1:
            global XT_WRITE_BUFFER_INDEX, WRITE_BUFFER_INSTANCES_LIST, WRITE_BUFFER_LIST
            WRITE_BUFFER_LIST.append(self)
            assert len(WRITE_BUFFER_LIST) <= XT_TOTAL_WRITE_BUFFER_COUNT, self.logger.error("WRITE_BUFFER_LIST Out of memory ")
            WRITE_BUFFER_INSTANCES_LIST[XT_WRITE_BUFFER_INDEX] = &self._buffer_instance
            self._buffer_instance.buf_index = XT_WRITE_BUFFER_INDEX << 4
            XT_WRITE_BUFFER_INDEX += 1

    cpdef get_pattern(self, unsigned long length=0):
        """
        :param length: 
        :return: 
        """
        cdef unsigned int pattern = 0xffffffff
        cdef unsigned char *a_pattern = <unsigned char *> &pattern
        cdef unsigned long  off = 0
        length = self.m_length if 0 == length else length
        while off < length:
            a_pattern[0] = a_pattern[0] & self.m_raw[off]
            a_pattern[1] = a_pattern[1] & self.m_raw[off + 1]
            a_pattern[2] = a_pattern[2] & self.m_raw[off + 2]
            a_pattern[3] = a_pattern[3] & self.m_raw[off + 3]
            off = off + 4
        return pattern

    def dump_buf(self, unsigned int offset=0, unsigned int length=0, line_length=0x20):
        """
        first 16 colum is address, print lineLength byte index
        :param offset:
        :param length:
        :param lineLength:
        :return:
        """
        cdef int i = 0
        cdef unsigned char *tmpaddr = self.m_raw + offset
        assert (offset + length) <= self.m_length,  self.logger.error("length out of the buffer range")
        length = length if 0 != length else self.m_length - offset
        dump_str = " " * 11
        for i in range(line_length):
            dump_str = dump_str + " %2x" % i
        self.logger.info(dump_str)
        self.logger.info(" " * 12 + "-" * (line_length * 3 - 1))
        dump_str, i = "0x%08x: "%0, 0
        while length > 0:
            if 0 == i % line_length and i: # print address
                self.logger.info(dump_str)
                # begin print new line
                dump_str, i = "0x%08x: " % (tmpaddr - self.m_raw), 0
            dump_str = dump_str + "%02x " % deref(tmpaddr)
            tmpaddr, length, i = tmpaddr + 1, length - 1, i + 1
        else:
            self.logger.info(dump_str)

    def get_raw_buf(self, offset=0, length=0, step=1):
        """
        :param offset:
        :param length:
        :param step:
        :return:
        """
        length = self.m_length if 0 == length else length
        length = self.m_length - offset if length + offset > self.m_length else length
        return self.m_raw[offset:offset + length:step]

    cpdef set_content(self, offset, unsigned char *value, len):
        cdef int i
        if offset + len > self.m_length:
            raise RuntimeError("set_content: offset is out of buffer range")
        else:
            for i in range(len):
                self.m_raw[offset + i] = value[i]

    cdef get_content(self, offset, unsigned char *value, len):
        cdef int i
        if offset + len > self.m_length:
            raise RuntimeError("get_content: offset is out of buffer range")
        else:
            for i in range(len):
                value[i] = self.m_raw[offset + i]

    cpdef set_uint8(self, unsigned int offset, unsigned char value, unsigned long long raw_buf=0):
        if raw_buf == 0:
            interf.xt_set_uint8(&self._buffer_instance, offset, value, 1)
        else:
            interf.xt_set_uint8(<void *>raw_buf, offset, value, 0)

    cpdef get_uint8(self, unsigned int offset, unsigned long long raw_buf=0):
        if raw_buf == 0:
            return interf.xt_get_uint8(&self._buffer_instance, offset, 1)
        else:
            return interf.xt_get_uint8(<void *>raw_buf, offset, 0)

    cpdef set_uint16(self, unsigned int offset, unsigned short value, unsigned long long raw_buf=0):
        if raw_buf == 0:
            interf.xt_set_uint16(&self._buffer_instance, offset, value, 1)
        else:
            interf.xt_set_uint16(<void *> raw_buf, offset, value, 0)

    cpdef get_uint16(self, unsigned int offset, unsigned long long raw_buf=0):
        if raw_buf == 0:
            return interf.xt_get_uint16(&self._buffer_instance, offset, 1)
        else:
            return interf.xt_get_uint16(<void *>raw_buf, offset, 0)

    cpdef set_uint32(self, unsigned int offset, unsigned int value, unsigned long long raw_buf=0):
        if raw_buf == 0:
            interf.xt_set_uint32(&self._buffer_instance, offset, value, 1)
        else:
            interf.xt_set_uint32(<void *>raw_buf, offset, value, 0)

    cpdef get_uint32(self, unsigned int offset, unsigned long long raw_buf=0):
        if raw_buf == 0:
            return interf.xt_get_uint32(&self._buffer_instance, offset, 1)
        else:
            return interf.xt_get_uint32(<void *>raw_buf, offset, 0)

    cpdef set_uint64(self, unsigned int offset, unsigned long long value, unsigned long long raw_buf=0):
        if raw_buf == 0:
            interf.xt_set_uint64(&self._buffer_instance, offset, value, 1)
        else:
            interf.xt_set_uint64(<void *>raw_buf, offset, value, 0)

    cpdef get_uint64(self, unsigned int offset, unsigned long long raw_buf=0):
        if raw_buf == 0:
            return interf.xt_get_uint64(&self._buffer_instance, offset, 1)
        else:
            return interf.xt_get_uint64(<void *>raw_buf, offset, 0)

    cpdef fill_stream(self, string, offset=0, length=0):
        if type(string) is str:
            bytes_str = string.encode()
        elif type(string) is bytes:
            bytes_str = string
        else:
            raise TypeError("input string type is not str or bytes")
        cdef unsigned int listLength = len(bytes_str)
        if length == 0:
            length = listLength
            memcpy(&self.m_raw[offset], <unsigned char *> bytes_str, length)
        else:
            if length > listLength:
                if length + offset > self.m_length:
                    raise ValueError("input length+offset:%d greater than bug length:%d", (length + offset), self.m_length)
                for index in range(length):
                    self.m_raw[offset + index] = bytes_str[index % listLength]
            else:
                memcpy(&self.m_raw[offset], <unsigned char *> bytes_str, length)

    # Fill Buffer to some specified value
    cpdef fill_byte(self, unsigned char value, unsigned int offset=0, unsigned int length=0):
        assert length <= self.m_length, self.logger.error("get a invalid length %s buffer max length %s" % (length, self.m_length))
        length = self.m_length if 0 == length else length
        for _offset in range(offset, length, sizeof(value)):
            self.set_uint8(_offset, value)

    cpdef fill_word(self, unsigned short value, unsigned int offset=0, unsigned int length=0):
        assert length <= self.m_length, self.logger.error("get a invalid length %s buffer max length %s"%(length, self.m_length))
        length = self.m_length if 0 == length else length
        for _offset in range(offset, length, sizeof(value)):
            self.set_uint16(_offset, value)

    cpdef fill_dword(self, unsigned int value, unsigned int offset=0, unsigned int length=0):
        assert length <= self.m_length, self.logger.error("get a invalid length %s buffer max length %s" % (length, self.m_length))
        length = self.m_length if 0 == length else length
        for _offset in range(offset, length, sizeof(value)):
            self.set_uint32(_offset, value)

    cpdef fill_qword(self, unsigned long long value, unsigned int offset=0, unsigned int length=0):
        assert length <= self.m_length, self.logger.error("get a invalid length %s buffer max length %s" % (length, self.m_length))
        length = self.m_length if 0 == length else length
        for _offset in range(offset, length, sizeof(value)):
            self.set_uint64(_offset, value)

    # fill while buffer
    cpdef fill_pattern(self, unsigned char *pattern, int pattern_width, unsigned int offset=0, unsigned int length=0):
        cdef unsigned int i
        self.pattern = pattern
        length = self.m_length if 0 == length else length
        for i in range(length):
            self.m_raw[i + offset] = pattern[i % pattern_width]

    cpdef fill_random(self, int offset=0):
        srand(rand())
        for i in range(offset, self.m_length):
            self.m_raw[i] = rand() % 256

    def size(self):
        return self.m_length

    cpdef unsigned long long get_buf_addr(self):
        return <unsigned long long> self.m_raw


    cpdef encode(self, offset=0, length=0):
        if 0 == length:
            length = self.m_length
        elif length + offset > self.m_length:
            length = self.m_length - offset
        # self.dump_buf()
        # print("offset %s length %s"%(offset, length))
        # print(self.m_raw)
        return self.m_raw[offset:offset + length]

    cpdef decode(self, data, offset=0, length=0):
        if 0 == length:
            length = self.m_length
        elif length + offset > self.m_length:
            length = self.m_length - offset
        for i in range(offset, offset + length):
            self.m_raw[i] = data[i - offset]

    cpdef write_buffer_init(self, pattern_file, unsigned int crc_type=8):
        if os.path.exists(pattern_file):
            write_buf_idx = int(pattern_file.split('-')[-1])
            if (self._buffer_instance.buf_index >> 4) != write_buf_idx:
                self.logger.error("expect pattern index is %s, actual is %s"%(self._buffer_instance.buf_index >> 4, write_buf_idx))
            if os.path.getsize(pattern_file) == 4:
                write_buf_idx = write_buf_idx << 4 | 0xF
            else:
                assert os.path.getsize(pattern_file) == 4096, self.logger.error("%s expect pattern size is 4096, actual is %s" % (pattern_file,
                                                                                 os.path.getsize(pattern_file)))
                write_buf_idx = write_buf_idx << 4
            self._buffer_instance.buf_index = write_buf_idx
            self.pattern = os.path.split(pattern_file)[-1]
        interf.xt_buffer_init_crc(&self._buffer_instance, crc_type=crc_type)
        self._buffer_instance.sector_size = 512
        self._buffer_instance.pi_type = 0

    cpdef fill_disorder(self, disorder_para, offset=0, length=0, byte_flag=False):
        cdef int count = 0, index = 0, list_length = 0
        cdef unsigned char byte
        cdef unsigned int value
        if length + offset > self.m_length:
            raise ValueError("input length+offset:%d greater than bug length:%d", (length + offset), self.m_length)
        if type(disorder_para) is list:
            self.pattern = disorder_para[0:8]
            list_length = len(disorder_para)
            length = self.m_length - offset if length == 0 else length
            if not byte_flag:
                while count < length - 1:
                    value = disorder_para[index % list_length]
                    self.fill_pattern(<unsigned char *> &value, sizeof(value), count, sizeof(value))
                    count, index = count + sizeof(value), index + 1
            else:
                while index < length - 1:
                    self.m_raw[index + offset] = disorder_para[index % list_length]
                    index = index + 1
        elif type(disorder_para) is str:
            self.pattern = disorder_para.split(os.path.sep)[-1]
            if os.path.exists(disorder_para):
                with open(disorder_para, "rb") as f:
                    file_content = f.read()
                    count = len(file_content)
                    length = self.m_length if length == 0 else length
                    for index in range(length):
                        self.m_raw[index + offset] = file_content[index % count]
                self.write_buffer_init(disorder_para)
            else:
                self.pattern = disorder_para[0:8]
                length = self.m_length - offset if length == 0 else length
                self.fill_stream(disorder_para, offset, length)
        elif type(disorder_para) is int:
            self.pattern = "0x%08x" % disorder_para
            value = disorder_para
            length = self.m_length - offset if length == 0 else length
            self.fill_pattern(<unsigned char *> &value, sizeof(value), offset, length)
        else:
            raise ValueError("input parameter error")

    cpdef calculate_crc64(self, offset=0, length=None):
        length = self.m_length if length is None else length
        return interf.xt_buffer_crc64(&self._buffer_instance, offset, length)

    cpdef calculate_crc32(self, offset=0, length=None):
        length = self.m_length if length is None else length
        return interf.xt_buffer_crc32(&self._buffer_instance, offset, length)

    cpdef calculate_crc16(self, offset=0, length=None):
        length = self.m_length if length is None else length
        return interf.xt_buffer_crc16(&self._buffer_instance, offset, length)

    cpdef calculate_crc8(self, offset=0, length=None):
        length = self.m_length if length is None else length
        return interf.xt_buffer_crc8(&self._buffer_instance, offset, length)

    def __str__(self, ):
        if type(self.pattern) is str:
            return self.pattern
        else:
            self.pattern = hex(self.get_uint32(0))
            return self.pattern

    def __repr__(self, ):
        if type(self.pattern) is str:
            return self.pattern
        else:
            self.pattern = hex(self.get_uint32(0))
            return self.pattern

    def __len__(self):
        return self.m_length

    def __getitem__(self, index):
        if isinstance(index, slice):
            return bytes([self[i] for i in range(*index.indices(len(self)))])
        elif isinstance(index, int):
            assert index < self.m_length
            return self.m_raw[index]
        else:
            raise TypeError()

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            start = 0 if index.start is None else index.start
            step = 1 if index.step is None else index.step
            assert len(value) != len(range(start, index.stop, step))
            for index, offset in enumerate(range(start, index.stop, step)):
                self[offset] = value[index]
        elif isinstance(index, int):
            assert index < self.m_length
            self.m_raw[index] = value
        else:
            raise TypeError()

    def mem_reset(self, value=0, length=None):
        length = self.m_length if length is None else length
        memset(self.m_raw, value, length)

    def __dealloc__(self):
        interf.xt_buffer_free(&self._buffer_instance)
        self.m_raw = NULL
        for item in self.alloc_buf_list:
            interf.xt_buffer_alloc_free(item[0], <void *>(item[1]))

    cpdef meta_data_change(self, unsigned int meta_sector_size, unsigned int pi_type, unsigned int sector_size):
        if self._buffer_instance.meta_sector_size == meta_sector_size and self._buffer_instance.pi_type == pi_type and \
            self._buffer_instance.sector_size == sector_size:
            return
        if pi_type == 2:
            interf.xt_buffer_dix_init(&self._buffer_instance, meta_sector_size)
        elif pi_type == 1:
            interf.xt_buffer_dif_init(&self._buffer_instance, meta_sector_size, sector_size)

    cpdef xt_alloc_memory(self, unsigned int alloc_type, unsigned int buf_length):
        cdef void* raw_buf = NULL
        raw_buf = interf.xt_buffer_alloc_memory(alloc_type, buf_length)
        if raw_buf != NULL:
            self.alloc_buf_list.append([alloc_type, <unsigned long long>raw_buf])
        return <unsigned long long>raw_buf

cdef class XT_IO_QPAIR(object):
    cdef:
        XT_DEVICES device
        XT_BUFFER default_buf
        interf.xt_io_qpair *io_qpair
        interf.xt_admin_qpair *_admin_qpair
        unsigned long long sys_tick_us
        unsigned int init_io_units_count
        unsigned int active_flag
        object logger

    def __cinit__(self, device, qdepth,  qprio=0, timeout=1000000, logger=None, init_io_qpair=True):
        self.device = device
        self.logger = logger
        self._admin_qpair = self.device._admin_qpair
        self.sys_tick_us = self.device.sys_tick_us # 1us = sys_tick
        self.io_qpair = <interf.xt_io_qpair *>interf.xt_allocate_aligned_memory(sizeof(interf.xt_io_qpair), sizeof(void *))
        memset(self.io_qpair, 0, sizeof(interf.xt_io_qpair))
        self.io_qpair.qpair_iodepth = qdepth
        if init_io_qpair:
            self.io_qpair.io_units = <interf.cmds_u *> interf.xt_allocate_aligned_memory(qdepth * sizeof(interf.cmds_u), sizeof(interf.cmds_u))
            memset(self.io_qpair.io_units, 0, qdepth * sizeof(interf.cmds_u))
            self.io_qpair.completed_cmds_u_ring = <interf.cmds_u_ring *> interf.xt_allocate_aligned_memory(sizeof(interf.cmds_u_ring), sizeof(void *))
            if not interf.cmds_u_rinit(self.io_qpair.completed_cmds_u_ring, qdepth):
                assert False, self.logger.error("init command units failed")
            for index in range(qdepth):
                interf.cmds_u_rpush(self.io_qpair.completed_cmds_u_ring, &self.io_qpair.io_units[index])
            self.default_buf = XT_BUFFER(buf_length=1024 * 1024, buf_align=4096, logger=self.logger, mem_init=1, buf_type=2, alloc_type=2)
            self.io_qpair.completed_check_index = qdepth
        else:
            self.io_qpair.completed_check_index = 0
        if interf.xt_qpair_create(self._admin_qpair, self.io_qpair, qprio, qdepth) == NULL:
            assert False, self.logger.error("create io qpair failed")
        self.init_io_units_count = qdepth
        self.active_flag = 1
        self.io_qpair.submit_count = 0
        self.io_qpair.qpair_completions = 0
        self.io_qpair.qpair_iodepth = qdepth
        self.io_qpair.write_buf_addr_list = WRITE_BUFFER_INSTANCES_LIST
        interf.xt_set_io_timespec_timeout(self.io_qpair, timeout)
        self.io_qpair.timeout = timeout * self.sys_tick_us

    def get_qdepth(self):
        return self.io_qpair.qpair_iodepth

    def inactive_io_qpair(self):
        self.active_flag = 0

    def get_qpair_id(self):
        return interf.xt_get_io_qpair_id(self.io_qpair)

    def get_qpair_status(self):
        return self.active_flag

    def reset_io_qpair(self):
        if self.io_qpair.completed_cmds_u_ring != NULL:
            interf.cmds_u_rreset(self.io_qpair.completed_cmds_u_ring)
            for index in range(self.io_qpair.qpair_iodepth):
                interf.cmds_u_rpush(self.io_qpair.completed_cmds_u_ring, &self.io_qpair.io_units[index])
            self.io_qpair.completed_check_index = self.io_qpair.qpair_iodepth
            self.io_qpair.qpair_completions = 0
            self.io_qpair.submit_count = 0
        if self.io_qpair.submit_cmds_u_ring != NULL:
            interf.cmds_u_rreset(self.io_qpair.submit_cmds_u_ring)

    def qpair_create(self, qdepth, qprio=0, timeout=1000000, init_io_qpair=True, report_error=True):
        assert self.active_flag == 0, self.logger.error("io qpair is active please check")
        if init_io_qpair:
            if self.io_qpair.completed_cmds_u_ring:
                interf.cmds_u_rexit(self.io_qpair.completed_cmds_u_ring)
            self.io_qpair.completed_cmds_u_ring = <interf.cmds_u_ring *> interf.xt_allocate_aligned_memory(sizeof(interf.cmds_u_ring), sizeof(void *))
            if not interf.cmds_u_rinit(self.io_qpair.completed_cmds_u_ring, qdepth):
                assert False, self.logger.error("init command units failed")
            if qdepth > self.init_io_units_count or self.io_qpair.io_units == NULL:
                if self.io_qpair.io_units != NULL:
                    interf.xt_free_aligned_memory(self.io_qpair.io_units)
                self.io_qpair.io_units = <interf.cmds_u *> interf.xt_allocate_aligned_memory(sizeof(interf.cmds_u) * qdepth, sizeof(interf.cmds_u))
                memset(self.io_qpair.io_units, 0, sizeof(interf.cmds_u) * qdepth)
                self.init_io_units_count = qdepth
            self.io_qpair.qpair_iodepth = qdepth
            for index in range(qdepth):
                interf.cmds_u_rpush(self.io_qpair.completed_cmds_u_ring, &self.io_qpair.io_units[index])
            self.io_qpair.completed_check_index = self.io_qpair.qpair_iodepth
            if self.io_qpair.submit_cmds_u_ring != NULL:
                interf.cmds_u_rreset(self.io_qpair.submit_cmds_u_ring)
        else:
            self.io_qpair.completed_check_index = 0
        if interf.xt_qpair_create(self._admin_qpair, self.io_qpair, qprio, qdepth) == NULL:
            if report_error:
                assert False, self.logger.error("recreate io qpair failed")
            return False
        self.io_qpair.submit_count = 0
        self.io_qpair.qpair_completions = 0
        interf.xt_set_io_timespec_timeout(self.io_qpair, timeout)
        self.io_qpair.timeout = timeout * self.sys_tick_us
        self.active_flag = 1
        return True

    def qpair_free(self, report_error=True):
        assert self.active_flag == 1, self.logger.error("io qpair is not active")
        if interf.xt_qpair_free(self._admin_qpair, self.io_qpair):
            if report_error:
                assert False, self.logger.error("free io qpair failed")
            return False
        if self.io_qpair.completed_cmds_u_ring:
            interf.cmds_u_rexit(self.io_qpair.completed_cmds_u_ring)
            self.io_qpair.completed_cmds_u_ring = NULL
        self.io_qpair.completed_check_index = 0
        self.io_qpair.qpair_completions = 0
        self.io_qpair.submit_count = 0
        self.active_flag = 0
        return True

    def qpair_destroy(self):
        assert self.active_flag == 1, self.logger.error("io qpair is not active")
        interf.xt_qpair_destroy(self._admin_qpair, self.io_qpair)
        if self.io_qpair.completed_cmds_u_ring:
            interf.cmds_u_rexit(self.io_qpair.completed_cmds_u_ring)
            self.io_qpair.completed_cmds_u_ring = NULL
        self.io_qpair.completed_check_index = 0
        self.io_qpair.qpair_completions = 0
        self.io_qpair.submit_count = 0
        self.active_flag = 0

    def __dealloc__(self):
        if self.io_qpair.io_units != NULL:
            interf.xt_free_aligned_memory(self.io_qpair.io_units)
        if self.io_qpair.completed_cmds_u_ring != NULL:
            interf.cmds_u_rexit(self.io_qpair.completed_cmds_u_ring)
        interf.free_sub_lcg(self.io_qpair.io_lcg)
        interf.free_sub_lcg(self.io_qpair.write_lcg)
        interf.free_sub_lcg(self.io_qpair.read_lcg)
        interf.xt_free_aligned_memory(self.io_qpair)

    def set_io_timeout(self, timeout=1000000):
        interf.xt_io_qpair_timeout(self.io_qpair, timeout * self.sys_tick_us)
        interf.xt_set_io_timespec_timeout(self.io_qpair, timeout)

cdef class XT_DRIVER(object):
    cdef:
        interf.xt_admin_qpair *_admin_qpair
        interf.cmds_u * admin_units
        interf.xt_engine_ops * engine_ops
        unsigned long long sys_tick_us
        unsigned long long timeout
        unsigned int init_char_device_flag
        unsigned int io_sync_flag
        unsigned int admin_sync_flag
        char traddr[64]
        void * bar_info
        object logger
        object devices_driver
        object pcie_setup_workspace
        object pcie_addr
        dict devices_dict
        list nvme_engines
        unsigned int nvme_engine_flag
        unsigned int spdk_engine_flag
        list tbd_engines
        list sata_engines
        unsigned int sata_engine_flag
        list simulator_engines
        unsigned int simulator_engine_flag
        object engine_opt_name

    def __cinit__(self, pcie_addr, engine_opt_name, logger=None, mem_size=256, pci_whitelist=None):
        cdef char * pcie_list
        cdef int index = 0
        cdef int pcie_count = len(pci_whitelist) if type(pci_whitelist) is list else 0
        self.engine_ops = NULL
        self.load_tdb_engines()
        self.load_nvme_engines()
        self.load_sata_engines()
        self.load_simulator_engines()
        self.engine_opt_name = engine_opt_name.lower()
        engine_opt_name = self.engine_opt_name
        self.logger = logger
        self._admin_qpair = <interf.xt_admin_qpair *> interf.xt_allocate_aligned_memory(sizeof(interf.xt_admin_qpair), sizeof(void *))
        memset(<void *> (self._admin_qpair), 0, sizeof(interf.xt_admin_qpair))
        self._admin_qpair.spdk_mem_size = mem_size
        self.init_char_device_flag = 0
        self.devices_dict = {}
        self.pcie_addr = pcie_addr
        if pcie_addr is not None:
            strncpy(self._admin_qpair.traddr, pcie_addr.encode('utf-8'), strlen(pcie_addr.encode('utf-8')) + 1)
        self._admin_qpair.admin_units = <interf.cmds_u *> interf.xt_allocate_aligned_memory(sizeof(interf.cmds_u) * XT_ADMIN_DEPTH, sizeof(interf.cmds_u))
        memset(self._admin_qpair.admin_units, 0, sizeof(interf.cmds_u) * XT_ADMIN_DEPTH)
        self._admin_qpair.qpair_iodepth = XT_ADMIN_DEPTH
        self._admin_qpair.completed_cmds_u_ring = <interf.cmds_u_ring *> interf.xt_allocate_aligned_memory(sizeof(interf.cmds_u_ring), sizeof(void *))
        if not interf.cmds_u_rinit(self._admin_qpair.completed_cmds_u_ring, XT_ADMIN_DEPTH):
            assert False, self.logger.error("init command units failed")
        for index in range(XT_ADMIN_DEPTH):
            interf.cmds_u_rpush(self._admin_qpair.completed_cmds_u_ring, &self._admin_qpair.admin_units[index])
        if pci_whitelist is not None:
            assert type(pci_whitelist) is list
            pcie_list = <char *> interf.xt_allocate_aligned_memory(XT_PCIE_NAME_SIZE * pcie_count, XT_PCIE_NAME_SIZE)
            memset(pcie_list, 0, XT_PCIE_NAME_SIZE * pcie_count)
            index = 0
            for pci_bdf in pci_whitelist:
                strncpy(&pcie_list[XT_PCIE_NAME_SIZE * index], pci_bdf.encode('utf-8'), strlen(pcie_addr.encode('utf-8')) + 1)
                index += 1
            interf.xt_admin_init(self._admin_qpair, pcie_list, pcie_count)
            interf.xt_free_aligned_memory(pcie_list)
        else:
            interf.xt_admin_init(self._admin_qpair, NULL, 0)
        self.pcie_setup_workspace = os.path.join(xt_project_path(), 'setup.sh')
        if engine_opt_name in self.nvme_engines or engine_opt_name in self.sata_engines:
            if os.path.exists("/sys/bus/pci/devices/%s" % pcie_addr):
                driver_link_path = "/sys/bus/pci/devices/%s/driver"%pcie_addr
                driver_path = os.readlink(driver_link_path)
                self.devices_driver = driver_path.split(os.path.sep)[-1]
            else:
                raise Exception("can't find pciPort %s" % pcie_addr)
        self.load_engines(engine_opt_name)
        if interf.xt_env_init(self._admin_qpair) != 0:
            raise Exception("init environment failed")
        self.sys_tick_us = <unsigned long long>(self._admin_qpair.sys_tick_hz / 1000000)
        self.bar_info = NULL

    cdef load_nvme_engines(self):
        if self.nvme_engines is None:
            self.nvme_engines = []
        if self.tbd_engines is None:
            self.load_tdb_engines()
        for item in engine_names:
            if 'nvme' in item and "simulator" not in item and item not in self.nvme_engines and item not in self.tbd_engines:
                self.nvme_engines.append(item)
    cdef load_tdb_engines(self):
        if self.tbd_engines is None:
            self.tbd_engines = []
        for item in engine_names:
            if 'tdb' in item and item not in self.tbd_engines:
                self.tbd_engines.append(item)

    cdef load_sata_engines(self):
        if self.sata_engines is None:
            self.sata_engines = []
        if self.tbd_engines is None:
            self.load_tdb_engines()
        for item in engine_names:
            if 'sata' in item and item not in self.sata_engines and item not in self.tbd_engines:
                self.sata_engines.append(item)

    cdef load_simulator_engines(self):
        if self.simulator_engines is None:
            self.simulator_engines = []
        if self.tbd_engines is None:
            self.load_tdb_engines()
        for item in engine_names:
            if 'simulator' in item and item not in self.simulator_engines and item not in self.tbd_engines:
                self.simulator_engines.append(item)
    cdef load_device_driver(self,):
        if self.engine_opt_name in self.nvme_engines or self.engine_opt_name in self.sata_engines:
            if os.path.exists("/sys/bus/pci/devices/%s" % self.pcie_addr):
                driver_link_path = "/sys/bus/pci/devices/%s/driver"%self.pcie_addr
                driver_path = os.readlink(driver_link_path)
                self.devices_driver = driver_path.split(os.path.sep)[-1]

    cdef load_engines_check(self, engine_opt_name):
        engine_opt_name = engine_opt_name.lower()
        if engine_opt_name in engine_names:
            if engine_opt_name in self.tbd_engines:
                assert False, self.logger.error("%s engine to be determined" % (engine_opt_name))
        else:
            assert False, self.logger.error("get a invalid engine %s, support engines list is : %s"%(engine_opt_name, engine_names))

    cdef load_engines(self, engine_opt_name):
        """
        'io_uring_nvme_tbd', 'libaio_nvme', 'null', 'ioctrl_nvme', 'sata_tbd', 'sde_xx_tbd', 'simulator_nvme', 'spdk_nvme', 'sync_nvme'
        Args:
            engine_opt_name: 
        Returns:
        """
        cdef unsigned int reload_engine_check = 0
        self.load_engines_check(engine_opt_name)
        engine_opt_name = engine_opt_name.lower()
        if self.engine_opt_name == engine_opt_name:
            if self.engine_ops != NULL:
                self.logger.info("current engine is %s load engine is %s"%(self.engine_opt_name, engine_opt_name))
                return
            else:
                reload_engine_check = 1
        else:
            if self.engine_opt_name is None:
                reload_engine_check = 1
            else:
                reload_engine_check = interf.reload_engine_check(self.engine_opt_name.encode('utf-8'), engine_opt_name.encode('utf-8'))
        assert reload_engine_check == 1, self.logger.error("current engine is %s load engine is %s reload engine check %s "%(self.engine_opt_name, engine_opt_name, reload_engine_check))
        if engine_opt_name in self.nvme_engines:
            self.__set_engine_flag(nvme_engine_flag=1)
            self.load_device_driver()
            if 'spdk_nvme' in engine_opt_name:
                self.__set_engine_flag(spdk_engine_flag=1)
                if self.devices_driver != 'uio' and self.devices_driver != 'vfio-pci':
                    self.bind_driver('uio')
            else:
                if 'nvme' not in self.devices_driver :
                    self.bind_driver('nvme')
                devices_list, char_device = [], ""
                for root, dirs, files in os.walk("/sys/block"):
                    for filename in dirs:
                        realpath = os.path.realpath(os.path.join(root, filename))
                        if 'nvme' in filename[:5] and self.pcie_addr in realpath:
                            char_device = "/dev/%s" % realpath.split(os.path.sep)[-2]
                            nsid = int(os.popen('cat %s/nsid' % realpath).read())
                            devices_list.append(['/dev/%s' % filename, nsid])
                            self.devices_dict[nsid] = '/dev/%s' % filename
                if devices_list and char_device:
                    if self.init_char_device_flag:
                        interf.xt_char_device_update_info(self._admin_qpair, char_device.encode('utf-8'), strlen(char_device.encode('utf-8')) + 1)
                    else:
                        interf.xt_char_device_info_init(self._admin_qpair, char_device.encode('utf-8'), strlen(char_device.encode('utf-8')) + 1, XT_MAX_NSID)
                        self.init_char_device_flag = 1
            self.load_device_driver()
        elif engine_opt_name in self.sata_engines:
            self.load_device_driver()
            self.__set_engine_flag(sata_engine_flag=1)
        elif engine_opt_name in self.simulator_engines:
            self.devices_driver = 'simulator'
            self.__set_engine_flag(simulator_engine_flag=1)
        else:
            self.devices_driver = 'null'
        self.engine_ops = interf.xt_load_engine(engine_opt_name.encode('utf-8'), self._admin_qpair)
        if self.engine_ops == NULL:
            assert False, self.logger.error("Load engine %s failed"%(engine_opt_name))
        self.logger.info("Load %s engines done 0x%x" % (engine_opt_name, <unsigned long long>self.engine_ops))
        self.io_sync_flag = interf.xt_get_engine_io_sync_flag(self._admin_qpair)
        self.admin_sync_flag = interf.xt_get_engine_admin_sync_flag(self._admin_qpair)
        self.engine_opt_name = engine_opt_name

    def __set_engine_flag(self, simulator_engine_flag=0, sata_engine_flag=0, nvme_engine_flag=0, spdk_engine_flag=0):
        self.simulator_engine_flag = simulator_engine_flag
        self.sata_engine_flag = sata_engine_flag
        self.nvme_engine_flag = nvme_engine_flag
        self.spdk_engine_flag = spdk_engine_flag

    def __getitem__(self, index):
        """access pcie config space by bytes."""
        if self.engine_opt_name in self.nvme_engines:
            if isinstance(index, slice):
                return [self[ii] for ii in range(index.stop)[index]]
            elif isinstance(index, int):
                return interf.xt_pcie_device_config_read8(self._admin_qpair, index)
        else:
            self.logger.error("%s don't support pcie config and return -1"%self.engine_opt_name)
            return -1

    def __setitem__(self, index, value):
        """set pcie config space by bytes."""
        if self.engine_opt_name in self.nvme_engines:
            if isinstance(index, int):
                interf.xt_pcie_device_config_write8(self._admin_qpair, index, value)
        else:
            self.logger.error("%s don't support pcie config set"%self.engine_opt_name)


    def dump_pcie_header(self, length=256, line_length=0x20):
        """
        :param lineLength:
        :return:
        """
        cdef int i = 0
        if self.engine_opt_name in self.nvme_engines:
            str = " " * 11
            for i in range(line_length):
                str = str + " %2x" % i
            self.logger.info(str)
            self.logger.info(" " * 12 + "-" * (line_length * 3 - 1))
            str, i = "0x%08x: "%0, 0
            while length > i:
                if 0 == i % line_length and i: # print pcie offset
                    self.logger.info(str)
                    str = "0x%08x: " % (i) # begin print new line
                str = str + "%02x " % self[i]
                i =  i + 1
            else:
                self.logger.info(str)
        else:
            self.logger.error("%s don't support pcie config dump"%self.engine_opt_name)

    def get_pcie_header_offset(self, offset, bytes_count = 1):
        if self.engine_opt_name in self.nvme_engines:
            if bytes_count == 1:
                return interf.xt_pcie_device_config_read8(self._admin_qpair, offset)
            elif bytes_count == 2:
                return interf.xt_pcie_device_config_read16(self._admin_qpair, offset)
            elif bytes_count == 4:
                return interf.xt_pcie_device_config_read32(self._admin_qpair, offset)
            elif bytes_count == 8:
                return interf.xt_pcie_device_config_read64(self._admin_qpair, offset)
            else:
                self.logger.error("get a invalid bytes_count %s"%(bytes_count))
        else:
            self.logger.error("%s don't support get pcie header offset" % self.engine_opt_name)

    def set_pcie_header_offset(self, offset, value, bytes_count = 1):
        if self.engine_opt_name in self.nvme_engines:
            if bytes_count == 1:
                return interf.xt_pcie_device_config_write8(self._admin_qpair, offset, value)
            elif bytes_count == 2:
                return interf.xt_pcie_device_config_write16(self._admin_qpair, offset, value)
            elif bytes_count == 4:
                return interf.xt_pcie_device_config_write32(self._admin_qpair, offset, value)
            elif bytes_count == 8:
                return interf.xt_pcie_device_config_write64(self._admin_qpair, offset, value)
            else:
                self.logger.error("set a invalid bytes_count %s"%(bytes_count))
        else:
            self.logger.error("%s don't support get pcie header offset" % self.engine_opt_name)

    def bind_driver(self, driver):
        if self.engine_opt_name in self.nvme_engines:
            if "uio" in driver or 'vfio-pci' in driver:
                cmdline = "%s config %s"%(self.pcie_setup_workspace, self.pcie_addr)
            else:
                cmdline = "%s reset %s" % (self.pcie_setup_workspace, self.pcie_addr)
            rc = os.system(cmdline)
            if (rc):
                self.logger.error("run command %s return %s"%(cmdline, rc))
        else:
            assert False, self.logger.error("%s don't support bind driver" % self.engine_opt_name)


    def pcie_bar_map(self, bir):
        if self.engine_opt_name in self.nvme_engines:
            assert bir >= 1 and bir <= 5
            interf.xt_pcie_bar_map(self._admin_qpair, bir)
        else:
            assert False, self.logger.error("%s don't support pcie bar map" % self.engine_opt_name)

    def pcie_bar_unmap(self, bir):
        if self.engine_opt_name in self.nvme_engines:
            assert bir >= 1 and bir <= 5
            interf.xt_pcie_bar_unmap(self._admin_qpair, bir)
        else:
            assert False, self.logger.error("%s don't support pcie bar unmap" % self.engine_opt_name)

    def pcie_bar_copy(self):
        if self.bar_info == NULL:
            self.bar_info = interf.xt_allocate_aligned_memory(interf.xt_admin_get_bar_size(self._admin_qpair), sizeof(void *))
        interf.xt_pcie_get_bar_data(self._admin_qpair, self.bar_info)

cdef class XT_DEVICES(object):
    cdef :
        XT_DRIVER driver
        XT_IO_QPAIR _default_io_qpair
        XT_BUFFER _default_admin_buffer
        unsigned long long *write_buf_addr_list
        unsigned long long sys_tick_us
        interf.xt_admin_qpair *_admin_qpair
        object logger
        object admin_buffer_lock
        int _max_data_transfer_size
        unsigned int io_unit_clear_size
        unsigned int nvme_register_size
        bytes _id_ctrl_raws
        dict  _id_ns_raws_dict
        unsigned char *nvme_register_raws
        list _active_ns

    def __cinit__(self, driver, logger, qdepth=128, timeout=1000000, update_ns=True, max_data_transfer_size=None,  disable_io_info_init=False):
        self.driver = driver
        self.logger = logger
        self._admin_qpair = self.driver._admin_qpair
        self.io_unit_clear_size = self._admin_qpair.io_unit_clear_size
        self.sys_tick_us = self.driver.sys_tick_us # 1us = sys_tick
        self.admin_buffer_lock = threading.Lock()
        self.nvme_register_size = 4096
        self.nvme_register_raws = <unsigned char *>interf.xt_allocate_aligned_memory(self.nvme_register_size, sizeof(void *))
        self._id_ns_raws_dict = {}
        self._active_ns = []
        if self.nvme_register_raws == NULL:
            assert False, self.logger.error("malloc nvme_register_raws failed")
        if not disable_io_info_init:
            if interf.xt_device_init(self._admin_qpair):
                assert False, self.logger.error("device init failed")
            self._default_io_qpair = XT_IO_QPAIR(self, qdepth=qdepth, timeout=100000, logger=self.logger)
            self._default_admin_buffer = XT_BUFFER(buf_length=4096, buf_align=64, logger=self.logger, mem_init=1, device=self)
            self.nvme_id_ctrl()
            if update_ns:
                self.update_name_spaces()
            self._max_data_transfer_size = interf.xt_get_mdts(self._admin_qpair) if max_data_transfer_size is None else max_data_transfer_size
            self.create_write_buffer_list()
        else:
            self.logger.info("-----------------skip io info init----------------")

    cpdef reload_engines(self, engine_opt_name):
        self.driver.load_engines(engine_opt_name=engine_opt_name)
        self._default_io_qpair.active_flag = 0
        self._default_io_qpair.qpair_create(self._default_io_qpair.io_qpair.qpair_iodepth)

    cpdef get_nvme_register_raws(self):
        if self._admin_qpair.nvme_regs == NULL:
            return bytes(self.nvme_register_size)
        else:
            memcpy(self.nvme_register_raws, <char *>self._admin_qpair.nvme_regs, self.nvme_register_size)
            return self.nvme_register_raws[0:self.nvme_register_size]
    @property
    def default_io_qpair(self):
        return self._default_io_qpair

    @property
    def id_ctrl_raws(self):
        # self._default_admin_buffer.dump_buf()
        return self._id_ctrl_raws[:self.nvme_register_size]

    @property
    def id_ns_raws_dict(self):
        return self._id_ns_raws_dict

    @property
    def active_ns(self):
        return self._active_ns

    @property
    def max_data_transfer_size(self):
        return self._max_data_transfer_size

    def create_write_buffer_list(self, unsigned int crc_type=8):
        cdef XT_BUFFER _xt_buf
        cdef unsigned int write_buf_idx = 0
        if len(WRITE_BUFFER_LIST) == 0:
            pattern_path = os.path.join(xt_project_path(), 'xt_pattern')
            filenames = os.listdir(pattern_path)
            # pattern name --> pattern name + - buffer index
            pattern_files = [os.path.join(pattern_path, f) for f in filenames if os.path.isfile(os.path.join(pattern_path, f))]
            pattern_dict = {}
            for pattern_file in pattern_files:
                write_buf_idx = int(pattern_file.split('-')[-1])
                pattern_dict[write_buf_idx] = pattern_file
            pattern_dict = {k: pattern_dict[k] for k in sorted(pattern_dict.keys())}
            for key in pattern_dict:
                pattern_file = pattern_dict[key]
                _xt_buf = XT_BUFFER(buf_length=self._max_data_transfer_size, buf_align=4096, logger=self.logger, buf_type=1, mem_init=1, device=self)
                _xt_buf.write_buffer_init(pattern_file)

    @property
    def get_write_buffer_list(self):
        return WRITE_BUFFER_LIST

    cdef dump_buffers_status(self, list buf_inst):
        cdef XT_BUFFER _xt_buf
        for _xt_buf in buf_inst:
            self.logger.info("buffer address 0x%x buffer status %s"%(<unsigned long long>&_xt_buf._buffer_instance, _xt_buf._buffer_instance.buf_status))
    cdef inline unsigned int prepare_io_buffer(self, list buf_inst, XT_BUFFER _xt_buf, XT_IO_QPAIR qpair, interf.xt_buffer * _buf, unsigned int next_buffer_index, unsigned int buf_inst_count, unsigned long long init_tick):
        if buf_inst is None:
            _buf = NULL
            return 0
        for index in range(next_buffer_index % buf_inst_count, buf_inst_count):
            _xt_buf = buf_inst[index]
            if _xt_buf._buffer_instance.buf_status == 0:
                _buf = &_xt_buf._buffer_instance
                return index
        while interf.get_system_ticks() - init_tick < qpair.io_qpair.timeout:
            next_buffer_index = 0
            for _xt_buf in buf_inst:
                if _xt_buf._buffer_instance.buf_status == 0:
                    _buf = &_xt_buf._buffer_instance
                    return next_buffer_index
                next_buffer_index += 1
                interf.xt_wait_completion_io(self._admin_qpair, qpair.io_qpair, 0)
        else:
            self.dump_buffers_status(buf_inst)
            interf.xt_dump_io_unit(qpair.io_qpair)
            assert False, self.logger.error("get io buffer timeout")

    cpdef wait_io_cmd_completed(self, unsigned long long io_u, XT_IO_QPAIR qpair, timeout_tick=1000000):
        cdef unsigned long long init_tick
        cdef interf.cmds_u * _io_u = <interf.cmds_u *> io_u
        init_tick = interf.get_system_ticks()
        if self.driver.io_sync_flag:
            cpl = self.xt_parse_cmd_cpl(<unsigned long long> _io_u)
            return cpl
        else:
            while interf.get_system_ticks() - init_tick < timeout_tick:
                if _io_u.cmd_status == 2:
                    break
                interf.xt_wait_completion_io(self._admin_qpair, qpair.io_qpair, 1)
            else:
                assert False, self.logger.error("get io unit timeout in qpair:%s, default io unit status %s timeout tick %s" % (qpair, _io_u.cmd_status, timeout_tick))
            cpl = self.xt_parse_cmd_cpl(<unsigned long long >_io_u)
            _io_u.cmd_status = 0
            return cpl

    cpdef wait_admin_cmd_completed(self, unsigned long long admin_unit, timeout_tick=1000000):
        cdef unsigned long long init_tick
        cdef interf.cmds_u * _admin_unit = <interf.cmds_u *> admin_unit
        init_tick = interf.get_system_ticks()
        if self.driver.admin_sync_flag:
            cpl = self.xt_parse_cmd_cpl(<unsigned long long> _admin_unit)
            return cpl
        else:
            while interf.get_system_ticks() - init_tick < timeout_tick:
                if _admin_unit.cmd_status == 2:
                    break
                interf.xt_wait_completion_admin(self._admin_qpair)
            else:
                assert False, self.logger.error("get admin unit timeout, default io unit status %s timeout_tick %s" % (_admin_unit.cmd_status, timeout_tick))
            cpl = self.xt_parse_cmd_cpl(<unsigned long long >_admin_unit)
            _admin_unit.cmd_status = 0
            return cpl

    cpdef xt_parse_cmd_cpl(self, unsigned long long cmd_u):
        # assert io_u.cmd_status == 2, self.logger.error("parse command unit cpl status is %d"%( io_u.cmd_status))
        cdef interf.cmds_u * _cmd_u = <interf.cmds_u *>cmd_u
        return ((_cmd_u.cpl_cdw0, _cmd_u.cpl_rsvd1, _cmd_u.cpl_sqhd, _cmd_u.cpl_sqid, _cmd_u.cpl_cid, _cmd_u.cpl_status.raw & 0x1, (_cmd_u.cpl_status.raw >> 1) & 0xFF,
               (_cmd_u.cpl_status.raw >> 9) & 0x7,  (_cmd_u.cpl_status.raw >> 12) & 0x3,  (_cmd_u.cpl_status.raw >> 14) & 0x1,  (_cmd_u.cpl_status.raw >> 15) & 0x1), _cmd_u.complete_time)

    cpdef cmd_status_check(self, unsigned long long cmd_unit, unsigned int status_code_expected=0, unsigned int status_code_type_expected=0):
        cdef interf.cmds_u * _cmd_unit =  <interf.cmds_u *> cmd_unit
        if ((_cmd_unit.cpl_status.raw >> 1) & 0xFF) != status_code_expected or ((_cmd_unit.cpl_status.raw >> 9) & 0x3) != status_code_type_expected:
            self.logger.error("check status fail: expect status code type %s actual %s, expect status code %s actual %s", ((_cmd_unit.cpl_status.raw >> 9) & 0x3),
                              status_code_type_expected, ((_cmd_unit.cpl_status.raw >> 1) & 0xFF) , status_code_expected)
            assert False

    cdef inline interf.cmds_u * get_io_unit(self, XT_IO_QPAIR qpair, interf.cmds_u * io_u, timeout_tick=1000000, init_tick=0):
        while interf.get_system_ticks() - init_tick < timeout_tick:
            interf.xt_wait_completion_io(self._admin_qpair, qpair.io_qpair, 1)
            # print(qpair.io_qpair.qpair_completions)
            io_u = interf.cmds_u_rpop(qpair.io_qpair.completed_cmds_u_ring)
            if io_u != NULL:
                return io_u
        else:
            assert False, self.logger.error("get io unit timeout %s init tick %s in qpair:%s" % (timeout_tick, init_tick, qpair))
        return NULL

    cdef inline void xt_io_qpair_nsid_check(self, XT_IO_QPAIR qpair, unsigned int nsid):
        if qpair.io_qpair.nsid != nsid:
            if self.driver.nvme_engine_flag:
                if self.driver.init_char_device_flag == 0:
                    self.driver.get_device_name()
                qpair.io_qpair.fid =  interf.xt_device_open(self._admin_qpair, self.driver.devices_dict[nsid].encode('utf-8'), nsid)
                assert qpair.io_qpair.fid > 0, self.logger.error("Open device failed %s"%qpair.io_qpair.fid)
            qpair.io_qpair.nsid = nsid

    cpdef send_admin_cmds(self, opcode, buf, fuse=0, psdt=0, cid=0, nsid=1, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0,
                            cdw12=0,  cdw13=0, cdw14=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=True, timeout=1000000,
                            io_status_code_expected=0,  io_status_code_type_expected=0):
        cdef interf.cmds_u * admin_unit = NULL
        cdef interf.xt_buffer * _buf = NULL
        cdef unsigned int _buf_type = 0
        cdef unsigned long long timeout_tick = self.sys_tick_us * timeout
        cdef XT_BUFFER _xt_buf
        cdef unsigned long long index = 0
        if buf is None:
            _buf = NULL
        else:
            _xt_buf = buf
            _buf = &_xt_buf._buffer_instance
        admin_unit = interf.xt_prepare_admin_unit(self._admin_qpair)
        assert admin_unit != NULL, self.logger.error("Get a invalid command unit")
        memset(admin_unit, 0, sizeof(interf.cmds_u))
        admin_unit.start_time = interf.get_system_ticks()
        admin_unit.opc = opcode
        admin_unit.flags =  ((psdt & 0x3) << 6)
        admin_unit.cid = cid
        admin_unit.nsid = nsid
        admin_unit.cdw2 = cdw2
        admin_unit.cdw3 = cdw3
        admin_unit.mptr = mptr
        admin_unit.prp1 = prp1
        admin_unit.prp2 = prp2
        admin_unit.cdw10 = cdw10
        admin_unit.cdw11 = cdw11
        admin_unit.cdw12 = cdw12
        admin_unit.cdw13 = cdw13
        admin_unit.cdw14 = cdw14
        admin_unit.cdw15 = cdw15
        admin_unit.io_status_code_expected = io_status_code_expected
        admin_unit.io_status_code_type_expected = io_status_code_type_expected
        admin_unit.completed_cmds_u_ring = self._admin_qpair.completed_cmds_u_ring
        interf.xt_submit_admin_cmd(self._admin_qpair, _buf, admin_unit, buf_size)
        if admin_unit.rc != 0:
            assert False, self.logger.error("error in submitting admin command, 0x%x" % admin_unit.rc)
        if wait_completed:
            self.wait_admin_cmd_completed(<unsigned long long>admin_unit, timeout_tick=timeout_tick)
        if rtn_cmds_u_addr:
            return <unsigned long long> admin_unit

    cpdef nvme_id_ctrl(self, unsigned int init_mem=0):
        cdef unsigned long long admin_unit
        cdef interf.cmds_u * _admin_unit
        self.admin_buffer_lock.acquire()
        if init_mem:
            memset(self._default_admin_buffer.m_raw, 0, 4096)
        admin_unit = self.send_admin_cmds(opcode=0x6, buf=self._default_admin_buffer, nsid=0, buf_size=4096, cdw10=1, wait_completed=1)
        self.cmd_status_check(admin_unit, 0, 0)
        # interf.memory_dump(self._default_admin_buffer.m_raw, 4096, 64, 0, NULL)
        interf.xt_update_ctrl_data(self._admin_qpair, self._default_admin_buffer.m_raw)
        self._id_ctrl_raws = self._default_admin_buffer.encode(0, 4096)
        self.admin_buffer_lock.release()

    cpdef nvme_id_ns(self, unsigned int nsid, unsigned int init_mem=0):
        cdef unsigned long long admin_unit
        cdef interf.cmds_u * _admin_unit
        self.admin_buffer_lock.acquire()
        if init_mem:
            memset(self._default_admin_buffer.m_raw, 0, 4096)
        admin_unit = self.send_admin_cmds(opcode=0x6, buf=self._default_admin_buffer, nsid=nsid, buf_size=4096, wait_completed=1)
        self.cmd_status_check(admin_unit, 0, 0)
        # interf.memory_dump(self._default_admin_buffer.m_raw, 4096, 64, 0, NULL)
        interf.xt_update_ns_data(self._admin_qpair, self._default_admin_buffer.m_raw, nsid)
        self._id_ns_raws_dict[nsid] = self._default_admin_buffer.encode(0, 4096)
        self.admin_buffer_lock.release()

    cpdef nvme_list_ns(self, unsigned int init_mem=0):
        cdef unsigned long long admin_unit
        cdef interf.cmds_u * _admin_unit
        self.admin_buffer_lock.acquire()
        self._active_ns = []
        if init_mem:
            memset(self._default_admin_buffer.m_raw, 0, 4096)
        admin_unit = self.send_admin_cmds(opcode=0x6, buf=self._default_admin_buffer, nsid=0, buf_size=4096, cdw10=2, wait_completed=1)
        self.cmd_status_check(admin_unit, 0, 0)
        for offset in range(0, 4096, 4):
            nsid = self._default_admin_buffer.get_uint32(offset)
            if nsid != 0:
                self._active_ns.append(nsid)
            else:
                break
        # interf.memory_dump(self._default_admin_buffer.m_raw, 4096, 64, 0, NULL)
        self.admin_buffer_lock.release()

    cpdef update_name_spaces(self, active_ns=None, unsigned int clear_next_open_index=1):
        if self.driver.devices_driver == 'nvme':
            devices_list, char_device = [], ""
            for root, dirs, files in os.walk("/sys/block"):
                for filename in dirs:
                    realpath = os.path.realpath(os.path.join(root, filename))
                    if 'nvme' in filename[:5] and self.driver.pcie_addr in realpath:
                        char_device = "/dev/%s"%realpath.split(os.path.sep)[-2]
                        nsid = int(os.popen('cat %s/nsid' % realpath).read())
                        devices_list.append(['/dev/%s' % filename, nsid])
                        self.driver.devices_dict[nsid] = '/dev/%s' % filename
            if devices_list and char_device:
                if self.driver.init_char_device_flag:
                    interf.xt_char_device_update_info(self._admin_qpair, char_device.encode('utf-8'), strlen(char_device.encode('utf-8')) + 1)
                else:
                    interf.xt_char_device_info_init(self._admin_qpair, char_device.encode('utf-8'), strlen(char_device.encode('utf-8')) + 1, XT_MAX_NSID)
                    self.driver.init_char_device_flag = 1
            else:
                self.logger.error("can't find devices %s and char device %s"%(devices_list, char_device))
            self.nvme_list_ns()
            for nsid in self._active_ns:
                interf.xt_block_device_update_info(self._admin_qpair, self.driver.devices_dict[nsid].encode('utf-8'), strlen(self.driver.devices_dict[nsid].encode('utf-8')) + 1,
                                                   nsid, clear_next_open_index)
                if active_ns is None or nsid in active_ns:
                    self.nvme_id_ns(nsid)
        elif 'uio' in self.driver.devices_driver or 'vfio-pci' in self.driver.devices_driver or 'simulator' in self.driver.devices_driver:
            if self.driver.init_char_device_flag == 0:
                interf.xt_char_device_info_init(self._admin_qpair, NULL, 0, XT_MAX_NSID)
                self.driver.init_char_device_flag = 1
            self.nvme_list_ns()
            for nsid in self._active_ns:
                if active_ns is None or nsid in active_ns:
                    self.nvme_id_ns(nsid)
        elif self.driver.devices_driver == 'null':
            if self.driver.init_char_device_flag == 0:
                interf.xt_char_device_info_init(self._admin_qpair, NULL, 0, XT_MAX_NSID)
                self.driver.init_char_device_flag = 1
            self._active_ns = [1]
            self.nvme_id_ns(1, 1)
        else:
            self.logger.info("%s needn't get devices name"%self.driver.engine_opt_name)

    cpdef get_io_submit_status(self, XT_IO_QPAIR qpair, iodepth=None):
        cdef interf.cmds_u * io_u = NULL
        cdef unsigned int offset = 0
        cdef unsigned long long submit_index = 0
        cdef unsigned long long _index = 0
        iodepth = iodepth if iodepth else qpair.io_qpair.qpair_iodepth
        _index = qpair.io_qpair.submit_count - iodepth + 1
        io_status_list = [0] * iodepth
        for offset in range(qpair.io_qpair.qpair_iodepth):
            io_u = &qpair.io_qpair.io_units[offset]
            submit_index = io_u.submit_index
            if submit_index < _index:
                continue
            assert io_status_list[submit_index - _index] is None
            if io_u.cmd_status == 2:
                io_status_list[submit_index - _index] = 1
        return io_status_list

    cpdef send_io_cmds(self, unsigned int opcode, XT_BUFFER buf=None, XT_IO_QPAIR qpair=None, unsigned int fuse=0, unsigned int psdt=0, unsigned int cid=0, unsigned int nsid=1, unsigned int cdw2=0,
                       unsigned int cdw3=0, unsigned long long mptr=0,  unsigned long long prp1=0, unsigned long long prp2=0, unsigned int cdw10=0, unsigned int cdw11=0,
                       unsigned int cdw12=0, unsigned int cdw13=0, unsigned int cdw14=0, unsigned int cdw15=0, unsigned int wait_completed=1, unsigned int sector_size=512,
                       unsigned int meta_sector_size=0, unsigned int rtn_io_u_addr=True, unsigned int timeout=1000000, unsigned int io_status_code_expected=0,
                       unsigned int io_status_code_type_expected=0, unsigned int io_tailer_flag=0, unsigned int pi_type=0):
        """
            io_buf_type: bit 0 need wait command return or compare done
        """
        cdef interf.cmds_u * io_u = NULL
        cdef interf.xt_buffer * _buf = NULL
        cdef unsigned int _buf_type = 0
        cdef unsigned long long timeout_tick = self.sys_tick_us * timeout
        cdef XT_BUFFER _xt_buf
        cdef unsigned long buf_size = 0
        # cdef unsigned long long _init_tick = 0
        cdef unsigned int _lbacnt = (cdw12 & 0xFFFF) + 1
        qpair = self._default_io_qpair if qpair is None else qpair
        if buf is None:
            _buf = NULL
        else:
            _xt_buf = buf
            _buf = &_xt_buf._buffer_instance
            if _buf.buf_type != pi_type:
                buf.meta_data_change(meta_sector_size, pi_type, sector_size)
        self.xt_io_qpair_nsid_check(qpair, nsid)
        io_u = self.get_io_unit(qpair, io_u, timeout_tick=timeout_tick, init_tick=interf.get_system_ticks())
        memset(io_u, 0, self.io_unit_clear_size)
        io_u.start_time = interf.get_system_ticks()
        buf_size = (sector_size + meta_sector_size) * _lbacnt
        io_u.opc = opcode
        io_u.flags =  ((psdt & 0x3) << 6) | fuse & 0x3
        io_u.cid = cid
        io_u.nsid = nsid
        io_u.cdw2 = cdw2
        io_u.cdw3 = cdw3
        io_u.mptr = mptr
        io_u.prp1 = prp1
        io_u.prp2 = prp2
        io_u.cdw10 = cdw10
        io_u.cdw11 = cdw11
        io_u.cdw12 = cdw12
        io_u.cdw13 = cdw13
        io_u.cdw14 = cdw14
        io_u.cdw15 = cdw15
        io_u.sector_size = sector_size
        io_u.meta_sector_size = meta_sector_size
        io_u.io_tailer_flag = io_tailer_flag
        io_u.io_status_code_expected = io_status_code_expected
        io_u.io_status_code_type_expected = io_status_code_type_expected
        io_u.qpair_info = qpair.io_qpair
        io_u.io_buffer = _buf
        io_u.completed_cmds_u_ring = qpair.io_qpair.completed_cmds_u_ring
        interf.xt_submit_io_cmd(self._admin_qpair, qpair.io_qpair, _buf, io_u, buf_size, _lbacnt)
        if self.driver.io_sync_flag:
            if io_u.rc < 0:
                assert False, self.logger.error("error in submitting io command, 0x%x with %s" % io_u.rc, self.driver.engine_opt_name)
        else:
            if io_u.rc != 0:
                assert False, self.logger.error("error in submitting io command, 0x%x" % io_u.rc)
        if wait_completed:
            self.wait_io_cmd_completed(<unsigned long long>io_u, qpair, timeout_tick=timeout_tick)
        if rtn_io_u_addr:
            return <unsigned long long> io_u

    cdef check_loop(self, slba=None, elba=None, lbacnt=None):
        if elba == 0:
            loop_cnt = len(slba) if type(slba) is list else 1
            elba = slba + lbacnt - 1 if (type(slba) is int and loop_cnt == 1) else 0
        else:
            if lbacnt:
                loop_cnt = len(slba) if type(slba) is list else (elba - slba + 1) // lbacnt if \
                    (elba - slba + 1) % lbacnt == 0 else (elba - slba + 1) // lbacnt + 1
                if loop_cnt == 1:
                    lbacnt = elba - slba + 1
            else:
                loop_cnt, lbacnt = 1, elba - slba + 1
        return loop_cnt, lbacnt, elba

    cdef check_io_qdepth(self, qdepth, XT_IO_QPAIR qpair, buf_list, reap_type, unsigned int io_mode, limit_iops_count=None, limit_io_count=None, microseconds_delay=None):
        """
            reap_type: type 0 async submit ensure that the queue is as full as possible;
                       type 1 submit iodepth x once, wait x command return
                       type 2 limit iops*
                       type 3 limit bw*
                       type 4 add delay time(us) in type 1
            io_mode: bit 0: 0 is read, 1 is write; 
                     bit 1 ~ 3:  000: buffer not change
                                 001: change buffer with io_tailer
                                 010: data verify for read
                                 011 ~ 111: reserved
                     other bits: reserved
        """
        cdef unsigned int _qdepth = 0
        cdef unsigned int _io_mode_type = (io_mode >> 1) & 0x7
        if io_mode & 0x1:
            if _io_mode_type == 0:
                _qdepth = qpair.io_qpair.qpair_iodepth if qdepth == 0 else qdepth
            elif _io_mode_type == 1:
                qdepth = qpair.io_qpair.qpair_iodepth if qdepth == 0 else qdepth
                _qdepth = len(buf_list) if type(buf_list) is list else 1
                _qdepth = min(qdepth, _qdepth)
            else:
                assert False, self.logger.error("can't init qdepth, qdepth: %s, qnum: %s buf_list: %s, reap_type: %s; io_mode:%s"%(
                                                 qdepth, qpair, buf_list, reap_type, hex(io_mode)))
        else:
            if _io_mode_type == 0:
                _qdepth = qpair.io_qpair.qpair_iodepth if qdepth == 0 else qdepth
            elif _io_mode_type == 2:
                qdepth = qpair.io_qpair.qpair_iodepth if qdepth == 0 else qdepth
                _qdepth = len(buf_list) if type(buf_list) is list else 1
                _qdepth = min(qdepth, _qdepth)
            else:
                assert False, self.logger.error("can't init qdepth, qdepth: %s, qnum: %s buf_list: %s, reap_type: %s; io_mode:%s"%(
                                                 qdepth, qpair, buf_list, reap_type, hex(io_mode)))
        if reap_type >= 2:
            if reap_type == 2:
                assert limit_iops_count != 0, self.logger.error("get a invalid value limit_iops_count is none")
                qpair.io_qpair.limit_iops_count = limit_iops_count
                qpair.io_qpair.limit_io_count = 0
                qpair.io_qpair.microseconds_delay = 0
            elif reap_type == 3:
                assert limit_io_count != 0, self.logger.error("get a invalid value limit_io_count is none")
                qpair.io_qpair.limit_io_count = limit_io_count
                qpair.io_qpair.limit_iops_count = 0
                qpair.io_qpair.microseconds_delay = 0
            elif reap_type == 4:
                assert microseconds_delay != 0, self.logger.error("get a invalid value microseconds_delay is none")
                qpair.io_qpair.microseconds_delay = microseconds_delay
                qpair.io_qpair.limit_iops_count = 0
                qpair.io_qpair.limit_io_count = 0
        else:
            qpair.io_qpair.limit_iops_count = 0
            qpair.io_qpair.limit_io_count = 0
            qpair.io_qpair.microseconds_delay = 0
        if self.driver.io_sync_flag:
            qpair.io_qpair.current_iodepth_count = 1
            _qdepth = 1
        else:
            qpair.io_qpair.current_iodepth_count = _qdepth
        qpair.io_qpair.reap_type = reap_type
        return _qdepth

    cdef inline void completed_io_unit_check(self, XT_IO_QPAIR qpair, interf.cmds_u * io_u):
        io_u = interf.cmds_u_get_ring_next(qpair.io_qpair.completed_cmds_u_ring, True)
        while io_u != NULL:
            assert io_u.cmd_status != 1, self.logger.error("io status in busy")
            if io_u.cmd_status == 2:
                interf.xt_completed_io_check(self._admin_qpair, io_u)
            elif io_u.cmd_status == 0:
                break
            io_u = interf.cmds_u_get_ring_next(qpair.io_qpair.completed_cmds_u_ring, False)

    cpdef wait_io_completion(self, XT_IO_QPAIR qpair, unsigned long long timeout_tick=0):
        cdef unsigned long long init_tick = interf.get_system_ticks()
        timeout_tick = timeout_tick if timeout_tick else qpair.io_qpair.timeout * (qpair.io_qpair.submit_count - qpair.io_qpair.last_submit_count)
        stime = time.time()
        while interf.get_system_ticks() - init_tick < timeout_tick:
            interf.xt_wait_completion_io(self._admin_qpair, qpair.io_qpair, 0)
            if qpair.io_qpair.submit_count - qpair.io_qpair.last_submit_count == qpair.io_qpair.qpair_completions:
                break
        else:
            assert False, self.logger.error("get io unit timeout %s init tick %s in qpair:%s qpair_completions %s" % (timeout_tick, init_tick, qpair, qpair.io_qpair.qpair_completions))
        qpair.io_qpair.submit_count = qpair.io_qpair.last_submit_count
        qpair.io_qpair.qpair_completions = 0

    cpdef wait_completion_qpair(self, XT_IO_QPAIR qpair):
        interf.xt_wait_completion_io(self._admin_qpair, qpair.io_qpair, 0)

    cdef inline unsigned int next_sequential_lba_count(self, unsigned long long slba, unsigned long long elba, unsigned int lbacnt):
        if slba + lbacnt - 1 < elba:
            return lbacnt
        else:
            return elba - slba + 1

    cdef inline unsigned long long next_sequential_slba(self, unsigned long long slba, unsigned long long elba, unsigned int lbacnt, unsigned long long _base_slba):
        if slba + lbacnt - 1 < elba:
            return slba + lbacnt
        else:
            return _base_slba

    cdef inline unsigned int next_sequential_buffer_index(self, unsigned int buffer_index, unsigned int buffer_count):
        if buffer_index >= buffer_count:
            return 0
        return buffer_index

    cdef inline void fill_io_unit(self, XT_IO_QPAIR qpair, interf.cmds_u * io_u, unsigned int opc, unsigned int psdt, unsigned int nsid, unsigned long long slba, unsigned int cdw12,
                                  unsigned int sector_size, unsigned int meta_sector_size, unsigned int io_status_code_expected=0, unsigned int io_status_code_type_expected=0,
                                  unsigned int cdw2=0, unsigned int cdw3=0, unsigned int cdw13=0, unsigned int cdw14=0, unsigned int cdw15=0):
        io_u.start_time = interf.get_system_ticks()
        io_u.opc = opc
        io_u.flags = ((psdt & 0x3) << 6)
        io_u.nsid = nsid
        io_u.cdw2 = cdw2
        io_u.cdw3 = cdw3
        io_u.cdw10 = slba & 0xffffffff
        io_u.cdw11 = (slba >> 32) & 0xffffffff
        io_u.cdw12 = cdw12
        io_u.cdw13 = cdw13
        io_u.cdw14 = cdw14
        io_u.cdw15 = cdw15
        io_u.sector_size = sector_size
        io_u.meta_sector_size = meta_sector_size
        io_u.io_status_code_expected = io_status_code_expected
        io_u.io_status_code_type_expected = io_status_code_type_expected
        io_u.qpair_info = qpair.io_qpair
        io_u.completed_cmds_u_ring = qpair.io_qpair.completed_cmds_u_ring

    cpdef send_io_read(self, XT_IO_QPAIR qpair, slba=None, lbacnt=None, unsigned long long elba=0, unsigned int cdw2=0, unsigned int cdw3=0,  unsigned int cdw13=0, unsigned int cdw14=0,
                       unsigned int cdw15=0,
                       unsigned int limitedRetry=0, unsigned int fua=0, unsigned int prinfo=0, unsigned int dtype=0, unsigned int sector_size=512, unsigned int meta_sector_size=0,
                       unsigned int reap_type=0, unsigned int qdepth=0, unsigned int nsid=1, unsigned int timeout=1000000, readbuf_list=None,  unsigned int status_check=True,
                       unsigned int io_check_type=1, writebuf_list=None, unsigned int limit_iops_count=0,unsigned int limit_io_count=0, unsigned int microseconds_delay=0, wait_completed=1,
                       unsigned int pi_type=0, unsigned int psdt=0):
        """
            io_check_type:  0 not check;  
                            bit 1 check status code and status code type; 
                            bit 2 read command check data include empty buffer  
                            bit 3 read command check data with excepted write buffer  
                            bit 4 read command check data with buffer tailer  
                            bit 5 read command only check buffer tailer (quickly performance check)
                            other bits resevered
        """
        cdef interf.cmds_u * io_u = NULL
        cdef unsigned int io_mode = (0x0 | (0x010 << 1))  if io_check_type else (0x0 | (0x000 << 1))
        cdef unsigned long long loop_num = 0
        cdef unsigned long long loop_cnt = 0
        cdef unsigned long long _slba = 0
        cdef unsigned int _lbacnt = 0
        cdef unsigned int buf_size = 0
        cdef unsigned int writebuf_list_count = len(writebuf_list) if type(writebuf_list) is list else 1
        cdef unsigned int writebuf_index = 0
        cdef unsigned int readbuf_list_count = 0
        cdef unsigned long long timeout_tick = self.sys_tick_us * timeout
        cdef int excepted_write_check = io_check_type & 0x8
        cdef interf.xt_buffer * _buf = NULL
        cdef XT_BUFFER _xt_buf
        cdef unsigned int slba_list_type, lbacnt_list_type
        cdef unsigned int next_buffer_index = 0
        readbuf_list = readbuf_list if type(readbuf_list) is list else [readbuf_list]
        _xt_buf = readbuf_list[0]
        readbuf_list_count = len(readbuf_list)
        qdepth = self.check_io_qdepth(qdepth, qpair, readbuf_list, reap_type, io_mode, limit_iops_count, limit_io_count, microseconds_delay)
        loop_cnt, lbacnt, elba = self.check_loop(slba, elba, lbacnt)
        slba_list_type,  lbacnt_list_type = type(slba) is list, type(lbacnt) is list
        assert slba_list_type == lbacnt_list_type, self.logger.error("slba and lbacnt need the same type, current slba type is %s, lbacnt type is %s"%(type(slba), type(lbacnt)))
        self.logger.info("send read commands with slba:0x%x elba:0x%x lbacnt: 0x%x loop count %s qdepth %s qinfo->completed_check_index %s"%(slba, elba, lbacnt, loop_cnt, qdepth,
                          qpair.io_qpair.completed_check_index))
        _lbacnt = lbacnt[0] if slba_list_type else lbacnt
        _slba =   slba[0] if slba_list_type else slba
        self.xt_io_qpair_nsid_check(qpair, nsid)
        while loop_num < loop_cnt:
            io_u = interf.xt_prepare_io_unit(self._admin_qpair, qpair.io_qpair)
            memset(io_u, 0, self.io_unit_clear_size)
            io_u.start_time = interf.get_system_ticks()
            if io_check_type > 1:
                next_buffer_index = self.prepare_io_buffer(readbuf_list, _xt_buf, qpair, _buf, next_buffer_index, readbuf_list_count, io_u.start_time)
                _xt_buf = readbuf_list[next_buffer_index]
                _buf = &_xt_buf._buffer_instance
            else:
                _xt_buf = readbuf_list[0]
                _buf = &_xt_buf._buffer_instance
            io_u.opc = 2
            io_u.flags = ((psdt & 0x3) << 6)
            io_u.nsid = nsid
            io_u.cdw2 = cdw2
            io_u.cdw3 = cdw3
            io_u.cdw10 = _slba & 0xffffffff
            io_u.cdw11 = (_slba >> 32) & 0xffffffff
            io_u.cdw12 = limitedRetry << 31 | fua << 30 | prinfo << 26 | dtype << 20 | (_lbacnt - 1)
            io_u.cdw13 = cdw13
            io_u.cdw14 = cdw14
            io_u.cdw15 = cdw15
            buf_size = (sector_size + meta_sector_size) * _lbacnt
            io_u.sector_size = sector_size
            io_u.meta_sector_size = meta_sector_size
            io_u.qpair_info =  qpair.io_qpair
            io_u.completed_cmds_u_ring = qpair.io_qpair.completed_cmds_u_ring
            # self.fill_io_unit(qpair=qpair, io_u=io_u, opc=2, psdt=psdt, nsid=nsid, slba=_slba, cdw12=limitedRetry << 31 | fua << 30 | prinfo << 26 | dtype << 20 | (_lbacnt - 1),
            #                   sector_size=sector_size, meta_sector_size=meta_sector_size, io_status_code_expected=0, io_status_code_type_expected=0, cdw2=cdw2, cdw3=cdw3,
            #                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15)
            io_u.io_buffer = _buf
            if excepted_write_check:
                io_u.excepted_write_check = 1
                _xt_buf = writebuf_list[writebuf_index]
                io_u.excepted_write_buffer_index = _xt_buf._buffer_instance.buf_index
                writebuf_index += 1
                if writebuf_index >= writebuf_list_count:
                    writebuf_index = 0
            interf.xt_submit_io_cmd(self._admin_qpair, qpair.io_qpair, _buf, io_u, buf_size, _lbacnt)
            if not slba_list_type:
                _slba += lbacnt
                _lbacnt = self.next_sequential_lba_count(_slba, elba, lbacnt)
            else:
                _slba = slba[loop_num]
                _lbacnt = lbacnt[loop_num]
            loop_num += 1
        if wait_completed == 1:
            interf.xt_wait_qpair_all_submission_io_completion(self._admin_qpair, qpair.io_qpair)

    cpdef send_io_write(self, XT_IO_QPAIR qpair, slba=None, lbacnt=None, unsigned long long elba=0, unsigned int cdw2=0, unsigned int cdw3=0,  unsigned int cdw13=0, unsigned int cdw14=0,
                        unsigned int cdw15=0,
                        unsigned int limitedRetry=0, unsigned int fua=0, unsigned int prinfo=0, unsigned int dtype=0, unsigned int sector_size=512, unsigned int meta_sector_size=0,
                        unsigned int reap_type=0, unsigned int qdepth=0, unsigned int nsid=1, unsigned int timeout=1000000, unsigned int status_check=True,
                        unsigned int limit_iops_count=0, unsigned int limit_io_count=0, unsigned int microseconds_delay=0, unsigned int io_tailer_flag=0, unsigned int wait_completed=1,
                        writebuf_list=None, unsigned int pi_type=0, unsigned int psdt=0):
        cdef interf.cmds_u * io_u = NULL
        cdef interf.xt_buffer * _buf = NULL
        cdef unsigned int io_mode = (0x1 | (0x001 << 1)) if io_tailer_flag else (0x1 | (0x000 << 1))
        cdef unsigned long long loop_num = 0
        cdef unsigned long long loop_cnt = 0
        cdef unsigned long long _slba = 0
        cdef unsigned int _lbacnt = 0
        cdef unsigned int buf_size = 0
        cdef unsigned int writebuf_list_count = len(writebuf_list) if type(writebuf_list) is list else 1
        cdef unsigned long long timeout_tick = self.sys_tick_us * timeout
        cdef unsigned int slba_list_type, lbacnt_list_type
        cdef unsigned int next_buffer_index = 0
        cdef XT_BUFFER _xt_buf
        loop_cnt, lbacnt, elba = self.check_loop(slba, elba, lbacnt)
        writebuf_list = writebuf_list if type(writebuf_list) is list else [writebuf_list]
        _xt_buf = writebuf_list[0]
        qdepth = self.check_io_qdepth(qdepth, qpair, writebuf_list, reap_type, io_mode, limit_iops_count, limit_io_count, microseconds_delay)
        for _xt_buf in writebuf_list:
            _xt_buf.meta_data_change(meta_sector_size=meta_sector_size, pi_type=pi_type, sector_size=sector_size)
        loop_cnt, lbacnt, elba = self.check_loop(slba, elba, lbacnt)
        slba_list_type,  lbacnt_list_type = type(slba) is list, type(lbacnt) is list
        assert slba_list_type == lbacnt_list_type, self.logger.error("slba and lbacnt need the same type, current slba type is %s, lbacnt type is %s"%(
                                                                      type(slba), type(lbacnt)))
        self.logger.info("send write commands with slba:0x%x elba:0x%x lbacnt: 0x%x loop count %s qdepth %s qinfo->completed_check_index %s"%(
                          slba, elba, lbacnt, loop_cnt, qdepth, qpair.io_qpair.completed_check_index))
        _lbacnt = lbacnt[0] if slba_list_type else lbacnt
        _slba =   slba[0] if slba_list_type else slba
        self.xt_io_qpair_nsid_check(qpair, nsid)
        while loop_num < loop_cnt:
            io_u = interf.xt_prepare_io_unit(self._admin_qpair, qpair.io_qpair)
            memset(io_u, 0, self.io_unit_clear_size)
            io_u.start_time = interf.get_system_ticks()
            if io_tailer_flag:
                next_buffer_index = self.prepare_io_buffer(writebuf_list, _xt_buf, qpair, _buf, next_buffer_index, writebuf_list_count, io_u.start_time)
                _xt_buf = writebuf_list[next_buffer_index]
                _buf = &_xt_buf._buffer_instance
            else:
                next_buffer_index = self.next_sequential_buffer_index(next_buffer_index, writebuf_list_count)
                _xt_buf = writebuf_list[next_buffer_index]
                _buf = &_xt_buf._buffer_instance
                next_buffer_index += 1
            io_u.opc = 1
            io_u.flags = ((psdt & 0x3) << 6)
            io_u.nsid = nsid
            io_u.cdw2 = cdw2
            io_u.cdw3 = cdw3
            io_u.cdw10 = _slba & 0xffffffff
            io_u.cdw11 = (_slba >> 32) & 0xffffffff
            io_u.cdw12 = limitedRetry << 31 | fua << 30 | prinfo << 26 | dtype << 20 | (_lbacnt - 1)
            io_u.cdw13 = cdw13
            io_u.cdw14 = cdw14
            io_u.cdw15 = cdw15
            buf_size = (sector_size + meta_sector_size) * _lbacnt
            io_u.sector_size = sector_size
            io_u.meta_sector_size = meta_sector_size
            io_u.qpair_info = qpair.io_qpair
            io_u.completed_cmds_u_ring = qpair.io_qpair.completed_cmds_u_ring
            # self.fill_io_unit(qpair=qpair, io_u=io_u, opc=1, psdt=psdt, nsid=nsid, slba=_slba, cdw12=limitedRetry << 31 | fua << 30 | prinfo << 26 | dtype << 20 | (_lbacnt - 1),
            #                   sector_size=sector_size, meta_sector_size=meta_sector_size, io_status_code_expected=0, io_status_code_type_expected=0, cdw2=cdw2, cdw3=cdw3,
            #                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15)
            io_u.io_buffer = _buf
            io_u.io_tailer_flag = io_tailer_flag
            interf.xt_submit_io_cmd(self._admin_qpair, qpair.io_qpair, _buf, io_u, buf_size, _lbacnt)
            if not slba_list_type:
                _slba += lbacnt
                _lbacnt = self.next_sequential_lba_count(_slba, elba, lbacnt)
            else:
                _slba = slba[loop_num]
                _lbacnt = lbacnt[loop_num]
            loop_num += 1
        #     send write commands with slba:0x0 elba:0xffffff lbacnt: 0x8 loop count 2097152 qdepth 1 qinfo->completed_check_index 1024
        if wait_completed == 1:
            interf.xt_wait_qpair_all_submission_io_completion(self._admin_qpair, qpair.io_qpair)

    cdef inline void _send_io_sequences(self, XT_IO_QPAIR qpair, list io_sequences=None, unsigned int psdt=0, unsigned int qdepth=1, list writebuf_list=None,
                                        list readbuf_list=None, unsigned long long timeout_tick=100000, unsigned int nsid=1, unsigned int cdw2=0, unsigned int cdw3=0,
                                        unsigned int cdw13=0, unsigned int cdw14=0, unsigned int cdw15=0, unsigned int pi_type=0):
        cdef interf.cmds_u * io_u = NULL
        cdef interf.xt_buffer * _buf = NULL
        cdef unsigned long long _slba = 0
        cdef unsigned char opcode = 0
        cdef unsigned int _lbacnt = 0
        cdef unsigned int buf_size = 0
        cdef unsigned long long loop_num = 0
        cdef unsigned int buf_index = 0
        cdef unsigned int sector_size = interf.xt_get_ns_sector_size(self._admin_qpair, nsid=nsid)
        cdef unsigned int meta_sector_size = interf.xt_get_ns_meta_data_size(self._admin_qpair, nsid=nsid)
        cdef XT_BUFFER _xt_buf
        for item in io_sequences:
            loop_num += 1
            opcode, _slba, _lbacnt, buf_index = item[0], item[1], item[2], item[3]
            io_u = interf.xt_prepare_io_unit(self._admin_qpair, qpair.io_qpair)
            if opcode == 1:
                _xt_buf = writebuf_list[buf_index]
                _buf = &_xt_buf._buffer_instance
            elif opcode == 2:
                _xt_buf = readbuf_list[buf_index]
                _buf = &_xt_buf._buffer_instance
            else:
                _buf = NULL
            memset(io_u, 0, self.io_unit_clear_size)
            buf_size = (sector_size + meta_sector_size) * _lbacnt
            io_u.start_time = interf.get_system_ticks()
            io_u.opc = opcode
            io_u.flags =  ((psdt & 0x3) << 6)
            io_u.nsid = nsid
            io_u.cdw10 = _slba & 0xffffffff
            io_u.cdw11 = (_slba >> 32) & 0xffffffff
            io_u.cdw12 = _lbacnt - 1
            io_u.sector_size = sector_size
            io_u.meta_sector_size = meta_sector_size
            io_u.io_status_code_expected = 0
            io_u.io_status_code_type_expected = 0
            io_u.qpair_info = qpair.io_qpair
            io_u.completed_cmds_u_ring = qpair.io_qpair.completed_cmds_u_ring
            # self.fill_io_unit(qpair=qpair, io_u=io_u, opc=1, psdt=psdt, nsid=nsid, slba=_slba, cdw12=_lbacnt - 1, sector_size=sector_size, meta_sector_size=meta_sector_size,
            #                   io_status_code_expected=0, io_status_code_type_expected=0, cdw2=cdw2, cdw3=cdw3, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15)
            io_u.io_buffer = _buf
            interf.xt_submit_io_cmd(self._admin_qpair, qpair.io_qpair, _buf, io_u, buf_size, _lbacnt)
        interf.xt_wait_qpair_all_submission_io_completion(self._admin_qpair, qpair.io_qpair)

    cdef __io_count_calculate(self, bs, unsigned long long _io_size):
        cdef unsigned int sum_item = 0
        cdef unsigned int index = 0
        cdef unsigned int key = 0
        cdef unsigned long long bs_sum = 0
        cdef unsigned long long io_count = 0
        cdef unsigned long long __io_size = 0
        if type(bs) is int:
            io_count = int(_io_size / bs)
        elif type(bs) is list or type(bs) is tuple or type(bs) is range:
            bs_sum = sum(bs)
            io_count = int(_io_size / bs_sum) * len(bs)
            __io_size = int(_io_size / bs_sum) * bs_sum
            for index in range(len(bs)):
                __io_size += bs[index]
                if __io_size <= _io_size:
                    io_count += 1
                else:
                    break
        elif type(bs) is dict:
            sum_item = sum(list(step.values()))
            for key in bs.keys():
                bs_sum += bs[key] * key
            io_count = int(_io_size / bs_sum) * sum_item
            __io_size = int(_io_size / bs_sum) * sum_item
            for key in bs.keys():
                for index in range(bs[key]):
                    __io_size += key
                    if __io_size <= _io_size:
                        io_count += 1
                    else:
                        break
        else:
            self.logger.error("get a invalid bs %s expect value type is int、list、tuple、range、dict"%bs)
        return io_count

    cdef init_lcg(self, XT_IO_QPAIR qpair, unsigned long long start, unsigned long long stop,  step, unsigned lcg_type=0, unsigned int reset_lcg=0):
        if lcg_type == 0:
            if qpair.io_qpair.io_lcg == NULL:
                qpair.io_qpair.io_lcg = <interf.xt_lcg_random *> interf.xt_allocate_aligned_memory(sizeof(interf.xt_lcg_random), sizeof(void *))
            else:
                interf.free_sub_lcg(qpair.io_qpair.io_lcg)
            memset(qpair.io_qpair.io_lcg, 0, sizeof(interf.xt_lcg_random))
            xt_lcg_init(start=start, stop=stop, step=step, lcg_random=<unsigned long long> qpair.io_qpair.io_lcg, reset_lcg=reset_lcg)
        elif lcg_type == 1:
            if qpair.io_qpair.write_lcg == NULL:
                qpair.io_qpair.write_lcg = <interf.xt_lcg_random *> interf.xt_allocate_aligned_memory(sizeof(interf.xt_lcg_random), sizeof(void *))
                memset(qpair.io_qpair.write_lcg, 0, sizeof(interf.xt_lcg_random))
                xt_lcg_init(start=start, stop=stop, step=step, lcg_random=<unsigned long long> qpair.io_qpair.write_lcg, reset_lcg=reset_lcg)
            else:
                if qpair.io_qpair.write_lcg.offset != start or qpair.io_qpair.write_lcg.max_value != stop or qpair.io_qpair.write_lcg.step != step:
                    interf.free_sub_lcg(qpair.io_qpair.write_lcg)
                    memset(qpair.io_qpair.write_lcg, 0, sizeof(interf.xt_lcg_random))
                    xt_lcg_init(start=start, stop=stop, step=step, lcg_random=<unsigned long long> qpair.io_qpair.write_lcg, reset_lcg=reset_lcg)
                else:
                    if reset_lcg:
                        xt_lcg_init(start=start, stop=stop, step=step, lcg_random=<unsigned long long> qpair.io_qpair.write_lcg, reset_lcg=reset_lcg)
        else:
            if qpair.io_qpair.read_lcg == NULL:
                qpair.io_qpair.read_lcg = <interf.xt_lcg_random *> interf.xt_allocate_aligned_memory(sizeof(interf.xt_lcg_random), sizeof(void *))
                memset(qpair.io_qpair.read_lcg, 0, sizeof(interf.xt_lcg_random))
                xt_lcg_init(start=start, stop=stop, step=step, lcg_random=<unsigned long long> qpair.io_qpair.read_lcg, reset_lcg=reset_lcg)
            else:
                if qpair.io_qpair.read_lcg.offset != start or qpair.io_qpair.read_lcg.max_value != stop or qpair.io_qpair.read_lcg.step != step:
                    interf.free_sub_lcg(qpair.io_qpair.read_lcg)
                    memset(qpair.io_qpair.read_lcg, 0, sizeof(interf.xt_lcg_random))
                    xt_lcg_init(start=start, stop=stop, step=step, lcg_random=<unsigned long long> qpair.io_qpair.read_lcg, reset_lcg=reset_lcg)
                else:
                    if reset_lcg:
                        xt_lcg_init(start=start, stop=stop, step=step, lcg_random=<unsigned long long> qpair.io_qpair.read_lcg, reset_lcg=reset_lcg)
    cpdef send_io_sequences(self, XT_IO_QPAIR qpair, list io_sequences=None, unsigned int psdt=0, bs=8, unsigned int qdepth=1, unsigned long long slba=0,
                            unsigned long long elba=1048576, unsigned long long size=0, unsigned int random_mode=True, unsigned int mix_write=100, unsigned long long runTime=0,
                            list writebuf_list=[], list readbuf_list=[], unsigned int sector_size=512, unsigned int meta_sector_size=0, unsigned int nsid=1, unsigned int pi_type=0,
                            unsigned int timeout=100000, unsigned int checkPass=1, unsigned int aligned=1, unsigned int cdw2=0, unsigned int cdw3=0, unsigned int cdw13=0,
                            unsigned int cdw14=0, unsigned int cdw15=0, unsigned int reap_type=0, unsigned int io_tailer_flag=0, unsigned int io_check_type=1, unsigned int lcg_radom=1,
                            unsigned int reset_lcg = 0):
            cdef unsigned long long _io_size = size if size != 0 else elba - slba + 1
            cdef unsigned long long _aligned = 0xFFFFFFFFFFFFFFFF - (aligned - 1)
            cdef unsigned long long _base_time = runTime * self._admin_qpair.sys_tick_hz if runTime else 0xFFFFFFFFFFFFFFFF
            cdef unsigned long long _io_count = 0
            cdef unsigned long long init_tick = 0
            cdef unsigned long long _write_buffer_index = 0
            cdef unsigned long long _read_buffer_index = 0
            cdef unsigned long long _write_length = 0
            cdef unsigned long long _read_length = 0
            cdef unsigned long long _slba = 0
            cdef unsigned long long _read_slba = slba
            cdef unsigned long long _write_slba = slba
            cdef unsigned long long write_count = 0
            cdef unsigned long long __write_count = 0
            cdef unsigned long long read_count = 0
            cdef unsigned long long __read_count = 0
            cdef unsigned long long next_io_type = 0
            cdef unsigned long long _mark = (elba - slba  + 1)
            cdef unsigned long long timeout_tick = self.sys_tick_us * timeout
            cdef unsigned int * next_bs_list = NULL
            cdef unsigned int _mark_pow = 0
            cdef unsigned int next_bs_index = 0
            cdef unsigned int _bs_count = 0
            cdef list _io_sequences
            cdef XT_BUFFER _xt_buf
            _write_length = len(writebuf_list) if writebuf_list is not None else 0
            _read_length = len(readbuf_list) if readbuf_list is not None else 0
            qpair.io_qpair.current_iodepth_count = qdepth
            if io_check_type > 1 and not (io_check_type & 0x10):
                assert False, self.logger.error("in send_io_sequences, io check type expect with io tailer(0x10), actual is %s"%io_check_type)
            qpair.io_qpair.io_check_type = io_check_type
            self.xt_io_qpair_nsid_check(qpair, nsid)
            if writebuf_list:
                for _xt_buf in writebuf_list:
                    _xt_buf.meta_data_change(meta_sector_size=meta_sector_size, pi_type=pi_type, sector_size=sector_size)
            if io_sequences is not None:
                self._send_io_sequences(qpair, io_sequences, psdt=psdt, qdepth=qdepth, writebuf_list=writebuf_list, readbuf_list=readbuf_list, timeout_tick=timeout_tick, nsid=nsid)
            else:
                if random_mode and lcg_radom:
                    self.init_lcg(qpair=qpair, start=slba, stop=elba, step=bs, lcg_type=1, reset_lcg=reset_lcg)
                    self.init_lcg(qpair=qpair, start=slba, stop=elba, step=bs, lcg_type=2, reset_lcg=reset_lcg)
                _bs_count = qpair.io_qpair.write_lcg.sub_m_modulus
                next_bs_list = qpair.io_qpair.write_lcg.sub_step_arrays
                if mix_write > 0:
                    write_count = self.__io_count_calculate(bs, _io_size)
                    read_count = int(write_count * (100 - mix_write) / mix_write)
                else:
                    read_count = self.__io_count_calculate(bs, _io_size)
                _io_size = write_count + read_count
                self.init_lcg(qpair=qpair, start=0, stop=_io_size-1, step=1, lcg_type=0)
                init_tick = interf.get_system_ticks()
                while True:
                    if runTime:
                        if interf.get_system_ticks() - init_tick > _base_time:
                            break
                    else:
                        if _io_count >= _io_size:
                            break
                    next_io_type = interf.lcg_next_start(qpair.io_qpair.io_lcg)
                    io_u = interf.xt_prepare_io_unit(self._admin_qpair, qpair.io_qpair)
                    memset(io_u, 0, self.io_unit_clear_size)
                    io_u.start_time = interf.get_system_ticks()
                    if random_mode:  # random write command, maybe have read commands
                        if lcg_radom:
                            if next_io_type < write_count:
                                _slba = interf.lcg_next_start(qpair.io_qpair.write_lcg)
                                next_bs_index = qpair.io_qpair.write_lcg.sub_next
                                __write_count += 1
                            else:
                                _slba = interf.lcg_next_start(qpair.io_qpair.read_lcg)
                                next_bs_index = qpair.io_qpair.read_lcg.sub_next
                                __read_count += 1
                        else:
                            _slba = interf.rand64()
                            _slba = (_slba % _mark + slba) & _aligned
                        if _slba + next_bs_list[next_bs_index] - 1 > elba:
                            _slba = elba - next_bs_list[next_bs_index] + 1
                    else:  # sequential write command, maybe have read commands
                        if next_io_type < write_count:
                            _slba = _write_slba
                            if _write_slba + next_bs_list[next_bs_index] - 1 < elba:
                                _write_slba = (_write_slba + next_bs_list[next_bs_index])
                            else:
                                _write_slba = slba
                        else:
                            _slba = _read_slba
                            if _read_slba + next_bs_list[next_bs_index] - 1 < elba:
                                _read_slba = (_read_slba + next_bs_list[next_bs_index])
                            else:
                                _read_slba = slba
                    if next_io_type < write_count:
                        _xt_buf = writebuf_list[_write_buffer_index]
                        _write_buffer_index += 1
                        if _write_buffer_index >= _write_length:
                            _write_buffer_index = 0
                        io_u.opc = 1
                        io_u.io_tailer_flag = io_tailer_flag
                    else:
                        _xt_buf = readbuf_list[_read_buffer_index]
                        io_u.opc = 2
                        _read_buffer_index += 1
                        if _read_buffer_index >= _read_length:
                            _read_buffer_index = 0
                    buf_size = (sector_size + meta_sector_size) * next_bs_list[next_bs_index]
                    _buf = &_xt_buf._buffer_instance
                    io_u.flags = ((psdt & 0x3) << 6)
                    io_u.nsid = nsid
                    io_u.cdw2 = cdw2
                    io_u.cdw3 = cdw3
                    io_u.cdw10 = _slba & 0xffffffff
                    io_u.cdw11 = (_slba >> 32) & 0xffffffff
                    io_u.cdw12 = next_bs_list[next_bs_index] - 1
                    io_u.cdw13 = cdw13
                    io_u.cdw14 = cdw14
                    io_u.cdw15 = cdw15
                    io_u.sector_size = sector_size
                    io_u.meta_sector_size = meta_sector_size
                    io_u.io_status_code_expected = 0
                    io_u.io_status_code_type_expected = 0
                    io_u.qpair_info = qpair.io_qpair
                    io_u.completed_cmds_u_ring = qpair.io_qpair.completed_cmds_u_ring
                    io_u.io_buffer = _buf
                    # self.logger.debug("opc: %s flags: %s nsid: %s, cdw2: %s cdw3:%s cdw10:%s cdw11:%s cdw12:%s cdw13:%s cdw14:%s cdw15 %s"%(io_u.opc, io_u.flags, io_u.nsid, io_u.cdw2, io_u.cdw3, io_u.cdw10, io_u.cdw11, io_u.cdw12, io_u.cdw13, io_u.cdw14, io_u.cdw15))
                    # self.logger.debug("_bs_count: %s next_bs_index:%s sub_m_modulus %s"%(_bs_count, next_bs_index, qpair.io_qpair.read_lcg.sub_m_modulus))
                    interf.xt_submit_io_cmd(self._admin_qpair, qpair.io_qpair, _buf, io_u, buf_size, next_bs_list[next_bs_index])
                    _io_count += 1
                    if _io_count > _io_size:
                        qpair.io_qpair.io_lcg.c_increment = (qpair.io_qpair.io_lcg.c_increment + 2) & qpair.io_qpair.io_lcg.m_mark
                        if runTime:
                            _io_count = 0
                    if __write_count and __write_count >= write_count:
                        if reset_lcg:
                            qpair.io_qpair.write_lcg.c_increment = (qpair.io_qpair.write_lcg.c_increment + 2) & qpair.io_qpair.write_lcg.m_mark
                            __write_count = 0
                    if __read_count and __read_count >= read_count:
                        if reset_lcg:
                            qpair.io_qpair.read_lcg.c_increment = (qpair.io_qpair.read_lcg.c_increment + 2) & qpair.io_qpair.read_lcg.m_mark
                        __read_count = 0
                    next_bs_index += 1
                    if next_bs_index >= _bs_count:
                        next_bs_index = 0
                interf.xt_wait_qpair_all_submission_io_completion(self._admin_qpair, qpair.io_qpair)
            self.logger.debug("expect io count %s io count %s write count %s read count %s total_io_size %s total_read_size %s total_write_size %s total_iops_count %s"%(_io_size,
                              _io_count, __write_count, __read_count, interf.get_total_io_size(), interf.get_total_read_size(), interf.get_total_write_size(), interf.get_total_iops_count()))

    cpdef send_random_write_full(self, XT_IO_QPAIR qpair, unsigned int psdt=0, unsigned int bs=8, unsigned int qdepth=1, unsigned long long slba=0, unsigned long long elba=1048576,
                                 unsigned int sector_size=512, unsigned int meta_sector_size=0, unsigned int nsid=1, unsigned int timeout=100000, unsigned int checkPass=1, unsigned int pi_type=0,
                                 list writebuf_list=[], unsigned int rand_reset=0, unsigned int reap_type=0, unsigned int io_tailer_flag=0, unsigned int cdw2=0, unsigned int cdw3=0,
                                 unsigned int cdw13=0, unsigned int cdw14=0, unsigned int cdw15=0, unsigned int reset_lcg=0):
        cdef interf.cmds_u * io_u = NULL
        cdef interf.xt_buffer * _buf = NULL
        cdef unsigned long long _write_buffer_index = 0
        cdef unsigned long long _write_slba = slba
        cdef unsigned int _write_length = len(writebuf_list) if writebuf_list is not None else 0
        cdef unsigned int io_mode = (0x1 | (0x001 << 1)) if io_tailer_flag else (0x1 | (0x000 << 1))
        cdef unsigned long long timeout_tick = self.sys_tick_us * timeout
        cdef unsigned long long loop_cnt = (elba - slba + 1) // bs
        cdef unsigned long long loop_number = 0
        cdef XT_BUFFER _xt_buf
        self.init_lcg(qpair=qpair, start=slba, stop=elba, step=bs, lcg_type=1, reset_lcg=reset_lcg)
        qdepth = self.check_io_qdepth(qdepth, qpair, writebuf_list, reap_type, io_mode)
        for _xt_buf in writebuf_list:
            _xt_buf.meta_data_change(meta_sector_size=meta_sector_size, pi_type=pi_type, sector_size=sector_size)
        self.xt_io_qpair_nsid_check(qpair, nsid)
        self.logger.info("send write commands with slba:0x%x elba:0x%x lbacnt: 0x%x loop count %s qdepth %s qinfo->completed_check_index %s"%(
                          slba, elba, bs, loop_cnt, qdepth, qpair.io_qpair.completed_check_index))
        for loop_number in range(loop_cnt):
            if loop_number == 0:
                _write_slba = xt_lcg_first(slba, elba, bs, lcg_random=<unsigned long long> qpair.io_qpair.write_lcg)
            else:
                _write_slba = interf.lcg_next_start(qpair.io_qpair.write_lcg)
            if _write_buffer_index >= _write_length:
                _write_buffer_index = 0
            _xt_buf = writebuf_list[_write_buffer_index]
            _buf = &_xt_buf._buffer_instance
            io_u = interf.xt_prepare_io_unit(self._admin_qpair, qpair.io_qpair)
            memset(io_u, 0, self.io_unit_clear_size)
            buf_size = (sector_size + meta_sector_size) * bs
            io_u.start_time = interf.get_system_ticks()
            io_u.opc = 1
            io_u.flags = ((psdt & 0x3) << 6)
            io_u.nsid = nsid
            io_u.cdw2 = cdw2
            io_u.cdw3 = cdw3
            io_u.cdw10 = _write_slba & 0xffffffff
            io_u.cdw11 = (_write_slba >> 32) & 0xffffffff
            io_u.cdw12 = bs - 1
            io_u.cdw13 = cdw13
            io_u.cdw14 = cdw14
            io_u.cdw15 = cdw15
            io_u.sector_size = sector_size
            io_u.meta_sector_size = meta_sector_size
            io_u.io_status_code_expected = 0
            io_u.io_status_code_type_expected = 0
            io_u.qpair_info = qpair.io_qpair
            io_u.completed_cmds_u_ring = qpair.io_qpair.completed_cmds_u_ring
            # self.fill_io_unit(qpair=qpair, io_u=io_u, opc=1, psdt=psdt, nsid=nsid, slba=_write_slba, cdw12=bs - 1,
            #                   sector_size=sector_size, meta_sector_size=meta_sector_size,
            #                   io_status_code_expected=0, io_status_code_type_expected=0,
            #                   cdw2=cdw2, cdw3=cdw3,
            #                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15)
            io_u.io_buffer = _buf
            interf.xt_submit_io_cmd(self._admin_qpair, qpair.io_qpair, _buf, io_u, buf_size, bs)
            _write_buffer_index += 1
        else:
            if loop_cnt * bs != (elba - slba + 1):
                _write_slba = slba + loop_cnt * bs
                bs = (elba - _write_slba + 1)
                _xt_buf = writebuf_list[_write_buffer_index]
                _buf = &_xt_buf._buffer_instance
                io_u = interf.xt_prepare_io_unit(self._admin_qpair, qpair.io_qpair)
                memset(io_u, 0, self.io_unit_clear_size)
                buf_size = (sector_size + meta_sector_size) * bs
                io_u.opc = 1
                io_u.flags = ((psdt & 0x3) << 6)
                io_u.nsid = nsid
                io_u.cdw2 = cdw2
                io_u.cdw3 = cdw3
                io_u.cdw10 = _write_slba & 0xffffffff
                io_u.cdw11 = (_write_slba >> 32) & 0xffffffff
                io_u.cdw12 = bs - 1
                io_u.cdw13 = cdw13
                io_u.cdw14 = cdw14
                io_u.cdw15 = cdw15
                io_u.sector_size = sector_size
                io_u.meta_sector_size = meta_sector_size
                io_u.io_status_code_expected = 0
                io_u.io_status_code_type_expected = 0
                io_u.qpair_info = qpair.io_qpair
                io_u.completed_cmds_u_ring = qpair.io_qpair.completed_cmds_u_ring
                # self.fill_io_unit(qpair=qpair, io_u=io_u, opc=1, psdt=psdt, nsid=nsid, slba=_write_slba, cdw12=bs - 1,
                #                   sector_size=sector_size, meta_sector_size=meta_sector_size,
                #                   io_status_code_expected=0, io_status_code_type_expected=0,
                #                   cdw2=cdw2, cdw3=cdw3,
                #                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15)
                io_u.io_buffer = _buf
                interf.xt_submit_io_cmd(self._admin_qpair, qpair.io_qpair, _buf, io_u, buf_size, bs)
        interf.xt_wait_qpair_all_submission_io_completion(self._admin_qpair, qpair.io_qpair)

    cpdef send_random_read_full(self, XT_IO_QPAIR qpair, unsigned int psdt=0, unsigned int bs=8, unsigned int qdepth=1, unsigned long long slba=0, unsigned long long elba=1048576,
                                unsigned int sector_size=512, unsigned int meta_sector_size=0, unsigned int nsid=1, unsigned int timeout=100000, unsigned int checkPass=1, unsigned int pi_type=0,
                                list writebuf_list=[], list readbuf_list=[], unsigned int rand_reset=0, unsigned int reap_type=0, unsigned int io_check_type=1, unsigned int cdw2=0,
                                unsigned int cdw3=0, unsigned int cdw13=0, unsigned int cdw14=0, unsigned int cdw15=0, unsigned int reset_lcg=0):
        cdef interf.cmds_u * io_u = NULL
        cdef interf.xt_buffer * _buf = NULL
        cdef unsigned long long _write_buffer_index = 0
        cdef unsigned long long _read_buffer_index = 0
        cdef unsigned long long _read_slba = slba
        cdef unsigned int _write_length = len(writebuf_list) if writebuf_list is not None else 0
        cdef unsigned int _read_length = len(readbuf_list) if readbuf_list is not None else 0
        cdef unsigned int io_mode = (0x0 | (0x010 << 1)) if io_check_type else (0x0 | (0x000 << 1))
        cdef unsigned long long timeout_tick = self.sys_tick_us * timeout
        cdef unsigned long long loop_cnt = (elba - slba + 1) // bs
        cdef unsigned long long loop_number = 0
        cdef XT_BUFFER _xt_buf
        qdepth = self.check_io_qdepth(qdepth, qpair, readbuf_list, reap_type, io_mode)
        self.logger.info("send read commands with slba:0x%x elba:0x%x lbacnt: 0x%x loop count %s qdepth %s qinfo->completed_check_index %s"%(slba, elba, bs, loop_cnt, qdepth,
                          qpair.io_qpair.completed_check_index))
        self.init_lcg(qpair=qpair, start=slba, stop=elba, step=bs, lcg_type=2, reset_lcg=reset_lcg)
        self.xt_io_qpair_nsid_check(qpair, nsid)
        for loop_number in range(loop_cnt):
            if loop_number == 0:
                _read_slba = xt_lcg_first(slba, elba, bs, lcg_random=<unsigned long long> qpair.io_qpair.read_lcg)
            else:
                _read_slba = interf.lcg_next_start(qpair.io_qpair.read_lcg)
            _xt_buf = readbuf_list[_read_buffer_index]
            _buf = &_xt_buf._buffer_instance
            io_u = interf.xt_prepare_io_unit(self._admin_qpair, qpair.io_qpair)
            memset(io_u, 0, self.io_unit_clear_size)
            buf_size = (sector_size + meta_sector_size) * bs
            io_u.opc = 2
            io_u.flags = ((psdt & 0x3) << 6)
            io_u.nsid = nsid
            io_u.cdw2 = cdw2
            io_u.cdw3 = cdw3
            io_u.cdw10 = _read_slba & 0xffffffff
            io_u.cdw11 = (_read_slba >> 32) & 0xffffffff
            io_u.cdw12 = bs - 1
            io_u.cdw13 = cdw13
            io_u.cdw14 = cdw14
            io_u.cdw15 = cdw15
            io_u.sector_size = sector_size
            io_u.meta_sector_size = meta_sector_size
            io_u.io_status_code_expected = 0
            io_u.io_status_code_type_expected = 0
            io_u.qpair_info = qpair.io_qpair
            io_u.completed_cmds_u_ring = qpair.io_qpair.completed_cmds_u_ring
            # self.fill_io_unit(qpair=qpair, io_u=io_u, opc=2, psdt=psdt, nsid=nsid, slba=_read_slba, cdw12=bs - 1, sector_size=sector_size, meta_sector_size=meta_sector_size,
            #                   io_status_code_expected=0, io_status_code_type_expected=0, cdw2=cdw2, cdw3=cdw3, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15)
            io_u.io_buffer = _buf
            io_u.excepted_write_check = 1
            _xt_buf = writebuf_list[_write_buffer_index]
            io_u.excepted_write_buffer_index = _xt_buf._buffer_instance.buf_index
            _write_buffer_index += 1
            _read_buffer_index += 1
            if _write_buffer_index >= _write_length:
                _write_buffer_index = 0
            if _read_buffer_index >= _read_length:
                _read_buffer_index = 0
            interf.xt_submit_io_cmd(self._admin_qpair, qpair.io_qpair, _buf, io_u, buf_size, bs)
        else:
            if loop_cnt * bs != (elba - slba + 1):
                _write_slba = slba + loop_cnt * bs
                bs = (elba - _write_slba + 1)
                _xt_buf = readbuf_list[_read_buffer_index]
                _buf = &_xt_buf._buffer_instance
                io_u = interf.xt_prepare_io_unit(self._admin_qpair, qpair.io_qpair)
                memset(io_u, 0, self.io_unit_clear_size)
                buf_size = (sector_size + meta_sector_size) * bs
                io_u.opc = 2
                io_u.flags = ((psdt & 0x3) << 6)
                io_u.nsid = nsid
                io_u.cdw2 = cdw2
                io_u.cdw3 = cdw3
                io_u.cdw10 = _read_slba & 0xffffffff
                io_u.cdw11 = (_read_slba >> 32) & 0xffffffff
                io_u.cdw12 = bs - 1
                io_u.cdw13 = cdw13
                io_u.cdw14 = cdw14
                io_u.cdw15 = cdw15
                io_u.sector_size = sector_size
                io_u.meta_sector_size = meta_sector_size
                io_u.io_status_code_expected = 0
                io_u.io_status_code_type_expected = 0
                io_u.qpair_info = qpair.io_qpair
                io_u.completed_cmds_u_ring = qpair.io_qpair.completed_cmds_u_ring
                # self.fill_io_unit(qpair=qpair, io_u=io_u, opc=2, psdt=psdt, nsid=nsid, slba=_write_slba, cdw12=bs - 1, sector_size=sector_size, meta_sector_size=meta_sector_size,
                #                   io_status_code_expected=0, io_status_code_type_expected=0, cdw2=cdw2, cdw3=cdw3, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15)
                io_u.io_buffer = _buf
                io_u.excepted_write_check = 1
                _xt_buf = writebuf_list[_write_buffer_index]
                io_u.excepted_write_buffer_index = _xt_buf._buffer_instance.buf_index
                interf.xt_submit_io_cmd(self._admin_qpair, qpair.io_qpair, _buf, io_u, buf_size, bs)
        interf.xt_wait_qpair_all_submission_io_completion(self._admin_qpair, qpair.io_qpair)

    cpdef enable_io_histogram(self):
        self._admin_qpair.histogram_flag = 1
        assert self._admin_qpair.histogram_flag == 1, self.logger.error("Enable io_histogram failed")

    cpdef disable_io_histogram(self):
        self._admin_qpair.histogram_flag = 0
        assert self._admin_qpair.histogram_flag == 0, self.logger.error("Disable io_histogram failed")

    cpdef print_io_histogram(self, unsigned int latency_summary=1, unsigned int latency_histogram=1):
        if self._admin_qpair.histogram_flag:
            interf.print_latency_histogram(self._admin_qpair, latency_summary, latency_histogram)
        else:
            self.logger.error("histogram not recover, please call enable_io_histogram")

    cpdef reset_io_histogram(self):
        interf.xt_io_histogram_reset(self._admin_qpair)

    def __getitem__(self, index):
        """access pcie config space by bytes."""
        if self.driver.nvme_engine_flag or self.driver.spdk_engine_flag or self.driver.simulator_engine_flag:
            if isinstance(index, slice):
                return [self[ii] for ii in range(index.stop)[index]]
            elif isinstance(index, int):
                return interf.xt_nvme_register_read8(self._admin_qpair, index)
        else:
            self.logger.error("%s don't support to get nvme register and return -1"%self.driver.engine_opt_name)
            return -1

    def __setitem__(self, index, value):
        """set pcie config space by bytes."""
        if self.driver.nvme_engine_flag or self.driver.spdk_engine_flag or self.driver.simulator_engine_flag:
            if isinstance(index, int):
                interf.xt_nvme_register_write8(self._admin_qpair, index, value)
        else:
            self.logger.error("%s don't support to set nvme register"%self.driver.engine_opt_name)

    cpdef get_nvme_register(self, offset, bytes_count = 1):
        if self.driver.nvme_engine_flag or self.driver.spdk_engine_flag or self.driver.simulator_engine_flag:
            if bytes_count == 1:
                return interf.xt_nvme_register_read8(self._admin_qpair, offset)
            elif bytes_count == 2:
                return interf.xt_nvme_register_read16(self._admin_qpair, offset)
            elif bytes_count == 4:
                return interf.xt_nvme_register_read32(self._admin_qpair, offset)
            elif bytes_count == 8:
                return interf.xt_nvme_register_read64(self._admin_qpair, offset)
            else:
                self.logger.error("get a invalid bytes_count %s"%(bytes_count))
        else:
            self.logger.error("%s don't support to get nvme register"%self.driver.engine_opt_name)

    cpdef set_nvme_register(self, offset, value, bytes_count=1):
        if self.driver.nvme_engine_flag or self.driver.spdk_engine_flag or self.driver.simulator_engine_flag:
            if bytes_count == 1:
                return interf.xt_nvme_register_write8(self._admin_qpair, offset, value)
            elif bytes_count == 2:
                return interf.xt_nvme_register_write16(self._admin_qpair, offset, value)
            elif bytes_count == 4:
                return interf.xt_nvme_register_write32(self._admin_qpair, offset, value)
            elif bytes_count == 8:
                return interf.xt_nvme_register_write64(self._admin_qpair, offset, value)
            else:
                self.logger.error("set a invalid bytes_count %s"%(bytes_count))
        else:
            self.logger.error("%s don't support to set nvme register"%self.driver.engine_opt_name)

    cpdef shutdown(self, abrupt=False, unsigned long long timeout=100000, check_status=True):
        cdef unsigned long long init_tick = 0
        cdef unsigned long long timeout_tick = timeout * self.sys_tick_us
        if self.driver.nvme_engine_flag or self.driver.spdk_engine_flag or self.driver.simulator_engine_flag:
            cc = self.get_nvme_register(0x14, 4)
            if abrupt:
                cc = cc | 0x8000
            else:
                cc = cc | 0x4000
            self.set_nvme_register(0x14, cc, bytes_count=4)
            get_cc = self.get_nvme_register(0x14, 4)
            assert get_cc == cc, self.logger.error("set shutdown expect %s actual %s" % (cc, get_cc))
            if not check_status:
                return
            init_tick = interf.get_system_ticks()
            while interf.get_system_ticks() - init_tick < timeout_tick:
                if (self[0x1c] & 0xc) == 0x8:
                    self.logger.error("csts.shst is %s"%(self[0x1c]))
                    break
            else:
                assert False, self.logger.error("check csts.shst timeout %sus"%timeout)
        elif "null" in self.driver.engine_opt_name or "sata" in self.driver.engine_opt_name or "sde" in self.driver.engine_opt_name:
            self.logger.info("engined %s don't support shutdown"%(self.driver.engine_opt_name))
        else:
            assert False, self.logger.error("engined %s shutdown is to be supplemented" % (self.driver.engine_opt_name))

    cpdef device_ready_check(self, timeout=5000000):
        cdef unsigned long long init_tick = 0
        cdef unsigned long long timeout_tick = timeout * self.sys_tick_us
        if self.driver.nvme_engine_flag or self.driver.spdk_engine_flag or self.driver.simulator_engine_flag:
            init_tick = interf.get_system_ticks()
            while interf.get_system_ticks() - init_tick < timeout_tick:
                if os.path.exists("/sys/bus/pci/devices/%s" % self.driver.pcie_addr):
                    break
                interf.xt_delay_us(10)
            else:
                assert False, self.logger.error("check pcie path timeout %sus"%timeout)
            init_tick = interf.get_system_ticks()
            while interf.get_system_ticks() - init_tick < timeout_tick:
                if (self[0x1c] & 0x1):
                    self.logger.error("cc is %s" % (self.get_nvme_register(0x1c, 4)))
                    break
            else:
                assert False, self.logger.error("check csts.ready timeout %sus"%timeout)
        elif "null" in self.driver.engine_opt_name or "sata" in self.driver.engine_opt_name or "sde" in self.driver.engine_opt_name:
            self.logger.info("engined %s don't support ready check"%(self.driver.engine_opt_name))
        else:
            assert False, self.logger.error("engined %s ready check is to be supplemented" %(self.driver.engine_opt_name))

    cpdef pcie_reset(self, timeout=5000000, pci_path_check=True):
        cdef unsigned long long init_tick = 0
        cdef unsigned long long timeout_tick = timeout * self.sys_tick_us
        if self.driver.nvme_engine_flag or self.driver.spdk_engine_flag:
            pci_path = "/sys/bus/pci/devices/%s" % self.driver.pcie_addr
            init_tick = interf.get_system_ticks()
            while pci_path_check and interf.get_system_ticks() - init_tick < timeout_tick:
                if os.path.exists(pci_path):
                    break
                interf.xt_delay_us(10)
            else:
                assert False, self.logger.error("check pcie path timeout %sus"%timeout)
            init_tick = interf.get_system_ticks()
            remove_cmdline = "echo 1 > %s/remove" %pci_path
            if os.system(remove_cmdline):
                self.logger.error("remove pcie failed")
            rescan_cmdline = "echo 1 > /sys/bus/pci/rescan"
            if os.system(remove_cmdline):
                self.logger.error("rescan pcie failed")
            while interf.get_system_ticks() - init_tick < timeout_tick:
                if os.path.exists(pci_path):
                    break
                interf.xt_delay_us(10)
            else:
                assert False, self.logger.error("check pcie path %s timeout %sus"%(timeout))
            init_tick = interf.get_system_ticks()
            while interf.get_system_ticks() - init_tick < timeout_tick:
                if (self[0x1c] & 0x1):
                    self.logger.error("cc is %s" % (self.get_nvme_register(0x1c, 4)))
                    break
            else:
                assert False, self.logger.error("check csts.ready timeout %sus"%timeout)
        elif "null" in self.driver.engine_opt_name or "sata" in self.driver.engine_opt_name or "sde" in self.driver.engine_opt_name or self.driver.simulator_engine_flag:
            self.logger.info("engined %s don't support pcie reset" % (self.driver.engine_opt_name))
        else:
            assert False, self.logger.error("engined %s pcie reset is to be supplemented" % (self.driver.engine_opt_name))

    cpdef controller_reset(self, timeout=5000000, cr_type=0, pci_path_check=True):
        cdef unsigned long long init_tick = 0
        cdef unsigned long long timeout_tick = timeout * self.sys_tick_us
        if self.driver.nvme_engine_flag or self.driver.spdk_engine_flag or self.driver.simulator_engine_flag:
            pci_path = "/sys/bus/pci/devices/%s" % self.driver.pcie_addr
            init_tick = interf.get_system_ticks()
            while pci_path_check and interf.get_system_ticks() - init_tick < timeout_tick:
                if os.path.exists(pci_path):
                    break
                interf.xt_delay_us(10)
            else:
                assert False, self.logger.error("check pcie path timeout %sus"%timeout)
            if cr_type == 0 and self.driver.nvme_engine_flag and "spdk_nvme" not in self.driver.engine_opt_name:
                ret = interf.xt_nvme_device_reset(self._admin_qpair)
                assert ret == 0, self.logger.error("reset failed by ioctrl ret %s" % ret)
            else:
                cc = self.get_nvme_register(offset=0x14, bytes_count=4)
                self.logger.info("init cc.en = %s, set cc.en to 0" %(cc & 0x1))
                assert cc & 0x1, self.logger.error("cc.en is 1 cc %s"%cc)
                cc = cc & 0xFFFFFFFE
                self.set_nvme_register(offset=0x14, value=cc, bytes_count=4)
                cc = self.get_nvme_register(offset=0x14, bytes_count=4)
                assert cc & 0x1 == 0, self.logger.error("disable cc.en expect cc.en is 0 cc %s"%cc)
                self.set_nvme_register(offset=0x14, value=cc | 0x1, bytes_count=4)
                cc = self.get_nvme_register(offset=0x14, bytes_count=4)
                assert cc & 0x1 == 1, self.logger.error("enable cc.en expect cc.en is 1 cc %s"%cc)
            init_tick = interf.get_system_ticks()
            while interf.get_system_ticks() - init_tick < timeout_tick:
                if (self[0x1c] & 0x1):
                    self.logger.error("cc is %s" % (self.get_nvme_register(0x1c, 4)))
                    break
            else:
                assert False, self.logger.error("check csts.ready timeout %sus"%timeout)
        elif "null" in self.driver.engine_opt_name or "sata" in self.driver.engine_opt_name or "sde" in self.driver.engine_opt_name:
            self.logger.info("engined %s don't support pcie reset" % (self.driver.engine_opt_name))
        else:
            assert False, self.logger.error("engined %s pcie reset is to be supplemented" % (self.driver.engine_opt_name))

    cpdef function_level_reset(self, timeout=5000000, flr_type=0, pci_path_check=True):
        cdef unsigned long long init_tick = 0
        cdef unsigned long long timeout_tick = timeout * self.sys_tick_us
        if self.driver.nvme_engine_flag or self.driver.spdk_engine_flag:
            pci_path = "/sys/bus/pci/devices/%s" % self.driver.pcie_addr
            init_tick = interf.get_system_ticks()
            while pci_path_check and interf.get_system_ticks() - init_tick < timeout_tick:
                if os.path.exists(pci_path):
                    break
                interf.xt_delay_us(10)
            else:
                assert False, self.logger.error("check pcie path timeout %sus"%timeout)
            if flr_type == 0:
                reset_pcie_cmdline = "echo 1 > %s/reset" %pci_path
                if os.system(reset_pcie_cmdline):
                    self.logger.error("reset pcie failed")
            else:
                cap_exp = self.driver.get_pcie_header_offset(offset=0x8, bytes_count=2)
                cap_exp = 0x8000 | cap_exp
                self.driver.set_pcie_header_offset(offset=0x8, value= cap_exp, bytes_count=2)
                get_cap_exp = self.driver.get_pcie_header_offset(offset=0x8, bytes_count=2)
                assert get_cap_exp == cap_exp, self.logger.error("set pcie link disable failed expect %s actual %s" %(cap_exp, get_cap_exp))
            self.pcie_reset(timeout=timeout, pci_path_check=False)
        elif "null" in self.driver.engine_opt_name or "sata" in self.driver.engine_opt_name or "sde" in self.driver.engine_opt_name or self.driver.simulator_engine_flag:
            self.logger.info("engined %s don't support pcie reset" % (self.driver.engine_opt_name))
        else:
            assert False, self.logger.error("engined %s pcie reset is to be supplemented" % (self.driver.engine_opt_name))

    cpdef subsystem_reset(self, timeout=5000000, timesleep=0, nssr_type=0):
        cdef unsigned long long init_tick = 0
        cdef unsigned long long timeout_tick = timeout * self.sys_tick_us
        cdef int ret = 0
        if self.driver.nvme_engine_flag or self.driver.spdk_engine_flag or self.driver.simulator_engine_flag:
            cap = self.get_nvme_register(offset=0, bytes_count=8)
            if cap & 0x1000000000:
                if self.driver.nvme_engine_flag and nssr_type == 0 and "spdk_nvme" not in self.driver.engine_opt_name:
                    ret = interf.xt_nvme_device_subsystem_reset(self._admin_qpair)
                    assert ret == 0, self.logger.error("subsystem reset failed by ioctrl ret %s"%ret)
                    time.sleep(timesleep)
                    self.pcie_reset(timeout=timeout, pci_path_check=False)
                else:
                    nssr = self.get_nvme_register(offset=0x20, bytes_count=4)
                    self.logger.info("init nssr = %s, set nssr to 0x4E564D65" % (nssr))
                    self.set_nvme_register(offset=0x20, value=0x4E564D65, bytes_count=4)
                    nssr = self.get_nvme_register(offset=0x20, bytes_count=4)
                    assert nssr == 0x4E564D65, self.logger.error("set nssr failed expect 0x4E564D65 actual %s"%nssr)
                    self.pcie_reset(timeout=timeout, pci_path_check=False)
            else:
                self.logger.error("device not support subsystem reset")
        elif "null" in self.driver.engine_opt_name or "sata" in self.driver.engine_opt_name or "sde" in self.driver.engine_opt_name:
            self.logger.info("engined %s don't support pcie reset" % (self.driver.engine_opt_name))
        else:
            assert False, self.logger.error("engined %s pcie reset is to be supplemented" % (self.driver.engine_opt_name))

    cpdef link_reset(self, timeout=5000000, pci_path_check=True):
        cdef unsigned long long init_tick = 0
        cdef unsigned long long timeout_tick = timeout * self.sys_tick_us
        if self.driver.nvme_engine_flag or self.driver.spdk_engine_flag:
            pci_path = "/sys/bus/pci/devices/%s" % self.driver.pcie_addr
            init_tick = interf.get_system_ticks()
            while pci_path_check and interf.get_system_ticks() - init_tick < timeout_tick:
                if os.path.exists("/sys/bus/pci/devices/%s" % self.driver.pcie_addr):
                    break
                interf.xt_delay_us(10)
            else:
                assert False, self.logger.error("check pcie path timeout %s"%timeout)
            dev_link_port = os.readlink(pci_path).split(os.path.sep)[-2]
            if 'pci' in dev_link_port:
                dev_link_port = dev_link_port[3:] + ":00.0"
            get_pci_cmdline = "sudo setpci -s %s CAP_EXP+10.b"%dev_link_port
            cap_exp_str = os.popen(get_pci_cmdline).read().rstrip()
            cap_exp_hex = hex(int(cap_exp_str, 16) | 0x10)  # link disable
            set_pci_cmdline = get_pci_cmdline + "=%s"%cap_exp_hex
            if os.system(set_pci_cmdline):
                self.logger.error("%s failed"%set_pci_cmdline)
            cap_exp_str = os.popen(get_pci_cmdline).read().rstrip()
            assert cap_exp_str in  cap_exp_hex, self.logger.error("set pcie failed expect %s actual %s" %(cap_exp_hex, cap_exp_str))
            self.pcie_reset(timeout=timeout, pci_path_check=False)
        elif "null" in self.driver.engine_opt_name or "sata" in self.driver.engine_opt_name or "sde" in self.driver.engine_opt_name or self.driver.simulator_engine_flag:
            self.logger.info("engined %s don't support pcie reset" % (self.driver.engine_opt_name))
        else:
            assert False, self.logger.error("engined %s pcie reset is to be supplemented" % (self.driver.engine_opt_name))

    cpdef device_fini(self,):
        return interf.xt_device_fini(self._admin_qpair)

    cpdef device_reinit(self,):
        return interf.xt_device_init(self._admin_qpair)

    cpdef device_detach(self,):
        interf.xt_device_destory(self._admin_qpair)

