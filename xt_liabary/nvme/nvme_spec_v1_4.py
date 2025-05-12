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
import os
import sys
from ctypes import *
from enum import Enum
path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(path)))
from xt_module.xt_structure import *

class CAP(StructureBase):
    _fields_ = [("MQES", c_uint64, 16),             # Maximum Queue Entries Supported 	                    MQES	 0	15	RO	Impl Spec
                ("CQR", c_uint64, 1),               # Contiguous Queues Required 	                        CQR	    16	16	RO	Impl Spec
                ("AMS", c_uint64, 2),               # Arbitration Mechanism Supported 	                    AMS	    17	18	RO	Impl Spec
                ("Reserved3", c_uint64, 5),         # Reserved	                                            RSV	    19	23	RO	0
                ("TO", c_uint64, 8),                # Timeout 	                                            TO	    24	31	RO	Impl Spec
                ("DSTRD", c_uint64, 4),             # Doorbell Stride 	                                    DSTRD	32	35	RO	Impl Spec
                ("NSSRS", c_uint64, 1),             # NVM Subsystem Reset Supported	                        NSSRS	36	36	RO	Impl Spec
                ("CCS", c_uint64, 8),               # Command Sets Supported	                            CCS	    37	44	RO	Impl Spec
                ("BPS", c_uint64, 1),               # Boot Partition Support 	                            BPS	    45	45	RO	Impl Spec
                ("Reserved2", c_uint64, 2),         # Reserved	                                            RSV	    46	47	RO	0
                ("MPSMIN", c_uint64, 4),            # Memory Page Size Minimum 	                            MPSMIN	48	51	RO	Impl Spec
                ("MPSMAX", c_uint64, 4),            # Memory Page Size Maximum 	                            MPSMAX	52	55	RO	Impl Spec
                ("PMRS", c_uint64, 1),              # Persistent Memory Region Supported 	                PMRS	56	56	RO	Impl Spec
                ("CMBS", c_uint64, 1),              # Controller Memory Buffer Supported 	                CMBS	57	57	RO	Impl Spec
                ("Reserved1", c_uint64, 6),         # Reserved	                                            RSV	    58	63	RO	0
                ]


class VS(StructureBase):
    _fields_ = [("TER", c_uint32, 8),               # Tertiary Version Number	                            TER	    0	7	RO	0
                ("MNR", c_uint32, 8),               # Minor Version Number	                                MNR	    8	15	RO	0
                ("MJR", c_uint32, 16),              # Major Version Number	                                MJR	    16	31	RO	1
                ]


class INTMS(StructureBase):
    _fields_ = [("IVMS", c_uint32),                 # Interrupt Vector Mask Set	                            IVMS	0	31	RWS	0
                ]


class INTMC(StructureBase):
    _fields_ = [("IVMC", c_uint32),                 # Interrupt Vector Mask Clear	                        IVMC	0	31	RWC	0
                ]


class CC(StructureBase):
    _fields_ = [("EN", c_uint32, 1),                # Enable 	                                            EN	    0	0	RW	0
                ("Reserved2", c_uint32, 3),         # Reserved	                                            RSV	    1	3	RO	0
                ("CSS", c_uint32, 3),               # I/O Command Set Selected 	                            CSS	    4	6	RW	0
                ("MPS", c_uint32, 4),               # Memory Page Size 	                                    MPS	    7	10	RW	0
                ("AMS", c_uint32, 3),               # Arbitration Mechanism Selected 	                    AMS	    11	13	RW	0
                ("SHN", c_uint32, 2),               # Shutdown Notification 	                            SHN	    14	15	RW	0
                ("IOSQES", c_uint32, 4),            # I/O Submission Queue Entry Size 	                    IOSQES	16	19	RW	0
                ("IOCQES", c_uint32, 4),            # I/O Completion Queue Entry Size	                    IOCQES	20	23	RW/RO	0
                ("Reserved1", c_uint32, 8),         # Reserved	                                            RSV	    24	31	RW/RO	0
                ]


class CSTS(StructureBase):
    _fields_ = [("RDY", c_uint32, 1),               # Ready 	                                            RDY	    0	0	RO	0
                ("CFS", c_uint32, 1),               # Controller Fatal Status 	                            CFS	    1	1	RO	HwInit
                ("SHST", c_uint32, 2),              # Shutdown Status 	                                    SHST	2	3	RO	0
                ("NSSRO", c_uint32, 1),             # NVM Subsystem Reset Occurred 	                        NSSRO	4	4	RWC	HwInit
                ("PP", c_uint32, 1),                # Processing Paused 	                                PP	    5	5	RO	0
                ("Reserved", c_uint32, 26),         # Reserved	                                            RSV	    6	31	RO	0
                ]


class NSSR(StructureBase):
    _fields_ = [("NSSRC", c_uint32),                # NVM Subsystem Reset Control 	                        NSSRC	0	31	RW	0
                ]


class AQA(StructureBase):
    _fields_ = [("ASQS", c_uint32, 12),             # Admin Submission Queue Size 	                        ASQS	0	11	RW	0
                ("Reserved2", c_uint32, 4),         # Reserved	                                            RSV	    12	15	RO	0
                ("ACQS", c_uint32, 12),             # Admin Completion Queue Size 	                        ACQS	16	27	RW	0
                ("Reserved1", c_uint32, 4),         # Reserved	                                            RSV	    28	31	RO	0
                ]


class ASQ(StructureBase):
    _fields_ = [("Reserved", c_uint64, 12),         # Reserved	                                            RSV	    0	11	RO	0
                ("ASQB", c_uint64, 52),             # Admin Submission Queue Base 	                        ASQB	12	63	RW	ImplSpec
                ]


class ACQ(StructureBase):
    _fields_ = [("Reserved", c_uint64, 12),         # Reserved	                                            RSV	    0	11	RO	0
                ("ACQB", c_uint64, 52),             # Admin Completion Queue Base 	                        ACQB	12	63	RW	ImplSpec
                ]


class CMBLOC(StructureBase):
    _fields_ = [("BIR", c_uint32, 3),               # Base Indicator Register 	                            BIR	    0	2	RO	ImplSpec
                ("CQMMS", c_uint32, 1),             # CMB Queue Mixed Memory Support 	                    CQMMS	3	3	RO	ImplSpec
                ("CQPDS", c_uint32, 1),             # CMB Queue Physically Discontiguous Support 	        CQPDS	4	4	RO	ImplSpec
                ("CDPMLS", c_uint32, 1),            # CMB Data Pointer Mixed Locations Support 	            CDPMLS	5	5	RO	ImplSpec
                ("CDPCILS", c_uint32, 1),           # CMB Data Pointer and Command Independent Locations Support 	CDPCILS	6	6	RO	ImplSpec
                ("CDMMMS", c_uint32, 1),            # CMB Data Metadata Mixed Memory Support 	            CDMMMS	7	7	RO	ImplSpec
                ("CQDA", c_uint32, 1),              # CMB Queue Dword Alignment 	                        CQDA	8	8	RO	ImplSpec
                ("Reserved", c_uint32, 3),          # Reserved	                                            RSV	    9	11	RO	0
                ("OFST", c_uint32, 20),             # Offset 	                                            OFST	12	31	RO	ImplSpec
                ]


class CMBSZ(StructureBase):
    _fields_ = [("SQS", c_uint32, 1),               # Submission Queue Support 	                            SQS	    0	0	RO	ImplSpec
                ("CQS", c_uint32, 1),               # Completion Queue Support 	                            CQS	    1	1	RO	ImplSpec
                ("LISTS", c_uint32, 1),             # PRP SGL List Support 	                                LISTS	2	2	RO	ImplSpec
                ("RDS", c_uint32, 1),               # Read Data Support 	                                RDS	    3	3	RO	ImplSpec
                ("WDS", c_uint32, 1),               # Write Data Support 	                                WDS	    4	4	RO	ImplSpec
                ("Reserved", c_uint32, 3),          # Reserved	                                            RSV	    5	7	RO	0
                ("SZU", c_uint32, 4),               # Size Units 	                                        SZU	    8	11	RO	ImplSpec
                ("SZ", c_uint32, 19),               # Size 	                                                SZ	    12	31	RO	ImplSpec
                ]


class BPINFO(StructureBase):
    _fields_ = [("BPSZ", c_uint32, 15),             # Boot Partition Size 	                                BPSZ	0	14	RO	ImplSpec
                ("Reserved2", c_uint32, 9),         # Reserved	                                            RSV	    15	23	RO	0
                ("BRS", c_uint32, 2),               # Boot Read Status 	                                    BRS	    24	25	RO	0
                ("Reserved1", c_uint32, 5),         # Reserved	                                            RSV	    26	30	RO	0
                ("ABPID", c_uint32, 1),             # Active Boot Partition ID 	                            ABPID	31	31	RO	ImplSpec
                ]


class BPRSEL(StructureBase):
    _fields_ = [("BPRSZ", c_uint32, 10),            # Boot Partition Read Size 	                            BPRSZ	0	9	RW	0
                ("BPROF", c_uint32, 20),            # Boot Partition Read Offset 	                        BPROF	10	29	RW	0
                ("Reserved", c_uint32, 1),          # Reserved	                                            RSV	    30	30	RO	0
                ("BPID", c_uint32, 1),              # Boot Partition Identifier 	                        BPID	31	31	RW	0
                ]


class BPMBL(StructureBase):
    _fields_ = [("Reserved", c_uint64, 12),         # Reserved	                                            RSV	    0	11	RO	0
                ("BMBBA", c_uint64, 52),            # Boot Partition Memory Buffer Base Address 	        BMBBA	12	63	RW	0
                ]


class CMBMSC(StructureBase):
    _fields_ = [("CRE", c_uint64, 1),               # Capabilities Registers Enabled 	                    CRE	    0	0	RW	0
                ("CMSE", c_uint64, 1),              # Controller Memory Space Enable 	                    CMSE	1	1	RW	0
                ("Reserved", c_uint64, 10),         # Reserved	                                            RSV	    2	11	RO	0
                ("CBA", c_uint64, 52),              # Controller Base Address 	                            CBA	    12	63	RW	0
                ]


class CMBSTS(StructureBase):
    _fields_ = [("CBAI", c_uint32, 1),              # Reserved	                                            RSV	    1	31	RO	0
                ("Reserved", c_uint32, 31),         # Controller Base Address Invalid 	                    CBAI	0	0	RO	0
                ]


class PMRCAP(StructureBase):
    _fields_ = [("Reserved3", c_uint32, 3),         # Reserved	                                            RSV 	0	2	RO	0
                ("RDS", c_uint32, 1),               # Read Data Support 	                                RDS	    3	3	RO	ImplSpec
                ("WDS", c_uint32, 1),               # Write Data Support 	                                WDS	    4	4	RO	ImplSpec
                ("BIR", c_uint32, 3),               # Base Indicator Register 	                            BIR	    5	7	RO	ImplSpec
                ("PMRTU", c_uint32, 2),             # Persistent Memory Region Time Units 	                PMRTU	8	9	RO	ImplSpec
                ("PMRWBM", c_uint32, 4),            # Persistent Memory Region Write Barrier Mechanisms 	PMRWBM	10	13	RO	ImplSpec
                ("Reserved2", c_uint32, 2),         # Reserved	                                            RSV	    14	15	RO	0
                ("PMRTO", c_uint32, 8),             # Persistent Memory Region Capabilities 	            PMRTO	16	23	RO	ImplSpec
                ("CMSS", c_uint32, 1),              # Controller Memory Space Supported 	                CMSS	24	24	RO	ImplSpec
                ("Reserved1", c_uint32, 6),         # Reserved	                                            RSV	    25	31	RO	0
                ]


class PMRCTL(StructureBase):
    _fields_ = [("EN", c_uint32, 1),                # Enable 	                                            EN	    0	0	RW	0
                ("Reserved", c_uint32, 31),         # Reserved	                                            RSV	    1	31	RO	0
                ]


class PMRSTS(StructureBase):
    _fields_ = [("ERR", c_uint32, 8),               # Error 	                                            ERR	    0	7	RO	0
                ("NRDY", c_uint32, 1),              # Not Ready 	                                        NRDY	8	8	RO	0
                ("HSTS", c_uint32, 3),              # Health Status 	                                    HSTS	9	11	RO	0
                ("CBAI", c_uint32, 1),              # Controller Base Address Invalid 	                    CBAI	12	12	RO	0
                ("Reserved", c_uint32, 19),         # Reserved	                                            RSV	    13	31	RO	0
                ]


class PMREBS(StructureBase):
    _fields_ = [("PMRSZU", c_uint32, 4),            # PMR Elasticity Buffer Size Units 	                    PMRSZU	0	3	RO	ImplSpec
                ("RBB", c_uint32, 1),               # Read Bypass Behavior	                                RBB	    4	4	RO	ImplSpec
                ("Reserved", c_uint32, 3),          # Reserved	                                            RSV	    5	7	RO	0
                ("PMRWBZ", c_uint32, 24),           # PMR Elasticity Buffer Size Base 	                    PMRWBZ	8	31	RO	ImplSpec
                ]


class PMRSWTP(StructureBase):
    _fields_ = [("PMRSWTU", c_uint32, 4),           # PMR Sustained Write Throughput Units 	                PMRSWTU	0	3	RO	ImplSpec
                ("Reserved", c_uint32, 4),          # Reserved	                                            RSV	    4	7	RO	0
                ("PMRSWTV", c_uint32, 24),          # PMR Sustained Write Throughput 	                    PMRSWTV	8	31	RO	ImplSpec
                ]


class PMRMSC(StructureBase):
    _fields_ = [("Reserved2", c_uint64, 1),         # Reserved	                                            RSV	    0	0	RO	0
                ("CMSE", c_uint64, 1),              # Controller Memory Space Enable 	                    CMSE	1	1	RW	0
                ("Reserved1", c_uint64, 10),        # Reserved	                                            RSV	    2	11	RO	0
                ("CBA", c_uint64, 52),              # Controller Base Address 	                            CBA	    12	63	RW	0
                ]


class NvmeRegister(StructureBase):
    _fields_ = [("CAP", CAP),                       # Controller Capabilities	                                            CAP	    0x0	     0x7	8
                ("VS", VS),                         # Version	                                                            VS	    0x8      0xB	4
                ("INTMS", INTMS),                   # Interrupt Mask Set	                                                INTMS	0xC      0xF	4
                ("INTMC", INTMC),                   # Interrupt Mask Clear	                                                INTMC	0x10	 0x13	4
                ("CC", CC),                         # Controller Configuration	                                            CC	    0x14	 0x17	4
                ("Reserved1", c_char * 4),          # Reserved	                                                            RSV 	0x18	 0x1B	4
                ("CSTS", CSTS),                     # Controller Status	                                                    CSTS	0x1C	 0x1F	4
                ("NSSR", NSSR),                     # NVM Subsystem Reset (Optional)	                                    NSSR	0x20	 0x23	4
                ("AQA", AQA),                       # Admin Queue Attributes	                                            AQA	    0x24	 0x27	4
                ("ASQ", ASQ),                       # Admin Submission Queue Base Address	                                ASQ	    0x28	 0x2F	8
                ("ACQ", ACQ),                       # Admin Completion Queue Base Address	                                ACQ	    0x30	 0x37	8
                ("CMBLOC", CMBLOC),                 # Controller Memory Buffer Location (Optional)	                        CMBLOC	0x38	 0x3B	4
                ("CMBSZ", CMBSZ),                   # Controller Memory Buffer Size (Optional)	                            CMBSZ	0x3C	 0x3F	4
                ("BPINFO", BPINFO),                 # Boot Partition Information (Optional)	                                BPINFO	0x40	 0x43	4
                ("BPRSEL", BPRSEL),                 # Boot Partition Read Select (Optional)	                                BPRSEL	0x44	 0x47	4
                ("BPMBL", BPMBL),                   # Boot Partition Memory Buffer Location (Optional)	                    BPMBL	0x48	 0x4F	8
                ("CMBMSC", CMBMSC),                 # Controller Memory Buffer Memory Space (Optional)	                    CMBMSC	0x50	 0x57	8
                ("CMBSTS", CMBSTS),                 # Controller Memory Buffer Status (Optional)	                        CMBSTS	0x58	 0x5B	4
                ("Reserved2", c_char * 3492),       # Reserved	                                                            RSV	    0x5C	 0xDFF	3492
                ("PMRCAP", PMRCAP),                 # Persistent Memory Capabilities (Optional)	                            PMRCAP	0xE00	 0xE03	4
                ("PMRCTL", PMRCTL),                 # Persistent Memory Region Control ((Optional)	                        PMRCTL	0xE04	 0xE07	4
                ("PMRSTS", PMRSTS),                 # Persistent Memory Region Status (Optional)	                        PMRSTS	0xE08	 0xE0B	4
                ("PMREBS", PMREBS),                 # Persistent Memory Region Elasticity Buffer Size	                    PMREBS	0xE0C	 0xE0F	4
                ("PMRSWTP", PMRSWTP),               # Persistent Memory Region Sustained Write Throughput	                PMRSWTP	0xE10	 0xE13	4
                ("PMRMSC", PMRMSC),                 # Persistent Memory Region Controller Memory Space Control (Optional)	PMRMSC	0xE14	 0xE1B	8
                ("Reserved3", c_char * 484),        # Command Set Specific	                                                RSV 	0xE1C	 0xFFF	484
                ]
    def __init__(self):
        super(NvmeRegister, self).__init__()
        self.format_dict = {item[0]:self.to_int for item in self._fields_ if not self.skip_reserved_pattern.search(item[0].lower())}

class NVME_SUBSYS_TYPE(Enum):
    NVME_NQN_DISC	= 1		            #  Discovery type target subsystem
    NVME_NQN_NVME	= 2		            #  NVME type target subsystem

class NVMF_ADRFAM(Enum):
    NVMF_TRTYPE_RDMA	= 1             #  RDMA
    NVMF_TRTYPE_FC		= 2             #  Fibre Channel
    NVMF_TRTYPE_TCP		= 3	            #  TCP
    NVMF_TRTYPE_LOOP	= 254	        #  Reserved for host usage
    NVMF_TRTYPE_MAX     = 255

class NVMF_TREQ(Enum):
    NVMF_TREQ_NOT_SPECIFIED	= 0         #  Not specified
    NVMF_TREQ_REQUIRED	= 1             #  Required
    NVMF_TREQ_NOT_REQUIRED	= 2         #  Not Required
    NVMF_TREQ_DISABLE_SQFLOW = (1 << 2) #  SQ flow control disable supported

class NVMF_RDMA_QPTYPE(Enum):
    NVMF_RDMA_QPTYPE_CONNECTED	= 1     #  Reliable Connected
    NVMF_RDMA_QPTYPE_DATAGRAM	= 2     #  Reliable Datagram

class NVMF_RDMA_PRTYPE(Enum):
    NVMF_RDMA_PRTYPE_NOT_SPECIFIED	= 1 #  No Provider Specified
    NVMF_RDMA_PRTYPE_IB		= 2         #  InfiniBand
    NVMF_RDMA_PRTYPE_ROCE		= 3     #  InfiniBand RoCE
    NVMF_RDMA_PRTYPE_ROCEV2		= 4     #  InfiniBand RoCEV2
    NVMF_RDMA_PRTYPE_IWARP		= 5     #  IWARP

class NVMF_RDMA_CMS_RDMA(Enum):
    NVMF_RDMA_CMS_RDMA_CM	= 1         #  Sockets based endpoint addressing

class NVMF_TCP_SECTYPE(Enum):
    NVMF_TCP_SECTYPE_NONE	= 0         #  No Security
    NVMF_TCP_SECTYPE_TLS	= 1         #  Transport Layer Security

class nvme_id_psd(StructureBase):
    """
    This class represents the NVMe device power state descriptors structure.
    It inherits from StructureBase and encapsulates the power-related attributes of an NVMe device state.
    """
    _fields_ = [
        ('max_power', c_uint16),       # Maximum power consumption of the power state in milliwatts.
        ('rsvd', c_uint8),
        ('flags', c_uint8),
        ('entry_lat', c_uint32),       # Latency for entering the power state, in microseconds.
        ('exit_lat', c_uint32),        # Latency for exiting the power state, in microseconds.
        ('read_tput', c_uint8),
        ('read_lat', c_uint8),
        ('write_tput', c_uint8),
        ('write_lat', c_uint8),
        ('idle_power', c_uint16),
        ('idle_scale', c_uint8),
        ('rsvd1', c_uint8),
        ('active_power', c_uint16),
        ('active_work_scale', c_uint8),
        ('rsvd2', c_uint8 * 9),
    ]


class NVME_PS_FLAGS(Enum):
    """
    Defines flags for NVMe power state settings.
    Each flag represents a specific attribute or behavior of the power state.
    """

    NVME_PS_FLAGS_MAX_POWER_SCALE = 1 << 0
    """
    Indicates that the power state supports maximum power scaling.
    This flag suggests that the power consumption can vary based on specific conditions.
    """

    NVME_PS_FLAGS_NON_OP_STATE = 1 << 1
    """
    Indicates that the power state is a non-operational state.
    This flag suggests that the device is not in a fully operational state during this power state.
    """


class nvme_id_ctrl(StructureBase):
    """
    NVMe Controller Identification Structure.

    This structure contains information about the NVMe controller, including its capabilities,
    features, and operational parameters.
    """
    _fields_ = [
        ('vid', c_uint16),              # PCI Vendor ID
        ('ssvid', c_uint16),            # PCI Subsystem Vendor ID
        ('sn', c_char * 20),            # Serial Number
        ('mn', c_char * 40),            # Model Number
        ('fr', c_char * 8),             # Firmware Revision
        ('rab', c_uint8),               # Recommended Arbitration Burst
        ('ieee', c_uint8 * 3),          # IEEE OUI Identifier
        ('cmic', c_uint8),              # Controller Multi-Path I/O and Namespace Sharing Capabilities
        ('mdts', c_uint8),              # Maximum Data Transfer Size
        ('cntlid', c_uint16),           # Controller ID
        ('ver', c_uint32),              # Version
        ('rtd3r', c_uint32),            # RTD3 Resume Latency
        ('rtd3e', c_uint32),            # RTD3 Entry Latency
        ('oaes', c_uint32),             # Optional Asynchronous Events Supported
        ('ctratt', c_uint32),           # Controller Attributes
        ('rrls', c_uint16),             # Read Recovery Level Support
        ('rsvd1', c_uint8 * 9),         # Reserved
        ('cntrltype', c_uint8),         # Controller Type
        ('fguid', c_char * 16),         # FRU Globally Unique Identifier
        ('crdt1', c_uint16),            # Command Retry Delay Time 1
        ('crdt2', c_uint16),            # Command Retry Delay Time 2
        ('crdt3', c_uint16),            # Command Retry Delay Time 3
        ('rsvd2', c_uint8 * 122),       # Reserved
        ('oacs', c_uint16),             # Optional Admin Command Support
        ('acl', c_uint8),               # Abort Command Limit
        ('aerl', c_uint8),              # Asynchronous Event Request Limit
        ('frmw', c_uint8),              # Firmware Updates
        ('lpa', c_uint8),               # Log Page Attributes
        ('elpe', c_uint8),              # Error Log Page Entries
        ('npss', c_uint8),              # Number of Power States Support
        ('avscc', c_uint8),             # Admin Vendor Specific Command Configuration
        ('apsta', c_uint8),             # Autonomous Power State Transition Attributes
        ('wctemp', c_uint16),           # Warning Composite Temperature Threshold
        ('cctemp', c_uint16),           # Critical Composite Temperature Threshold
        ('mtfa', c_uint16),             # Maximum Time for Firmware Activation
        ('hmpre', c_uint32),            # Host Memory Buffer Preferred Size
        ('hmmin', c_uint32),            # Host Memory Buffer Minimum Size
        ('tnvmcap', c_uint8 * 16),      # Total NVM Capacity
        ('unvmcap', c_uint8 * 16),      # Unallocated NVM Capacity
        ('rpmbs', c_uint32),            # Replay Protected Memory Block Support
        ('edstt', c_uint16),            # Endurance Group Descriptor Table Entry Size
        ('dsto', c_uint8),              # Device Self-test Options
        ('fwug', c_uint8),              # Firmware Update Granularity
        ('kas', c_uint16),              # Keep Alive Support
        ('hctma', c_uint16),            # Host Controlled Thermal Management Attributes
        ('mntmt', c_uint16),            # Minimum Temperature Threshold
        ('mxtmt', c_uint16),            # Maximum Temperature Threshold
        ('sanicap', c_uint32),          # Sanitize Capabilities
        ('hmminds', c_uint32),          # Host Memory Buffer Minimum Descriptor Entry Size
        ('hmmaxd', c_uint16),           # Host Memory Buffer Maximum Descriptors
        ('nsetidmax', c_uint16),        # Namespace Set Identifier Maximum
        ('endgidmax', c_uint16),        # Endurance Group Identifier Maximum
        ('anatt', c_uint8),             # ANA Transition Time
        ('anacap', c_uint8),            # ANA Capabilities
        ('anagrpmax', c_uint32),        # ANA Group Identifier Maximum
        ('nanagrpid', c_uint32),        # Number of ANA Group Identifiers
        ('pels', c_uint32),             # Persistent Event Log Size
        ('rsvd3', c_uint8 * 156),       # Reserved
        ('sqes', c_uint8),              # Submission Queue Entry Size
        ('cqes', c_uint8),              # Completion Queue Entry Size
        ('maxcmd', c_uint16),           # Maximum Outstanding Commands
        ('nn', c_uint32),               # Number of Namespaces
        ('oncs', c_uint16),             # Optional NVM Command Support
        ('fuses', c_uint16),            # Fused Operation Support
        ('fna', c_uint8),               # Format NVM Attributes
        ('vwc', c_uint8),               # Volatile Write Cache
        ('awun', c_uint16),             # Atomic Write Unit Normal
        ('awupf', c_uint16),            # Atomic Write Unit Power Fail
        ('nvscc', c_uint8),             # NVM Vendor Specific Command Configuration
        ('nwpc', c_uint8),              # Namespace Write Protection Capabilities
        ('acwu', c_uint16),             # Atomic Compare & Write Unit
        ('rsvd4', c_uint8 * 2),         # Reserved
        ('sgls', c_uint32),             # SGL Support
        ('mnan', c_uint32),             # Maximum Number of Allowed Namespaces
        ('rsvd5', c_uint8 * 224),       # Reserved
        ('subnqn', c_char * 256),       # Subsystem NQN
        ('rsvd6', c_uint8 * 768),       # Reserved
        ('ioccsz', c_uint32),           # I/O Command Capsule Size
        ('iorcsz', c_uint32),           # I/O Response Capsule Size
        ('icdoff', c_uint16),           # I/O Command Descriptor Offset
        ('ctrattr', c_uint8),           # Controller Attributes
        ('msdbd', c_uint8),             # Maximum SGL Data Block Descriptors
        ('rsvd7', c_uint8 * 1024),      # Reserved
        ('psd', nvme_id_psd * 32), # Power State Descriptors
        ('vs', c_uint8 * 1024),         # Vendor Specific
    ]

class NVME_CTRL_INFO(Enum):
    """
    Defines the various capabilities and attributes of an NVMe controller.

    Each attribute represents a specific operation or feature supported by the controller,
    identified by a bit flag.
    """
    NVME_CTRL_ONCS_COMPARE			        = 1 << 0    # Controller supports the Compare command
    NVME_CTRL_ONCS_WRITE_UNCORRECTABLE	    = 1 << 1    # Controller supports the Write Uncorrectable command
    NVME_CTRL_ONCS_DSM			            = 1 << 2    # Controller supports the Dataset Management command
    NVME_CTRL_ONCS_WRITE_ZEROES		        = 1 << 3    # Controller supports the Write Zeroes command
    NVME_CTRL_ONCS_TIMESTAMP		        = 1 << 6    # Controller supports the Timestamp command

    NVME_CTRL_VWC_PRESENT			        = 1 << 0    # Volatile Write Cache is present

    NVME_CTRL_OACS_SEC_SUPP                 = 1 << 0    # Security commands are supported
    NVME_CTRL_OACS_DIRECTIVES		        = 1 << 5    # Directives commands are supported
    NVME_CTRL_OACS_DBBUF_SUPP		        = 1 << 8    # Device Self-test with Background Buffer is supported

    NVME_CTRL_LPA_CMD_EFFECTS_LOG		    = 1 << 1    # Command effects log page is supported

    NVME_CTRL_CTRATT_128_ID			        = 1 << 0    # 128-bit controller identifier is supported
    NVME_CTRL_CTRATT_NON_OP_PSP		        = 1 << 1    # Non-operational power state permissive is supported
    NVME_CTRL_CTRATT_NVM_SETS		        = 1 << 2    # NVM sets are supported
    NVME_CTRL_CTRATT_READ_RECV_LVLS		    = 1 << 3    # Read receive levels are supported
    NVME_CTRL_CTRATT_ENDURANCE_GROUPS	    = 1 << 4    # Endurance groups are supported
    NVME_CTRL_CTRATT_PREDICTABLE_LAT	    = 1 << 5    # Predictable Latency Mode is supported
    NVME_CTRL_CTRATT_NAMESPACE_GRANULARITY	= 1 << 7    # Namespace granularity log page is supported
    NVME_CTRL_CTRATT_UUID_LIST		        = 1 << 9    # UUID list log page is supported


class nvme_lbaf(StructureBase):
    """
    NVMe Logical Block Address Format structure.

    This structure defines the logical block address format used by NVMe devices,
    including metadata size, data size, and protection information size.
    """
    _fields_ = [
        ('ms', c_uint16),  # Metadata size, in bytes.
        ('ds', c_uint8),   # Data size, in bytes.
        ('rp', c_uint8),   # Relative performance, indicating the performance level of the LBA format.
    ]


class nvme_id_ns(StructureBase):
    """
    NVMe Namespace Identification Structure

    This structure provides detailed information about a specific namespace in an NVMe device, including its size, capacity,
    features, and various operational parameters.
    """
    _fields_ = [
        ('nsze', c_uint64),  # Namespace size in logical blocks (LBAs)
        ('ncap', c_uint64),  # Namespace capacity in logical blocks (LBAs)
        ('nuse', c_uint64),  # Namespace utilization in logical blocks (LBAs)
        ('nsfeat', c_uint8),  # Namespace features
        ('nlbaf', c_uint8),  # Number of LBA formats supported
        ('flbas', c_uint8),  # Formatted LBA size
        ('mc', c_uint8),  # Metadata capabilities
        ('dpc', c_uint8),  # End-to-end data protection capabilities
        ('dps', c_uint8),  # End-to-end data protection settings
        ('nmic', c_uint8),  # Namespace multipath and sharing capabilities
        ('rescap', c_uint8),  # Reservation capabilities
        ('fpi', c_uint8),  # Format progress indicator
        ('dlfeat', c_uint8),  # Deallocate feature support
        ('nawun', c_uint16),  # Namespace optimal write granularity
        ('nawupf', c_uint16),  # Namespace optimal write granularity in power of 2
        ('nacwu', c_uint16),  # Namespace atomic write unit
        ('nabsn', c_uint16),  # Namespace atomic boundary size
        ('nabo', c_uint16),  # Namespace atomic boundary offset
        ('nabspf', c_uint16),  # Namespace atomic boundary size in power of 2
        ('noiob', c_uint16),  # Namespace optimal I/O boundary
        ('nvmcap', c_uint8 * 16),  # Namespace capacity in bytes
        ('npwg', c_uint16),  # Namespace preferred write granularity
        ('npwa', c_uint16),  # Namespace preferred write granularity alignment
        ('npdg', c_uint16),  # Namespace preferred deallocation granularity
        ('npda', c_uint16),  # Namespace preferred deallocation alignment
        ('nows', c_uint16),  # Namespace optimal write size
        ('rsvd1', c_uint8 * 18),  # Reserved for future use
        ('anagrpid', c_uint32),  # ANA group identifier
        ('rsvd2', c_uint8 * 3),  # Reserved for future use
        ('nsattr', c_uint8),  # Namespace attributes
        ('nvmsetid', c_uint16),  # NVM set identifier
        ('endgid', c_uint16),  # Endurance group identifier
        ('nguid', c_uint8 * 16),  # Namespace globally unique identifier
        ('eui64', c_uint8 * 8),  # Namespace IEEE EUI-64 identifier
        ('lbaf', nvme_lbaf * 16),  # LBA format support
        ('rsvd3', c_uint8 * 192),  # Reserved for future use
        ('vs', c_uint8 * 3712),  # Vendor specific data
    ]

class NVME_ID_CNS(Enum):
    """
    Enum class defining constants for NVMe Identify Controller and Namespace data structures.
    These constants are used to specify different types of identify operations and the data they return.
    """
    NVME_ID_CNS_NS = 0x00  # Identifier for Namespace
    NVME_ID_CNS_CTRL = 0x01  # Identifier for Controller
    NVME_ID_CNS_NS_ACTIVE_LIST = 0x02  # Identifier for Active Namespace List
    NVME_ID_CNS_NS_DESC_LIST = 0x03  # Identifier for Namespace Description List
    NVME_ID_CNS_NVMSET_LIST = 0x04  # Identifier for NVM Set List
    NVME_ID_CNS_NS_PRESENT_LIST = 0x10  # Identifier for Present Namespace List
    NVME_ID_CNS_NS_PRESENT = 0x11  # Identifier for Present Namespace
    NVME_ID_CNS_CTRL_NS_LIST = 0x12  # Identifier for Controller Namespace List
    NVME_ID_CNS_CTRL_LIST = 0x13  # Identifier for Controller List
    NVME_ID_CNS_SCNDRY_CTRL_LIST = 0x15  # Identifier for Secondary Controller List
    NVME_ID_CNS_NS_GRANULARITY = 0x16  # Identifier for Namespace Granularity
    NVME_ID_CNS_UUID_LIST = 0x17  # Identifier for UUID List


class NVME_NS_INFO(Enum):
    """
    NVMe namespace information flags and constants.

    This enumeration defines various flags and constants related to NVMe namespace features,
    logical block address formats, protection information, and other attributes.
    """

    # Namespace supports thin provisioning
    NVME_NS_FEAT_THIN	    = 1 << 0

    # Mask for the LBA size field in the FLBAS (Formatted LBA Size) field
    NVME_NS_FLBAS_LBA_MASK	= 0xf

    # FLBAS field indicates metadata extension
    NVME_NS_FLBAS_META_EXT	= 0x10

    # Best relative performance point for LBA format
    NVME_LBAF_RP_BEST	    = 0

    # Better relative performance point for LBA format
    NVME_LBAF_RP_BETTER	    = 1

    # Good relative performance point for LBA format
    NVME_LBAF_RP_GOOD	    = 2

    # Degraded relative performance point for LBA format
    NVME_LBAF_RP_DEGRADED	= 3

    # Last protection information (PI) type in the namespace
    NVME_NS_DPC_PI_LAST	    = 1 << 4

    # First protection information (PI) type in the namespace
    NVME_NS_DPC_PI_FIRST	= 1 << 3

    # Type 3 protection information (PI) supported in the namespace
    NVME_NS_DPC_PI_TYPE3	= 1 << 2

    # Type 2 protection information (PI) supported in the namespace
    NVME_NS_DPC_PI_TYPE2	= 1 << 1

    # Type 1 protection information (PI) supported in the namespace
    NVME_NS_DPC_PI_TYPE1	= 1 << 0

    # First protection information (PI) type in the namespace
    NVME_NS_DPS_PI_FIRST	= 1 << 3

    # Mask for the protection information (PI) types in the namespace
    NVME_NS_DPS_PI_MASK	    = 0x7

    # Type 1 protection information (PI) in the namespace
    NVME_NS_DPS_PI_TYPE1	= 1

    # Type 2 protection information (PI) in the namespace
    NVME_NS_DPS_PI_TYPE2	= 2

    # Type 3 protection information (PI) in the namespace
    NVME_NS_DPS_PI_TYPE3	= 3


class nvme_id_ns_desc(StructureBase):
    """
    NVMe namespace identifier descriptor structure.

    This class defines the structure for NVMe namespace identifier descriptors, inheriting from StructureBase.
    It includes fields for the namespace identifier type, namespace identifier length, and a reserved field.
    """
    _fields_ = [
        ('nidt', c_uint8),  # Namespace identifier type.
        ('nidl', c_uint8),  # Namespace identifier length.
        ('reserved', c_uint16),  # Reserved field for future use or alignment.
    ]


class NVME_NIDT(Enum):
    """
    NVMe Namespace Identifier Type (NIDT) definitions.
    These identifiers are used to specify the type of namespace identifier used in NVMe commands.
    """
    NVME_NIDT_EUI64 = 0x01  # EUI-64 identifier type
    NVME_NIDT_NGUID = 0x02  # NGUID identifier type
    NVME_NIDT_UUID = 0x03   # UUID identifier type


class nvme_nvmset_attr_entry(StructureBase):
    """
    Represents the attributes of an NVMe NVM Set.

    This structure contains information about the characteristics of an NVM Set, including its identifier,
    endurance group, and capacity details.
    """
    _fields_ = [
        ('id', c_uint16),                       # Identifier for the NVM Set.
        ('endurance_group_id', c_uint16),       # Identifier for the endurance group to which the NVM Set belongs.
        ('rsvd1', c_uint32),                    # Reserved field for future use or alignment.
        ('random_4k_read_typical', c_uint32),   # Typical performance metric for 4KB random read operations.
        ('opt_write_size', c_uint32),           # Optimal write size for achieving best performance.
        ('total_nvmset_cap', c_uint8 * 16),     # Total capacity of the NVM Set, represented in 16 bytes.
        ('unalloc_nvmset_cap', c_uint8 * 16),   # Unallocated capacity within the NVM Set, represented in 16 bytes.
        ('rsvd2', c_uint8 * 80),                # Reserved field for future use or alignment.
    ]


class nvme_id_nvmset_list(StructureBase):
    """
    Represents the NVMe NVM Set Identifier structure.

    This class is used to define the structure of NVMe NVM Set Identifiers, inheriting from StructureBase.
    It includes fields such as the NVM Set ID and reserve space, as well as attributes of the NVM Set.
    """
    _fields_ = [
        ('nid', c_uint8),  # NVM Set Identifier, a single unsigned 8-bit integer.
        ('rsvd1', c_uint8 * 127),  # Reserved space, consisting of 127 unsigned 8-bit integers.
        ('ent', nvme_nvmset_attr_entry * 31),  # NVM Set attribute entries, containing 31 such entries.
    ]


class nvme_id_ns_granularity_desc(StructureBase):
    """
    NVMe Namespace Granularity List Entry Structure.

    This structure represents an entry in the namespace granularity list, which defines the granularity
    of namespace size and capacity for NVMe devices.
    """
    _fields_ = [
        ('nszegran', c_uint64),  # Granularity of namespace size in bytes.
        ('ncapgran', c_uint64),  # Granularity of namespace capacity in bytes.
    ]


class nvme_id_ns_granularity_list(StructureBase):
    """
    NVMe Namespace Granularity List Structure.

    This structure contains information about the granularity of namespaces in an NVMe device,
    including attributes, the number of descriptors, reserved fields, and the entries themselves.
    """
    _fields_ = [
        ('attributes', c_uint32),  # Attributes related to the namespace granularity.
        ('num_descriptors', c_uint8),  # Number of descriptors in the granularity list.
        ('rsvd1', c_uint8 * 27),  # Reserved field for future use or alignment.
        ('entry', nvme_id_ns_granularity_desc * 16),  # Array of granularity list entries.
    ]

class nvme_id_uuid_list_entry(StructureBase):
    """
    Represents an entry in the NVMe UUID List.

    This structure defines the format of a single entry in the UUID list, which is used to store unique identifiers
    for namespaces or other NVMe resources. Each entry consists of a header, reserved fields, and a UUID.
    """
    _fields_ = [
        ('header', c_uint8),  # Header field, used for identifying or managing the UUID entry.
        ('rsvd1', c_uint8 * 15),  # Reserved fields, used for future expansion or alignment.
        ('uuid', c_uint8 * 16),  # UUID field, stores a 128-bit universally unique identifier.
    ]


class nvme_id_uuid_list(StructureBase):
    """
    Represents the NVMe Identifier UUID List structure.

    This structure contains a list of UUID entries, each representing a unique identifier
    associated with the NVMe device. The list can hold up to 128 entries.
    """
    _fields_ = [
        ('entry', nvme_id_uuid_list_entry * 128), # Each entry is of type nvme_id_uuid_list_entry and contains a UUID and additional metadata.
    ]


class nvme_telemetry_log(StructureBase):
    """
    NVMe Telemetry Log Page Header Structure.

    This structure defines the header information of an NVMe telemetry log page, including log page index,
    vendor-specific data, controller availability, and diagnostic information.
    """
    _fields_ = [
        ('lpi', c_uint8),  # Log page index, identifies a specific log page.
        ('rsvd', c_uint8 * 4),  # Reserved fields for future expansion or alignment.
        ('iee_oui', c_uint8 * 3),  # IEEE Organizationally Unique Identifier, identifies the source of the log page.
        ('dalb1', c_uint16),  # Data area length byte 1, indicates the length of the first data area.
        ('dalb2', c_uint16),  # Data area length byte 2, indicates the length of the second data area.
        ('dalb3', c_uint16),  # Data area length byte 3, indicates the length of the third data area.
        ('rsvd1', c_uint8 * 368),  # Reserved fields for future expansion or alignment.
        ('ctrlavail', c_uint8),  # Controller availability, indicates the current availability status of the controller.
        ('ctrldgn', c_uint8),  # Controller diagnostic result, indicates the health or fault status of the controller.
        ('rsnident', c_uint8 * 128),  # Identification information, used to further identify or describe the log page.
        ('telemetry_dataarea', Pointer(c_uint8, 'dalb3')),  # Telemetry data area, actual data size depends on specific implementation and requirements.
    ]


class nvme_endurance_group_log(StructureBase):
    """
    NVMe Endurance Group Log Structure.

    This structure contains information about the endurance and usage statistics of an NVMe endurance group.
    It includes various fields that provide insights into the health, usage patterns, and error conditions of the endurance group.
    """
    _fields_ = [
        ('critical_warning', c_uint8),  # Critical warning indicators for the endurance group.
        ('rsvd1', c_uint8 * 2),  # Reserved bytes for future use or alignment.
        ('avl_spare', c_uint8),  # Available spare capacity percentage.
        ('avl_spare_threshold', c_uint8),  # Threshold for available spare capacity that triggers a warning.
        ('percent_used', c_uint8),  # Percentage of endurance group life used.
        ('rsvd2', c_uint8 * 26),  # Reserved bytes for future use or alignment.
        ('endurance_estimate', c_uint8 * 16),  # Estimated endurance of the endurance group.
        ('data_units_read', c_uint8 * 16),  # Total data units read from the endurance group.
        ('data_units_written', c_uint8 * 16),  # Total data units written to the endurance group.
        ('media_units_written', c_uint8 * 16),  # Total media units written to the endurance group.
        ('host_read_cmds', c_uint8 * 16),  # Total read commands issued by the host to the endurance group.
        ('host_write_cmds', c_uint8 * 16),  # Total write commands issued by the host to the endurance group.
        ('media_data_integrity_err', c_uint8 * 16),  # Total media data integrity errors detected in the endurance group.
        ('num_err_info_log_entries', c_uint8 * 16),  # Number of error information log entries for the endurance group.
        ('rsvd3', c_uint8 * 352),  # Reserved bytes for future use or alignment.
    ]


class nvme_smart_log(StructureBase):
    """
    NVMe SMART Log Structure.

    This structure contains SMART (Self-Monitoring, Analysis, and Reporting Technology)
    data for NVMe devices, providing information about the device's health and usage.
    """
    _fields_ = [
        ('critical_warning', c_uint8),  # Critical warning flags indicating device health issues
        ('temperature', c_uint8 * 2),  # Temperature readings, typically in Celsius
        ('avail_spare', c_uint8),  # Percentage of available spare space
        ('spare_thresh', c_uint8),  # Threshold for available spare space below which a warning is issued
        ('percent_used', c_uint8),  # Percentage of NVM life used
        ('endu_grp_crit_warn_sumry', c_uint8),  # Summary of critical warnings for endurance groups
        ('rsvd1', c_uint8 * 25),  # Reserved bytes for future use
        ('data_units_read', c_uint8 * 16),  # Total data units read, typically in 512-byte units
        ('data_units_written', c_uint8 * 16),  # Total data units written, typically in 512-byte units
        ('host_reads', c_uint8 * 16),  # Total number of host read commands
        ('host_writes', c_uint8 * 16),  # Total number of host write commands
        ('ctrl_busy_time', c_uint8 * 16),  # Total time the controller was busy, in minutes
        ('power_cycles', c_uint8 * 16),  # Total number of power cycles
        ('power_on_hours', c_uint8 * 16),  # Total power-on hours
        ('unsafe_shutdowns', c_uint8 * 16),  # Total number of unsafe shutdowns
        ('media_errors', c_uint8 * 16),  # Total number of media errors
        ('num_err_info_log_entries', c_uint8 * 16),  # Total number of error information log entries
        ('warning_temp_time', c_uint32),  # Total time the device was at a warning temperature
        ('critical_comp_time', c_uint32),  # Total time the device was at a critical composite temperature
        ('temp_sensor', c_uint16 * 8),  # Temperature readings from up to 8 sensors
        ('thm_temp1_trans_count', c_uint32),  # Number of transitions into thermal temperature 1
        ('thm_temp2_trans_count', c_uint32),  # Number of transitions into thermal temperature 2
        ('thm_temp1_total_time', c_uint32),  # Total time in thermal temperature 1
        ('thm_temp2_total_time', c_uint32),  # Total time in thermal temperature 2
        ('rsvd2', c_uint8 * 280),  # Reserved bytes for future use
    ]


class nvme_self_test_res(StructureBase):
    """
    NVMe Self-Test Result Structure.

    This structure contains the result of an NVMe device self-test, including various status and error information.
    """
    _fields_ = [
        ('dsts', c_uint8),  # Device Self-Test Status, indicates the status of the self-test.
        ('seg', c_uint8),   # Segment Number, identifies the segment of the self-test.
        ('vdi', c_uint8),   # Valid Diagnostic Information, indicates the validity of the diagnostic information.
        ('rsvd3', c_uint8), # Reserved, reserved for future use.
        ('poh', c_uint64),  # Power-On Hours, indicates the number of power-on hours at the time of the self-test.
        ('nsid', c_uint32), # Namespace Identifier, identifies the namespace on which the self-test was performed.
        ('flba', c_uint64), # First Failed Logical Block Address, indicates the address of the first failed block.
        ('sct', c_uint8),   # Status Code Type, indicates the type of status code.
        ('sc', c_uint8),    # Status Code, indicates the specific status code of the self-test result.
        ('vs', c_uint8 * 2),# Vendor Specific, vendor-specific information.
    ]


class NVME_ST_INFO(Enum):
    """
    Enum class defining constants for NVMe Self-Test Information.

    This enumeration contains various status codes and flags related to NVMe self-test operations.
    Each member represents a specific status or flag used in the self-test process.
    """

    # Bit shift value for extracting the status code from a result
    NVME_ST_CODE_SHIFT = 4

    # Status codes for short and extended operations
    NVME_ST_CODE_SHORT_OP = 0x1  # Short operation status code
    NVME_ST_CODE_EXT_OP = 0x2     # Extended operation status code
    NVME_ST_CODE_VS = 0xe         # Vendor-specific status code

    # Mask for isolating the result field in a status code
    NVME_ST_RES_MASK = 0xf

    # Result codes indicating different self-test outcomes
    NVME_ST_RES_NO_ERR = 0x0          # No error occurred
    NVME_ST_RES_ABORTED = 0x1         # Operation was aborted
    NVME_ST_RES_CLR = 0x2             # Cleared state
    NVME_ST_RES_NS_REMOVED = 0x3      # Namespace removed during operation
    NVME_ST_RES_ABORTED_FORMAT = 0x4  # Format operation was aborted
    NVME_ST_RES_FATAL_ERR = 0x5       # Fatal error occurred
    NVME_ST_RES_UNKNOWN_SEG_FAIL = 0x6  # Unknown segment failure
    NVME_ST_RES_KNOWN_SEG_FAIL = 0x7   # Known segment failure
    NVME_ST_RES_ABORTED_UNKNOWN = 0x8  # Aborted for an unknown reason
    NVME_ST_RES_ABORTED_SANITIZE = 0x9 # Sanitize operation was aborted
    NVME_ST_RES_NOT_USED = 0xf        # Result not used

    # Flags indicating which fields in the self-test result are valid
    NVME_ST_VALID_NSID = 1 << 0  # Namespace ID is valid
    NVME_ST_VALID_FLBA = 1 << 1  # First Logical Block Address is valid
    NVME_ST_VALID_SCT = 1 << 2   # Status Code Type is valid
    NVME_ST_VALID_SC = 1 << 3    # Status Code is valid

    # Number of reports generated by the self-test
    NVME_ST_REPORTS = 20


class nvme_self_test_log(StructureBase):
    """
    NVMe Self-Test Log Structure

    This structure represents the NVMe self-test log, which contains information about the current device self-test operation
    and the results of up to 20 previous self-tests.
    """
    _fields_ = [
        ('crnt_dev_selftest_oprn', c_uint8), # Current device self-test operation code, indicating the type of self-test currently being performed.
        ('crnt_dev_selftest_compln', c_uint8),# Current device self-test completion percentage, representing the progress of the ongoing self-test.
        ('rsvd', c_uint8 * 2), # Reserved bytes, used for future expansion or alignment.
        ('result', nvme_self_test_res * 20),# Array of self-test results, each entry is of type nvme_self_test_res, containing details of up to 20 previous self-tests.
    ]

class nvme_firmware_slot(StructureBase):
    """
    NVMe Firmware Slot Information Log Structure

    This structure represents the NVMe firmware slot information log, which provides details about the firmware slots
    available on the NVMe device, including the active firmware slot and the firmware revision for each slot.
    """
    _fields_ = [
        ('afi', c_uint8),  # Active Firmware Info, indicates the active firmware slot.
        ('rsvd1', c_uint8 * 7),  # Reserved field, used for future expansion or alignment.
        ('frs', c_uint64 * 7),  # Firmware Revision Slots, firmware revision for each of the 7 firmware slots.
        ('rsvd2', c_uint8 * 448),  # Reserved field, used for future expansion or alignment.
    ]


class nvme_lba_status_desc(StructureBase):
    """
    NVMe LBA Status Descriptor Structure.

    This structure represents the status of a range of Logical Block Addresses (LBAs) in an NVMe device.
    It includes the starting LBA, the number of LBAs, and the status of the range.
    """
    _fields_ = [
        ('dslba', c_uint64),  # Starting LBA of the range.
        ('nlb', c_uint32),    # Number of LBAs in the range.
        ('rsvd1', c_uint8),   # Reserved field for future use or alignment.
        ('status', c_uint8),  # Status of the LBA range.
        ('rsvd2', c_uint8 * 2),  # Reserved fields for future use or alignment.
    ]


class nvme_lba_status(StructureBase):
    """
    NVMe LBA Status Structure.

    This structure represents the status of Logical Block Addresses (LBAs) in an NVMe device.
    It includes information about the number of LBA status descriptors, the completion count,
    reserved fields, and a pointer to an array of LBA status descriptors.
    """
    _fields_ = [
        ('nlsd', c_uint32),  # Number of LBA status descriptors.
        ('cmpc', c_uint8),   # Completion count.
        ('rsvd', c_uint8 * 3),  # Reserved fields for future use or alignment.
        ('descs', Pointer(nvme_lba_status_desc, "nlsd")),  # Pointer to an array of LBA status descriptors.
    ]


class NVME_NS_WRITE_PROTECT_INFO(Enum):
    """
    Defines the write protection states for an NVMe namespace.

    This enumeration specifies the different levels of write protection that can be applied to an NVMe namespace.
    """

    NVME_NS_NO_WRITE_PROTECT            = 0
    """
    Indicates that the namespace has no write protection enabled.
    Data can be freely written to the namespace.
    """

    NVME_NS_WRITE_PROTECT               = 1
    """
    Indicates that the namespace is write-protected.
    Write operations are restricted until the protection is explicitly removed.
    """

    NVME_NS_WRITE_PROTECT_POWER_CYCLE   = 2
    """
    Indicates that the namespace is write-protected until the next power cycle.
    After a power cycle, the write protection will be automatically removed.
    """

    NVME_NS_WRITE_PROTECT_PERMANENT     = 3
    """
    Indicates that the namespace is permanently write-protected.
    Write operations are permanently disabled and cannot be reverted.
    """


class nvme_ns_list(StructureBase):
    """
    This class represents the NVMe namespace list.

    It inherits from StructureBase and is used to define the structure of the NVMe changed namespace list log.
    The main purpose of this class is to encapsulate the log data of the changed namespace list, making it convenient to access and manage.
    """
    _fields_ = [
        ('log', c_uint32 * 1024),
        """
        Defines the log field as an array of type c_uint32 with a length of 1024.
        This field is used to store the list of changed namespace IDs.
        Using a fixed-length array facilitates efficient storage and processing of log data.
        """
    ]


class NVME_CMD_EFFECTS(Enum):
    """
    Defines the command effects for NVMe commands.

    Each command effect is represented by a bit flag, indicating specific behaviors or outcomes
    associated with the execution of NVMe commands.
    """
    NVME_CMD_EFFECTS_CSUPP      = 1 << 0 # Command Supported (CSUPP): Indicates that the command is supported by the controller.
    NVME_CMD_EFFECTS_LBCC       = 1 << 1 # Logical Block Content Change (LBCC): Indicates that the command may change the logical block contents.
    NVME_CMD_EFFECTS_NCC        = 1 << 2 # Namespace Capability Change (NCC): Indicates that the command may change the namespace capabilities.
    NVME_CMD_EFFECTS_NIC        = 1 << 3 # Namespace Inventory Change (NIC): Indicates that the command may change the namespace inventory.
    NVME_CMD_EFFECTS_CCC        = 1 << 4 # Controller Capability Change (CCC): Indicates that the command may change the controller capabilities.
    NVME_CMD_EFFECTS_CSE_MASK   = 3 << 16 # Command Submission and Execution Mask (CSE_MASK): A mask for command submission and execution effects.
    NVME_CMD_EFFECTS_UUID_SEL   = 1 << 19 # UUID Selection (UUID_SEL): Indicates that the command may select a UUID.


class nvme_cmd_effects_log(StructureBase):
    """
    NVMe Effects Log structure, used to describe the effects log of NVMe devices.
    This class inherits from StructureBase.

    The effects log is used to describe the effects of various commands on the NVMe device,
    such as changes in available capacity, impacts on performance, etc.
    """
    _fields_ = [
        ('acs', c_uint32 * 256),  # Array of 256 32-bit unsigned integers, used to store the effects of administrative commands
        ('iocs', c_uint32 * 256),  # Array of 256 32-bit unsigned integers, used to store the effects of I/O commands
        ('rsvd', c_uint8 * 2048),  # Array of 2048 8-bit unsigned integers, reserved for future use or special purposes
    ]


class NVME_ANA_STATE(Enum):
    """
    Defines the enumeration class for NVMe ANA (Asymmetric Namespace Access) states.
    Each member represents a specific ANA state of an NVMe device.
    """
    NVME_ANA_OPTIMIZED = 0x01 # ANA state: Optimized
    NVME_ANA_NONOPTIMIZED = 0x02 # ANA state: Non-optimized
    NVME_ANA_INACCESSIBLE = 0x03 # ANA state: Inaccessible
    NVME_ANA_PERSISTENT_LOSS = 0x04 # ANA state: Persistent Loss
    NVME_ANA_CHANGE = 0x0f # ANA state: Change


class nvme_ana_group_desc(StructureBase):
    """
    NVMe ANA Group Descriptor Structure

    This class represents the NVMe ANA (Asymmetric Namespace Access) group descriptor,
    inheriting from StructureBase. It contains information about a specific ANA group,
    including its identifier, the number of namespaces, change count, state, reserved fields,
    and a pointer to an array of namespace identifiers.
    """
    _fields_ = [
        ('grpid', c_uint32),  # ANA Group Identifier, uniquely identifies the ANA group.
        ('nnsids', c_uint32),  # Number of Namespace Identifiers in the ANA group.
        ('chgcnt', c_uint64),  # Change Count, indicates the number of times the ANA group has changed.
        ('state', c_uint8),  # State of the ANA group, indicating its accessibility.
        ('rsvd1', c_uint8 * 15),  # Reserved field, used for future expansion or alignment.
        ('nsids', Pointer(c_uint32, "nnsids")),  # Pointer to an array of Namespace Identifiers belonging to the ANA group.
    ]


class nvme_ana_log(StructureBase):
    """
    NVMe ANA (Asymmetric Namespace Access) Response Header Structure.

    This structure represents the header of the NVMe ANA response, which provides information
    about the ANA groups and their states. The ANA feature allows NVMe devices to report
    the accessibility of namespaces from different controllers.
    """
    _fields_ = [
        ('chgcnt', c_uint64),  # Change Count: A 64-bit value that increments each time the ANA state changes.
        ('ngrps', c_uint16),   # Number of Groups: A 16-bit value indicating the number of ANA groups.
        ('rsvd1', c_uint16 * 3),  # Reserved: 3 x 16-bit reserved fields for future use.
    ]


class NVME_SMART_CRIT(Enum):
    """
    An enumeration class for NVMe SSD smart critical warning flags.

    Each member of the enumeration represents a specific health or status concern for the NVMe drive,
    with corresponding bit values to indicate which aspects of the drive's health are below normal operating conditions.
    """
    NVME_SMART_CRIT_SPARE = 1 << 0 # Represents the critical warning flag for spare resources, indicating potential issues with the drive's reserve space.
    NVME_SMART_CRIT_TEMPERATURE = 1 << 1 # Represents the critical warning flag for temperature, indicating that the drive temperature may affect performance or reliability.
    NVME_SMART_CRIT_RELIABILITY = 1 << 2 # Represents the general reliability critical warning flag, indicating potential issues with the drive's reliability.
    NVME_SMART_CRIT_MEDIA = 1 << 3 # Represents the critical warning flag for media errors, indicating problems with the drive's storage media.
    NVME_SMART_CRIT_VOLATILE_MEMORY = 1 << 4# Represents the critical warning flag for volatile memory, indicating issues with the drive's volatile memory, such as cache.


class NVME_AER_INFO(Enum):
    """
    NVMe Asynchronous Event Request (AER) Information Types.

    This enumeration defines the different types of asynchronous events that can be reported by an NVMe device.
    Each event type is associated with a specific identifier used to identify and handle the event.
    """
    NVME_AER_ERROR = 0
    """
    Error event.
    Indicates that an error condition has been detected by the NVMe device.
    """

    NVME_AER_SMART = 1
    """
    SMART event.
    Indicates that there is a change in the SMART (Self-Monitoring, Analysis, and Reporting Technology) status of the NVMe device.
    """

    NVME_AER_CSS = 6
    """
    Change in Controller State event.
    Indicates that there is a change in the state of the NVMe controller.
    """

    NVME_AER_VS = 7
    """
    Vendor Specific event.
    Indicates that a vendor-specific asynchronous event has occurred.
    """


class nvme_lba_range_type(StructureBase):
    """
    Represents the NVMe LBA (Logical Block Address) Range Type structure.
    This structure defines the layout and attributes of an LBA range type for NVMe devices.
    """
    _fields_ = [
        ('type', c_uint8),   # Defines the attributes of the LBA range.
        ('attributes', c_uint8), # Defines the attributes of the LBA range.
        ('rsvd1', c_uint8 * 14),  # Reserved field for future use, ensuring compatibility with future standards or extensions.
        ('slba', c_uint64), # Starting LBA (Logical Block Address) of the range, indicating where the range begins on the NVMe device.
        ('nlb', c_uint64), # Number of logical blocks in the range, indicating the size of the range.
        ('guid', c_uint8 * 16), # Globally unique identifier for the LBA range, used to uniquely identify the range.
        ('rsvd2', c_uint8 * 16), # Additional reserved field, further ensuring compatibility or used for supplementary features.
    ]


class NVME_LBART_INFO(Enum):
    """
    Enum class defining constants for NVMe LBA Range Type Information.

    This enumeration specifies various types and attributes of NVMe LBA ranges.
    Each member represents a specific type or attribute used to categorize and describe LBA ranges within an NVMe device.
    """

    # LBA Range Types
    NVME_LBART_TYPE_FS = 0x01
    """
    Indicates that the LBA range is used for file system data.
    """

    NVME_LBART_TYPE_RAID = 0x02
    """
    Indicates that the LBA range is used for RAID configurations.
    """

    NVME_LBART_TYPE_CACHE = 0x03
    """
    Indicates that the LBA range is used for caching purposes.
    """

    NVME_LBART_TYPE_SWAP = 0x04
    """
    Indicates that the LBA range is used for swap space.
    """

    # LBA Range Attributes
    NVME_LBART_ATTRIB_TEMP = 1 << 0
    """
    Indicates that the LBA range has a temporary attribute.
    This suggests that the range may not persist across reboots or other state changes.
    """

    NVME_LBART_ATTRIB_HIDE = 1 << 1
    """
    Indicates that the LBA range should be hidden from certain views or operations.
    This attribute can be used to prevent the range from being displayed or accessed in specific contexts.
    """


class nvme_plm_config(StructureBase):
    """
    NVMe Performance Logging and Monitoring Configuration Structure

    This structure defines the configuration parameters for performance logging and monitoring in an NVMe device.
    It includes settings to enable or disable events and set thresholds for read, write, and time windows.
    """
    _fields_ = [
        ('enable_event', c_uint16),       # Flag to enable or disable performance monitoring events. Setting this flag allows or prevents the generation of performance-related events.
        ('rsvd1', c_uint8 * 30),          # Reserved field for future use or expansion. Currently not utilized but provides space for additional configuration parameters.
        ('dtwin_reads_thresh', c_uint64), # Threshold for read operations within a data window. When the number of read operations exceeds this threshold, a performance event is triggered.
        ('dtwin_writes_thresh', c_uint64),# Threshold for write operations within a data window. When the number of write operations exceeds this threshold, a performance event is triggered.
        ('dtwin_time_thresh', c_uint64),  # Time threshold for the data window. If the specified time duration elapses, a performance event is generated based on the activity within that window.
        ('rsvd2', c_uint8 * 456),         # Another reserved field for future use or expansion, providing additional space for potential configuration parameters.
    ]


class nvme_resv_status_item(StructureBase):
    """
    NVMe Reservation Status Item Structure.

    This structure represents an item in the NVMe reservation status list, which contains information about
    reservations held by different controllers and hosts.
    """
    _fields_ = [
        ('cntlid', c_uint16),  # Controller Identifier, uniquely identifies the controller holding the reservation.
        ('rcsts', c_uint8),    # Reservation Status Code, indicates the status of the reservation.
        ('resv1', c_uint8 * 5),# Reserved field, used for future expansion or alignment.
        ('hostid', c_uint64),  # Host Identifier, uniquely identifies the host holding the reservation.
        ('rkey', c_uint64),    # Reservation Key, a unique key associated with the reservation.
    ]


class nvme_resv_status(StructureBase):
    """
    NVMe Reservation Status Structure.

    This structure represents the reservation status of an NVMe namespace, including details about the reservation
    generation, type, control, and pointers to additional reservation status items.
    """
    _fields_ = [
        ('gen', c_uint32),  # Reservation generation number.
        ('rtype', c_uint8),  # Reservation type.
        ('regctl', c_uint8 * 2),  # Reservation control.
        ('ptpls', c_uint8),  # Persistent Through Power Loss State (PTPLS).
        ('rsvd10', c_uint8 * 13),  # Reserved fields.
        ('entry', Pointer(nvme_resv_status_item, "gen")),  # Pointer to an array of reservation control data structures.
    ]


class nvme_registered_ctrl_ext(StructureBase):
    """
    NVMe Reservation Status Extended Item Structure.

    This structure represents an extended item in the NVMe reservation status log, providing detailed information
    about the reservation status of a namespace for a specific controller.
    """
    _fields_ = [
        ('cntlid', c_uint16),  # Controller ID, identifies the controller that holds the reservation.
        ('rcsts', c_uint8),    # Reservation status code, indicates the status of the reservation.
        ('resv1', c_uint8 * 5),# Reserved field, used for future expansion or alignment.
        ('rkey', c_uint64),    # Reservation key, a unique identifier for the reservation.
        ('hostid', c_uint8 * 16),# Host ID, identifies the host that holds the reservation.
        ('resv32', c_uint8 * 32),# Reserved field, used for future expansion or alignment.
    ]


class nvme_reservation_status_ext(StructureBase):
    """
    NVMe Reservation Status Extension Structure.

    This structure extends the NVMe reservation status information, providing additional details about the reservation status
    of an NVMe namespace. It includes fields for generation, reservation type, registration control, persistent reservation type
    list, reserved fields, and a pointer to extended registration control data items.
    """
    _fields_ = [
        ('gen', c_uint32),  # Generation, indicates the version of the reservation status information.
        ('rtype', c_uint8),  # Reservation Type, specifies the type of reservation.
        ('regctl', c_uint16),  # Registration Control, contains control information for the reservation.
        ('ptpls', c_uint8),  # Persistent Reservation Type List Support, indicates support for different persistent reservation types.
        ('rsvd10', c_uint8 * 14),  # Reserved, reserved for future use or alignment.
        ('resv24', c_uint8 * 40),  # Reserved, reserved for future use or alignment.
        ('regctl_eds', Pointer(nvme_registered_ctrl_ext, "regctl")),  # Pointer to an array of extended registration control data items.
    ]


class NVME_ASYNC_EVENT_TYPE(Enum):
    """
    Defines the types of asynchronous events that can be reported by an NVMe device.

    Each event type is associated with a specific identifier used to identify and handle the event.
    """
    NVME_AER_TYPE_ERROR = 0
    """
    Error event.
    Indicates that an error condition has been detected by the NVMe device.
    """

    NVME_AER_TYPE_SMART = 1
    """
    SMART event.
    Indicates that there is a change in the SMART (Self-Monitoring, Analysis, and Reporting Technology) status of the NVMe device.
    """

    NVME_AER_TYPE_NOTICE = 2
    """
    Notice event.
    Indicates that a general notification has been issued by the NVMe device.
    """


class NVME_OPCODE(Enum):
    """
    NVMe Command Opcodes Enumeration.

    This enumeration defines the command opcodes used in NVMe (NVM Express) commands.
    Each opcode corresponds to a specific operation that can be performed on an NVMe device.
    """
    nvme_cmd_flush = 0x00  # Flush command, used to flush cached data to the storage device.
    nvme_cmd_write = 0x01  # Write command, used to write data to the storage device.
    nvme_cmd_read = 0x02  # Read command, used to read data from the storage device.
    nvme_cmd_write_uncor = 0x04  # Write Uncorrectable command, used to write uncorrectable data to the storage device.
    nvme_cmd_compare = 0x05  # Compare command, used to compare data on the storage device with provided data.
    nvme_cmd_write_zeroes = 0x08  # Write Zeroes command, used to write zeroes to a specified range on the storage device.
    nvme_cmd_dsm = 0x09  # Dataset Management command, used to manage datasets on the storage device, such as Trim.
    nvme_cmd_verify = 0x0c  # Verify command, used to verify the integrity of data on the storage device.
    nvme_cmd_resv_register = 0x0d  # Reservation Register command, used to register a reservation key for a namespace.
    nvme_cmd_resv_report = 0x0e  # Reservation Report command, used to report the reservation status of a namespace.
    nvme_cmd_resv_acquire = 0x11  # Reservation Acquire command, used to acquire a reservation on a namespace.
    nvme_cmd_resv_release = 0x15  # Reservation Release command, used to release a reservation on a namespace.


class NVME_SGL_FMT(Enum):
    """
    NVMe SGL (Scatter-Gather List) Format Enumerations.

    This enumeration defines the different formats used for NVMe Scatter-Gather Lists,
    which are used to describe the data buffers for NVMe commands.
    """
    NVME_SGL_FMT_ADDRESS = 0x00
    """
    Indicates that the SGL format uses an address-based approach.
    Each segment in the SGL specifies a memory address and length.
    """
    NVME_SGL_FMT_OFFSET = 0x01
    """
    Indicates that the SGL format uses an offset-based approach.
    Each segment in the SGL specifies an offset from a base address and length.
    """
    NVME_SGL_FMT_TRANSPORT_A = 0x0A
    """
    Indicates that the SGL format uses a transport-specific format A.
    This format is defined by the transport layer and may vary.
    """
    NVME_SGL_FMT_INVALIDATE = 0x0f
    """
    Indicates that the SGL format is used to invalidate a previously provided SGL.
    This is used to release resources associated with a previous SGL.
    """


class NVME_SGL_TYPE(Enum):
    """
    Defines the types of Scatter-Gather List (SGL) formats used in NVMe commands.

    Each type specifies a different way of describing data buffers for data transfer operations.
    """

    NVME_SGL_FMT_DATA_DESC = 0x00
    """
    Data Descriptor format.
    Used to describe a segment of data for data transfer.
    """

    NVME_SGL_FMT_SEG_DESC = 0x02
    """
    Segment Descriptor format.
    Used to describe a segment of data with additional metadata.
    """

    NVME_SGL_FMT_LAST_SEG_DESC = 0x03
    """
    Last Segment Descriptor format.
    Used to describe the last segment of data in a sequence.
    """

    NVME_KEY_SGL_FMT_DATA_DESC = 0x04
    """
    Keyed Data Descriptor format.
    Used to describe a segment of data with an associated key.
    """

    NVME_TRANSPORT_SGL_DATA_DESC = 0x05
    """
    Transport Layer Data Descriptor format.
    Used to describe data segments at the transport layer.
    """


class nvme_sgl_desc(StructureBase):
    """
    NVMe Scatter-Gather List (SGL) Descriptor Structure

    This class represents the structure of an NVMe Scatter-Gather List descriptor,
    which is used to describe the memory regions involved in data transfers.
    """
    _fields_ = [
        ('addr', c_uint64),  # Address of the data buffer, using 64-bit unsigned integer.
        ('length', c_uint32),  # Length of the data buffer, using 32-bit unsigned integer.
        ('rsvd', c_uint8 * 3),  # Reserved field, used for future expansion or alignment.
        ('type', c_uint8),  # Type of the SGL descriptor, using 8-bit unsigned integer.
    ]


class nvme_keyed_sgl_desc(StructureBase):
    """
    NVMe Keyed Scatter-Gather List Descriptor Structure.

    This structure represents a keyed scatter-gather list (SGL) descriptor used in NVMe commands.
    It includes fields for the address, length, key, and type of the SGL descriptor.
    """
    _fields_ = [
        ('addr', c_uint64),  # Address of the data block.
        ('length', c_uint8 * 3),  # Length of the data block, using 3 uint8 fields.
        ('key', c_uint32),  # Key associated with the data block.
        ('type', c_uint8),  # Type of the SGL descriptor.
    ]


class NVME_CMD_INFO(Enum):
    """
    Defines flags for NVMe command information.

    These flags are used to specify various attributes or behaviors of NVMe commands,
    particularly related to command fusion and scatter-gather list (SGL) handling.
    """

    NVME_CMD_FUSE_FIRST = (1 << 0)
    """
    Indicates that the command is the first command in a fused command sequence.
    """

    NVME_CMD_FUSE_SECOND = (1 << 1)
    """
    Indicates that the command is the second command in a fused command sequence.
    """

    NVME_CMD_SGL_METABUF = (1 << 6)
    """
    Indicates that the command uses a metadata buffer in the scatter-gather list (SGL).
    """

    NVME_CMD_SGL_METASEG = (1 << 7)
    """
    Indicates that the command uses a metadata segment in the scatter-gather list (SGL).
    """

    NVME_CMD_SGL_ALL = NVME_CMD_SGL_METABUF | NVME_CMD_SGL_METASEG
    """
    Indicates that the command uses both a metadata buffer and a metadata segment in the scatter-gather list (SGL).
    """


class NVME_RW_INFO(Enum):
    """
    NVMe Read/Write Operation Information Flags.

    This enumeration defines various flags used to specify characteristics and behaviors of NVMe read/write operations.
    Each flag represents a specific attribute or feature that can be applied to read/write commands.
    """

    # Limited Range flag, indicating that the read operation is limited to a specific range.
    NVME_RW_LR = 1 << 15

    # Force Unit Access flag, indicating that the write operation should not be cached.
    NVME_RW_FUA = 1 << 14

    # Deallocate Access Count flag, related to wear leveling and garbage collection.
    NVME_RW_DEAC = 1 << 9

    # Data Set Management (DSM) frequency flags, indicating the expected frequency of data access.
    NVME_RW_DSM_FREQ_UNSPEC = 0
    NVME_RW_DSM_FREQ_TYPICAL = 1
    NVME_RW_DSM_FREQ_RARE = 2
    NVME_RW_DSM_FREQ_READS = 3
    NVME_RW_DSM_FREQ_WRITES = 4
    NVME_RW_DSM_FREQ_RW = 5
    NVME_RW_DSM_FREQ_ONCE = 6
    NVME_RW_DSM_FREQ_PREFETCH = 7
    NVME_RW_DSM_FREQ_TEMP = 8

    # DSM latency flags, indicating the expected latency for the operation.
    NVME_RW_DSM_LATENCY_NONE = 0 << 4
    NVME_RW_DSM_LATENCY_IDLE = 1 << 4
    NVME_RW_DSM_LATENCY_NORM = 2 << 4
    NVME_RW_DSM_LATENCY_LOW = 3 << 4

    # Sequential request flag, indicating that the operation is part of a sequential access pattern.
    NVME_RW_DSM_SEQ_REQ = 1 << 6

    # Compressed data flag, indicating that the data is compressed.
    NVME_RW_DSM_COMPRESSED = 1 << 7

    # Protection Information (PI) check flags, used for data integrity checks.
    NVME_RW_PRINFO_PRCHK_REF = 1 << 10
    NVME_RW_PRINFO_PRCHK_APP = 1 << 11
    NVME_RW_PRINFO_PRCHK_GUARD = 1 << 12
    NVME_RW_PRINFO_PRACT = 1 << 13

    # Data type streams flag, indicating that the data is part of a stream.
    NVME_RW_DTYPE_STREAMS = 1 << 4

class NVME_DSMGMT(Enum):
    """
    NVMe Dataset Management (DSM) Flags.

    This enumeration defines the flags used in NVMe Dataset Management (DSM) commands.
    Each flag indicates a specific operation or attribute related to dataset management.
    """

    NVME_DSMGMT_IDR = 1 << 0
    """
    Identify Read (IDR).

    This flag indicates that the DSM command should perform an identify read operation.
    """

    NVME_DSMGMT_IDW = 1 << 1
    """
    Identify Write (IDW).

    This flag indicates that the DSM command should perform an identify write operation.
    """

    NVME_DSMGMT_AD = 1 << 2
    """
    Attribute Descriptor (AD).

    This flag indicates that the DSM command should include attribute descriptors.
    """


class nvme_dsm_range(StructureBase):
    """
    NVMe Dataset Management (DSM) Range Structure.

    This structure is used to specify a range of Logical Block Addresses (LBAs) for dataset management operations.
    It includes fields for command attributes, the number of logical blocks, and the starting LBA.
    """
    _fields_ = [
        ('cattr', c_uint32),  # Command attributes, specifying the behavior of the dataset management operation.
        ('nlb', c_uint32),    # Number of logical blocks to be managed in the dataset management operation.
        ('slba', c_uint64),   # Starting Logical Block Address (LBA) of the range to be managed.
    ]

class nvme_feat_auto_pst(StructureBase):
    """
    This class defines the structure for NVMe automatic power state features.

    It inherits from StructureBase, indicating that it is specifically designed for NVMe features,
    ensuring that the structure is correctly interpreted and utilized in NVMe environments.
    """
    _fields_ = [
        ('entries', c_uint64 * 32),
        """
        An array consisting of 32 c_uint64 elements. 
        Each element represents a power state configuration entry, totaling 32 entries. 
        This design allows for the detailed configuration and management of NVMe device power states, optimizing performance and energy efficiency.
        """
    ]


class NVME_HOST_MEM(Enum):
    """
    Defines flags related to NVMe host memory buffer operations.

    Each flag represents a specific operation or state related to the host memory buffer used by NVMe devices.
    """

    NVME_HOST_MEM_ENABLE = (1 << 0)
    """
    Indicates that the NVMe host memory buffer should be enabled.

    This flag is used to enable the use of the host memory buffer for NVMe operations.
    """

    NVME_HOST_MEM_RETURN = (1 << 1)
    """
    Indicates that the NVMe host memory buffer should be returned.

    This flag is used to request the return or release of the host memory buffer used by NVMe operations.
    """


class NVME_ADMIN_OPCODE(Enum):
    """
    NVMe Admin Command Opcodes.

    This enumeration defines the opcodes for NVMe admin commands, which are used to manage and configure NVMe devices.
    Each opcode corresponds to a specific administrative operation that can be performed on the NVMe controller or namespaces.
    """
    nvme_admin_delete_sq        = 0x00,  # Delete Submission Queue
    nvme_admin_create_sq        = 0x01,  # Create Submission Queue
    nvme_admin_get_log_page     = 0x02,  # Get Log Page
    nvme_admin_delete_cq        = 0x04,  # Delete Completion Queue
    nvme_admin_create_cq        = 0x05,  # Create Completion Queue
    nvme_admin_identify         = 0x06,  # Identify
    nvme_admin_abort_cmd        = 0x08,  # Abort Command
    nvme_admin_set_features     = 0x09,  # Set Features
    nvme_admin_get_features     = 0x0a,  # Get Features
    nvme_admin_async_event      = 0x0c,  # Asynchronous Event Request
    nvme_admin_ns_mgmt          = 0x0d,  # Namespace Management
    nvme_admin_activate_fw      = 0x10,  # Activate Firmware
    nvme_admin_download_fw      = 0x11,  # Download Firmware
    nvme_admin_dev_self_test    = 0x14,  # Device Self-test
    nvme_admin_ns_attach        = 0x15,  # Namespace Attachment
    nvme_admin_keep_alive       = 0x18,  # Keep Alive
    nvme_admin_directive_send   = 0x19,  # Directive Send
    nvme_admin_directive_recv   = 0x1a,  # Directive Receive
    nvme_admin_virtual_mgmt     = 0x1c,  # Virtualization Management
    nvme_admin_nvme_mi_send     = 0x1d,  # NVMe Management Interface Send
    nvme_admin_nvme_mi_recv     = 0x1e,  # NVMe Management Interface Receive
    nvme_admin_dbbuf            = 0x7C,  # Doorbell Buffer Config
    nvme_admin_format_nvm       = 0x80,  # Format NVM
    nvme_admin_security_send    = 0x81,  # Security Send
    nvme_admin_security_recv    = 0x82,  # Security Receive
    nvme_admin_sanitize_nvm     = 0x84,  # Sanitize NVM
    nvme_admin_get_lba_status   = 0x86,  # Get LBA Status



class NVME_ADMIN_FEATURES_CODING(Enum):
    """
    NVMe Admin Command Feature Codes.

    This enumeration defines the feature codes used in NVMe admin commands for configuring and retrieving
    various settings and logs from the NVMe controller.
    """

    NVME_QUEUE_PHYS_CONTIG = (1 << 0)
    """
    Queue Physical Contiguity.
    Indicates whether the queue is physically contiguous in memory.
    """

    NVME_CQ_IRQ_ENABLED = (1 << 1)
    """
    Completion Queue Interrupt Enabled.
    Indicates whether interrupts are enabled for the completion queue.
    """

    NVME_SQ_PRIO_URGENT = (0 << 1)
    """
    Submission Queue Priority - Urgent.
    Sets the submission queue priority to urgent.
    """

    NVME_SQ_PRIO_HIGH = (1 << 1)
    """
    Submission Queue Priority - High.
    Sets the submission queue priority to high.
    """

    NVME_SQ_PRIO_MEDIUM = (2 << 1)
    """
    Submission Queue Priority - Medium.
    Sets the submission queue priority to medium.
    """

    NVME_SQ_PRIO_LOW = (3 << 1)
    """
    Submission Queue Priority - Low.
    Sets the submission queue priority to low.
    """

    NVME_FEAT_ARBITRATION = 0x01
    """
    Arbitration Feature.
    Feature code for configuring the arbitration settings of the NVMe controller.
    """

    NVME_FEAT_POWER_MGMT = 0x02
    """
    Power Management Feature.
    Feature code for configuring the power management settings of the NVMe controller.
    """

    NVME_FEAT_LBA_RANGE = 0x03
    """
    LBA Range Feature.
    Feature code for configuring the LBA range settings of the NVMe controller.
    """

    NVME_FEAT_TEMP_THRESH = 0x04
    """
    Temperature Threshold Feature.
    Feature code for configuring the temperature threshold settings of the NVMe controller.
    """

    NVME_FEAT_ERR_RECOVERY = 0x05
    """
    Error Recovery Feature.
    Feature code for configuring the error recovery settings of the NVMe controller.
    """

    NVME_FEAT_VOLATILE_WC = 0x06
    """
    Volatile Write Cache Feature.
    Feature code for configuring the volatile write cache settings of the NVMe controller.
    """

    NVME_FEAT_NUM_QUEUES = 0x07
    """
    Number of Queues Feature.
    Feature code for configuring the number of queues supported by the NVMe controller.
    """

    NVME_FEAT_IRQ_COALESCE = 0x08
    """
    IRQ Coalescing Feature.
    Feature code for configuring the IRQ coalescing settings of the NVMe controller.
    """

    NVME_FEAT_IRQ_CONFIG = 0x09
    """
    IRQ Configuration Feature.
    Feature code for configuring the IRQ settings of the NVMe controller.
    """

    NVME_FEAT_WRITE_ATOMIC = 0x0a
    """
    Write Atomicity Feature.
    Feature code for configuring the write atomicity settings of the NVMe controller.
    """

    NVME_FEAT_ASYNC_EVENT = 0x0b
    """
    Asynchronous Event Configuration Feature.
    Feature code for configuring the asynchronous event settings of the NVMe controller.
    """

    NVME_FEAT_AUTO_PST = 0x0c
    """
    Autonomous Power State Transition Feature.
    Feature code for configuring the autonomous power state transition settings of the NVMe controller.
    """

    NVME_FEAT_HOST_MEM_BUF = 0x0d
    """
    Host Memory Buffer Feature.
    Feature code for configuring the host memory buffer settings of the NVMe controller.
    """

    NVME_FEAT_TIMESTAMP = 0x0e
    """
    Timestamp Feature.
    Feature code for configuring the timestamp settings of the NVMe controller.
    """

    NVME_FEAT_KATO = 0x0f
    """
    Keep Alive Timeout Feature.
    Feature code for configuring the keep alive timeout settings of the NVMe controller.
    """

    NVME_FEAT_HCTM = 0x10
    """
    Host Controlled Thermal Management Feature.
    Feature code for configuring the host controlled thermal management settings of the NVMe controller.
    """

    NVME_FEAT_NOPSC = 0x11
    """
    NVM Subsystem Power State Change Feature.
    Feature code for configuring the NVM subsystem power state change settings of the NVMe controller.
    """

    NVME_FEAT_RRL = 0x12
    """
    Read Recovery Level Feature.
    Feature code for configuring the read recovery level settings of the NVMe controller.
    """

    NVME_FEAT_PLM_CONFIG = 0x13
    """
    Predictable Latency Mode Configuration Feature.
    Feature code for configuring the predictable latency mode settings of the NVMe controller.
    """

    NVME_FEAT_PLM_WINDOW = 0x14
    """
    Predictable Latency Mode Window Feature.
    Feature code for configuring the predictable latency mode window settings of the NVMe controller.
    """

    NVME_FEAT_HOST_BEHAVIOR = 0x16
    """
    Host Behavior Feature.
    Feature code for configuring the host behavior settings of the NVMe controller.
    """

    NVME_FEAT_SANITIZE = 0x17
    """
    Sanitize Feature.
    Feature code for configuring the sanitize settings of the NVMe controller.
    """

    NVME_FEAT_SW_PROGRESS = 0x80
    """
    Software Progress Feature.
    Feature code for retrieving the software progress status of the NVMe controller.
    """

    NVME_FEAT_HOST_ID = 0x81
    """
    Host ID Feature.
    Feature code for configuring the host ID settings of the NVMe controller.
    """

    NVME_FEAT_RESV_MASK = 0x82
    """
    Reservation Mask Feature.
    Feature code for configuring the reservation mask settings of the NVMe controller.
    """

    NVME_FEAT_RESV_PERSIST = 0x83
    """
    Reservation Persistence Feature.
    Feature code for configuring the reservation persistence settings of the NVMe controller.
    """

    NVME_FEAT_WRITE_PROTECT = 0x84
    """
    Write Protect Feature.
    Feature code for configuring the write protect settings of the NVMe controller.
    """

    NVME_LOG_ERROR = 0x01
    """
    Error Log.
    Log page code for retrieving the error log from the NVMe controller.
    """

    NVME_LOG_SMART = 0x02
    """
    SMART Log.
    Log page code for retrieving the SMART log from the NVMe controller.
    """

    NVME_LOG_FW_SLOT = 0x03
    """
    Firmware Slot Log.
    Log page code for retrieving the firmware slot log from the NVMe controller.
    """

    NVME_LOG_CHANGED_NS = 0x04
    """
    Changed Namespace Log.
    Log page code for retrieving the changed namespace log from the NVMe controller.
    """

    NVME_LOG_CMD_EFFECTS = 0x05
    """
    Command Effects Log.
    Log page code for retrieving the command effects log from the NVMe controller.
    """

    NVME_LOG_DEVICE_SELF_TEST = 0x06
    """
    Device Self-Test Log.
    Log page code for retrieving the device self-test log from the NVMe controller.
    """

    NVME_LOG_TELEMETRY_HOST = 0x07
    """
    Telemetry Host Log.
    Log page code for retrieving the telemetry host log from the NVMe controller.
    """

    NVME_LOG_TELEMETRY_CTRL = 0x08
    """
    Telemetry Controller Log.
    Log page code for retrieving the telemetry controller log from the NVMe controller.
    """

    NVME_LOG_ENDURANCE_GROUP = 0x09
    """
    Endurance Group Log.
    Log page code for retrieving the endurance group log from the NVMe controller.
    """

    NVME_LOG_ANA = 0x0c
    """
    Asymmetric Namespace Access Log.
    Log page code for retrieving the asymmetric namespace access log from the NVMe controller.
    """

    NVME_LOG_DISC = 0x70
    """
    Discovery Log.
    Log page code for retrieving the discovery log from the NVMe controller.
    """

    NVME_LOG_RESERVATION = 0x80
    """
    Reservation Log.
    Log page code for retrieving the reservation log from the NVMe controller.
    """

    NVME_LOG_SANITIZE = 0x81
    """
    Sanitize Log.
    Log page code for retrieving the sanitize log from the NVMe controller.
    """

    NVME_FWACT_REPL = (0 << 3)
    """
    Firmware Activate - Replace.
    Firmware activation type for replacing the firmware.
    """

    NVME_FWACT_REPL_ACTV = (1 << 3)
    """
    Firmware Activate - Replace and Activate.
    Firmware activation type for replacing and activating the firmware.
    """

    NVME_FWACT_ACTV = (2 << 3)
    """
    Firmware Activate - Activate.
    Firmware activation type for activating the firmware.
    """


class NVME_LOG_CONSTANT(Enum):
    """
    Defines constants for NVMe log page specific parameters (LSP) and log page offsets (LPO).

    These constants are used to specify different log pages and their parameters in NVMe commands.
    """

    NVME_NO_LOG_LSP       = 0x0
    """
    Indicates that no log page specific parameter is specified.
    """

    NVME_NO_LOG_LPO       = 0x0
    """
    Indicates that no log page offset is specified.
    """

    NVME_LOG_ANA_LSP_RGO  = 0x1
    """
    Specifies the log page specific parameter for ANA (Asymmetric Namespace Access) log page,
    requesting the RGO (Range Grained Optimize) information.
    """

    NVME_TELEM_LSP_CREATE = 0x1
    """
    Specifies the log page specific parameter for telemetry log page,
    indicating the creation of a telemetry log.
    """


class NVME_SANITIZE_INFO(Enum):
    """
    Defines constants related to NVMe sanitize operations and log status.

    These constants are used to specify different actions and statuses during the sanitize process of an NVMe device.
    Each constant represents a specific behavior or state in the sanitize operation.
    """

    NVME_SANITIZE_NO_DEALLOC = 0x00000200 # Indicates that no deallocation should occur during the sanitize operation.
    NVME_SANITIZE_OIPBP = 0x00000100 # Indicates that the sanitize operation should overwrite the in-progress bit pattern.
    NVME_SANITIZE_OWPASS_SHIFT = 0x00000004 # Defines the shift value for the overwrite pass count in the sanitize operation.
    NVME_SANITIZE_AUSE = 0x00000008 # Indicates that the sanitize operation should use the Automatic Unit Sanitize (AUS) feature.
    NVME_SANITIZE_ACT_CRYPTO_ERASE = 0x00000004 # Specifies that the sanitize action should be a cryptographic erase.
    NVME_SANITIZE_ACT_OVERWRITE = 0x00000003 # Specifies that the sanitize action should be an overwrite.
    NVME_SANITIZE_ACT_BLOCK_ERASE = 0x00000002 # Specifies that the sanitize action should be a block erase.
    NVME_SANITIZE_ACT_EXIT = 0x00000001 # Specifies that the sanitize action should exit the current operation.
    NVME_SANITIZE_LOG_DATA_LEN = 0x0014 # Defines the length of the sanitize log data in bytes.
    NVME_SANITIZE_LOG_GLOBAL_DATA_ERASED = 0x0100 # Indicates that the global data has been erased during the sanitize operation.
    NVME_SANITIZE_LOG_NUM_CMPLTED_PASS_MASK = 0x00F8 # Mask to extract the number of completed passes from the sanitize log.
    NVME_SANITIZE_LOG_STATUS_MASK = 0x0007 # Mask to extract the status from the sanitize log.
    NVME_SANITIZE_LOG_NEVER_SANITIZED = 0x0000 # Indicates that the device has never been sanitized.
    NVME_SANITIZE_LOG_COMPLETED_SUCCESS = 0x0001 # Indicates that the sanitize operation completed successfully.
    NVME_SANITIZE_LOG_IN_PROGESS = 0x0002 # Indicates that the sanitize operation is currently in progress.
    NVME_SANITIZE_LOG_COMPLETED_FAILED = 0x0003 # Indicates that the sanitize operation completed with a failure.
    NVME_SANITIZE_LOG_ND_COMPLETED_SUCCESS = 0x0004 # Indicates that the sanitize operation completed successfully without deallocation.

class nvme_sanitize_log_page(StructureBase):
    """
    NVMe Sanitize Log Page Structure.

    This structure represents the NVMe sanitize log page, which provides information about the progress and status
    of the sanitize operation, including estimated times for different types of erase operations.
    """
    _fields_ = [
        ('progress', c_uint16),  # Progress of the sanitize operation, expressed as a percentage.
        ('status', c_uint16),  # Current status of the sanitize operation.
        ('cdw10_info', c_uint32),  # Information contained in Command Dword 10, providing additional details about the sanitize operation.
        ('est_ovrwrt_time', c_uint32),  # Estimated time for the overwrite sanitize operation, in seconds.
        ('est_blk_erase_time', c_uint32),  # Estimated time for the block erase sanitize operation, in seconds.
        ('est_crypto_erase_time', c_uint32),  # Estimated time for the cryptographic erase sanitize operation, in seconds.
        ('est_ovrwrt_time_with_no_deallocate', c_uint32),  # Estimated time for the overwrite sanitize operation without deallocation, in seconds.
        ('est_blk_erase_time_with_no_deallocate', c_uint32),  # Estimated time for the block erase sanitize operation without deallocation, in seconds.
        ('est_crypto_erase_time_with_no_deallocate', c_uint32),  # Estimated time for the cryptographic erase sanitize operation without deallocation, in seconds.
    ]


class NVMF_FABRICS_OPCODE(Enum):
    """
    NVMe over Fabrics Command Opcode Enumeration.

    This enumeration defines the opcode for NVMe over Fabrics commands, which are used in the NVMe over Fabrics protocol
    to specify the type of operation to be performed. The `nvme_fabrics_command` opcode is specifically used for
    NVMe over Fabrics commands.
    """
    nvme_fabrics_command     = 0x7f  # Opcode for NVMe over Fabrics commands, with a value of 0x7f.


class NVMF_CAPSULE_COMMAND(Enum):
    """
    Enumeration class for NVMe over Fabrics (NVMe-oF) capsule command types.

    This class defines the types of commands that can be encapsulated in an NVMe-oF capsule.
    Each command type is represented by a unique hexadecimal value.
    """
    nvme_fabrics_type_property_set	= 0x00 # Command to set properties in the NVMe-oF subsystem.
    nvme_fabrics_type_connect	= 0x01  # Command to establish a connection in the NVMe-oF subsystem.
    nvme_fabrics_type_property_get	= 0x04 # Command to retrieve properties from the NVMe-oF subsystem.


class nvmf_rdma(StructureBase):
    """
    RDMA (Remote Direct Memory Access) Structure.

    This class represents the RDMA configuration structure, which is used to define the parameters
    for RDMA communication. It includes fields for queue pair type, protection domain type,
    communication management service type, reserved fields, and a partition key.
    """
    _fields_ = [
        ('qptype', c_uint8),  # Queue Pair Type
        ('prtype', c_uint8),  # Protection Domain Type
        ('cms', c_uint8),     # Communication Management Service Type
        ('resv1', c_uint8 * 5),  # Reserved field
        ('pkey', c_uint16),   # Partition Key
        ('resv10', c_uint8 * 246),  # Reserved field
    ]

class nvmf_tcp(StructureBase):
    """
    Represents the TCP (Transmission Control Protocol) configuration structure.
    This class defines the structure for TCP-related configurations, specifically focusing on the security type used in TCP communications.
    """
    _fields_ = [
        ('sectype', c_uint8), #  This field determines the type of security protocol or mechanism applied to the TCP connection.
    ]

class nvmf_tsas(Union):
    """
    The `tsas` class is a Union that represents a Transport Specific Address Structure (TSAS).
    It allows the storage of different transport-specific address formats in the same memory location.
    The Union can store one of the following:
    """
    _fields_ = [
        ('common', c_char * 256),  # Common character array for generic transport.
        ('rdma', nvmf_rdma),            # RDMA transport-specific structure.
        ('tcp', nvmf_tcp),              # TCP transport-specific structure.
    ]


class nvmf_disc_log_entry(StructureBase):
    """
    This class represents an entry in the NVMe over Fabrics (NVMe-oF) Discovery Response Page.
    It inherits from StructureBase and defines the structure of a single entry in the discovery response page,
    which contains information about a discovered NVMe-oF subsystem.
    """
    _fields_ = [
        ('trtype', c_uint8), # Transport type, indicating the type of transport protocol used (e.g., RDMA, TCP),
        ('adrfam', c_uint8), # Address family, indicating the type of address used (e.g., IPv4, IPv6)
        ('subtype', c_uint8), # Subsystem type, indicating the type of NVMe-oF subsystem (e.g., Discovery, NVMe),
        ('treq', c_uint8), # Transport requirements, specifying any special requirements for the transport
        ('portid', c_uint16), # Port ID, identifying the port used for communication
        ('cntlid', c_uint16), # Controller ID, identifying the controller associated with this entry
        ('asqsz', c_uint16), # Admin Submission Queue Size, specifying the size of the admin submission queue
        ('resv8', c_uint8 * 22), # Reserved field, 22 bytes
        ('trsvcid', c_char * 32), #Transport service ID, identifying the service associated with the transport
        ('resv64', c_uint8 * 192), #Reserved field, 192 bytes
        ('subnqn', c_char * 256), # Subsystem NQN (NVMe Qualified Name), uniquely identifying the NVMe-oF subsystem
        ('traddr', c_char * 256), # Transport address, specifying the address used for communication
        ('tsas', nvmf_tsas), # Transport Specific Address Subtype, a union that contains transport-specific address information
    ]

class nvmf_discovery_log(StructureBase):
    """
    This class represents the header of the NVMe over Fabrics (NVMe-oF) Discovery Response Page.
    It contains metadata about the discovery response, including the generation counter, number of records,
    record format, and a pointer to the list of discovery response entries.
    """
    _fields_ = [
        ('genctr', c_uint64), # Generation counter, used to track changes in the discovery response page.
        ('numrec', c_uint64), # Number of records in the discovery response page.
        ('recfmt', c_uint16), # Record format, specifying the format of the records in the response.
        ('resv14', c_uint8 * 1006), # Reserved field for future use or alignment.
        ('entries', Pointer(nvmf_disc_log_entry, "numrec")), # Pointer to an array of discovery response entries.
    ]


class nvmf_connect_data(StructureBase):
    """
    The `nvmf_connect_data` class represents the structure of NVMe over Fabrics (NVMe-oF) connection data.
    It inherits from `StructureBase` and defines the layout of fields for NVMe-oF connection data.
    """
    _fields_ = [
        ('hostid', c_uint8 * 16), # the unique identifier of the host.
        ('cntlid', c_uint16), # the controller identifier.
        ('resv4', c_uint8 * 238), # reserved for future expansion or alignment.
        ('subsysnqn', c_char * 256), # the subsystem's NQN (NVMe Qualified Name).
        ('hostnqn', c_char * 256), # the host's NQN (NVMe Qualified Name).
        ('resv5', c_uint8 * 256), # reserved for future expansion or alignment.
    ]


class nvme_streams_directive_params(StructureBase):
    """
    Represents the parameters for the Streams Directive in NVMe.

    This structure defines the fields used to configure and manage stream-related operations in NVMe devices.
    Each field corresponds to a specific aspect of stream management, such as stream length, allocation, and offsets.

    Fields:
    - msl: Maximum Stream Length. Specifies the maximum length of a stream in logical blocks.
    - nssa: Number of Streams Allocated. Indicates the number of streams currently allocated.
    - nsso: Number of Streams Supported. Specifies the total number of streams supported by the device.
    - rsvd1: Reserved field for future use. Consists of 10 bytes.
    - sws: Stream Write Size. Defines the size of writes for a stream in logical blocks.
    - sgs: Stream Granularity Size. Specifies the granularity of stream operations in logical blocks.
    - nsa: Number of Streams Active. Indicates the number of streams currently active.
    - nso: Number of Streams Open. Specifies the number of streams that are open for operations.
    - rsvd2: Reserved field for future use. Consists of 6 bytes.
    """
    _fields_ = [
        ('msl', c_uint16), # Maximum Stream Length. Specifies the maximum length of a stream in logical blocks.
        ('nssa', c_uint16), # Number of Streams Allocated. Indicates the number of streams currently allocated.
        ('nsso', c_uint16), # Number of Streams Supported. Specifies the total number of streams supported by the device.
        ('rsvd1', c_uint8 * 10), # Reserved field for future use. Consists of 10 bytes.
        ('sws', c_uint32), # Stream Write Size. Defines the size of writes for a stream in logical blocks.
        ('sgs', c_uint16), # Stream Granularity Size. Specifies the granularity of stream operations in logical blocks.
        ('nsa', c_uint16), # Number of Streams Active. Indicates the number of streams currently active.
        ('nso', c_uint16), # Number of Streams Open. Specifies the number of streams that are open for operations.
        ('rsvd2', c_uint8 * 6), # Reserved field for future use. Consists of 6 bytes.
    ]

class nvme_cmd_effects_log(StructureBase):
    """
    NVMe Effects Log Page Structure.

    This class represents the NVMe Effects Log Page, which contains information about the effects of various
    commands on the NVMe device, including administrative command sets (ACS) and I/O command sets (IOCs).
    The log page is used to track and analyze the impact of commands on the device's performance and behavior.

    Attributes:
        acs (c_uint32 * 256): An array of 256 unsigned 32-bit integers representing the effects of administrative commands.
                              Each entry corresponds to a specific administrative command and its impact on the device.
        iocs (c_uint32 * 256): An array of 256 unsigned 32-bit integers representing the effects of I/O commands.
                               Each entry corresponds to a specific I/O command and its impact on the device.
        resv (c_uint8 * 2048): A reserved field of 2048 bytes for future use or alignment purposes.
    """
    _fields_ = [
        ('acs', c_uint32 * 256),  # Administrative Command Set effects
        ('iocs', c_uint32 * 256),  # I/O Command Set effects
        ('resv', c_uint8 * 2048),  # Reserved field
    ]


class nvme_error_log_page(StructureBase):
    """
    NVMe Error Log Page Structure.

    This structure represents the error log page for NVMe devices, which contains detailed information about errors that have occurred.
    Each field in the structure provides specific details about the error, such as the error count, command details, and location information.
    """
    _fields_ = [
        ('error_count', c_uint64), # The total number of errors that have occurred
        ('sqid', c_uint16), # The Submission Queue ID where the error occurred
        ('cmdid', c_uint16), # The Command ID of the command that caused the error
        ('status_field', c_uint16), # The status field of the error
        ('parm_error_location', c_uint16), # The parameter error location
        ('lba', c_uint64), # The Logical Block Address (LBA) where the error occurred
        ('nsid', c_uint32), # The Namespace ID associated with the error
        ('vs', c_uint8), # Vendor-specific information
        ('trtype', c_uint8), # The transport type
        ('resv', c_uint8 * 2), # Reserved field for future use
        ('cs', c_uint64), # Command-specific information
        ('trtype_spec_info', c_uint16), # Transport type-specific information
        ('resv2', c_uint8 * 22),  # Reserved field for future use
    ]


class nvme_firmware_slot(StructureBase):
    """
    NVMe Firmware Log Page Structure.

    This class represents the NVMe firmware log page, which provides information about the firmware slots
    and their revision numbers. It is used to retrieve firmware-related details from an NVMe device.
    """
    _fields_ = [
        ('afi', c_uint8),  # Active Firmware Info, indicates the currently active firmware slot.
        ('resv', c_uint8 * 7),  # Reserved field, used for future expansion or alignment.
        ('frs', c_uint64 * 7),  # Firmware Revision Slots, contains the firmware revision numbers for each of the 7 firmware slots.
        ('resv2', c_uint8 * 448),  # Reserved field, used for future expansion or alignment.
    ]


class nvme_host_mem_buf_attrs(StructureBase):
    """
    NVMe Host Memory Buffer Structure.

    This class represents the structure of an NVMe host memory buffer, which is used to describe
    the memory buffer allocated by the host for NVMe operations. It includes fields for the size
    of the buffer, memory descriptor addresses, and a reserved field for future use.
    """
    _fields_ = [
        ('hsize', c_uint32), # Size of the host memory buffer in bytes
        ('hmdlal', c_uint32), # Lower 32 bits of the memory descriptor address
        ('hmdlau', c_uint32), # Upper 32 bits of the memory descriptor address
        ('hmdlec', c_uint32), # Error check code for the memory descriptor
        ('rsvd1', c_uint8 * 4080), # Reserved field for future use or alignment
    ]


class nvme_auto_pst(StructureBase):
    """
    nvme_auto_pst class represents the NVMe Autonomous Power State Transition (PST) structure.

    This class is used to define the structure for NVMe autonomous power state transitions, which allows the NVMe device
    to automatically transition between different power states based on predefined criteria. It inherits from StructureBase.
    """
    _fields_ = [
        ('data', c_uint32),  # Power state transition data.
        ('rsvd1', c_uint32),  # Reserved field for future use or alignment.
    ]


class nvme_timestamp(StructureBase):
    """
    NVMe Timestamp Structure.

    This class represents the NVMe timestamp structure, which is used to store timestamp information
    related to NVMe operations. It includes fields for the timestamp value, attributes, and a reserved field.
    """
    _fields_ = [
        ('timestamp', c_uint8 * 6),  # 6-byte array for the timestamp value
        ('attr', c_uint8),           # 8-bit unsigned integer for timestamp attributes
        ('rsvd', c_uint8),           # 8-bit unsigned integer reserved for future use
    ]

class nvme_bar_cap(StructureBase):
    """
    nvme_bar_cap Class.

    This class represents the NVMe Controller Capability Register (CAP) structure.
    It defines the fields that describe the capabilities of an NVMe controller, including
    maximum queue entries, arbitration mechanisms, timeout settings, and other controller-specific features.
    """
    _fields_ = [
        ('mqes', c_uint16), # Maximum Queue Entries Supported. Specifies the maximum number of queue entries supported by the controller, minus one.
        ('ams_cqr', c_uint8), # Arbitration Mechanism Supported and Controller Reset Support. The lower 4 bits indicate supported arbitration mechanisms, and the upper 4 bits indicate controller reset support.
        ('to', c_uint8), # Timeout. Specifies the timeout value for controller reset or initialization.
        ('bps_css_nssrs_dstrd', c_uint16), # Boot Partition Support, Controller State Support, Namespace Support, and Doorbell Stride. The lower 4 bits indicate the Doorbell stride, and the remaining bits indicate other support features.
        ('mpsmax_mpsmin', c_uint8), # Maximum and Minimum Memory Page Size. Specifies the maximum and minimum memory page sizes supported by the controller.
        ('rsvd_cmbs_pmrs', c_uint8), # Reserved, Controller Memory Buffer Support, and Persistent Memory Region Support. The lower 2 bits indicate persistent memory region support, and the remaining bits indicate controller memory buffer support.
    ]

class NVME_STATUS_FIELD(Enum):
    """
    NVME_SCT (Status Code Type) Enumeration.

    This enumeration defines the different types of status codes that can be returned by NVMe commands.
    Each type represents a specific category of status information, helping to classify the nature of the response.
    """
    NVME_SCT_GENERIC		            = 0x0 # Generic status code type, indicating a general status or error.
    NVME_SCT_CMD_SPECIFIC		        = 0x1 # Command-specific status code type, indicating a status or error specific to the executed command.
    NVME_SCT_MEDIA			            = 0x2 # Media-related status code type, indicating a status or error related to the storage media.

    """
    The `NVME_SC_GENERIC` enumeration class represents generic status codes for the NVMe (Non-Volatile Memory Express) protocol.
    Each enumeration value corresponds to a specific status code that describes the result or error condition of an NVMe command execution.
    """
    NVME_SC_SUCCESS                     = 0x0 # Successful completion of the command.
    NVME_SC_INVALID_OPCODE              = 0x1 # Invalid opcode.
    NVME_SC_INVALID_FIELD               = 0x2 # Invalid field in the command.
    NVME_SC_CMDID_CONFLICT              = 0x3 # Command ID conflict.
    NVME_SC_DATA_XFER_ERROR             = 0x4 # Data transfer error.
    NVME_SC_POWER_LOSS                  = 0x5 # Power loss.
    NVME_SC_INTERNAL                    = 0x6 # Internal error.
    NVME_SC_ABORT_REQ                   = 0x7 # Command aborted by request.
    NVME_SC_ABORT_QUEUE                 = 0x8 # Queue aborted.
    NVME_SC_FUSED_FAIL                  = 0x9 # Fused command failed.
    NVME_SC_FUSED_MISSING               = 0xa # Missing fused command.
    NVME_SC_INVALID_NS                  = 0xb # Invalid namespace.
    NVME_SC_CMD_SEQ_ERROR               = 0xc # Command sequence error.
    NVME_SC_SGL_INVALID_LAST            = 0xd # Invalid last descriptor in the SGL（Scatter Gather List）.
    NVME_SC_SGL_INVALID_COUNT           = 0xe # Invalid SGL count.
    NVME_SC_SGL_INVALID_DATA            = 0xf # Invalid SGL data.
    NVME_SC_SGL_INVALID_METADATA        = 0x10 # Invalid SGL metadata.
    NVME_SC_SGL_INVALID_TYPE            = 0x11 # Invalid SGL type.
    NVME_SC_CMB_INVALID_USE             = 0x12 # Invalid use of Controller Memory Buffer (CMB).
    NVME_SC_PRP_INVALID_OFFSET          = 0x13 # Invalid Physical Region Page (PRP) offset.
    NVME_SC_ATOMIC_WRITE_UNIT_EXCEEDED  = 0x14 # Atomic write unit exceeded.
    NVME_SC_OPERATION_DENIED            = 0x15 # Operation denied.
    NVME_SC_SGL_INVALID_OFFSET          = 0x16 # Invalid SGL offset.
    NVME_SC_INCONSISTENT_HOST_ID        = 0x18 # Inconsistent host ID.
    NVME_SC_KEEP_ALIVE_EXPIRED          = 0x19 # Keep-alive expired.
    NVME_SC_KEEP_ALIVE_INVALID          = 0x1A # Invalid keep-alive request.
    NVME_SC_PREEMPT_ABORT               = 0x1B # Preemption aborted.
    NVME_SC_SANITIZE_FAILED             = 0x1C # Sanitize operation failed.
    NVME_SC_SANITIZE_IN_PROGRESS        = 0x1D # Sanitize operation in progress.
    NVME_SC_NS_WRITE_PROTECTED          = 0x20 # Namespace write-protected.
    NVME_SC_CMD_INTERRUPTED             = 0x21 # Command interrupted.
    NVME_SC_TRANSIENT_TRANSPORT         = 0x22 # Transient transport error.
    NVME_SC_LBA_RANGE                   = 0x80 # Logical block address out of range.
    NVME_SC_CAP_EXCEEDED                = 0x81 # Capacity exceeded.
    NVME_SC_NS_NOT_READY                = 0x82 # Namespace not ready.
    NVME_SC_RESERVATION_CONFLICT        = 0x83 # Reservation conflict.
    NVME_SC_FORMAT_IN_PROGRESS          = 0x84 # Format operation in progress.

    # General Error Status Codes
    NVME_SC_CQ_INVALID		            = 0x100  # Completion Queue Invalid
    NVME_SC_QID_INVALID		            = 0x101  # Queue ID Invalid
    NVME_SC_QUEUE_SIZE		            = 0x102  # Queue Size Invalid
    NVME_SC_ABORT_LIMIT		            = 0x103  # Abort Request Limit Exceeded
    NVME_SC_ABORT_MISSING		        = 0x104  # Abort Request Missing
    NVME_SC_ASYNC_LIMIT		            = 0x105  # Asynchronous Event Request Limit Exceeded
    NVME_SC_FIRMWARE_SLOT		        = 0x106  # Firmware Slot Invalid
    NVME_SC_FIRMWARE_IMAGE		        = 0x107  # Firmware Image Invalid
    NVME_SC_INVALID_VECTOR		        = 0x108  # Interrupt Vector Invalid
    NVME_SC_INVALID_LOG_PAGE	        = 0x109  # Log Page Invalid
    NVME_SC_INVALID_FORMAT		        = 0x10a  # Format Invalid
    NVME_SC_FW_NEEDS_CONV_RESET	        = 0x10b  # Firmware Requires Conventional Reset
    NVME_SC_INVALID_QUEUE		        = 0x10c  # Queue Invalid
    NVME_SC_FEATURE_NOT_SAVEABLE	    = 0x10d  # Feature Not Saveable
    NVME_SC_FEATURE_NOT_CHANGEABLE	    = 0x10e  # Feature Not Changeable
    NVME_SC_FEATURE_NOT_PER_NS	        = 0x10f  # Feature Not Applicable to Namespace
    NVME_SC_FW_NEEDS_SUBSYS_RESET	    = 0x110  # Firmware Requires Subsystem Reset
    NVME_SC_FW_NEEDS_RESET		        = 0x111  # Firmware Requires Reset
    NVME_SC_FW_NEEDS_MAX_TIME	        = 0x112  # Firmware Requires Maximum Time
    NVME_SC_FW_ACTIVATE_PROHIBITED	    = 0x113  # Firmware Activation Prohibited
    NVME_SC_OVERLAPPING_RANGE	        = 0x114  # Overlapping Range
    NVME_SC_NS_INSUFFICIENT_CAP	        = 0x115  # Namespace Capacity Insufficient
    NVME_SC_NS_ID_UNAVAILABLE	        = 0x116  # Namespace ID Unavailable
    NVME_SC_NS_ALREADY_ATTACHED	        = 0x118  # Namespace Already Attached
    NVME_SC_NS_IS_PRIVATE		        = 0x119  # Namespace is Private
    NVME_SC_NS_NOT_ATTACHED		        = 0x11a  # Namespace Not Attached
    NVME_SC_THIN_PROV_NOT_SUPP	        = 0x11b  # Thin Provisioning Not Supported
    NVME_SC_CTRL_LIST_INVALID	        = 0x11c  # Controller List Invalid
    NVME_SC_DEVICE_SELF_TEST_IN_PROGRESS= 0x11d  # Device Self-Test in Progress
    NVME_SC_BP_WRITE_PROHIBITED	        = 0x11e  # Write Operation Prohibited
    NVME_SC_INVALID_CTRL_ID		        = 0x11f  # Controller ID Invalid
    NVME_SC_INVALID_SECONDARY_CTRL_STATE= 0x120  # Secondary Controller State Invalid
    NVME_SC_INVALID_NUM_CTRL_RESOURCE	= 0x121  # Controller Resource Count Invalid
    NVME_SC_INVALID_RESOURCE_ID	        = 0x122  # Resource ID Invalid
    NVME_SC_PMR_SAN_PROHIBITED	        = 0x123  # PMR SAN Prohibited
    NVME_SC_ANA_INVALID_GROUP_ID        = 0x124  # ANA Group ID Invalid
    NVME_SC_ANA_ATTACH_FAIL		        = 0x125  # ANA Attach Failed

    # I/O Command Set Specific Error Status Codes - NVM Commands
    NVME_SC_BAD_ATTRIBUTES		        = 0x180  # Bad Attributes
    NVME_SC_INVALID_PI		            = 0x181  # Invalid Protection Information
    NVME_SC_READ_ONLY		            = 0x182  # Read Only
    NVME_SC_ONCS_NOT_SUPPORTED	        = 0x183  # ONCS Not Supported


    # I/O Command Set Specific - Fabrics commands:
    NVME_SC_CONNECT_FORMAT		        = 0x180  # Indicates that the connection request format is invalid.
    NVME_SC_CONNECT_CTRL_BUSY	        = 0x181  # Indicates that the controller is busy and cannot process the connection request.
    NVME_SC_CONNECT_INVALID_PARAM	    = 0x182  # Indicates that the connection request contains invalid parameters.
    NVME_SC_CONNECT_RESTART_DISC	    = 0x183  # Indicates that the discovery process needs to be restarted.
    NVME_SC_CONNECT_INVALID_HOST	    = 0x184  # Indicates that the host identifier is invalid.

    # 发现相关状态码
    NVME_SC_DISCOVERY_RESTART	        = 0x190  # Indicates that the discovery process needs to be restarted.
    NVME_SC_AUTH_REQUIRED		        = 0x191  # Indicates that authentication is required for the connection.

    # 读写错误状态码
    NVME_SC_WRITE_FAULT		            = 0x280  # Indicates a write operation failure.
    NVME_SC_READ_ERROR		            = 0x281  # Indicates a read operation failure.
    NVME_SC_GUARD_CHECK		            = 0x282  # Indicates a data protection (guard check) failure.
    NVME_SC_APPTAG_CHECK		        = 0x283  # Indicates an application tag check failure.
    NVME_SC_REFTAG_CHECK		        = 0x284  # Indicates a reference tag check failure.
    NVME_SC_COMPARE_FAILED		        = 0x285  # Indicates a data comparison failure.
    NVME_SC_ACCESS_DENIED		        = 0x286  # Indicates that access to the resource is denied.
    NVME_SC_UNWRITTEN_BLOCK		        = 0x287  # Indicates an attempt to read an unwritten block.

    # ANA (Asymmetric Namespace Access) 相关状态码
    NVME_SC_ANA_PERSISTENT_LOSS	        = 0x301  # Indicates persistent loss of ANA access.
    NVME_SC_ANA_INACCESSIBLE	        = 0x302  # Indicates that the namespace is inaccessible.
    NVME_SC_ANA_TRANSITION		        = 0x303  # Indicates a transition in ANA state.

    # 其他状态码
    NVME_SC_CRD			                = 0x1800  # Indicates a command retry delay.
    NVME_SC_DNR			                = 0x4000  # Indicates that the command should not be retried.