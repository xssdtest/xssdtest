#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from xt_module.xt_structure import *

WDC_STATUS_SUCCESS = 0
WDC_STATUS_FAILURE = -1
WDC_STATUS_INSUFFICIENT_MEMORY = -2
WDC_STATUS_INVALID_PARAMETER = -3
WDC_STATUS_FILE_SIZE_ZERO = -27
WDC_STATUS_UNABLE_TO_WRITE_ALL_DATA = -34
WDC_STATUS_DIR_ALREADY_EXISTS = -36
WDC_STATUS_PATH_NOT_FOUND = -37
WDC_STATUS_CREATE_DIRECTORY_FAILED = -38
WDC_STATUS_DELETE_DIRECTORY_FAILED = -39
WDC_STATUS_UNABLE_TO_OPEN_FILE = -41
WDC_STATUS_UNABLE_TO_ARCHIVE_EXCEEDED_FILES_LIMIT = -256
WDC_STATUS_NO_DATA_FILE_AVAILABLE_TO_ARCHIVE = -271
WDC_NVME_FIRMWARE_REV_LEN = 9
WDC_SERIAL_NO_LEN = 20
SECONDS_IN_MIN = 60
MAX_PATH_LEN = 256
WRITE_SIZE = sizeof(c_int8 * 4096)
WDC_NVME_SUBCMD_SHIFT = 8
WDC_NVME_LOG_SIZE_DATA_LEN = 0x08
WDC_NVME_LOG_SIZE_HDR_LEN = 0x08
WDC_OPENFLEX_MI_DEVICE_MODEL = "OpenFlex"
WDC_RESULT_MORE_DATA = 0x80000000
WDC_RESULT_NOT_AVAILABLE = 0x7FFFFFFF
WDC_NVME_VID = 0x1c58
WDC_NVME_VID_2 = 0x1b96
WDC_NVME_SNDK_VID = 0x15b7
WDC_NVME_SN100_DEV_ID = 0x0003
WDC_NVME_SN200_DEV_ID = 0x0023
WDC_NVME_SN630_DEV_ID = 0x2200
WDC_NVME_SN630_DEV_ID_1 = 0x2201
WDC_NVME_SN840_DEV_ID = 0x2300
WDC_NVME_SN840_DEV_ID_1 = 0x2500
WDC_NVME_SN640_DEV_ID = 0x2400
WDC_NVME_SN640_DEV_ID_1 = 0x2401
WDC_NVME_SN640_DEV_ID_2 = 0x2402
WDC_NVME_SN640_DEV_ID_3 = 0x2404
WDC_NVME_ZN540_DEV_ID = 0x2600
WDC_NVME_SN540_DEV_ID = 0x2610
WDC_NVME_SN650_DEV_ID = 0x2700
WDC_NVME_SN650_DEV_ID_1 = 0x2701
WDC_NVME_SN650_DEV_ID_2 = 0x2702
WDC_NVME_SN650_DEV_ID_3 = 0x2720
WDC_NVME_SN650_DEV_ID_4 = 0x2721
WDC_NVME_SN655_DEV_ID = 0x2722
WDC_NVME_SN860_DEV_ID = 0x2730
WDC_NVME_SN660_DEV_ID = 0x2704
WDC_NVME_SN560_DEV_ID_1 = 0x2712
WDC_NVME_SN560_DEV_ID_2 = 0x2713
WDC_NVME_SN560_DEV_ID_3 = 0x2714
WDC_NVME_SN861_DEV_ID = 0x2750
WDC_NVME_SN861_DEV_ID_1 = 0x2751
WDC_NVME_SN550_DEV_ID = 0x2708
WDC_NVME_SXSLCL_DEV_ID = 0x2001
WDC_NVME_SN520_DEV_ID = 0x5003
WDC_NVME_SN520_DEV_ID_1 = 0x5004
WDC_NVME_SN520_DEV_ID_2 = 0x5005
WDC_NVME_SN530_DEV_ID_1 = 0x5007
WDC_NVME_SN530_DEV_ID_2 = 0x5008
WDC_NVME_SN530_DEV_ID_3 = 0x5009
WDC_NVME_SN530_DEV_ID_4 = 0x500b
WDC_NVME_SN530_DEV_ID_5 = 0x501d
WDC_NVME_SN350_DEV_ID = 0x5019
WDC_NVME_SN570_DEV_ID = 0x501A
WDC_NVME_SN850X_DEV_ID = 0x5030
WDC_NVME_SN5000_DEV_ID_1 = 0x5034
WDC_NVME_SN5000_DEV_ID_2 = 0x5035
WDC_NVME_SN5000_DEV_ID_3 = 0x5036
WDC_NVME_SN5000_DEV_ID_4 = 0x504A
WDC_NVME_SN7000S_DEV_ID_1 = 0x5039
WDC_NVME_SN7150_DEV_ID_1 = 0x503b
WDC_NVME_SN7150_DEV_ID_2 = 0x503c
WDC_NVME_SN7150_DEV_ID_3 = 0x503d
WDC_NVME_SN7150_DEV_ID_4 = 0x503e
WDC_NVME_SN7150_DEV_ID_5 = 0x503f
WDC_NVME_SN7100_DEV_ID_1 = 0x5043
WDC_NVME_SN7100_DEV_ID_2 = 0x5044
WDC_NVME_SN7100_DEV_ID_3 = 0x5045
WDC_NVME_SN8000S_DEV_ID = 0x5049
WDC_NVME_SN720_DEV_ID = 0x5002
WDC_NVME_SN730_DEV_ID = 0x5006
WDC_NVME_SN740_DEV_ID = 0x5015
WDC_NVME_SN740_DEV_ID_1 = 0x5016
WDC_NVME_SN740_DEV_ID_2 = 0x5017
WDC_NVME_SN740_DEV_ID_3 = 0x5025
WDC_NVME_SN340_DEV_ID = 0x500d
WDC_NVME_ZN350_DEV_ID = 0x5010
WDC_NVME_ZN350_DEV_ID_1 = 0x5018
WDC_NVME_SN810_DEV_ID = 0x5011
WDC_NVME_SN820CL_DEV_ID = 0x5037
WDC_DRIVE_CAP_CAP_DIAG = 0x0000000000000001
WDC_DRIVE_CAP_INTERNAL_LOG = 0x0000000000000002
WDC_DRIVE_CAP_C1_LOG_PAGE = 0x0000000000000004
WDC_DRIVE_CAP_CA_LOG_PAGE = 0x0000000000000008
WDC_DRIVE_CAP_D0_LOG_PAGE = 0x0000000000000010
WDC_DRIVE_CAP_DRIVE_STATUS = 0x0000000000000020
WDC_DRIVE_CAP_CLEAR_ASSERT = 0x0000000000000040
WDC_DRIVE_CAP_CLEAR_PCIE = 0x0000000000000080
WDC_DRIVE_CAP_RESIZE = 0x0000000000000100
WDC_DRIVE_CAP_NAND_STATS = 0x0000000000000200
WDC_DRIVE_CAP_DRIVE_LOG = 0x0000000000000400
WDC_DRIVE_CAP_CRASH_DUMP = 0x0000000000000800
WDC_DRIVE_CAP_PFAIL_DUMP = 0x0000000000001000
WDC_DRIVE_CAP_FW_ACTIVATE_HISTORY = 0x0000000000002000
WDC_DRIVE_CAP_CLEAR_FW_ACT_HISTORY = 0x0000000000004000
WDC_DRVIE_CAP_DISABLE_CTLR_TELE_LOG = 0x0000000000008000
WDC_DRIVE_CAP_REASON_ID = 0x0000000000010000
WDC_DRIVE_CAP_LOG_PAGE_DIR = 0x0000000000020000
WDC_DRIVE_CAP_NS_RESIZE = 0x0000000000040000
WDC_DRIVE_CAP_INFO = 0x0000000000080000
WDC_DRIVE_CAP_C0_LOG_PAGE = 0x0000000000100000
WDC_DRIVE_CAP_TEMP_STATS = 0x0000000000200000
WDC_DRIVE_CAP_VUC_CLEAR_PCIE = 0x0000000000400000
WDC_DRIVE_CAP_VU_FID_CLEAR_PCIE = 0x0000000000800000
WDC_DRIVE_CAP_FW_ACTIVATE_HISTORY_C2 = 0x0000000001000000
WDC_DRIVE_CAP_VU_FID_CLEAR_FW_ACT_HISTORY = 0x0000000002000000
WDC_DRIVE_CAP_CLOUD_SSD_VERSION = 0x0000000004000000
WDC_DRIVE_CAP_PCIE_STATS = 0x0000000008000000
WDC_DRIVE_CAP_HW_REV_LOG_PAGE = 0x0000000010000000
WDC_DRIVE_CAP_C3_LOG_PAGE = 0x0000000020000000
WDC_DRIVE_CAP_CLOUD_BOOT_SSD_VERSION = 0x0000000040000000
WDC_DRIVE_CAP_CLOUD_LOG_PAGE = 0x0000000080000000
WDC_DRIVE_CAP_DRIVE_ESSENTIALS = 0x0000000100000000
WDC_DRIVE_CAP_DUI_DATA = 0x0000000200000000
WDC_SN730B_CAP_VUC_LOG = 0x0000000400000000
WDC_DRIVE_CAP_DUI = 0x0000000800000000
WDC_DRIVE_CAP_PURGE = 0x0000001000000000
WDC_DRIVE_CAP_OCP_C1_LOG_PAGE = 0x0000002000000000
WDC_DRIVE_CAP_OCP_C4_LOG_PAGE = 0x0000004000000000
WDC_DRIVE_CAP_OCP_C5_LOG_PAGE = 0x0000008000000000
WDC_DRIVE_CAP_DEVICE_WAF = 0x0000010000000000
WDC_DRIVE_CAP_SET_LATENCY_MONITOR = 0x0000020000000000
WDC_DRIVE_CAP_SMART_LOG_MASK = (WDC_DRIVE_CAP_C0_LOG_PAGE | WDC_DRIVE_CAP_C1_LOG_PAGE | WDC_DRIVE_CAP_CA_LOG_PAGE | WDC_DRIVE_CAP_D0_LOG_PAGE)
WDC_DRIVE_CAP_CLEAR_PCIE_MASK = (WDC_DRIVE_CAP_CLEAR_PCIE | WDC_DRIVE_CAP_VUC_CLEAR_PCIE | WDC_DRIVE_CAP_VU_FID_CLEAR_PCIE)
WDC_DRIVE_CAP_FW_ACTIVATE_HISTORY_MASK = (WDC_DRIVE_CAP_FW_ACTIVATE_HISTORY | WDC_DRIVE_CAP_FW_ACTIVATE_HISTORY_C2)
WDC_DRIVE_CAP_CLEAR_FW_ACT_HISTORY_MASK = (WDC_DRIVE_CAP_CLEAR_FW_ACT_HISTORY | WDC_DRIVE_CAP_VU_FID_CLEAR_FW_ACT_HISTORY)
WDC_DRIVE_CAP_INTERNAL_LOG_MASK = (WDC_DRIVE_CAP_INTERNAL_LOG | WDC_DRIVE_CAP_DUI | WDC_DRIVE_CAP_DUI_DATA | WDC_SN730B_CAP_VUC_LOG)
SN730_NVME_GET_LOG_OPCODE = 0xc2
SN730_GET_FULL_LOG_LENGTH = 0x00080009
SN730_GET_KEY_LOG_LENGTH = 0x00090009
SN730_GET_COREDUMP_LOG_LENGTH = 0x00120009
SN730_GET_EXTENDED_LOG_LENGTH = 0x00420009
SN730_GET_FULL_LOG_SUBOPCODE = 0x00010009
SN730_GET_KEY_LOG_SUBOPCODE = 0x00020009
SN730_GET_CORE_LOG_SUBOPCODE = 0x00030009
SN730_GET_EXTEND_LOG_SUBOPCODE = 0x00040009
SN730_LOG_CHUNK_SIZE = 0x1000
WDC_CUSTOMER_ID_GN = 0x0001
WDC_CUSTOMER_ID_GD = 0x0101
WDC_CUSTOMER_ID_BD = 0x1009
WDC_CUSTOMER_ID_0x1005 = 0x1005
WDC_CUSTOMER_ID_0x1004 = 0x1004
WDC_CUSTOMER_ID_0x1008 = 0x1008
WDC_CUSTOMER_ID_0x1304 = 0x1304
WDC_INVALID_CUSTOMER_ID = -1
WDC_ALL_PAGE_MASK = 0xFFFF
WDC_C0_PAGE_MASK = 0x0001
WDC_C1_PAGE_MASK = 0x0002
WDC_CA_PAGE_MASK = 0x0004
WDC_D0_PAGE_MASK = 0x0008
WDC_NVME_DRIVE_RESIZE_OPCODE = 0xCC
WDC_NVME_DRIVE_RESIZE_CMD = 0x03
WDC_NVME_DRIVE_RESIZE_SUBCMD = 0x01
WDC_NVME_NAMESPACE_RESIZE_OPCODE = 0xFB
WDC_NVME_DRIVE_INFO_OPCODE = 0xC6
WDC_NVME_DRIVE_INFO_CMD = 0x22
WDC_NVME_DRIVE_INFO_SUBCMD = 0x06
WDC_NVME_PCIE_STATS_OPCODE = 0xD1
WDC_NVME_CAP_DIAG_HEADER_TOC_SIZE = WDC_NVME_LOG_SIZE_DATA_LEN
WDC_NVME_CAP_DIAG_OPCODE = 0xE6
WDC_NVME_CAP_DIAG_CMD_OPCODE = 0xC6
WDC_NVME_CAP_DIAG_SUBCMD = 0x00
WDC_NVME_CAP_DIAG_CMD = 0x00
WDC_NVME_CRASH_DUMP_TYPE = 1
WDC_NVME_PFAIL_DUMP_TYPE = 2
WDC_NVME_CAP_DUI_HEADER_SIZE = 0x400
WDC_NVME_CAP_DUI_OPCODE = 0xFA
WDC_NVME_CAP_DUI_DISABLE_IO = 0x01
WDC_NVME_DUI_MAX_SECTION = 0x3A
WDC_NVME_DUI_MAX_SECTION_V2 = 0x26
WDC_NVME_DUI_MAX_SECTION_V3 = 0x23
WDC_NVME_DUI_MAX_DATA_AREA = 0x05
WDC_NVME_SN730_SECTOR_SIZE = 512
WDC_TELEMETRY_TYPE_NONE = 0x0
WDC_TELEMETRY_TYPE_HOST = 0x1
WDC_TELEMETRY_TYPE_CONTROLLER = 0x2
WDC_TELEMETRY_HEADER_LENGTH = 512
WDC_TELEMETRY_BLOCK_SIZE = 512
WDC_NVME_CRASH_DUMP_SIZE_DATA_LEN = WDC_NVME_LOG_SIZE_DATA_LEN
WDC_NVME_CRASH_DUMP_SIZE_NDT = 0x02
WDC_NVME_CRASH_DUMP_SIZE_CMD = 0x20
WDC_NVME_CRASH_DUMP_SIZE_SUBCMD = 0x03
WDC_NVME_CRASH_DUMP_OPCODE = WDC_NVME_CAP_DIAG_CMD_OPCODE
WDC_NVME_CRASH_DUMP_CMD = 0x20
WDC_NVME_CRASH_DUMP_SUBCMD = 0x04
WDC_NVME_PF_CRASH_DUMP_SIZE_DATA_LEN = WDC_NVME_LOG_SIZE_HDR_LEN
WDC_NVME_PF_CRASH_DUMP_SIZE_NDT = 0x02
WDC_NVME_PF_CRASH_DUMP_SIZE_CMD = 0x20
WDC_NVME_PF_CRASH_DUMP_SIZE_SUBCMD = 0x05
WDC_NVME_PF_CRASH_DUMP_OPCODE = WDC_NVME_CAP_DIAG_CMD_OPCODE
WDC_NVME_PF_CRASH_DUMP_CMD = 0x20
WDC_NVME_PF_CRASH_DUMP_SUBCMD = 0x06
WDC_NVME_DRIVE_LOG_SIZE_OPCODE =  WDC_NVME_CAP_DIAG_CMD_OPCODE
WDC_NVME_DRIVE_LOG_SIZE_DATA_LEN = WDC_NVME_LOG_SIZE_DATA_LEN
WDC_NVME_DRIVE_LOG_SIZE_NDT = 0x02
WDC_NVME_DRIVE_LOG_SIZE_CMD = 0x20
WDC_NVME_DRIVE_LOG_SIZE_SUBCMD = 0x01
WDC_NVME_DRIVE_LOG_OPCODE = WDC_NVME_CAP_DIAG_CMD_OPCODE
WDC_NVME_DRIVE_LOG_CMD = 0x20
WDC_NVME_DRIVE_LOG_SUBCMD = 0x00
WDC_NVME_PURGE_CMD_OPCODE = 0xDD
WDC_NVME_PURGE_MONITOR_OPCODE = 0xDE
WDC_NVME_PURGE_MONITOR_DATA_LEN = 0x2F
WDC_NVME_PURGE_MONITOR_CMD_CDW10 = 0x0000000C
WDC_NVME_PURGE_MONITOR_TIMEOUT = 0x7530
WDC_NVME_PURGE_CMD_SEQ_ERR = 0x0C
WDC_NVME_PURGE_INT_DEV_ERR = 0x06
WDC_NVME_PURGE_STATE_IDLE = 0x00
WDC_NVME_PURGE_STATE_DONE = 0x01
WDC_NVME_PURGE_STATE_BUSY = 0x02
WDC_NVME_PURGE_STATE_REQ_PWR_CYC = 0x03
WDC_NVME_PURGE_STATE_PWR_CYC_PURGE = 0x04
WDC_NVME_CLEAR_DUMP_OPCODE = 0xFF
WDC_NVME_CLEAR_CRASH_DUMP_CMD = 0x03
WDC_NVME_CLEAR_CRASH_DUMP_SUBCMD = 0x05
WDC_NVME_CLEAR_PF_CRASH_DUMP_SUBCMD = 0x06
WDC_NVME_CLEAR_FW_ACT_HIST_OPCODE = 0xC6
WDC_NVME_CLEAR_FW_ACT_HIST_CMD = 0x23
WDC_NVME_CLEAR_FW_ACT_HIST_SUBCMD = 0x05
WDC_NVME_CLEAR_FW_ACT_HIST_VU_FID = 0xC1
WDC_ADD_LOG_BUF_LEN = 0x4000
WDC_NVME_ADD_LOG_OPCODE = 0xC1
WDC_GET_LOG_PAGE_SSD_PERFORMANCE = 0x37
WDC_NVME_GET_STAT_PERF_INTERVAL_LIFETIME = 0x0F
WDC_NVME_GET_DEV_MGMNT_LOG_PAGE_ID = 0xC2
WDC_NVME_GET_DEV_MGMNT_LOG_PAGE_ID_C8 = 0xC8
WDC_C2_LOG_BUF_LEN = 0x1000
WDC_C2_LOG_PAGES_SUPPORTED_ID = 0x08
WDC_C2_CUSTOMER_ID_ID = 0x15
WDC_C2_THERMAL_THROTTLE_STATUS_ID = 0x18
WDC_C2_ASSERT_DUMP_PRESENT_ID = 0x19
WDC_C2_USER_EOL_STATUS_ID = 0x1A
WDC_C2_USER_EOL_STATE_ID = 0x1C
WDC_C2_SYSTEM_EOL_STATE_ID = 0x1D
WDC_C2_FORMAT_CORRUPT_REASON_ID = 0x1E
WDC_EOL_STATUS_NORMAL = 0x00000000
WDC_EOL_STATUS_END_OF_LIFE = 0x00000001
WDC_EOL_STATUS_READ_ONLY = 0x00000002
WDC_ASSERT_DUMP_NOT_PRESENT = 0x00000000
WDC_ASSERT_DUMP_PRESENT = 0x00000001
WDC_THERMAL_THROTTLING_OFF = 0x00000000
WDC_THERMAL_THROTTLING_ON = 0x00000001
WDC_THERMAL_THROTTLING_UNAVAILABLE = 0x00000002
WDC_FORMAT_NOT_CORRUPT = 0x00000000
WDC_FORMAT_CORRUPT_FW_ASSERT = 0x00000001
WDC_FORMAT_CORRUPT_UNKNOWN = 0x000000FF
WDC_NVME_GET_DEVICE_INFO_LOG_OPCODE = 0xCA
WDC_FB_CA_LOG_BUF_LEN = 0x80
WDC_BD_CA_LOG_BUF_LEN = 0xA0
WDC_NVME_GET_EOL_STATUS_LOG_OPCODE = 0xC0
WDC_NVME_EOL_STATUS_LOG_LEN = 0x200
WDC_NVME_SMART_CLOUD_ATTR_LEN = 0x200
WDC_NVME_GET_SMART_CLOUD_ATTR_LOG_ID = 0xC0
WDC_NVME_GET_FW_ACT_HISTORY_LOG_ID = 0xCB
WDC_FW_ACT_HISTORY_LOG_BUF_LEN = 0x3d0
WDC_NVME_GET_FW_ACT_HISTORY_C2_LOG_ID = 0xC2
WDC_FW_ACT_HISTORY_C2_LOG_BUF_LEN = 0x1000
WDC_MAX_NUM_ACT_HIST_ENTRIES = 20
WDC_C2_GUID_LENGTH = 16
WDC_LATENCY_MON_LOG_BUF_LEN = 0x200
WDC_LATENCY_MON_LOG_ID = 0xC3
WDC_LATENCY_MON_VERSION = 0x0001
WDC_C3_GUID_LENGTH = 16
WDC_NVME_GET_VU_SMART_LOG_OPCODE = 0xD0
WDC_NVME_VU_SMART_LOG_LEN = 0x200
NVME_LOG_PERSISTENT_EVENT = 0x0D
WDC_LOG_ID_C0 = 0xC0
WDC_LOG_ID_C1 = 0xC1
WDC_LOG_ID_C2 = WDC_NVME_GET_DEV_MGMNT_LOG_PAGE_ID
WDC_LOG_ID_C3 = 0xC3
WDC_LOG_ID_C4 = 0xC4
WDC_LOG_ID_C5 = 0xC5
WDC_LOG_ID_C6 = 0xC6
WDC_LOG_ID_C8 = WDC_NVME_GET_DEV_MGMNT_LOG_PAGE_ID_C8
WDC_LOG_ID_CA = WDC_NVME_GET_DEVICE_INFO_LOG_OPCODE
WDC_LOG_ID_CB = WDC_NVME_GET_FW_ACT_HISTORY_LOG_ID
WDC_LOG_ID_D0 = WDC_NVME_GET_VU_SMART_LOG_OPCODE
WDC_LOG_ID_D1 = 0xD1
WDC_LOG_ID_D6 = 0xD6
WDC_LOG_ID_D7 = 0xD7
WDC_LOG_ID_D8 = 0xD8
WDC_LOG_ID_DE = 0xDE
WDC_LOG_ID_F0 = 0xF0
WDC_LOG_ID_F1 = 0xF1
WDC_LOG_ID_F2 = 0xF2
WDC_LOG_ID_FA = 0xFA
WDC_NVME_CLEAR_PCIE_CORR_OPCODE = WDC_NVME_CAP_DIAG_CMD_OPCODE
WDC_NVME_CLEAR_PCIE_CORR_CMD = 0x22
WDC_NVME_CLEAR_PCIE_CORR_SUBCMD = 0x04
WDC_NVME_CLEAR_PCIE_CORR_OPCODE_VUC = 0xD2
WDC_NVME_CLEAR_PCIE_CORR_FEATURE_ID = 0xC3
WDC_NVME_CLEAR_ASSERT_DUMP_OPCODE = 0xD8
WDC_NVME_CLEAR_ASSERT_DUMP_CMD = 0x03
WDC_NVME_CLEAR_ASSERT_DUMP_SUBCMD = 0x05
WDC_VU_DISABLE_CNTLR_TELEMETRY_OPTION_FEATURE_ID = 0xD2
WDC_DE_DEFAULT_NUMBER_OF_ERROR_ENTRIES = 64
WDC_DE_GENERIC_BUFFER_SIZE = 80
WDC_DE_GLOBAL_NSID = 0xFFFFFFFF
WDC_DE_DEFAULT_NAMESPACE_ID = 0x01
WDC_DE_PATH_SEPARATOR = "/"
WDC_DE_TAR_FILES = "*.bin"
WDC_DE_TAR_FILE_EXTN = ".tar.gz"
WDC_DE_TAR_CMD = "tar -czf"
WDC_NVME_NAND_STATS_LOG_ID = 0xFB
WDC_NVME_NAND_STATS_SIZE = 0x200
WDC_DE_VU_READ_SIZE_OPCODE = 0xC0
WDC_DE_VU_READ_BUFFER_OPCODE = 0xC2
WDC_NVME_ADMIN_ENC_MGMT_SND = 0xC9
WDC_NVME_ADMIN_ENC_MGMT_RCV = 0xCA
WDC_DE_FILE_HEADER_SIZE = 4
WDC_DE_FILE_OFFSET_SIZE = 2
WDC_DE_FILE_NAME_SIZE = 32
WDC_DE_VU_READ_BUFFER_STANDARD_OFFSET = 0x8000
WDC_DE_READ_MAX_TRANSFER_SIZE = 0x8000
WDC_DE_MANUFACTURING_INFO_PAGE_FILE_NAME = "manufacturing_info"
WDC_DE_CORE_DUMP_FILE_NAME = "core_dump"
WDC_DE_EVENT_LOG_FILE_NAME = "event_log"
WDC_DE_DESTN_SPI = 1
WDC_DE_DUMPTRACE_DESTINATION = 6
NVME_ID_CTRL_MODEL_NUMBER_SIZE = 40
NVME_ID_CTRL_SERIAL_NUMBER_SIZE = 20
WDC_NVME_ENC_LOG_SIZE_CHUNK = 0x1000
WDC_NVME_ENC_NIC_LOG_SIZE = 0x400000
WDC_ENC_NIC_CRASH_DUMP_ID_SLOT_1 = 0xD1
WDC_ENC_NIC_CRASH_DUMP_ID_SLOT_2 = 0xD2
WDC_ENC_NIC_CRASH_DUMP_ID_SLOT_3 = 0xD3
WDC_ENC_NIC_CRASH_DUMP_ID_SLOT_4 = 0xD4
WDC_ENC_CRASH_DUMP_ID = 0xE4
WDC_ENC_LOG_DUMP_ID = 0xE2
NVME_FEAT_OCP_LATENCY_MONITOR = 0xC5

FID_ARBITRATION                                 = 0x01
FID_POWER_MANAGEMENT                            = 0x02
FID_LBA_RANGE_TYPE                              = 0x03
FID_TEMPERATURE_THRESHOLD                       = 0x04
FID_ERROR_RECOVERY                              = 0x05
FID_VOLATILE_WRITE_CACHE                        = 0x06
FID_NUMBER_OF_QUEUES                            = 0x07
FID_INTERRUPT_COALESCING                        = 0x08
FID_INTERRUPT_VECTOR_CONFIGURATION              = 0x09
FID_WRITE_ATOMICITY                             = 0x0A
FID_ASYNCHRONOUS_EVENT_CONFIGURATION            = 0x0B
FID_AUTONOMOUS_POWER_STATE_TRANSITION           = 0x0C
FID_SOFTWARE_PROGRESS_MARKER                    = 0x80
FID_HOST_IDENTIFIER                             = 0x81
FID_RESERVATION_NOTIFICATION_MASK               = 0x82
FID_RESERVATION_PERSISTENCE                     = 0x83

WDC_DE_TYPE_IDENTIFY            = 0x1
WDC_DE_TYPE_SMARTATTRIBUTEDUMP  = 0x2
WDC_DE_TYPE_EVENTLOG            = 0x4
WDC_DE_TYPE_DUMPTRACE           = 0x8
WDC_DE_TYPE_DUMPSNAPSHOT        = 0x10
WDC_DE_TYPE_ATA_LOGS            = 0x20
WDC_DE_TYPE_SMART_LOGS          = 0x40
WDC_DE_TYPE_SCSI_LOGS           = 0x80
WDC_DE_TYPE_SCSI_MODE_PAGES     = 0x100
WDC_DE_TYPE_NVMe_FEATURES       = 0x200
WDC_DE_TYPE_DUMPSMARTERRORLOG3  = 0x400
WDC_DE_TYPE_DUMPLOG3E           = 0x800
WDC_DE_TYPE_DUMPSCRAM           = 0x1000
WDC_DE_TYPE_PCU_LOG             = 0x2000
WDC_DE_TYPE_DUMP_ERROR_LOGS     = 0x4000
WDC_DE_TYPE_FW_SLOT_LOGS        = 0x8000
WDC_DE_TYPE_MEDIA_SETTINGS      = 0x10000
WDC_DE_TYPE_SMART_DATA          = 0x20000
WDC_DE_TYPE_NVME_SETTINGS       = 0x40000
WDC_DE_TYPE_NVME_ERROR_LOGS     = 0x80000
WDC_DE_TYPE_NVME_LOGS           = 0x100000
WDC_DE_TYPE_UART_LOGS           = 0x200000
WDC_DE_TYPE_DLOGS_SPI           = 0x400000
WDC_DE_TYPE_DLOGS_RAM           = 0x800000
WDC_DE_TYPE_NVME_MANF_INFO      = 0x2000000
WDC_DE_TYPE_NONE                = 0x1000000
WDC_DE_TYPE_ALL                 = 0xFFFFFFF

SCAO_V1_PMUWT              =  0	    # /* Physical media units written TLC */
SCAO_V1_PMUWS              = 16	    # /* Physical media units written SLC */
SCAO_V1_BUNBN              = 32	    # /* Bad user nand blocks normalized */
SCAO_V1_BUNBR              = 34	    # /* Bad user nand blocks raw */
SCAO_V1_XRC                = 40 	# /* XOR recovery count */
SCAO_V1_UREC               = 48	    # /* Uncorrectable read error count */
SCAO_V1_EECE               = 56	    # /* End to end corrected errors */
SCAO_V1_EEDE               = 64	    # /* End to end detected errors */
SCAO_V1_EEUE               = 72	    # /* End to end uncorrected errors */
SCAO_V1_SDPU               = 80	    # /* System data percent used */
SCAO_V1_MNUDEC             = 84	    # /* Min User data erase counts (TLC) */
SCAO_V1_MXUDEC             = 92	    # /* Max User data erase counts (TLC) */
SCAO_V1_AVUDEC             = 100	# /* Average User data erase counts (TLC) */
SCAO_V1_MNEC               = 108	# /* Min Erase counts (SLC) */
SCAO_V1_MXEC               = 116	# /* Max Erase counts (SLC) */
SCAO_V1_AVEC               = 124	# /* Average Erase counts (SLC) */
SCAO_V1_PFCN               = 132	# /* Program fail count normalized */
SCAO_V1_PFCR               = 134	# /* Program fail count raw */
SCAO_V1_EFCN               = 140	# /* Erase fail count normalized */
SCAO_V1_EFCR               = 142	# /* Erase fail count raw */
SCAO_V1_PCEC               = 148	# /* PCIe correctable error count */
SCAO_V1_PFBU               = 156	# /* Percent free blocks (User) */
SCAO_V1_SVN                = 160	# /* Security Version Number */
SCAO_V1_PFBS               = 168	# /* Percent free blocks (System) */
SCAO_V1_DCC                = 172	# /* Deallocate Commands Completed */
SCAO_V1_TNU                = 188	# /* Total Namespace Utilization */
SCAO_V1_FCC                = 196	# /* Format NVM Commands Completed */
SCAO_V1_BBPG               = 198	# /* Background Back-Pressure Gauge */
SCAO_V1_SEEC               = 202	# /* Soft ECC error count */
SCAO_V1_RFSC               = 210	# /* Refresh count */
SCAO_V1_BSNBN              = 218	# /* Bad system nand blocks normalized */
SCAO_V1_BSNBR              = 220	# /* Bad system nand blocks raw */
SCAO_V1_EEST               = 226	# /* Endurance estimate */
SCAO_V1_TTC                = 242	# /* Thermal throttling count */
SCAO_V1_UIO                = 244	# /* Unaligned I/O */
SCAO_V1_PMUR               = 252	# /* Physical media units read */
SCAO_V1_RTOC               = 268	# /* Read command timeout count */
SCAO_V1_WTOC               = 272	# /* Write command timeout count */
SCAO_V1_TTOC               = 276	# /* Trim command timeout count */
SCAO_V1_PLRC               = 284	# /* PCIe Link Retraining Count */
SCAO_V1_PSCC               = 292	# /* Power State Change Count */
SCAO_V1_MAVF               = 300	# /* Boot SSD major version field */
SCAO_V1_MIVF               = 302	# /* Boot SSD minor version field */
SCAO_V1_PVF                = 304	# /* Boot SSD point version field */
SCAO_V1_EVF                = 306	# /* Boot SSD errata version field */
SCAO_V1_FTLUS              = 308	# /* FTL Unit Size */
SCAO_V1_TCGOS              = 312	# /* TCG Ownership Status */
SCAO_V1_LPV                = 494	# /* Log page version - 0x0001 */
SCAO_V1_LPG                = 496	# /* Log page GUID */

SCAO_PMUW               =  0 	# /* Physical media units written */
SCAO_PMUR               = 16 	# /* Physical media units read */
SCAO_BUNBR              = 32 	# /* Bad user nand blocks raw */
SCAO_BUNBN              = 38 	# /* Bad user nand blocks normalized */
SCAO_BSNBR              = 40 	# /* Bad system nand blocks raw */
SCAO_BSNBN              = 46 	# /* Bad system nand blocks normalized */
SCAO_XRC                = 48 	# /* XOR recovery count */
SCAO_UREC               = 56 	# /* Uncorrectable read error count */
SCAO_SEEC               = 64 	# /* Soft ecc error count */
SCAO_EECE               = 72 	# /* End to end corrected errors */
SCAO_EEDC               = 76 	# /* End to end detected errors */
SCAO_SDPU               = 80 	# /* System data percent used */
SCAO_RFSC               = 81 	# /* Refresh counts */
SCAO_MXUDEC             = 88 	# /* Max User data erase counts */
SCAO_MNUDEC             = 92 	# /* Min User data erase counts */
SCAO_NTTE               = 96 	# /* Number of Thermal throttling events */
SCAO_CTS                = 97 	# /* Current throttling status */
SCAO_EVF                = 98       # /* Errata Version Field */
SCAO_PVF                = 99       # /* Point Version Field */
SCAO_MIVF               = 101      # /* Minor Version Field */
SCAO_MAVF               = 103      # /* Major Version Field */
SCAO_PCEC               = 104 	# /* PCIe correctable error count */
SCAO_ICS                = 112 	# /* Incomplete shutdowns */
SCAO_PFB                = 120 	# /* Percent free blocks */
SCAO_CPH                = 128 	# /* Capacitor health */
SCAO_NEV                = 130      # /* NVMe Errata Version */
SCAO_UIO                = 136 	# /* Unaligned I/O */
SCAO_SVN                = 144 	# /* Security Version Number */
SCAO_NUSE               = 152 	# /* NUSE - Namespace utilization */
SCAO_PSC                = 160 	# /* PLP start count */
SCAO_EEST               = 176 	# /* Endurance estimate */
SCAO_PLRC               = 192      # /* PCIe Link Retraining Count */
SCAO_PSCC               = 200 	# /* Power State Change Count */
SCAO_LPV                = 494 	# /* Log page version */
SCAO_LPG                = 496 	# /* Log page GUID */

FS_CURRENT                      = 0
FS_DEFAULT                      = 1
FS_SAVED                        = 2
FS_SUPPORTED_CAPBILITIES        = 3

WDC_C0_GUID_LENGTH = 16
WDC_SCA_V1_NAND_STATS = 0x1
WDC_SCA_V1_ALL = 0xF

EOL_RBC                 = 76	# /* Realloc Block Count */
EOL_ECCR                = 80	# /* ECC Rate */
EOL_WRA                 = 84	# /* Write Amp */
EOL_PLR                 = 88	# /* Percent Life Remaining */
EOL_RSVBC               = 92	# /* Reserved Block Count */
EOL_PFC                 = 96	# /* Program Fail Count */
EOL_EFC                 = 100	# /* Erase Fail Count */
EOL_RRER                = 108	# /* Raw Read Error Rate */

WDC_NVME_C6_GUID_LENGTH = 16
WDC_NVME_GET_HW_REV_LOG_OPCODE = 0xc6
WDC_NVME_HW_REV_LOG_PAGE_LEN = 512

NVME_DE_LOGPAGE_E3 = 0x01
NVME_DE_LOGPAGE_C0 = 0x02

WDC_NVME_ADMIN_VUC_OPCODE_D2 = 0xD2
WDC_VUC_SUBOPCODE_VS_DRIVE_INFO_D2 = 0x0000010A
WDC_VUC_SUBOPCODE_LOG_PAGE_DIR_D2 = 0x00000105

NVME_LOG_NS_BASE			= 0x80
NVME_LOG_VS_BASE			= 0xC0

LATENCY_LOG_BUCKET_READ         = 3
LATENCY_LOG_BUCKET_TRIM         = 1
LATENCY_LOG_BUCKET_RESERVED     = 0
LATENCY_LOG_MEASURED_LAT_READ   = 2
LATENCY_LOG_MEASURED_LAT_WRITE  = 1
LATENCY_LOG_MEASURED_LAT_TRIM   = 0

WDC_OCP_C1_GUID_LENGTH = 16
WDC_ERROR_REC_LOG_BUF_LEN = 512
WDC_ERROR_REC_LOG_ID = 0xC1
WDC_ERROR_REC_LOG_VERSION1 = 0x0001
WDC_ERROR_REC_LOG_VERSION2 = 0x0002
WDC_OCP_C4_GUID_LENGTH = 16
WDC_DEV_CAP_LOG_BUF_LEN = 4096
WDC_DEV_CAP_LOG_ID = 0xC4
WDC_DEV_CAP_LOG_VERSION = 0x0001
WDC_OCP_C4_NUM_PS_DESCR = 127
WDC_OCP_C5_GUID_LENGTH = 16
WDC_UNSUPPORTED_REQS_LOG_BUF_LEN = 4096
WDC_UNSUPPORTED_REQS_LOG_ID = 0xC5
WDC_UNSUPPORTED_REQS_LOG_VERSION = 0x0001
WDC_NUM_UNSUPPORTED_REQ_ENTRIES = 253
WDC_REASON_INDEX_MAX = 16
WDC_REASON_ID_ENTRY_LEN = 128


wdc_lat_mon_guid = [0x92, 0x7a, 0xc0, 0x8c, 0xd0, 0x84, 0x6c, 0x9c, 0x70, 0x43, 0xe6, 0xd4, 0x58, 0x5e, 0xd4, 0x85]
wdc_uuid = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2d, 0xb9, 0x8c, 0x52, 0x0c, 0x4c, 0x5a, 0x15, 0xab, 0xe6, 0x33, 0x29,
            0x9a, 0x70, 0xdf, 0xd0]
wdc_uuid_sn640_3 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x22, 0x22, 0x22,
                    0x22, 0x22, 0x22, 0x22, 0x22]
uuid_end = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00]
ext_smart_guid = [0x65, 0x43, 0x88, 0x78, 0xAC, 0xD8, 0x78, 0xA1, 0x66, 0x42, 0x1E, 0x0F, 0x92, 0xD7, 0x6D, 0xC4]
scao_guid = [0xC5, 0xAF, 0x10, 0x28, 0xEA, 0xBF, 0xF2, 0xA4, 0x9C, 0x4F, 0x6F, 0x7C, 0xC9, 0x14, 0xD5, 0xAF]
hw_rev_log_guid = [0xAA, 0xB0, 0x05, 0xF5, 0x13, 0x5E, 0x48, 0x15, 0xAB, 0x89, 0x05, 0xBA, 0x8B, 0xE2, 0xBF, 0x3C]
wdc_ocp_c1_guid = [0x44, 0xD9, 0x31, 0x21, 0xFE, 0x30, 0x34, 0xAE, 0xAB, 0x4D, 0xFD, 0x3D, 0xBA, 0x83, 0x19, 0x5A]
wdc_ocp_c4_guid = [0x97, 0x42, 0x05, 0x0D, 0xD1, 0xE1, 0xC9, 0x98, 0x5D, 0x49, 0x58, 0x4B, 0x91, 0x3C, 0x05, 0xB7]
wdc_ocp_c5_guid = [0x2F, 0x72, 0x9C, 0x0E, 0x99, 0x23, 0x2C, 0xBB, 0x63, 0x48, 0x32, 0xD0, 0xB7, 0x98, 0xBB, 0xC7]

class wdc_utils_time_info(StructureBase):
    _fields_ = [
        ("year", c_uint32),
        ("month", c_uint32),
        ("day_of_week", c_uint32),
        ("day_of_month", c_uint32),
        ("hour", c_uint32),
        ("minute", c_uint32),
        ("second", c_uint32),
        ("msecs", c_uint32),
        ("isDST", c_uint8),
        ("zone", c_int32),
    ]

class wdc_nvme_ext_smart_log(StructureBase):
    _fields_ = [
        ("ext_smart_pmuwt", c_uint8 * 16),
        ("ext_smart_pmuws", c_uint8 * 16),
        ("ext_smart_bunbc", c_uint8 * 8),
        ("ext_smart_xrc", c_uint64),
        ("ext_smart_urec", c_uint64),
        ("ext_smart_eece", c_uint64),
        ("ext_smart_eede", c_uint64),
        ("ext_smart_eeue", c_uint64),
        ("ext_smart_sdpu", c_uint8),
        ("rsvd1", c_uint8 * 3),
        ("ext_smart_mnudec", c_uint64),
        ("ext_smart_mxudec", c_uint64),
        ("ext_smart_avudec", c_uint64),
        ("ext_smart_mnec", c_uint64),
        ("ext_smart_mxec", c_uint64),
        ("ext_smart_avec", c_uint64),
        ("ext_smart_pfc", c_uint8 * 8),
        ("ext_smart_efc", c_uint8 * 8),
        ("ext_smart_pcec", c_uint64),
        ("ext_smart_pfbu", c_uint8),
        ("rsvd2", c_uint8 * 3),
        ("ext_smart_svn", c_uint64),
        ("ext_smart_pfbs", c_uint8),
        ("rsvd3", c_uint8 * 3),
        ("ext_smart_dcc", c_uint8 * 16),
        ("ext_smart_tnu", c_uint64),
        ("ext_smart_fcc", c_uint16),
        ("ext_smart_bbpg", c_uint8),
        ("rsvd4", c_uint8 * 3),
        ("ext_smart_seec", c_uint64),
        ("ext_smart_rfsc", c_uint64),
        ("ext_smart_bsnbc", c_uint8 * 8),
        ("ext_smart_eest", c_uint8 * 16),
        ("ext_smart_ttc", c_uint16),
        ("ext_smart_uio", c_uint64),
        ("ext_smart_pmur", c_uint8 * 16),
        ("ext_smart_rtoc", c_uint32),
        ("ext_smart_wtoc", c_uint32),
        ("ext_smart_ttoc", c_uint32),
        ("rsvd5", c_uint8 * 4),
        ("ext_smart_plrc", c_uint64),
        ("ext_smart_pscc", c_uint64),
        ("ext_smart_maj", c_uint16),
        ("ext_smart_min", c_uint16),
        ("ext_smart_pt", c_uint16),
        ("ext_smart_err", c_uint16),
        ("ext_smart_ftlus", c_uint32),
        ("ext_smart_tcgos", c_uint32),
        ("rsvd6", c_uint8 * 178),
        ("ext_smart_lpv", c_uint16),
        ("ext_smart_lpg", c_uint8 * 16),
    ]

class ocp_bad_nand_block_count(StructureBase):
    _fields_ = [
        ("raw", c_uint64),
        ("normalized", c_uint16),
    ]

class ocp_e2e_correction_count(StructureBase):
    _fields_ = [
        ("detected", c_uint32),
        ("corrected", c_uint32),
    ]

class ocp_user_data_erase_count(StructureBase):
    _fields_ = [
        ("maximum", c_uint32),
        ("minimum", c_uint32),
    ]

class ocp_thermal_status(StructureBase):
    _fields_ = [
        ("num_events", c_uint8),
        ("current_status", c_uint8),
    ]

class ocp_dssd_specific_ver(StructureBase):
    _fields_ = [
        ("errata_ver", c_uint8),
        ("point_ver", c_uint16),
        ("minor_ver", c_uint16),
        ("major_ver", c_uint8),
    ]

class ocp_cloud_smart_log(StructureBase):
    _fields_ = [
        ("physical_media_units_written", c_uint8 * 16),
        ("physical_media_units_read", c_uint8 * 16),
        ("bad_user_nand_blocks", ocp_bad_nand_block_count),
        ("bad_system_nand_blocks", ocp_bad_nand_block_count),
        ("xor_recovery_count", c_uint64),
        ("uncorrectable_read_error_count", c_uint64),
        ("soft_ecc_error_count", c_uint64),
        ("e2e_correction_counts", ocp_e2e_correction_count),
        ("system_data_percent_used", c_uint8),
        ("refresh_counts", c_uint64),
        ("user_data_erase_counts", ocp_user_data_erase_count),
        ("thermal_status", ocp_thermal_status),
        ("dssd_specific_ver", ocp_dssd_specific_ver),
        ("pcie_correctable_error_count", c_uint64),
        ("incomplete_shutdowns", c_uint32),
        ("rsvd1", c_uint8 * 4),
        ("percent_free_blocks", c_uint8),
        ("rsvd2", c_uint8 * 7),
        ("capacitor_health", c_uint16),
        ("nvme_errata_ver", c_uint8),
        ("rsvd3", c_uint8 * 5),
        ("unaligned_io", c_uint64),
        ("security_version_number", c_uint64),
        ("total_nuse", c_uint64),
        ("plp_start_count", c_uint8 * 16),
        ("endurance_estimate", c_uint8 * 16),
        ("pcie_link_retraining_cnt", c_uint64),
        ("power_state_change_cnt", c_uint64),
        ("rsvd4", c_uint8 * 286),
        ("log_page_version", c_uint16),
        ("log_page_guid", c_uint8 * 16),
    ]

class wdc_nvme_hw_rev_log(StructureBase):
    _fields_ = [
        ("hw_rev_gdr", c_uint8),
        ("hw_rev_ar", c_uint8),
        ("hw_rev_pbc_mc", c_uint8),
        ("hw_rev_dram_mc", c_uint8),
        ("hw_rev_nand_mc", c_uint8),
        ("hw_rev_pmic1_mc", c_uint8),
        ("hw_rev_pmic2_mc", c_uint8),
        ("hw_rev_c1_mc", c_uint8),
        ("hw_rev_c2_mc", c_uint8),
        ("hw_rev_c3_mc", c_uint8),
        ("hw_rev_c4_mc", c_uint8),
        ("hw_rev_c5_mc", c_uint8),
        ("hw_rev_c6_mc", c_uint8),
        ("hw_rev_c7_mc", c_uint8),
        ("hw_rev_c8_mc", c_uint8),
        ("hw_rev_c9_mc", c_uint8),
        ("rsrvd1", c_uint8 * 48),
        ("hw_rev_dev_mdi", c_uint8 * 16),
        ("hw_rev_asic_di", c_uint8 * 16),
        ("hw_rev_pcb_di", c_uint8 * 16),
        ("hw_rev_dram_di", c_uint8 * 16),
        ("hw_rev_nand_di", c_uint8 * 16),
        ("hw_rev_pmic1_di", c_uint8 * 16),
        ("hw_rev_pmic2_di", c_uint8 * 16),
        ("hw_rev_c1_di", c_uint8 * 16),
        ("hw_rev_c2_di", c_uint8 * 16),
        ("hw_rev_c3_di", c_uint8 * 16),
        ("hw_rev_c4_di", c_uint8 * 16),
        ("hw_rev_c5_di", c_uint8 * 16),
        ("hw_rev_c6_di", c_uint8 * 16),
        ("hw_rev_c7_di", c_uint8 * 16),
        ("hw_rev_c8_di", c_uint8 * 16),
        ("hw_rev_c9_di", c_uint8 * 16),
        ("hw_rev_sn", c_uint8 * 32),
        ("rsrvd2", c_uint8 * 142),
        ("hw_rev_version", c_uint16),
        ("hw_rev_guid", c_uint8 * 16),
    ]

class wdc_de_file_meta_data(StructureBase):
    _fields_ = [
        ("file_name", c_char * WDC_DE_FILE_NAME_SIZE),
        ("file_id", c_uint16),
        ("file_size", c_uint64),
    ]

class wdc_drive_essentials(StructureBase):
    _fields_ = [
        ("meta_data", wdc_de_file_meta_data),
        ("essential_type", c_uint32),
    ]

class wdc_de_vu_log_directory(StructureBase):
    _fields_ = [
        ("log_entry", POINTER(wdc_drive_essentials)),
        ("max_num_log_entries", c_uint32),
        ("num_of_valid_log_entries", c_uint32),
    ]

class wdc_de_csa_feature_id_list(StructureBase):
    _fields_ = [
        ("feature_id", c_uint8),
        ("feature_name", c_char * WDC_DE_GENERIC_BUFFER_SIZE),
    ]

class tarfile_metadata(StructureBase):
    _fields_ = [
        ("file_name", c_char * MAX_PATH_LEN),
        ("buffer_folder_path", c_char * MAX_PATH_LEN),
        ("buffer_folder_name", c_char * MAX_PATH_LEN),
        ("tar_file_name", c_char * MAX_PATH_LEN),
        ("tar_files", c_char * MAX_PATH_LEN),
        ("tar_cmd", c_char * MAX_PATH_LEN),
        ("curr_dir", c_char * MAX_PATH_LEN),
        ("time_info", wdc_utils_time_info),
        ("time_string", c_char * MAX_PATH_LEN),
    ]

class nvme_vu_de_log_page_list(StructureBase):
    _fields_ = [
        ("log_page_name", c_uint32),
        ("log_page_id", c_uint32),
        ("log_page_len", c_uint32),
        ("log_page_id_str", c_char * 5),
    ]

class wdc_nvme_de_log_page(StructureBase):
    _fields_ = [
        ("vu_log_page_reqd", c_uint32),
        ("num_of_vu_log_pages", c_uint32),
    ]

class ocp_drive_info(StructureBase):
    _fields_ = [
        ("hw_revision", c_uint32),
        ("ftl_unit_size", c_uint32),
    ]

class log_page_directory(StructureBase):
    _fields_ = [
        ("supported_lid_bitmap", c_uint64),
        ("rsvd", c_uint64),
        ("supported_ns_lid_bitmap", c_uint64),
        ("supported_vs_lid_bitmap", c_uint64),
    ]

class feature_latency_monitor(StructureBase):
    _fields_ = [
        ("active_bucket_timer_threshold", c_uint16),
        ("active_threshold_a", c_uint8),
        ("active_threshold_b", c_uint8),
        ("active_threshold_c", c_uint8),
        ("active_threshold_d", c_uint8),
        ("active_latency_config", c_uint16),
        ("active_latency_minimum_window", c_uint8),
        ("debug_log_trigger_enable", c_uint16),
        ("discard_debug_log", c_uint8),
        ("latency_monitor_feature_enable", c_uint8),
        ("reserved", c_uint8 * 4083),
    ]

class wdc_log_size(StructureBase):
    _fields_ = [
        ("log_size", c_uint32),
    ]

class wdc_e6_log_hdr(StructureBase):
    _fields_ = [
        ("eye_catcher", c_uint32),
        ("log_size", c_uint32),
    ]

class wdc_dui_log_section(StructureBase):
    _fields_ = [
        ("section_type", c_uint16),
        ("reserved", c_uint16),
        ("section_size", c_uint32),
    ]

class wdc_dui_log_section_v2(StructureBase):
    _fields_ = [
        ("section_type", c_uint16),
        ("data_area_id", c_uint8),
        ("reserved", c_uint8),
    ]

class wdc_dui_log_section_v4(StructureBase):
    _fields_ = [
        ("section_type", c_uint16),
        ("data_area_id", c_uint8),
        ("reserved", c_uint8),
        ("section_size_sectors", c_uint32),
    ]

class wdc_dui_log_hdr(StructureBase):
    _fields_ = [
        ("telemetry_hdr", c_uint8 * 512),
        ("hdr_version", c_uint16),
        ("section_count", c_uint16),
        ("log_size", c_uint32),
        ("log_section", wdc_dui_log_section * WDC_NVME_DUI_MAX_SECTION),
        ("log_data", c_uint8 * 40),
    ]

class wdc_dui_log_hdr_v2(StructureBase):
    _fields_ = [
        ("telemetry_hdr", c_uint8 * 512),
        ("hdr_version", c_uint16),
        ("product_id", c_uint8),
        ("section_count", c_uint16),
        ("log_size", c_uint32),
        ("log_section", wdc_dui_log_section_v2 * WDC_NVME_DUI_MAX_SECTION_V2),
        ("log_data", c_uint8 * 40),
    ]

class wdc_dui_log_hdr_v3(StructureBase):
    _fields_ = [
        ("telemetry_hdr", c_uint8 * 512),
        ("hdr_version", c_uint16),
        ("product_id", c_uint8),
        ("section_count", c_uint16),
        ("log_size", c_uint32),
        ("log_section", wdc_dui_log_hdr_v2 * WDC_NVME_DUI_MAX_SECTION_V3),
        ("security_nonce", c_uint8 * 36),
        ("log_data", c_uint8 * 40),
    ]

class wdc_dui_log_hdr_v4(StructureBase):
    _fields_ = [
        ("telemetry_hdr", c_uint8 * 512),
        ("hdr_version", c_uint16),
        ("product_id", c_uint8),
        ("section_count", c_uint16),
        ("log_size_sectors", c_uint32),
        ("log_section", wdc_dui_log_section_v4 * WDC_NVME_DUI_MAX_SECTION),
        ("log_data", c_uint8 * 40),
    ]

class wdc_nvme_purge_monitor_data(StructureBase):
    _fields_ = [
        ("rsvd1", c_uint16),
        ("rsvd2", c_uint16),
        ("first_erase_failure_cnt", c_uint16),
        ("second_erase_failure_cnt", c_uint16),
        ("rsvd3", c_uint16),
        ("programm_failure_cnt", c_uint16),
        ("rsvd4", c_uint32),
        ("rsvd5", c_uint32),
        ("entire_progress_total", c_uint32),
        ("entire_progress_current", c_uint32),
        ("rsvd6", c_uint8 * 14),
    ]

class wdc_log_page_header(StructureBase):
    _fields_ = [
        ("num_subpages", c_uint8),
        ("reserved", c_uint8),
        ("total_log_size", c_uint16),
    ]

class wdc_log_page_subpage_header(StructureBase):
    _fields_ = [
        ("spcode", c_uint8),
        ("pcset", c_uint8),
        ("subpage_length", c_uint16),
    ]

class wdc_ssd_perf_stats(StructureBase):
    _fields_ = [
        ("hr_cmds", c_uint64),
        ("hr_blks", c_uint64),
        ("hr_ch_cmds", c_uint64),
        ("hr_ch_blks", c_uint64),
        ("hr_st_cmds", c_uint64),
        ("hw_cmds", c_uint64),
        ("hw_blks", c_uint64),
        ("hw_os_cmds", c_uint64),
        ("hw_oe_cmds", c_uint64),
        ("hw_st_cmds", c_uint64),
        ("nr_cmds", c_uint64),
        ("nw_cmds", c_uint64),
        ("nr_bw", c_uint64),
    ]

class wdc_c2_log_page_header(StructureBase):
    _fields_ = [
        ("length", c_uint32),
        ("version", c_uint32),
    ]

class wdc_c2_log_subpage_header(StructureBase):
    _fields_ = [
        ("length", c_uint32),
        ("entry_id", c_uint32),
        ("data", c_uint32),
    ]

class wdc_c2_cbs_data(StructureBase):
    _fields_ = [
        ("length", c_uint32),
        ("data", Pointer(c_uint8, "length")),
    ]

class wdc_bd_ca_log_format(StructureBase):
    _fields_ = [
        ("field_id", c_uint8),
        ("reserved1", c_uint8 * 2),
        ("normalized_value", c_uint8),
        ("raw_value", c_uint8 * 8),
    ]

class wdc_ssd_latency_monitor_log(StructureBase):
    _fields_ = [
        ("feature_status", c_uint8),
        ("rsvd1", c_uint8 * 2),
        ("active_bucket_timer", c_uint16),
        ("active_bucket_timer_threshold", c_uint16),
        ("active_threshold_a", c_uint8),
        ("active_threshold_b", c_uint8),
        ("active_threshold_c", c_uint8),
        ("active_threshold_d", c_uint8),
        ("active_latency_config", c_uint16),
        ("active_latency_min_window", c_uint8),
        ("rsvd2", c_uint8 * 0x13),
        ("active_bucket_counter", c_uint32 * 16),
        ("active_latency_timestamp", c_uint64 * 12),
        ("active_measured_latency", c_uint16 * 12),
        ("active_latency_stamp_units", c_uint16),
        ("rsvd3", c_uint8 * 0x16),
        ("active_bucket_counter", c_uint32 * 16),
        ("active_latency_timestamp", c_uint64 * 12),
        ("active_measured_latency", c_uint16 * 12),
        ("active_latency_stamp_units", c_uint16),
        ("rsvd4", c_uint8 * 0x16),
        ("debug_log_trigger_enable", c_uint16),
        ("debug_log_measured_latency", c_uint16),
        ("debug_log_latency_stamp", c_uint64),
        ("debug_log_ptr", c_uint16),
        ("debug_log_counter_trigger", c_uint16),
        ("debug_log_stamp_units", c_uint8),
        ("rsvd5", c_uint8 * 0x1D),
        ("log_page_version", c_uint16),
        ("log_page_guid", c_uint8 * 0x10),
    ]

class wdc_ssd_ca_perf_stats(StructureBase):
    _fields_ = [
        ("nand_bytes_wr_lo", c_uint64),
        ("nand_bytes_wr_hi", c_uint64),
        ("nand_bytes_rd_lo", c_uint64),
        ("nand_bytes_rd_hi", c_uint64),
        ("nand_bad_block", c_uint64),
        ("uncorr_read_count", c_uint64),
        ("ecc_error_count", c_uint64),
        ("ssd_detect_count", c_uint32),
        ("ssd_correct_count", c_uint32),
        ("data_percent_used", c_uint8),
        ("data_erase_max", c_uint32),
        ("data_erase_min", c_uint32),
        ("refresh_count", c_uint64),
        ("program_fail", c_uint64),
        ("user_erase_fail", c_uint64),
        ("system_erase_fail", c_uint64),
        ("thermal_throttle_status", c_uint8),
        ("thermal_throttle_count", c_uint8),
        ("pcie_corr_error", c_uint64),
        ("incomplete_shutdown_count", c_uint32),
        ("percent_free_blocks", c_uint8),
        ("rsvd", c_uint8 * 392),
    ]

class wdc_ssd_d0_smart_log(StructureBase):
    _fields_ = [
        ("smart_log_page_header", c_uint32),
        ("lifetime_realloc_erase_block_count", c_uint32),
        ("lifetime_power_on_hours", c_uint32),
        ("lifetime_uecc_count", c_uint32),
        ("lifetime_wrt_amp_factor", c_uint32),
        ("trailing_hr_wrt_amp_factor", c_uint32),
        ("reserve_erase_block_count", c_uint32),
        ("lifetime_program_fail_count", c_uint32),
        ("lifetime_block_erase_fail_count", c_uint32),
        ("lifetime_die_failure_count", c_uint32),
        ("lifetime_link_rate_downgrade_count", c_uint32),
        ("lifetime_clean_shutdown_count", c_uint32),
        ("lifetime_unclean_shutdown_count", c_uint32),
        ("current_temp", c_uint32),
        ("max_recorded_temp", c_uint32),
        ("lifetime_retired_block_count", c_uint32),
        ("lifetime_read_disturb_realloc_events", c_uint32),
        ("lifetime_nand_writes", c_uint64),
        ("capacitor_health", c_uint32),
        ("lifetime_user_writes", c_uint64),
        ("lifetime_user_reads", c_uint64),
        ("lifetime_thermal_throttle_act", c_uint32),
        ("percentage_pe_cycles_remaining", c_uint32),
        ("rsvd", c_uint8 * 408),
    ]

class wdc_ocp_c1_error_recovery_log(StructureBase):
    _fields_ = [
        ("panic_reset_wait_time", c_uint16),
        ("panic_reset_action", c_uint8),
        ("dev_recovery_action1", c_uint8),
        ("panic_id", c_uint64),
        ("dev_capabilities", c_uint32),
        ("vs_recovery_opc", c_uint8),
        ("rsvd1", c_uint8 * 3),
        ("vs_cmd_cdw12", c_uint32),
        ("vs_cmd_cdw13", c_uint32),
        ("vs_cmd_to", c_uint8),
        ("dev_recovery_action2", c_uint8),
        ("dev_recovery_action2_to", c_uint8),
        ("rsvd2", c_uint8 * 463),
        ("log_page_version", c_uint16),
        ("log_page_guid", c_uint8 * WDC_OCP_C1_GUID_LENGTH),
    ]

class wdc_nand_stats(StructureBase):
    _fields_ = [
        ("nand_write_tlc", c_uint8 * 16),
        ("nand_write_slc", c_uint8 * 16),
        ("nand_prog_failure", c_uint32),
        ("nand_erase_failure", c_uint32),
        ("bad_block_count", c_uint32),
        ("nand_rec_trigger_event", c_uint64),
        ("e2e_error_counter", c_uint64),
        ("successful_ns_resize_event", c_uint64),
        ("rsvd", c_uint8 * 442),
        ("log_page_version", c_uint16),
    ]

class wdc_nand_stats_V3(StructureBase):
    _fields_ = [
        ("nand_write_tlc", c_uint8 * 16),
        ("nand_write_slc", c_uint8 * 16),
        ("bad_nand_block_count", c_uint8 * 8),
        ("xor_recovery_count", c_uint64),
        ("uecc_read_error_count", c_uint64),
        ("ssd_correction_counts", c_uint8 * 16),
        ("percent_life_used", c_uint8),
        ("user_data_erase_counts", c_uint64 * 4),
        ("program_fail_count", c_uint8 * 8),
        ("erase_fail_count", c_uint8 * 8),
        ("correctable_error_count", c_uint64),
        ("percent_free_blocks_user", c_uint8),
        ("security_version_number", c_uint64),
        ("percent_free_blocks_system", c_uint8),
        ("trim_completions", c_uint8 * 25),
        ("back_pressure_guage", c_uint8),
        ("soft_ecc_error_count", c_uint64),
        ("refresh_count", c_uint64),
        ("bad_sys_nand_block_count", c_uint8 * 8),
        ("endurance_estimate", c_uint8 * 16),
        ("thermal_throttling_st_ct", c_uint8 * 2),
        ("unaligned_io", c_uint64),
        ("physical_media_units", c_uint8 * 16),
        ("rsvd", c_uint8 * 279),
        ("log_page_version", c_uint16),
    ]

class wdc_vs_pcie_stats(StructureBase):
    _fields_ = [
        ("unsupported_request_error_count", c_uint64),
        ("ecrc_error_status_count", c_uint64),
        ("malformed_tlp_status_count", c_uint64),
        ("receiver_overflow_status_count", c_uint64),
        ("unexpected_cmpltn_status_count", c_uint64),
        ("complete_abort_status_count", c_uint64),
        ("cmpltn_timout_status_count", c_uint64),
        ("flow_control_error_status_count", c_uint64),
        ("poisoned_tlp_status_count", c_uint64),
        ("dLink_prtcl_error_status_count", c_uint64),
        ("advsry_nfatal_err_status_count", c_uint64),
        ("replay_timer_to_status_count", c_uint64),
        ("replay_num_rollover_st_count", c_uint64),
        ("bad_dllp_status_count", c_uint64),
        ("bad_tlp_status_count", c_uint64),
        ("receiver_err_status_count", c_uint64),
        ("rsvd", c_uint8 * 384),
    ]

class wdc_fw_act_history_log_hdr(StructureBase):
    _fields_ = [
        ("eye_catcher", c_uint32),
        ("version", c_uint8),
        ("reserved1", c_uint8),
        ("num_entries", c_uint8),
        ("reserved2", c_uint8),
        ("entry_size", c_uint32),
        ("reserved3", c_uint32),
    ]

class wdc_fw_act_history_log_entry(StructureBase):
    _fields_ = [
        ("entry_num", c_uint32),
        ("power_cycle_count", c_uint64),
        ("power_on_seconds", c_uint64),
        ("previous_fw_version", c_uint64),
        ("new_fw_version", c_uint64),
        ("slot_number", c_uint8),
        ("commit_action_type", c_uint8),
        ("result", c_uint16),
        ("reserved", c_uint8 * 12),
    ]

class wdc_fw_act_history_log_entry_c2(StructureBase):
    _fields_ = [
        ("entry_version_num", c_uint8),
        ("entry_len", c_uint8),
        ("reserved", c_uint16),
        ("fw_act_hist_entries", c_uint16),
        ("timestamp", c_uint64),
        ("reserved2", c_uint8 * 8),
        ("power_cycle_count", c_uint64),
        ("previous_fw_version", c_uint64),
        ("current_fw_version", c_uint64),
        ("slot_number", c_uint8),
        ("commit_action_type", c_uint8),
        ("result", c_uint16),
        ("reserved3", c_uint8 * 14),
    ]

class wdc_fw_act_history_log_format_c2(StructureBase):
    _fields_ = [
        ("log_identifier", c_uint8),
        ("reserved", c_uint8 * 3),
        ("num_entries", c_uint32),
        ("entry", wdc_fw_act_history_log_entry_c2 * WDC_MAX_NUM_ACT_HIST_ENTRIES),
        ("reserved2", c_uint8 * 2790),
        ("log_page_version", c_uint16),
        ("log_page_guid", c_uint8 * WDC_C2_GUID_LENGTH),
    ]

class wdc_ocp_C4_dev_cap_log(StructureBase):
    _fields_ = [
        ("num_pcie_ports", c_uint16),
        ("oob_mgmt_support", c_uint16),
        ("wrt_zeros_support", c_uint16),
        ("sanitize_support", c_uint16),
        ("dsm_support", c_uint16),
        ("wrt_uncor_support", c_uint16),
        ("fused_support", c_uint16),
        ("min_dssd_ps", c_uint16),
        ("rsvd1", c_uint8),
        ("dssd_ps_descr", c_uint8 * WDC_OCP_C4_NUM_PS_DESCR),
        ("rsvd2", c_uint8 * 3934),
        ("log_page_version", c_uint16),
        ("log_page_guid", c_uint8 * WDC_OCP_C4_GUID_LENGTH),
    ]

class wdc_ocp_C5_unsupported_reqs(StructureBase):
    _fields_ = [
        ("unsupported_count", c_uint16),
        ("rsvd1", c_uint8 * 14),
        ("unsupported_req_list", c_uint8 * WDC_NUM_UNSUPPORTED_REQ_ENTRIES * 16),
        ("rsvd2", c_uint8 * 14),
        ("log_page_version", c_uint16),
        ("log_page_guid", c_uint8 * WDC_OCP_C5_GUID_LENGTH),
    ]