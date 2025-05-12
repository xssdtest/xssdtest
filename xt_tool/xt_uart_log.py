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
import sys
import serial
import signal
import time
import datetime
import threading
import argparse
parser = argparse.ArgumentParser(description="xSSD Test uart print")
parser.add_argument("-u", "--uart_path", type="str", dest="uart_path", default="/dev/ttyUSB0", help="uart path for serial default value is /dev/ttyUSB0")
parser.add_argument("-b", "--baudrate", type="int", dest="baudrate", default=921600, help="serial baudrate, default value is 921600")
parser.add_argument("-d", "--dump_path", type="str", dest="dump_path", default=None, help="dump log path , default is None")
parser.add_argument("-r", "--runtime", type="int", dest="runtime", default=86400, help="max run time, default is 1 day")
args = parser.parse_args()
dump_fd = None
if args.dump_path and os.path.exists(args.dump_path):
    dump_fd = open(args.dump_path, "ab+")

# Handle interrupt sign, main process exit
def handle_sigint(sig, frame):
    if dump_fd is not None:
        dump_fd.flush()
        dump_fd.close()
    sys.exit(0)

# Send command to uart and echo Command
def send_cmd(ser):
    stime = time.time()
    while time.time() - stime <  args.runtime:
        cmd_line =  input("")
        if len(cmd_line) == 0:
            continue
        cmd_line = cmd_parse(cmd_line)
        ser.write(cmd_line.encode())
        print(cmd_line, end='')

# parse send command to uart
def cmd_parse(cmd_line):
    return cmd_line + '\n'

# parse get log from uart
def log_parse(line_log):
    return line_log

# get log from uart
def get_log_from_uart(ser):
    line_count = 0
    stime = time.time()
    while time.time() - stime <  args.runtime:
        line_log = ser.readline()
        line_log = log_parse(line_log)
        if line_log:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            line_log = bytes(now + ": ", "ascii") + line_log
            if dump_fd:
                dump_fd.write(line_log)
            line_count += 1
            print(line_count, line_log)
        if line_count % 1000 == 0 and dump_fd:
            dump_fd.flush()

if __name__=="__main__":
    signal.signal(signal.SIGINT, handle_sigint)
    ser = serial.Serial()
    ser.baudrate = args.baudrate
    if os.path.exists(args.uart_path):
        ser.port = args.uart_path
    else:
        assert False, print("%s path not exist")
    ser.open()

    threads = []
    threads.append(threading.Thread(target=get_log_from_uart, args=(ser,)))
    threads.append(threading.Thread(target=send_cmd, args=(ser,)))
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    if dump_fd:
        dump_fd.flush()
        dump_fd.close()
