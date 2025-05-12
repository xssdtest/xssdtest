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
BYTE_OF_64K = 65536
BYTE_OF_32K = 32768
BYTE_OF_16K = 16384
BYTE_OF_4K = 4096
BYTE_OF_512 = 512
BYTE_OF_256 = 256
BYTE_OF_128 = 128
VENDOR_SMART_LOG_PAGE = 0xc0

class inspur_r1_am_cap_transtime(StructureBase):
    _fields_ = [
        ('cap_trans_time1', c_uint16),
        ('cap_trans_time2', c_uint16),
    ]

class inspur_vendor_warning_bit(StructureBase):
    _fields_ = [
        ('high_format_fail', c_uint32, 1),
        ('low_format_fail', c_uint32, 1),
        ('rebuild_fail1', c_uint32, 1),
        ('rebuild_fail2', c_uint32, 1),
        ('rebuild_fail3', c_uint32, 1),
        ('rebuild_fail4', c_uint32, 1),
        ('rebuild_fail5', c_uint32, 1),
        ('rebuild_fail6', c_uint32, 1),
        ('self_test_fail1', c_uint32, 1),
        ('self_test_fail2', c_uint32, 1),
        ('self_test_fail3', c_uint32, 1),
        ('self_test_fail4', c_uint32, 1),
        ('internal_err1', c_uint32, 1),
        ('internal_err2', c_uint32, 1),
        ('internal_err3', c_uint32, 1),
        ('internal_err4', c_uint32, 1),
        ('internal_err5', c_uint32, 1),
        ('internal_err6', c_uint32, 1),
        ('internal_err7', c_uint32, 1),
        ('internal_err8', c_uint32, 1),
        ('internal_err9', c_uint32, 1),
        ('internal_err10', c_uint32, 1),
        ('internal_err11', c_uint32, 1),
        ('internal_err12', c_uint32, 1),
        ('internal_err13', c_uint32, 1),
        ('internal_err14', c_uint32, 1),
        ('internal_err15', c_uint32, 1),
        ('internal_err16', c_uint32, 1),
        ('capacitance_test_fail', c_uint32, 1),
        ('IO_read_fail', c_uint32, 1),
        ('IO_write_fail', c_uint32, 1),
        ('readOnly_after_rebuild', c_uint32, 1),
        ('firmware_loss', c_uint32, 1),
        ('cap_unsupply', c_uint32, 1),
        ('spare_space_warning', c_uint32, 1),
        ('lifetime_warning', c_uint32, 1),
        ('temp_high_warning', c_uint32, 1),
        ('temp_low_warning', c_uint32, 1),
        ('mcu_disable', c_uint32, 1),
        ('rsv', c_uint32, 25),
    ]

class inspur_r1_vendor_log_ncm_count(StructureBase):
    _fields_ = [
        ('nand_rd_unc_cnt', c_uint32),
        ('nand_rd_srr_cnt', c_uint32),
        ('nand_rd_soft_decode_cnt', c_uint32),
        ('nand_rd_rebuild_fail_cnt', c_uint32),
        ('nand_prg_fail_cnt', c_uint32),
        ('nand_eras_fail_cnt', c_uint32),
        ('nand_rd_cnt', c_uint64),
        ('nand_prg_cnt', c_uint64),
        ('nand_eras_cnt', c_uint64),
        ('be_scan_unc_cnt', c_uint32),
        ('rebuild_req_cnt', c_uint32),
        ('retry_req_cnt', c_uint16),
        ('retry_success_cnt', c_uint16),
        ('prg_badblk_num', c_uint32),
        ('eras_badblk_num', c_uint32),
        ('unc_badblk_num', c_uint32),
    ]

class inspur_r1_wearlvl_vendor_log_count(StructureBase):
    _fields_ = [
        ('fbb_count', c_uint32),
        ('ebb_count', c_uint32),
        ('lbb_count', c_uint32),
        ('gc_read_count', c_uint32),
        ('gc_write_count', c_uint32),
        ('gc_write_fail_count', c_uint32),
        ('force_gc_count', c_uint32),
        ('avg_pe_count', c_uint32),
        ('max_pe_count', c_uint32),
        ('free_blk_num1', c_uint32),
        ('free_blk_num2', c_uint32),
    ]

class inspur_vendor_media_err(StructureBase):
    _fields_ = [
        ('lba_err', c_uint64 * 10),
    ]

class inspur_r1_vendor_log_io_err(StructureBase):
    _fields_ = [
        ('io_guard_err', c_uint32),
        ('io_apptag_err', c_uint32),
        ('io_reftag_err', c_uint32),
        ('io_dma_linkdown_err', c_uint32),
        ('io_dma_disable_err', c_uint32),
        ('io_dma_timeout_err', c_uint32),
        ('io_dma_fatal_err', c_uint32),
        ('io_write_fail_cout', c_uint32),
        ('io_read_fail_cout', c_uint32),
        ('lba_err', c_uint64 * 6),
    ]

class inspur_r1_cli_vendor_log(StructureBase):
    _fields_ = [
        ('max_power', c_uint32),
        ('disk_max_temper', c_uint32),
        ('disk_overtemper_cout', c_uint32),
        ('ctrl_max_temper', c_uint32),
        ('ctrl_overtemper_cout', c_uint32),
        ('cap_trans_time1', c_uint16),
        ('cap_trans_time2', c_uint16),
        ('cap_health_state', c_uint32),
        ('device_state', c_uint32),
        ('io_err', inspur_r1_vendor_log_io_err * 4),
        ('detail_warning_bit', inspur_vendor_warning_bit),
        ('detail_warning_his_bit', inspur_vendor_warning_bit),
        ('ddr_bit_err_cout', c_uint32),
        ('temp_throttle_per', c_uint32),
        ('port0_fundamental_reset_cnt', c_uint64),
        ('port0_hot_reset_cnt', c_uint64),
        ('port0_func_reset_cnt', c_uint64),
        ('port0_linkdown_cnt', c_uint64),
        ('port0_ctrl_reset_cnt', c_uint64),
        ('nand_bytes_written', c_uint64 * 4),
        ('power_info', c_uint32),
        ('voltage_info', c_uint32),
        ('current_info', c_uint32),
        ('current_temp', c_uint32 * 4),
        ('nand_max_temper', c_uint32),
        ('nand_overtemper_cout', c_uint32),
        ('mcu_data_id', c_uint32),
        ('commit_id', c_uint8 * 16),
        ('ces_rcv_err_cnt', c_uint32),
        ('ces_bad_tlp_cnt', c_uint32),
        ('ces_bad_dllp_cnt', c_uint32),
        ('ces_rplyover_cnt', c_uint32),
        ('ces_rply_to_cnt', c_uint32),
        ('ces_hlo_cnt', c_uint32),
        ('scan_db_err_cnt', c_uint32),
        ('db_int_err_cnt', c_uint32),
        ("rsvd1", c_uint8 * 56),
        ('vendor_log_nandctl_cnt', inspur_r1_vendor_log_ncm_count * 4),
        ('temp_ctrl_limit_cnt', c_uint32),
        ('temp_ctrl_stop_cnt', c_uint32),
        ("rsvd2", c_uint8 * 216),
        ('wearlvl_vendor_log_count', inspur_r1_wearlvl_vendor_log_count * 4),
        ("rsvd3", c_int8 * 468),
        ('e2e_check_err_cnt1', c_uint32),
        ('e2e_check_err_cnt2', c_uint32),
        ('e2e_check_err_cnt3', c_uint32),
        ('e2e_check_err_cnt4', c_uint32),
        ('media_err', inspur_vendor_media_err * 4),
        ('rsvd4', c_uint8 * 176),
    ]