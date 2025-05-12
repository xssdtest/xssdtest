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



class ID(StructureBase):
    _fields_ = [("VID", c_uint16),                  # Vendor ID	                                                            VID	    0x00	0x01	2
                ("DID", c_uint16),                  # Device ID	                                                            DID	    0x02	0x03	2
    ]

class CMD(StructureBase):
    _fields_ = [("IOSE", c_uint16, 1),                # I/O Space Enable	                                                CMD	    0x00	0x00	1
                ("MSE", c_uint16, 1),                 # Memory Space Enable	                                                DCTL	0x01	0x01	1
                ("BME", c_uint16, 1),                 # Bus Master Enable	                                                DSTS	0x02	0x02	1
                ("SCE", c_uint16, 1),                 # Special Cycle Enable                                                SCE     0x03	0x03	1
                ("MWIE", c_uint16, 1),                # Memory Write and Invalidate Enable	                                MWIE	0x04	0x04	1
                ("VGA", c_uint16, 1),                 # VGA Palette Snooping Enable	                                        VGA	    0x05	0x05	1
                ("PEE", c_uint16, 1),                 # Parity Error Response Enable                                        PEE     0x06    0x06    1
                ("Reserved", c_uint16, 1),            # Hardwired to 0.                                                     RSV     0x07    0x07    1
                ("SEE", c_uint16, 1),                 # SERR# Enable                                                        SEE     0x08    0x08    1
                ("FBE", c_uint16, 1),                 # Fast Back-to-Back Enable                                            FBE     0x09    0x09    1
                ("ID", c_uint16, 1),                  # Interrupt Disable                                                   ID      0x0A    0x0A    1
                ("Reserved1", c_uint16, 5),           # Reserved	                                                        RSV	    0x0B	0x0F	5
    ]

class STS(StructureBase):
    _fields_ = [("Reserved", c_uint16, 3),            # Reserved	                                                        RSV	    0x00	0x02	3
                ("IS", c_uint16, 1),                  # Interrupt Status	                                                IS  	0x03	0x03	1
                ("CL", c_uint16, 1),                  # Capabilities List	                                                DSTS	0x04	0x04	1
                ("C66", c_uint16, 1),                 # 66 MHz Capable                                                      C66     0x05	0x05	1
                ("Reserved1", c_uint16, 1),           # Reserved	                                                        RSV 	0x06	0x06	1
                ("FBC", c_uint16, 1),                 # Fast Back-to-Back Capable	                                        FBC	    0x07	0x07	1
                ("PEE", c_uint16, 1),                 # Master Data Parity Error Detected                                   DPD     0x08    0x08    1
                ("DEVT", c_uint16, 1),                # DEVSEL# Timing                                                      DEVT    0x09    0x0A    2
                ("STA", c_uint16, 1),                 # Signaled Target-Abort                                               STA     0x0B    0x0B    1
                ("RTA", c_uint16, 1),                 # Received Target Abort                                               RTA     0x0C    0x0C    1
                ("RMA", c_uint16, 1),                 # Received Master-Abort                                               RMA     0x0D    0x0D    1
                ("SSE", c_uint16, 1),                 # Signaled System Error	                                            SSE	    0x0E	0x0E	1
                ("DPE", c_uint16, 1),                 # Detected Parity Error	                                            DPE	    0x0E	0x0E	1
    ]

class ClassCode(StructureBase):
    _fields_ = [("PI", c_uint8),                      # Programming Interface	                                            PI	    0x00	0x07	8
                ("SCC", c_uint8),                     # Sub Class Code	                                                    SCC	    0x08	0x0F	8
                ("BCC", c_uint8),                     # Programming Interface	                                            BCC	    0x10	0x17	8
    ]

class HTYPE(StructureBase):
    _fields_ = [("HL", c_uint8, 7),                   # Header Layout	                                                    HL	    0x00	0x06	7
                ("MFD", c_uint8, 1),                  # Multi-Function Device	                                            MFD 	0x07	0x07	1
    ]

class BIST(StructureBase):
    _fields_ = [("CC", c_uint8, 4),                  # Completion Code	                                                CC  	0x00	0x03	4
                ("Reserved", c_uint8, 2),            # Reserved	                                                        RSV	    0x04	0x05	2
                ("SB", c_uint8, 1),                  # Start BIST	                                                    SB	    0x06	0x06	1
                ("BC", c_uint8, 1),                  # BIST Capable	                                                    BC	    0x07	0x07	1
    ]

class BAR0(StructureBase):
    _fields_ = [("RTE", c_uint32, 1),                # Resource Type Indicator	                                        RTE	    0x00	0x00	1
                ("TP", c_uint32, 2),                 # Type	                                                            TP  	0x01	0x02	2
                ("PF", c_uint32, 1),                 # Prefetchable                                                     PF	    0x03	0x03	1
                ("Reserved", c_uint8, 2),            # Reserved	                                                        RSV	    0x04	0x0C	10
                ("BA", c_uint32, 18),                # Base Address                                                     BA	    0x0E	0x1F	18
    ]

class BAR2(StructureBase):
    _fields_ = [("RTE", c_uint32, 1),                # Resource Type Indicator	                                        RTE	    0x00	0x00	1
                ("TP", c_uint32, 2),                 # Type	                                                            TP  	0x01	0x02	2
                ("BA", c_uint32, 29),                # Base Address                                                     BA	    0x03	0x1F	29
    ]

class SS(StructureBase):
    _fields_ = [("SSVID", c_uint16),                 # Subsystem Vendor ID	                                            SSVID	0x00	0x0F	16
                ("SSID", c_uint16),                  # Subsystem ID	                                                    SSID  	0x10	0x1F	16
    ]

class INTR(StructureBase):
    _fields_ = [("ILINE", c_uint16),                 # Interrupt Line	                                                ILINE	0x00	0x0F	16
                ("IPIN", c_uint16),                  # Interrupt Pin	                                                IPIN  	0x10	0x1F	16
    ]

class PcieHeader(StructureBase):
    _fields_ = [ ("ID", c_uint32),                  # Identifiers                                                            ID	    0x00	0x03	4
                 ("CMD", c_uint16),                 # Command Register                                                       CMD	0x04    0x05    2
                 ("STS", c_uint16),                 # Device Status	                                                         STS	0x06	0x07	2
                 ("RID", c_uint8),                  # Revision ID	                                                         RID	0x08	0x08	1
                 ("CC", c_uint8 * 3),               # Class Code	                                                         CC	    0x09	0x0B	3
                 ("CLS", c_uint8),                  # Cache Line Size	                                                     CLS	0x0C	0x0C	1
                 ("MLT", c_uint8),                  # Master Latency Timer                                                   MLT	0x0D	0x0D	1
                 ("HTYPE", c_uint8),                # Header Type	                                                         HTYPE	0x0E	0x0E	1
                 ("BIST", c_uint8),                 # Built-in Self Test	                                                 BIST	0x0F	0x0F	1
                 ("BAR0", c_uint32),                # Memory Register Base Address, lower 32-bits                            BAR0   0x10    0x13    4
                 ("BAR1", c_uint32),                # Memory Register Base Address, upper 32-bits                            BAR1   0x14    0x17    4
                 ("BAR2", c_uint32),                # Refer to section                                                       BAR2   0x18    0x1B    4
                 ("BAR3", c_uint32),                # Vendor Specific                                                        BAR3   0x1C    0x1F    4
                 ("BAR4", c_uint32),                # Vendor Specific                                                        BAR4   0x20    0x23    4
                 ("BAR5", c_uint32),                # Vendor Specific                                                        BAR5   0x24    0x27    4
                 ("CCPTR", c_uint32),               # CardBus CIS Pointer	                                                 CCPTR	0x28	0x2B	4
                 ("SS", c_uint32),                  # Subsystem Identifiers	                                                 SS 	0x2C	0x2F	4
                 ("EROM", c_uint32),                # Expansion ROM Base Address	                                         EROM   0x30    0x33    4
                 ("CAP", c_uint8),                  # Capabilities Pointer	                                                 CAP    0x34    0x34    1
                 ("Reserved1", c_uint8 * 7),        # Reserved	                                                             RSV    0x35    0x3B    7
                 ("INTR", c_uint16),                # Interrupt Information	                                                 INTR   0x3C    0x3D    2
                 ("MGNT", c_uint8),                 # Interrupt Pin	                                                         MGNT   0x3E    0x3E    1
                 ("MLAT", c_uint8),                 # Interrupt Pin	                                                         MLAT   0x3F    0x3F    1
    ]
    def __init__(self):
        super(PcieHeader, self).__init__()
        self.format_dict = {item[0]:self.to_int for item in self._fields_ if not self.skip_reserved_pattern.search(item[0].upper())}
