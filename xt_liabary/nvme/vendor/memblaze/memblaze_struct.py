#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from xt_module.xt_structure import *
SMART_INFO_OLD_SIZE = 512
SMART_INFO_NEW_SIZE = 4096
ID_SIZE = 3
NM_SIZE = 2
RAW_SIZE = 7
RAISIN_SI_VD_PROGRAM_FAIL_ID = 0xAB
RAISIN_SI_VD_ERASE_FAIL_ID = 0xAC
RAISIN_SI_VD_WEARLEVELING_COUNT_ID = 0xAD
RAISIN_SI_VD_E2E_DECTECTION_COUNT_ID = 0xB8
RAISIN_SI_VD_PCIE_CRC_ERR_COUNT_ID = 0xC7
RAISIN_SI_VD_TIMED_WORKLOAD_MEDIA_WEAR_ID = 0xE2
RAISIN_SI_VD_TIMED_WORKLOAD_HOST_READ_ID = 0xE3
RAISIN_SI_VD_TIMED_WORKLOAD_TIMER_ID = 0xE4
RAISIN_SI_VD_THERMAL_THROTTLE_STATUS_ID = 0xEA
RAISIN_SI_VD_RETRY_BUFF_OVERFLOW_COUNT_ID = 0xF0
RAISIN_SI_VD_PLL_LOCK_LOSS_COUNT_ID = 0xF3
RAISIN_SI_VD_TOTAL_WRITE_ID = 0xF4
RAISIN_SI_VD_HOST_WRITE_ID = 0xF5
RAISIN_SI_VD_SYSTEM_AREA_LIFE_LEFT_ID = 0xF6
RAISIN_SI_VD_TOTAL_READ_ID = 0xFA
RAISIN_SI_VD_TEMPT_SINCE_BORN_ID = 0xE7
RAISIN_SI_VD_POWER_CONSUMPTION_ID = 0xE8
RAISIN_SI_VD_TEMPT_SINCE_BOOTUP_ID = 0xAF
RAISIN_SI_VD_POWER_LOSS_PROTECTION_ID = 0xEC
RAISIN_SI_VD_READ_FAIL_ID = 0xF2
RAISIN_SI_VD_THERMAL_THROTTLE_TIME_ID = 0xEB
RAISIN_SI_VD_FLASH_MEDIA_ERROR_ID = 0xED
RAISIN_SI_VD_PROGRAM_FAIL = 0
RAISIN_SI_VD_ERASE_FAIL = 1
RAISIN_SI_VD_WEARLEVELING_COUNT = 2
RAISIN_SI_VD_E2E_DECTECTION_COUNT = 3
RAISIN_SI_VD_PCIE_CRC_ERR_COUNT = 4
RAISIN_SI_VD_TIMED_WORKLOAD_MEDIA_WEAR = 5
RAISIN_SI_VD_TIMED_WORKLOAD_HOST_READ = 6
RAISIN_SI_VD_TIMED_WORKLOAD_TIMER = 7
RAISIN_SI_VD_THERMAL_THROTTLE_STATUS = 8
RAISIN_SI_VD_RETRY_BUFF_OVERFLOW_COUNT = 9
RAISIN_SI_VD_PLL_LOCK_LOSS_COUNT = 10
RAISIN_SI_VD_TOTAL_WRITE = 11
RAISIN_SI_VD_HOST_WRITE = 12
RAISIN_SI_VD_SYSTEM_AREA_LIFE_LEFT = 13
RAISIN_SI_VD_TOTAL_READ = 14
RAISIN_SI_VD_TEMPT_SINCE_BORN = 15
RAISIN_SI_VD_POWER_CONSUMPTION = 16
RAISIN_SI_VD_TEMPT_SINCE_BOOTUP = 17
RAISIN_SI_VD_POWER_LOSS_PROTECTION = 18
RAISIN_SI_VD_READ_FAIL = 19
RAISIN_SI_VD_THERMAL_THROTTLE_TIME = 20
RAISIN_SI_VD_FLASH_MEDIA_ERROR = 21
RAISIN_SI_VD_SMART_INFO_ITEMS_MAX = 22
TOTAL_WRITE = 0
TOTAL_READ = 1
THERMAL_THROTTLE = 2
TEMPT_SINCE_RESET = 3
POWER_CONSUMPTION = 4
TEMPT_SINCE_BOOTUP = 5
POWER_LOSS_PROTECTION = 6
WEARLEVELING_COUNT = 7
HOST_WRITE = 8
THERMAL_THROTTLE_CNT = 9
CORRECT_PCIE_PORT0 = 10
CORRECT_PCIE_PORT1 = 11
REBUILD_FAIL = 12
ERASE_FAIL = 13
PROGRAM_FAIL = 14
READ_FAIL = 15
NR_SMART_ITEMS = 22

class temperature(StructureBase):
    _fields_ = [
        ("max", c_uint16),
        ("min", c_uint16),
        ("curr", c_uint16),
    ]

class power(StructureBase):
    _fields_ = [
        ("max", c_uint16),
        ("min", c_uint16),
        ("curr", c_uint16),
    ]
class thermal_throttle_mb(StructureBase):
    _fields_ = [
        ("on", c_uint8),
        ("count", c_uint32),
    ]
class temperature_p(StructureBase):
    _fields_ = [
        ("max", c_uint16),
        ("min", c_uint16),
        ("curr", c_uint16),
    ]
class power_loss_protection(StructureBase):
    _fields_ = [
        ("curr", c_uint8),
    ]

class wearleveling_count(StructureBase):
    _fields_ = [
        ("min", c_uint16),
        ("max", c_uint16),
        ("avg", c_uint16),
    ]

class thermal_throttle_cnt(StructureBase):
    _fields_ = [
        ("active", c_uint8),
        ("count", c_uint32),
    ]

class smart_log_union(Union):
    _fields_ = [
        ("rawval", c_uint8 * 6),
        ("power", power),
        ("temperature", temperature),
        ("thermal_throttle_mb", thermal_throttle_mb),
        ("temperature_p", temperature_p),
        ("power_loss_protection", power_loss_protection),
        ("wearleveling_count", wearleveling_count),
        ("thermal_throttle_cnt", thermal_throttle_cnt),
    ]

class nvme_smart_log_item(StructureBase):
    _fields_ = [
        ("id", c_uint8 * 3),
        ("nmval", c_uint16),
        ("item", smart_log_union),
        ("resv", c_uint8),
    ]

class memblaze_nvme_smart_log(StructureBase):
    _fields_ = [
        ("items", nvme_smart_log_item * NR_SMART_ITEMS),
        ("resv", c_uint8 * (SMART_INFO_OLD_SIZE - 12 * NR_SMART_ITEMS)),
    ]

class nvme_p4_smart_log_item(StructureBase):
    _fields_ = [
        ("id", c_uint8 * ID_SIZE),
        ("nmval", c_uint8 * NM_SIZE),
        ("rawVal", c_uint8 * RAW_SIZE),
    ]

class memblaze_nvme_p4_smart_log(StructureBase):
    _fields_ = [
        ("item", nvme_p4_smart_log_item * NR_SMART_ITEMS),
        ("resv", c_uint8 * (SMART_INFO_NEW_SIZE - 12 * NR_SMART_ITEMS)),
    ]
