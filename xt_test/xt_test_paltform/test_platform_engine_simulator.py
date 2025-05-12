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
import os
import time
pathList = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)
parPath = os.path.sep.join([item for item in pathList[:-2]])
sys.path.append(parPath)
sys.path.append(os.path.sep.join((parPath, 'xt_platform')))
from xt_platform import xt_interface as xt
if __name__ == '__main__':
    logger = xt.Logger()
    driver = xt.XT_DRIVER("0000:00:00.0", 'simulator_nvme_xssdtest', logger=logger)
    qdepth = 512
    device = xt.XT_DEVICES(driver, logger, qdepth=qdepth)
    test_buffer = xt.XT_BUFFER(buf_length=4096 * 64, buf_align=4096, buf_type=2, logger=logger, mem_init=0, device=device)
    io_qpair = device.default_io_qpair
    device.enable_io_histogram()
    elba, index = 0x1000000-1, 0
    writebuf_list = device.get_write_buffer_list

    ## test send_io_cmds
    for slba in range(0, elba, 8):
        # device.send_io_cmds(opcode=1, buf=writebuf_list[index], cdw10=slba&0xffffffff, cdw11=(slba >> 32) & 0xffffffff, cdw12=7, wait_completed=0, io_tailer_flag=1)
        device.send_io_cmds(opcode=2, buf=test_buffer, cdw10=slba&0xffffffff, cdw11=(slba >> 32) & 0xffffffff, cdw12=7, wait_completed=0, io_tailer_flag=1)
        index += 1
        if index % qdepth == 0:
            # logger.info("submit commit %d take time %s"%(qdepth, (time.time() - stime)))
            device.wait_io_completion(io_qpair)
            index = 0
            # device.wait_qpair_completioned(qpair)

    ## test send_io_read
    device.send_io_read(io_qpair, slba=0, elba=elba, lbacnt=8, readbuf_list=test_buffer, io_check_type=0, reap_type=0)
    ## test send_io_write
    device.send_io_write(io_qpair, slba=0, elba=elba, lbacnt=8, writebuf_list=device.get_write_buffer_list, reap_type=0, io_tailer_flag=0, qdepth=4)
    ## test send_random_write_full
    device.send_random_write_full(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, qdepth=1024)
    ## test send_random_read_full
    device.send_random_read_full(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024)

    ## test send_io_sequences
    ## send_io_sequences
    device.send_io_sequences(io_qpair, io_sequences=[[2, 0, 8, 0]] * 0x10000000, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1)
    ## sequential write
    device.send_io_sequences(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024, random_mode=False)
    ## sequential read
    device.send_io_sequences(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024, random_mode=False, mix_write=0)
    ## mix read and write
    device.send_io_sequences(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024, random_mode=False, mix_write=50)
    ## random read
    device.send_io_sequences(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024, random_mode=True, mix_write=0)
    ## random write
    device.send_io_sequences(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024, random_mode=True, mix_write=100)
    ## random mix read and write
    device.send_io_sequences(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024, random_mode=True, mix_write=50)
    ## random mix read and write and runtime
    device.send_io_sequences(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024, random_mode=True, mix_write=50, runTime=10)
    device.print_io_histogram()
