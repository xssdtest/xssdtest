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
import crcmod
import sys
import pathlib
extend_tool_path = str(pathlib.Path(__file__).parent)
if extend_tool_path not in sys.path:
    sys.path.append(extend_tool_path)
from quarchpy_tool import QuarchpyTool
class ExtendTool(object):
    def __init__(self, device):
        self.device = device
        self.logger = self.device.logger
        self.quarchpy_tool = QuarchpyTool(device)
        self.default_crc8_func = crcmod.mkCrcFun(poly=0x107, initCrc=0x00, rev=False, xorOut=0xFF)
        self.default_crc16_func = crcmod.mkCrcFun(poly=0x18005, initCrc=0x00, rev=False, xorOut=0xFFFF)
        self.default_crc32_func = crcmod.mkCrcFun(poly=0x104C11DB7, initCrc=0x00, rev=False, xorOut=0xFFFFFFFF)
        self.default_crc64_func = crcmod.mkCrcFun(poly=0x142F0E1EBA9EA3693, initCrc=0x00, rev=False, xorOut=0xFFFFFFFFFFFFFFFF)

    def make_crc_func(self, poly, initCrc=0x00, rev=False, xorOut=0x00):
        crc_func = crcmod.mkCrcFun(poly=poly, initCrc=initCrc, rev=rev, xorOut=xorOut)
        return crc_func








