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
import signal
import datetime
import argparse
path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(path)))
from xt_liabary.ssh import SSH

# Handle interrupt sign, main process exit
def handle_sigint(sig, frame):
    sys.exit(0)

if __name__=="__main__":
    signal.signal(signal.SIGINT, handle_sigint)
    parser = argparse.ArgumentParser(description="xSSD Test ssh")
    parser.add_argument("-u", "--user", type=str, dest="user", default=None, help="ssh host user name default is None")
    parser.add_argument("-p", "--password", type=str, dest="password", default=None, help="ssh host password default is None")
    parser.add_argument("-host", "--hostname", type=str, dest="hostname", default=None, help="ssh host name default is None")
    parser.add_argument("-c", "--command", type=str, dest="command", default=None, help="ssh run command in host default is None")
    args = parser.parse_args()
    assert args.user and args.password and args.hostname, print("input user %s password %s hostname %s"%(args.user, args.password, args.hostname))
    active_ssh = SSH(args.user, args.password, args.hostname)
    if args.command is None:
        while True:
            try:
                signal.alarm(3600)  # set session timeout
                user_input = input("%s@xt:%s $"%(args.user, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                signal.alarm(0)  # cancel timeout
            except KeyboardInterrupt:
                print("session timeout")
                sys.exit(1)
            if len(user_input) == 0:
                continue
            active_ssh.session_run(user_input)
            if 'exit' == user_input:
                print("session exit layout")
                sys.exit(1)
    else:
        active_ssh.session_run(args.command)


