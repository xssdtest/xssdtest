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
import re
from xt_platform import xt_interface as xt
class Buffer(object):
    """
    A utility class for managing buffer creation, comparison, and retrieval operations.

    This class provides methods to create, compare, and fetch buffers used in test scenarios,
    particularly useful for I/O testing with various data patterns and compression levels.

    Attributes:
        logger (Logger): Instance of a logging object used throughout the class.
        write_buffer_list (list): List of pre-defined write buffers retrieved from `xt.get_init_write_buffer_list()`.
    """

    def __init__(self, logger):
        """
        Initializes the Buffer instance with a logger.

        Parameters:
            logger (Logger): Logger instance for logging messages during buffer operations.
        """
        self.logger = logger

    @property
    def write_buffer_list(self):
        """
        Retrieves the list of initialized write buffers.

        Returns:
            list: A list of write buffer names or identifiers.
        """
        return xt.get_init_write_buffer_list()

    def create_buffer(self, buf_length, buf_align=512, buf_type=0, alloc_type=None, pi_type=0, mem_init=1, device=None, pattern=None):
        """
        Creates a new buffer based on provided parameters and optionally fills it with a data pattern.

        Parameters:
            buf_length (int): Length of the buffer in bytes.
            buf_align (int): Alignment boundary for the buffer. Default is 512.
            buf_type (int): Type of the buffer. Default is 0.
            alloc_type (int): Optional allocation type.
            pi_type (int): Protection information type. Default is 0.
            mem_init (int): Whether to initialize memory. Default is 1 (initialize).
            device (object): Device context associated with this buffer.
            pattern (str): Pattern name used to fill the buffer if needed.

        Returns:
            object: An initialized buffer object (`XT_BUFFER`).
        """
        buffer = xt.XT_BUFFER(buf_length=buf_length, buf_align=buf_align, buf_type=buf_type, alloc_type=alloc_type, pi_type=pi_type,
                              logger=self.logger, mem_init=mem_init, device=device)
        if pattern is not None:
            buffer.fill_disorder(pattern)
        return buffer

    def create_buffer_list(self, buff_count, buf_length, buf_align=512, buf_type=0, alloc_type=None, pi_type=0, mem_init=1, device=None, patterns=None):
        """
        Creates a list of buffers with optional individual or uniform pattern filling.

        Parameters:
            buff_count (int): Number of buffers to create.
            buf_length (int): Length of each buffer in bytes.
            buf_align (int): Alignment boundary for each buffer. Default is 512.
            buf_type (int): Type of buffer. Default is 0.
            alloc_type (int): Optional allocation type.
            pi_type (int): Protection information type. Default is 0.
            mem_init (int): Whether to initialize memory. Default is 1 (initialize).
            device (object): Device context for buffer creation.
            patterns (list or str): Data pattern(s) to apply. If a list, assigns per buffer;
                                    if a string, applies the same to all.

        Returns:
            list: A list of created buffer objects.
        """
        buffer_list = []
        for i in range(buff_count):
            pattern = patterns[i] if (type(patterns) is list and len(patterns) == buff_count) else patterns
            buffer = self.create_buffer(buf_length, buf_align, buf_type, alloc_type, pi_type, mem_init, device, pattern)
            buffer_list.append(buffer)
        return buffer_list

    def create_admin_buffer(self, buf_length=4096, buf_align=4096, mem_init=1):
        """
        Creates an admin buffer with standard settings.

        Parameters:
            buf_length (int): Length of the admin buffer. Default is 4096.
            buf_align (int): Alignment value. Default is 4096.
            mem_init (int): Whether to initialize memory. Default is 1 (initialize).

        Returns:
            object: The created admin buffer.
        """
        return xt.create_buffer(buf_length, buf_align, 1, 0, 0, self.logger, mem_init)

    def buffer_compare(self, source_buff, target_buff, compare_len=None, miscompare=False, show_diff=False, report_error=True):
        """
        Compares two buffers and reports whether they match or differ.

        Parameters:
            source_buff (object): Source buffer for comparison.
            target_buff (object): Target buffer for comparison.
            compare_len (int): Optional length to limit comparison. Defaults to full buffer length.
            miscompare (bool): If True, expects mismatch and passes when buffers differ.
            show_diff (bool): If True, logs detailed buffer content on mismatch.
            report_error (bool): If True, raises an assertion error on mismatch.

        Returns:
            bool: True if buffers match (or mismatch as expected), False otherwise.
        """
        compare_len = len(source_buff) if compare_len is None else compare_len
        listA = source_buff.get_raw_buf(0, compare_len)
        listB = target_buff.get_raw_buf(0, compare_len)
        data_compare = listA != listB
        result = True if (data_compare and not miscompare) or (not data_compare and miscompare) else False
        if result:
            self.logger.info("### %s Buffer and %s Buffer Compare With miscompare %s is Pass ###!" %
                             (source_buff.get_pattern(), target_buff.get_pattern(), miscompare))
        else:
            if show_diff:
                self.logger.info("----------Data miscompare----------")
                self.logger.info("---------Dump %s Buffer---------" % source_buff.get_pattern())
                source_buff.dump_buf(0, compare_len)
                if miscompare:
                    self.logger.info("---------Dump %s Buffer---------" % target_buff.get_pattern())
                    target_buff.dump_buf(0, compare_len)
        if report_error:
            assert False, self.logger.error("check %s with %s buffer failed, miscompare %s" %
                                           (source_buff.get_pattern(), target_buff.get_pattern(), miscompare))
        return result

    def multi_buffer_compare(self, source_buff, compare_buffs, compare_len=None, miscompare=False, show_diff=False, report_error=True):
        """
        Compares a source buffer against multiple target buffers.

        Parameters:
            source_buff (object): Buffer to compare.
            compare_buffs (list): List of buffers to compare against.
            compare_len (int): Optional length to limit comparison.
            miscompare (bool): If True, expects mismatch and passes when any buffer matches.
            show_diff (bool): If True, dumps buffer contents on mismatch.
            report_error (bool): If True, raises an assertion error on mismatch.

        Returns:
            bool: True if match found (or no match expected), False otherwise.
        """
        compare_len = len(source_buff) if compare_len is None else compare_len
        for target_buff in compare_buffs:
            result = self.buffer_compare(source_buff, target_buff, compare_len, miscompare, show_diff=False, report_error=False)
            if result:
                break
        else:
            if show_diff:
                self.logger.info("----------Data miscompare----------")
                self.logger.info("---------Dump %s Buffer---------" % source_buff.get_pattern())
                source_buff.dump_buf(0, compare_len)
            result = False
        if report_error and not result:
            assert False, self.logger.error("check %s with %s buffer failed, miscompare %s" %
                                           (source_buff.get_pattern(), compare_buffs, miscompare))

    def get_write_buffer(self, pattern_mode):
        """
        Filters write buffers by matching their name with a regex pattern.

        Parameters:
            pattern_mode (re.Pattern): Regex pattern to match buffer names.

        Returns:
            list: Matching buffer names.
        """
        return [write_buffer for write_buffer in self.write_buffer_list if pattern_mode.search(write_buffer)]

    def get_compression_buffers(self, compression=None):
        """
        Returns appropriate write buffers based on the specified compression level.

        Parameters:
            compression (int): Compression level ranging from 0 to 16 or higher.

        Returns:
            list: List of buffers corresponding to the given compression level.
        """
        if compression is None or compression == 0:
            return self.write_buffer_list
        elif compression == 1:
            return self.incompressible_write_buffers
        elif compression == 2:
            return self.two_compressible_write_buffers
        elif compression == 3:
            return self.third_compressible_write_buffers
        elif compression == 4:
            return self.quarter_compressible_write_buffers
        elif compression == 6:
            return self.six_compressible_write_buffers
        elif compression == 8:
            return self.eighth_compressible_write_buffers
        elif compression == 12:
            return self.twelve_compressible_write_buffers
        elif compression == 16:
            return self.sixteen_compressible_write_buffers
        elif compression > 16:
            return self.high_compressible_write_buffers
        else:
            self.logger.error("compression value %s is not support" % compression)

    @property
    def high_compressible_write_buffers(self):
        """
        Returns write buffers that are highly compressible (i.e., excludes 'incompressible' buffers).

        Returns:
            list: Highly compressible write buffers.
        """
        pattern_mode = re.compile('incompressible')
        return list(set(self.write_buffer_list) - set(self.get_write_buffer(pattern_mode)))

    @property
    def incompressible_write_buffers(self):
        """
        Returns buffers marked as incompressible.

        Returns:
            list: Incompressible write buffers.
        """
        pattern_mode = re.compile('^incompressible_data')
        return self.get_write_buffer(pattern_mode)

    @property
    def two_compressible_write_buffers(self):
        """
        Returns buffers marked as 2x compressible.

        Returns:
            list: Buffers tagged with '^2x_compressible_data'.
        """
        pattern_mode = re.compile('^2x_compressible_data')
        return self.get_write_buffer(pattern_mode)

    @property
    def third_compressible_write_buffers(self):
        """
        Returns buffers marked as 3x compressible.

        Returns:
            list: Buffers tagged with '^3x_compressible_data'.
        """
        pattern_mode = re.compile('^3x_compressible_data')
        return self.get_write_buffer(pattern_mode)

    @property
    def quarter_compressible_write_buffers(self):
        """
        Returns buffers marked as 4x compressible.

        Returns:
            list: Buffers tagged with '^4x_compressible_data'.
        """
        pattern_mode = re.compile('^4x_compressible_data')
        return self.get_write_buffer(pattern_mode)

    @property
    def six_compressible_write_buffers(self):
        """
        Returns buffers marked as 6x compressible.

        Returns:
            list: Buffers tagged with '^6x_compressible_data'.
        """
        pattern_mode = re.compile('^6x_compressible_data')
        return self.get_write_buffer(pattern_mode)

    @property
    def eighth_compressible_write_buffers(self):
        """
        Returns buffers marked as 8x compressible.

        Returns:
            list: Buffers tagged with '^8x_compressible_data'.
        """
        pattern_mode = re.compile('^8x_compressible_data')
        return self.get_write_buffer(pattern_mode)

    @property
    def twelve_compressible_write_buffers(self):
        """
        Returns buffers marked as 12x compressible.

        Returns:
            list: Buffers tagged with '^12x_compressible_data'.
        """
        pattern_mode = re.compile('^12x_compressible_data')
        return self.get_write_buffer(pattern_mode)

    @property
    def sixteen_compressible_write_buffers(self):
        """
        Returns buffers marked as 16x compressible.

        Returns:
            list: Buffers tagged with '^16x_compressible_data'.
        """
        pattern_mode = re.compile('^16x_compressible_data')
        return self.get_write_buffer(pattern_mode)





