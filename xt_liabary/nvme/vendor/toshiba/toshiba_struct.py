#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from xt_module.xt_structure import *

OP_SCT_STATUS = 0xE0
OP_SCT_COMMAND_TRANSFER = 0xE0
OP_SCT_DATA_TRANSFER = 0xE1
DW10_SCT_COMMAND_TRANSFER = 0x1
INTERNAL_LOG_ACTION_CODE = 0xFFFB
CURRENT_LOG_FUNCTION_CODE = 0x0001
SAVED_LOG_FUNCTION_CODE = 0x0002
MASK_0 = 1 << 0
MASK_1 = 1 << 1
MASK_IGNORE = 0
CODE_0 = 0x0D
CODE_1 = 0x10