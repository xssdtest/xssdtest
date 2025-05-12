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
    driver = xt.XT_DRIVER("0000:01:00.0", 'libaio_nvme', logger=logger)
    qdepth = 1024
    device = xt.XT_DEVICES(driver, logger, qdepth=qdepth)
    test_buffer = xt.XT_BUFFER(buf_length=4096 * 64, buf_align=4096, buf_type=2, logger=logger, mem_init=0, alloc_type=1)
    io_qpair = device.default_io_qpair
    device.enable_io_histogram()
    elba, index = 0x1000000-1, 0
    writebuf_list = device.get_write_buffer_list
    ## test send_io_cmds
    for slba in range(0, elba, 8):
        # device.send_io_cmds(opcode=1, buf=writebuf_list[index], cdw10=slba&0xffffffff, cdw11=(slba >> 32) & 0xffffffff, cdw12=7, wait_completed=0, io_tailer_flag=1)
        device.send_io_cmds(opcode=2, buf=test_buffer, cdw10=slba&0xffffffff, cdw11=(slba >> 32) & 0xffffffff, cdw12=7, wait_completed=0, io_tailer_flag=1)
        index += 1
        # if index % qdepth == 0:
        if index % qdepth == 0:
            # logger.info("submit commit %d take time %s"%(qdepth, (time.time() - stime)))
            device.wait_io_completion(io_qpair)
            index = 0
            # device.wait_qpair_completioned(qpair)
    # test send_io_read
    device.send_io_read(io_qpair, slba=0, elba=elba, lbacnt=8, readbuf_list=test_buffer, io_check_type=0, reap_type=0)
    #this case current IOPS count 453214.00 /s write data 0x0                * 512  current speed is 0.00  M/s   this case current read data 0x146f00000        * 512   current speed is 1770.00M/s   take time 1.00
    #fio --name=continuous-read -direct=1 -thread -ioengine=libaio --rw=read --bs=4k --size=30G --numjobs=1 --time_based --runtime=30 -filename=/dev/nvme1n1 -iodepth=1024
    # read: IOPS=445k, BW=1739MiB/s (1824MB/s)(51.0GiB/30001msec)
    # test send_io_write
    device.send_io_write(io_qpair, slba=0, elba=elba, lbacnt=8, writebuf_list=device.get_write_buffer_list, reap_type=0, io_tailer_flag=0, qdepth=1024)
    #this case current IOPS count 458215.00 /s write data 0x1b995f000        * 512  current speed is 1789.00M/s   this case current read data 0x0                * 512   current speed is 0.00  M/s   take time 1.00
    #fio --name=continuous-read -direct=1 -thread -ioengine=libaio --rw=write --bs=4k --size=30G --numjobs=1 --time_based --runtime=30 -filename=/dev/nvme1n1 -iodepth=1024
    #Jobs: 1 (f=1): [W(1)][100.0%][w=1680MiB/s][w=430k IOPS][eta 00m:00s]
    # test send_random_write_full
    # device.send_random_write_full(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, qdepth=1024)
    # this case current IOPS count 449052.00 /s write data 0x14540a000        * 512  current speed is 1754.00M/s   this case current read data 0x0                * 512   current speed is 0.00  M/s   take time 1.00
    # fio --name=continuous-read -direct=1 -thread -ioengine=libaio --rw=randwrite --bs=4k --size=30G --numjobs=1 --time_based --runtime=30 -filename=/dev/nvme1n1 -iodepth=1024
    # Jobs: 1 (f=1): [w(1)][100.0%][w=1649MiB/s][w=422k IOPS][eta 00m:00s]
    # test send_random_read_full
    device.send_random_read_full(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024)
    # this case current IOPS count 450550.00 /s write data 0x0                * 512  current speed is 0.00  M/s   this case current read data 0x147452000        * 512   current speed is 1759.00M/s   take time 1.00
    # fio --name=continuous-read -direct=1 -thread -ioengine=libaio --rw=randread --bs=4k --size=30G --numjobs=1 --time_based --runtime=30 -filename=/dev/nvme1n1 -iodepth=1024
    # Jobs: 1 (f=1): [r(1)][100.0%][r=1716MiB/s][r=439k IOPS][eta 00m:00s]
    # test send_io_sequences
    # send_io_sequences
    device.send_io_sequences(io_qpair, io_sequences=[[2, 0, 8, 0]] * 0x100000, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024)

    # sequential write
    device.send_io_sequences(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024, random_mode=False, mix_write=100)
    # this case current IOPS count 471743.00 /s write data 0x1556a2000        * 512  current speed is 1842.00M/s   this case current read data 0x0                * 512   current speed is 0.00  M/s   take time 1.00
    # fio --name=continuous-read -direct=1 -thread -ioengine=libaio --rw=write --bs=4k --size=30G --numjobs=1 --time_based --runtime=30 -filename=/dev/nvme1n1 -iodepth=1024
    # Jobs: 1 (f=1): [W(1)][100.0%][w=1680MiB/s][w=430k IOPS][eta 00m:00s]
    # sequential read
    device.send_io_sequences(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024, random_mode=False, mix_write=0)
    # this case current IOPS count 456592.00 /s write data 0x0                * 512  current speed is 0.00  M/s   this case current read data 0x14996e000        * 512   current speed is 1783.00M/s   take time 1.00
    # fio --name=continuous-read -direct=1 -thread -ioengine=libaio --rw=read --bs=4k --size=30G --numjobs=1 --time_based --runtime=30 -filename=/dev/nvme1n1 -iodepth=1024
    # read: IOPS=445k, BW=1739MiB/s (1824MB/s)(51.0GiB/30001msec)
    # mix read and write
    device.send_io_sequences(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024, random_mode=False, mix_write=50)
    # this case current IOPS count 468789.00 /s write data 0x12255a000        * 512  current speed is 929.50M/s   this case current read data 0x11a178000        * 512   current speed is 901.50M/s   take time 2.00
    # fio --name=continuous-read -direct=1 -thread -ioengine=libaio --rw=rw -rwmixread=50 --bs=4k --size=30G --numjobs=1 --time_based --runtime=30 -filename=/dev/nvme1n1 -iodepth=1024
    #   read: IOPS=222k, BW=868MiB/s (911MB/s)(25.4GiB/30001msec)
    #   write: IOPS=222k, BW=868MiB/s (910MB/s)(25.4GiB/30001msec)
    # random read
    device.send_io_sequences(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024, random_mode=True, mix_write=0, lcg_radom=1)
    # this case current IOPS count 426692.00 /s write data 0x0                * 512  current speed is 0.00  M/s   this case current read data 0x133373000        * 512   current speed is 1666.00M/s   take time 1.00  lcg_radom = 1
    # this case current IOPS count 372200.00 /s write data 0x0                * 512  current speed is 0.00  M/s   this case current read data 0x17fb13000        * 512   current speed is 1453.00M/s   take time 1.00  lcg_radom = 0
    # fio --name=continuous-read -direct=1 -thread -ioengine=libaio --rw=randread --bs=4k --size=30G --numjobs=1 --time_based --runtime=30 -filename=/dev/nvme1n1 -iodepth=1024
    # Jobs: 1 (f=1): [r(1)][100.0%][r=1716MiB/s][r=439k IOPS][eta 00m:00s]
    # random write
    device.send_io_sequences(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024, random_mode=True, mix_write=100, lcg_radom=0, aligned=8)
    # this case current IOPS count 459917.00 /s write data 0x1509a1000        * 512  current speed is 1796.00M/s   this case current read data 0x0                * 512   current speed is 0.00  M/s   take time 1.00
    # fio --name=continuous-read -direct=1 -thread -ioengine=libaio --rw=randwrite --bs=4k --size=30G --numjobs=1 --time_based --runtime=30 -filename=/dev/nvme1n1 -iodepth=1024
    # Jobs: 1 (f=1): [w(1)][100.0%][w=1649MiB/s][w=422k IOPS][eta 00m:00s]

    # random mix read and write
    device.send_io_sequences(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024, random_mode=True, mix_write=50)
    # this case current IOPS count 463148.50 /s write data 0x11d065000        * 512  current speed is 920.00M/s   this case current read data 0x113a7f000        * 512   current speed is 888.50M/s   take time 2.00
    # fio --name=continuous-read -direct=1 -thread -ioengine=libaio --rw=randrw -rwmixread=50 --bs=4k --size=30G --numjobs=1 --time_based --runtime=30 -filename=/dev/nvme1n1 -iodepth=1024
    #   read: IOPS=216k, BW=844MiB/s (885MB/s)(24.7GiB/30001msec)
    #   write: IOPS=216k, BW=843MiB/s (884MB/s)(24.7GiB/30001msec)
    # random mix read and write and runtime
    device.send_io_sequences(io_qpair, slba=0, elba=elba, bs=8, writebuf_list=writebuf_list, readbuf_list=[test_buffer], qdepth=1024, random_mode=True, mix_write=50, runTime=10, lcg_radom=0)
    # this case current IOPS count 463689.50 /s write data 0x11bf4b000        * 512  current speed is 917.50M/s   this case current read data 0x113e48000        * 512   current speed is 893.50M/s   take time 2.00 lcg_radom = 1
    # this case current IOPS count 269520.00 /s write data 0x62eeb000         * 512  current speed is 400.33M/s   this case current read data 0x62785000         * 512   current speed is 398.33M/s   take time 3.00 lcg_radom = 0
    # fio --name=continuous-read -direct=1 -thread -ioengine=libaio --rw=randrw -rwmixread=50 --bs=4k --size=30G --numjobs=1 --time_based --runtime=30 -filename=/dev/nvme1n1 -iodepth=1024
    #   read: IOPS=216k, BW=844MiB/s (885MB/s)(24.7GiB/30001msec)
    #   write: IOPS=216k, BW=843MiB/s (884MB/s)(24.7GiB/30001msec)
    device.print_io_histogram()
