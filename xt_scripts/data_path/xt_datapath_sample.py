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
import pathlib
project_path = str(pathlib.Path(__file__).parent.parent.parent)
if project_path not in sys.path:
    sys.path.append(project_path)
from xt_liabary.test_cases import *
from xt_liabary.catch_exceptions import *

class DataPath_Sample(TestCase):
    def __init__(self):
        super(DataPath_Sample, self).__init__()
        self.device = self.default_device

    @CatchException
    def run(self):
        io_qpair = self.device.qpair_inst.create_io_queues(1024)
        self.device.set_io_histogram(enable=True)
        elba =self.device.max_lba
        writebuf_list = self.device.buffer.write_buffer_list
        readbuffer = self.device.buffer.create_buffer(self.device.max_data_transfer_size)
        self.device.send_io_read(io_qpair, slba=0, elba=elba, lbacnt=8, readbuf_list=readbuffer, io_check_type=0, reap_type=0)
        # self.device.send_io_write(io_qpair, slba=0, elba=elba, lbacnt=8, writebuf_list=writebuf_list, reap_type=0, io_tailer_flag=0, qdepth=4)
        self.device.show_io_histogram()

if __name__ == '__main__':
    test_inst = DataPath_Sample()
    test_inst.run