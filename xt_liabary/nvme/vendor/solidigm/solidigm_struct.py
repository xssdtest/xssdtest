#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from xt_module.xt_structure import *

SLDGM_TEMP_STATS_LID = 0xC5
VU_SMART_PAGE_SIZE = 512
BUCKET_LIST_SIZE_4_0 = 512
BUCKET_LIST_SIZE_4_1 = 1216
BASE_RANGE_BITS_4_0 = 3
BASE_RANGE_BITS_4_1 = 6
DWORD_SIZE = 4
NLOG = 0
EVENTLOG = 1
ASSERTLOG = 2
VU_GC_MAX_ITEMS = 100

class temp_stats(StructureBase):
    _fields_ = [
        ('curr', c_uint64),
        ('last_overtemp', c_uint64),
        ('life_overtemp', c_uint64),
        ('highest_temp', c_uint64),
        ('lowest_temp', c_uint64),
        ('rsvd', c_uint8 * 40),
        ('max_operating_temp', c_uint64),
        ('min_operating_temp', c_uint64),
        ('est_offset', c_uint64),
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

class nvme_additional_smart_log_item(StructureBase):
    _fields_ = [
        ('key', c_uint8),
        ('_kp', c_uint8 * 2),
        ('normalized', c_uint8),
        ('_np', c_uint8),
        ('item', additional_smart_log_union),
        ('_rp', c_uint8),
    ]


class solidigm_nvme_additional_smart_log(StructureBase):
    _fields_ = [
        ('item', nvme_additional_smart_log_item * 42),
    ]

class solidigm_latency_statistics(StructureBase):
    _fields_ = [
        ('version_major', c_uint16),
        ('version_minor', c_uint16),
        ('data', c_uint32 * BUCKET_LIST_SIZE_4_1),
        ('average_latency', c_uint64),
    ]

class version(StructureBase):
    _fields_ = [
        ('major', c_uint16),
        ('minor', c_uint16),
    ]

class solidigm_event_dump_instance(StructureBase):
    _fields_ = [
        ('numeventdumps', c_uint32),
        ('coresize', c_uint32),
        ('coreoffset', c_uint32),
        ('eventidoffset', c_uint32 * 16),
        ('eventIdValidity', c_uint8 * 16),
    ]

class solidigm_commom_header(StructureBase):
    _fields_ = [
        ('version', version),
        ('header_size', c_uint32),
        ('log_size', c_uint32),
        ('numcores', c_uint32),
    ]

class solidigm_event_dump_header(StructureBase):
    _fields_ = [
        ('header', solidigm_commom_header),
        ('eventidsize', c_uint32),
        ('edumps', Pointer(solidigm_event_dump_instance, "eventidsize")),
    ]

class assert_dump_core(StructureBase):
    _fields_ = [
        ('coreoffset', c_uint32),
        ('assertsize', c_uint32),
        ('assertdumptype', c_uint8),
        ('assertvalid', c_uint8),
        ('reserved', c_uint8 * 2),
    ]

class solidigm_assert_dump_header(StructureBase):
    _fields_ = [
        ('header', solidigm_commom_header),
        ('assertdump', Pointer(assert_dump_core, "instance.header.numcores")),
    ]

class solidigm_nlog_dump_header_common(StructureBase):
    _fields_ = [
        ('version', version),
        ('log_select', c_uint32),
        ('total_nlogs', c_uint32),
        ('nlogn_um', c_uint32),
        ('nlog_name', c_char * 4),
        ('nlog_bytesize', c_uint32),
        ('nlog_primary_buffsize', c_uint32),
        ('tick_spersecond', c_uint32),
        ('core_count', c_uint32),
    ]

class solidigm_nlog_dump_header3_0(StructureBase):
    _fields_ = [
        ('common', solidigm_nlog_dump_header_common),
        ('nlog_pause_status', c_uint32),
        ('select_offset_ref', c_uint32),
        ('select_nlog_pause', c_uint32),
        ('select_added_offset', c_uint32),
        ('nlog_bufnum', c_uint32),
        ('nlog_bufnum_max', c_uint32),
    ]

class solidigm_nlog_dump_header4_0(StructureBase):
    _fields_ = [
        ('common', solidigm_nlog_dump_header_common),
        ('nlog_pause_status', c_uint64),
        ('select_offset_ref', c_uint32),
        ('select_nlog_pause', c_uint32),
        ('select_added_offset', c_uint32),
        ('nlog_bufnum', c_uint32),
        ('nlog_bufnum_max', c_uint32),
        ('core_selected', c_uint32),
        ('reserved', c_uint32 * 2),
    ]

class solidigm_nlog_dump_header4_1(StructureBase):
    _fields_ = [
        ('common', solidigm_nlog_dump_header_common),
        ('nlog_pause_status', c_uint64),
        ('select_offset_ref', c_uint32),
        ('select_nlog_pause', c_uint32),
        ('select_added_offset', c_uint32),
        ('nlog_bufnum', c_uint32),
        ('nlog_bufnum_max', c_uint32),
        ('core_selected', c_uint32),
        ('lpa_pointer1_high', c_uint32),
        ('lpa_pointer1_low', c_uint32),
        ('lpa_pointer2_high', c_uint32),
        ('lpa_pointer2_low', c_uint32),
    ]

class gc_item(StructureBase):
    _fields_ = [
        ('timer_type', c_uint32),
        ('timestamp', c_uint64),
    ]

class solidigm_garbage_control_collection_log(StructureBase):
    _fields_ = [
        ('version_major', c_uint16),
        ('version_minor', c_uint16),
        ('item', gc_item * VU_GC_MAX_ITEMS),
        ('reserved', c_uint8 * 2892),
    ]