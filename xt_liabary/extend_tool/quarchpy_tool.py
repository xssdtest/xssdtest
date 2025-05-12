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
from quarchpy.device import quarchDevice
class QuarchpyTool(object):
    def __init__(self, device):
        self.device = device
        self.logger = self.device.logger
        self.quarchpy_name = self.check_quarchpy_path()

    def power_cycle_by_quarchpy(self, run_type=0, device_name=None):
        device_name = device_name if device_name else "/dev/ttyUSB0"
        self.logger.info("quarchpy power on/off start")
        device = quarchDevice(f"SERIAL:{device_name}")
        if run_type == 0 :
            self.logger.info("quarchpy power off start")
            device.sendCommand("run:power down")
            self.logger.info("quarchpy power off end")
        else:
            self.logger.info("quarchpy power on start")
            device.sendCommand("run:power up")
            self.logger.info("quarchpy power on end")
        device.closeConnection()
        self.logger.info("quarchpy power on/off end")

    def check_quarchpy_path(self):
        pci_info = self.device.pci_info
        return "/dev/ttyUSB0"
