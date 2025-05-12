#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from xt_module.xt_structure import *

PROGRAM_FAIL_CNT = 0
ERASE_FAIL_CNT = 1
WEARLEVELING_COUNT = 2
E2E_ERR_CNT = 3
CRC_ERR_CNT =4
TIME_WORKLOAD_MEDIA_WEAR = 5
TIME_WORKLOAD_HOST_READS = 6
TIME_WORKLOAD_TIMER = 7
THERMAL_THROTTLE = 8
RETRY_BUFFER_OVERFLOW = 9
PLL_LOCK_LOSS = 10
NAND_WRITE = 11
HOST_WRITE = 12
SRAM_ERROR_CNT = 13
ADD_SMART_ITEMS = 14


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

class shannon_nvme_smart_log_item(StructureBase):
    _fields_ = [
        ('rsv1', c_uint8 * 3),
        ('norm', c_uint8),
        ('rsv2', c_uint8),
        ('item', additional_smart_log_union),
        ('_rp', c_uint8),
    ]

class shannon_nvme_smart_log(StructureBase):
    _fields_ = [
        ('items', shannon_nvme_smart_log_item * ADD_SMART_ITEMS),
        ('vend_spec_resv', c_uint8),
    ]