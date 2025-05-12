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
import random
pathList = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)
parPath = os.path.sep.join([item for item in pathList[:-2]])
sys.path.append(parPath)
sys.path.append(os.path.sep.join((parPath, 'xt_platform')))
from xt_platform import *

if __name__ == '__main__':
    logger = xt_interface.Logger()
    test_buffer = xt_interface.XT_BUFFER(buf_length=4096, buf_align=4096, buf_type=1, logger=logger, mem_init=0)
    logger.info("test buffer pattern info: 0x%x"%(test_buffer.get_pattern()))
    test_buffer.dump_buf(offset=0, length=0x40)
    logger.info("test buffer: get raw buf %s"%(test_buffer.get_raw_buf(offset=0, length=0x100, step=0x10)))
    test_buffer.fill_stream("xssdtest")
    test_buffer.dump_buf(offset=0, length=0x40)

    _value = random.randint(0, 255)
    test_buffer.set_uint8(offset=0, value=_value)
    if test_buffer.get_uint8(offset=0) == _value:
        logger.info("test buffer: set value successfully")
    else:
        assert False, logger.info("test buffer: set value %s is not equal to get value %s"%(_value, test_buffer.get_uint8(offset=0)))

    _value = random.randint(0, 255)
    test_buffer.set_uint16(offset=0, value=_value)
    if test_buffer.get_uint16(offset=0) == _value:
        logger.info("test buffer: set value successfully")
    else:
        assert False, logger.info("test buffer: set value %s is not equal to get value %s"%(_value, test_buffer.get_uint16(offset=0)))
    test_buffer.set_uint32(offset=0, value=_value)
    if test_buffer.get_uint32(offset=0) == _value:
        logger.info("test buffer: set value successfully")
    else:
        assert False, logger.info("test buffer: set value %s is not equal to get value %s"%(_value, test_buffer.get_uint32(offset=0)))
    test_buffer.set_uint64(offset=0, value=_value)
    if test_buffer.get_uint64(offset=0) == _value:
        logger.info("test buffer: set value successfully")
    else:
        assert False, logger.info("test buffer: set value %s is not equal to get value %s"%(_value, test_buffer.get_uint64(offset=0)))

    _value = random.randint(0, 255)
    test_buffer.fill_byte(value=_value)
    test_buffer.dump_buf(offset=0, length=0x40)

    test_buffer.fill_word(value=_value)
    test_buffer.dump_buf(offset=0, length=0x40)

    test_buffer.fill_dword(value=_value)
    test_buffer.dump_buf(offset=0, length=0x40)

    test_buffer.fill_qword(value=_value)
    test_buffer.dump_buf(offset=0, length=0x40)

    test_buffer.fill_random(offset=0)

    value = test_buffer.calculate_crc8()
    logger.info("test buffer: crc8 value: 0x%x"%(value))
    value = test_buffer.calculate_crc16()
    logger.info("test buffer: crc16 value: 0x%x"%(value))
    value = test_buffer.calculate_crc32()
    logger.info("test buffer: crc32 value: 0x%x"%(value))
    value = test_buffer.calculate_crc64()
    logger.info("test buffer: crc64 value: 0x%x"%(value))

    logger.info("test buffer: __str__  %s"%str(test_buffer))
    logger.info("test buffer: __repr__ %s" %test_buffer)
    logger.info("test buffer: __len__ %s" % len(test_buffer))

    value = test_buffer[0]
    test_buffer[0] = 0xff - value
    if test_buffer[0] == (0xff - value):
        logger.info("test buffer: set value successfully")
    else:
        assert False, logger.info("test buffer: set value %s is not equal to get value %s" % (_value, test_buffer.get_uint8(offset=0)))

    del test_buffer
