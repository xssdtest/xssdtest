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

class temperature(StructureBase):
    _fields_ = [
        ('max', c_uint16),
        ('min', c_uint16),
        ('cur', c_uint16),
    ]

class power_consumption(StructureBase):
    _fields_ = [
        ('max', c_uint16),
        ('min', c_uint16),
        ('avg', c_uint16),
    ]

class thermal_throttle_time(StructureBase):
    _fields_ = [
        ('sts', c_uint8),
        ('time', c_uint32),
        ('rsv', c_uint8),
    ]

class additional_smart_log_union(Union):
    _fields_ = [
        ("wear_level", wear_level),
        ('thermal_throttle', thermal_throttle),
        ('temperature', temperature),
        ('power_consumption', power_consumption),
        ('thermal_throttle_time', thermal_throttle_time),
        ('raw', c_uint8 * 6),
    ]

class nvme_additional_smart_log_item(StructureBase):
    _fields_ = [
        ('key', c_uint8),
        ('_kp', c_uint8 * 2),
        ('norm', c_uint8),
        ('_np', c_uint8),
        ('item', additional_smart_log_union),
        ('_rp', c_uint8),
    ]

class dapu_nvme_additional_smart_log(StructureBase):
    _fields_ = [
        ('program_fail_cnt', nvme_additional_smart_log_item),
        ('erase_fail_cnt', nvme_additional_smart_log_item),
        ('wear_leveling_cnt', nvme_additional_smart_log_item),
        ('e2e_err_cnt', nvme_additional_smart_log_item),
        ('crc_err_cnt', nvme_additional_smart_log_item),
        ('timed_workload_media_wear', nvme_additional_smart_log_item),
        ('timed_workload_host_reads', nvme_additional_smart_log_item),
        ('timed_workload_timer', nvme_additional_smart_log_item),
        ('thermal_throttle_status', nvme_additional_smart_log_item),
        ('retry_buffer_overflow_cnt', nvme_additional_smart_log_item),
        ('pll_lock_loss_cnt', nvme_additional_smart_log_item),
        ('nand_bytes_written', nvme_additional_smart_log_item),
        ('host_bytes_written', nvme_additional_smart_log_item),
    ]

class dapu_nvme_extended_additional_smart_log(StructureBase):
    _fields_ = [
        ('sys_area_life_remain', nvme_additional_smart_log_item),
        ('nand_bytes_read', nvme_additional_smart_log_item),
        ('temperature', nvme_additional_smart_log_item),
        ('power_consumption', nvme_additional_smart_log_item),
        ('power_on_temperature', nvme_additional_smart_log_item),
        ('power_loss_protection',nvme_additional_smart_log_item),
        ('read_fail_count', nvme_additional_smart_log_item),
        ('thermal_throttle_time', nvme_additional_smart_log_item),
        ('flash_error_media_count', nvme_additional_smart_log_item),
        ('lifetime_write_amplification', nvme_additional_smart_log_item),
        ('firmware_update_count', nvme_additional_smart_log_item),
        ('dram_cecc_count', nvme_additional_smart_log_item),
        ('dram_uecc_count', nvme_additional_smart_log_item),
        ('xor_pass_count', nvme_additional_smart_log_item),
        ('xor_fail_count', nvme_additional_smart_log_item),
        ('xor_invoked_count', nvme_additional_smart_log_item),
        ('inflight_read_io_cmd', nvme_additional_smart_log_item),
        ('temp_since_bootup', nvme_additional_smart_log_item),
        ('inflight_write_io_cmd', nvme_additional_smart_log_item),
    ]