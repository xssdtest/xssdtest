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
from xt_module.xt_structure import *
NVME_VSC_GET_EVENT_LOG = 0xC2
NVME_VSC_GET = 0xE6
NVME_VSC_TYPE1_GET = 0xFE
VSC_FN_GET_CDUMP = 0x08
IGVSC_SIG = 0x69677673
EVLOG_SIG = 0x65766C67
SRB_SIGNATURE = 0x544952474F4E4E49

class innogrit_evlg_flush_hdr(StructureBase):
    _fields_ = [
        ("signature", c_uint32),
        ("fw_ver", c_uint32 * 2),
        ("fw_type", c_uint8),
        ("log_type", c_uint8),
        ("project", c_uint16),
        ("trace_cnt", c_uint32),
        ("sout_crc", c_uint32),
        ("reserved", c_uint32 * 2),
    ]

class innogrit_eventlog(StructureBase):
    _fields_ = [
        ("ms", c_uint32),
        ("param", c_uint32 * 7),
    ]

class innogrit_drvinfo_t(StructureBase):
    _fields_ = [
        ("signature", c_uint8),
        ("fw_base", c_uint8),
        ("socid", c_uint16),
        ("soc_ver", c_uint8 * 4),
        ("loader_version", c_uint8 * 8),
        ("nand_devids", c_uint8 * 6),
        ("ddr_type", c_uint8),
        ("ddr_size", c_uint8),
        ("rsvd1", c_uint8 * 8),
        ("origin_fw_name", c_uint8 * 8),
        ("nand_type", c_uint64),
        ("board_type", c_uint32 * 5),
        ("soc_type", c_uint16),
        ("build_mode", c_uint8),
        ("rsvd2", c_uint8),
        ("ftl_build_num", c_uint32),
        ("soc_reg", c_uint16),
        ("rsvd3", c_uint8 * 2),
        ("cur_cpu_clk", c_uint32),
        ("cur_nf_clk", c_uint32),
        ("nand_geo", c_uint8 * 4),
        ("fw_d2h_info_bit", c_uint32),
        ("spi_flash_id", c_uint32),
        ("rom_version", c_uint8 * 8),
        ("rsvd4", c_uint8 * 404),
    ]

class innogrit_cdump_pack(StructureBase):
    _fields_ = [
        ("ilenth", c_uint32),
        ("fwver", c_uint8 * 8),
    ]

class innogrit_cdumpinfo(StructureBase):
    _fields_ = [
        ("signature", c_uint32),
        ("ipackcount", c_uint32),
        ("cdumppack", innogrit_cdump_pack * 32),
    ]



