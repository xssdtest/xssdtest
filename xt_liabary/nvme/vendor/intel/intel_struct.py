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

MEDIA_MAJOR_IDX = 0
MEDIA_MINOR_IDX = 1
MEDIA_MAX_LEN   = 2
OPTANE_V1000_BUCKET_LEN = 8
NAND_LAT_STATS_LEN = 4868

class intel_temp_stats(StructureBase):
    _fields_ = [
        ("curr", c_uint64),
        ("last_overtemp", c_uint64),
        ("life_overtemp", c_uint64),
        ("highest_temp", c_uint64),
        ("lowest_temp", c_uint64),
        ("rsvd", c_uint8 * 40),
        ("max_operating_temp", c_uint64),
        ("min_operating_temp", c_uint64),
        ("est_offset", c_uint64),
    ]

class intel_lat_stats(StructureBase):
    _fields_ = [
        ("maj", c_uint16),
        ("min", c_uint16),
        ("data", c_uint32 * 1216),
    ]

class optane_lat_stats(StructureBase):
    _fields_ = [
        ("maj", c_uint16),
        ("min", c_uint16),
        ("data", c_uint64 * 9),
    ]

class v1000_thresholds(StructureBase):
    _fields_ = [
        ("read", c_uint32 * OPTANE_V1000_BUCKET_LEN),
        ("write", c_uint32 * OPTANE_V1000_BUCKET_LEN),
    ]

class intel_assert_dump(StructureBase):
    _fields_ = [
        ("coreoffset", c_uint32),
        ("assertsize", c_uint32),
        ("assertdumptype", c_uint8),
        ("assertvalid", c_uint8),
        ("rsvd", c_uint8 * 2),
    ]

class intel_event_dump(StructureBase):
    _fields_ = [
        ("numeventdumps", c_uint32),
        ("coresize", c_uint32),
        ("coreoffset", c_uint32),
        ("eventidoffset", c_uint32 * 16),
        ("eventIdValidity", c_uint8 * 16),
    ]

class intel_vu_version(StructureBase):
    _fields_ = [
        ("major", c_uint16),
        ("minor", c_uint16),
    ]

class intel_event_header(StructureBase):
    _fields_ = [
        ("eventidsize", c_uint32),
        ("edumps", Pointer(intel_event_dump, "eventidsize")),
    ]

class intel_vu_log(StructureBase):
    _fields_ = [
        ("ver", intel_vu_version),
        ("header", c_uint32),
        ("size", c_uint32),
        ("numcores", c_uint32),
        ("reserved", c_uint8 * 4080),
    ]

class intel_vu_nlog(StructureBase):
    _fields_ = [
        ("ver", intel_vu_version),
        ("logselect", c_uint32),
        ("totalnlogs", c_uint32),
        ("nlognum", c_uint32),
        ("nlogname", c_uint32),
        ("nlogbytesize", c_uint32),
        ("nlogprimarybuffsize", c_uint32),
        ("tickspersecond", c_uint32),
        ("corecount", c_uint32),
        ("nlogpausestatus", c_uint32),
        ("selectoffsetref", c_uint32),
        ("selectnlogpause", c_uint32),
        ("selectaddedoffset", c_uint32),
        ("nlogbufnum", c_uint32),
        ("nlogbufnummax", c_uint32),
        ("coreselected", c_uint32),
        ("reserved", c_uint32 * 3),
    ]

class intel_cd_log(StructureBase):
    _fields_ = [
        ("select_log", c_uint32, 3),
        ("select_core", c_uint32, 2),
        ("select_nlog", c_uint32, 8),
        ("select_offset_ref", c_uint32, 1),
        ("select_nlog_pause", c_uint32, 2),
        ("reserved", c_uint32, 16),
    ]

class wear_level(StructureBase):
    _fields_ = [
        ('min', c_uint16),
        ('max', c_uint16),
        ('avg', c_uint16),
    ]

class thermal_throttle(StructureBase):
    _fields_ = [
        ('pct', c_uint8),
        ('count', c_uint32),
    ]

class additional_smart_log_union(Union):
    _fields_ = [
        ('raw', c_uint8 * 6),
        ('wear_level', wear_level),
        ('thermal_throttle', thermal_throttle),
    ]

class sfx_nvme_additional_smart_log_item(StructureBase):
    _fields_ = [
        ('key', c_uint8),
        ('_kp', c_uint8 * 2),
        ('norm', c_uint8),
        ('_np', c_uint8),
        ('item', additional_smart_log_union),
        ('_rp', c_uint8),
    ]

class intel_nvme_additional_smart_log(StructureBase):
    _fields_ = [
        ('program_fail_cnt', sfx_nvme_additional_smart_log_item),
        ('erase_fail_cnt', sfx_nvme_additional_smart_log_item),
        ('wear_leveling_cnt', sfx_nvme_additional_smart_log_item),
        ('e2e_err_cnt', sfx_nvme_additional_smart_log_item),
        ('crc_err_cnt', sfx_nvme_additional_smart_log_item),
        ('timed_workload_media_wear', sfx_nvme_additional_smart_log_item),
        ('timed_workload_host_reads', sfx_nvme_additional_smart_log_item),
        ('timed_workload_timer', sfx_nvme_additional_smart_log_item),
        ('thermal_throttle_status', sfx_nvme_additional_smart_log_item),
        ('retry_buffer_overflow_cnt', sfx_nvme_additional_smart_log_item),
        ('pll_lock_loss_cnt', sfx_nvme_additional_smart_log_item),
        ('nand_bytes_written', sfx_nvme_additional_smart_log_item),
        ('host_bytes_written', sfx_nvme_additional_smart_log_item),
        ('host_ctx_wear_used', sfx_nvme_additional_smart_log_item),
        ('perf_stat_indicator', sfx_nvme_additional_smart_log_item),
        ('re_alloc_sectr_cnt', sfx_nvme_additional_smart_log_item),
        ('soft_ecc_err_rate', sfx_nvme_additional_smart_log_item),
        ('unexp_power_loss', sfx_nvme_additional_smart_log_item),
        ('media_bytes_read', sfx_nvme_additional_smart_log_item),
        ('avail_fw_downgrades', sfx_nvme_additional_smart_log_item),
    ]