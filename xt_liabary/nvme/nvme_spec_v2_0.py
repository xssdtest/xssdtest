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
                ("NSSS", c_uint64, 1),              # NVM Subsystem Shutdown Supported   	                NSSS	58	58	RO	Impl Spec
                ("CRMS", c_uint64, 2),              # Controller Ready Modes Supported   	                CRMS	59	60	RO	Impl Spec
                ("Reserved1", c_uint64, 3),         # Reserved	                                            RSV	    61	63	RO	0
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
                ("CRIME", c_uint32, 1),             # Controller Ready Independent of Media Enable	        CRIME	24	24	RW/RO	0
                ("Reserved1", c_uint32, 7),         # Reserved	                                            RSV	    25	31	RW/RO	0
                ]


class CSTS(StructureBase):
    _fields_ = [("RDY", c_uint32, 1),               # Ready 	                                            RDY	    0	0	RO	0
                ("CFS", c_uint32, 1),               # Controller Fatal Status 	                            CFS	    1	1	RO	HwInit
                ("SHST", c_uint32, 2),              # Shutdown Status 	                                    SHST	2	3	RO	0
                ("NSSRO", c_uint32, 1),             # NVM Subsystem Reset Occurred 	                        NSSRO	4	4	RWC	HwInit
                ("PP", c_uint32, 1),                # Processing Paused 	                                PP	    5	5	RO	0
                ("ST", c_uint32, 1),                # Shutdown Type	                                        ST	    6	6	RO	Impl Spec
                ("Reserved", c_uint32, 25),         # Reserved	                                            RSV	    7	31	RO	0
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
    _fields_ = [("CBAI", c_uint32, 1),              # Controller Base Address Invalid	                    CBAI	    0	0	RO	0
                ("Reserved", c_uint32, 31),         #Reserved                    	                        RSV	        1	31	RO	0
                ]

class CMBEBS(StructureBase):
    _fields_ = [("CMBSZU", c_uint32, 4),            # CMB Elasticity Buffer Size Units	                    CMBSZU	    0	3	RO	ImplSpec
                ("RBB", c_uint32, 1),               # Read Bypass Behavior 	                                EBS	        4	4	RO	ImplSpec
                ("Reserved", c_uint32, 3),          # Reserved          	                                RSV	        5	7	RO	ImplSpec
                ("CMBWBZ", c_uint32, 24),           # CMB Elasticity Buffer Size Base 	                    CMBWBZ	    8	31	RO	ImplSpec
                ]

class CMBSWTP(StructureBase):
    _fields_ = [("CMBSWTU", c_uint32, 4),           # CMB Sustained Write Throughput Units	                CMBSWTU	    0	3	RO	ImplSpec
                ("Reserved", c_uint32, 4),          # Reserved          	                                RSV	        4	7	RO	0
                ("CMBSWTV", c_uint32, 24),          # CMB Sustained Write Throughput 	                    CMBSWTV	    8	31	RO	ImplSpec
                ]

class NSSD(StructureBase):
    _fields_ = [("NSSC", c_uint32),                 # NVM Subsystem Shutdown Control	                    NSSC	    0	31	RW	0
                ]

class CRTO(StructureBase):
    _fields_ = [("CRWMT", c_uint16),                # Controller Ready With Media Timeout	                CRWMT	    0	15	RO	ImplSpec
                ("CRIMT", c_uint16),                # Controller Ready Independent of Media Timeout	        CRIMT	    16	31	RO	ImplSpec
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
                ("CMBEBS", CMBEBS),                 # Controller Memory Buffer Elasticity Buffer Size	                    CMBEBS	0x5C	 0x5F	4
                ("CMBSWTP", CMBSWTP),               # Controller Memory Buffer Sustained Write Throughput                   CMBSWTP	0x60	 0x63	4
                ("NSSD", NSSD),                     # NVM Subsystem Shutdown                                                NSSD	0x64	 0x67	4
                ("CRTO", CRTO),                     # Controller Ready Timeouts	                                            CRTO	0x68	 0x6B	4
                ("Reserved2", c_char * 3476),       # Reserved	                                                            RSV	    0x6C	 0xDFF	3476
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

class NVME_CONSTANTS(Enum):
    """
        A place to stash various constant nvme values
    """
    NVME_NSID_ALL = 0xffffffff                          # A broadcast value that is used to specify all namespaces
    NVME_NSID_NONE = 0                                  # The invalid namespace id, for when the nsid parameter is not used in a command
    NVME_UUID_NONE = 0                                  # Use to omit a uuid command parameter
    NVME_CNTLID_NONE = 0                                # Use to omit a cntlid command parameter
    NVME_CNSSPECID_NONE = 0                             # Use to omit a cns_specific_id command parameter
    NVME_LOG_LSP_NONE = 0                               # Use to omit a log lsp command parameter
    NVME_LOG_LSI_NONE = 0                               # Use to omit a log lsi command parameter
    NVME_LOG_LPO_NONE = 0                               # Use to omit a log lpo command parameter
    NVME_IDENTIFY_DATA_SIZE = 4096                      # The transfer size for nvme identify commands
    NVME_LOG_SUPPORTED_LOG_PAGES_MAX = 256              # The largest possible index in the supported log pages log
    NVME_ID_NVMSET_LIST_MAX = 31                        # The largest possible nvmset index in identify nvmeset
    NVME_ID_UUID_LIST_MAX = 127                         # The largest possible uuid index in identify uuid list
    NVME_ID_CTRL_LIST_MAX = 2047                        # The largest possible controller index in identify controller list
    NVME_ID_NS_LIST_MAX = 1024                          # The largest possible namespace index in identify namespace list
    NVME_ID_SECONDARY_CTRL_MAX = 127                    # The largest possible secondary controller index in identify secondary controller
    NVME_ID_DOMAIN_LIST_MAX = 31                        # The largest possible domain index in the in domain list
    NVME_ID_ENDURANCE_GROUP_LIST_MAX = 2047             # The largest possible endurance group index in the endurance group list
    NVME_ID_ND_DESCRIPTOR_MAX = 16                      # The largest possible namespace granularity index in the namespace granularity descriptor list
    NVME_FEAT_LBA_RANGE_MAX = 64                        # The largest possible LBA range index in feature lba range type
    NVME_LOG_ST_MAX_RESULTS = 20                        # The largest possible self test result index in the device self test log
    NVME_LOG_TELEM_BLOCK_SIZE = 512                     # Specification defined size of Telemetry Data Blocks
    NVME_LOG_FID_SUPPORTED_EFFECTS_MAX = 256            # The largest possible FID index in the feature	identifiers effects log.
    NVME_LOG_MI_CMD_SUPPORTED_EFFECTS_MAX = 256         # The largest possible MI Command index in the MI Command effects log.
    NVME_LOG_MI_CMD_SUPPORTED_EFFECTS_RESERVED = 768    # The reserved space in the MI Command effects log.
    NVME_DSM_MAX_RANGES = 256                           # The largest possible range index in a data-set management command
    NVME_NQN_LENGTH = 256                               # Max length for NVMe Qualified Name
    NVMF_TRADDR_SIZE = 256                              # Max Transport Address size
    NVMF_TSAS_SIZE = 256                                # Max Transport Specific Address Subtype size
    NVME_ZNS_CHANGED_ZONES_MAX = 511                    # Max number of zones in the changed zones log page


class NVME_CSI(Enum):
    """
        Defined command set indicators
    """
    NVME_CSI_NVM = 0                                    # NVM Command Set
    NVME_CSI_KV = 1                                     # Key Value Command Set
    NVME_CSI_ZNS = 2                                    # Zoned Namespace Command Set

class NVME_FLABS(Enum):
    """
    NVME_FLABS is an enumeration class that defines bit shift values and masks for the NVMe (Non-Volatile Memory Express)
    Format Logical Block Attributes (FLABS) register. This class is used to manage and interpret the fields within the
    FLABS register, which specifies the format and attributes of logical blocks in NVMe.

    The constants defined in this class include:
    - NVME_FLABS_LOWER_SHIFT: Bit shift for the lower format logical block attributes field.
    - NVME_FLABS_META_EXT_SHIFT: Bit shift for the metadata extension field.
    - NVME_FLABS_HIGHER_SHIFT: Bit shift for the higher format logical block attributes field.
    - NVME_FLABS_LOWER_MASK: Bit mask for the lower format logical block attributes field.
    - NVME_FLABS_META_EXT_MASK: Bit mask for the metadata extension field.
    - NVME_FLABS_HIGHER_MASK: Bit mask for the higher format logical block attributes field.

    These constants are used to extract or manipulate specific fields within the FLABS register, enabling precise
    control over the format and attributes of logical blocks in NVMe.
    """
    NVME_FLABS_LOWER_SHIFT		= 0
    NVME_FLABS_META_EXT_SHIFT	= 4
    NVME_FLABS_HIGHER_SHIFT		= 5
    NVME_FLABS_LOWER_MASK		= 0xf
    NVME_FLABS_META_EXT_MASK	= 0x1
    NVME_FLABS_HIGHER_MASK		= 0x3


class NVME_PSD_FLAGS(Enum):
    """
        Possible flag values in nvme power state descriptor
    """
    NVME_PSD_FLAGS_MXPS	= 1 << 0
    """
        Indicates the scale for the Maximum Power field. If this bit is cleared, then the scale of the
	    Maximum Power field is in 0.01 Watts. If this bit is set, then the scale of the Maximum Power field is in
		0.0001 Watts.
    """
    NVME_PSD_FLAGS_NOPS	= 1 << 1
    """
        Indicates whether the controller processes I/O commands in this power state. If this bit is cleared,
 		then the controller processes I/O commands in this power state. If this bit is set, then the controller
 		does not process I/O commands in this power state.
    """

class NVME_PSD_PS(Enum):
    """
        enum nvme_psd_ps - Known values for &struct nvme_psd %ips and %aps. Use with nvme_psd_power_scale() to extract the power scale field
        to match this enum.
    """
    NVME_PSD_PS_NOT_REPORTED	= 0     # Not reported
    NVME_PSD_PS_100_MICRO_WATT	= 1     # 0.0001 watt scale
    NVME_PSD_PS_10_MILLI_WATT	= 2     # 0.01 watt scale

class NVME_PSD_WORKLOAD(Enum):
    """
        Specifies a workload hint in the Power Management Feature (see &struct nvme_psd.apw) to inform the
 	    NVM subsystem or indicate the conditions for the active power level.
    """
    NVME_PSD_WORKLOAD_NP	= 0 # The workload is unknown or not provided.
    NVME_PSD_WORKLOAD_1	= 1
    """
        Extended Idle Period with a Burst of Random Write consists of five minutes of idle followed by
        thirty-two random write commands of size 1 MiB submitted to a single controller while all other
        controllers in the NVM subsystem are idle, and then thirty (30) seconds of idle.
    """
    NVME_PSD_WORKLOAD_2	= 2
    """
        Heavy Sequential Writes consists of 80,000 sequential write commands of size 128 KiB submitted to
        a single controller while all other controllers in the NVM subsystem are idle.  The submission queue(s)
        should be sufficiently large allowing the host to ensure there are multiple commands pending at all
        times during the workload.   
    """

class nvme_id_psd(StructureBase):
    _fields_ = [
        ('mp', c_uint16),   # Maximum Power indicates the sustained maximum power consumed by the the value in this field multiplied by the scale specified in the Max Power Scale bit (see &enum nvme_psd_flags). A value of 0 indicates Maximum Power is not reported.
        ('rsvd1', c_uint8), # Reserved
        ('flags', c_uint8), # Additional decoding flags, see &enum nvme_psd_flags.
        ('enlat', c_uint32),# Entry Latency indicates the maximum latency in microseconds associated with entering this power state. A value of 0 indicates Entry Latency is not reported.
        ('exlat', c_uint32),# Exit Latency indicates the maximum latency in microseconds associated with exiting this power state. A value of 0 indicates Exit Latency is not reported.
        ('rrt', c_uint8),   # Relative Read Throughput indicates the read throughput rank associated with this power state relative to others. The value in this is less than the number of supported power states.
        ('rrl', c_uint8),   # Relative Read Latency indicates the read latency rank associated with this power state relative to others. The value in this field is less than the number of supported power states.
        ('rwt', c_uint8),   # Relative Write Throughput indicates the write throughput rank associated with this power state relative to others. The value in this field is less than the number of supported power states.
        ('rwl', c_uint8),   # Relative Write Latency indicates the write latency rank associated with this power state relative to others. The value in this field is less than the number of supported power states.
        ('idlp', c_uint16), # Idle Power indicates the power consumed by the controller in this power state when the controller is idle. A value of 0 indicates Idle Power is not reported.
        ('ips', c_uint8),   # Idle Power Scale indicates the scale for &struct nvme_id_psd.idlp,  see &enum nvme_psd_ps for decoding this field.
        ('rsvd2', c_uint8), # Reserved
        ('actp', c_uint16), # Active Power indicates the largest average power consumed by the NVM subsystem over a 10 second period in this power state with the workload indicated in the Active Power Workload field.
        ('apws', c_uint8),  # Bits 7-6: Active Power Scale(APS) indicates the scale for the &struct nvme_id_psd.actp field, see &enum nvme_psd_ps for decoding this field. Bits 2-0: Active Power Workload(APW) indicates the workload used to calculate maximum power for this power state. See &enum nvme_psd_workload for decoding this field.
        ('rsvd3', c_uint8 * 9), # Reserved
    ]

class nvme_id_ctrl(StructureBase):
    """
        Identify Controller data structure
    """
    _fields_ = [
        ('vid', c_uint16),          # PCI Vendor ID, the company vendor identifier that is assigned by the PCI SIG.
        ('ssvid', c_uint16),        # PCI Subsystem Vendor ID, the company vendor identifier that is assigned by the PCI SIG for the subsystem.
        ('sn', c_char * 20),        # Serial Number, a globally unique identifier for the controller.
        ('mn', c_char * 40),        # Model Number, a globally unique identifier for the controller.
        ('fr', c_char * 8),         # Firmware Revision, a string that identifies the firmware revision level of the controller.
        ('rab', c_uint8),           # Recommended Arbitration Burst, reported as a power of two
        ('ieee', c_uint8 * 3),      # IEEE OUI Identifier, a three-byte IEEE OUI assigned to the vendor.
        ('cmic', c_uint8),          # Controller Multi-Path I/O and Namespace Sharing Capabilities, see &enum nvme_ctrl_mic for decoding this field.
        ('mdts', c_uint8),          # Max Data Transfer Size is the largest data transfer size. The host should not submit a command that exceeds this maximum data transfer size. The value is in units of the minimum memory page size (CAP.MPSMIN) and is reported as a power of two
        ('cntlid', c_uint16),       # Controller ID, a unique identifier for the controller.
        ('ver', c_uint32),          # Version, this field contains the value reported in the Version register, or property (see &enum nvme_registers %NVME_REG_VS).
        ('rtd3r', c_uint32),        # RTD3 Resume Latency, the expected latency in microseconds to resume from Runtime D3
        ('rtd3e', c_uint32),        # RTD3 Exit Latency, the typical latency in microseconds to enter Runtime D3.
        ('oaes', c_uint32),         # Optional Async Events Supported, see @enum nvme_id_ctrl_oaes.
        ('ctratt', c_uint32),       # Controller Attributes, see @enum nvme_id_ctrl_ctratt.
        ('rrls', c_uint16),         # Read Recovery Levels. If a bit is set, then the corresponding Read Recovery Level is supported. If a bit is cleared, then the corresponding Read Recovery Level is not supported.
        ('rsvd1', c_uint8 * 9),     # Reserved
        ('cntrltype', c_uint8),     # Controller Type, see &enum nvme_id_ctrl_cntrltype
        ('fguid', c_uint8 * 16),    # Firmware GUID, a 128-bit value that is globally unique for a given Firmware Unit
        ('crdt1', c_uint16),        # Controller Retry Delay time in 100 millisecond units if CQE CRD field is 1
        ('crdt2', c_uint16),        # Controller Retry Delay time in 100 millisecond units if CQE CRD field is 2
        ('crdt3', c_uint16),        # Controller Retry Delay time in 100 millisecond units if CQE CRD field is 3
        ('rsvd2', c_uint8 * 119),   # Reserved
        ('nvmsr', c_uint8),         # NVM Subsystem Report, see &enum nvme_id_ctrl_nvmsr
        ('vwci', c_uint8),          # VPD Write Cycle Information, see &enum nvme_id_ctrl_vwci
        ('mec', c_uint8),           # Management Endpoint Capabilities, see &enum nvme_id_ctrl_mec
        ('oacs', c_uint16),         # Optional Admin Command Support,the optional Admin commands and features supported by the controller, see &enum nvme_id_ctrl_oacs.
        ('acl', c_uint8),           # Abort Command Limit, the maximum number of concurrently executing Abort commands supported by the controller. This is a 0's based value.
        ('aerl', c_uint8),          # Async Event Request Limit, the maximum number of concurrently outstanding Asynchronous Event Request commands supported by the controller This is a 0's based value.
        ('frmw', c_uint8),          # Firmware Updates indicates capabilities regarding firmware updates. See &enum nvme_id_ctrl_frmw.
        ('lpa', c_uint8),           # Log Page Attributes, see &enum nvme_id_ctrl_lpa.
        ('elpe', c_uint8),          # Error Log Page Entries, the maximum number of Error Information log entries that are stored by the controller. This field is a 0's based value.
        ('npss', c_uint8),          # Number of Power States Supported, the number of NVM Express power states supported by the controller, indicating the number of valid entries in &struct nvme_id_ctrl.psd. This is a 0's based value.
        ('avscc', c_uint8),         # Admin Vendor Specific Command Configuration, see  &enum nvme_id_ctrl_avscc.
        ('apsta', c_uint8),         # Autonomous Power State Transition Attributes, see  &enum nvme_id_ctrl_apsta.
        ('wctemp', c_uint16),       # Warning Composite Temperature Threshold indicates the minimum Composite Temperature field value (see &struct nvme_smart_log.critical_comp_time) that indicates an overheating condition during which controller operation continues.
        ('cctemp', c_uint16),       # Critical Composite Temperature Threshold, field indicates the minimum Composite Temperature field value (see &struct nvme_smart_log.critical_comp_time) that indicates a critical overheating condition.
        ('mtfa', c_uint16),         # Maximum Time for Firmware Activation indicates the maximum time the controller temporarily stops processing commands to activate  the firmware image, specified in 100 millisecond units. This field is always valid if the controller supports firmware activation without a reset.
        ('hmpre', c_uint32),        # Host Memory Buffer Preferred Size indicates the preferred size that the host is requested to allocate for the Host Memory Buffer feature in 4 KiB units.
        ('hmmin', c_uint32),        # Host Memory Buffer Minimum Size indicates the minimum size that the host is requested to allocate for the Host Memory Buffer feature in 4 KiB units.
        ('tnvmcap', c_uint8 * 16),  # Total NVM Capacity, the total NVM capacity in the NVM subsystem. The value is in bytes.
        ('unvmcap', c_uint8 * 16),  # Unallocated NVM Capacity, the unallocated NVM capacity in the NVM subsystem. The value is in bytes.
        ('rpmbs', c_uint32),        # Replay Protected Memory Block Support, see &enum nvme_id_ctrl_rpmbs.
        ('edstt', c_uint16),        # Extended Device Self-test Time, if Device Self-test command is supported (see &struct nvme_id_ctrl.oacs, %NVME_CTRL_OACS_SELF_TEST),then this field indicates the nominal amount of time in oneminute units that the controller takes to complete an extended device self-test operation when in power state 0.
        ('dsto', c_uint8),          # Device Self-test Options, see &enum nvme_id_ctrl_dsto.
        ('fwug', c_uint8),          # Firmware Update Granularity indicates the granularity and alignment requirement of the firmware image being updated by the Firmware Image Download command. The value is reported in 4 KiB units. A value of 0h indicates no information on granularity is provided. A value of FFh indicates no restriction
        ('kas', c_uint16),          # Keep Alive Support indicates the granularity of the Keep Alive  Timer in 100 millisecond units.
        ('hctma', c_uint16),        # Host Controlled Thermal Management Attributes, see &enum nvme_id_ctrl_hctm.
        ('mntmt', c_uint16),        # Minimum Time for Temperature-based Shutdown indicates the maximum time the controller temporarily stops processing commands to shutdown the device due to a temperature-based shutdown condition, specified in 100 millisecond units.
        ('mxtmt', c_uint16),        # Maximum Time for Temperature-based Shutdown indicates the maximum time the controller temporarily stops processing commands to shutdown the device due to a temperature-based shutdown condition, specified in 100 millisecond units.
        ('sanicap', c_uint32),      # Sanitize Attributes, see &enum nvme_id_ctrl_sanicap.
        ('hmminds', c_uint32),      # Host Memory Maximum Indicator Size, indicates the maximum size of the Host Memory Buffer feature in 4 KiB units.
        ('hmmaxd', c_uint16),       # Host Memory Maximum Descriptors Entries indicates the number of usable Host Memory Buffer Descriptor Entries.
        ('nsetidmax', c_uint16),    # NVM Set Identifier Maximum, defines the maximum value of a valid NVM Set Identifier for any controller in the NVM subsystem.
        ('endgidmax', c_uint16),    # Endurance Group Identifier Maximum, defines the maximum value of a valid Endurance Group Identifier for any controller in the NVM subsystem.
        ('anatt', c_uint8),         # ANA Transition Time indicates the maximum amount of time, in seconds, for a transition between ANA states or the maximum amount of time, in seconds, that the controller reports the ANA change state.
        ('anacap', c_uint8),        # Asymmetric Namespace Access Capabilities, see &enum nvme_id_ctrl_anacap.
        ('anagrpmax', c_uint32),    # ANA Group Identifier Maximum indicates the maximum value of a valid ANA Group Identifier for any controller in the NVM subsystem.
        ('nanagrpid', c_uint32),    # Number of ANA Group Identifiers indicates the number of ANA groups supported by this controller.
        ('pels', c_uint32),         # Persistent Event Log Size indicates the maximum reportable size for the Persistent Event Log.
        ('domainid', c_uint16),     # Domain Identifier indicates the identifier of the domain that contains this controller.
        ('rsvd3', c_uint8 * 10),  # Reserved
        ('megcap', c_uint8 * 16),   # Max Endurance Group Capacity indicates the maximum capacity of a single Endurance Group.
        ('rsvd4', c_uint8 * 128), # Reserved
        ('sqes', c_uint8),          # Submission Queue Entry Size, see &enum nvme_id_ctrl_sqes.
        ('cqes', c_uint8),          # Completion Queue Entry Size, see &enum nvme_id_ctrl_cqes.
        ('maxcmd', c_uint16),       # Maximum Outstanding Commands indicates the maximum number of commands that the controller processes at one time for a particular queue.
        ('nn', c_uint32),           # Number of Namespaces indicates the maximum value of a valid nsid for the NVM subsystem. If the MNAN (&struct nvme_id_ctrl.mnan field is cleared to 0h, then this field also indicates the maximum number of namespaces supported by the NVM subsystem.
        ('oncs', c_uint16),         # Optional NVM Command Support, see &enum nvme_id_ctrl_oncs.
        ('fuses', c_uint16),        # Fused Operation Support, see &enum nvme_id_ctrl_fuses.
        ('fna', c_uint8),           # Format NVM Attributes, see &enum nvme_id_ctrl_fna.
        ('vwc', c_uint8),           # Volatile Write Cache, see &enum nvme_id_ctrl_vwc.
        ('awun', c_uint16),         # Atomic Write Unit Normal indicates the size of the write operation guaranteed to be written atomically to the NVM across all namespaces with any supported namespace format during normal operation. This field is specified in logical blocks and is a 0's based value.
        ('awupf', c_uint16),        # Atomic Write Unit Power Fail indicates the size of the write operation guaranteed to be written atomically to the NVM across all namespaces with any supported namespace format during a power fail or error condition. This field is specified in logical blocks and is a 0’s based value.
        ('icsvscc', c_uint8),       # NVM Vendor Specific Command Configuration, see  &enum nvme_id_ctrl_nvscc.
        ('nwpc', c_uint8),          # NVM Command Support, see &enum nvme_id_ctrl_nwpc.
        ('acwu', c_uint16),         # Atomic Compare & Write Unit indicates the size of the compare and write operation guaranteed to be written atomically to the NVM across all namespaces with any supported namespace format during normal operation. This field is specified in logical blocks and is a 0's based value.
        ('ocfs', c_uint16),         # Optional Copy Formats Supported, each bit n means controller supports Copy Format n.
        ('sgls', c_uint32),         # SGL Support, see &enum nvme_id_ctrl_sgls
        ('mnan', c_uint32),         # Maximum Number of Allowed Namespaces indicates the maximum number of namespaces supported by the NVM subsystem.
        ('maxdna', c_uint8 * 16),   # Maximum Domain Namespace Attachments indicates the maximum of the sum of the number of namespaces attached to each I/O controller in the Domain.
        ('maxcna', c_uint32),       # Maximum I/O Controller Namespace Attachments indicates the maximum number of namespaces that are allowed to be attached to  this I/O controller.
        ('oaqd', c_uint32),         # Optimal Aggregated Queue Depth indicates the recommended maximum total number of outstanding I/O commands across all I/O queues on the controller for optimal operation.
        ('rsvd5', c_uint8 * 200), # Reserved
        ('subnqn', c_char * 256),   # NVM Subsystem NVMe Qualified Name, UTF-8 null terminated string
        ('rsvd6', c_uint8 * 768),   # Reserved
        ('ioccsz', c_uint32),       # I/O Queue Command Capsule Supported Size, defines the maximum I/O command capsule size in 16 byte units.
        ('iorcsz', c_uint32),       # I/O Queue Response Capsule Supported Size, defines the maximum I/O response capsule size in 16 byte units.
        ('icdoff', c_uint16),       # In Capsule Data Offset, defines the offset where data starts within a capsule. This value is applicable to I/O Queues only.
        ('fcatt', c_uint8),         # Fabrics Controller Attributes, see &enum nvme_id_ctrl_fcatt.
        ('msdbd', c_uint8),         # Maximum SGL Data Block Descriptors indicates the maximum number of SGL Data Block or Keyed SGL Data Block descriptors that a host is allowed to place in a capsule. A value of 0h indicates no limit.
        ('ofcs', c_uint16),         # Optional Fabric Commands Support, see &enum nvme_id_ctrl_ofcs.
        ('dctype', c_uint8),        # Discovery Controller Type (DCTYPE). This field indicates what type of Discovery controller the controller is (see enum nvme_id_ctrl_dctype)
        ('rsvd7', c_uint8 * 241),   # Reserved
        ('psd', nvme_id_psd * 32),  # Power State Descriptors, see &struct nvme_id_psd.
        ('vs', c_uint8 * 1024),     # Vendor Specific
    ]

class  NVME_ID_CTRL_CMIC(Enum):
    """
        Controller Multipath IO and Namespace Sharing Capabilities of the controller and NVM subsystem.
    """
    NVME_CTRL_CMIC_MULTI_PORT		= 1 << 0        # If set, then the NVM subsystem may contain more than one NVM subsystem port, otherwise the NVM subsystem contains only a single NVM subsystem port.
    NVME_CTRL_CMIC_MULTI_CTRL		= 1 << 1        # If set, then the NVM subsystem may contain two or more controllers, otherwise the NVM subsystem contains only a single controller. An NVM subsystem that contains multiple controllers may be used by multiple hosts, or may provide multiple paths for a single host.
    NVME_CTRL_CMIC_MULTI_SRIOV		= 1 << 2        # If set, then the controller is associated with an SR-IOV Virtual Function, otherwise it is associated with a PCI Function or a Fabrics connection.
    NVME_CTRL_CMIC_MULTI_ANA_REPORTING	= 1 << 3    # If set, then the NVM subsystem supports Asymmetric Namespace Access Reporting.

class  NVME_ID_CTRL_OAES(Enum):
    NVME_CTRL_OAES_NA			= 1 << 8            # Optional Asynchronous Events Supported
    NVME_CTRL_OAES_FA			= 1 << 9            # Firmware Activation Notices event supported
    NVME_CTRL_OAES_ANA			= 1 << 11           # ANA Change Notices supported
    NVME_CTRL_OAES_PLEA			= 1 << 12           # Predictable Latency Event Aggregate Log Change Notices event supported
    NVME_CTRL_OAES_LBAS			= 1 << 13           # LBA Status Information Notices event supported
    NVME_CTRL_OAES_EGE			= 1 << 14           # Endurance Group Events Aggregate Log Change Notices event supported
    NVME_CTRL_OAES_NS			= 1 << 15           # Normal NVM Subsystem Shutdown event supported
    NVME_CTRL_OAES_ZD			= 1 << 27           # Zone Descriptor Change Notifications supported
    NVME_CTRL_OAES_DL			= 1 << 31           # Discover Log Page Change Notices supported

class  NVME_ID_CTRL_CTRATT(Enum):
    """
        Controller attributes
    """
    NVME_CTRL_CTRATT_128_ID			= 1 << 0        # 128-bit Host Identifier supported
    NVME_CTRL_CTRATT_NON_OP_PSP		= 1 << 1        # Non-Operational Poser State Permissive Mode supported
    NVME_CTRL_CTRATT_NVM_SETS		= 1 << 2        # NVM Sets supported
    NVME_CTRL_CTRATT_READ_RECV_LVLS		= 1 << 3    # Read Recovery Levels supported
    NVME_CTRL_CTRATT_ENDURANCE_GROUPS	= 1 << 4    # Endurance Groups supported
    NVME_CTRL_CTRATT_PREDICTABLE_LAT	= 1 << 5    # Predictable Latency Mode supported
    NVME_CTRL_CTRATT_TBKAS			= 1 << 6        # Traffic Based Keep Alive supported
    NVME_CTRL_CTRATT_NAMESPACE_GRANULARITY	= 1 << 7# Namespace Granularity reporting supported
    NVME_CTRL_CTRATT_SQ_ASSOCIATIONS	= 1 << 8    # SQ Associations supported
    NVME_CTRL_CTRATT_UUID_LIST		= 1 << 9        # UUID List reporting supported
    NVME_CTRL_CTRATT_MDS			= 1 << 10       # Multi-Domain Subsystem supported
    NVME_CTRL_CTRATT_FIXED_CAP		= 1 << 11       # Fixed Capacity Management  supported
    NVME_CTRL_CTRATT_VARIABLE_CAP		= 1 << 12   # Variable Capacity Management supported
    NVME_CTRL_CTRATT_DEL_ENDURANCE_GROUPS	= 1 << 13# Delete Endurance Groups supported
    NVME_CTRL_CTRATT_DEL_NVM_SETS		= 1 << 14   # Delete NVM Sets supported
    NVME_CTRL_CTRATT_ELBAS			= 1 << 15       # Extended LBA Formats supported
    NVME_CTRL_CTRATT_FDPS			= 1 << 19       # Flexible Data Placement supported

class  NVME_ID_CTRL_CNTRLTYPE(Enum):
    """
        Controller types
    """
    NVME_CTRL_CNTRLTYPE_IO			= 1             # NVM I/O controller
    NVME_CTRL_CNTRLTYPE_DISCOVERY		= 2         # Discovery controller
    NVME_CTRL_CNTRLTYPE_ADMIN		= 3             # Admin controller

class  NVME_ID_CTRL_DCTYPE(Enum):
    """
        Discovery Controller types
    """
    NVME_CTRL_DCTYPE_NOT_REPORTED	= 0             # Not reported (I/O, Admin, and pre-TP8010)
    NVME_CTRL_DCTYPE_DDC		= 1                 # Direct Discovery controller
    NVME_CTRL_DCTYPE_CDC		= 2                 # Central Discovery controller

class  NVME_ID_CTRL_NVMSR(Enum):
    """
        This field reports information associated with the NVM Subsystem, see &struct nvme_id_ctrl.nvmsr.
    """
    NVME_CTRL_NVMSR_NVMESD			= 1 << 0        # If set, then the NVM Subsystem is part of an NVMe Storage Device; if cleared, then the NVM Subsystem is not part of an NVMe Storage Device.
    NVME_CTRL_NVMSR_NVMEE			= 1 << 1        # If set, then the NVM Subsystem is part of an NVMe Enclosure; if cleared, then the NVM Subsystem is not part of an NVMe Enclosure.

class  NVME_ID_CTRL_VWCI(Enum):
    """
        This field indicates information about remaining number of times that VPD contents are able to be updated using the VPD Write command, see &struct nvme_id_ctrl.vwci.
    """
    NVME_CTRL_VWCI_VWCR			= 0x7f << 0
    """
        Mask to get value of VPD Write Cycles Remaining. If the VPD Write Cycle Remaining Valid bit is set, then
        this field contains a value indicating the remaining number of times that VPD contents are able to be
        updated using the VPD Write command. If this field is set to 7Fh, then the remaining number of times that
        VPD contents are able to be updated using the VPD  Write command is greater than or equal to 7Fh.
    """
    NVME_CTRL_VWCI_VWCRV		= 1 << 7
    """
        VPD Write Cycle Remaining Valid. If this bit is set, then the VPD Write Cycle Remaining field is valid. If
        this bit is cleared, then the VPD Write Cycles Remaining field is invalid and cleared to 0h.
    """

class  NVME_ID_CTRL_MEC(Enum):
    """
        Flags indicating the capabilities of the Management Endpoint in the Controller, &struct nvme_id_ctrl.mec.
    """
    NVME_CTRL_MEC_SMBUSME			= 1 << 0        # If set, then the NVM Subsystem contains a Management Endpoint on an SMBus/I2C port.
    NVME_CTRL_MEC_PCIEME			= 1 << 1        # If set, then the NVM Subsystem contains a Management Endpoint on a PCI port

class  NVME_ID_CTRL_OACS(Enum):
    """
        Flags indicating the optional Admin commands and features supported by the controller, see &struct nvme_id_ctrl.oacs.
    """
    NVME_CTRL_OACS_SECURITY			= 1 << 0        # If set, then the controller supports the Security Send and Security Receive commands.
    NVME_CTRL_OACS_FORMAT			= 1 << 1        # If set then the controller supports the Format NVM command.
    NVME_CTRL_OACS_FW			    = 1 << 2        # If set, then the controller supports the Firmware Commit and Firmware Image Download commands.
    NVME_CTRL_OACS_NS_MGMT			= 1 << 3        # If set, then the controller supports the Namespace Management capability
    NVME_CTRL_OACS_SELF_TEST		= 1 << 4        # If set, then the controller supports the Device Self-test command.
    NVME_CTRL_OACS_DIRECTIVES		= 1 << 5        # If set, then the controller supports the Directives and the Directive Send and Directive Receive commands.
    NVME_CTRL_OACS_NVME_MI			= 1 << 6        # If set, then the controller supports the NVMe-MI commands.
    NVME_CTRL_OACS_VIRT_MGMT		= 1 << 7        # If set, then the controller supports the Virtualization Management commands.
    NVME_CTRL_OACS_DBBUF_CFG		= 1 << 8        # If set, then the controller supports the Dual Boot Buffer Configuration command.
    NVME_CTRL_OACS_LBA_STATUS		= 1 << 9        # If set, then the controller supports the LBA Status Information command.
    NVME_CTRL_OACS_CMD_FEAT_LD		= 1 << 10       # If set, then the controller supports the Command and Feature Lockdown capability.

class NVME_ID_CTRL_FRMW(Enum):
    """
        Flags and values indicates capabilities regarding firmware updates from &struct nvme_id_ctrl.frmw.
    """
    NVME_CTRL_FRMW_1ST_RO			= 1 << 0        # If set, the first firmware slot is readonly
    NVME_CTRL_FRMW_NR_SLOTS			= 3 << 1        # Mask to get the value of the number of firmware slots that the controller supports.
    NVME_CTRL_FRMW_FW_ACT_NO_RESET		= 1 << 4    # If set, the controller supports firmware activation without a reset.
    NVME_CTRL_FRMW_MP_UP_DETECTION		= 1 << 5    # If set, the controller is able to detect overlapping firmware/boot partition image update.

class  NVME_ID_CTRL_LPA(Enum):
    """
        Flags indicating optional attributes for log pages that are accessed via the Get Log Page command.
    """
    NVME_CTRL_LPA_SMART_PER_NS		    = 1 << 0    # If set, the controller supports SMART/Health log page on a per namespace basis.
    NVME_CTRL_LPA_CMD_EFFECTS		    = 1 << 1    # If set, the controller supports the commands supported and effects log page.
    NVME_CTRL_LPA_EXTENDED			    = 1 << 2    # If set, the controller supports extended data for log page command including extended number of dwords and log page offset fields.
    NVME_CTRL_LPA_TELEMETRY			    = 1 << 3    # If set, the controller supports the telemetry host-initiated and telemetry controller-initiated log pages and sending telemetry log notices.
    NVME_CTRL_LPA_PERSETENT_EVENT		= 1 << 4    # If set, the controller supports persistent event log.
    NVME_CTRL_LPA_LI0_LI5_LI12_LI13		= 1 << 5    # If set, the controller supports:
                                                    # - log pages log page.
                                                    # - returning scope of each command in commands supported and effects log page.
                                                    # - feature identifiers supported and effects log page.
                                                    # - NVMe-MI commands supported and effects log page.
    NVME_CTRL_LPA_DA4_TELEMETRY		    = 1 << 6,   # If set, the controller supports data area 4 for telemetry host-initiated and telemetry.

class NVME_ID_CTRL_AVSCC(Enum):
    """
        Flags indicating the configuration settings for Admin Vendor Specific command handling.
    """
    NVME_CTRL_AVSCC_AVS = 1 << 0                    # If set, all Admin Vendor Specific Commands use the optional vendor specific command format with NDT and NDM fields.

class NVME_ID_CTRL_RPMBS(Enum):
    """
        This field indicates if the controller supports one or more Replay Protected Memory Blocks, from &struct nvme_id_ctrl.rpmbs.
    """
    NVME_CTRL_RPMBS_NR_UNITS		= 7 << 0        # Mask to get the value of the Number of RPMB Units
    NVME_CTRL_RPMBS_AUTH_METHOD		= 7 << 3        # Mask to get the value of the Authentication Method
    NVME_CTRL_RPMBS_TOTAL_SIZE		= 0xff << 16    # Mask to get the value of Total Size
    NVME_CTRL_RPMBS_ACCESS_SIZE		= 0xff << 24    # Mask to get the value of Access Size

class  NVME_ID_CTRL_DSTO(Enum):
    """
        Flags indicating the optional Device Self-test command or operation behaviors supported by the controller or NVM subsystem.
    """
    NVME_CTRL_DSTO_ONE_DST			= 1 << 0        # If set, then the controller supports only one device self-test operation in progress at a time.

class  NVME_ID_CTRL_HCTM(Enum):
    """
        Flags indicate the attributes of the host controlled thermal management feature
    """
    NVME_CTRL_HCTMA_HCTM = 1 << 0                    # If set, then the controller supports host controlled thermal management, and Get Features command with the Feature Identifier field set to %NVME_FEAT_FID_HCTM.

class  NVME_ID_CTRL_SANICAP(Enum):
    """
        Indicates attributes for sanitize operations.
    """
    NVME_CTRL_SANICAP_CES			= 1 << 0        # Crypto Erase Support. If set, then the controller supports the Crypto Erase sanitize operation.
    NVME_CTRL_SANICAP_BES			= 1 << 1        # Block Erase Support. If set, then the controller supports the Block Erase sanitize operation.
    NVME_CTRL_SANICAP_OWS			= 1 << 2        # Overwrite Support. If set, then the controller supports the Overwrite sanitize operation.
    NVME_CTRL_SANICAP_NDI			= 1 << 29       # No-Deallocate Inhibited. If set and the No- Deallocate Response Mode bit is set, then the controller deallocates after the sanitize operation even if the No-Deallocate After Sanitize bit is set in a Sanitize command.
    NVME_CTRL_SANICAP_NODMMAS		= 3 << 30       # No-Deallocate Modifies Media After Sanitize, mask to extract value.

class NVME_ID_CTRL_ANACAP(Enum):
    """
        This field indicates the capabilities associated with Asymmetric Namespace Access Reporting.
    """
    NVME_CTRL_ANACAP_OPT			= 1 << 0        # If set, then the controller is able to report ANA Optimized state.
    NVME_CTRL_ANACAP_NON_OPT		= 1 << 1        # If set, then the controller is able to report ANA Non-Optimized state.
    NVME_CTRL_ANACAP_INACCESSIBLE		= 1 << 2    # If set, then the controller is able to report ANA Inaccessible state.
    NVME_CTRL_ANACAP_PERSISTENT_LOSS	= 1 << 3    # If set, then the controller is able to report ANA Persistent Loss state.
    NVME_CTRL_ANACAP_CHANGE			= 1 << 4        # If set, then the controller is able to report ANA Change state.
    NVME_CTRL_ANACAP_GRPID_NO_CHG		= 1 << 6    # If set, then the ANAGRPID field in the Identify Namespace data structure (&struct nvme_id_ns.anagrpid), does not change while the namespace is attached to any controller.
    NVME_CTRL_ANACAP_GRPID_MGMT		= 1 << 7        # If set, then the controller supports a management operation to change the ANA state of a namespace.

class NVME_ID_CTRL_SQES(Enum):
    """
        Defines the required and maximum Submission Queue entry size when using the NVM Command Set.
    """
    NVME_CTRL_SQES_MIN			= 0xf << 0          # Mask to get the value of the required Submission Queue Entry size when using the NVM Command Set.
    NVME_CTRL_SQES_MAX			= 0xf << 4          # Mask to get the value of the maximum Submission Queue entry size when using the NVM Command Set.

class NVME_ID_CTRL_CQES(Enum):
    """
        Defines the required and maximum Completion Queue entry size when using the NVM Command Set.
    """
    NVME_CTRL_CQES_MIN			= 0xf << 0          # Mask to get the value of the required Completion Queue Entry size when using the NVM Command Set.
    NVME_CTRL_CQES_MAX			= 0xf << 4          # Mask to get the value of the maximum Completion Queue entry size when using the NVM Command Set.

class NVME_ID_CTRL_ONCS(Enum):
    """
        This field indicates the optional NVM commands and features supported by the controller.
    """
    NVME_CTRL_ONCS_COMPARE			= 1 << 0        # If set, then the controller supports the Compare command.
    NVME_CTRL_ONCS_WRITE_UNCORRECTABLE	= 1 << 1    # If set, then the controller supports the Write Uncorrectable command.
    NVME_CTRL_ONCS_DSM			= 1 << 2            # If set, then the controller supports the Dataset Management command.
    NVME_CTRL_ONCS_WRITE_ZEROES		= 1 << 3        # If set, then the controller supports the Write Zeroes command.
    NVME_CTRL_ONCS_SAVE_FEATURES		= 1 << 4    # If set, then the controller supports the Save Features command.
    NVME_CTRL_ONCS_RESERVATIONS		= 1 << 5        # If set, then the controller supports the Reservation commands.
    NVME_CTRL_ONCS_TIMESTAMP		= 1 << 6        # If set, then the controller supports the Timestamp feature.
    NVME_CTRL_ONCS_VERIFY			= 1 << 7        # If set, then the controller supports the Verify command.
    NVME_CTRL_ONCS_COPY			= 1 << 8            # If set, then the controller supports the Copy command.

class NVME_ID_CTRL_FUSE(Enum):
    """
        his field indicates the fused operations that the controller supports
    """
    NVME_CTRL_FUSES_COMPARE_AND_WRITE = 1 << 0      # If set, then the controller supports the Compare and Write fused operation.

class NVME_ID_CTRL_FNA(Enum):
    """
        This field indicates attributes for the Format NVM command
    """
    NVME_CTRL_FNA_FMT_ALL_NAMESPACES	= 1 << 0    # If set, then all namespaces in an NVM subsystem shall be configured with the same attributes and a format (excluding secure erase) of any namespace results in a format of all namespaces in an NVM subsystem. If cleared, then the controller supports format on a per namespace basis.
    NVME_CTRL_FNA_SEC_ALL_NAMESPACES	= 1 << 1    # If set, then any secure erase performed as part of a format operation results in a secure erase of all namespaces in the NVM subsystem. If cleared, then any secure erase performed as part of a format results in a secure erase of the particular namespace specified.
    NVME_CTRL_FNA_CRYPTO_ERASE		= 1 << 2        # If set, then cryptographic erase is supported.
    NVME_CTRL_FNA_NSID_FFFFFFFF		= 1 << 3        # If set, then format does not support nsid value set to FFFFFFFFh. If cleared, format supports nsid value set to FFFFFFFFh.

class NVME_ID_CTRL_VWC(Enum):
    """
        enum nvme_id_ctrl_vwc - Volatile write cache
    """
    NVME_CTRL_VWC_PRESENT			= 1 << 0    # If set, indicates a volatile write cache is present. If a volatile write cache is present, then the host controls whether the volatile write cache is enabled  with a Set Features command specifying the value %NVME_FEAT_FID_VOLATILE_WC.
    NVME_CTRL_VWC_FLUSH			= 3 << 1        # Mask to get the value of the flush command behavior.

class NVME_ID_CTRL_NVSCC(Enum):
    """
        This field indicates the configuration settings for NVM Vendor Specific command handling.
    """
    NVME_CTRL_NVSCC_FMT = 1 << 0               # If set, all NVM Vendor Specific Commands use the format with NDT and NDM fields.

class NVME_ID_CTRL_NWPC(Enum):
    """
        This field indicates the optional namespace write protection capabilities supported by the controller.
    """
    NVME_CTRL_NWPC_WRITE_PROTECT = 1 << 0               # If set, then the controller shall support the No Write Protect and Write Protect namespace write protection states and may support  the Write Protect Until Power Cycle state and Permanent Write Protect namespace write protection states.
    NVME_CTRL_NWPC_WRITE_PROTECT_POWER_CYCLE = 1 << 1   # If set, then the controller supports the Write Protect Until  Power Cycle state.
    NVME_CTRL_NWPC_WRITE_PROTECT_PERMANENT = 1 << 2     # If set, then the controller supports the Permanent Write Protect state.

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

class NVME_ID_CTRL_SGLS(Enum):
    """
    This class represents the NVMe Controller SGL (Scatter Gather List) Support field.
    It indicates whether SGLs are supported for the NVM Command Set and the specific SGL types supported.

    Attributes:
        NVME_CTRL_SGLS_SUPPORTED: Indicates if SGLs are supported for the NVM Command Set.
        NVME_CTRL_SGLS_KEYED: Indicates if keyed SGLs are supported.
        NVME_CTRL_SGLS_BIT_BUCKET: Indicates if bit bucket SGLs are supported.
        NVME_CTRL_SGLS_MPTR_BYTE_ALIGNED: Indicates if the memory pointer in SGLs is byte-aligned.
        NVME_CTRL_SGLS_OVERSIZE: Indicates if oversize SGLs are supported.
        NVME_CTRL_SGLS_MPTR_SGL: Indicates if the memory pointer in SGLs is itself an SGL.
        NVME_CTRL_SGLS_OFFSET: Indicates if offset SGLs are supported.
        NVME_CTRL_SGLS_TPORT: Indicates if transport SGLs are supported.
    """
    NVME_CTRL_SGLS_SUPPORTED		= 3 << 0
    NVME_CTRL_SGLS_KEYED			= 1 << 2
    NVME_CTRL_SGLS_BIT_BUCKET		= 1 << 16
    NVME_CTRL_SGLS_MPTR_BYTE_ALIGNED	= 1 << 17
    NVME_CTRL_SGLS_OVERSIZE			= 1 << 18
    NVME_CTRL_SGLS_MPTR_SGL			= 1 << 19
    NVME_CTRL_SGLS_OFFSET			= 1 << 20
    NVME_CTRL_SGLS_TPORT			= 1 << 21


class NVME_ID_CTRL_FCATT(Enum):
    """
        This field indicates attributes of the controller that are specific to NVMe over Fabrics.
    """
    NVME_CTRL_FCATT_DYNAMIC = 1 << 0        # If cleared, then the NVM subsystem uses a dynamic controller model. If set, then the NVM subsystem uses a static controller model.

class NVME_ID_CTRL_OFCS(Enum):
    """
        Indicate whether the controller supports optional fabric commands.
    """
    NVME_CTRL_OFCS_DISCONNECT		= 1 << 0        # If set, then the controller supports the Disconnect command and deletion of individual I/O Queues.

class nvme_lbaf(StructureBase):
    """
        LBA Format Data Structure
    """
    _fields_ = [
        ("ms", c_uint16),       # Metadata Size indicates the number of metadata bytes provided per LBA based on the LBA Data Size indicated.
        ("ds", c_uint8),        # LBA Data Size indicates the LBA data size supported, reported as a power of two.
        ("rp", c_uint8),        # Relative Performance, see &enum nvme_lbaf_rp.
    ]

class NVME_LBAF_RP(Enum):
    """
        enum nvme_lbaf_rp - This field indicates the relative performance of the LBA
        format indicated relative to other LBA formats supported
        by the controller.
    """
    NVME_LBAF_RP_BEST = 0               # Best performance
    NVME_LBAF_RP_BETTER = 1             # Better performance
    NVME_LBAF_RP_GOOD = 2               # Good performance
    NVME_LBAF_RP_DEGRADED = 3           # Degraded

class nvme_id_ns(StructureBase):
    """
        Identify Namespace data structure
    """
    _fields_ = [
        ('nsze', c_uint64),         # Namespace Size indicates the total size of the namespace in logical blocks. The number of logical blocks is based on the formatted LBA size.
        ('ncap', c_uint64),         # Namespace Capacity indicates the maximum number of logical blocks that may be allocated in the namespace at any point in time. The number of logical blocks is
                                    # based on the formatted LBA size.
        ('nuse', c_uint64),         # Namespace Utilization indicates the current number of logical blocks allocated in the namespace. This field is smaller than or equal to the Namespace Capacity.
                                    # The number of logical blocks is  based on the formatted LBA size.
        ('nsfeat', c_uint8),        # Namespace Features, see &enum nvme_id_nsfeat.
        ('nlbaf', c_uint8),         # Number of LBA Formats defines the number of supported LBA data size and metadata size combinations supported by the namespace and the highest possible index to &struct nvme_id_ns.lbaf.
        ('flbas', c_uint8),         # Formatted LBA Size, see &enum nvme_id_ns_flbas.
        ('mc', c_uint8),            # Metadata Capabilities, see &enum nvme_id_ns_mc.
        ('dpc', c_uint8),           # End-to-end Data Protection Capabilities, see &enum nvme_id_ns_dpc.
        ('dps', c_uint8),           # End-to-end Data Protection Type Settings, see &enum nvme_id_ns_dps.
        ('nmic', c_uint8),          # Namespace Multi-path I/O and Namespace Sharing Capabilities, see &enum nvme_id_ns_nmic.
        ('rescap', c_uint8),        # Reservation Capabilities, see &enum nvme_id_ns_rescap.
        ('fpi', c_uint8),           # Format Progress Indicator, see &enum nvme_nd_ns_fpi.
        ('dlfeat', c_uint8),        # Deallocate Logical Block Features, see &enum nvme_id_ns_dlfeat.
        ('nawun', c_uint16),        # Namespace Atomic Write Unit Normal indicates the namespace specific size of the write operation guaranteed to be written atomically to the NVM during normal operation.
        ('nawupf', c_uint16),       # Namespace Atomic Write Unit Power Fail indicates the namespace specific size of the write operation guaranteed to be written atomically to the NVM during a power fail or error condition.
        ('nacwu', c_uint16),        # Namespace Atomic Compare & Write Unit indicates the namespace specific size of the write operation guaranteed to be written atomically to the NVM for a Compare and Write fused command.
        ('nabsn', c_uint16),        # Namespace Atomic Boundary Size Normal indicates the atomic boundary size for this namespace for the NAWUN value. This field is specified in logical blocks.
        ('nabo', c_uint16),         # Namespace Atomic Boundary Offset indicates the LBA on this namespace where the first atomic boundary starts.
        ('nabspf', c_uint16),       # Namespace Atomic Boundary Size Power Fail indicates the atomic boundary size for this namespace specific to the Namespace Atomic Write Unit Power Fail value.
                                    # This field is specified in logical blocks.
        ('noiob', c_uint16),        # Namespace Optimal I/O Boundary indicates the optimal I/O boundary for this namespace. This field is specified in logical blocks. The host should construct
                                    # Read and Write commands that do not cross the I/O boundary to achieve optimal performance.
        ('nvmcap', c_uint8 * 16),   # NVM Capacity indicates the total size of the NVM allocated to this namespace. The value is in bytes.
        ('npwg', c_uint16),         # Namespace Preferred Write Granularity indicates the smallest recommended write granularity in logical blocks for this namespace. This is a 0's based value.
        ('npwa', c_uint16),         # Namespace Preferred Write Alignment indicates the recommended write alignment in logical blocks for this namespace. This is a 0's based value.
        ('npdg', c_uint16),         # Namespace Preferred Deallocate Granularity indicates the recommended granularity in logical blocks for the Dataset Management command with the Attribute - Deallocate bit.
        ('npda', c_uint16),         # Namespace Preferred Deallocate Alignment indicates the recommended alignment in logical blocks for the Dataset Management command with the Attribute - Deallocate bit
        ('nows', c_uint16),         # Namespace Optimal Write Size indicates the size in logical blocks for optimal write performance for this namespace. This is a 0's based value.
        ('mssrl', c_uint16),        # Maximum Single Source Range Length indicates the maximum number of logical blocks that may be specified in each valid Source Range field of a Copy command.
        ('mcl', c_uint32),          # Maximum Copy Length indicates the maximum number of logical blocks that may be specified in a Copy command.
        ('msrc', c_uint8),          # Maximum Source Range Count indicates the maximum number of Source  Range entries that may be used to specify source data in a Copy command. This is a 0’s based value.
        ('rsvd81', c_uint8),        # Reserved
        ('nulbaf', c_uint8),        # Number of Unique Capability LBA Formats defines the number of supported user data size and metadata size combinations supported by the namespace
                                    # that may not share the same capabilities. LBA formats shall be allocated in order and packed sequentially.
        ('rsvd83', c_uint8 * 9),    # Reserved
        ('anagrpid', c_uint32),     # ANA Group Identifier indicates the ANA Group Identifier of the ANA group of which the namespace is a member.
        ('rsvd96', c_uint8 * 3),    # Reserved
        ('nsattr', c_uint8),        # Namespace Attributes, see &enum nvme_id_ns_attr.
        ('nvmsetid', c_uint16),     # NVM Set Identifier indicates the NVM Set with which this namespace is associated.
        ('endgid', c_uint16),       # Endurance Group Identifier indicates the Endurance Group with which this namespace is associated.
        ('nguid', c_uint8 * 16),    # Namespace Globally Unique Identifier contains a 128-bit value that is globally unique and assigned to the namespace when the namespace is created.
                                    # This field remains fixed throughout the life of the namespace and is preserved across namespace and controller operations
        ('eui64', c_uint8 * 8),     # IEEE Extended Unique Identifier contains a 64-bit IEEE Extended Unique Identifier (EUI-64) that is globally unique and assigned to the namespace when the
                                    # namespace is created. This field remains fixed throughout the life of the namespace and is  preserved across namespace and controller operations
        ('lbaf', nvme_lbaf * 64),   # LBA Format, see &struct nvme_lbaf.
        ('lbstm', c_uint64),        # Logical Block Storage Tag Mask for end-to-end protection
        ('vs', c_uint8 * 3704),     # Vendor Specific
    ]

class NVME_ID_NSFEAT(Enum):
    """
        This field defines features of the namespace.
    """
    NVME_NS_FEAT_THIN		= 1 << 0        # If set, indicates that the namespace supports thin provisioning. Specifically, the Namespace Capacity reported may be less than the Namespace Size.
    NVME_NS_FEAT_NATOMIC		= 1 << 1    # If set, indicates that the fields NAWUN, NAWUPF, and NACWU are defined for this namespace and should be used by the host for this namespace instead of
                                            # the AWUN, AWUPF, and ACWU fields in the Identify Controller data structure.
    NVME_NS_FEAT_DULBE		= 1 << 2        # If set, indicates that the controller supports the Deallocated or Unwritten Logical Block error for this namespace.
    NVME_NS_FEAT_ID_REUSE		= 1 << 3    # If set, indicates that the value in the NGUID field for this namespace, if non- zero, is never reused by the controller. and that the value in the EUI64
                                            # field for this namespace, if non-zero, is never reused by the controller.
    NVME_NS_FEAT_IO_OPT		= 1 << 4        # If set, indicates that the fields NPWG, NPWA, NPDG,  NPDA, and NOWS are defined for this namespace and should be used by the host for I/O optimization

class NVME_ID_NS_FLABS(Enum):
    """
        his field indicates the LBA data size & metadata size combination that the namespace has been formatted with
    """
    NVME_NS_FLBAS_LOWER_MASK	= 15 << 0   # Mask to get the index of one of the supported LBA Formats's least significant 4bits indicated in struct nvme_id_ns.lbaf.
    NVME_NS_FLBAS_META_EXT		= 1 << 4    # Applicable only if format contains metadata. If this bit is set, indicates that the metadata is transferred at the end of the data LBA,
                                            # creating an extended data LBA. If cleared, indicates that all of the metadata for a command is transferred as a separate contiguous buffer of data.
    NVME_NS_FLBAS_HIGHER_MASK	= 3 << 5    # Mask to get the index of one of the supported LBA Formats's most significant 2bits indicated in struct nvme_id_ns.lbaf.


class NVME_ID_NS_ELBAF(Enum):
    """
        This field indicates the extended LBA format
    """
    NVME_NVM_ELBAF_STS_MASK		= 127 << 0  # Mask to get the storage tag size used to determine the variable-sized storage tag/reference tag fields
    NVME_NVM_ELBAF_PIF_MASK		= 3 << 7    # Mask to get the protection information format for the extended LBA format.

class NVME_ID_NS_MC(Enum):
    """
        This field indicates the capabilities for metadata.
    """
    NVME_NS_MC_EXTENDED		= 1 << 0    # If set, indicates the namespace supports the metadata being transferred as part of a separate buffer that is specified in the Metadata Pointer.
    NVME_NS_MC_SEPARATE		= 1 << 1    # If set, indicates that the namespace supports the metadata being transferred as part of an extended data LBA.

class NVME_ID_NS_DPC(Enum):
    """
        This field indicates the capabilities for the end-to-end data protection feature.
    """
    NVME_NS_DPC_PI_TYPE1		= 1 << 0        # If set, indicates that the namespace supports Protection Information Type 1.
    NVME_NS_DPC_PI_TYPE2		= 1 << 1        # If set, indicates that the namespace supports Protection Information Type 2.
    NVME_NS_DPC_PI_TYPE3		= 1 << 2        # If set, indicates that the namespace supports Protection Information Type 3.
    NVME_NS_DPC_PI_FIRST		= 1 << 3        # If set, indicates that the namespace supports protection information transferred as the first eight bytes of metadata.
    NVME_NS_DPC_PI_LAST		    = 1 << 4        # If set, indicates that the namespace supports protection information transferred as the last eight bytes of metadata.

class NVME_ID_NS_DPS(Enum):
    """
        This field indicates the Type settings for the end-to-end data protection feature.
    """
    NVME_NS_DPS_PI_NONE		    = 0        # Protection information is not enabled
    NVME_NS_DPS_PI_TYPE1		= 1        # Protection information is enabled, Type 1
    NVME_NS_DPS_PI_TYPE2		= 2        # Protection information is enabled, Type 2
    NVME_NS_DPS_PI_TYPE3		= 3        # Protection information is enabled, Type 3
    NVME_NS_DPS_PI_MASK		    = 7 << 0   # Mask to get the value of the PI type
    NVME_NS_DPS_PI_FIRST		= 1 << 3   # If set, indicates that the protection information, if enabled, is transferred as the first eight bytes of metadata.

class NVME_ID_NS_NMIC(Enum):
    """
        This field specifies multi-path I/O and namespace sharing capabilities of the namespace.
    """
    NVME_NS_NMIC_SHARED		= 1 << 0    # If set, then the namespace may be attached to two or more controllers in the NVM subsystem concurrently.

class NVME_ID_NS_RESCAP(Enum):
    """
        This field indicates the reservation capabilities of the namespace.
    """
    NVME_NS_RESCAP_PTPL		= 1 << 0            # If set, indicates that the namespace supports the Persist Through Power Loss capability.
    NVME_NS_RESCAP_WE		= 1 << 1            # If set, indicates that the namespace supports the Write Exclusive reservation type.
    NVME_NS_RESCAP_EA		= 1 << 2            # If set, indicates that the namespace supports the Exclusive Access reservation type.
    NVME_NS_RESCAP_WERO		= 1 << 3            # If set, indicates that the namespace supports the Write Exclusive - Registrants Only reservation type.
    NVME_NS_RESCAP_EARO		= 1 << 4            # If set, indicates that the namespace supports the Exclusive Access - Registrants Only reservation type.
    NVME_NS_RESCAP_WEAR		= 1 << 5            # If set, indicates that the namespace supports the Write Exclusive - All Registrants reservation type.
    NVME_NS_RESCAP_EAAR		= 1 << 6            # If set, indicates that the namespace supports the Exclusive Access - All Registrants reservation type.
    NVME_NS_RESCAP_IEK_13	= 1 << 7            # If set, indicates that Ignore Existing Key is used as defined in revision 1.3 or later of this specification.


class NVME_ID_NS_FPI(Enum):
    """
        If a format operation is in progress, this field indicates the percentage of the namespace that remains to be formatted.
    """
    NVME_NS_FPI_REMAINING		= 0x7f << 0  # Mask to get the format percent remaining value
    NVME_NS_FPI_SUPPORTED		= 1 << 7     # If set, indicates that the namespace supports the Format Progress Indicator defined for the field.

class NVME_ID_NS_DLFEAT(Enum):
    """
        This field indicates information about features that affect deallocating logical blocks for this  namespace.
    """
    NVME_NS_DLFEAT_RB		    = 7 << 0        # Mask to get the value of the read behavior
    NVME_NS_DLFEAT_RB_NR		= 0             # Read behvaior is not reported
    NVME_NS_DLFEAT_RB_ALL_0S	= 1             # A deallocated logical block returns all bytes cleared to 0h.
    NVME_NS_DLFEAT_RB_ALL_FS	= 2             # A deallocated logical block returns all bytes set to FFh.
    NVME_NS_DLFEAT_WRITE_ZEROES	= 1 << 3        # If set, indicates that the controller supports the Deallocate bit in the Write Zeroes command for this namespace.
    NVME_NS_DLFEAT_CRC_GUARD	= 1 << 4        # If set, indicates that the Guard field for deallocated logical blocks that contain protection information is set to the CRC for the value read from
                                                # the deallocated logical block and its metadata

class NVME_ID_NS_ATTR(Enum):
    """
        Specifies attributes of the namespace.
    """
    NVME_NS_NSATTR_WRITE_PROTECTED	= 1 << 0        # If set, then the namespace is currently write protected and all write access to the namespace shall fail.

class nvme_id_ns_desc(StructureBase):
    """
        Namespace identifier type descriptor
    """
    _fields_ = [
        ("nidt", c_uint8),          # Namespace Identifier Type,
        ("nidl", c_uint8),          # Namespace Identifier Length contains the length in bytes of the &struct nvme_id_ns.nid.
        ("rsvd", c_uint16),         # Reserved
        ("nid", Pointer(c_uint8, "nidl")),       # Namespace Identifier contains a value that is globally unique and assigned to the namespace when the namespace is created. The length is defined in &struct nvme_id_ns.nidl.
    ]

class NVME_ID_NS_DESC_NIDT(Enum):
    """
        enum nvme_id_ns_desc_nidt - Known namespace identifier types
    """
    NVME_NIDT_EUI64		= 1        # IEEE Extended Unique Identifier, the NID field contains a copy of the EUI64 field in the struct nvme_id_ns.eui64.
    NVME_NIDT_NGUID		= 2        # Namespace Globally Unique Identifier,the NID field contains a copy of the NGUID field in struct nvme_id_ns.nguid.
    NVME_NIDT_UUID		= 3        # The NID field contains a 128-bit Universally Unique Identifier (UUID) as specified in RFC 4122.
    NVME_NIDT_CSI		= 4        # The NID field contains the command set identifier.

class NVME_ID_NS_DESC_NIDT_LEN(Enum):
    """
        enum nvme_ns_id_desc_nidt_lens - Namespace identifier type lengths
    """
    NVME_NIDT_EUI64_LEN		= 8        # IEEE Extended Unique Identifier, the NID field contains a copy of the EUI64 field in the struct nvme_id_ns.eui64.
    NVME_NIDT_NGUID_LEN		= 16       # Namespace Globally Unique Identifier,the NID field contains a copy of the NGUID
    NVME_NIDT_UUID_LEN		= 16       # The NID field contains a 128-bit Universally Unique Identifier (UUID) as specified in RFC 4122.
    NVME_NIDT_CSI_LEN		= 1        # The NID field contains the command set identifier.

class nvme_nvmset_attr_entry(StructureBase):
    """
        NVM Set Attributes Entry
    """
    _fields_ = [
        ("nvmsetid", c_uint16),     # NVM Set Identifier
        ("endgid", c_uint16),       # Endurance Group Identifier
        ("rsvd4", c_uint8 * 4),     # Reserved
        ("rr4kt", c_uint32),        # Random 4 KiB Read Typical indicates the typical time to complete a 4 KiB random read in 100 nanosecond units when the NVM Set is in a Predictable Latency Mode
                                    # Deterministic Window and there is 1 outstanding command per NVM Set.
        ("ows", c_uint32),          # Optimal Write Size
        ("tnvmsetcap", c_uint8 * 16),# Total NVM Set Capacity
        ("unvmsetcap", c_uint8 * 16),# Unallocated NVM Set Capacity
        ("rsvd48", c_uint8 * 80),   # Reserved
    ]

class nvme_id_nvmset_list(StructureBase):
    """
        NVM set list
    """
    _fields_ = [
        ("nid", c_uint8),                   # Nvmset id
        ("rsvd1", c_uint8 * 127),           # Reserved
        ("ent", nvme_nvmset_attr_entry * 31),     # nvmset id list
    ]

class nvme_id_independent_id_ns(StructureBase):
    """
        Identify - I/O Command Set Independent Identify Namespace Data Structure
    """
    _fields_ = [
        ("nsfeat", c_uint8),        # Common namespace features
        ("nmic", c_uint8),          # Namespace Multi-path I/O and Namespace Sharing Capabilities
        ("rescap", c_uint8),        # Reservation Capabilities
        ("fpi", c_uint8),           # Format Progress Indicator
        ("anagrpid", c_uint32),     # ANA Group Identifier
        ("nsattr", c_uint8),        # Namespace Attributes
        ("rsvd9", c_uint8),         # Reserved
        ("nvmsetid", c_uint16),     # NVM Set Identifier
        ("endgid", c_uint16),       # Endurance Group Identifier
        ("nstat", c_uint8),         # Namespace Status
        ("rsvd15", c_uint8 * 4081), # Reserved
    ]

class nvme_id_ns_granularity_desc(StructureBase):
    """
        Namespace Granularity Descriptor
    """
    _fields_ = [
        ("nszegran", c_uint64),     # Namespace Size Granularity
        ("ncapgran", c_uint64),     # Namespace Capacity Granularity
    ]

class nvme_id_ns_granularity_list(StructureBase):
    """
        Namespace Granularity List
    """
    _fields_ = [
        ("attributes", c_uint32),       # Namespace Granularity Attributes
        ("num_descriptors", c_uint8),   # Number of Descriptors
        ("rsvd5", c_uint8 * 27),        # Reserved
        ("entry", nvme_id_ns_granularity_desc * 16), # Namespace Granularity Descriptor
        ("rsvd288", c_uint8 * 3808),    # Reserved
    ]

class nvme_id_uuid_list_entry(StructureBase):
    """
        UUID List Entry
    """
    _fields_ = [
        ("header", c_uint8),        # UUID Lists Entry Header
        ("rsvd1", c_uint8 * 15),    # reserved
        ("uuid", c_uint8 * 16),     # 128-bit Universally Unique Identifier
    ]

class NVME_ID_UUID(Enum):
    """
        enum nvme_id_uuid - Identifier Association
    """
    NVME_ID_UUID_HDR_ASSOCIATION_MASK		    = 0x3
    NVME_ID_UUID_ASSOCIATION_NONE			    = 0
    NVME_ID_UUID_ASSOCIATION_VENDOR			    = 1
    NVME_ID_UUID_ASSOCIATION_SUBSYSTEM_VENDOR	= 2

class nvme_id_uuid_list(StructureBase):
    """
        UUID list
    """
    _fields_ = [
        ("rsvd0", c_uint8 * 32),                        # reserved
        ("entry", nvme_id_uuid_list_entry * 127),       # UUID list entry
    ]

class nvme_ctrl_list(StructureBase):
    """
        Controller List
    """
    _fields_ = [
        ("num", c_uint16),                      # Number of Identifiers
        ("identifier", c_uint16 * 2047),         # NVM subsystem unique controller identifier
    ]

class nvme_ns_list(StructureBase):
    """
        Namespace List
    """
    _fields_ = [
        ("ns", c_uint32 * 1024),        # Namespace Identifier
    ]

class nvme_id_ctrl_nvm(StructureBase):
    """
        I/O Command Set Specific Identify Controller data structure
    """
    _fields_ = [
        ("vsl", c_uint8),           # Verify Size Limit
        ("wzsl", c_uint8),          # Write Zeroes Size Limit
        ("wusl", c_uint8),          # Write Uncorrectable Size Limit
        ("dmrl", c_uint8),          # Dataset Management Ranges Limit
        ("dmrsl", c_uint32),        # Dataset Management Range Size Limit
        ("dmsl", c_uint64),         # Dataset Management Size Limit
        ("rsvd16", c_uint8 * 4080), # Reserved
    ]

class nvme_nvm_id_ns(StructureBase):
    """
        NVME Command Set I/O Command Set Specific Identify Namespace Data Structure
    """
    _fields_ = [
        ("lbstm", c_uint64),    # Logical Block Storage Tag Mask
        ("pic", c_uint8),       # Protection Information Capabilities
        ("rsvd9", c_uint8 * 3), # Reserved
        ("elbaf", c_uint32 * 64),# List of Extended LBA Format Support
        ("rsvd268", c_uint8 * 3828),# Reserved
    ]

class nvme_zns_lbafe(StructureBase):
    """
        Zone Size Extension Data Structure
    """
    _fields_ = [
        ("zsze", c_uint64),     # Zone Size
        ("zdes", c_uint8),      # Zone Descriptor Extension Size
        ("rsvd9", c_uint8 * 7), # Reserved
    ]

class nvme_zns_id_ns(StructureBase):
    """
        Zoned Namespace Command Set Specific  Identify Namespace Data Structure
    """
    _fields_ = [
        ("zoc", c_uint16),          # Zone Operation Characteristics
        ("ozcs", c_uint16),         # Optional Zoned Command Support
        ("mar", c_uint32),          # Maximum Active Resources
        ("mor", c_uint32),          # Maximum Open Resources
        ("rrl", c_uint32),          # Reset Recommended Limit
        ("frl", c_uint32),          # Finish Recommended Limit
        ("rrl1", c_uint32),         # Reset Recommended Limit 1
        ("rrl2", c_uint32),         # Reset Recommended Limit 2
        ("rrl3", c_uint32),         # Reset Recommended Limit 3
        ("frl1", c_uint32),         # Finish Recommended Limit 1
        ("frl2", c_uint32),         # Finish Recommended Limit 2
        ("frl3", c_uint32),         # Finish Recommended Limit 3
        ("numzrwa", c_uint32),      # Number of ZRWA Resources
        ("zrwafg", c_uint16),       # ZRWA Flush Granularity
        ("zrwasz", c_uint16),       # ZRWA Size
        ("zrwacap", c_uint8),       # ZRWA Capability
        ("rsvd53", c_uint8 * 2763), # Reserved
        ("lbafe", nvme_zns_lbafe * 64), # LBA Format Extension
        ("vs", c_uint8 * 256),      # Vendor Specific
    ]

class nvme_zns_id_ctrl(StructureBase):
    """
        I/O Command Set Specific Identify Controller Data Structure for the Zoned Namespace Command Set
    """
    _fields_ = [
        ("zasl", c_uint8),      # Zone Append Size Limit
        ("rsvd1", c_uint8 * 4095), # Reserved
    ]

class nvme_primary_ctrl_cap(StructureBase):
    """
        Identify - Controller Capabilities Structure
    """
    _fields_ = [
        ("cntlid", c_uint16),       # Controller Identifier
        ("portid", c_uint16),       # Port Identifier
        ("crt", c_uint8),           # Controller Resource Types
        ("rsvd5", c_uint8 * 27),    # reserved
        ("vqfrt", c_uint32),        # VQ Resources Flexible Total
        ("vqrfa", c_uint32),        # VQ Resources Flexible Assigned
        ("vqrfap", c_uint16),       # VQ Resources Flexible
        ("vqprt", c_uint16),        # VQ Resources Private Total
        ("vqfrsm", c_uint16),       # VQ Resources Flexible Secondary Maximum
        ("vqgran", c_uint16),       # VQ Flexible Resource Preferred Granularity
        ("rsvd48", c_uint8 * 16),   # reserved
        ("vifrt", c_uint32),        # VI Resources Flexible Total
        ("virfa", c_uint32),        # VI Resources Flexible Assigned
        ("virfap", c_uint16),       # VI Resources Flexible
        ("viprt", c_uint16),        # VI Resources Private Total
        ("vifrsm", c_uint16),       # VI Resources Flexible Secondary Maximum
        ("vigran", c_uint16),       # VI Flexible Resource Preferred Granularity
        ("rsvd80", c_uint8 * 4016), # reserved
    ]

class nvme_secondary_ctrl(StructureBase):
    """
        Secondary Controller Entry
    """
    _fields_ = [
        ("scid", c_uint16),     # Secondary Controller Identifier
        ("pcid", c_uint16),     # Primary Controller Identifier
        ("scs", c_uint8),       # Secondary Controller State
        ("rsvd5", c_uint8 * 3), # Reserved
        ("vfn", c_uint16),      # Virtual Function Number
        ("nvq", c_uint16),      # Number of VQ Flexible Resources Assigned
        ("nvi", c_uint16),      # Number of VI Flexible Resources Assigned
        ("rsvd14", c_uint8 * 18), # Reserved
    ]

class nvme_secondary_ctrl_list(StructureBase):
    """
        Secondary Controller List
    """
    _fields_ = [
        ("num", c_uint8),       # Number of Identifiers
        ("rsvd", c_uint8 * 31), # Reserved
        ("sc_entry", nvme_secondary_ctrl * 127), # Secondary Controller Entry
    ]

class nvme_id_iocs(StructureBase):
    """
        NVMe Identify IO Command Set data structure
    """
    _fields_ = [
        ("iocsc", c_uint64 * 512), # List of supported IO Command Set Combination vectors
    ]

class nvme_id_domain_attr(StructureBase):
    """
        Domain Attributes Entry
    """
    _fields_ = [
        ("dom_id", c_uint16),       # Domain Identifier
        ("rsvd2", c_uint8 * 14),    # Reserved
        ("dom_cap", c_uint8 * 16),  # Total Domain Capacity
        ("unalloc_dom_cap", c_uint8 * 16), # Unallocated Domain Capacity
        ("max_egrp_dom_cap", c_uint8 * 16), # Max Endurance Group Domain Capacity
        ("rsvd64", c_uint8 * 64),   # Reserved
    ]

class nvme_id_domain_list(StructureBase):
    """
        Domain List
    """
    _fields_ = [
        ("num", c_uint8),       # Number of domain attributes
        ("rsvd", c_uint8 * 127), # Reserved
        ("domain_attr", nvme_id_domain_attr * 31), # Domain Attributes Entry
    ]

class nvme_id_endurance_group_list(StructureBase):
    """
        Endurance Group List
    """
    _fields_ = [
        ("num", c_uint16),       # Number of Identifiers
        ("identifier", c_uint16 * 2047), # Endurance Group Identifier
    ]

class nvme_supported_log_pages(StructureBase):
    """
        Supported Log Pages - Log
    """
    _fields_ = [
        ("lid_support", c_uint32 * 256), # Log Page Identifier Supported
    ]

class nvme_error_log_page(StructureBase):
    """
        Error Information Log Entry (Log Identifier 01h)
    """
    _fields_ = [
        ("error_count", c_uint64),      # Error Count: a 64-bit incrementing error count, indicating a unique identifier for this error. The error count starts at %1h, is incremented for each unique error
                                        # log entry, and is retained across power off conditions.  A value of %0h indicates an invalid entry; this value is used when there are lost entries or when there are
                                        # fewer errors than the maximum number of entries the controller supports. If the value of this field is %FFFFFFFFh, then the field shall be set to 1h when incremented
                                        #  (i.e., rolls over to %1h). Prior to NVMe 1.4, processing of incrementing beyond %FFFFFFFFh is unspecified.
        ("sqid", c_uint16),             # Submission Queue ID: indicates the Submission Queue Identifier of the command that the error information is associated with. If the error is not specific to
                                        # a particular command, then this field shall be set to %FFFFh.
        ("cmdid", c_uint16),            # Command ID: indicates the Command Identifier of the command that the error is associated with. If the error is not specific to a particular command, then this field
                                        # shall be set to %FFFFh.
        ("status_field", c_uint16),     # Bits 15-1: Status Field: indicates the Status Field for the command that completed. If the error is not specific to a particular command, then this field reports the
                                        # most applicable status value. Bit 0: Phase Tag: may indicate the Phase Tag posted for the command.
        ("parm_error_location", c_uint16), #  Parameter Error Location: indicates the byte and bit of  the command parameter that the error is associated with, if applicable. If the parameter spans multiple
                                        # bytes or  bits, then the location indicates the first byte and bit of the parameter. Bits 10-8: Bit in command that contained the error. Valid values are 0 to 7.
                                        # Bits 7-0: Byte in command that contained the error.  Valid values are 0 to 63.
        ("lba", c_uint64),              # LBA: This field indicates the first LBA that experienced the error condition, if applicable.
        ("nsid", c_uint32),             # Namespace: This field indicates the NSID of the namespace that the error is associated with, if applicable.
        ("vs", c_uint8),                # Vendor Specific Information Available: If there is additional vendor specific error information available, this field provides the log page identifier associated
                                        # with that page. A value of %0h indicates that no additional information is available. Valid values are in the range of %80h to %FFh.
        ("trtype", c_uint8),            # Transport Type (TRTYPE): indicates the Transport Type of the transport associated with the error. The values in this field are the same as the TRTYPE values
                                        # in the Discovery Log Page Entry. If the error is not transport related, this field shall be cleared to %0h. If the error is transport related, this field shall
                                        # be set to the type of the transport - see &enum nvme_trtype.
        ("csi", c_uint8),               # Command Set Indicator: This field contains command set indicator for the command that the error is associated  with.
        ("opcode", c_uint8),            # This field contains opcode for the command that the error is associated with.
        ("cs", c_uint64),               # Command Specific Information: This field contains command specific information. If used, the command definition specifies the information returned.
        ("trtype_spec_info", c_uint16), # Transport Type Specific Information
        ("rsvd", c_uint8 * 21),         # Reserved
        ("log_page_version", c_uint8),  # This field shall be set to 1h. If set, @csi and @opcode  will have valid values.
    ]

class NVME_ERR_PEL(Enum):
    NVME_ERR_PEL_BYTE_MASK = 0xf
    NVME_ERR_PEL_BIT_MASK = 0x70


class nvme_smart_log(StructureBase):
    """
        SMART / Health Information Log (Log Identifier 02h)
    """
    _fields_ = [
        ('critical_warning', c_uint8),              # This field indicates critical warnings for the state of the controller. Critical warnings may result in an asynchronous event notification to the host. Bits in
                                                    # this field represent the current associated state and are not persistent (see &enum nvme_smart_crit).
        ('temperature', c_uint8 * 2),               # Composite Temperature: Contains a value corresponding to a temperature in Kelvins that represents the current composite temperature of the controller and namespace(s)
                                                    # associated with that controller. The manner in which this value is computed is implementation specific and  may not represent the actual temperature of any physical
                                                    # point in the NVM subsystem. Warning and critical overheating composite temperature threshold values are reported by the WCTEMP and CCTEMP fields in the Identify
                                                    # Controller data structure.
        ('avail_spare', c_uint8),                   # Available Spare: Contains a normalized percentage (0% to 100%) of the remaining spare capacity available.
        ('spare_thresh', c_uint8),                  # Available Spare Threshold: When the Available Spare falls below the threshold indicated in this field, an asynchronous event completion may occur. The value is
                                                    #  indicated as a normalized percentage (0% to 100%). The values 101 to 255 are reserved.
        ('percent_used', c_uint8),                  # Percentage Used: Contains a vendor specific estimate of the percentage of NVM subsystem life used based on the actual usage and the manufacturer's prediction of
                                                    # NVM life. A value of 100 indicates that the estimated endurance of the NVM in the NVM subsystem has been consumed, but may not indicate an NVM subsystem failure.
                                                    # The value is allowed to exceed 100. Percentages greater than 254 shall be represented as 255. This value shall be updated once per power-on hour (when the controller
                                                    # is not in a sleep state).
        ('endu_grp_crit_warn_sumry', c_uint8),      #  Endurance Group Critical Warning Summary: This field  indicates critical warnings for the state of Endurance Groups. Bits in this field represent the current associated
                                                    #  state and are not persistent (see &enum nvme_smart_egcw).
        ('rsvd7', c_uint8 * 25),                    # Reserved
        ('data_units_read', c_uint8 * 16),          #  Data Units Read: Contains the number of 512 byte data units read from the controller; this value  does not include metadata. This value is reported in
                                                    #  thousands (i.e., a value of 1 corresponds to 1000 units of 512 bytes read) and is rounded up (e.g., one indicates the that number of 512 byte data units read
                                                    # is from 1 to 1000, three indicates that the number of  512 byte data units read is from 2001 to 3000). When the LBA size is a value other than 512 bytes, the
                                                    # controller shall convert the amount of data read to 512 byte units. For the NVM command set, logical blocks read as part of Compare, Read, and Verify operations
                                                    # shall be included in this value. A value of %0h in this field indicates that the number of Data Units Read is not reported.
        ('data_units_written', c_uint8 * 16),       # Data Units Read: Contains the number of 512 byte data units the host has read from the controller; this value does not include metadata. This value is
                                                    # reported in thousands (i.e., a value of 1 corresponds to 1000 units of 512 bytes written) and is rounded up (e.g., one indicates that the number of 512
                                                    # byte data units written is from 1 to 1,000, three indicates that the number of 512 byte data units written is from 2001 to 3000). When the LBA size is a value other than 512 bytes,
                                                    # the controller shall convert the amount of data written to 512 byte units. For the NVM command set, logical blocks written as part of Write operations shall be included in this value.
                                                    # Write Uncorrectable commands and Write Zeroes commands shall not impact this value. A value of %0h in this field indicates that the number of Data Units Written is not reported.
        ('host_reads', c_uint8 * 16),               # Host Reads: Contains the number of read commands completed by the controller. For the NVM command set, this value is the sum of the number of Compare commands and
                                                    # the number of Read commands.
        ('host_writes', c_uint8 * 16),              # Host Writes: Contains the number of write commands completed by the controller. For the NVM command set, this is the number of Write commands.
        ('ctrl_busy_time', c_uint8 * 16),           # Controller Busy Time: Contains the amount of time the controller is busy with I/O commands. The controller is busy when there is a command outstanding to an I/O
                                                    # Queue (specifically, a command was issued via an I/O Submission Queue Tail doorbell write and the corresponding completion queue entry has not been posted yet to the
                                                    # associated I/O Completion Queue). This value is reported in minutes.
        ('power_cycles', c_uint8 * 16),             # Power Cycles: Contains the number of power cycles.
        ('power_on_hours', c_uint8 * 16),           # Power On Hours: Contains the number of power-on hours. This may not include time that the controller was powered and in a non-operational power state.
        ('unsafe_shutdowns', c_uint8 * 16),         # Unsafe Shutdowns: Contains the number of unsafe shutdowns. This count is incremented when a Shutdown Notification (CC.SHN) is not received prior to loss of power.
        ('media_errors', c_uint8 * 16),             # Media and Data Integrity Errors: Contains the number of occurrences where the controller detected an unrecovered data integrity error. Errors such as
                                                    # uncorrectable ECC, CRC checksum failure, or LBA tag mismatch are included in this field. Errors introduced as a result of a Write Uncorrectable command may or
                                                    # may not be included in this field.
        ('num_err_log_entries', c_uint8 * 16),      # Number of Error Information Log Entries: Contains the number of Error Information log entries over the life of the controller.
        ('warning_temp_time', c_uint32),            # Warning Composite Temperature Time: Contains the amount of time in minutes that the controller is operational and the Composite Temperature is greater than or equal
                                                    # to the Warning Composite Temperature Threshold (WCTEMP) field and less than the Critical Composite Temperature Threshold (CCTEMP) field in the Identify Controller
                                                    # data structure. If the value of the WCTEMP or CCTEMP field is %0h, then this field is always cleared to %0h regardless of the Composite Temperature value.
        ('critical_comp_time', c_uint32),           # Critical Composite Temperature Time: Contains the amount of time in minutes that the controller is operational and the Composite Temperature is greater than or equal
                                                    # to the Critical Composite Temperature Threshold (CCTEMP) field in the Identify Controller data structure. If  the value of the CCTEMP field is %0h, then this field
                                                    # is always cleared to %0h regardless of the Composite Temperature value.
        ('temp_sensor', c_uint16 * 8),              #Temperature Sensor 1-8: Contains the current temperature in degrees Kelvin reported by temperature sensors 1-8. The physical point in the NVM subsystem whose temperature
                                                    # is reported by the temperature sensor and the temperature accuracy is implementation specific. An implementation that does not implement the temperature sensor reports
                                                    # a value of %0h.
        ('thm_temp1_trans_count', c_uint32),        # Thermal Management Temperature 1 Transition Count: Contains the number of times the controller transitioned to lower power active power states or performed vendor
                                                    # specific thermal management actions while minimizing the impact on performance in order to attempt to reduce the Composite Temperature because of the host controlled
                                                    # thermal management feature (i.e., the Composite Temperature rose above the Thermal Management Temperature 1). This counter shall not wrap once the value %FFFFFFFFh
                                                    # is reached. A value of %0h, indicates that this transition has never occurred or this field is not implemented.
        ('thm_temp2_trans_count', c_uint32),        # Thermal Management Temperature 2 Transition Count
        ('thm_temp1_total_time', c_uint32),         # Total Time For Thermal Management Temperature 1: Contains the number of seconds that the controller had transitioned to lower power active power states or
                                                    # performed vendor specific thermal management actions while minimizing the impact on performance in order to attempt to reduce the Composite Temperature because of
                                                    #  the host controlled thermal management feature. This counter shall not wrap once the value %FFFFFFFFh is  reached. A value of %0h, indicates that this transition
                                                    #  has never occurred or this field is not implemented.
        ('thm_temp2_total_time', c_uint32),         # Total Time For Thermal Management Temperature 2
        ('rsvd232', c_uint8 * 280),                 # Reserved
    ]

class NVME_SMART_CRIT(Enum):
    """
        Critical Warning
    """
    NVME_SMART_CRIT_SPARE = 1 << 0          # If set, then the available spare capacity has fallen below the threshold.
    NVME_SMART_CRIT_TEMPERATURE = 1 << 1    # If set, then a temperature is either greater than or equal to an over temperature threshold; or less than or equal to an under temperature threshold.
    NVME_SMART_CRIT_DEGRADED = 1 << 2       # If set, then the NVM subsystem reliability has been degraded due to significant media related errors or any internal error that degrades NVM subsystem reliability.
    NVME_SMART_CRIT_MEDIA = 1 << 3          # If set, then all of the media has been placed in read only mode. The controller shall not set this bit if the read-only condition on the media is a result of
                                            # a change in the write protection state of a namespace.
    NVME_SMART_CRIT_VOLATILE_MEMORY = 1 << 4# If set, then the volatile memory backup device has failed. This field is only valid if the controller has a volatile memory backup solution.
    NVME_SMART_CRIT_PMR_RO = 1 << 5         # If set, then the Persistent Memory Region has become read-only or unreliable.

class NVME_SMART_EGCW(Enum):
    """
        Endurance Group Critical Warning Summary
    """
    NVME_SMART_EGCW_SPARE = 1 << 0              # If set, then the available spare capacity of one or more Endurance Groups has fallen below the threshold.
    NVME_SMART_EGCW_DEGRADED = 1 << 2           # If set, then the reliability of one or more Endurance Groups has been degraded due to significant media related errors or any internal error that degrades NVM subsystem reliability.
    NVME_SMART_EGCW_RO = 1 << 3                 # If set, then the namespaces in one or more Endurance Groups have been placed in read only mode not as a result of a change in the write protection state of a namespace.

class nvme_firmware_log(StructureBase):
    """
        Firmware Slot Information Log
    """
    _fields_ = [
        ('afi', c_uint8),               # Active Firmware Info: Indicates the currently active firmware slot. The value of this field shall be %0h, %1h, %2h, or %3h. If the value is %0h, then the first firmware slot is active. If the value is %1h, then the second firmware slot is active. If the value is%2h, then the third firmware slot is active. If the value
        ('rsvd1', c_uint8 * 7),         # Reserved
        ('frs1', c_char * 8),           # Firmware Revision for Slot: Contains the firmware revision for the firmware slot.
        ('frs2', c_char * 8),           # Firmware Revision for Slot: Contains the firmware revision for the firmware slot.
        ('frs3', c_char * 8),           # Firmware Revision for Slot: Contains the firmware revision for the firmware slot.
        ('frs4', c_char * 8),           # Firmware Revision for Slot: Contains the firmware revision for the firmware slot.
        ('frs5', c_char * 8),           # Firmware Revision for Slot: Contains the firmware revision for the firmware slot.
        ('frs6', c_char * 8),           # Firmware Revision for Slot: Contains the firmware revision for the firmware slot.
        ('frs7', c_char * 8),           # Firmware Revision for Slot: Contains the firmware revision for the firmware slot.
        ('rsvd2', c_uint8 * 448),       # Reserved
    ]

class nvme_cmd_effects_log(StructureBase):
    """
        Commands Supported and Effects Log
    """
    _fields_ = [
        ('acs', c_uint32 * 256),        # Admin Command Supported
        ('iocs', c_uint32 * 256),       # I/O Command Supported
        ('rsvd', c_uint8 * 2048),       # Reserved
    ]

class nvme_cmd_effects_log_entry(StructureBase):
    """
    This class represents the data structure for the NVMe Command Effects Log, which describes the effects of commands on the controller and namespace states.
    """
    _fields_ = [
        ('csupp', c_uint32, 1),             # Indicates whether the command supports the Controller State Update feature.
        ('lbcc', c_uint32, 1),              # Indicates whether the command causes a Logical Block Content Change.
        ('ncc', c_uint32, 1),               # Indicates whether the command causes a Namespace Capacity Change.
        ('nic', c_uint32, 1),               # Indicates whether the command causes a Namespace Identifier Change.
        ('ccc', c_uint32, 1),               # Indicates whether the command causes a Controller Configuration Change.
        ('rsvd', c_uint32, 9),              # Reserved for future use.
        ('cser', c_uint32, 2),              # Indicates the Command State Enable Register value.
        ('cse', c_uint32, 3),               # Indicates the Command State Enable value.
        ('csp', c_uint32, 12),              # Indicates the Command State Parameter value.
    ]

class nvme_self_test_res(StructureBase):
    """
        NVMe Self-Test Result Structure.
        This structure contains the result of an NVMe device self-test, including various status and error information.
    """
    _fields_ = [
        ('dsts', c_uint8),              # Device Self-test Status: Indicates the device self-test code and the status of the operation (see &enum nvme_status_result and &enum nvme_st_code).
        ('seg', c_uint8),               # Segment Number: Iindicates the segment number where the first self-test failure occurred. If Device Self-test Status (@dsts) is not set to NVME_ST_RESULT_KNOWN_SEG_FAIL, then this field should be ignored.
        ('vdi', c_uint8),               # Valid Diagnostic Information: Indicates the diagnostic failure information that is reported. See &enum nvme_st_valid_diag_info.
        ('rsvd', c_uint8),              # Reserved
        ('poh', c_uint64),              # Power On Hours (POH): Indicates the number of power-on hours at the time the device self-test operation was completed or aborted. This does not include time that the controller was powered and in a low power state condition.
        ('nsid', c_uint32),             # Namespace Identifier (NSID): Indicates the namespace that the Failing LBA occurred on. Valid only when the NSID Valid bit  (#NVME_ST_VALID_DIAG_INFO_NSID) is set in the Valid Diagnostic  Information (@vdi) field.
        ('flba', c_uint64),             # Failing LBA: indicates the LBA of the logical block that caused the test to fail. If the device encountered more than one failed logical block during the test, then this field only indicates one of those
                                        # failed logical blocks. Valid only when the NSID Valid bit (#NVME_ST_VALID_DIAG_INFO_FLBA) is set in the Valid Diagnostic Information (@vdi) field.
        ('sct', c_uint8),               # Status Code Type: This field may contain additional information related to errors or conditions. Bits 2:0 may contain additional information relating to errors or conditions that occurred during the device
                                        # self-test operation represented in the same format used in the Status Code Type field of the completion queue entry (refer to &enum nvme_status_field). Valid only when the NSID Valid bit (#NVME_ST_VALID_DIAG_INFO_SCT) is
                                        # set in the Valid Diagnostic Information (@vdi) field.
        ('sc', c_uint8),                # Status Code: This field may contain additional information relating to errors or conditions that occurred during the device self-test operation represented in the same format used in the Status Code field
                                        # of the completion queue entry. Valid only when the NSID Valid bit (#NVME_ST_VALID_DIAG_INFO_SC) is set in the Valid Diagnostic Information (@vdi) field.
        ('vs', c_uint8 * 2),            # Vendor Specific.
    ]

class NVME_ST_RESULT(Enum):
    """
        Result of the device self-test operation
    """
    NVME_ST_RESULT_NO_ERR		= 0x0               # Operation completed without error.
    NVME_ST_RESULT_ABORTED		= 0x1               # Operation was aborted by a Device Self-test command.
    NVME_ST_RESULT_CLR		= 0x2                   # Operation was aborted by a Controller Level Reset.
    NVME_ST_RESULT_NS_REMOVED	= 0x3               # Operation was aborted due to a removal of a namespace from the namespace inventory.
    NVME_ST_RESULT_ABORTED_FORMAT	= 0x4           # Operation was aborted due to the processing of a Format NVM command.
    NVME_ST_RESULT_FATAL_ERR	= 0x5               # A fatal error or unknown test error occurred while the controller was executing the device self-test operation and the operation did
                                                    # not complete.
    NVME_ST_RESULT_UNKNOWN_SEG_FAIL	= 0x6           # Operation completed with a segment that failed and the segment that failed is not known.
    NVME_ST_RESULT_KNOWN_SEG_FAIL	= 0x7           # Operation completed with one or more failed segments and the first segment that failed is indicated in the Segment Number field.
    NVME_ST_RESULT_ABORTED_UNKNOWN	= 0x8           # Operation was aborted for unknown reason.
    NVME_ST_RESULT_ABORTED_SANITIZE	= 0x9           # Operation was aborted due to a sanitize operation.
    NVME_ST_RESULT_NOT_USED		= 0xf               # Entry not used (does not contain a test result).
    NVME_ST_RESULT_MASK		= 0xf                   # Mask to get the status result value from the &struct nvme_st_result.dsts field.

class NVME_ST_CODE(Enum):
    """
        Self-test Code value
    """
    NVME_ST_CODE_RESERVED		= 0x0               # Reserved.
    NVME_ST_CODE_SHORT		= 0x1                   # Short device self-test operation.
    NVME_ST_CODE_EXTENDED		= 0x2               # Extended device self-test operation.
    NVME_ST_CODE_VS		= 0xe                       # Vendorspecific.
    NVME_ST_CODE_ABORT		= 0xf                   # Abort device self-test operation.
    NVME_ST_CODE_SHIFT		= 4                     # Shift amount to get the code value from the &struct nvme_st_result.dsts field.

class NVME_ST_CURR_OP(Enum):
    NVME_ST_CURR_OP_NOT_RUNNING	= 0x0                   # No device self-test operation in progress.
    NVME_ST_CURR_OP_SHORT		= 0x1                   # Short device self-test operation in progress.
    NVME_ST_CURR_OP_EXTENDED		= 0x2               # Extended device self-test operation in progress.
    NVME_ST_CURR_OP_VS		= 0xe                       # Vendor specific.
    NVME_ST_CURR_OP_RESERVED		= 0xf               # Reserved.
    NVME_ST_CURR_OP_MASK		= 0xf                   # Mask to get the current operation value from the &struct nvme_self_test_log.current_operation field.
    NVME_ST_CURR_OP_CMPL_MASK		= 0x7f              # Mask to get the current operation completion value from the &struct nvme_self_test_log.completion field.

class NVME_ST_VALID_DIAG_INFO(Enum):
    """
        Valid Diagnostic Information
    """
    NVME_ST_VALID_DIAG_INFO_NSID		= 1 << 0        # Namespace Identifier Valid: if set, then the contents of the Namespace Identifier field are valid.
    NVME_ST_VALID_DIAG_INFO_FLBA		= 1 << 1        # Failing LBA Valid: if set, then the contents of the Failing LBA field are valid.
    NVME_ST_VALID_DIAG_INFO_SCT		    = 1 << 2        # Status Code Type Valid: if set, then the contents of the Status Code Type field are valid.
    NVME_ST_VALID_DIAG_INFO_SC		    = 1 << 3        # Status Code Valid: if set, then the contents of the Status Code field are valid.

class nvme_self_test_log(StructureBase):
    """
        Device Self-test (Log Identifier 06h)
    """
    _fields_ = [
        ("current_operation", c_uint8),         # Current Device Self-Test Operation: indicates the status of the current device self-test operation. If a device self-test operation is in process (i.e., this field is set
                                                # to #NVME_ST_CURR_OP_SHORT or #NVME_ST_CURR_OP_EXTENDED), then the controller shall not set this field to #NVME_ST_CURR_OP_NOT_RUNNING until a new Self-test Result
                                                # Data Structure is created (i.e., if a device self-test operation completes or is aborted, then the controller shall create a Self-test Result Data Structure prior to
                                                # setting this field to #NVME_ST_CURR_OP_NOT_RUNNING). See &enum nvme_st_curr_op.
        ("completion", c_uint8),                # Current Device Self-Test Completion: indicates the percentage of the device self-test operation that is complete (e.g., a value of 25 indicates that 25% of the device self-test
                                                # operation is complete and 75% remains to be tested). If the @current_operation field is cleared to #NVME_ST_CURR_OP_NOT_RUNNING (indicating there is no device
                                                # self-test operation in progress), then this field is ignored.
        ("rsvd", c_uint8 * 2),                  # Reserved
        ("result", nvme_self_test_res * 20),    # Self-test Result Data Structures, see &struct nvme_st_result.
    ]

class NVME_CMD_GET_LOG_TELEMETRY_HOST_LSP(Enum):
    """
        Telemetry Host-Initiated log specific field
    """
    NVME_LOG_TELEM_HOST_LSP_RETAIN		= 0               # Get Telemetry Data Blocks
    NVME_LOG_TELEM_HOST_LSP_CREATE		= 1               # Create Telemetry Data Blocks

class nvme_telemetry_log(StructureBase):
    """
        Retrieve internal data specific to the manufacturer.
    """
    _fields_ = [
        ("lpi", c_uint8),                   # Log Identifier, either %NVME_LOG_LID_TELEMETRY_HOST or %NVME_LOG_LID_TELEMETRY_CTRL
        ("rsvd1", c_uint8 * 4),             # Reserved
        ("ieee", c_uint8 * 3),              # IEEE OUI Identifier is the Organization Unique Identifier (OUI) for the controller vendor that is able to interpret the data.
        ("dalb1", c_uint16),                # Telemetry Controller-Initiated Data Area 1 Last Block is the value of the last block in this area.
        ("dalb2", c_uint16),                # Telemetry Controller-Initiated Data Area 1 Last Block is the value of the last block in this area.
        ("dalb3", c_uint16),                # Telemetry Controller-Initiated Data Area 1 Last Block is the value of the last block in this area.
        ("rsvd14", c_uint8 * 2),            # Reserved
        ("dalb4", c_uint32),                # Telemetry Controller-Initiated Data Area 4 Last Block is  the value of the last block in this area.
        ("rsvd20", c_uint8 * 361),          # Reserved
        ("hostdgn", c_uint8),               # Telemetry Host-Initiated Data Generation Number is a value that is incremented each time the host initiates a capture of its internal controller state in the controller .
        ("ctrlavail", c_uint8),             # Telemetry Controller-Initiated Data Available, if cleared, then the controller telemetry log does not contain saved internal controller state. If this field is set to 1h, the
                                            # controller log contains saved internal controller state. If this field is set to 1h, the data will be latched until the host releases it by reading the log with RAE cleared.
        ("ctrldgn", c_uint8),               # Telemetry Controller-Initiated Data Generation Number is a value that is incremented each time the controller initiates a capture of its internal controller state in the controller .
        ("rsnident", c_uint8 * 128),        # Reason Identifiers a vendor specific identifier that describes the operating conditions of the controller at the time of  capture.
        # ("telemetry_dataarea", Pointer(c_uint8, "dalb3")),         # Telemetry data blocks, vendor specific information data.
    ]

class nvme_endurance_group_log(StructureBase):
    """
        Endurance Group Information Log
    """
    _fields_ = [
        ("critical_warning", c_uint8),                  # Critical Warning: indicates the current status of the controller.
        ("endurance_group_features", c_uint8),          # Endurance Group Features: indicates the current status of the endurance group.
        ("rsvd2", c_uint8),                             # Reserved
        ("avl_spare", c_uint8),                         # Available Spare: indicates the percentage of spare capacity remaining in the endurance group.
        ("avl_spare_threshold", c_uint8),               # Available Spare Threshold: indicates the percentage of spare capacity remaining in the endurance group that is considered to be low.
        ("percent_used", c_uint8),                      # Percentage Used: indicates the percentage of the endurance group that is currently used.
        ("domain_identifier", c_uint16),                # Domain Identifier: indicates the domain identifier of the endurance group.
        ("rsvd8", c_uint8 * 24),                        # Reserved
        ("endurance_estimate",c_uint8 * 16),            # Endurance Estimate: indicates the estimated number of data units that can be written to the endurance group before the endurance group is no longer guaranteed to maintain the endurance
        ("data_units_read", c_uint8 * 16),              # Data Units Read: indicates the number of data units read from the endurance group.
        ("data_units_written", c_uint8 * 16),           # Data Units Written: indicates the number of data units written to the endurance group.
        ("media_units_written", c_uint8 * 16),          # Media Units Written: indicates the number of media units written to the endurance group.
        ("host_read_cmds", c_uint8 * 16),               # Host Read Commands: indicates the number of host read commands issued to the endurance group.
        ("host_write_cmds", c_uint8 * 16),              # Host Write Commands: indicates the number of host write commands issued to the endurance group.
        ("media_data_integrity_err", c_uint8 * 16),     # Media and Data Integrity Errors: indicates the number of media and data integrity errors that have occurred on the endurance group.
        ("num_err_info_log_entries", c_uint8 * 16),     # Number of Error Information Log Entries:
        ("total_end_grp_cap", c_uint8 * 16),            # Total Endurance Group Capacity: indicates the total capacity of the endurance group.
        ("unalloc_end_grp_cap", c_uint8 * 16),          # Unallocated Endurance Group Capacity: indicates the amount of unallocated capacity in the endurance group.
        ("rsvd192", c_uint8 * 320),                     # Reserved
    ]

class NVME_EG_CRITICAL_WARNING_FLAGS(Enum):
    """
        Endurance Group Information Log - Critical Warning
    """
    NVME_EG_CRITICAL_WARNING_SPARE          = 0x1       # Available spare capacity of the Endurance Group has fallen below the threshold
    NVME_EG_CRITICAL_WARNING_DEGRADED       = 0x4       # Endurance Group reliability has been degraded
    NVME_EG_CRITICAL_WARNING_READ_ONLY      = 0x8       # Endurance Group has been placed in read only mode

class nvme_aggregate_endurance_group_event(StructureBase):
    """
        Endurance Group Event Aggregate
    """
    _fields_ = [
        ("num_entries", c_uint64),                      # Number or entries
        ("entries", Pointer(c_uint16, "num_entries")),                      # List of entries
    ]

class nvme_nvmset_predictable_lat_log(StructureBase):
    """
        Predictable Latency Mode - Deterministic Threshold Configuration Data
    """
    _fields_ = [
        ("status", c_uint8),                            # Status
        ("rsvd1", c_uint8),                             # Reserved
        ("event_type", c_uint16),                       # Event Type
        ("rsvd4", c_uint8 * 28),                        # Reserved
        ("dtwin_rt", c_uint64),                         # DTWIN Reads Typical
        ("dtwin_wt", c_uint64),                         # DTWIN Writes Typical
        ("dtwin_tmax", c_uint64),                       # DTWIN Time Maximum
        ("ndwin_tmin_hi", c_uint64),                    # NDWIN Time Minimum High
        ("ndwin_tmin_lo", c_uint64),                    # NDWIN Time Minimum Low
        ("rsvd72", c_uint8 * 56),                       # Reserved
        ("dtwin_re", c_uint64),                         # DTWIN Reads Estimate
        ("dtwin_we", c_uint64),                         # DTWIN Writes Estimate
        ("dtwin_te", c_uint64),                         # DTWIN Time Estimate
        ("rsvd152", c_uint8 * 360),                     # Reserved
    ]

class NVME_NVMESET_PL_STATUS(Enum):
    """
        Predictable Latency Per NVM Set Log - Status
    """
    NVME_NVMSET_PL_STATUS_DISABLED      = 0x0       # Not used (Predictable Latency Mode not enabled)
    NVME_NVMSET_PL_STATUS_DTWIN         = 0x1       # Deterministic Window (DTWIN)
    NVME_NVMSET_PL_STATUS_NDWIN         = 0x2       # Non-Deterministic Window (NDWIN)

class NVME_NVMSET_PL_EVENTS(Enum):
    """
        Predictable Latency Per NVM Set Log - Event Type
    """
    NVME_NVMSET_PL_EVENT_DTWIN_READ_WARN	= 1 << 0        # DTWIN Reads Warning
    NVME_NVMSET_PL_EVENT_DTWIN_WRITE_WARN	= 1 << 1        # DTWIN Writes Warning
    NVME_NVMSET_PL_EVENT_DTWIN_TIME_WARN	= 1 << 2        # DTWIN Time Warning
    NVME_NVMSET_PL_EVENT_DTWIN_EXCEEDED	    = 1 << 14       # Autonomous transition from DTWIN to NDWIN due to typical or maximum value exceeded
    NVME_NVMSET_PL_EVENT_DTWIN_EXCURSION	= 1 << 15       # Autonomous transition from DTWIN to NDWIN due to Deterministic Excursion

class nvme_aggregate_predictable_lat_event(StructureBase):
    """
        Predictable Latency Event Aggregate Log Page
    """
    _fields_ = [
        ("num_entries", c_uint64),                      # Number or entries
        ("entries", Pointer(c_uint16, "num_entries")),                      # List of entries
    ]

class nvme_ana_group_desc(StructureBase):
    """
        ANA Group Descriptor
    """
    _fields_ = [
        ("grpid", c_uint32),                            # ANA group id
        ("nnsids", c_uint32),                           # Number of namespaces in @nsids
        ("chgcnt", c_uint64),                           # Change counter
        ("state", c_uint8),                             # ANA state
        ("rsvd17", c_uint8 * 15),                       # Reserved
        ("nsids", Pointer(c_uint32, "nnsids")),                        # List of namespaces
    ]

class NVME_ANA_STATE(Enum):
    """
        Asymmetric Namespace Access State
    """
    NVME_ANA_STATE_OPTIMIZED        = 0x1       # ANA Optimized state
    NVME_ANA_STATE_NONOPTIMIZED     = 0x2       # ANA Non-Optimized state
    NVME_ANA_STATE_INACCESSIBLE     = 0x3       # ANA Inaccessible state
    NVME_ANA_STATE_PERSISTENT_LOSS  = 0x4       # ANA Persistent Loss state
    NVME_ANA_STATE_CHANGE           = 0xf       # ANA Change state

class nvme_ana_log(StructureBase):
    """
        Asymmetric Namespace Access Log
    """
    _fields_ = [
        ("chgcnt", c_uint64),                       # Change Count
        ("ngrps", c_uint16),                        # Number of ANA Group Descriptors
        ("rsvd10", c_uint8 * 6),                    # Reserved
        ("descs", Pointer(nvme_ana_group_desc, "ngrps")),         # ANA Group Descriptor
    ]

class nvme_persistent_event_log(StructureBase):
    """
        Persistent Event Log
    """
    _fields_ = [
        ("lid", c_uint8),                               # Log Identifier
        ("rsvd1", c_uint8 * 3),                         # Reserved
        ("tnev", c_uint32),                             # Total Number of Events
        ("tll", c_uint64),                              # Total Log Length
        ("rv", c_uint8),                                # Log Revision
        ("rsvd17", c_uint8),                            # Reserved
        ("lhl", c_uint16),                              # Log Header Length
        ("ts", c_uint64),                               # Timestamp
        ("poh", c_uint8 * 16),                          # Power on Hours
        ("pcc", c_uint64),                              # Power Cycle Count
        ("vid", c_uint16),                              # PCI Vendor ID
        ("ssvid", c_uint16),                            # PCI Subsystem Vendor ID
        ("sn", c_char * 20),                            # Serial Number
        ("mn", c_char * 40),                            # Model Number
        ("subnqn", c_char * 256),                       # NVM Subsystem NVMe Qualified Name
        ("gen_number", c_uint16),                       # Generation Number
        ("rci", c_uint32),                              # Reporting Context Information
        ("rsvd378", c_uint8 * 102),                     # Reserved
        ("seb", c_uint8 * 32),                          # Supported Events Bitmap
    ]

class nvme_persistent_event_entry(StructureBase):
    """
        Persistent Event
    """
    _fields_ = [
        ("etype", c_uint8),                             # Event Type
        ("etype_rev", c_uint8),                         # Event Type Revision
        ("ehl", c_uint8),                               # Event Header Length
        ("ehai", c_uint8),                              # Event Header Additional Info
        ("cntlid", c_uint16),                           # Controller Identifier
        ("ets", c_uint64),                              # Event Timestamp
        ("pelpid", c_uint16),                           # Port Identifier
        ("rsvd16", c_uint8 * 4),                        # Reserved
        ("vsil", c_uint16),                             # Vendor Specific Information Length
        ("el", c_uint16),                               # Event Length
    ]

class NVME_PERSISTENT_EVENT_TYPES(Enum):
    """
        Persistent event log events
    """
    NVME_PEL_SMART_HEALTH_EVENT         = 0x01      # SMART / Health Log Snapshot Event
    NVME_PEL_FW_COMMIT_EVENT            = 0x02      # Firmware Commit Event
    NVME_PEL_TIMESTAMP_EVENT            = 0x03      # Timestamp Change Event
    NVME_PEL_POWER_ON_RESET_EVENT       = 0x04      # Power-on or ResetEvent
    NVME_PEL_NSS_HW_ERROR_EVENT         = 0x05      # NVM Subsystem Hardware Error Event
    NVME_PEL_CHANGE_NS_EVENT            = 0x06      # Change Namespace Event
    NVME_PEL_FORMAT_START_EVENT         = 0x07      # Format NVM Start Event
    NVME_PEL_FORMAT_COMPLETION_EVENT    = 0x08      # Format NVM Completion Event
    NVME_PEL_SANITIZE_START_EVENT       = 0x09      # Sanitize Start Event
    NVME_PEL_SANITIZE_COMPLETION_EVENT  = 0x0a      # Sanitize Completion Event
    NVME_PEL_SET_FEATURE_EVENT          = 0x0b      # Set Feature Event
    NVME_PEL_TELEMETRY_CRT              = 0x0c      # Telemetry Log Create Event
    NVME_PEL_THERMAL_EXCURSION_EVENT    = 0x0d      # Thermal Excursion Event

class nvme_fw_commit_event(StructureBase):
    """
        Firmware Commit Event Data
    """
    _fields_ = [
        ("old_fw_rev", c_uint64),                       # Old Firmware Revision
        ("new_fw_rev", c_uint64),                       # New Firmware Revision
        ("fw_commit_action", c_uint8),                  # Firmware Commit Action
        ("fw_slot", c_uint8),                           # Firmware Slot
        ("sct_fw", c_uint8),                            # Status Code Type for Firmware Commit Command
        ("sc_fw", c_uint8),                             # Status Returned for Firmware Commit Command
        ("vndr_assign_fw_commit_rc", c_uint16),         # Vendor Assigned Firmware Commit Result Code
    ]

class nvme_timestamp(StructureBase):
    """
        Data Structure for Get Features
    """
    _fields_ = [
        ("timestamp", c_uint8 * 6),                     # Timestamp value based on origin and synch field
        ("attr", c_uint8),                              # Attribute
        ("rsvd", c_uint8),                              # Reserved
    ]

class nvme_time_stamp_change_event(StructureBase):
    """
        Timestamp Change Event
    """
    _fields_ = [
        ("previous_timestamp", c_uint64),               # Previous Timestamp
        ("ml_secs_since_reset", c_uint64),              # Milliseconds Since Reset
    ]

class nvme_power_on_reset_info_list(StructureBase):
    """
        Controller Reset Information
    """
    _fields_ = [
        ("cid", c_uint16),                              # Controller ID
        ("fw_act", c_uint8),                            # Firmware Activation
        ("op_in_prog", c_uint8),                        # Operation in Progress
        ("rsvd4", c_uint8 * 12),                        # Reserved
        ("ctrl_power_cycle", c_uint32),                 # Controller Power Cycle
        ("power_on_ml_seconds", c_uint64),              # Power on milliseconds
        ("ctrl_time_stamp", c_uint64),                  # Controller Timestamp
    ]

class nvme_nss_hw_err_event(StructureBase):
    """
        NVM Subsystem Hardware Error Event
    """
    _fields_ = [
        ("nss_hw_err_event_code", c_uint16),            # NVM Subsystem Hardware Error Event Code
        ("rsvd2", c_uint8 * 2),                         # Reserved
        ("add_hw_err_info", Pointer(c_uint8, "nss_hw_err_event_code")),          # Additional Hardware Error Information
    ]

class nvme_change_ns_event(StructureBase):
    """
        Change Namespace Event Data
    """
    _fields_ = [
        ("nsmgt_cdw10", c_uint32),                      # Namespace Management CDW10
        ("rsvd4", c_uint8 * 4),                         # Reserved
        ("nsze", c_uint64),                             # Namespace Size
        ("rsvd16", c_uint8 * 8),                        # Reserved
        ("nscap", c_uint64),                            # Namespace Capacity
        ("flbas", c_uint8),                             #Formatted LBA Size
        ("dps", c_uint8),                               # End-to-end Data Protection Type Settings
        ("nmic", c_uint8),                              # Namespace Multi-path I/O and Namespace Sharing Capabilities
        ("rsvd35", c_uint8),                            # Reserved
        ("ana_grp_id", c_uint32),                       # ANA Group Identifier
        ("nvmset_id", c_uint16),                        # NVM Set Identifier
        ("rsvd42", c_uint16),                           # Reserved
        ("nsid", c_uint32),                             # Namespace ID
    ]

class nvme_format_nvm_start_event(StructureBase):
    """
        Format NVM Start Event Data
    """
    _fields_ = [
        ("nsid", c_uint32),                             # Namespace Identifier
        ("fna", c_uint8),                               # Format NVM Attributes
        ("rsvd5", c_uint8 * 3),                         # Reserved
        ("format_nvm_cdw10", c_uint32),                 # Format NVM CDW10
    ]

class nvme_format_nvm_compln_event(StructureBase):
    """
        Format NVM Completion Event Data
    """
    _fields_ = [
        ("nsid", c_uint32),                             # Namespace Identifier
        ("smallest_fpi", c_uint8),                      # Smallest Format Progress Indicator
        ("format_nvm_status", c_uint8),                 # Format NVM Status
        ("compln_info", c_uint16),                      # Completion Information
        ("status_field", c_uint32),                     # Status Field
    ]

class nvme_sanitize_start_event(StructureBase):
    """
        Sanitize Start Event Data
    """
    _fields_ = [
        ("sani_cap", c_uint32),                         # SANICAP
        ("sani_cdw10", c_uint32),                       # Sanitize CDW10
        ("sani_cdw11", c_uint32),                       # Sanitize CDW11
    ]


class nvme_sanitize_compln_event(StructureBase):
    """
        Sanitize Completion Event Data
    """
    _fields_ = [
        ("sani_prog", c_uint16),                        # Sanitize Progress
        ("sani_status", c_uint16),                      # Sanitize Status
        ("cmpln_info", c_uint16),                       # Completion Information
        ("rsvd6", c_uint8 * 2),                         # Reserved
    ]


class nvme_set_feature_event(StructureBase):
    """
        Set Feature Event Data
    """
    _fields_ = [
        ("layout", c_uint32),                           # Set Feature Event Layout
        ("cdw_mem", Pointer(c_uint32, "layout")),                 # Command Dwords Memory buffer
    ]

class nvme_thermal_exc_event(StructureBase):
    """
        Thermal Excursion Event Data
    """
    _fields_ = [
        ("over_temp", c_uint8),                         # Over Temperature
        ("threshold", c_uint8),                         # Temperature Threshold
    ]

class nvme_lba_rd(StructureBase):
    """
        LBA Range Descriptor
    """
    _fields_ = [
        ("rslba", c_uint64),                            # Range Starting LBA
        ("rnlb", c_uint32),                             # Range Number of Logical Blocks
        ("rsvd12", c_uint8 * 4),                        # Reserved
    ]

class nvme_lbas_ns_element(StructureBase):
    """
        LBA Status Log Namespace Element
    """
    _fields_ = [
        ("neid", c_uint32),                             # Namespace Element Identifier
        ("nlrd", c_uint32),                             # Number of LBA Range Descriptors
        ("ratype", c_uint8),                            # Recommended Action Type
        ("rsvd8", c_uint8 * 7),                         # Reserved
        ("lba_rd", Pointer(nvme_lba_rd, "nlrd")),                    # LBA Range Descriptor
    ]

class NVME_LBA_STATUS_ATYPE(Enum):
    """
        Potentially Unrecoverable LBAs
    """
    NVME_LBA_STATUS_ATYPE_SCAN_UNTRACKED = 0x10             # Potentially Unrecoverable LBAs
    NVME_LBA_STATUS_ATYPE_SCAN_TRACKED = 0x11               # Potentially Unrecoverable LBAs associated with physical storage

class nvme_lba_status_log(StructureBase):
    """
        LBA Status Information Log
    """
    _fields_ = [
        ("lslplen", c_uint32),                          # LBA Status Log Page Length
        ("nlslne", c_uint32),                           # Number of LBA Status Log Namespace Elements
        ("estulb", c_uint32),                           # Estimate of Unrecoverable Logical Blocks
        ("rsvd12", c_uint8 * 2),                        # Reserved
        ("lsgc", c_uint16),                             # LBA Status Generation Counter
        ("elements", Pointer(nvme_lbas_ns_element, "nlslne")),         # LBA Status Log Namespace Element List
    ]

class nvme_eg_event_aggregate_log(StructureBase):
    """
        Endurance Group Event Aggregate
    """
    _fields_ = [
        ("nr_entries", c_uint64),                       # Number of Entries
        ("egids", Pointer(c_uint16, "nr_entries")),                        # Endurance Group Identifier
    ]

class NVME_FID_SUPPORTED_EFFECTS(Enum):
    """
        FID Supported and Effects Data Structure definitions
    """
    NVME_FID_SUPPORTED_EFFECTS_FSUPP = 1 << 0           # FID Supported
    NVME_FID_SUPPORTED_EFFECTS_UDCC = 1 << 1            # User Data Content Change
    NVME_FID_SUPPORTED_EFFECTS_NCC = 1 << 2             # Namespace Capability Change
    NVME_FID_SUPPORTED_EFFECTS_NIC = 1 << 3             # Namespace Inventory Change
    NVME_FID_SUPPORTED_EFFECTS_CCC = 1 << 4             # Controller Capability Change
    NVME_FID_SUPPORTED_EFFECTS_UUID_SEL = 1 << 19       # UUID Selection Supported
    NVME_FID_SUPPORTED_EFFECTS_SCOPE_SHIFT = 20         # FID Scope Shift
    NVME_FID_SUPPORTED_EFFECTS_SCOPE_MASK = 0xfff       # FID Scope Mask
    NVME_FID_SUPPORTED_EFFECTS_SCOPE_NS = 1 << 0        # Namespace Scope
    NVME_FID_SUPPORTED_EFFECTS_SCOPE_CTRL = 1 << 1      # Controller Scope
    NVME_FID_SUPPORTED_EFFECTS_SCOPE_NVM_SET = 1 << 2   # NVM Set Scope
    NVME_FID_SUPPORTED_EFFECTS_SCOPE_ENDGRP = 1 << 3    # Endurance Group Scope
    NVME_FID_SUPPORTED_EFFECTS_SCOPE_DOMAIN = 1 << 4    # Domain Scope
    NVME_FID_SUPPORTED_EFFECTS_SCOPE_NSS = 1 << 5       # NVM Subsystem Scope

class nvme_fid_supported_effects_log(StructureBase):
    """
        Feature Identifiers Supported and Effects
    """
    _fields_ = [
        ("fid_support", c_uint32 * 256),                  # Feature Identifier Supported
    ]

class NVME_MI_CMD_SUPPORTED_EFFECTS(Enum):
    """
        MI Command Supported and Effects Data Structure
    """
    NVME_MI_CMD_SUPPORTED_EFFECTS_CSUPP = 1 << 0           # Command Supported
    NVME_MI_CMD_SUPPORTED_EFFECTS_UDCC = 1 << 1            # User Data Content Change
    NVME_MI_CMD_SUPPORTED_EFFECTS_NCC = 1 << 2             # Namespace Capability Change
    NVME_MI_CMD_SUPPORTED_EFFECTS_NIC= 1 << 3              # Namespace Inventory Change
    NVME_MI_CMD_SUPPORTED_EFFECTS_CCC = 1 << 4             # Controller Capability Change
    NVME_MI_CMD_SUPPORTED_EFFECTS_SCOPE_SHIFT = 20         # FID Scope Shift
    NVME_MI_CMD_SUPPORTED_EFFECTS_SCOPE_MASK = 0xfff       #  # FID Scope Mask
    NVME_MI_CMD_SUPPORTED_EFFECTS_SCOPE_NS = 1 << 0        # Namespace Scope
    NVME_MI_CMD_SUPPORTED_EFFECTS_SCOPE_CTRL = 1 << 1      # Controller Scope
    NVME_MI_CMD_SUPPORTED_EFFECTS_SCOPE_NVM_SET = 1 << 2   # NVM Set Scope
    NVME_MI_CMD_SUPPORTED_EFFECTS_SCOPE_ENDGRP = 1 << 3    # Endurance Group Scope
    NVME_MI_CMD_SUPPORTED_EFFECTS_SCOPE_DOMAIN = 1 << 4    # Domain Scope
    NVME_MI_CMD_SUPPORTED_EFFECTS_SCOPE_NSS = 1 << 5       # NVM Subsystem Scope

class nvme_mi_cmd_supported_effects_log(StructureBase):
    """
        NVMe-MI Commands Supported and Effects Log
    """
    _fields_ = [
        ("mi_cmd_support", c_uint32 * 256),                  # NVMe-MI Commands Supported
        ("reserved1", c_uint32 * 768),                       # Reserved
    ]

class nvme_boot_partition(StructureBase):
    """
        Boot Partition Log
    """
    _fields_ = [
        ("lid", c_uint8),                               # Boot Partition Identifier
        ("rsvd1", c_uint8 * 3),                         # Reserved
        ("bpinfo", c_uint32),                           # Boot Partition Information
        ("rsvd8", c_uint8 * 8),                         # Reserved
        ("boot_partition_data", Pointer(c_uint8, "lid")),           # Contains the contents of the specified Boot Partition
    ]

class nvme_eom_lane_desc(StructureBase):
    _fields_ = [
        ("rsvd0", c_uint8),                               # Reserved
        ("mstatus", c_uint8),                             # Measurement Status
        ("lane", c_uint8),                                # Lane number
        ("eye", c_uint8),                                 # Eye number
        ("top", c_uint16),                                # Absolute number of rows from center to top edge of eye
        ("bottom", c_uint16),                             # Absolute number of rows from center to bottomedge of eye
        ("left", c_uint16),                               # Absolute number of rows from center to left edge of eye
        ("right", c_uint16),                              # Absolute number of rows from center to right edge of eye
        ("nrows", c_uint16),                              # Number of Rows
        ("ncols", c_uint16),                              # Number of Columns
        ("edlen", c_uint16),                              # Eye Data Length
        ("rsvd18", c_uint8 * 14),                         # Reserved
        ("eye_desc", Pointer(c_uint8, "eye")),                        # Contains the contents of the specified Eye
    ]

class nvme_phy_rx_eom_log(StructureBase):
    """
        Physical Interface Receiver Eye Opening Measurement Log
    """
    _fields_ = [
        ("lid", c_uint8),                               # Log Identifier
        ("eomip", c_uint8),                             # EOM In Progress
        ("hsize", c_uint16),                            # Header Size
        ("rsize", c_uint32),                            # Result Size
        ("eomdgn", c_uint8),                            # EOM Data Generation Number
        ("lr", c_uint8),                                # Log Revision
        ("odp",c_uint8),                                # Optional Data Present
        ("lanes", c_uint8),                             # Number of lanes configured for this port
        ("epl", c_uint8),                               # Eyes Per Lane
        ("lspfc", c_uint8),                             # Log Specific Parameter Field Copy
        ("li", c_uint8),                                # Link Information
        ("rsvd15", c_uint8 * 3),                        # Reserved
        ("lsic", c_uint16),                             # Log Specific Identifier Copy
        ("dsize", c_uint32),                            # Descriptor Size
        ("nd", c_uint16),                               # Number of Descriptors
        ("maxtb", c_uint16),                            # Maximum Top Bottom
        ("maxlr", c_uint16),                            # Maximum Left Right
        ("etgood", c_uint16),                           # Estimated Time for Good Quality
        ("etbetter", c_uint16),                         # Estimated Time for Better Quality
        ("etbest", c_uint16),                           # Estimated Time for Best Quality
        ("rsvd36", c_uint8 * 28),                       # Reserved
        ("descs", Pointer(nvme_eom_lane_desc, "nd")),              # Contains the contents of the specified Eye
    ]

class NVME_EOM_OPTIONAL_DATA(Enum):
    """
        EOM Optional Data Present Fields
    """
    NVME_EOM_EYE_DATA_PRESENT = 1                       # Eye Data Present
    NVME_EOM_PRINTABLE_EYE_PRESENT = 1 << 1             # Printable Eye Present

class NVME_PHY_RX_EOM_PROGRESS(Enum):
    """
        EOM In Progress Values
    """
    NVME_PHY_RX_EOM_NOT_STARTED = 0                     # EOM Not Started
    NVME_PHY_RX_EOM_IN_PROGRESS = 1                     # EOM In Progress
    NVME_PHY_RX_EOM_COMPLETED = 2                       # EOM Completed

class nvme_media_unit_stat_desc(StructureBase):
    """
        Media Unit Status Descriptor
    """
    _fields_ = [
        ("muid", c_uint16),                             # Media Unit Identifier
        ("domainid", c_uint16),                         # Domain Identifier
        ("endgid", c_uint16),                           # Endurance Group Identifier
        ("nvmsetid", c_uint16),                         # NVM Set Identifier
        ("cap_adj_fctr", c_uint16),                     # Capacity Adjustment Factor
        ("avl_spare", c_uint8),                         # Available Spare
        ("percent_used", c_uint8),                      # Percentage Used
        ("mucs", c_uint8),                              # Number of Channels attached to media units
        ("cio", c_uint8),                               # Channel Identifiers Offset
    ]

class nvme_media_unit_stat_log(StructureBase):
    """
        Media Unit Status
    """
    _fields_ = [
        ("nmu", c_uint16),                               # Number unit status descriptor
        ("cchans", c_uint16),                            # Number of Channels
        ("sel_config", c_uint16),                        # Selected Configuration
        ("rsvd6", c_uint8 * 10),                         # Reserved
        ("mus_desc", Pointer(nvme_media_unit_stat_desc, "nmu")),     # Media unit statistic descriptors
    ]

class nvme_media_unit_config_desc(StructureBase):
    """
        Media Unit Configuration Descriptor
    """
    _fields_ = [
        ("muid", c_uint16),                              # Media Unit Identifier
        ("rsvd2", c_uint8 * 4),                          # Reserved
        ("mudl", c_uint16),                              # Media Unit Descriptor Length
    ]

class nvme_channel_config_desc(StructureBase):
    """
        Channel Configuration Descriptor
    """
    _fields_ = [
        ("chanid", c_uint16),                                   # Channel Identifier
        ("chmus", c_uint16),                                    # Number Channel Media Units
        ("mu_config_desc", Pointer(nvme_media_unit_config_desc, "chmus")),    # Channel Unit config descriptors
    ]

class nvme_end_grp_chan_desc(StructureBase):
    """
        Endurance Group Channel Configuration Descriptor
    """
    _fields_ = [
        ("egchans", c_uint16),                                  # Number of Channels
        ("chan_config_desc", Pointer(nvme_channel_config_desc, "egchans")),     # Channel config descriptors
    ]

class nvme_end_grp_config_desc(StructureBase):
    """
        Endurance Group Configuration Descriptor
    """
    _fields_ = [
        ("endgid", c_uint16),                                   # Endurance Group Identifier
        ("cap_adj_factor", c_uint16),                           # Capacity Adjustment Factor
        ("rsvd4", c_uint8 * 12),                                # Reserved
        ("tegcap", c_uint8 * 16),                               # Total Endurance Group Capacity
        ("segcap", c_uint8 * 16),                               # Spare Endurance Group Capacity
        ("end_est", c_uint8 * 16),                              # Endurance Estimate
        ("rsvd64", c_uint8 * 16),                               # Reserved
        ("egsets", c_uint16),                                   # Number of NVM Sets
        ("nvmsetid", Pointer(c_uint16, "egsets")),                             # NVM Set Identifier
    ]

class nvme_capacity_config_desc(StructureBase):
    """
        Capacity Configuration structure definitions
    """
    _fields_ = [
        ("cap_config_id", c_uint16),                            # Capacity Configuration Identifier
        ("domainid", c_uint16),                                 # Domain Identifier
        ("egcn", c_uint16),                                     # Number Endurance Group Configuration Descriptors
        ("rsvd6", c_uint8 * 26),                                # Reserved
        ("egcd", Pointer(nvme_end_grp_config_desc, "egcn")),                # Endurance Group Config descriptors.
    ]

class nvme_supported_cap_config_list_log(StructureBase):
    """
        Supported Capacity Configuration list log page
    """
    _fields_ = [
        ("sccn", c_uint8),                                  # Number of capacity configuration
        ("rsvd1", c_uint8 * 15),                            # Reserved
        ("cap_config_desc", Pointer(nvme_capacity_config_desc, "sccn")), # Capacity configuration descriptor
    ]

class nvme_resv_notification_log(StructureBase):
    """
        Reservation Notification Log
    """
    _fields_ = [
        ("lpc", c_uint64),                                  # Log Page Count
        ("rnlpt", c_uint8),                                 # See &enum nvme_resv_notify_rnlpt.
        ("nalp", c_uint8),                                  # Number of Available Log Pages
        ("rsvd9", c_uint8 * 2),                             # Reserved
        ("nsid", c_uint32),                                 # Namespace ID
        ("rsvd16",c_uint8 * 48),                           # Reserved
    ]

class NVME_RESV_NOTIFY_RNLPT(Enum):
    """
        Reservation Notification Log - Reservation Notification Log Page Type
    """
    NVME_RESV_NOTIFY_RNLPT_EMPTY = 0                            # Empty Log Page
    NVME_RESV_NOTIFY_RNLPT_REGISTRATION_PREEMPTED = 1           # Registration Preempted
    NVME_RESV_NOTIFY_RNLPT_RESERVATION_RELEASED = 2             # Reservation Released
    NVME_RESV_NOTIFY_RNLPT_RESERVATION_PREEMPTED = 3            # Reservation Preempted

class nvme_sanitize_log_page(Structure):
    """
        Sanitize Status (Log Identifier 81h)
    """
    _fields_ = [
        ('sprog', c_uint16),                    # Sanitize Progress (SPROG): indicates the fraction complete of the sanitize operation. The value is a numerator of the fraction complete that has 65,536 (10000h) as its denominator. This value
                                                # shall be set to FFFFh if the @sstat field is not set to %NVME_SANITIZE_SSTAT_STATUS_IN_PROGESS.
        ('sstat', c_uint16),                    # Sanitize Status (SSTAT): indicates the status associated with the most recent sanitize operation. See &enum nvme_sanitize_sstat.
        ('scdw10', c_uint32),                   # Sanitize Command Dword 10 Information (SCDW10): contains the value of the Command Dword 10 field of the Sanitize command that started the sanitize operation.
        ('eto', c_uint32),                      # Estimated Time For Overwrite: indicates the number of seconds required to complete an Overwrite sanitize operation with 16 passes in the background when the No-Deallocate Modifies Media After Sanitize
                                                # field is not set to 10b. A value of 0h indicates that the sanitize operation is expected to be completed in the background when the Sanitize command that started that operation is completed. A value
                                                # of FFFFFFFFh indicates that no time period is reported.
        ('etbe', c_uint32),                     # Estimated Time For Block Erase: indicates the number of seconds required to complete a Block Erase sanitize operation in the background when the No-Deallocate Modifies Media After Sanitize
                                                # field is not set to 10b. A value of 0h indicates that the sanitize operation is expected to be completed in the background when the Sanitize command that started that operation is completed.
                                                # A value of FFFFFFFFh indicates that no time period is reported.
        ('etce', c_uint32),                     # Estimated Time For Crypto Erase: indicates the number of seconds required to complete a Crypto Erase sanitize operation in the background when the No-Deallocate Modifies Media After Sanitize
                                                # field is not set to 10b. A value of 0h indicates that the sanitize operation is expected to be completed in the background when the Sanitize command that started that operation is completed.
                                                # A value of FFFFFFFFh indicates that no time period is reported.
        ('etond', c_uint32),                    # Estimated Time For Overwrite With No-Deallocate Media Modification: indicates the number of seconds required to complete an Overwrite sanitize operation and the associated additional media modification
                                                # after the Overwrite sanitize operation in the background when the No-Deallocate After Sanitize bit was set to 1 in the Sanitize command that requested the Overwrite sanitize operation; and
                                                # the No-Deallocate Modifies Media After Sanitize field is set to 10b. A value of 0h indicates that the sanitize operation is expected to be completed in the background when the Sanitize command that
                                                # started that operation is completed. A value of FFFFFFFFh indicates that no time period is reported.
        ('etbend', c_uint32),                   # Estimated Time For Block Erase With No-Deallocate Media Modification: indicates the number of seconds required to complete a Block Erase sanitize operation and the associated additional media modification
                                                # after the Block Erase sanitize operation in the background when the No-Deallocate After Sanitize bit was set to 1 in the Sanitize command that requested the Overwrite sanitize operation; and
                                                # the No-Deallocate Modifies Media After Sanitize field is set to 10b. A value of 0h indicates that the sanitize operation is expected  to be completed in the background when the Sanitize command that
                                                # started that operation is completed. A value of FFFFFFFFh indicates that no time period is reported.
        ('etcend', c_uint32),                   # Estimated Time For Crypto Erase With No-Deallocate Media Modification: indicates the number of seconds required to complete a Crypto Erase sanitize operation and the associated additional media modification
                                                # after the Crypto Erase sanitize operation in the background when the No-Deallocate After Sanitize bit was set to 1 in the Sanitize command that requested the Overwrite sanitize operation; and
                                                # the No-Deallocate Modifies Media After Sanitize field is set to 10b. A value of 0h indicates that the sanitize operation is expected to be completed in the background when the Sanitize command that
                                                # started that operation is completed. A value of FFFFFFFFh indicates that no time period is reported.
        ('rsvd32', c_uint8 * 480),              # Reserved
    ]

class NVME_SANITIZE_SSTAT(Enum):
    """
        Sanitize Status (SSTAT)
    """
    NVME_SANITIZE_SSTAT_STATUS_SHIFT		= 0                 # Shift amount to get the status value of the most recent sanitize operation from the &struct nvme_sanitize_log_page.sstat field.
    NVME_SANITIZE_SSTAT_STATUS_MASK			= 0x7               # Mask to get the status value of the most recent sanitize operation.
    NVME_SANITIZE_SSTAT_STATUS_NEVER_SANITIZED	= 0             # The NVM subsystem has never been sanitized.
    NVME_SANITIZE_SSTAT_STATUS_COMPLETE_SUCCESS	= 1             # The most recent sanitize operation completed successfully including any additional media modification.
    NVME_SANITIZE_SSTAT_STATUS_IN_PROGESS		= 2             # A sanitize operation is currently in progress.
    NVME_SANITIZE_SSTAT_STATUS_COMPLETED_FAILED	= 3             # The most recent sanitize operation failed.
    NVME_SANITIZE_SSTAT_STATUS_ND_COMPLETE_SUCCESS	= 4         # The most recent sanitize operation for which No-Deallocate After Sanitize was requested has completed successfully with deallocation of all user data.
    NVME_SANITIZE_SSTAT_COMPLETED_PASSES_SHIFT	= 3             # Shift amount to get the number of completed passes if the most recent sanitize operation was an Overwrite. This  value shall be cleared to 0h if the most
                                                                # recent sanitize operation was not an Overwrite.
    NVME_SANITIZE_SSTAT_COMPLETED_PASSES_MASK	= 0x1f          # Mask to get the number of completed passes.
    NVME_SANITIZE_SSTAT_GLOBAL_DATA_ERASED_SHIFT	= 8         # Shift amount to get the Global Data Erased value from the &struct nvme_sanitize_log_page.sstat field.
    NVME_SANITIZE_SSTAT_GLOBAL_DATA_ERASED_MASK	= 0x1           # Mask to get the Global Data Erased value.
    NVME_SANITIZE_SSTAT_GLOBAL_DATA_ERASED		= 1 << 8        # Global Data Erased: if set, then no namespace user data in the NVM subsystem has been written to and no Persistent Memory Region in the NVM subsystem has
                                                                # been enabled since being manufactured and the NVM subsystem has never been sanitized; or since the most recent successful sanitize operation.

class nvme_zns_changed_zone_log(Structure):
    """
        ZNS Changed Zone List log
    """
    _fields_ = [
        ('nrzid', c_uint16),                   # Number of Zone Identifiers: indicates the number of zone identifiers in the &struct nvme_zns_changed_zone_log.zid array.
        ('rsvd2', c_uint8 * 6),                # Reserved
        ('zid', c_uint64 * 511),                # Zone Identifier: indicates the zone identifier of a zone that has been modified since the last time the NVM subsystem was sanitized.
    ]

class NVME_ZNS_ZT(Enum):
    """
        Zone Descriptor Data Structure - Zone Type
    """
    NVME_ZNS_ZT_SEQWRITE_REQ		= 0x2       # Sequential Write Required

class NVME_ZNS_ZA(Enum):
    """
        Zone Descriptor Data Structure
    """
    NVME_ZNS_ZA_ZFC			= 1 << 0        # Zone Finished by Controller
    NVME_ZNS_ZA_FZR			= 1 << 1        # Finish Zone Recommended
    NVME_ZNS_ZA_RZR			= 1 << 2        # Reset Zone Recommended
    NVME_ZNS_ZA_ZRWAV		= 1 << 3        # Zone Reset by Controller
    NVME_ZNS_ZA_ZDEV		= 1 << 7        # Zone Descriptor Extension Valid

class NVME_ZNS_ZS(Enum):
    """
        Zone Descriptor Data Structure - Zone State
    """
    NVME_ZNS_ZS_EMPTY		= 0x1           # Empty state
    NVME_ZNS_ZS_IMPL_OPEN		= 0x2           # Implicitly open state
    NVME_ZNS_ZS_EXPL_OPEN		= 0x3           # Explicitly open state
    NVME_ZNS_ZS_CLOSED		= 0x4           # Closed state
    NVME_ZNS_ZS_READ_ONLY		= 0xd           # Read only state
    NVME_ZNS_ZS_FULL		= 0xe           # Full state
    NVME_ZNS_ZS_OFFLINE		= 0xf           # Offline state

class nvme_zns_desc(StructureBase):
    """
        Zone Descriptor Data Structure
    """
    _fields_ = [
        ('zt', c_uint8),                       # Zone Type
        ('zs', c_uint8),                       # Zone State
        ('za', c_uint8),                       # Zone Attributes
        ('zai', c_uint8),                      # Zone Attributes Information
        ('rsvd4', c_uint8 * 4),                # Reserved
        ('zcap', c_uint64),                    # Zone Capacity
        ('zslba', c_uint64),                  # Zone Start Logical Block Address
        ('wp', c_uint64),                      # Write Pointer
        ('rsvd32', c_uint8 * 32),              # Reserved
    ]

class nvme_zone_report(StructureBase):
    """
        Report Zones Data Structure
    """
    _fields_ = [
        ('nr_zones', c_uint64),                # Number of descriptors in @entries
        ('rsvd8', c_uint8 * 56),               # Reserved
        ('entries', Pointer(nvme_zns_desc, 'nr_zones')),        # Zoned namespace descriptors
    ]

class NVME_FDP_RUH_TYPE(Enum):
    """
        Reclaim Unit Handle Type
    """
    NVME_FDP_RUHT_INITIALLY_ISOLATED		= 1       # Initially Isolated
    NVME_FDP_RUHT_PERSISTENTLY_ISOLATED		= 2       # Persistently Isolated

class nvme_fdp_ruh_desc(StructureBase):
    """
        Reclaim Unit Handle Descriptor
    """
    _fields_ = [
        ('ruht', c_uint8),                     # Reclaim Unit Handle Type
        ('rsvd1', c_uint8 * 3),                # Reserved
    ]

class NVME_FDP_CONFIG_FDPA(Enum):
    """
        FDP Attributes
    """
    NVME_FDP_CONFIG_FDPA_RGIF_SHIFT	= 0                 # Reclaim Group Identifier Format Shift
    NVME_FDP_CONFIG_FDPA_RGIF_MASK	= 0xf               # Reclaim Group Identifier Format Mask
    NVME_FDP_CONFIG_FDPA_FDPVWC_SHIFT	= 4             # FDP Volatile Write Cache Shift
    NVME_FDP_CONFIG_FDPA_FDPVWC_MASK	= 0x1           # FDP Volatile Write
    NVME_FDP_CONFIG_FDPA_VALID_SHIFT	= 7             # FDP Configuration Valid Shift
    NVME_FDP_CONFIG_FDPA_VALID_MASK	= 0x1               # FDP Configuration Valid Mask

class nvme_fdp_config_desc(StructureBase):
    """
        FDP Configuration Descriptor
    """
    _fields_ = [
        ('size', c_uint16),                    # Descriptor size
        ('fdpa', c_uint8),                     # FDP Attributes
        ('vss', c_uint8),                      # Vendor Specific Size
        ('nrg', c_uint32),                     # Number of Reclaim Groups
        ('nruh', c_uint16),                    # Number of Reclaim Unit Handles
        ('maxpids', c_uint16),                 # Max Placement Identifiers
        ('nnss', c_uint32),                    # Number of Namespaces Supported
        ('runs', c_uint64),                    # Reclaim Unit Nominal Size
        ('erutl', c_uint32),                   # Estimated Reclaim Unit Time Limit
        ('rsvd28', c_uint8 * 36),              # Reserved
        ('ruhs', Pointer(nvme_fdp_ruh_desc, 'nruh')),       # Reclaim Unit Handle descriptors
    ]

class nvme_fdp_config_log(StructureBase):
    """
        FDP Configurations Log Page
    """
    _fields_ = [
        ('n', c_uint16),                       # Number of FDP Configurations
        ('version', c_uint8),                  # Log page version
        ('rsvd3', c_uint8),                    # Reserved
        ('size', c_uint32),                    # Log page size in bytes
        ('rsvd8', c_uint8 * 8),                # Reserved
        ('configs', Pointer(nvme_fdp_config_desc, 'n')), # FDP Configuration descriptors
    ]

class NVME_FDP_RUHA(Enum):
    """
        Reclaim Unit Handle Attributes
    """
    NVME_FDP_RUHA_HOST_SHIFT		= 0                 # Host Specified Reclaim Unit Handle Shift
    NVME_FDP_RUHA_HOST_MASK		= 0x1               # Host Specified Reclaim Unit Handle Mask
    NVME_FDP_RUHA_CTRL_SHIFT		= 1                 # Controller Specified Reclaim Unit Handle Shift
    NVME_FDP_RUHA_CTRL_MASK		= 0x1               # Controller Specified Reclaim Unit Handle Mask

class nvme_fdp_ruhu_desc(StructureBase):
    """
        Reclaim Unit Handle Usage Descriptor
    """
    _fields_ = [
        ('ruha', c_uint8),                     # Reclaim Unit Handle Attributes
        ('rsvd1', c_uint8 * 7),                # Reserved
    ]

class nvme_fdp_ruhu_log(StructureBase):
    """
        Reclaim Unit Handle Usage Log Page
    """
    _fields_ = [
        ('nruh', c_uint16),                    # Number of Reclaim Unit Handles
        ('rsvd2', c_uint8 * 6),                # Reserved
        ('ruhus', Pointer(nvme_fdp_ruhu_desc, 'nruh')),     # Reclaim Unit Handle Usage descriptors
    ]

class nvme_fdp_stats_log(StructureBase):
    """
        FDP Statistics Log Page
    """
    _fields_ = [
        ('hbmw', c_uint8 * 16),                # Host Bytes with Metadata Written
        ('mbmw', c_uint8 * 16),                # Media Bytes with Metadata Written
        ('mbe', c_uint8 * 16),                 # Media Bytes Erased
        ('rsvd48', c_uint8 * 16),              # Reserved
    ]

class NVME_FDP_EVENT_TYPE(Enum):
    """
        FDP Event Types
    """
    # Host Events
    NVME_FDP_EVENT_RUNFW		= 0x0       # Reclaim Unit Not Fully Written
    NVME_FDP_EVENT_RUTLE		= 0x1       # Reclaim Unit Time Limit Exceeded
    NVME_FDP_EVENT_RESET		= 0x2       # Controller Level Reset Modified Reclaim Unit Handles
    NVME_FDP_EVENT_PID		= 0x3           # Invalid Placement Identifier
    # Controller Events
    NVME_FDP_EVENT_REALLOC	= 0x80          # Media Reallocated
    NVME_FDP_EVENT_MODIFY		= 0x81          # Implicitly Modified Reclaim Unit Handle

class NVME_FDP_EVENT_REALLOC_FLAGS(Enum):
    """
        Media Reallocated Event Type Specific Flags
    """
    NVME_FDP_EVENT_REALLOC_F_LBAV	= 0x1       # LBA Valid

class nvme_fdp_event_realloc(StructureBase):
    """
        Media Reallocated Event Type Specific Information
    """
    _fields_ = [
        ('flags', c_uint8),                    # Event Type Specific flags
        ('rsvd1', c_uint8),                    # Reserved
        ('nlbam', c_uint16),                   # Number of LBAs Moved
        ('lba', c_uint64),                     # Logical Block Address
        ('rsvd12', c_uint8 * 4),               # Reserved
    ]

class NVME_FDP_EVENT_FLAGS(Enum):
    """
        FDP Event Flags
    """
    NVME_FDP_EVENT_F_PIV	= 1 << 0            # Placement Identifier Valid
    NVME_FDP_EVENT_F_NSIDV	= 1 << 1            # Namespace Identifier Valid
    NVME_FDP_EVENT_F_LV	= 1 << 2                # Location Valid

class nvme_fdp_event(StructureBase):
    """
        FDP Event
    """
    _fields_ = [
        ('type', c_uint8),                     # Event Type
        ('flags', c_uint8),                    # Event Flags
        ('pid', c_uint16),                     # Placement Identifier
        ('ts', nvme_timestamp),                # Timestamp
        ('nsid', c_uint32),                    # Namespace Identifier
        ('type_specific', c_uint8 * 16),       # Event Type Specific Information
        ('rgid', c_uint16),                    # Reclaim Group Identifier
        ('ruhid', c_uint8),                    # Reclaim Unit Handle Identifier
        ('rsvd35', c_uint8 * 5),               # Reserved
        ('vs', c_uint8 * 24),                  # Vendor Specific
    ]

class nvme_fdp_events_log(StructureBase):
    """
        FDP Events Log Page
    """
    _fields_ = [
        ('n', c_uint32),                       # Number of FDP Events
        ('rsvd4', c_uint8 * 60),               # Reserved
        ('events', nvme_fdp_event * 63),       # FDP Events
    ]

class nvme_feat_fdp_events_cdw11(StructureBase):
    """
        FDP Events Feature Command Dword 11
    """
    _fields_ = [
        ('phndl', c_uint16),                   # Placement Handle
        ('noet', c_uint8),                     # Number of FDP Event Types
        ('rsvd24', c_uint8),                   # Reserved
    ]

class NVME_FDP_SUPPORTED_EVENT_ATTRIBUTES(Enum):
    """
        Supported FDP Event Attributes
    """
    NVME_FDP_SUPP_EVENT_ENABLED_SHIFT	= 0                 # FDP Event Enable Shift
    NVME_FDP_SUPP_EVENT_ENABLED_MASK	= 0x1               # FDP Event Enable Mask

class nvme_fdp_supported_event_desc(StructureBase):
    """
        Supported FDP Event Descriptor
    """
    _fields_ = [
        ('evt', c_uint8),                      # FDP Event Type
        ('evta', c_uint8),                     # FDP Event Type Attributes
    ]

class nvme_fdp_ruh_status_desc(StructureBase):
    """
        Reclaim Unit Handle Status Descriptor
    """
    _fields_ = [
        ('pid', c_uint16),                     # Placement Identifier
        ('ruhid', c_uint16),                   # Reclaim Unit Handle Identifier
        ('earutr', c_uint32),                  # Estimated Active Reclaim Unit Time Remaining
        ('ruamw', c_uint64),                   # Reclaim Unit Available Media Writes
        ('rsvd16', c_uint8 * 16),              # Reserved
    ]

class nvme_fdp_ruh_status(StructureBase):
    """
        Reclaim Unit Handle Status
    """
    _fields_ = [
        ('rsvd0', c_uint8 * 14),               # Reserved
        ('nruhsd', c_uint16),                  # Number of Reclaim Unit Handle Status Descriptors
        ('ruhss', Pointer(nvme_fdp_ruh_status_desc, "nruhsd")),     # Reclaim Unit Handle Status descriptors
    ]

class nvme_lba_status_desc(StructureBase):
    """
        LBA Status Descriptor Entry
    """
    _fields_ = [
        ('dslba', c_uint64),                   # Descriptor Starting LBA
        ('nlb', c_uint32),                     # Number of Logical Blocks
        ('rsvd12', c_uint8),                   # Reserved
        ('status', c_uint8),                   # Additional status about this LBA range
        ('rsvd14', c_uint8 * 2),               # Reserved
    ]

class nvme_lba_status(StructureBase):
    """
        LBA Status Descriptor List
    """
    _fields_ = [
        ('nlsd', c_uint32),                    # Number of LBA Status Descriptors
        ('cmpc', c_uint8),                     # Completion Condition
        ('rsvd5', c_uint8 * 3),                # Reserved
        ('descs', Pointer(nvme_lba_status_desc, "nlsd")),   # LBA status descriptor Entry
    ]

class nvme_feat_auto_pst(StructureBase):
    """
        Autonomous Power State Transition
    """
    _fields_ = [
        ('apst_entry', c_uint64 * 32),
    ]

class NVME_APST_ENTRY(Enum):
    """
        Autonomous Power State Transition
    """
    NVME_APST_ENTRY_ITPS_SHIFT	= 3     # Idle Transition Power State Shift
    NVME_APST_ENTRY_ITPT_SHIFT	= 8     # Idle Time Prior to Transition Shift
    NVME_APST_ENTRY_ITPS_MASK	= 0x1f     # Idle Transition Power State Mask
    NVME_APST_ENTRY_ITPT_MASK	= 0xffffff  # Idle Time Prior to Transition Mask

class nvme_metadata_element_desc(StructureBase):
    """
        Metadata Element Descriptor
    """
    _fields_ = [
        ('type', c_uint8),                     # Element Type (ET)
        ('rev', c_uint8),                      # Element Revision (ER)
        ('len', c_uint16),                     # Element Length (ELEN)
        ('val', Pointer(c_uint8, "len")),                  # Element Value (EVAL), UTF-8 string
    ]

class nvme_host_metadata_descs(StructureBase):
    """
        Host Metadata Data Structure
    """
    _fields_ = [
        ('ndesc', c_uint8),                    # Number of metadata element descriptors
        ('rsvd1', c_uint8),                    # Reserved
        ("entrys",  Pointer(nvme_metadata_element_desc, "ndesc"))
    ]

class nvme_host_metadata_descs_buf(StructureBase):
    """
        Host Metadata Data Structure
    """
    _fields_ = [
        ('ndesc', c_uint8),                    # Number of metadata element descriptors
        ('rsvd1', c_uint8),                    # Reserved
        ("descs_buf", c_uint8 * 4094),         # Metadata element descriptor buffer
    ]

class NVME_CTRL_METADATA_TYPE(Enum):
    """
        Controller Metadata Element Types
    """
    NVME_CTRL_METADATA_OS_CTRL_NAME = 0x01          # Name of the controller in the operating system.
    NVME_CTRL_METADATA_OS_DRIVER_NAME = 0x02        # Name of the driver in the operating system.
    NVME_CTRL_METADATA_OS_DRIVER_VER = 0x03         # Version of the driver in the operating system.
    NVME_CTRL_METADATA_PRE_BOOT_CTRL_NAME = 0x04    # Name of the controller in the pre-boot environment.
    NVME_CTRL_METADATA_PRE_BOOT_DRIVER_NAME = 0x05  # Name of the driver in the pre-boot environment.
    NVME_CTRL_METADATA_PRE_BOOT_DRIVER_VER = 0x06   # Version of the driver in the pre-boot environment.
    NVME_CTRL_METADATA_SYS_PROC_MODEL = 0x07        # Model of the processor.
    NVME_CTRL_METADATA_CHIPSET_DRV_NAME = 0x08      # Chipset driver name.
    NVME_CTRL_METADATA_CHIPSET_DRV_VERSION = 0x09   # Chipset driver version.
    NVME_CTRL_METADATA_OS_NAME_AND_BUILD = 0x0a     # Operating system name and build.
    NVME_CTRL_METADATA_SYS_PROD_NAME = 0x0b         # System product name.
    NVME_CTRL_METADATA_FIRMWARE_VERSION = 0x0c      # Host firmware (e.g UEFI) version.
    NVME_CTRL_METADATA_OS_DRIVER_FILENAME = 0x0d    # Operating system driver filename.
    NVME_CTRL_METADATA_DISPLAY_DRV_NAME = 0x0e      # Display driver name.
    NVME_CTRL_METADATA_DISPLAY_DRV_VERSION = 0x0f   # Display driver version.
    NVME_CTRL_METADATA_HOST_DET_FAIL_REC = 0x10     # Failure record.

class NVME_NS_METADATA_TYPE(Enum):
    """
        Namespace Metadata Element Types
    """
    NVME_NS_METADATA_OS_NS_NAME = 0x01          # Name of the namespace in the operating system.
    NVME_NS_METADATA_PRE_BOOT_NS_NAME = 0x02    # Name of the namespace in the pre-boot environment.
    NVME_NS_METADATA_OS_NS_QUAL_1 = 0x03        # First qualifier of the Operating System Namespace Name.
    NVME_NS_METADATA_OS_NS_QUAL_2 = 0x04        # Second qualifier of the Operating System Namespace Name.

class nvme_lba_range_type_entry(StructureBase):
    """
        LBA Range Type - Data Structure Entry
    """
    _fields_ = [
        ('type', c_uint8),                     # Specifies the Type of the LBA range
        ('attributes', c_uint8),               # Specifies attributes of the LBA range
        ('rsvd2', c_uint8 * 14),               # Reserved
        ('slba', c_uint64),                    # Starting LBA
        ('nlb', c_uint64),                     # Number of Logical Blocks
        ('guid', c_uint8 * 16),                # UniqueIdentifier
        ('rsvd48', c_uint8 * 16),              # Reserved
    ]

class NVME_LBART(Enum):
    """
        LBA Range Type - Data Structure Entry
    """
    NVME_LBART_TYPE_GP = 0          # General Purpose
    NVME_LBART_TYPE_FS = 1          # Filesystem
    NVME_LBART_TYPE_RAID = 2        # RAID
    NVME_LBART_TYPE_CACHE = 3       # Cache
    NVME_LBART_TYPE_SWAP = 4        # Page / swap file
    NVME_LBART_ATTRIB_TEMP = 1 << 0 # Temp
    NVME_LBART_ATTRIB_HIDE = 1 << 1 # Hidden

class  nvme_lba_range_type(StructureBase):
    """
        LBA Range Type
    """
    _fields_ = [
        ('entry', nvme_lba_range_type_entry * 64),  # LBA range type entry
    ]

class nvme_plm_config(StructureBase):
    """
        Predictable Latency Mode - Deterministic Threshold Configuration Data Structure
    """
    _fields_ = [
        ('ee', c_uint16),                      # Enable Event
        ('rsvd2', c_uint8 * 30),               # Reserved
        ('dtwinrt', c_uint64),                 # DTWIN Reads Threshold
        ('dtwinwt', c_uint64),                 # DTWIN Writes Threshold
        ('dtwintt', c_uint64),                 # DTWIN Time Threshold
        ('rsvd56', c_uint8 * 456),             # Reserved
    ]

class nvme_feat_host_behavior(StructureBase):
    """
        Host Behavior Support - Data Structure
    """
    _fields_ = [
        ('acre', c_uint8),                     # Advanced Command Retry Enable
        ('rsvd1', c_uint8 * 511),              # Reserved
    ]

class NVME_HOST_BEHAVIOR_SUPPORT(Enum):
    """
        Enable Advanced Command
    """
    NVME_ENABLE_ACRE = 1 << 0           # Enable Advanced Command Retry Enable

class nvme_dsm_range(StructureBase):
    """
        Dataset Management - Range Definition
    """
    _fields_ = [
        ('cattr', c_uint32),                # Context Attributes
        ('nlb', c_uint32),                  # Length in logical blocks
        ('slba', c_uint64),                 # Starting LBA
    ]

class nvme_copy_range(StructureBase):
    _fields_ = [
        ('rsvd0', c_uint8 * 8),               # Reserved
        ('slba', c_uint64),                   # Starting LBA
        ('nlb', c_uint16),                    # Number of Logical Blocks
        ('rsvd18', c_uint8 * 6),              # Reserved
        ('eilbrt', c_uint32),                 # Expected Initial Logical Block Reference Tag Expected Logical Block Storage Tag
        ('elbat', c_uint16),                  # Expected Logical Block Application Tag
        ('elbatm', c_uint16),                 # Expected Logical Block Application Tag Mask
    ]

class nvme_copy_range_f1(StructureBase):
    _fields_ = [
        ('rsvd0', c_uint8 * 8),               # Reserved
        ('slba', c_uint64),                   # Starting LBA
        ('nlb', c_uint16),                    # Number of Logical Blocks
        ('rsvd18', c_uint8 * 8),              # Reserved
        ('elbt', c_uint8 * 10),               # Expected Initial Logical Block Reference Tag Expected Logical Block Storage Tag
        ('elbat', c_uint16),                  # Expected Logical Block Application Tag
        ('elbatm', c_uint16),                 # Expected Logical Block Application Tag Mask
    ]

class nvme_registered_ctrl(StructureBase):
    """
        Registered Controller Data Structure
    """
    _fields_ = [
        ('cntlid', c_uint16),                 # Controller ID
        ('rcsts', c_uint8),                   # Reservation Status
        ('rsvd3', c_uint8 * 5),               # Reserved
        ('hostid', c_uint64),                 # Host Identifier
        ('rkey', c_uint64),                   # Reservation Key
    ]

class nvme_registered_ctrl_ext(StructureBase):
    """
        Registered Controller Extended Data Structure
    """
    _fields_ = [
        ('cntlid', c_uint16),                 # Controller ID
        ('rcsts', c_uint8),                   # Reservation Status
        ('rsvd3', c_uint8 * 5),               # Reserved
        ('rkey', c_uint64),                   # Reservation Key
        ('hostid', c_uint8 * 16),             # Host Identifier
        ('rsvd32', c_uint8 * 32),             # Reserved
    ]

class nvme_resv_status_regctl_eds(StructureBase):
    _fields_ = [
        ('rsvd24', c_uint8 * 40),             # Reserved
        ('regctl_eds', nvme_registered_ctrl_ext), # Registered Controller Extended Data Structure
    ]

class nvme_resv_status_item(Union):
    _fields_ = [
        ('regctl_item', nvme_resv_status_regctl_eds),
        ('regctl_ds', nvme_registered_ctrl),
    ]

class nvme_resv_status(StructureBase):
    """
        Reservation Status Data Structure
    """
    _fields_ = [
        ('gen', c_uint32),                    # Generation
        ('rtype', c_uint8),                   # Reservation Type
        ('regctl', c_uint8 * 2),              # Number of Registered Controllers
        ('rsvd7', c_uint8 * 2),               # Reserved
        ('ptpls', c_uint8),                   # Persist Through Power Loss State
        ('rsvd10', c_uint8 * 14),             # Reserved
        ("entry", nvme_resv_status_item)
    ]

class nvme_streams_directive_params(StructureBase):
    """
        Streams Directive - Return Parameters Data Structure
    """
    _fields_ = [
        ('msl', c_uint16),                    # Max Streams Limit
        ('nssa', c_uint16),                   # NVM Subsystem Streams Available
        ('nsso', c_uint16),                   # NVM Subsystem Streams Open
        ('nssc', c_uint8),                    # NVM Subsystem Stream Capability
        ('rsvd', c_uint8 * 9),                # Reserved
        ('sws', c_uint32),                    # StreamWrite Size
        ('sgs', c_uint16),                    # Stream Granularity Size
        ('nsa', c_uint16),                    # Namespace Streams Allocated
        ('nso', c_uint16),                    # Namespace Streams Open
        ('rsvd2', c_uint8 * 6),               # Reserved
    ]

class nvme_streams_directive_status(StructureBase):
    """
        Streams Directive - Get Status Data Structure
    """
    _fields_ = [
        ('osc', c_uint16),                    # Open Stream Count
        ('sid', Pointer(c_uint16, "osc")),                # Stream Identifier
    ]

class nvme_id_directives(StructureBase):
    """
        Identify Directive - Return Parameters Data Structure
    """
    _fields_ = [
        ('supported', c_uint8 * 32),          # Identify directive is supported
        ('enabled', c_uint8 * 32),            # Identify directive is Enabled
        ('rsvd64', c_uint8 * 4032),           # Reserved
    ]

class NVME_DIRECTIVE_TYPES(Enum):
    """
        Directives Supported or Enabled
    """
    NVME_ID_DIR_ID_BIT	= 0                 # Identify directive is supported
    NVME_ID_DIR_SD_BIT	= 1                 # Streams directive is supported
    NVME_ID_DIR_DP_BIT	= 2                 # Direct Placement directive is supported

class nvme_host_mem_buf_attrs(StructureBase):
    """
        Host Memory Buffer - Attributes Data Structure
    """
    _fields_ = [
        ('hsize', c_uint32),                  # Host Memory Buffer Size
        ('hmdlal', c_uint32),                 # Host Memory Descriptor List Lower Address
        ('hmdlau', c_uint32),                 # Host Memory Descriptor List Upper Address
        ('hmdlec', c_uint32),                 # Host Memory Descriptor List Entry Count
        ('rsvd16', c_uint8 * 4080),           # Reserved
    ]

class  NVME_AE_TYPE(Enum):
    """
        Asynchronous Event Type
    """
    NVME_AER_ERROR				= 0     # Error event
    NVME_AER_SMART				= 1     # SMART / Health Status event
    NVME_AER_NOTICE				= 2     # Notice event
    NVME_AER_CSS				= 6     # NVM Command Set Specific events
    NVME_AER_VS				= 7         # Vendor Specific event

class NVME_AE_INFO_ERROR(Enum):
    """
        Asynchronous Event Information - Error Status
    """
    NVME_AER_ERROR_INVALID_DB_REG			= 0x00              # Write to Invalid Doorbell Register
    NVME_AER_ERROR_INVALID_DB_VAL			= 0x01              # Invalid Doorbell Write Value
    NVME_AER_ERROR_DIAG_FAILURE			= 0x02                  # Diagnostic Failure
    NVME_AER_ERROR_PERSISTENT_INTERNAL_ERROR	= 0x03              # Persistent Internal Error
    NVME_AER_ERROR_TRANSIENT_INTERNAL_ERROR		= 0x04              # Transient Internal Error
    NVME_AER_ERROR_FW_IMAGE_LOAD_ERROR		= 0x05              # Firmware Image Load Error

class NVME_AE_INFO_SMART(Enum):
    """
        Asynchronous Event Information - SMART / Health Status
    """
    NVME_AER_SMART_SUBSYSTEM_RELIABILITY		= 0x00      # NVM subsystem Reliability
    NVME_AER_SMART_TEMPERATURE_THRESHOLD		= 0x01      # Temperature Threshold
    NVME_AER_SMART_SPARE_THRESHOLD			= 0x02      # Spare Below Threshold

class NVME_AE_INFO_CSS_NVM(Enum):
    """
        Asynchronous Event Information - I/O Command Specific Status
    """
    NVME_AER_CSS_NVM_RESERVATION			= 0x00          # Reservation Log Page Available
    NVME_AER_CSS_NVM_SANITIZE_COMPLETED		= 0x01          # Sanitize Operation Completed
    NVME_AER_CSS_NVM_UNEXPECTED_SANITIZE_DEALLOC	= 0x02          # Sanitize Operation Completed With Unexpected Deallocation

class NVME_AE_INFO_NOTICE(Enum):
    """
        Asynchronous Event Information - Notice
    """
    NVME_AER_NOTICE_NS_CHANGED			= 0x00              # Namespace Attribute Changed
    NVME_AER_NOTICE_FW_ACT_STARTING			= 0x01              # Firmware Activation Starting
    NVME_AER_NOTICE_TELEMETRY			= 0x02              # Telemetry Log Changed
    NVME_AER_NOTICE_ANA				= 0x03              # Asymmetric Namespace Access Change
    NVME_AER_NOTICE_PL_EVENT			= 0x04              # Predictable Latency Event Aggregate Log Change
    NVME_AER_NOTICE_LBA_STATUS_ALERT		= 0x05      # LBA Status Information Alert
    NVME_AER_NOTICE_EG_EVENT			= 0x06              # Endurance Group Event Aggregate Log Page Change
    NVME_AER_NOTICE_DISC_CHANGED			= 0xf0              # Discovery Log Page Change

class NVME_SUBSYS_TYPE(Enum):
    """
       Type of the NVM subsystem.
    """
    NVME_NQN_DISC	= 1         # Discovery type target subsystem. Describes a referral to another Discovery Service composed of Discovery controllers that provide additional discovery records. Multiple Referral entries may
                                # be reported for each Discovery Service (if that Discovery Service has multiple NVM subsystem ports or supports multiple protocols).
    NVME_NQN_NVME	= 2         # NVME type target subsystem. Describes an NVM subsystem whose controllers may have attached namespaces (an NVM subsystem that is not composed of Discovery controllers). Multiple NVM
                                # Subsystem entries may be reported for each NVM subsystem if the current Discovery subsystem has multiple NVM subsystem ports.
    NVME_NQN_CURR	= 3         # Current Discovery type target subsystem. Describes this Discovery subsystem (the Discovery Service that contains the controller processing the Get Log Page command). Multiple Current Discovery
                                # Subsystem entries may be reported for this Discovery subsystem if the current Discovery subsystem has multiple NVM subsystem ports.


class NVMF_DISC_EFLAGS(Enum):
    """
        Discovery Log Page entry flags.
    """
    NVMF_DISC_EFLAGS_NONE		= 0             # Indicates that none of the DUPRETINFO or EPCSD features are supported.
    NVMF_DISC_EFLAGS_DUPRETINFO	= 1 << 0        # Duplicate Returned Information (DUPRETINFO): Indicates that using the content of this entry to access this Discovery Service returns the same
                                                # information that is returned by using the content of other entries in this log page that also have this flag set.
    NVMF_DISC_EFLAGS_EPCSD		= 1 << 1        # Explicit Persistent Connection Support for Discovery (EPCSD): Indicates that Explicit Persistent Connections are supported for the Discovery controller.
    NVMF_DISC_EFLAGS_NCC		= 1 << 2        #  No CDC Connectivity (NCC): If set to '1', then no DDC that describes this entry is currently connected to the CDC. If cleared to '0', then at least one DDC that
                                                # describes this entry is currently connected to the CDC. If the Discovery controller returning this log page is not  a CDC, then this bit shall be cleared to
                                                # '0' and should be ignored by the host.
class nvmf_rdma(StructureBase):
    """
        RDMA transport specific attribute settings
    """
    _fields_ = [
        ('qptype', c_uint8),                # RDMA QP Service Type (RDMA_QPTYPE): Specifies the type of RDMA Queue Pair. See &enum nvmf_rdma_qptype.
        ('prtype', c_uint8),                # RDMA Provider Type (RDMA_PRTYPE): Specifies the type of RDMA provider. See &enum nvmf_rdma_prtype.
        ('cms', c_uint8),                   # RDMA Connection Management Service (RDMA_CMS): Specifies the type of RDMA IP Connection Management Service. See &enum nvmf_rdma_cms.
        ('rsvd3', c_uint8 * 5),             # Reserved
        ('pkey', c_uint16),                 # RDMA_PKEY: Specifies the Partition Key when AF_IB (InfiniBand) address family type is used.
        ('rsvd10', c_uint8 * 246),          # Reserved
    ]

class nvmf_tcp(StructureBase):
    """
         TCP transport specific attribute settings
    """
    _fields_ = [
        ('sectype', c_uint8),               # Security Type (SECTYPE): Specifies the type of security used by the NVMe/TCP port. If SECTYPE is a value of 0h (No Security), then the host shall set up a normal TCP connection.
                                            # See &enum nvmf_tcp_sectype.
    ]

class  nvmf_tsas(Union):
    _fields_ = [
        ('common', c_char * 256),           # Common transport specific attributes
        ('rdma', nvmf_rdma),                # RDMA transport specific attributes
        ('tcp', nvmf_tcp),                  # TCP transport specific attributes
    ]

class nvmf_disc_log_entry(StructureBase):
    _fields_ = [
        ('trtype', c_uint8),                # Transport Type (TRTYPE): Specifies the NVMe Transport type. See &enum nvmf_trtype.
        ('adrfam', c_uint8),                # Address Family (ADRFAM): Specifies the address family.  See &enum nvmf_addr_family.
        ('subtype', c_uint8),               # Subsystem Type (SUBTYPE): Specifies the type of the NVM subsystem
        ('treq', c_uint8),                  # Transport Requirements (TREQ): Indicates requirements for the NVMe Transport. See &enum nvmf_treq. Port ID value (e.g. a Port ID may support both iWARP and RoCE).
        ('portid', c_uint16),               # Port ID (PORTID): Specifies a particular NVM subsystem port. Different NVMe Transports or address families may utilize the same
        ('cntlid', c_uint16),               # Controller ID (CNTLID): Specifies the controller ID. If the NVM subsystem uses a dynamic controller model, then this field shall be set to FFFFh. If the NVM subsystem uses a static
                                            # controller model, to FFEFh are valid). If the NVM subsystem uses a static controller model and the value indicated is FFFEh, then the host should remember the Controller ID returned
                                            # as part of the Fabrics Connect command in order to re-establish an association in the future with the same controller.
        ('asqsz', c_uint16),                # Admin Max SQ Size (ASQSZ): Specifies the maximum size of an Admin Submission Queue. This applies to all controllers in the NVM subsystem. The value shall be a minimum of 32 entries.
        ('eflags', c_uint16),               # Entry Flags (EFLAGS): Indicates additional information related to the current entry. See &enum nvmf_disc_eflags.
        ('rsvd12', c_uint8 * 20),           # Reserved then this field may be set to a specific controller ID (values 0h
        ('trsvcid', c_char * 32),           # Transport Service Identifier (TRSVCID): Specifies the NVMe Transport service identifier as an ASCII string. The NVMe Transport service identifier is specified by
                                            # the associated NVMe Transport binding specification.
        ('rsvd64', c_uint8 * 192),          # Reserved
        ('subnqn', c_char * 256),           # NVM Subsystem Qualified Name (SUBNQN): NVMe Qualified Name (NQN) that uniquely identifies the NVM subsystem. For a subsystem, if that Discovery subsystem has a unique
                                            # NQN (i.e., the NVM Subsystem NVMe Qualified Name (SUBNQN) field in that Discovery subsystem's Identify Controller data structure contains a unique NQN value), then the
                                            #  value returned shall be that unique NQN. If the Discovery subsystem does not have a unique NQN, then the value returned shall be the well-known Discovery Service NQN
                                            # (nqn.2014-08.org.nvmexpress.discovery).
        ('traddr', c_char * 256),           # Transport Address (TRADDR): Specifies the address of the NVM subsystem that may be used for a Connect command as an ASCII string. The Address Family field describes the
                                            # reference for parsing this field.
        ('tsas', nvmf_tsas),                # Transport specific attribute settings
    ]

class NVMF_TRTYPE(Enum):
    """
        Transport Type codes for Discovery Log Page entry TRTYPE field
    """
    NVMF_TRTYPE_UNSPECIFIED = 0         # Not indicated
    NVMF_TRTYPE_RDMA = 1                # RDMA
    NVMF_TRTYPE_FC = 2                  # Fibre Channel
    NVMF_TRTYPE_TCP = 3                 # TCP
    NVMF_TRTYPE_LOOP = 254              # Intra-host Transport (i.e., loopback), reserved for host usage.
    NVMF_TRTYPE_MAX = 255               # Maximum value for &enum nvmf_trtype

class NVMF_ADDR_FAMILY(Enum):
    """
        Address Family codes for Discovery Log Page entry ADRFAM field
    """
    NVMF_ADDR_FAMILY_PCI = 0            # PCIe
    NVMF_ADDR_FAMILY_IP4 = 1            # AF_INET: IPv4 address family.
    NVMF_ADDR_FAMILY_IP6 = 2            # AF_INET6: IPv6 address family.
    NVMF_ADDR_FAMILY_IB = 3             # AF_IB: InfiniBand address family.
    NVMF_ADDR_FAMILY_FC = 4             # Fibre Channel address family.
    NVMF_ADDR_FAMILY_LOOP = 254         # Intra-host Transport (i.e., loopback), reserved for host usage.

class NVMF_TREQ(Enum):
    NVMF_TREQ_NOT_SPECIFIED		= 0             # Not specified
    NVMF_TREQ_REQUIRED		= 1                 # Required
    NVMF_TREQ_NOT_REQUIRED		= 2             # Not Required
    NVMF_TREQ_DISABLE_SQFLOW	= 4             # SQ flow control disable supported

class NVMF_RDMA_QPTYPE(Enum):
    """
        RDMA QP Service Type codes for Discovery Log Page entry TSAS RDMA_QPTYPE field
    """
    NVMF_RDMA_QPTYPE_CONNECTED = 1
    NVMF_RDMA_QPTYPE_DATAGRAM = 2

class NVMF_RDMA_PRTYPE(Enum):
    """
        RDMA Provider Type codes for Discovery Log Page entry TSAS RDMA_PRTYPE field
    """
    NVMF_RDMA_PRTYPE_NOT_SPECIFIED = 1
    NVMF_RDMA_PRTYPE_IB = 2
    NVMF_RDMA_PRTYPE_ROCE = 3
    NVMF_RDMA_PRTYPE_ROCEV2 = 4
    NVMF_RDMA_PRTYPE_IWARP = 5

class NVMF_RDMA_CMS(Enum):
    """
        RDMA Connection Management Service Type codes for Discovery Log Page entry TSAS RDMA_CMS field
    """
    NVMF_RDMA_CMS_RDMA_CM = 1           # Sockets based endpoint addressing

class NVMF_TCP_SECTYPE(Enum):
    """
        Transport Specific Address Subtype Definition for NVMe/TCP Transport
    """
    NVMF_TCP_SECTYPE_NONE = 0           # No Security
    NVMF_TCP_SECTYPE_TLS = 1            # Transport Layer Security version 1.2
    NVMF_TCP_SECTYPE_TLS13 = 2          # Transport Layer Security version 1.3 or a subsequent version. The TLS protocol negotiates the version and cipher suite for each TCP connection.

class NVMF_LOG_DISC_LID_SUPPORT(Enum):
    """
        Discovery log specific support
    """
    NVMF_LOG_DISC_LID_NONE		= 0                 # None
    NVMF_LOG_DISC_LID_EXTDLPES	= (1 << 0)          # Extended Discovery Log Page Entries Supported
    NVMF_LOG_DISC_LID_PLEOS		= (1 << 1)          # Port Local Entries Only Supported
    NVMF_LOG_DISC_LID_ALLSUBES	= (1 << 2)          # All NVM Subsystem Entries Supported

class NVMF_LOG_DISCOVERY_LSP(Enum):
    """
        Discovery log specific field
    """
    NVMF_LOG_DISC_LSP_NONE		= 0             # None
    NVMF_LOG_DISC_LSP_EXTDLPE	= (1 << 0)      # Extended Discovery Log Page Entries
    NVMF_LOG_DISC_LSP_PLEO		= (1 << 1)      # Port Local Entries Only
    NVMF_LOG_DISC_LSP_ALLSUBE	= (1 << 2)      # All NVM Subsystem Entries

class nvmf_discovery_log(StructureBase):
    """
        Discovery Log Page (Log Identifier 70h)
    """
    _fields_ = [
        ("genctr", c_uint64),                   # Generation Counter (GENCTR): Indicates the version of the discovery information, starting at a value of 0h. For each change in the Discovery Log Page,
                                                # this counter is incremented by one. If the value of this field is FFFFFFFF_FFFFFFFFh, then the field shall be cleared to 0h when incremented (i.e., rollsover to 0h).
        ("numrec", c_uint64),                   # Number of Records (NUMREC): Indicates the number of records contained in the log.
        ("recfmt", c_uint16),                   # Record Format (RECFMT): Specifies the format of the Discovery Log Page. If a new format is defined, this value is incremented by one.
                                                # The format of the record specified in this definition shall be 0h.
        ("rsvd14", c_uint8 * 1006),             # Reserved
        ("entries", Pointer(nvmf_disc_log_entry, "numrec"))    # Discovery Log Page Entries - see &struct nvmf_disc_log_entry.
    ]

class NVMF_DIM_TAS(Enum):
    """
        Discovery Information Management Task
    """
    NVMF_DIM_TAS_REGISTER	= 0x00              # Register
    NVMF_DIM_TAS_DEREGISTER	= 0x01              # Deregister
    NVMF_DIM_TAS_UPDATE	= 0x02                  # Update

class NVMF_DIM_ENTFMT(Enum):
    """
        Discovery Information Management Entry Format
    """
    NVMF_DIM_ENTFMT_BASIC		= 0x01          # Basic discovery information entry
    NVMF_DIM_ENTFMT_EXTENDED	= 0x02          # Extended discovery information entry

class NVMF_DIM_ETYPE(Enum):
    """
        Discovery Information Management Entity Type
    """
    NVMF_DIM_ETYPE_HOST	= 0x01      # Host
    NVMF_DIM_ETYPE_DDC	= 0x02      # Direct Discovery controller
    NVMF_DIM_ETYPE_CDC	= 0x03      # Centralized Discovery controller

class NVMF_EXATTYPE(Enum):
    """
        Extended Attribute Type
    """
    NVMF_EXATTYPE_HOSTID	= 0x01      # Host Identifier
    NVMF_EXATTYPE_SYMNAME	= 0x02      # Symblic Name

class nvmf_ext_attr(StructureBase):
    """
        Extended Attribute (EXAT)
    """
    _fields_ = [
        ("exattype", c_uint16),                 # Extended Attribute Type (EXATTYPE) - see &enum nvmf_exattype
        ("exatlen", c_uint16),                  # Extended Attribute Length (EXATLEN)
        ("exatval", Pointer(c_uint8, "exatlen"))                # Extended Attribute Value (EXATVAL) - size allocated for array must be a multiple of 4 bytes
    ]

class nvmf_ext_die(StructureBase):
    """
        Extended Discovery Information Entry (DIE)
    """
    _fields_ = [
        ("trtype", c_uint8),                    # Transport Type (TRTYPE): Indicates the transport type.
        ("adrfam", c_uint8),                    # Address Family (ADRFAM): Indicates the address family.
        ("subtype", c_uint8),                   # Subsystem Type (SUBTYPE): Indicates the subsystem type.
        ("treq", c_uint8),                      # Transport Requirements (TREQ): Indicates the transport requirements.
        ("portid", c_uint16),                   # Port ID ()
        ("cntlid", c_uint16),                   # Controller ID (CNTLID): Indicates the controller ID.
        ("asqsz", c_uint16),                    # Admin Max SQ Size (ASQSZ): Indicates the maximum size of the Admin SQ.
        ("rsvd10", c_uint8 * 22),               # Reserved
        ("trsvcid", c_char * 32),               # Transport Service Identifier (TRSVCID): Indicates the transport service identifier.
        ("resv64", c_uint8 * 192),              # Reserved
        ("nqn", c_char * 256),                  # NVM Qualified Name (NQN): Indicates the NVM qualified name.
        ("traddr", c_char * 256),               # Transport Address (TRADDR): Indicates the transport address.
        ("tsas", nvmf_tsas),                    # Transport Specific Address Subtype (TSAS): Indicates the transport specific address subtype.
        ("tel", c_uint32),                      # Total Entry Length (TEL): Indicates the total length of the entry, including the header and all extended attributes.
        ("numexat", c_uint16),                  # Number of Extended Attributes (NUMEXAT): Indicates the number of extended attributes.
        ("resv1030", c_uint8 * 2),              # Reserved
        ("exat", Pointer(nvmf_ext_attr, "numexat"))             # Extended Attributes (EXAT): Indicates the extended attributes.
    ]

class nvmf_dim_data_basic(StructureBase):
    """
        Discovery Information Management (DIM) - Data
    """
    _fields_ = [
        ("tdl", c_uint32),                      # Total Data Length
        ("rsvd4", c_uint8 * 4),                 # Reserved
        ("nument", c_uint64),                   # Number of entries
        ("entfmt", c_uint16),                   # Entry Format (&enum nvmf_dim_entfmt)
        ("etype", c_uint16),                    # Entity Type (&enum nvmf_dim_etype)
        ("portlcl", c_uint8),                   # Port Local
        ("rsvd21", c_uint8),                    # Reserved
        ("ektype", c_uint16),                   # Entry Key Type
        ("eid", c_char * 256),                  # Entity Identifier (e.g. Host NQN)
        ("ename", c_char * 256),                # Entity Name (e.g. hostname)
        ("ever", c_char * 64),                  # Entity Version (e.g. OS Name/Version)
        ("rsvd600", c_uint8 * 424),             # Reserved
        ("die", Pointer(nvmf_disc_log_entry, "nument"))                   # Discovery Information Entry (see @nument above)
    ]

class nvmf_dim_data_extended(StructureBase):
    """
        Discovery Information Management (DIM) - Data
    """
    _fields_ = [
        ("tdl", c_uint32),                      # Total Data Length
        ("rsvd4", c_uint8 * 4),                 # Reserved
        ("nument", c_uint64),                   # Number of entries
        ("entfmt", c_uint16),                   # Entry Format (&enum nvmf_dim_entfmt)
        ("etype", c_uint16),                    # Entity Type (&enum nvmf_dim_etype)
        ("portlcl", c_uint8),                   # Port Local
        ("rsvd21", c_uint8),                    # Reserved
        ("ektype", c_uint16),                   # Entry Key Type
        ("eid", c_char * 256),                  # Entity Identifier (e.g. Host NQN)
        ("ename", c_char * 256),                # Entity Name (e.g. hostname)
        ("ever", c_char * 64),                  # Entity Version (e.g. OS Name/Version)
        ("rsvd600", c_uint8 * 424),             # Reserved
        ("die", nvmf_ext_die)                   # Discovery Information Entry (see @nument above)
    ]

class nvmf_connect_data(StructureBase):
    """
        Data payload for the 'connect' command
    """
    _fields_ = [
        ("hostid", c_uint8 * 16),               # Host ID of the connecting host
        ("cntlid", c_uint16),                   # Requested controller ID
        ("rsvd4", c_uint8 * 238),               # Reserved
        ("subsysnqn", c_char * 256),            # Subsystem NQN to connect to
        ("hostnqn", c_char * 256),              # Host NQN of the connecting host
        ("rsvd5", c_uint8 * 256)                # Reserved
    ]

class nvme_mi_read_nvm_ss_info(StructureBase):
    """
        NVM Subsystem Information Data Structure
    """
    _fields_ = [
        ("nump", c_uint8),                      # Number of Ports
        ("mjr", c_uint8),                       # NVMe-MI Major Version Number
        ("mnr", c_uint8),                       # NVMe-MI Minor Version Number
        ("rsvd3", c_uint8 * 29)                 # Reserved
    ]

class nvme_mi_port_pcie(StructureBase):
    """
        PCIe Port Specific Data
    """
    _fields_ = [
        ("mps", c_uint8),                       # PCIe Maximum Payload Size
        ("sls", c_uint8),                       # PCIe Supported Link Speeds Vector
        ("cls", c_uint8),                       # PCIe Current Link Speed
        ("mlw", c_uint8),                       # PCIe Maximum Link Width
        ("nlw", c_uint8),                       # PCIe Negotiated Link Width
        ("pn",c_uint8),                        # PCIe Port Number
        ("rsvd14", c_uint8 * 18)                # Reserved
    ]

class nvme_mi_port_smb(StructureBase):
    """
        SMBus Port Specific Data
    """
    _fields_ = [
        ("vpd_addr", c_uint8),                  # Current VPD SMBus/I2C Address
        ("mvpd_freq", c_uint8),                 # Maximum VPD Access SMBus/I2C Frequency
        ("mme_addr", c_uint8),                  # Current Management Endpoint SMBus/I2C Address
        ("mme_freq", c_uint8),                  # Maximum Management Endpoint SMBus/I2CFrequency
        ("nvmebm", c_uint8),                    # NVMe Basic Management
        ("rsvd13", c_uint8 * 19)                # Reserved
    ]

class nvme_mi_read_port_info_item(Union):
    _fields_ = [
        ("pcie", nvme_mi_port_pcie),            # PCIe Port Specific Data
        ("smb", nvme_mi_port_smb)               # SMBus Port Specific Data
    ]

class nvme_mi_read_port_info(StructureBase):
    """
        Port Information Data Structure
    """
    _fields_ = [
        ("portt", c_uint8),                     # Port Type
        ("rsvd1", c_uint8),                     # Reserved
        ("mmctptus", c_uint16),                 # Maximum MCTP Transmission Unit Size
        ("meb", c_uint32),                      # Management Endpoint Buffer Size
        ("portinfo", nvme_mi_read_port_info_item)   # PCIe Port Specific Data
    ]

class nvme_mi_read_ctrl_info(StructureBase):
    """
        Controller Information Data Structure
    """
    _fields_ = [
        ("portid", c_uint8),                    # Port Identifier
        ("rsvd1", c_uint8 * 4),                 # Reserved
        ("prii", c_uint8),                      # PCIe Routing ID Information
        ("pri", c_uint16),                      # PCIe Routing ID
        ("vid", c_uint16),                      # PCI Vendor ID
        ("did", c_uint16),                      # PCI Device ID
        ("ssvid", c_uint16),                    # PCI Subsystem Vendor ID
        ("ssid", c_uint16),                     # PCI Subsystem Device ID
        ("rsvd16", c_uint8 * 16)                # Reserved
    ]

class nvme_mi_osc(StructureBase):
    """
        Optionally Supported Command Data Structure
    """
    _fields_ = [
        ("type", c_uint8),                      # Command Type
        ("opc", c_uint8)                        # Opcode
    ]

class nvme_mi_read_sc_list(StructureBase):
    """
        Management Endpoint Buffer Supported Command List Data Structure
    """
    _fields_ = [
        ("numcmd", c_uint16),                   # Number of Commands
        ("cmds", Pointer(nvme_mi_osc, "numcmd"))               # MEB supported Command Data Structure
    ]

class nvme_mi_nvm_ss_health_status(StructureBase):
    """
        Subsystem Management Data Structure
    """
    _fields_ = [
        ("nss", c_uint8),                       # NVM Subsystem Status
        ("sw", c_uint8),                        # Smart Warnings
        ("ctemp", c_uint8),                     # Composite Temperature
        ("pdlu", c_uint8),                      # Percentage Drive Life Used
        ("ccs", c_uint16),                      # Composite Controller Status
        ("rsvd8", c_uint8 * 2)                  # Reserved
    ]

class NVME_MI_CCS(Enum):
    """
        Get State Control Primitive Success Response Fields - Control Primitive Specific Response
    """
    NVME_MI_CCS_RDY = 1 << 0            # Ready
    NVME_MI_CCS_CFS = 1 << 1            # Controller Fatal Status
    NVME_MI_CCS_SHST = 1 << 2           # Shutdown Status
    NVME_MI_CCS_NSSRO = 1 << 4          # NVM Subsystem Reset Occurred
    NVME_MI_CCS_CECO = 1 << 5           # Controller Enable Change Occurred
    NVME_MI_CCS_NAC = 1 << 6            # Namespace Attribute Changed
    NVME_MI_CCS_FA = 1 << 7             # Firmware Activated
    NVME_MI_CCS_CSTS = 1 << 8           # Controller Status Change
    NVME_MI_CCS_CTEMP = 1 << 9          # Composite Temperature Change
    NVME_MI_CCS_PDLU = 1 << 10          # Percentage Used
    NVME_MI_CCS_SPARE = 1 << 11         # Available Spare
    NVME_MI_CCS_CCWARN = 1 << 12        # Critical Warning

class nvme_mi_ctrl_health_status(StructureBase):
    """
        Controller Health Data Structure (CHDS)
    """
    _fields_ = [
        ("ctlid", c_uint16),                    # Controller Identifier
        ("csts", c_uint16),                     # Controller Status
        ("ctemp", c_uint16),                    # Composite Temperature
        ("pdlu", c_uint8),                      # Percentage Used
        ("spare", c_uint8),                     # Available Spare
        ("cwarn", c_uint8),                     # Critical Warning
        ("rsvd9", c_uint8 * 7)                  # Reserved
    ]

class NVME_MI_CSTS(Enum):
    """
        Controller Health Data Structure (CHDS) - Controller Status (CSTS)
    """
    NVME_MI_CSTS_RDY = 1 << 0           # Ready
    NVME_MI_CSTS_CFS = 1 << 1           # Controller Fatal Status
    NVME_MI_CSTS_SHST = 1 << 2          # Shutdown Status
    NVME_MI_CSTS_NSSRO = 1 << 4         # NVM Subsystem Reset Occurred
    NVME_MI_CSTS_CECO = 1 << 5          # Controller Enable Change Occurred
    NVME_MI_CSTS_NAC = 1 << 6           # Namespace Attribute Changed
    NVME_MI_CSTS_FA = 1 << 7            # Firmware Activated

class NVME_MI_CWARN(Enum):
    """
        Controller Health Data Structure (CHDS) - Critical Warning (CWARN)
    """
    NVME_MI_CWARN_ST = 1 << 0           # Spare Threshold
    NVME_MI_CWARN_TAUT = 1 << 1          # Temperature Above or Under Threshold
    NVME_MI_CWARN_RD = 1 << 2           # Reliability Degraded
    NVME_MI_CWARN_RO = 1 << 3           # Read Only
    NVME_MI_CWARN_VMBF = 1 << 4         # Volatile Memory Backup Failed

class nvme_mi_vpd_mra(StructureBase):
    """
        VMe MultiRecord Area
    """
    _fields_ = [
        ("nmravn", c_uint8),                    # NVMe MultiRecord Area Version Number
        ("ff", c_uint8),                        # Form Factor
        ("rsvd7", c_uint8 * 6),                 # Reserved
        ("i18vpwr", c_uint8),                   # Initial 1.8 V Power Supply Requirements
        ("m18vpwr", c_uint8),                   # Maximum 1.8 V Power Supply Requirements
        ("i33vpwr", c_uint8),                   # Initial 3.3 V Power Supply Requirements
        ("m33vpwr", c_uint8),                   # Maximum 3.3 V Power Supply Requirements
        ("rsvd17", c_uint8),                    # Reserved
        ("m33vapsr", c_uint8),                  # Maximum 3.3 Vi aux Power Supply Requirements
        ("i5vapsr", c_uint8),                   # Initial 5 V Power Supply Requirements
        ("m5vapsr", c_uint8),                   # Maximum 5 V Power Supply Requirements
        ("i12vapsr", c_uint8),                  # Initial 12 V Power Supply Requirements
        ("m12vapsr", c_uint8),                  # Maximum 12 V Power Supply Requirements
        ("mtl", c_uint8),                       # Maximum Thermal Load
        ("tnvmcap", c_uint8 * 16),              # Total NVM Capacity
        ("rsvd37", c_uint8 * 27),               # Reserved
    ]

class nvme_mi_vpd_ppmra(StructureBase):
    """
        NVMe PCIe Port MultiRecord Area
    """
    _fields_ = [
        ("nppmravn", c_uint8),                  # NVMe PCIe Port MultiRecord Area Version Number
        ("pn", c_uint8),                        # PCIe Port Number
        ("ppi", c_uint8),                       # Port Information
        ("ls", c_uint8),                        # PCIe Link Speed
        ("mlw", c_uint8),                       # PCIe Maximum Link Width
        ("mctp", c_uint8),                      # MCTP Support
        ("refccap", c_uint8),                   # Ref Clk Capability
        ("pi", c_uint8),                        # Port Identifier
        ("rsvd13", c_uint8 * 3),                # Reserved
    ]

class nvme_mi_vpd_telem(StructureBase):
    """
        Vital Product Data Element Descriptor
    """
    _fields_ = [
        ("type", c_uint8),                      # Type of the Element Descriptor
        ("rev", c_uint8),                       # Revision of the Element Descriptor
        ("len", c_uint8),                       # Number of bytes in the Element Descriptor
        ("data", Pointer(c_uint8, "len"))                   # Type-specific informationassociated with
    ]

class NVME_MI_ELEM(Enum):
    """
        Element Descriptor Types
    """
    NVME_MI_ELEM_EED = 1                # Extended Element Descriptor
    NVME_MI_ELEM_USCE = 2               # Upstream Connector Element Descriptor
    NVME_MI_ELEM_ECED = 3               # Expansion Connector Element Descriptor
    NVME_MI_ELEM_LED = 4                # Label Element Descriptor
    NVME_MI_ELEM_SMBMED = 5             # SMBus/I2C Mux Element Descriptor
    NVME_MI_ELEM_PCIESED = 6            # PCIe Switch Element Descriptor
    NVME_MI_ELEM_NVMED = 7              # NVM Subsystem Element Descriptor

class nvme_mi_vpd_tra(StructureBase):
    """
        Vital Product Data Topology MultiRecord
    """
    _fields_ = [
        ("vn", c_uint8),                    # Version Number
        ("rsvd6", c_uint8),                 # Reserved
        ("ec", c_uint8),                    # Element Count
        ("elems", Pointer(nvme_mi_vpd_telem, "ec"))    # Element Descriptor
    ]

class nvme_mi_vpd_mr_common_item(Union):
    _fields_ = [
        ("nmra", nvme_mi_vpd_mra),
        ("ppmra", nvme_mi_vpd_ppmra),
        ("tmra", nvme_mi_vpd_tra),
    ]

class nvme_mi_vpd_mr_common(StructureBase):
    """
        Vital Product Data Topology
    """
    _fields_ = [
        ("type", c_uint8),                      # Type
        ("rf", c_uint8),                        # Record Format
        ("rlen", c_uint8),                      # Record Length
        ("rchksum", c_uint8),                   # Record Checksum
        ("hchksum", c_uint8),                   # Header Checksum
        ("vpdcommon", nvme_mi_vpd_mr_common_item),   # Item
    ]

class nvme_mi_vpd_hdr(StructureBase):
    _fields_ = [
        ("ipmiver", c_uint8),                   # IPMI Format Version Number
        ("iuaoff", c_uint8),                    # Internal Use Area Starting Offset
        ("ciaoff", c_uint8),                    # Chassis Info Area Starting Offset
        ("biaoff", c_uint8),                    # Board Info Area Starting Offset
        ("piaoff", c_uint8),                    # Product Info Area Starting Offset
        ("mrioff", c_uint8),                    # MultiRecord Info Area Starting Offset
        ("rsvd6", c_uint8),                     # Reserved
        ("chchk", c_uint8),                     # Common Header Checksum
        ("vpd", Pointer(c_uint8, "iuaoff")),                   # Vital Product Data
    ]


class NVME_STATUS_FIELD(Enum):
    """
        Defines all parts of the nvme status field: status  code, status code type, and additional flags.
    """
    # Status Code Type indicators
    NVME_SCT_GENERIC		= 0x0,                  # Generic errors applicable to multiple opcodes
    NVME_SCT_CMD_SPECIFIC		= 0x1,              # Errors associated to a specific opcode
    NVME_SCT_MEDIA			= 0x2,                  # Errors associated with media and data integrity
    NVME_SCT_PATH			= 0x3,                  # Errors associated with the paths connection
    NVME_SCT_VS			= 0x7,                      # Vendor specific errors
    NVME_SCT_MASK			= 0x7,                  # Mask to get the value of the Status Code Type
    NVME_SCT_SHIFT			= 0x8,                  # Shift value to get the value of the Status Code Type
    # Status Code inidicators
    NVME_SC_MASK			= 0xff,                 # Mask to get the value of the status code
    NVME_SC_SHIFT			= 0x0,                  # Shift value to get the value of the status code
    # Generic Command Status Codes:
    NVME_SC_SUCCESS				= 0x0,              # Successful Completion: The command completed without error.
    NVME_SC_INVALID_OPCODE			= 0x1,          # Invalid Command Opcode: A reserved coded value or an unsupported value in the command opcode field.
    NVME_SC_INVALID_FIELD			= 0x2,          # Invalid Field in Command: A reserved coded value or an unsupported value in a defined field.
    NVME_SC_CMDID_CONFLICT			= 0x3,          # Command ID Conflict: The command identifier is already in use.
    NVME_SC_DATA_XFER_ERROR			= 0x4,          # Data Transfer Error: Transferring the data or metadata associated with a command experienced an error.
    NVME_SC_POWER_LOSS			= 0x5,              # Commands Aborted due to Power Loss Notification: Indicates that the command was aborted due to a power loss notification.
    NVME_SC_INTERNAL			= 0x6,              # Internal Error: The command was not completed successfully due to an internal error.
    NVME_SC_ABORT_REQ			= 0x7,              # Command Abort Requested: The command was aborted due to an Abort command being received that specified the Submission
                                                    # Queue Identifier and Command Identifier of this command.
    NVME_SC_ABORT_QUEUE			= 0x8,              # Command Aborted due to SQ Deletion: The command was aborted due to the deletion of the Submission Queue to which the command was submitted.
    NVME_SC_FUSED_FAIL			= 0x9,              # Command Aborted due to Failed Fused Command: The command was aborted due to the other command in a fused operation failing.
    NVME_SC_FUSED_MISSING			= 0xa,          # Aborted due to Missing Fused Command: The fused command was aborted due to the adjacent submission queue entry not containing a fused command that is the other command.
    NVME_SC_INVALID_NS			= 0xb,              # Invalid Namespace or Format: The namespace or the format of that namespace is invalid.
    NVME_SC_CMD_SEQ_ERROR			= 0xc,          # Command Sequence Error: The command was aborted due to a protocol violation in a multi-command sequence.
    NVME_SC_SGL_INVALID_LAST		= 0xd,          # Invalid SGL Segment Descriptor: The command includes an invalid SGL Last Segment or SGL Segment descriptor.
    NVME_SC_SGL_INVALID_COUNT		= 0xe,          # Invalid Number of SGL Descriptors: There is an SGL Last Segment descriptor or an SGL Segment descriptor in a location other than the last descriptor of a
                                                    # segment based on the length indicated.
    NVME_SC_SGL_INVALID_DATA		= 0xf,          # Data SGL Length Invalid: This may occur if the length of a Data SGL is too short. This may occur if the length of a Data  SGL is too long and the controller does
                                                    # not support SGL transfers longer than the amount of data to be transferred as indicated in the SGL Support field of the Identify Controller data structure.
    NVME_SC_SGL_INVALID_METADATA		= 0x10,     # Metadata SGL Length Invalid: This may occur if the length of a Metadata SGL is too short. This may occur if the length of a Metadata SGL is too long and the
                                                    # controller does not support SGL transfers longer than the amount of metadata to be transferred as indicated in the SGL Support field of the Identify Controller data structure.
    NVME_SC_SGL_INVALID_TYPE		= 0x11,         # SGL Descriptor Type Invalid: The type of an SGL Descriptor is a type that is not supported by the controller.
    NVME_SC_CMB_INVALID_USE			= 0x12,         # Invalid Use of Controller Memory Buffer: The attempted use of the Controller Memory Buffer is not supported by the controller.
    NVME_SC_PRP_INVALID_OFFSET		= 0x13,         # PRP Offset Invalid: The Offset field for a PRP entry is invalid.
    NVME_SC_AWU_EXCEEDED			= 0x14,         # Atomic Write Unit Exceeded: The length specified exceeds the atomic write unit size.
    NVME_SC_OP_DENIED			= 0x15,             # Operation Denied: The command was denied due to lack of access rights. Refer to the appropriate security specification.
    NVME_SC_SGL_INVALID_OFFSET		= 0x16,         # SGL Offset Invalid: The offset specified in a descriptor is invalid. This may occur when using capsules for data transfers in NVMe over Fabrics implementations and an
                                                    # invalid offset in a descriptor is specified.
    NVME_SC_HOSTID_FORMAT			= 0x18,         # Host Identifier Inconsistent Format: The NVM subsystem detected the simultaneous use of 64- bit and 128-bit Host Identifier values on different controllers.
    NVME_SC_KAT_EXPIRED			= 0x19,             # Keep Alive Timer Expired: The Keep Alive Timer expired.
    NVME_SC_KAT_INVALID			= 0x1a,             # Keep Alive Timeout Invalid: The Keep Alive Timeout value specified is invalid.
    NVME_SC_CMD_ABORTED_PREMEPT		= 0x1b,         # Command Aborted due to Preempt and Abort: The command was aborted due to a Reservation Acquire command.
    NVME_SC_SANITIZE_FAILED			= 0x1c,         # Sanitize Failed: The most recent sanitize operation failed and no recovery action has been successfully completed.
    NVME_SC_SANITIZE_IN_PROGRESS		= 0x1d,     # Sanitize In Progress: The requested function (e.g., command) is prohibited while a sanitize operation is in progress.
    NVME_SC_SGL_INVALID_GRANULARITY		= 0x1e,     # SGL Data Block Granularity Invalid: The address alignment or length granularity for an SGL Data Block descriptor is invalid.
    NVME_SC_CMD_IN_CMBQ_NOT_SUPP		= 0x1f,     # Command Not Supported for Queue in CMB: The implementation does not support submission of the command to a Submission Queue in the Controller Memory Buffer or
                                                    # command completion to a Completion Queue in the Controller Memory Buffer.
    NVME_SC_NS_WRITE_PROTECTED		= 0x20,         # Namespace is Write Protected: The command is prohibited while the namespace is write protected as a result of a change in the namespace write protection state
                                                    # as defined by the Namespace Write Protection State Machine.
    NVME_SC_CMD_INTERRUPTED			= 0x21,         # Command Interrupted: Command processing was interrupted and the controller is unable to successfully complete the command. The host should retry the command.
    NVME_SC_TRAN_TPORT_ERROR		= 0x22,         # Transient Transport Error: A transient transport error was detected. If the command is retried on the same controller, the command is likely to succeed.
                                                    # A command that fails with a transient transport error four or more times should be treated as a persistent transport error that is not likely to
                                                    # succeed if retried on the same controller.
    NVME_SC_PROHIBITED_BY_CMD_AND_FEAT	= 0x23,     # Command Prohibited by Command and Feature Lockdown: The command was aborted due to command execution being prohibited by the Command and Feature Lockdown.
    NVME_SC_ADMIN_CMD_MEDIA_NOT_READY	= 0x24,     # Admin Command Media Not Ready: The Admin command requires access to media and the media is not ready.
    NVME_SC_FDP_DISABLED			= 0x29,         # Flexible Data Placement Disabled: The command is not allowed when Flexible Data Placement is disabled.
    NVME_SC_INVALID_PLACEMENT_HANDLE_LIST	= 0x2A, # The Placement Handle List is invalid due to invalid Reclaim Unit Handle Identifier or valid Reclaim Unit Handle Identifier but restricted or the Placement
                                                    # Handle List number of entries exceeded the maximum number allowed.
    NVME_SC_LBA_RANGE			= 0x80,             # LBA Out of Range: The command references an LBA that exceeds the size of the namespace.
    NVME_SC_CAP_EXCEEDED			= 0x81,         # Capacity Exceeded: Execution of the command has caused the capacity of the namespace to be exceeded.
    NVME_SC_NS_NOT_READY			= 0x82,         # Namespace Not Ready: The namespace is not ready to be accessed as a result of a condition other than a condition that is reported as an Asymmetric Namespace Access condition.
    NVME_SC_RESERVATION_CONFLICT		= 0x83,     # Reservation Conflict: The command was aborted due to a conflict with a reservation held on the accessed namespace.
    NVME_SC_FORMAT_IN_PROGRESS		= 0x84,         # Format In Progress: A Format NVM command is in progress on the namespace.

    # Command Specific Status Codes:
    NVME_SC_CQ_INVALID			= 0x00,             # Completion Queue Invalid: The Completion Queue identifier specified in the command does not exist.
    NVME_SC_QID_INVALID			= 0x01,             #  Invalid Queue Identifier: The creation of the I/O Completion Queue failed due to an invalid queue identifier specified as part of the command. An invalid queue
                                                    #  identifier is one that is currently in use or one that is outside the range supported by the controller.
    NVME_SC_QUEUE_SIZE			= 0x02,             #  Invalid Queue Size: The host attempted to create an I/O Completion Queue with an invalid number of entries.
    NVME_SC_ABORT_LIMIT			= 0x03,             # Abort Command Limit Exceeded: The number of concurrently outstanding Abort commands has exceeded the limit indicated in the Identify Controller data structure.
    NVME_SC_ABORT_MISSING			= 0x04,         # Abort Command is missing: The abort command is missing.
    NVME_SC_ASYNC_LIMIT			= 0x05,             # Asynchronous Event Request Limit Exceeded: The number of concurrently outstanding Asynchronous Event Request commands has been exceeded.
    NVME_SC_FIRMWARE_SLOT			= 0x06,         # Invalid Firmware Slot: The firmware slot specified is invalid or read only. This error is indicated if the firmware slot exceeds the number supported.
    NVME_SC_FIRMWARE_IMAGE			= 0x07,         # Invalid Firmware Image: The firmware image specified for activation is invalid and not loaded by the controller.
    NVME_SC_INVALID_VECTOR			= 0x08,         # Invalid Interrupt Vector: The creation of the I/O Completion Queue failed due to an invalid interrupt vector specified as part of the command.
    NVME_SC_INVALID_LOG_PAGE		= 0x09,         # Invalid Log Page: The log page indicated is invalid. This error condition is also returned if a reserved log page is requested.
    NVME_SC_INVALID_FORMAT			= 0x0a,         # Invalid Format: The LBA Format specified is invalid.
    NVME_SC_FW_NEEDS_CONV_RESET		= 0x0b,         # Firmware Activation Requires Conventional Reset: The firmware activation command failed due to a conventional reset being required to complete the activation.
    NVME_SC_INVALID_QUEUE			= 0x0c,         # Invalid Queue Deletion: Invalid I/O Completion Queue specified to delete.
    NVME_SC_FEATURE_NOT_SAVEABLE		= 0x0d,     # Feature Identifier Not Saveable: The Feature Identifier specified does not support a saveable value.
    NVME_SC_FEATURE_NOT_CHANGEABLE		= 0x0e,     # Feature Not Changeable: The Feature Identifier is not able to be changed.
    NVME_SC_FEATURE_NOT_PER_NS		= 0x0f,         # Feature Not Namespace Specific: The Feature Identifier specified is not namespace specific. The Feature Identifier settings apply across all namespaces.
    NVME_SC_FW_NEEDS_SUBSYS_RESET		= 0x10,     # Firmware Activation Requires Subsystem Reset: The firmware commit was successful, however, activation of the firmware image requires an NVM Subsystem.
    NVME_SC_FW_NEEDS_RESET			= 0x11,         # Firmware Activation Requires Controller Level Reset: The firmware commit was successful, however, activation of the firmware image requires a controller level reset.
    NVME_SC_FW_NEEDS_MAX_TIME		= 0x12,         # Firmware Activation Requires Maximum Time Violation: The image specified if activated immediately would exceed the Maximum Time for Firmware Activation(MTFA)
                                                    # value reported in Identify Controller
    NVME_SC_FW_ACTIVATE_PROHIBITED		= 0x13,     # Firmware Activation Prohibited: The image specified is being prohibited from activation by the controller for vendor-specific reasons.
    NVME_SC_OVERLAPPING_RANGE		= 0x14,         # Overlapping Range: The downloaded firmware image has overlapping ranges.
    NVME_SC_NS_INSUFFICIENT_CAP		= 0x15,         # Namespace Insufficient Capacity: Creating the namespace requires more free space than is currently available.
    NVME_SC_NS_ID_UNAVAILABLE		= 0x16,         # Namespace Identifier Unavailable: The number of namespaces supported has been exceeded
    NVME_SC_NS_ALREADY_ATTACHED		= 0x18,         # Namespace Already Attached: The controller is already attached to the  namespace specified.
    NVME_SC_NS_IS_PRIVATE			= 0x19,         # Namespace Is Private: The namespace is private and is already attached to one controller.
    NVME_SC_NS_NOT_ATTACHED			= 0x1a,         # Namespace Not Attached: The request to detach the controller could not be completed because the controller is not attached to the namespace specified.
    NVME_SC_THIN_PROV_NOT_SUPP		= 0x1b,         # Thin Provisioning Not Supported: Thin provisioning is not supported by the controller.
    NVME_SC_CTRL_LIST_INVALID		= 0x1c,         # Controller List Invalid: The controller list provided contains invalid controller ids.
    NVME_SC_SELF_TEST_IN_PROGRESS		= 0x1d,     # Device Self-test In Progress: The controller or NVM subsystem already has a device self-test operation in process.
    NVME_SC_BP_WRITE_PROHIBITED		= 0x1e,         # Boot Partition Write Prohibited: The command is trying to modify a locked Boot Partition.
    NVME_SC_INVALID_CTRL_ID			= 0x1f,         # Invalid Controller Identifier: The controller identifier specified is invalid.
    NVME_SC_INVALID_SEC_CTRL_STATE		= 0x20,     # Invalid Secondary Controller State: The secondary controller is in an invalid state.
    NVME_SC_INVALID_CTRL_RESOURCES		= 0x21,     # Invalid Number of Controller Resources: The number of controller resources specified is invalid.
    NVME_SC_INVALID_RESOURCE_ID		= 0x22,         # Invalid Resource Identifier: The resource identifier specified is invalid.
    NVME_SC_PMR_SAN_PROHIBITED		= 0x23,         # Sanitize Prohibited While Persistent Memory Region is Enabled: The sanitize command is prohibited while the persistent memory region is enabled.
    NVME_SC_ANA_GROUP_ID_INVALID		= 0x24,     # ANA Group Identifier Invalid: The specified ANA Group Identifier (ANAGRPID) is not supported in the submitted command.
    NVME_SC_ANA_ATTACH_FAILED		= 0x25,         # ANA Attach Failed: The controller is not attached to the namespace as a result of an ANA condition.
    NVME_SC_INSUFFICIENT_CAP		= 0x26,         # Insufficient Capacity: Requested operation cannot be completed due to insufficient capacity.
    NVME_SC_NS_ATTACHMENT_LIMIT_EXCEEDED	= 0x27, # Namespace Attachment Limit Exceeded: Attaching the ns to a controller causes max number of ns attachments allowed to be exceeded.
    NVME_SC_PROHIBIT_CMD_EXEC_NOT_SUPPORTED = 0x28, # Prohibition of Command Execution Not Supported
    # Command Set Specific - Namespace Types commands:
    NVME_SC_IOCS_NOT_SUPPORTED		= 0x29,         # I/O Command Set Not Supported: The I/O Command Set specified in the I/O Command Set Identifier (ICSN) field of the command is not supported by the controller.
    NVME_SC_IOCS_NOT_ENABLED		= 0x2a,         # I/O Command Set Not Enabled: The I/O Command Set specified in the I/O Command Set Identifier (ICSN) field of the command is not enabled by the controller.
    NVME_SC_IOCS_COMBINATION_REJECTED	= 0x2b,     # I/O Command Set Combination Rejected: The I/O Command Set specified in the I/O Command Set Identifier (ICSN) field of the command is not supported by the controller.
    NVME_SC_INVALID_IOCS			= 0x2c,         # Invalid I/O Command Set: The I/O Command Set specified in the I/O Command Set Identifier (ICSN) field of the command is not supported by the controller.
    NVME_SC_ID_UNAVAILABLE			= 0x2d,         # Identifier Unavailable: The identifier specified is not available.
    # Discovery Information Management
    NVME_SC_INVALID_DISCOVERY_INFO		= 0x2f,     # Invalid Discovery Information: The discovery information provided in one or more extended discovery information entries is not applicable for the
                                                    # type of entity selected in the Entity Type (ETYPE) field of the Discovery Information Management command data portion’s header.
    NVME_SC_ZONING_DATA_STRUCT_LOCKED	= 0x30,     # The requested Zoning data structure is locked on the CDC.
    NVME_SC_ZONING_DATA_STRUCT_NOTFND	= 0x31,     #  The requested Zoning data structure does not exist on the CDC.
    NVME_SC_INSUFFICIENT_DISC_RES		= 0x32,     #  The number of discover information entries provided in the data portion of the Discovery Information Management command for a registration task (i.e., TAS field cleared to 0h)
                                                    #  exceeds the available capacity for new discovery information entries on the CDC or DDC. This may be a transient condition.
    NVME_SC_REQSTD_FUNCTION_DISABLED	= 0x33,     # TFabric Zoning is not enabled on the CDC.
    NVME_SC_ZONEGRP_ORIGINATOR_INVLD	= 0x34,     # The NQN contained in the ZoneGroup Originator field does not match the Host NQN used by the DDC to connect to the CDC.
    # I/O Command Set Specific - NVM commands:
    NVME_SC_BAD_ATTRIBUTES		= 0x80,             # Conflicting Dataset Management Attributes
    NVME_SC_INVALID_PI		= 0x81,                 # Invalid Protection Information
    NVME_SC_READ_ONLY		= 0x82,                 # Attempted Write to Read Only Range
    NVME_SC_CMD_SIZE_LIMIT_EXCEEDED = 0x83,         # Command Size Limit Exceeded
    # I/O Command Set Specific - Fabrics commands:
    NVME_SC_CONNECT_FORMAT		= 0x80,             # Incompatible Format: The NVM subsystem does not support the record format specified by the host.
    NVME_SC_CONNECT_CTRL_BUSY	= 0x81,             # Controller Busy: The controller is already associated with a host.
    NVME_SC_CONNECT_INVALID_PARAM	= 0x82,         # Connect Invalid Parameters: One or more of the command parameters.
    NVME_SC_CONNECT_RESTART_DISC	= 0x83,         # Connect Restart Discovery: The NVM subsystem requested is not available.
    NVME_SC_CONNECT_INVALID_HOST	= 0x84,         # Connect Invalid Host: The host is either not allowed to establish an association to any controller in the NVM subsystem or the host is not allowed to establish an
                                                    # association to the specified controller
    NVME_SC_DISCONNECT_INVALID_QTYPE= 0x85,         # Invalid Queue Type: The command was sent on the wrong queue type.
    NVME_SC_DISCOVERY_RESTART	= 0x90,             # Discovery Restart: The snapshot of the records is now invalid or out of date.
    NVME_SC_AUTH_REQUIRED		= 0x91,             # Authentication Required: NVMe in-band authentication is required and the queue has not yet been authenticated.
    # I/O Command Set Specific - ZNS commands:
    NVME_SC_ZNS_INVALID_OP_REQUEST	       = 0xb6,  # Invalid Zone Operation Request: The operation requested is invalid. This may be due to various conditions, including: attempting to allocate a ZRWA when a zone
                                                    # is not in the ZSE:Empty state; or invalid Flush Explicit ZRWA Range Send Zone Action operation.
    NVME_SC_ZNS_ZRWA_RESOURCES_UNAVAILABLE = 0xb7,  # ZRWA Resources Unavailable: No ZRWAs are available.
    NVME_SC_ZNS_BOUNDARY_ERROR	       = 0xb8,      # Zone Boundary Error: The command specifies logical blocks in more than one zone.
    NVME_SC_ZNS_FULL		       = 0xb9,          # Zone Is Full: The accessed zone is in the ZSF:Full state.
    NVME_SC_ZNS_READ_ONLY		       = 0xba,      # Zone Is Read Only: The accessed zone is in the ZSRO:Read Only state.
    NVME_SC_ZNS_OFFLINE		       = 0xbb,          # Zone Is Offline: The accessed zone is in the ZSO:Offline state.
    NVME_SC_ZNS_INVALID_WRITE	       = 0xbc,      # Zone Invalid Write: The write to a zone was not at the write pointer.
    NVME_SC_ZNS_TOO_MANY_ACTIVE	       = 0xbd,      # Too Many Active Zones: The controller does not allow additional active zones.
    NVME_SC_ZNS_TOO_MANY_OPENS	       = 0xbe,      # Too Many Open Zones: The controller does not allow additional open zones.
    NVME_SC_ZNS_INVAL_TRANSITION	       = 0xbf,  # Invalid Zone State Transition: The request is not a valid zone state transition.
    # Media and Data Integrity Errors:
    NVME_SC_WRITE_FAULT		= 0x80,                 # Write Fault: The write data could not be committed to the media.
    NVME_SC_READ_ERROR		= 0x81,                 # Unrecovered Read Error: The read data could not be recovered from the media.
    NVME_SC_GUARD_CHECK		= 0x82,                 # Guard Check Error: The command was aborted due to an end-to-end guard check failure.
    NVME_SC_APPTAG_CHECK		= 0x83,             # End-to-end App Tag Check Error: The command was aborted due to an end-to-end app tag check failure.
    NVME_SC_REFTAG_CHECK		= 0x84,             # End-to-end Reference Tag Check Error: The command was aborted due to an end-to-end reference tag check failure.
    NVME_SC_COMPARE_FAILED		= 0x85,             # Compare Failure: The command failed due to a miscompare during a Compare command.
    NVME_SC_ACCESS_DENIED		= 0x86,             # Access Denied: Access to the namespace and/or LBA range is denied due to lack of access rights.
    NVME_SC_UNWRITTEN_BLOCK		= 0x87,             # Deallocated or Unwritten Logical Block: The command failed due to an attempt to read from or verify an LBA range containing a deallocated or unwritten logical block.
    NVME_SC_STORAGE_TAG_CHECK	= 0x88,             # End-to-End Storage Tag Check Error: The command was aborted due to an end-to-end storage tag check failure.
    # Path-related Errors:
    NVME_SC_ANA_INTERNAL_PATH_ERROR	= 0x00,         # Internal Path Error: The command was not completed as the result of a controller internal error that is specific to the controller processing the command.
    NVME_SC_ANA_PERSISTENT_LOSS	= 0x01,             # Asymmetric Access Persistent Loss: The requested function (e.g., command) is not able to be performed as a result of the relationship between the controller
                                                    # and the namespace being in the ANA Persistent Loss state.
    NVME_SC_ANA_INACCESSIBLE	= 0x02,             #  Asymmetric Access Inaccessible: The requested function (e.g., command) is not able to be performed as a result of the relationship between the controller
                                                    # and the namespace being in the ANA Inaccessible state.
    NVME_SC_ANA_TRANSITION		= 0x03,             # Asymmetric Access Transition: requested function (e.g., command) is not able to be performed as a result of the relationship between the controller and
                                                    # the namespace transitioning between Asymmetric Namespace Access states.
    NVME_SC_CTRL_PATH_ERROR		= 0x60,             # Controller Pathing Error: A pathing error was detected by the controller.
    NVME_SC_HOST_PATH_ERROR		= 0x70,             # Host Pathing Error: A pathing error was detected by the host.
    NVME_SC_CMD_ABORTED_BY_HOST	= 0x71,             # Command Aborted By Host: The command was aborted as a result of host action.
    # Additional status field flags
    NVME_SC_CRD			= 0x1800,                   # Mask to get value of Command Retry Delay index
    NVME_SC_MORE			= 0x2000,               # More bit. If set, more status information for this command as part of the Error Information log that may be retrieved with the Get Log Page command.
    NVME_SC_DNR			= 0x4000,                   # Do Not Retry bit. If set, if the same command is re-submitted to any controller in the NVM subsystem, then that re-submitted command is expected to fail.

class NVME_STATUS_TYPE(Enum):
    """
        type encoding for NVMe return values, when represented as an int.
        The nvme_* api returns an int, with negative values indicating an internal or syscall error, zero signifying success, positive values representing
        the NVMe status.
        That latter case (the NVMe status) may represent status values from different parts of the transport/controller/etc, and are at most 16 bits of
        data. So, we use the most-significant 3 bits of the signed int to indicate which type of status this is.
    """
    NVME_STATUS_TYPE_SHIFT = 27         # shift value for status bits
    NVME_STATUS_TYPE_MASK = 0x7         # mask value for status bits
    NVME_STATUS_TYPE_NVME = 0           # NVMe command status value, typically from CDW3
    NVME_STATUS_TYPE_MI = 1             # NVMe-MI header status

class NVME_ADMIN_OPCODE(Enum):
    """
        Known NVMe admin opcodes
    """
    nvme_admin_delete_sq		= 0x00,                     # Delete I/O Submission Queue
    nvme_admin_create_sq		= 0x01,                     # Create I/O Submission Queue
    nvme_admin_get_log_page		= 0x02,                     # Get Log Page
    nvme_admin_delete_cq		= 0x04,                     # Delete I/O Completion Queue
    nvme_admin_create_cq		= 0x05,                     # Create I/O Completion Queue
    nvme_admin_identify		= 0x06,                         # Identify
    nvme_admin_abort_cmd		= 0x08,                     # Abort
    nvme_admin_set_features		= 0x09,                     # Set Features
    nvme_admin_get_features		= 0x0a,                     # Get Features
    nvme_admin_async_event		= 0x0c,                     # Asynchronous Event Request
    nvme_admin_ns_mgmt		= 0x0d,                         # Namespace Management
    nvme_admin_fw_commit		= 0x10,                     # Firmware Commit
    nvme_admin_fw_activate		= nvme_admin_fw_commit,     # Firmware Commit
    nvme_admin_fw_download		= 0x11,                     # Firmware Image Download
    nvme_admin_dev_self_test	= 0x14,                     # Device Self-test
    nvme_admin_ns_attach		= 0x15,                     # Namespace Attachment
    nvme_admin_keep_alive		= 0x18,                     # Keep Alive
    nvme_admin_directive_send	= 0x19,                     # Directive Send
    nvme_admin_directive_recv	= 0x1a,                     # Directive Receive
    nvme_admin_virtual_mgmt		= 0x1c,                     # Virtualization Management
    nvme_admin_nvme_mi_send		= 0x1d,                     # NVMe-MI Send
    nvme_admin_nvme_mi_recv		= 0x1e,                     # NVMe-MI Receive
    nvme_admin_capacity_mgmt	= 0x20,                     # Capacity Management
    nvme_admin_discovery_info_mgmt	= 0x21,                 # Discovery Information Management (DIM)
    nvme_admin_fabric_zoning_recv	= 0x22,                 # Fabric Zoning Receive
    nvme_admin_lockdown		= 0x24,                         # Lockdown
    nvme_admin_fabric_zoning_lookup	= 0x25,                 # Fabric Zoning Lookup
    nvme_admin_fabric_zoning_send	= 0x29,                 # Fabric Zoning Send
    nvme_admin_dbbuf		= 0x7c,                         # Doorbell Buffer Config
    nvme_admin_fabrics		= 0x7f,                         # fabrics commands
    nvme_admin_format_nvm		= 0x80,                     # Format NVM
    nvme_admin_security_send	= 0x81,                     # Security Send
    nvme_admin_security_recv	= 0x82,                     # Security Receive
    nvme_admin_sanitize_nvm		= 0x84,                     # Sanitize
    nvme_admin_get_lba_status	= 0x86,                     # Get LBA Status

class NVME_IDENTIFY_CNS(Enum):
    NVME_IDENTIFY_CNS_NS					= 0x00,             # Identify Namespace data structure
    NVME_IDENTIFY_CNS_CTRL					= 0x01,             # Identify Controller data structure
    NVME_IDENTIFY_CNS_NS_ACTIVE_LIST			= 0x02,         # Active Namespace ID list
    NVME_IDENTIFY_CNS_NS_DESC_LIST				= 0x03,         # Namespace Identification Descriptor list
    NVME_IDENTIFY_CNS_NVMSET_LIST				= 0x04,         # NVM Set List
    NVME_IDENTIFY_CNS_CSI_NS				= 0x05,             # I/O Command Set specific Identify Namespace data structure
    NVME_IDENTIFY_CNS_CSI_CTRL				= 0x06,             # I/O Command Set specific Identify Controller data structure
    NVME_IDENTIFY_CNS_CSI_NS_ACTIVE_LIST			= 0x07,     # Active Namespace ID list associated with the specified I/O Command Set
    NVME_IDENTIFY_CNS_CSI_INDEPENDENT_ID_NS			= 0x08,     # I/O Command Set Independent Identify
    NVME_IDENTIFY_CNS_NS_USER_DATA_FORMAT			= 0x09,     # Namespace user data format
    NVME_IDENTIFY_CNS_CSI_NS_USER_DATA_FORMAT		= 0x0A,     # I/O Command Set specific user data format Namespace data structure
    NVME_IDENTIFY_CNS_ALLOCATED_NS_LIST			= 0x10,         # Allocated Namespace ID list
    NVME_IDENTIFY_CNS_ALLOCATED_NS				= 0x11,         # Identify Namespace data structure for the specified allocated NSID
    NVME_IDENTIFY_CNS_NS_CTRL_LIST				= 0x12,         # Controller List of controllers attached to the specified NSID
    NVME_IDENTIFY_CNS_CTRL_LIST				= 0x13,             # Controller List of controllers that exist in the NVM subsystem
    NVME_IDENTIFY_CNS_PRIMARY_CTRL_CAP			= 0x14,         # Primary Controller Capabilities data structure for the specified primary controller
    NVME_IDENTIFY_CNS_SECONDARY_CTRL_LIST			= 0x15,     # Secondary Controller list of controllers associated with the primary controller processing the command
    NVME_IDENTIFY_CNS_NS_GRANULARITY			= 0x16,         # A Namespace Granularity List
    NVME_IDENTIFY_CNS_UUID_LIST				= 0x17,             # A UUID List
    NVME_IDENTIFY_CNS_DOMAIN_LIST				= 0x18,         # Domain List
    NVME_IDENTIFY_CNS_ENDURANCE_GROUP_ID			= 0x19,     # Endurance Group List
    NVME_IDENTIFY_CNS_CSI_ALLOCATED_NS_LIST			= 0x1A,     # I/O Command Set specific Allocated Namespace ID list
    NVME_IDENTIFY_CNS_CSI_ID_NS_DATA_STRUCTURE		= 0x1B,     # I/O Command Set specific ID Namespace Data Structure for Allocated Namespace ID
    NVME_IDENTIFY_CNS_COMMAND_SET_STRUCTURE			= 0x1C,     # Base Specification 2.0a section 5.17.2.21

class NVME_CMD_GET_LOG_LID(Enum):
    NVME_LOG_LID_SUPPORTED_LOG_PAGES			= 0x00,                     # Supported Log Pages
    NVME_LOG_LID_ERROR					= 0x01,                             # Error Information
    NVME_LOG_LID_SMART					= 0x02,                             # SMART / Health Information
    NVME_LOG_LID_FW_SLOT					= 0x03,                         # Firmware Slot Information
    NVME_LOG_LID_CHANGED_NS					= 0x04,                         # Changed Namespace List
    NVME_LOG_LID_CMD_EFFECTS				= 0x05,                         # Commands Supported and Effects
    NVME_LOG_LID_DEVICE_SELF_TEST				= 0x06,                     # Device Self-test
    NVME_LOG_LID_TELEMETRY_HOST				= 0x07,                         # Telemetry Host-Initiated
    NVME_LOG_LID_TELEMETRY_CTRL				= 0x08,                         # Telemetry Controller-Initiated
    NVME_LOG_LID_ENDURANCE_GROUP				= 0x09,                     # Endurance Group Information
    NVME_LOG_LID_PREDICTABLE_LAT_NVMSET			= 0x0a,                     # Predictable Latency Per NVM Set
    NVME_LOG_LID_PREDICTABLE_LAT_AGG			= 0x0b,                     # Predictable Latency Event Aggregate
    NVME_LOG_LID_ANA					= 0x0c,                             # Asymmetric Namespace Access
    NVME_LOG_LID_PERSISTENT_EVENT				= 0x0d,                     # Persistent Event Log
    NVME_LOG_LID_LBA_STATUS					= 0x0e,                         # LBA Status Information
    NVME_LOG_LID_ENDURANCE_GRP_EVT				= 0x0f,                     # Endurance Group Event Aggregate
    NVME_LOG_LID_MEDIA_UNIT_STATUS				= 0x10,                     # Media Unit Status
    NVME_LOG_LID_SUPPORTED_CAP_CONFIG_LIST			= 0x11,                 # Supported Capacity Configuration List
    NVME_LOG_LID_FID_SUPPORTED_EFFECTS			= 0x12,                     # Feature Identifiers Supported and Effects
    NVME_LOG_LID_MI_CMD_SUPPORTED_EFFECTS			= 0x13,                 # NVMe-MI Commands Supported and Effects
    NVME_LOG_LID_BOOT_PARTITION				= 0x15,                         # Boot Partition
    NVME_LOG_LID_PHY_RX_EOM					= 0x19,                         # Physical Interface Receiver Eye Opening Measurement
    NVME_LOG_LID_FDP_CONFIGS				= 0x20,                         # FDP Configurations
    NVME_LOG_LID_FDP_RUH_USAGE				= 0x21,                         # Reclaim Unit Handle Usage
    NVME_LOG_LID_FDP_STATS					= 0x22,                         # FDP Statistics
    NVME_LOG_LID_FDP_EVENTS					= 0x23,                         # FDP Events
    NVME_LOG_LID_DISCOVER					= 0x70,                         # Discovery
    NVME_LOG_LID_RESERVATION				= 0x80,                         # Reservation Notification
    NVME_LOG_LID_SANITIZE					= 0x81,                         # Sanitize Status
    NVME_LOG_LID_ZNS_CHANGED_ZONES				= 0xbf,                     # Changed Zone List

class NVME_FEATURES_ID(Enum):
    NVME_FEAT_FID_ARBITRATION				= 0x01,                     # Arbitration
    NVME_FEAT_FID_POWER_MGMT				= 0x02,                     # Power Management
    NVME_FEAT_FID_LBA_RANGE					= 0x03,                     # LBA Range Type
    NVME_FEAT_FID_TEMP_THRESH				= 0x04,                     # Temperature Threshold
    NVME_FEAT_FID_ERR_RECOVERY				= 0x05,                     # Error Recovery
    NVME_FEAT_FID_VOLATILE_WC				= 0x06,                     # Volatile Write Cache
    NVME_FEAT_FID_NUM_QUEUES				= 0x07,                     # Number of Queues
    NVME_FEAT_FID_IRQ_COALESCE				= 0x08,                     # Interrupt Coalescing
    NVME_FEAT_FID_IRQ_CONFIG				= 0x09,                     # Interrupt Vector Configuration
    NVME_FEAT_FID_WRITE_ATOMIC				= 0x0a,                     # Write Atomicity Normal
    NVME_FEAT_FID_ASYNC_EVENT				= 0x0b,                     # Asynchronous Event Configuration
    NVME_FEAT_FID_AUTO_PST					= 0x0c,                     # Autonomous Power State Transition
    NVME_FEAT_FID_HOST_MEM_BUF				= 0x0d,                     # Host Memory Buffer
    NVME_FEAT_FID_TIMESTAMP					= 0x0e,                     # Timestamp
    NVME_FEAT_FID_KATO					= 0x0f,                         # Keep Alive Timer
    NVME_FEAT_FID_HCTM					= 0x10,                         # Host Controlled Thermal Management
    NVME_FEAT_FID_NOPSC					= 0x11,                         # Non-Operational Power State Config
    NVME_FEAT_FID_RRL					= 0x12,                         # Read Recovery Level Config
    NVME_FEAT_FID_PLM_CONFIG				= 0x13,                     # Predictable Latency Mode Config
    NVME_FEAT_FID_PLM_WINDOW				= 0x14,                     # Predictable Latency Mode Window
    NVME_FEAT_FID_LBA_STS_INTERVAL				= 0x15,                 # LBA Status Information Report Interval
    NVME_FEAT_FID_HOST_BEHAVIOR				= 0x16,                     # Host Behavior Support
    NVME_FEAT_FID_SANITIZE					= 0x17,                     # Endurance Group Event Configuration
    NVME_FEAT_FID_ENDURANCE_EVT_CFG				= 0x18,                 # Endurance Group Event Configuration
    NVME_FEAT_FID_IOCS_PROFILE				= 0x19,                     # I/O Command Set Profile
    NVME_FEAT_FID_SPINUP_CONTROL				= 0x1a,                 # Spinup Control
    NVME_FEAT_FID_FDP					= 0x1d,                         # Flexible Data Placement
    NVME_FEAT_FID_FDP_EVENTS				= 0x1e,                     # FDP Events
    NVME_FEAT_FID_ENH_CTRL_METADATA				= 0x7d,                 # Enhanced Controller Metadata
    NVME_FEAT_FID_CTRL_METADATA				= 0x7e,                     # Controller Metadata
    NVME_FEAT_FID_NS_METADATA				= 0x7f,                     # Namespace Metadata
    NVME_FEAT_FID_SW_PROGRESS				= 0x80,                     # Software Progress Marker
    NVME_FEAT_FID_HOST_ID					= 0x81,                     # Host Identifier
    NVME_FEAT_FID_RESV_MASK					= 0x82,                     # Reservation Notification Mask
    NVME_FEAT_FID_RESV_PERSIST				= 0x83,                     # Reservation Persistence
    NVME_FEAT_FID_WRITE_PROTECT				= 0x84,                     # Namespace Write Protection Config

class NVME_FEAT(Enum):
    """
        Features Access Shifts/Masks values
    """
    NVME_FEAT_ARBITRATION_BURST_SHIFT	= 0,
    NVME_FEAT_ARBITRATION_BURST_MASK	= 0x7,
    NVME_FEAT_ARBITRATION_LPW_SHIFT		= 8,
    NVME_FEAT_ARBITRATION_LPW_MASK		= 0xff,
    NVME_FEAT_ARBITRATION_MPW_SHIFT		= 16,
    NVME_FEAT_ARBITRATION_MPW_MASK		= 0xff,
    NVME_FEAT_ARBITRATION_HPW_SHIFT		= 24,
    NVME_FEAT_ARBITRATION_HPW_MASK		= 0xff,
    NVME_FEAT_PWRMGMT_PS_SHIFT		= 0,
    NVME_FEAT_PWRMGMT_PS_MASK		= 0x1f,
    NVME_FEAT_PWRMGMT_WH_SHIFT		= 5,
    NVME_FEAT_PWRMGMT_WH_MASK		= 0x7,
    NVME_FEAT_LBAR_NR_SHIFT			= 0,
    NVME_FEAT_LBAR_NR_MASK			= 0x3f,
    NVME_FEAT_TT_TMPTH_SHIFT		= 0,
    NVME_FEAT_TT_TMPTH_MASK			= 0xffff,
    NVME_FEAT_TT_TMPSEL_SHIFT		= 16,
    NVME_FEAT_TT_TMPSEL_MASK		= 0xf,
    NVME_FEAT_TT_THSEL_SHIFT		= 20,
    NVME_FEAT_TT_THSEL_MASK			= 0x3,
    NVME_FEAT_ERROR_RECOVERY_TLER_SHIFT	= 0,
    NVME_FEAT_ERROR_RECOVERY_TLER_MASK	= 0xffff,
    NVME_FEAT_ERROR_RECOVERY_DULBE_SHIFT	= 16,
    NVME_FEAT_ERROR_RECOVERY_DULBE_MASK	= 0x1,
    NVME_FEAT_VWC_WCE_SHIFT		= 0,
    NVME_FEAT_VWC_WCE_MASK		= 0x1,
    NVME_FEAT_NRQS_NSQR_SHIFT	= 0,
    NVME_FEAT_NRQS_NSQR_MASK	= 0xffff,
    NVME_FEAT_NRQS_NCQR_SHIFT	= 16,
    NVME_FEAT_NRQS_NCQR_MASK	= 0xffff,
    NVME_FEAT_IRQC_THR_SHIFT	= 0,
    NVME_FEAT_IRQC_THR_MASK	= 0xff,
    NVME_FEAT_IRQC_TIME_SHIFT	= 8,
    NVME_FEAT_IRQC_TIME_MASK	= 0xff,
    NVME_FEAT_ICFG_IV_SHIFT		= 0,
    NVME_FEAT_ICFG_IV_MASK		= 0xffff,
    NVME_FEAT_ICFG_CD_SHIFT		= 16,
    NVME_FEAT_ICFG_CD_MASK		= 0x1,
    NVME_FEAT_WA_DN_SHIFT		= 0,
    NVME_FEAT_WA_DN_MASK		= 0x1,
    NVME_FEAT_AE_SMART_SHIFT	= 0,
    NVME_FEAT_AE_SMART_MASK		= 0xff,
    NVME_FEAT_AE_NAN_SHIFT		= 8,
    NVME_FEAT_AE_NAN_MASK		= 0x1,
    NVME_FEAT_AE_FW_SHIFT		= 9,
    NVME_FEAT_AE_FW_MASK		= 0x1,
    NVME_FEAT_AE_TELEM_SHIFT	= 10,
    NVME_FEAT_AE_TELEM_MASK		= 0x1,
    NVME_FEAT_AE_ANA_SHIFT		= 11,
    NVME_FEAT_AE_ANA_MASK		= 0x1,
    NVME_FEAT_AE_PLA_SHIFT		= 12,
    NVME_FEAT_AE_PLA_MASK		= 0x1,
    NVME_FEAT_AE_LBAS_SHIFT		= 13,
    NVME_FEAT_AE_LBAS_MASK		= 0x1,
    NVME_FEAT_AE_EGA_SHIFT		= 14,
    NVME_FEAT_AE_EGA_MASK		= 0x1,
    NVME_FEAT_APST_APSTE_SHIFT	= 0,
    NVME_FEAT_APST_APSTE_MASK	= 0x1,
    NVME_FEAT_HMEM_EHM_SHIFT	= 0,
    NVME_FEAT_HMEM_EHM_MASK		= 0x1,
    NVME_FEAT_HCTM_TMT2_SHIFT	= 0,
    NVME_FEAT_HCTM_TMT2_MASK	= 0xffff,
    NVME_FEAT_HCTM_TMT1_SHIFT	= 16,
    NVME_FEAT_HCTM_TMT1_MASK	= 0xffff,
    NVME_FEAT_NOPS_NOPPME_SHIFT	= 0,
    NVME_FEAT_NOPS_NOPPME_MASK	= 0x1,
    NVME_FEAT_RRL_RRL_SHIFT		= 0,
    NVME_FEAT_RRL_RRL_MASK		= 0xff,
    NVME_FEAT_PLM_PLME_SHIFT	= 0,
    NVME_FEAT_PLM_PLME_MASK		= 0x1,
    NVME_FEAT_PLMW_WS_SHIFT		= 0,
    NVME_FEAT_PLMW_WS_MASK		= 0x7,
    NVME_FEAT_LBAS_LSIRI_SHIFT	= 0,
    NVME_FEAT_LBAS_LSIRI_MASK	= 0xffff,
    NVME_FEAT_LBAS_LSIPI_SHIFT	= 16,
    NVME_FEAT_LBAS_LSIPI_MASK	= 0xffff,
    NVME_FEAT_SC_NODRM_SHIFT	= 0,
    NVME_FEAT_SC_NODRM_MASK		= 0x1,
    NVME_FEAT_EG_ENDGID_SHIFT	= 0,
    NVME_FEAT_EG_ENDGID_MASK	= 0xffff,
    NVME_FEAT_EG_EGCW_SHIFT		= 16,
    NVME_FEAT_EG_EGCW_MASK		= 0xff,
    NVME_FEAT_SPM_PBSLC_SHIFT	= 0,
    NVME_FEAT_SPM_PBSLC_MASK	= 0xff,
    NVME_FEAT_HOSTID_EXHID_SHIFT	= 0,
    NVME_FEAT_HOSTID_EXHID_MASK	= 0x1,
    NVME_FEAT_RM_REGPRE_SHIFT	= 1,
    NVME_FEAT_RM_REGPRE_MASK	= 0x1,
    NVME_FEAT_RM_RESREL_SHIFT	= 2,
    NVME_FEAT_RM_RESREL_MASK	= 0x1,
    NVME_FEAT_RM_RESPRE_SHIFT	= 0x3,
    NVME_FEAT_RM_RESPRE_MASK	= 0x1,
    NVME_FEAT_RP_PTPL_SHIFT		= 0,
    NVME_FEAT_RP_PTPL_MASK		= 0x1,
    NVME_FEAT_WP_WPS_SHIFT		= 0,
    NVME_FEAT_WP_WPS_MASK		= 0x7,
    NVME_FEAT_IOCSP_IOCSCI_SHIFT	= 0,
    NVME_FEAT_IOCSP_IOCSCI_MASK	= 0x1ff,
    NVME_FEAT_FDP_ENABLED_SHIFT	= 0,
    NVME_FEAT_FDP_ENABLED_MASK	= 0x1,
    NVME_FEAT_FDP_INDEX_SHIFT	= 8,
    NVME_FEAT_FDP_INDEX_MASK	= 0xf,
    NVME_FEAT_FDP_EVENTS_ENABLE_SHIFT = 0,
    NVME_FEAT_FDP_EVENTS_ENABLE_MASK  = 0x1,

class NVME_GET_FEATURES_SEL(Enum):
    """
        Get Features - Select
    """
    NVME_GET_FEATURES_SEL_CURRENT				= 0,            # Current value
    NVME_GET_FEATURES_SEL_DEFAULT				= 1,            # Default value
    NVME_GET_FEATURES_SEL_SAVED				= 2,                # Saved value
    NVME_GET_FEATURES_SEL_SUPPORTED				= 3,            # Supported capabilities

class NVME_CMD_FORMAT_MSET(Enum):
    """
        Format NVM - Metadata Settings
    """
    NVME_FORMAT_MSET_SEPARATE				= 0,                # indicates that the metadata is transferred as part of a separate buffer.
    NVME_FORMAT_MSET_EXTENDED				= 1,                # indicates that the metadata is transferred as part of an extended data LBA.

class NVME_CMD_FORMAT_PI(Enum):
    """
        Format NVM - Protection Information
    """
    NVME_FORMAT_PI_DISABLE					= 0,            # Protection information is not enabled.
    NVME_FORMAT_PI_TYPE1					= 1,            # Protection information is enabled, Type 1.
    NVME_FORMAT_PI_TYPE2					= 2,            # Protection information is enabled, Type 2.
    NVME_FORMAT_PI_TYPE3					= 3,            # Protection information is enabled, Type 3.


class NVME_CMD_FORMAT_PIL(Enum):
    """
        Format NVM - Protection Information Location
    """
    NVME_FORMAT_PIL_LAST					= 0,            # Protection information is transferred as the last bytes of metadata.
    NVME_FORMAT_PIL_FIRST					= 1,            # Protection information is transferred as the first bytes of metadata.

class NVME_CMD_FORMAT_SES(Enum):
    """
        Format NVM - Secure Erase Settings
    """
    NVME_FORMAT_SES_NONE					= 0,                # No secure erase operation requested.
    NVME_FORMAT_SES_USER_DATA_ERASE				= 1,            # User Data Erase: All user data shall be erased, contents of the user data after the erase is indeterminate (e.g. the user data may be zero filled, one filled, etc.).
                                                                # If a User Data Erase is requested and all affected user data is encrypted, then the controller is allowed to use a cryptographic erase to perform the requested User
                                                                # Data Erase.
    NVME_FORMAT_SES_CRYPTO_ERASE				= 2,            # Cryptographic Erase: All user data shall be erased cryptographically. This is accomplished by deleting the encryption key.

class NVME_NS_MGMT_SEL(Enum):
    """
        Namespace Management - Select
    """
    NVME_NS_MGMT_SEL_CREATE					= 0,            # Namespace Create selection
    NVME_NS_MGMT_SEL_DELETE					= 1,            # Namespace Delete selection

class NVME_NS_ATTACH_SEL(Enum):
    """
        Namespace Attachment - Select
    """
    NVME_NS_ATTACH_SEL_CTRL_ATTACH				= 0,            # Namespace attach selection
    NVME_NS_ATTACH_SEL_CTRL_DEATTACH				= 1,            # Namespace detach selection

class NVME_FW_COMMIT_CA(Enum):
    """
        Firmware Commit - Commit Action
    """
    NVME_FW_COMMIT_CA_REPLACE					= 0,                # Downloaded image replaces the existing image, if any, in the specified Firmware Slot. The newly placed image is not activated.
    NVME_FW_COMMIT_CA_REPLACE_AND_ACTIVATE			= 1,            # Downloaded image replaces the existing image, if any, in the specified Firmware Slot. The newly placed image is activated at the next Controller Level Reset.
    NVME_FW_COMMIT_CA_SET_ACTIVE				= 2,                # The existing image in the specified Firmware Slot is activated at the next Controller Level Reset.
    NVME_FW_COMMIT_CA_REPLACE_AND_ACTIVATE_IMMEDIATE	= 3,        # Downloaded image replaces the existing image, if any, in the specified Firmware Slot and is then activated immediately. If there is not a newly downloaded image,
                                                                    # then the existing image in the specified firmware slot is activated immediately.
    NVME_FW_COMMIT_CA_REPLACE_BOOT_PARTITION		= 6,            # Downloaded image replaces the Boot Partition specified by the Boot Partition ID field.
    NVME_FW_COMMIT_CA_ACTIVATE_BOOT_PARTITION		= 7,            # Mark the Boot Partition specified in the BPID field as active and update BPINFO.ABPID.

class NVME_DIRECTIVE_DTYPE(Enum):
    """
        Directive Types
    """
    NVME_DIRECTIVE_DTYPE_IDENTIFY				= 0,            # Identify directive type
    NVME_DIRECTIVE_DTYPE_STREAMS				= 1,            # Streams directive type

class NVME_DIRECTIVE_RECEIVE_DOPER(Enum):
    """
        Directive Receive Directive Operation
    """
    NVME_DIRECTIVE_RECEIVE_IDENTIFY_DOPER_PARAM		= 0x01,
    NVME_DIRECTIVE_RECEIVE_STREAMS_DOPER_PARAM		= 0x01,
    NVME_DIRECTIVE_RECEIVE_STREAMS_DOPER_STATUS		= 0x02,
    NVME_DIRECTIVE_RECEIVE_STREAMS_DOPER_RESOURCE		= 0x03,

class NVME_DIRECTIVE_SEND_DOPER(Enum):
    """
        Directive Send Directive Operation
    """
    NVME_DIRECTIVE_SEND_IDENTIFY_DOPER_ENDIR		= 0x01,
    NVME_DIRECTIVE_SEND_STREAMS_DOPER_RELEASE_IDENTIFIER	= 0x01,
    NVME_DIRECTIVE_SEND_STREAMS_DOPER_RELEASE_RESOURCE	= 0x02,

class NVME_DIRECTIVE_SEND_IDENTIFY_ENDIR(Enum):
    """
        Directive Send Identify Enable Directive
    """
    NVME_DIRECTIVE_SEND_IDENTIFY_ENDIR_DISABLE		= 0,
    NVME_DIRECTIVE_SEND_IDENTIFY_ENDIR_ENABLE		= 1,

class NVME_SANITIZE_SANACT(Enum):
    """
        Sanitize Action
    """
    NVME_SANITIZE_SANACT_EXIT_FAILURE			= 1,            # Exit Failure Mode.
    NVME_SANITIZE_SANACT_START_BLOCK_ERASE			= 2,        # Start a Block Erase sanitize operation.
    NVME_SANITIZE_SANACT_START_OVERWRITE			= 3,        # Start an Overwrite sanitize operation.
    NVME_SANITIZE_SANACT_START_CRYPTO_ERASE			= 4,        # Start a Crypto Erase sanitize operation.

class NVME_DST_STC(Enum):
    """
        Action taken by the Device Self-test command
    """
    NVME_DST_STC_SHORT					= 0x1,        # Start a short device self-test operation
    NVME_DST_STC_LONG					= 0x2,        # Start an extended device self-test operation
    NVME_DST_STC_VS						= 0xe,        # Start a vendor specific device self-test operation
    NVME_DST_STC_ABORT					= 0xf,        # Abort device self-test operation

class NVME_VIRT_MGMT_ACT(Enum):
    """
        Virtualization Management - Action
    """
    NVME_VIRT_MGMT_ACT_PRIM_CTRL_FLEX_ALLOC			= 1,            # Primary Controller Flexible Allocation
    NVME_VIRT_MGMT_ACT_OFFLINE_SEC_CTRL			= 7,            # Secondary Controller Offline
    NVME_VIRT_MGMT_ACT_ASSIGN_SEC_CTRL			= 8,            # Secondary Controller Ass

class NVME_VIRT_MGMT_RT(Enum):
    """
        Virtualization Management - Resource Type
    """
    NVME_VIRT_MGMT_RT_VQ_RESOURCE				= 0,            # VQ Resources
    NVME_VIRT_MGMT_RT_VI_RESOURCE				= 1,            # VI Resources

class NVME_NS_WRITE_PROTECT_CFG(Enum):
    """
        Write Protection - Write Protection State
    """
    NVME_NS_WP_CFG_NONE					= 0,            # No Write Protect
    NVME_NS_WP_CFG_PROTECT					= 1,            # Write Protect
    NVME_NS_WP_CFG_PROTECT_POWER_CYCLE			= 2,            # Write Protect Until Power Cycle
    NVME_NS_WP_CFG_PROTECT_PERMANENT            = 3,            # Permanent Write Protect

class NVME_LOG_ANA_LSP(Enum):
    """
        Asymmetric Namespace Access - Return Groups Only
    """
    NVME_LOG_ANA_LSP_RGO_NAMESPACES				= 0,
    NVME_LOG_ANA_LSP_RGO_GROUPS_ONLY			= 1,

class NVME_LOG_PHY_RX_EOM_ACTION(Enum):
    """
        Physical Interface Receiver Eye Opening Measurement Action
    """
    NVME_LOG_PHY_RX_EOM_READ					= 0,        # Read Log Data
    NVME_LOG_PHY_RX_EOM_START_READ				= 1,        # Start Measurement and Read Log Data
    NVME_LOG_PHY_RX_EOM_ABORT_CLEAR				= 2,        # Abort Measurement and Clear Log Data

class NVME_LOG_PHY_RX_EOM_QUALITY(Enum):
    """
        Physical Interface Receiver Eye Opening Measurement Quality
    """
    NVME_LOG_PHY_RX_EOM_GOOD					= 0,        # <= Better Quality
    NVME_LOG_PHY_RX_EOM_BETTER					= 1,        # <= Best Quality, >= Good Quality
    NVME_LOG_PHY_RX_EOM_BEST					= 2,        # >= Better Quality

class NVME_PEVENT_LOG_ACTION(Enum):
    """
        Persistent Event Log - Action
    """
    NVME_PEVENT_LOG_READ			= 0x0,        # Read Log Data
    NVME_PEVENT_LOG_EST_CTX_AND_READ	= 0x1,        # Establish Context and Read Log Data
    NVME_PEVENT_LOG_RELEASE_CTX		= 0x2,        # Release Context

class NVME_FEATURE_TEMPTHRESH_THSEL(Enum):
    """
        Temperature Threshold - Threshold Type Select
    """
    NVME_FEATURE_TEMPTHRESH_THSEL_OVER			= 0,        # Over temperature threshold select
    NVME_FEATURE_TEMPTHRESH_THSEL_UNDER			= 1,        # Under temperature threshold select

class NVME_FEATURES_ASYNC_EVENT_CONFIG_FLAGS(Enum):
    """
        Asynchronous Event Configuration configuration flags
    """
    NVME_FEATURE_AENCFG_SMART_CRIT_SPARE			= 1 << 0,
    NVME_FEATURE_AENCFG_SMART_CRIT_TEMPERATURE		= 1 << 1,
    NVME_FEATURE_AENCFG_SMART_CRIT_DEGRADED			= 1 << 2,
    NVME_FEATURE_AENCFG_SMART_CRIT_READ_ONLY		= 1 << 3,
    NVME_FEATURE_AENCFG_SMART_CRIT_VOLATILE_BACKUP		= 1 << 4,
    NVME_FEATURE_AENCFG_SMART_CRIT_READ_ONLY_PMR		= 1 << 5,
    NVME_FEATURE_AENCFG_NOTICE_NAMESPACE_ATTRIBUTES		= 1 << 8,
    NVME_FEATURE_AENCFG_NOTICE_FIRMWARE_ACTIVATION		= 1 << 9,
    NVME_FEATURE_AENCFG_NOTICE_TELEMETRY_LOG		= 1 << 10,
    NVME_FEATURE_AENCFG_NOTICE_ANA_CHANGE			= 1 << 11,
    NVME_FEATURE_AENCFG_NOTICE_PL_EVENT			= 1 << 12,
    NVME_FEATURE_AENCFG_NOTICE_LBA_STATUS			= 1 << 13,
    NVME_FEATURE_AENCFG_NOTICE_EG_EVENT			= 1 << 14,
    NVME_FEATURE_AENCFG_NOTICE_DISCOVERY_CHANGE		= 1 << 31,

class NVME_FEAT_PLM_WINDOW_SELECT(Enum):
    """
        Predictable Latency Per NVM Set Log - Window Select
    """
    NVME_FEATURE_PLM_DTWIN					= 1,                # Deterministic Window select
    NVME_FEATURE_PLM_NDWIN					= 2,                # Non-Deterministic Window select


class NVME_FEATURE_RESERVATION_NOTIFY_FLAGS(Enum):
    """
        Reservation Notification Configuration
    """
    NVME_FEATURE_RESERVATION_NOTIFY_REGPRE		= 1 << 1,           # Mask Registration Preempted Notification
    NVME_FEATURE_RESERVATION_NOTIFY_RESREL		= 1 << 2,           # Mask Reservation Released Notification
    NVME_FEATURE_RESERVATION_NOTIFY_RESPRE		= 1 << 3,           # Mask Reservation Preempted Notification

class NVME_FEAT_NSWPCFG_STATE(Enum):
    """
        Write Protection - Write Protection State
    """
    NVME_FEAT_NSWPCFG_STATE_NO_WRITE_PROTECT		= 0,        # No Write Protect
    NVME_FEAT_NSWPCFG_STATE_WRITE_PROTECT		= 1,        # Write Protect
    NVME_FEAT_NSWPCFG_STATE_WRITE_PROTECT_PWR_CYCLE	= 2,        # Write Protect Until Power Cycle
    NVME_FEAT_NSWPCFG_STATE_WRITE_PROTECT_PERMANENT	= 3,        # Permanent Write Protect

class NVME_FCTYPE(Enum):
    """
        Fabrics Command Types
    """
    NVME_FCTYPE_PROPERTY_SET			= 0x00,     # Property set
    NVME_FCTYPE_CONNECT				= 0x01,     # Connect
    NVME_FCTYPE_PROPERTY_GET			= 0x04,     # Property Get
    NVME_FCTYPE_AUTH_SEND			= 0x05,     # Authentication Send
    NVME_FCTYPE_AUTH_RECEIVE			= 0x06,     # Authentication Receive
    NVME_FCTYPE_DISCONNECT			= 0x08,     # Disconnect

class NVME_DATA_TFR(Enum):
    """
        Data transfer direction of the command
    """
    NVME_DATA_TFR_NO_DATA_TFR			= 0x0,        # No data transfer
    NVME_DATA_TFR_HOST_TO_CTRL			= 0x1,        # Host to controller
    NVME_DATA_TFR_CTRL_TO_HOST			= 0x2,        # Controller to host
    NVME_DATA_TFR_BIDIRECTIONAL			= 0x3,        # Bidirectional

class NVME_IO_OPCODE(Enum):
    """
        I/O Command opcodes
    """
    NVME_IO_OPCODE_FLUSH				= 0x00,        # Flush
    NVME_IO_OPCODE_WRITE				= 0x01,        # Write
    NVME_IO_OPCODE_READ				= 0x02,        # Read
    NVME_IO_OPCODE_WRITE_UNCOR			= 0x04,        # Write Uncorrectable
    NVME_IO_OPCODE_COMPARE			= 0x05,        # Compare
    NVME_IO_OPCODE_WRITE_ZEROES			= 0x08,        # Write Zeros
    NVME_IO_OPCODE_DSM				= 0x09,        # Dataset Management
    NVME_IO_OPCODE_VERIFY				= 0x0c,        # Verify
    NVME_IO_OPCODE_RESV_REGISTER			= 0x0d,        # Reservation Register
    NVME_IO_OPCODE_RESV_REPORT			= 0x0e,        # Reservation Report
    NVME_IO_OPCODE_RESV_ACQUIRE			= 0x11,         # Reservation Acquire
    NVME_IO_OPCODE_IO_MGMT_RECV			= 0x12,        # I/O Management Receive
    NVME_IO_OPCODE_RESV_RELEASE			= 0x15,        # Reservation Release
    NVME_IO_OPCODE_COPY				= 0x19,        # Copy
    NVME_IO_OPCODE_IO_MGMT_SEND			= 0x1d,        # I/O Management Send
    NVME_IO_OPCODE_ZNS_MGMT_SEND			= 0x79,        # Zone Management Send
    NVME_IO_OPCODE_ZNS_MGMT_RECV			= 0x7a,        # Zone Management
    NVME_IO_OPCODE_ZNS_APPEND			= 0x7d,        # Zone Append

class NVME_IO_CONTROL_FLAGS(Enum):
    """
        I/O control flags
    """
    NVME_IO_DTYPE_STREAMS		= 1 << 4,               # Directive Type Streams
    NVME_IO_STC			= 1 << 8,                       # Storage Tag Check
    NVME_IO_DEAC			= 1 << 9,                   # Deallocate
    NVME_IO_ZNS_APPEND_PIREMAP	= 1 << 9,               # Protection Information Remap
    NVME_IO_PRINFO_PRCHK_REF	= 1 << 10,              # Protection Information Check Reference Tag
    NVME_IO_PRINFO_PRCHK_APP	= 1 << 11,              # Protection Information Check Application Tag
    NVME_IO_PRINFO_PRCHK_GUARD	= 1 << 12,              # Protection Information Check Guard field
    NVME_IO_PRINFO_PRACT		= 1 << 13,              # Protection Information Action
    NVME_IO_FUA			= 1 << 14,                      # Force Unit Access
    NVME_IO_LR			= 1 << 15,                      # Limited Retry

class NVME_IO_DSM_FLAGS(Enum):
    """
        Dataset Management flags
    """
    NVME_IO_DSM_FREQ_UNSPEC		= 0,                    # No frequency information provided
    NVME_IO_DSM_FREQ_TYPICAL	= 1,                    # Typical number of reads and writes expected for this LBA range
    NVME_IO_DSM_FREQ_RARE		= 2,                    # Infrequent writes and infrequent reads to the LBA range indicated
    NVME_IO_DSM_FREQ_READS		= 3,                    # Infrequent writes and frequent reads to the LBA range indicated
    NVME_IO_DSM_FREQ_WRITES		= 4,                    # Frequent writes and infrequent reads to the LBA range indicated
    NVME_IO_DSM_FREQ_RW		= 5,                        # Frequent writes and frequent reads to the LBA range indicated
    NVME_IO_DSM_FREQ_ONCE		= 6,                    # Once
    NVME_IO_DSM_FREQ_PREFETCH	= 7,                    # Prefetch
    NVME_IO_DSM_FREQ_TEMP		= 8,                    # Temperature sensitive
    NVME_IO_DSM_LATENCY_NONE	= 0 << 4,               # No latency information provided
    NVME_IO_DSM_LATENCY_IDLE	= 1 << 4,               # Longer latency acceptable
    NVME_IO_DSM_LATENCY_NORM	= 2 << 4,               # Typical latency
    NVME_IO_DSM_LATENCY_LOW		= 3 << 4,               # Smallest possible latency
    NVME_IO_DSM_SEQ_REQ		= 1 << 6,                   # Sequential request
    NVME_IO_DSM_COMPRESSED		= 1 << 7,               # Compressed data

class NVME_DSM_ATTRIBUTES(Enum):
    """
        Dataset Management attributes
    """
    NVME_DSMGMT_IDR		= 1 << 0,               # Attribute -Integral Dataset for Read
    NVME_DSMGMT_IDW		= 1 << 1,               # Attribute - Integral Dataset for Write
    NVME_DSMGMT_AD		= 1 << 2,               # Attribute - Deallocate

class NVME_RESERVATION_RTYPE(Enum):
    """
        Reservation Type Encoding
    """
    NVME_RESERVATION_RTYPE_WE		= 1,                    # Write Exclusive Reservation
    NVME_RESERVATION_RTYPE_EA		= 2,                    # Exclusive Access Reservation
    NVME_RESERVATION_RTYPE_WERO	= 3,                    # Write Exclusive - Registrants Only Reservation
    NVME_RESERVATION_RTYPE_EARO	= 4,                    # Exclusive Access - Registrants Only Reservation
    NVME_RESERVATION_RTYPE_WEAR	= 5                     # Write Exclusive - All Registrants Reservation
    NVME_RESERVATION_RTYPE_EAAR	= 6                     # Exclusive Access - All Registrants Reservation

class NVME_RESERVATION_RACQA(Enum):
    """
        Reservation Acquire - Reservation Acquire Action
    """
    NVME_RESERVATION_RACQA_ACQUIRE		= 0,                    # Acquire
    NVME_RESERVATION_RACQA_PREEMPT		= 1,                    # Preempt
    NVME_RESERVATION_RACQA_PREEMPT_AND_ABORT	= 2                     # Preempt and Abort

class NVME_RESERVATION_RREGA(Enum):
    """
        Reservation Register - Reservation Register Action
    """
    NVME_RESERVATION_RREGA_REGISTER_KEY		= 0,                    # Register Reservation Key
    NVME_RESERVATION_RREGA_UNREGISTER_KEY		= 1,                    # Unregister Reservation Key
    NVME_RESERVATION_RREGA_REPLACE_KEY		= 2                     # Replace Reservation Key

class NVME_RESERVATION_CPTPL(Enum):
    """
        Reservation Register - Change Persist Through Power Loss State
    """
    NVME_RESERVATION_CPTPL_NO_CHANGE		= 0,                    # No change to PTPL state
    NVME_RESERVATION_CPTPL_CLEAR			= 2,                    # Reservations are released and registrants are cleared on a power on
    NVME_RESERVATION_CPTPL_PERSIST			= 3                     # Reservations and registrants persist across a power loss

class NVME_RESERVATION_RRELA(Enum):
    """
        Reservation Release - Reservation Release Action
    """
    NVME_RESERVATION_RRELA_RELEASE		= 0,                    # Release
    NVME_RESERVATION_RRELA_CLEAR		= 1                     # Clear

class NVME_ZNS_SEND_ACTION(Enum):
    """
        Zone Management Send - Zone Send Action
    """
    NVME_ZNS_ZSA_CLOSE		= 0x1,                    # Close Zone
    NVME_ZNS_ZSA_FINISH		= 0x2,                    # Finish Zone
    NVME_ZNS_ZSA_OPEN		= 0x3,                    # Open Zone
    NVME_ZNS_ZSA_RESET		= 0x4,                    # Reset Zone
    NVME_ZNS_ZSA_OFFLINE		= 0x5,                    # Offline Zone
    NVME_ZNS_ZSA_SET_DESC_EXT	= 0x10,                   # Set Zone Descriptor Extension
    NVME_ZNS_ZSA_ZRWA_FLUSH		= 0x11                     # Flush

class NVME_ZNS_RECV_ACTION(Enum):
    """
        Zone Management Receive - Zone Receive Action Specific Features
    """
    NVME_ZNS_ZRA_REPORT_ZONES		= 0x0,          # Report Zones
    NVME_ZNS_ZRA_EXTENDED_REPORT_ZONES	= 0x1,      # Extended Report Zones

class NVME_ZNS_REPORT_OPTIONS(Enum):
    """
        Zone Management Receive - Zone Receive Action Specific Field
    """
    NVME_ZNS_ZRAS_REPORT_ALL		= 0x0,                  # List all zones
    NVME_ZNS_ZRAS_REPORT_EMPTY		= 0x1,                  # List the zones in the ZSE:Empty state
    NVME_ZNS_ZRAS_REPORT_IMPL_OPENED	= 0x2,              # List the zones in the ZSIO:Implicitly Opened state
    NVME_ZNS_ZRAS_REPORT_EXPL_OPENED	= 0x3,              # List the zones in the ZSEO:Explicitly Opened state
    NVME_ZNS_ZRAS_REPORT_CLOSED		= 0x4,                  # List the zones in the ZSC:Closed state
    NVME_ZNS_ZRAS_REPORT_FULL		= 0x5,                  # List the zones in the ZSF:Full state
    NVME_ZNS_ZRAS_REPORT_READ_ONLY		= 0x6,              # List the zones in the ZSRO:Read Only state
    NVME_ZNS_ZRAS_REPORT_OFFLINE		= 0x7,              # List the zones in the ZSO:Offline state

class NVME_IO_MGMT_RECV_MO(Enum):
    """
        I/O Management Receive - Management Operation
    """
    NVME_IO_MGMT_RECV_RUH_STATUS = 0x1,         # Reclaim Unit Handle Status

class NVME_IO_MGMT_SEND_MO(Enum):
    """
        I/O Management Send - Management Operation
    """
    NVME_IO_MGMT_SEND_RUH_UPDATE = 0x1,             # Reclaim Unit Handle Update


class nvme_ns_mgmt_host_sw_specified_zns(StructureBase):
    _fields_ = [
        ("znsco", c_uint8),                          # Zoned Namespace Create Options Bits 7-1: Reserved. Bits 0: Allocate ZRWA Resources (AZR): If set to ‘1’, then the namespace is to be created with the number of
                                                     # ZRWA resource specified in the RNUMZRWA  field of this data structure. If cleared to ‘0’, then no ZRWA resources are allocated to the namespace to be created.
                                                     # If the ZRWASUP bit is cleared to ‘0’, then this field shall be ignored by the controller.
        ("rar", c_uint32),                           # Requested Active Resources specifies the number of active resources to be allocated to the created namespace.
        ("ror", c_uint32),                           # Requested Open Resources specifies the number of open resources to be allocated to the created namespace.
        ("rnumzrwa", c_uint32),                      # Requested Number of ZRWA Resources specifies the number of ZRWA resources to be allocated to the created namespace. see &struct nvme_ns_mgmt_host_sw_specified_zns.
    ]

class nvme_ns_mgmt_host_sw_specified_item(Union):
    _fields_ = [
        ("zns", nvme_ns_mgmt_host_sw_specified_zns),
        ("rsvd499", c_char * 13),                       # Reserved for I/O Command Sets that extend this specification.
    ]

class nvme_ns_mgmt_host_sw_specified(StructureBase):
    """
        Namespace management Host Software
    """
    _fields_ = [
        ("nsze", c_uint64),                     # Namespace Size indicates the total size of the namespace in logical blocks. The number of logical blocks is based on the formatted LBA size.
        ("ncap", c_uint64),                     # Namespace Capacity indicates the maximum number of logical blocks that may be allocated in the namespace at any point in time. The number of logical blocks is based on the formatted LBA size.
        ("rsvd16", c_uint8 * 10),               # Reserved
        ("flbas", c_uint8),                     # Formatted LBA Size, see &enum nvme_id_ns_flbas.
        ("rsvd27", c_uint8 * 2),                # Reserved
        ("dps", c_uint8),                       # End-to-end Data Protection Type Settings, see&enum nvme_id_ns_dps.
        ("nmic", c_uint8),                      # Namespace Multi-path I/O and Namespace Sharing Capabilities, see &enum nvme_id_ns_nmic.
        ("rsvd31", c_uint8 * 61),               # Reserved
        ("anagrpid", c_uint32),                 # ANA Group Identifier indicates the ANA Group Identifier of the ANA group of which the namespace is a member.
        ("rsvd96", c_uint8 * 4),                # Reserved
        ("nvmsetid", c_uint16),                 # NVM Set Identifier indicates the NVM Set with which this namespace is associated.
        ("endgid", c_uint16),                   # Endurance Group Identifier indicates the Endurance Group with which this namespace is associated.
        ("rsvd104", c_uint8 * 280),             # Reserved
        ("lbstm", c_uint64),                    # Logical Block Storage Tag Mask Identifies the mask for the Storage Tag field for the protection information
        ("nphndls", c_uint16),                  # Number of Placement Handles specifies the number of Placement Handles included in the Placement Handle List
        ("rsvd394", c_uint8 * 105),             # Reserved
        ("item", nvme_ns_mgmt_host_sw_specified_item),
        ("phndl", c_uint16 * 128),              # Placement Handle Associated RUH : This field specifies the Reclaim Unit Handle Identifier to be associated with the Placement Handle value. If the Flexible Data Placement capability is
                                                # not supported or not enabled in specified Endurance Group, then the controller shall ignore this field.
        ("rsvd768", c_uint8 * 3328),            # Reserved
    ]