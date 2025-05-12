#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from xt_module.xt_structure import *

SFX_LOG_LATENCY_READ_STATS  = 0xc1
SFX_LOG_EXTENDED_HEALTH     = 0xc2
SFX_LOG_LATENCY_WRITE_STATS = 0xc3
SFX_LOG_QUAL                = 0xc4
SFX_LOG_MISMATCHLBA         = 0xc5
SFX_LOG_MEDIA               = 0xc6
SFX_LOG_BBT                 = 0xc7
SFX_LOG_IDENTIFY            = 0xcc
SFX_FEAT_ATOMIC             = 0x01
SFX_FEAT_UP_P_CAP           = 0xac
SFX_LOG_EXTENDED_HEALTH_ALT = 0xd2
SFX_FEAT_CLR_CARD           = 0xdc
SFX_CRIT_PWR_FAIL_DATA_LOSS = 0x01
SFX_CRIT_OVER_CAP           = 0x02
SFX_CRIT_RW_LOCK            = 0x04
nvme_admin_query_cap_info   = 0xd3
nvme_admin_change_cap       = 0xd4
nvme_admin_sfx_set_features = 0xd5
nvme_admin_sfx_get_features = 0xd6

class sfx_freespace_ctx(StructureBase):
    _fields_ = [
        ('free_space', c_uint64),
        ('phy_cap', c_uint64),
        ('phy_space', c_uint64),
        ('user_space', c_uint64),
        ('hw_used', c_uint64),
        ('app_written', c_uint64),
        ('out_of_space', c_uint64),
        ('map_unit', c_uint64),
        ('max_user_space', c_uint64),
        ('extendible_user_cap_lba_count', c_uint64),
        ('friendly_change_cap_support', c_uint64),
    ]

class sfx_nvme_capacity_info(StructureBase):
    _fields_ = [
        ('lba_sec_sz', c_uint64),
        ('phy_sec_sz', c_uint64),
        ('used_space', c_uint64),
        ('free_space', c_uint64),
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

class sfx_lat_stats_vanda(StructureBase):
    _fields_ = [
        ('maj', c_uint16),
        ('min', c_uint16),
        ('bucket_1', c_uint32 * 32),
        ('bucket_2', c_uint32 * 31),
        ('bucket_3', c_uint32 * 31),
        ('bucket_4', c_uint32),
        ('bucket_5', c_uint32),
        ('bucket_6', c_uint32),
    ]

class sfx_lat_stats_myrtle(StructureBase):
    _fields_ = [
        ('maj', c_uint16),
        ('min', c_uint16),
        ('bucket_1', c_uint32 * 64),
        ('bucket_2', c_uint32 * 64),
        ('bucket_3', c_uint32 * 64),
        ('bucket_4', c_uint32 * 64),
        ('bucket_5', c_uint32 * 64),
        ('bucket_6', c_uint32 * 64),
        ('bucket_7', c_uint32 * 64),
        ('bucket_8', c_uint32 * 64),
        ('bucket_9', c_uint32 * 64),
        ('bucket_10', c_uint32 * 64),
        ('bucket_11', c_uint32 * 64),
        ('bucket_12', c_uint32 * 64),
        ('bucket_13', c_uint32 * 64),
        ('bucket_14', c_uint32 * 64),
        ('bucket_15', c_uint32 * 64),
        ('bucket_16', c_uint32 * 64),
        ('bucket_17', c_uint32 * 64),
        ('bucket_18', c_uint32 * 64),
        ('bucket_19', c_uint32 * 64),
        ("average", c_uint64)
    ]

class sfx_lat_status_ver(StructureBase):
    _fields_ = [
        ('maj', c_uint16),
        ('min', c_uint16),
    ]

class sfx_lat_stats(Union):
    _fields_ = [
        ('ver', sfx_lat_status_ver),
        ('vanda', sfx_lat_stats_vanda),
        ('myrtle', sfx_lat_stats_myrtle),
    ]

class sfx_nvme_additional_smart_log(StructureBase):
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
        ('raid_recover_cnt', sfx_nvme_additional_smart_log_item),
        ('prog_timeout_cnt', sfx_nvme_additional_smart_log_item),
        ('erase_timeout_cnt', sfx_nvme_additional_smart_log_item),
        ('read_timeout_cnt', sfx_nvme_additional_smart_log_item),
        ('read_ecc_cnt', sfx_nvme_additional_smart_log_item),
        ('non_media_crc_err_cnt', sfx_nvme_additional_smart_log_item),
        ('compression_path_err_cnt', sfx_nvme_additional_smart_log_item),
        ('out_of_space_flag', sfx_nvme_additional_smart_log_item),
        ('physical_usage_ratio', sfx_nvme_additional_smart_log_item),
        ('grown_bb', sfx_nvme_additional_smart_log_item),
    ]

class sfx_extended_health_info_myrtle(StructureBase):
    _fields_ = [
        ('soft_read_recoverable_errs', c_uint32),
        ('flash_die_raid_recoverable_errs', c_uint32),
        ('pcie_rx_correct_errs', c_uint32),
        ('pcie_rx_uncorrect_errs', c_uint32),
        ('data_read_from_flash', c_uint32),
        ('data_write_to_flash', c_uint32),
        ('temp_throttle_info', c_uint32),
        ('power_consumption', c_uint32),
        ('pf_bbd_read_cnt', c_uint32),
        ('sfx_critical_warning', c_uint32),
        ('raid_recovery_total_count', c_uint32),
        ('rsvd', c_uint32),
        ('opn', c_uint8 * 32),
        ('total_physical_capability', c_uint64),
        ('free_physical_capability', c_uint64),
        ('physical_usage_ratio', c_uint32),
        ('comp_ratio', c_uint32),
        ('otp_rsa_en', c_uint32),
        ('power_mw_consumption', c_uint32),
        ('io_speed', c_uint32),
        ('max_formatted_capability', c_uint64),
        ('map_unit', c_uint32),
        ('extendible_cap_lbacount', c_uint64),
        ('friendly_changecap_support', c_uint32),
        ('rvd1', c_uint32),
        ('cur_formatted_capability', c_uint64),
    ]