#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from xt_module.xt_structure import *

SEAGATE_PLUGIN_VERSION_MAJOR = 1
SEAGATE_PLUGIN_VERSION_MINOR = 2
SEAGATE_OCP_PLUGIN_VERSION_MAJOR = 1
SEAGATE_OCP_PLUGIN_VERSION_MINOR = 0

PERSIST_FILE_SIZE = 2764800
ONE_MB = 1048576
PERSIST_CHUNK = 65536
FOUR_KB = 4096
STX_NUM_LEGACY_DRV = 123
NUMBER_EXTENDED_SMART_ATTRIBUTES  = 42
EXTENDED_SMART_VERSION_NONE = 0
EXTENDED_SMART_VERSION_GEN = 1
EXTENDED_SMART_VERSION_VENDOR1 = 2

TELEMETRY_BLOCKS_TO_READ = 8

VS_ATTR_ID_SOFT_READ_ERROR_RATE = 1
VS_ATTR_ID_REALLOCATED_SECTOR_COUNT  = 5
VS_ATTR_ID_POWER_ON_HOURS = 9
VS_ATTR_ID_POWER_FAIL_EVENT_COUNT = 11
VS_ATTR_ID_DEVICE_POWER_CYCLE_COUNT = 12
VS_ATTR_ID_RAW_READ_ERROR_RATE = 13
VS_ATTR_ID_GROWN_BAD_BLOCK_COUNT = 40
VS_ATTR_ID_END_2_END_CORRECTION_COUNT = 41
VS_ATTR_ID_MIN_MAX_WEAR_RANGE_COUNT = 42
VS_ATTR_ID_REFRESH_COUNT = 43
VS_ATTR_ID_BAD_BLOCK_COUNT_USER = 44
VS_ATTR_ID_BAD_BLOCK_COUNT_SYSTEM = 45
VS_ATTR_ID_THERMAL_THROTTLING_STATUS = 46
VS_ATTR_ID_ALL_PCIE_CORRECTABLE_ERROR_COUNT = 47
VS_ATTR_ID_ALL_PCIE_UNCORRECTABLE_ERROR_COUNT = 48
VS_ATTR_ID_INCOMPLETE_SHUTDOWN_COUNT = 49
VS_ATTR_ID_GB_ERASED_LSB = 100
VS_ATTR_ID_GB_ERASED_MSB = 101
VS_ATTR_ID_LIFETIME_ENTERING_PS4_COUNT = 102
VS_ATTR_ID_LIFETIME_ENTERING_PS3_COUNT = 103
VS_ATTR_ID_LIFETIME_DEVSLEEP_EXIT_COUNT = 104
VS_ATTR_ID_RETIRED_BLOCK_COUNT = 170
VS_ATTR_ID_PROGRAM_FAILURE_COUNT = 171
VS_ATTR_ID_ERASE_FAIL_COUNT = 172
VS_ATTR_ID_AVG_ERASE_COUNT = 173
VS_ATTR_ID_UNEXPECTED_POWER_LOSS_COUNT = 174
VS_ATTR_ID_WEAR_RANGE_DELTA = 177
VS_ATTR_ID_SATA_INTERFACE_DOWNSHIFT_COUNT = 183
VS_ATTR_ID_END_TO_END_CRC_ERROR_COUNT = 184
VS_ATTR_ID_UNCORRECTABLE_READ_ERRORS = 188
VS_ATTR_ID_MAX_LIFE_TEMPERATURE = 194
VS_ATTR_ID_RAISE_ECC_CORRECTABLE_ERROR_COUNT = 195
VS_ATTR_ID_UNCORRECTABLE_RAISE_ERRORS = 198
VS_ATTR_ID_DRIVE_LIFE_PROTECTION_STATUS = 230
VS_ATTR_ID_REMAINING_SSD_LIFE  = 231
VS_ATTR_ID_LIFETIME_WRITES_TO_FLASH_LSB = 233
VS_ATTR_ID_LIFETIME_WRITES_TO_FLASH_MSB = 234
VS_ATTR_ID_LIFETIME_WRITES_FROM_HOST_LSB = 241
VS_ATTR_ID_LIFETIME_WRITES_FROM_HOST_MSB = 242
VS_ATTR_ID_LIFETIME_READS_TO_HOST_LSB = 243
VS_ATTR_ID_LIFETIME_READS_TO_HOST_MSB = 244
VS_ATTR_ID_FREE_SPACE = 245
VS_ATTR_ID_TRIM_COUNT_LSB = 250
VS_ATTR_ID_TRIM_COUNT_MSB = 251
VS_ATTR_ID_OP_PERCENTAGE = 252
VS_ATTR_ID_MAX_SOC_LIFE_TEMPERATURE = 253

VS_ATTR_SOFT_READ_ERROR_RATE = 0                # /* 0    OFFSET : 02 -13     bytes */
VS_ATTR_REALLOCATED_SECTOR_COUNT = 1            # /* 1    OFFSET : 14 -25     bytes */
VS_ATTR_POWER_ON_HOURS = 2                      # /* 2    OFFSET : 26 -37     bytes */
VS_ATTR_POWER_FAIL_EVENT_COUNT = 3              # /* 3    OFFSET : 38 -49     bytes */
VS_ATTR_DEVICE_POWER_CYCLE_COUNT = 4            # /* 4    OFFSET : 50 -61     bytes */
VS_ATTR_GB_ERASED = 5                           # /* 5    OFFSET : 62 -73     bytes */
VS_ATTR_LIFETIME_DEVSLEEP_EXIT_COUNT = 6        # /* 6    OFFSET : 74 -85     bytes */
VS_ATTR_LIFETIME_ENTERING_PS4_COUNT = 7         # /* 7    OFFSET : 86 -97     bytes */
VS_ATTR_LIFETIME_ENTERING_PS3_COUNT = 8         # /* 8    OFFSET : 98 -109    bytes */
VS_ATTR_RETIRED_BLOCK_COUNT = 9                 # /* 9    OFFSET : 110 -121   bytes */
VS_ATTR_PROGRAM_FAILURE_COUNT = 10              # /* 10   OFFSET : 122 -133   bytes */
VS_ATTR_ERASE_FAIL_COUNT = 11                   # /* 11   OFFSET : 134 -145   bytes */
VS_ATTR_AVG_ERASE_COUNT = 12                    # /* 12   OFFSET : 146 -157   bytes */
VS_ATTR_UNEXPECTED_POWER_LOSS_COUNT = 13        # /* 13   OFFSET : 158 -169   bytes */
VS_ATTR_WEAR_RANGE_DELTA = 14                   # /* 14   OFFSET : 170 -181   bytes */
VS_ATTR_SATA_INTERFACE_DOWNSHIFT_COUNT = 15     # /* 15   OFFSET : 182 -193   bytes */
VS_ATTR_END_TO_END_CRC_ERROR_COUNT = 16         # /* 16   OFFSET : 194 -205   bytes */
VS_ATTR_MAX_LIFE_TEMPERATURE = 17               # /* 17   OFFSET : 206 -217   bytes */
VS_ATTR_UNCORRECTABLE_RAISE_ERRORS = 18         # /* 18   OFFSET : 218 -229   bytes */
VS_ATTR_DRIVE_LIFE_PROTECTION_STATUS = 19       # /* 19   OFFSET : 230 -241   bytes */
VS_ATTR_REMAINING_SSD_LIFE = 20                 # /* 20   OFFSET : 242 -253   bytes */
VS_ATTR_LIFETIME_WRITES_TO_FLASH = 21           # /* 21   OFFSET : 254 -265   bytes */
VS_ATTR_LIFETIME_WRITES_FROM_HOST = 22          # /* 22   OFFSET : 266 -277   bytes */
VS_ATTR_LIFETIME_READS_TO_HOST = 23             # /* 23   OFFSET : 278 -289   bytes */
VS_ATTR_FREE_SPACE = 24                         # /* 24   OFFSET : 290 -301   bytes */
VS_ATTR_TRIM_COUNT_LSB = 25                     # /* 25   OFFSET : 302 -313   bytes */
VS_ATTR_TRIM_COUNT_MSB = 26                     # /* 26   OFFSET : 314 -325   bytes */
VS_ATTR_OP_PERCENTAGE = 27                      # /* 27   OFFSET : 326 -337   bytes */
VS_ATTR_RAISE_ECC_CORRECTABLE_ERROR_COUNT = 28 	# /* 28   OFFSET : 338 -349   bytes */
VS_ATTR_UNCORRECTABLE_ECC_ERRORS = 29           # /* 29   OFFSET : 350 -361   bytes */
VS_ATTR_LIFETIME_WRITES0_TO_FLASH = 30          # /* 30   OFFSET : 362-372    bytes */
VS_ATTR_LIFETIME_WRITES1_TO_FLASH = 31          # /* 31   OFFSET : 374-385    bytes */
VS_ATTR_LIFETIME_WRITES0_FROM_HOST = 32         # /* 32   OFFSET : 386-397    bytes */
VS_ATTR_LIFETIME_WRITES1_FROM_HOST = 33         # /* 33   OFFSET : 398-409    bytes */
VS_ATTR_LIFETIME_READ0_FROM_HOST = 34           # /* 34   OFFSET : 410-421    bytes */
VS_ATTR_LIFETIME_READ1_FROM_HOST = 35           # /* 35   OFFSET : 422-433    bytes */
VS_ATTR_PCIE_PHY_CRC_ERROR = 36                 # /* 36   OFFSET : 434-445    bytes */
VS_ATTR_BAD_BLOCK_COUNT_SYSTEM = 37             # /* 37   OFFSET : 446-457    bytes */
VS_ATTR_BAD_BLOCK_COUNT_USER = 38               # /* 38   OFFSET : 458-469    bytes */
VS_ATTR_THERMAL_THROTTLING_STATUS = 39          # /* 39   OFFSET : 470-481    bytes */
VS_ATTR_POWER_CONSUMPTION = 40                  # /* 40   OFFSET : 482-493    bytes */
VS_ATTR_MAX_SOC_LIFE_TEMPERATURE = 41           # /* 41   OFFSET : 494-505    bytes */
VS_MAX_ATTR_NUMBER = 42

stx_jag_pan_mn = ["ST1000KN0002", "ST1000KN0012", "ST2000KN0002", "ST2000KN0012", "ST4000KN0002", "XP1600HE10002",
                  "XP1600HE10012", "XP1600HE30002", "XP1600HE30012", "XP1920LE10002", "XP1920LE10012", "XP1920LE30002",
                  "XP1920LE30012", "XP3200HE10002", "XP3200HE10012", "XP3840LE10002", "XP3840LE10012", "XP400HE30002",
                  "XP400HE30012", "XP400HE30022", "XP400HE30032", "XP480LE30002", "XP480LE30012", "XP480LE30022",
                  "XP480LE30032", "XP800HE10002", "XP800HE10012", "XP800HE30002", "XP800HE30012", "XP800HE30022",
                  "XP800HE30032", "XP960LE10002", "XP960LE10012", "XP960LE30002", "XP960LE30012", "XP960LE30022",
                  "XP960LE30032", "XP256LE30011", "XP256LE30021", "XP7680LE80002", "XP7680LE80003", "XP15360LE80003",
                  "XP30720LE80003", "XP7200-1A2048", "XP7200-1A4096", "XP7201-2A2048", "XP7201-2A4096", "XP7200-1A8192",
                  "ST1000HM0021", "ST1000HM0031", "ST1000HM0061", "ST1000HM0071", "ST1000HM0081", "ST1200HM0001",
                  "ST1600HM0031", "ST1800HM0001", "ST1800HM0011", "ST2000HM0011", "ST2000HM0031", "ST400HM0061",
                  "ST400HM0071", "ST500HM0021", "ST500HM0031", "ST500HM0061", "ST500HM0071", "ST500HM0081",
                  "ST800HM0061", "ST800HM0071", "ST1600HM0011", "ST1600KN0001", "ST1600KN0011", "ST1920HM0001",
                  "ST1920KN0001", "ST1920KN0011", "ST400HM0021", "ST400KN0001", "ST400KN0011", "ST480HM0001",
                  "ST480KN0001", "ST480KN0011", "ST800HM0021", "ST800KN0001", "ST800KN0011", "ST960HM0001",
                  "ST960KN0001", "ST960KN0011", "XF1441-1AA251024", "XF1441-1AA252048", "XF1441-1AA25512", "XF1441-1AB251024",
                  "XF1441-1AB252048", "XF1441-1AB25512", "XF1441-1BA251024", "XF1441-1BA252048", "XF1441-1BA25512", "XF1441-1BB251024",
                  "XF1441-1BB252048", "XF1441-1BB25512", "ST400HM0031", "ST400KN0021", "ST400KN0031", "ST480HM0011",
                  "ST480KN0021", "ST480KN0031", "ST800HM0031", "ST800KN0021", "ST800KN0031", "ST960HM0011",
                  "ST960KN0021", "ST960KN0031", "XM1441-1AA111024", "XM1441-1AA112048", "XM1441-1AA11512", "XM1441-1AA801024",
                  "XM1441-1AA80512", "XM1441-1AB111024", "XM1441-1AB112048", "XM1441-1BA111024", "XM1441-1BA112048", "XM1441-1BA11512",
                  "XM1441-1BA801024", "XM1441-1BA80512", "XM1441-1BB112048"]

class log_page_map_entry(StructureBase):
    _fields_ = [
        ('log_page_id', c_uint32),
        ('log_page_signature', c_uint32),
        ('log_page_version', c_uint32),
    ]
MAX_SUPPORTED_LOG_PAGE_ENTRIES = (4096 - sizeof(c_uint32)) // sizeof(log_page_map_entry)

class stx_log_page_map(StructureBase):
    _fields_ = [
        ('num_log_pages', c_uint32),
        ('log_page_entry', log_page_map_entry * MAX_SUPPORTED_LOG_PAGE_ENTRIES),
    ]

class stx_smart_vendor_specific(StructureBase):
    _fields_ = [
        ('attribute_number', c_uint8),
        ('smart_status', c_uint16),
        ('nominal_value', c_uint8),
        ('lifetime_worst_value', c_uint8),
        ('raw0_3', c_uint32),
        ('waw_high', c_uint8 * 3),
    ]

class stx_extended_smart_info(StructureBase):
    _fields_ = [
        ('version', c_uint16),
        ('vendor_specific', stx_smart_vendor_specific * NUMBER_EXTENDED_SMART_ATTRIBUTES),
        ('vendor_specific_reserved', c_uint8 * 6),
    ]

class vendor_smart_attribute_data(StructureBase):
    _fields_ = [
        ('attribute_number', c_uint8),
        ('rsvd', c_uint8 * 3),
        ('ls_dword', c_uint32),
        ('ms_dword', c_uint32),
    ]

class stx_nvme_temetry_log_hdr(StructureBase):
    _fields_ = [
        ('log_id', c_uint8),
        ('rsvd1', c_uint8 * 4),
        ('ieee_id', c_uint8 * 3),
        ('tele_data_area1', c_uint16),
        ('tele_data_area2', c_uint16),
        ('tele_data_area3', c_uint16),
        ('rsvd2', c_uint8 * 368),
        ('tele_data_aval', c_uint8),
        ('tele_data_gen_num', c_uint8),
        ('reason_identifier', c_uint8 * 128),
    ]

class U128(Structure):
    _fields_ = [
        ('ls__u64', c_uint64),
        ('ms__u64', c_uint64),
    ]

class stx_vendor_log_page_cf_attr(StructureBase):
    _fields_ = [
        ('super_cap_current_temperature', c_uint16),
        ('super_cap_maximum_temperature', c_uint16),
        ('super_cap_status', c_uint8),
        ('reserved', c_uint8 * 3),
        ('data_units_read_to_dram_namespace', U128),
        ('data_units_written_to_dram_namespace', U128),
        ('dram_correctable_error_count', c_uint64),
        ('dram_uncorrectable_error_count', c_uint64),
    ]
class stx_vendor_log_page_cf(StructureBase):
    _fields_ = [
        ('attr_cf', stx_vendor_log_page_cf_attr),
        ('reserved', c_uint8 * 456),
    ]

class stx_ext_smart_log_page_c0(StructureBase):
    _fields_ = [
        ('phy_media_units_wrt', U128),
        ('phy_media_units_rd', U128),
        ('bad_usr_nand_blocks', c_uint64),
        ('bad_sys_nand_blocks', c_uint64),
        ('xor_recovery_cnt', c_uint64),
        ('uc_rd_ec', c_uint64),
        ('soft_ecc_ec', c_uint64),
        ('etoe_crr_cnt', c_uint64),
        ('sys_data_used', c_uint64, 8),
        ('refresh_count', c_uint64, 56),
        ('usr_data_erase_cnt', c_uint64),
        ('thermal_throttling', c_uint16),
        ('dssd_spec_ver_errata', c_uint8),
        ('dssd_spec_ver_point', c_uint16),
        ('dssd_spec_ver_minor', c_uint16),
        ('dssd_spec_ver_major', c_uint16),
        ('pcie_corr_ec', c_uint64),
        ('incomplete_shutdowns', c_uint32),
        ('rsvd1', c_uint32 * 4),
        ('free_blocks', c_uint8),
        ('rsvd2', c_uint8 * 7),
        ('cap_health', c_uint16),
        ('nvme_errata_ver', c_uint8),
        ('rsvd3', c_uint8 * 5),
        ("unaligned_io", c_uint64),
        ("sec_ver_num", c_uint64),
        ("total_nuse", c_uint64),
        ("plp_start_cnt", U128),
        ("endurance_estimate", U128),
        ("pcie_link_ret_cnt", c_uint64),
        ("pow_state_change_cnt", c_uint64),
        ("rsvd4", c_uint8 * 286),
        ("log_page_ver", c_uint16),
        ("log_page_guid", U128),

    ]
class stx_pcie_error_log_page(StructureBase):
    _fields_ = [
        ('version', c_uint32),
        ('bad_dllp_err_cnt', c_uint32),
        ('bad_tlp_err_cnt', c_uint32),
        ('rcvr_err_cnt', c_uint32),
        ('replay_to_err_cnt', c_uint32),
        ('replay_num_rollover_err_cnt', c_uint32),
        ('fc_protocol_err_cnt', c_uint32),
        ('dllp_protocol_err_cnt', c_uint32),
        ('cmpltn_to_err_cnt', c_uint32),
        ('rcvr_q_overflow_err_cnt', c_uint32),
        ('unexpected_cpl_tlp_err_cnt', c_uint32),
        ('cpl_tlp_ure_err_cnt', c_uint32),
        ('cpl_tlp_ca_err_cnt', c_uint32),
        ('req_ca_err_cnt', c_uint32),
        ('req_ur_err_cnt', c_uint32),
        ('ecrc_err_cnt', c_uint32),
        ('malformed_tlp_err_cnt', c_uint32),
        ('cpl_tlp_poisoned_err_cnt', c_uint32),
        ('mem_rd_tlp_poisoned_err_cnt', c_uint32),

    ]

class stx_fw_activ_his_ele(StructureBase):
    _fields_ = [
        ('entry_ver_num', c_uint8),
        ('entry_len', c_uint8),
        ('rsv1', c_uint16),
        ('fw_activ_cnt', c_uint16),
        ('time_stamp', c_uint64),
        ('rsv2', c_uint64),
        ('pow_cycle_cnt', c_uint64),
        ('previous_fw', c_uint8 * 8),
        ('new_fw', c_uint8 *8),
        ('slot_num', c_uint8),
        ('commit_action_type', c_uint8),
        ('result', c_uint16),
        ('rsv3', c_uint8 * 14),
    ]

class stx_fw_activ_history_log_page(StructureBase):
    _fields_ = [
        ('log_id', c_uint8),
        ('rsv1', c_uint8 * 3),
        ('num_valid_fw_act_his_ent', c_uint32),
        ('fw_act_his_ent', stx_fw_activ_his_ele * 20),
        ('rsv2', c_uint8 * 2790),
        ('log_page_ver', c_uint16),
        ('log_page_guid', c_uint8 * 16),
    ]