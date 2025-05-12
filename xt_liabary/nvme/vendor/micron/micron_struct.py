#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from xt_module.xt_structure import *

class micron_pcie_error_counters(StructureBase):
    _fields_ = [
        ('receiver_error', c_uint16),
        ('bad_tlp', c_uint16),
        ('bad_dllp', c_uint16),
        ('replay_num_rollover', c_uint16),
        ('replay_timer_timeout', c_uint16),
        ('advisory_non_fatal_error', c_uint16),
        ('DLPES', c_uint16),
        ('poisoned_tlp', c_uint16),
        ('FCPC', c_uint16),
        ('completion_timeout', c_uint16),
        ('completion_abort', c_uint16),
        ('unexpected_completion', c_uint16),
        ('receiver_overflow', c_uint16),
        ('malformed_tlp', c_uint16),
        ('ecrc_error', c_uint16),
        ('unsupported_request_error', c_uint16),
    ]

class micron_common_log_header(StructureBase):
    _fields_ = [
     ('id', c_uint8),
     ('version', c_uint8),
     ('pn', c_uint16),
     ('log_size', c_uint32),
     ('max_size', c_uint32),
     ('write_pointer', c_uint32),
     ('next_pointer', c_uint32),
     ('overwritten_bytes', c_uint32),
     ('flags', c_uint8),
     ('reserved', c_uint8 * 7),
    ]