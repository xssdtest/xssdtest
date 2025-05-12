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

DEVICE_STATUS_READY = 0x00
DEVICE_STATUS_QUICK_REBUILDING = 0x01
DEVICE_STATUS_FULL_REBUILDING = 0x02
DEVICE_STATUS_RAW_REBUILDING = 0x03
DEVICE_STATUS_CARD_READ_ONLY = 0x04
DEVICE_STATUS_FATAL_ERROR = 0x05
DEVICE_STATUS_BUSY = 0x06
DEVICE_STAUTS_LOW_LEVEL_FORMAT = 0x07
DEVICE_STAUTS_FW_COMMITING = 0x08
DEVICE_STAUTS__OVER_TEMPRATURE = 0x09

class dera_nvme_smart_info_log(StructureBase):
    _fields_ = [
        ("quick_rebuild_cnt0", c_uint32),
        ("quick_rebuild_cnt1", c_uint32),
        ("full_rebuild_cnt0", c_uint32),
        ("full_rebuild_cnt1", c_uint32),
        ("raw_rebuild_cnt0", c_uint32),
        ("raw_rebuild_cnt1", c_uint32),
        ("cap_aged", c_uint8),
        ("cap_aged_ratio",c_uint8),
        ("cap_status", c_uint8),
        ("cap_voltage", c_uint32),
        ("cap_charge_ctrl_en", c_uint8),
        ("cap_charge_ctrl_val", c_uint16),
        ("cap_charge_max_thr", c_uint16),
        ("cap_charge_min_thr", c_uint16),
        ("dev_status", c_uint8),
        ("dev_status_up", c_uint8),
        ("nand_erase_err_cnt", c_uint32),
        ("nand_program_err_cnt", c_uint32),
        ("ddra_1bit_err", c_uint16),
        ("ddra_2bit_err", c_uint16),
        ("ddrb_1bit_err", c_uint16),
        ("ddrb_2bit_err", c_uint16),
        ("ddr_err_bit", c_uint8),
        ("pcie_corr_err", c_uint16),
        ("pcie_uncorr_err", c_uint16),
        ("pcie_fatal_err", c_uint16),
        ("pcie_err_bit", c_uint8),
        ("power_level", c_uint8),
        ("current_power", c_uint16),
        ("nand_init_fail", c_uint16),
        ("fw_loader_version", c_char * 8),
        ("uefi_driver_version", c_char * 8),
        ("gpio0_err", c_uint16),
        ("gpio5_err", c_uint16),
        ("gpio_err_bit", c_uint16),
        ("rebuild_percent", c_uint8),
        ("pcie_volt_status", c_uint8),
        ("current_pcie_volt", c_uint16),
        ("init_pcie_volt_thr", c_uint16),
        ("rt_pcie_volt_thr", c_uint16),
        ("init_pcie_volt_low", c_uint16),
        ("rt_pcie_volt_low", c_uint16),
        ("temp_sensor_abnormal", c_uint16),
        ("nand_read_retry_fail_cnt", c_uint32),
        ("fw_slot_version", c_uint64),
        ("rsved", c_uint8 * 395),
    ]