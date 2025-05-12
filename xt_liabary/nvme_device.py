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
from xt_liabary.nvme.nvme_bar import NvmeBar
from xt_liabary.nvme.nvme_command import *
from xt_liabary.qpair import *
from xt_liabary.buffer import *
from xt_liabary.ssh import *
from xt_liabary.nvme.nvme_structure import *
from xt_liabary.power_cycle import PowerCycle
from xt_module.xt_structure import *
from xt_module.xt_system import SystemCmd
from xt_platform import xt_interface as xt
vendor_id_dict = {'0x1d0f':"amzn",        "0x1028":"dell",     "0x1d78":"dera",       "0x19e5":"huawei",
                  "0x1dbe":"innogrit",    "0x8086":"intel",    "0x1c5f":"memblaze",   "0x1344":"micron",
                  "0x1275":"netapp",      "0x10de":"nvidia",   "0xcc53":"scaleflux",  "0x1bb1":"seagate",
                  "0x1cb0":"shannon",     "0x144d":"samsung",  "0x1179":"toshiba",    "0x1f9f":"virtium",
                  "0x1d79":"transcend",   "0x1b96":"wdc",      "0x1e49":"ymtc",       "0x1e3b":"dapu" }

nvme_ver_dict = {"1.0": 0x00010000, "1.1": 0x00010100, "1.2": 0x00010200, "1.2.1": 0x00010201,
                 "1.3": 0x00010300, "1.4": 0x00010400, "2.0": 0x00020000, "2.1": 0x00020100,}
class CompletionEntry(StructureBase):
    _fields_ = [ ('cpl_cdw0', c_uint32),
                 ('cpl_sqhd', c_uint32),
                 ('cpl_sqhd', c_int16),
                 ('cpl_sqid', c_int16),
                 ('cpl_cid', c_int16),
                 ('cpl_phase_tag', c_uint16, 1),
                 ('cpl_sc', c_uint16, 8),
                 ('cpl_sct', c_uint16, 3),
                 ('cpl_rsvd2', c_uint16, 2),
                 ('cpl_more', c_uint16, 1),
                 ('cpl_dnr', c_uint16, 1),
                 ('complete_time', c_uint64),
    ]

class NvmeDevice(object):
    """
    A class representing an NVMe device, providing comprehensive management and control over the device's features.

    This class encapsulates NVMe device initialization, configuration, command submission,
    namespace handling, and vendor-specific operations. It integrates with test infrastructure
    to support both standard and custom NVMe commands.

    Attributes:
        test_inst (object): Reference to the test instance for global test settings.
        environment (Environment): System environment information.
        logger (Logger): Logging utility for tracking device behavior and errors.
        pci_info (str): PCIe address of the NVMe device.
        pcie_path (str): Filesystem path to the PCIe device node.
        __device_fini_flag (bool): Internal flag indicating whether the device has been finalized.
        admin_cmds_timeout (int): Admin command timeout value in microseconds.
        io_cmds_timeout (int): I/O command timeout value in microseconds.
        buffer (Buffer): Utility for managing memory buffers used in I/O operations.
        engine_opt_name (str): Engine type name (e.g., 'spdk_nvme').
        nvme_version (int): NVMe specification version supported by the controller.
        vendor_spec_path (str): Path to vendor-specific implementation if available.
        system_cmds (SystemCmd): Interface for executing system-level shell commands.
        hugepage (int): Size of hugepages allocated for this device.
        pci_whitelist (str): List of allowed PCI devices for filtering.
        max_ioqueue_entry (int): Maximum number of I/O queue entries.
        driver_inst (XT_DRIVER): Underlying driver interface (SPDK or Linux).
        device_inst (XT_DEVICES): Device abstraction layer for command execution.
        qpair_inst (QueuePair): Manages I/O queue pairs associated with this device.
        vendor_commands (VendorCommands): Vendor-specific command set if available.
        nvme_regs (CtrlRegister): Register interface for low-level controller access.
        id_ctrl (IdentifyCtrl): Controller identify data structure.
        smart_log (SmartLog): SMART log interface for health monitoring.
        firmware_manager (FirmwareManager): Firmware update and control utilities.
        power_cycle (PowerCycle): Power cycle control utilities.
    """

    def __init__(self, pci_info, test_inst):
        """
        Initializes a new instance of NvmeDevice with the given PCI info and test context.

        Parameters:
            pci_info (str): The PCIe address of the NVMe device.
            test_inst (object): Reference to the test case object containing environment and config.

        Raises:
            AssertionError: If the device is not found on the PCIe bus and is not a simulator.
        """
        self.test_inst = test_inst
        assert test_inst is not None, print("Test instance is not exist")

        # Test context and logging
        self.environment = self.test_inst.environment
        self.logger = self.test_inst.logger
        self.pci_info = pci_info

        # System paths
        self.pcie_path = os.path.join("/sys/bus/pci/devices", self.pci_info)
        self.pcie_config = os.path.join(self.pcie_path, "config")
        self.__device_fini_flag = True

        # Validate existence of physical device unless it's a simulator
        assert os.path.isfile(self.pcie_path) or "0000:00:00.0" in self.pci_info, self.logger.error("PCI info %s is not exist" % self.pci_info)

        # Set command timeouts from test instance or use defaults
        self.admin_cmds_timeout = 1000000 * 300 if self.test_inst.admin_cmds_timeout is None else self.test_inst.admin_cmds_timeout
        self.io_cmds_timeout = 1000000 * 300 if self.test_inst.io_cmds_timeout is None else self.test_inst.io_cmds_timeout
        self.dsm_cmds_timeout = 1000000 * 300 if self.test_inst.dsm_cmds_timeout is None else self.test_inst.dsm_cmds_timeout
        self.fw_active_cmds_timeout = 1000000 * 300 if self.test_inst.fw_active_cmds_timeout is None else self.test_inst.fw_active_cmds_timeout
        self.vu_timeout = 1000000 * 300 if self.test_inst.vu_timeout is None else self.test_inst.vu_timeout
        self.format_timeout = 1000000 * 300 if self.test_inst.format_timeout is None else self.test_inst.format_timeout
        self.sanitize_timeout = 1000000 * 300 if self.test_inst.sanitize_timeout is None else self.test_inst.sanitize_timeout
        self.shutdown_timeout = 100000 * 300 if self.test_inst.shutdown_timeout is None else self.test_inst.shutdown_timeout
        self.power_failed_timeout = 1000000 * 300 if self.test_inst.power_failed_timeout is None else self.test_inst.power_failed_timeout
        self.probe_timeout = 1000000 * 300 if self.test_inst.probe_timeout is None else self.test_inst.probe_timeout
        self.reset_timeout = 1000000 * 300 if self.test_inst.reset_timeout is None else self.test_inst.reset_timeout

        # Initialize helper components
        self.buffer = Buffer(self.logger)
        self.engine_opt_name = self.test_inst.engine_type
        self.switch_driver()
        self.nvme_version = self.get_nvme_version() if self.test_inst.nvme_version is None else nvme_ver_dict.get(self.test_inst.nvme_version, 0x00020000)
        self.vendor_name = None if self.test_inst.vendor_name is None else self.test_inst.vendor_name.lower()
        self.vendor_spec_path = self.get_vendor_spec_path()
        self.nvme_spec_path = self.get_nvme_spec_path()

        # Command execution and hardware interaction tools
        self.system_cmds = SystemCmd(self.logger)
        self.hugepage = self.test_inst.hugepage
        self.pci_whitelist = self.test_inst.pci_whitelist
        self.max_ioqueue_entry = self.get_max_queue_entries()
        qdepth = 128 if self.max_ioqueue_entry > 128 else self.max_ioqueue_entry

        # Initialize underlying driver and device interfaces
        self.driver_inst = xt.XT_DRIVER(self.pci_info, self.engine_opt_name, logger=self.logger, mem_size=self.hugepage, pci_whitelist=self.pci_whitelist)
        self.device_inst = xt.XT_DEVICES(driver=self.driver_inst, logger=self.logger, qdepth=qdepth)

        # Queue management and command interfaces
        self.qpair_inst = QueuePair(self)

        # Load optional vendor-specific command module
        if self.vendor_spec_path is not None:
            self.vendor_module = self.test_inst.path_import.module_import_from_path(self.vendor_spec_path)
            self.vendor_commands = self.vendor_module.VendorCommands(device=self)
        else:
            self.vendor_module = None
            self.vendor_commands = None

        # Load NVMe spec module and register interface
        self.nvme_spec_module = self.test_inst.path_import.module_import_from_path(self.nvme_spec_path)
        self.nvme_regs = CtrlRegister(self, update=True)
        self.id_ctrl = IdentifyCtrl(self, self.device_inst.id_ctrl_raws, update=False)

        # Derived device properties
        self.max_data_transfer_size = (2 ** self.id_ctrl.mdts) * (2 ** (12 + self.nvme_regs.ctrl_reg.CAP.MPSMIN))
        self.admin_max_data_transfer_size = self.max_data_transfer_size if self.test_inst.admin_max_data_transfer_size is None else self.test_inst.admin_max_data_transfer_size
        self.sq_entries, self.cq_entries = self.get_io_queue_entries()
        self.max_queues_entries = self.nvme_regs.ctrl_reg.CAP.MQES + 1
        self.fw_version = self.id_ctrl.id_ctrl.fr
        self.pci_vendor_id = self.id_ctrl.vid
        self.sub_vendor_id = self.id_ctrl.ssvid
        self.model_number = self.id_ctrl.id_ctrl.mn
        self.serial_number = self.id_ctrl.id_ctrl.sn

        # Command sets
        self.nvme_commands = NvmeCommands(self)

        # Namespace management
        self.init_namespace()
        self.default_nsid = self.device_inst.active_ns[0] if self.test_inst.default_nsid is None else self.test_inst.default_nsid
        self.max_lba = self.ns[self.default_nsid].max_lba
        self.sector_size = self.ns[self.default_nsid].sector_size

        # Log interfaces
        self.smart_log = SmartLog(self)
        self.smart_log_add = SmartLogAdd(self)
        self.device_self_test = DeviceSelfTest(self)
        self.lba_status = LBAStatus(self)
        self.telemetry_log = TelemetryLog(self)
        self.persist_event_log = PersistentEventLog(self)
        self.error_log = ErrorLog(self)
        self.effect_log = EffectLog(self)

        # Manager objects
        self.namespace_manager = NamespaceManager(self)
        self.firmware_manager = FirmwareManager(self)

        # Plugin modules
        self.mi_module = self.test_inst.path_import.module_import_from_path("xt_liabary/nvme/plugins/management_interface/mi.py")
        self.mi_command = self.mi_module.MICommands(device=self)
        self.fdp_module = self.test_inst.path_import.module_import_from_path("xt_liabary/nvme/plugins/flexible_data_placement/fdp.py")
        self.fdp_command = self.fdp_module.FDPCommands(device=self)
        self.kv_module = self.test_inst.path_import.module_import_from_path("xt_liabary/nvme/plugins/key_value/key_value.py")
        self.kv_command = self.kv_module.KVCommands(device=self)
        self.ocp_module = self.test_inst.path_import.module_import_from_path("xt_liabary/nvme/plugins/open_compute_project/ocp.py")
        self.ocp_command = self.ocp_module.OCPCommands(device=self)
        self.tcg_module = self.test_inst.path_import.module_import_from_path("xt_liabary/nvme/plugins/trusted_computing_group/tcg.py")
        self.tcg_command = self.tcg_module.TCGCommands(device=self)
        self.zns_module = self.test_inst.path_import.module_import_from_path("xt_liabary/nvme/plugins/zone_namespace/zns.py")
        self.zns_command = self.zns_module.ZNSCommands(device=self)
        self.extend_tool_module = self.test_inst.path_import.module_import_from_path("xt_liabary/extend_tool/extend_tool.py")
        self.extend_tool = self.extend_tool_module.ExtendTool(self)

        # Optional vendor-specific command interface
        self.vu_command = self.vendor_commands.load_vendor_unique_command() if hasattr(self.vendor_commands, "load_vendor_unique_command") else None

        # Power cycle manager
        self.power_cycle = PowerCycle(self)


    def init_namespace(self):
        nn = max(self.id_ctrl.nn, self.id_ctrl.mnan) + 2
        self.ns = [None] * nn
        for nsid in self.device_inst.active_ns:
            raw_data = self.device_inst.id_ns_raws_dict.get(nsid, None)
            self.ns[nsid] = NameSpace(self, nsid, raw_data)
    def update_namespace(self):
        self.device_inst.update_name_spaces()
        self.id_ctrl.update()
        nn = max(self.id_ctrl.nn, self.id_ctrl.mnan) + 2
        if nn > len(self.ns):
            self.ns = self.ns + [None] * (nn - len(self.ns))
        for nsid in range(nn):
            if nsid in self.device_inst.active_ns:
                raw_data = self.device_inst.id_ns_raws_dict.get("%s"%nsid, None)
                if self.ns[nsid] is None:
                    self.ns[nsid] = NameSpace(self, nsid, raw_data)
                else:
                    self.ns[nsid].update_id_namespace(raw_data)
            else:
                self.ns[nsid] = None

    def update_mdts(self):
        if "null" in self.engine_opt_name:
            return 1024 * 1024 // 512
        else:
            self.id_ctrl.update()
            self.nvme_regs.update()
            self.max_data_transfer_size = (2 ** self.id_ctrl.mdts) * (2 ** (12 + self.nvme_regs.ctrl_reg.CAP.MPSMIN))

    def update_max_lba_and_sector_size(self, nsid=None):
        if nsid is None:
            self.device_inst.update_name_spaces()
        else:
            if self.ns[nsid] is None:
                self.ns[nsid] = NameSpace(self, nsid)
            self.ns[nsid].update_id_namespace()
            if nsid == self.default_nsid:
                self.max_lba = self.ns[self.default_nsid].max_lba
                self.sector_size = self.ns[self.default_nsid].sector_size

    def get_io_queue_entries(self):
        if "null" in self.engine_opt_name:
            return 1024, 1024
        else:
            rtn_cmds_u = self.nvme_commands.admin_feature_number_of_queues(rtn_cmds_u_addr=True)
            cqe = self.parse_command_return(rtn_cmds_u)
            return cqe.cpl_cdw0 & 0xFFFF, cqe.cpl_cdw0 >> 16

    def get_ctrl_device(self):
        if 'nvme' in self.driver:
            path = "/sys/bus/pci/devices/%s/nvme/"%self.pci_info
            if os.path.exists(path):
                ctrl_device = os.popen("ls /sys/bus/pci/devices/%s/nvme/" % self.pci_info).read().strip()
                assert ctrl_device, self.logger.error("Get a invalid device info %s"%ctrl_device)
                return ctrl_device
            else:
                ctrl_device = os.popen("ls /dev/nvme*").read()
                self.logger.info("Get Block Device: Current Device Info %s"%ctrl_device)
                return None
        else:
            return None
    def get_nvme_version(self):
        if "0000:00:00.0" in self.pci_info:
            return nvme_ver_dict["2.0"]
        else:
            nvme_bar = NvmeBar(self.pci_info, 0)
            return nvme_bar.get_int_value(0x8)

    def get_max_queue_entries(self):
        if "0000:00:00.0" in self.pci_info:
            return 1024
        else:
            nvme_bar = NvmeBar(self.pci_info, 0)
            return nvme_bar.get_short_value(0x0) + 1

    def get_nvme_spec_path(self):
        if self.nvme_version >= nvme_ver_dict["2.0"]:
            return os.path.join(self.test_inst.project_path, "xt_liabary/nvme/nvme_spec_v2_0.py")
        else:
            return os.path.join(self.test_inst.project_path, "xt_liabary/nvme/nvme_spec_v1_4.py")

    def get_vendor_spec_path(self):
        vendor_id, vendor_spec_path = None, None
        if self.vendor_name is None:
            vendor_path = os.path.join(self.pcie_path, "vendor")
            if os.path.exists(vendor_path):
                with open(vendor_path, "r") as f:
                    vendor_id = f.read()
                    vendor_name = vendor_id_dict.get(vendor_id, None)
            self.vendor_name = vendor_name
        else:
            vendor_name = self.vendor_name
        if vendor_name:
            vendor_spec_path = os.path.join(self.test_inst.project_path, f"xt_liabary/nvme/vendor/{vendor_name}/{vendor_name}.py")
        return vendor_spec_path

    def get_driver(self):
        if "0000:00:00.0" in self.pci_info:
            self.driver = "simulator"
        else:
            cmdline = "lspci -s %s -v | grep -i driver"%(self.pci_info)
            ret = self.system_cmds.send_cmd(cmdline, stdout=True)
            assert ret, self.logger.error("%s return None")
            self.driver = ret.split(":")[1].strip()
    def switch_spdk_driver(self):
        if 'uio' in self.driver or 'vfio' in self.driver:
            self.logger.info("current driver is %s"%self.driver)
        else:
            setup_path = os.path.join(self.test_inst.project_path, "setup.sh")
            cmdline = "sh %s config %s"%(setup_path, self.pci_info)
            self.system_cmds.send_cmd(cmdline, check_ret=True, check_pass=True, check_code=0, raise_flag=True, get_status_output=False)
            self.get_driver()
            if not ('uio' in self.driver or 'vfio' in self.driver):
                assert False, self.logger.error("switch spdk driver failed")
    def switch_nvme_driver(self):
        if 'nvme' in self.driver:
            self.logger.info("current driver is %s"%self.driver)
        else:
            setup_path = os.path.join(self.test_inst.project_path, "setup.sh")
            cmdline = "sh %s reset %s"%(setup_path, self.pci_info)
            self.system_cmds.send_cmd(cmdline, check_ret=True, check_pass=True, check_code=0, raise_flag=True, get_status_output=False)
            self.get_driver()
            if not ('nvme' in self.driver):
                assert False, self.logger.error("switch nvme driver failed")

    def switch_driver(self, engine_opt_name=None):
        engine_opt_name = engine_opt_name if engine_opt_name else self.engine_opt_name
        self.logger.info("Load engine is %s" % engine_opt_name)
        if "0000:00:00.0" in self.pci_info:
            if not hasattr(self, "driver"):
                self.get_driver()
        else:
            if "spdk" in engine_opt_name.lower():
                self.switch_spdk_driver()
            elif "nvme" in engine_opt_name.lower():
                self.switch_nvme_driver()
            else:
                assert False, self.logger.error("Invalid engine name %s"%engine_opt_name)
    def parse_command_return(self, cmd_u: int):
        cqe = CompletionEntry()
        cqe.from_tuple(self.device_inst.xt_parse_cmd_cpl(cmd_u))
        return cqe

    def wait_admin_cmd_completed(self, admin_unit: int, timeout_tick=None):
        timeout_tick = timeout_tick if timeout_tick else self.admin_cmds_timeout
        cmd_u = self.device_inst.wait_admin_cmd_completed(admin_unit, timeout_tick)
        return self.parse_command_return(cmd_u)

    def send_admin_cmds(self, opcode, buf, fuse=0, psdt=0, cid=0, nsid=1, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0,  cdw13=0, cdw14=0,
                        cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=True, timeout=1000000, io_status_code_expected=0,
                        io_status_code_type_expected=0):
        cmd_u = self.device_inst.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cid=cid, nsid=nsid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                                 prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15,
                                                 buf_size=buf_size, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                                 io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)
        return cmd_u

    def get_io_submit_status(self, qpair, iodepth=None):
        io_status_list = self.device_inst.get_io_submit_status(qpair, iodepth=iodepth)
        return io_status_list

    def wait_io_completion(self, qpair, timeout_tick=None):
        timeout_tick = timeout_tick if timeout_tick else self.io_cmds_timeout
        self.device_inst.wait_io_completion(qpair, timeout_tick)

    def wait_completion_qpair(self, qpair=None):
        qpair_list = self.qpair_inst.get_qpairs() if qpair is None else [qpair]
        for qpair in qpair_list:
            if self.qpair_inst.get_qpairs(qpair):
                self.wait_admin_cmd_completed(qpair.qpair_u)

    def send_io_cmds(self, opcode, buf, qpair, fuse=0, psdt=0, cid=0, nsid=1, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0,
                     cdw15=0, buf_size=0, wait_completed=0, rtn_cmds_u_addr=0, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                     io_tailer_flag=0, pi_type=0):
        timeout = self.io_cmds_timeout if timeout is None else timeout
        io_u = self.device_inst.send_io_cmds(opcode=opcode, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, nsid=nsid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                             prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size,
                                             wait_completed=wait_completed, rtn_io_u_addr=rtn_cmds_u_addr, timeout=timeout, io_status_code_expected=io_status_code_expected,
                                             io_status_code_type_expected=io_status_code_type_expected, io_tailer_flag=io_tailer_flag, pi_type=pi_type)
        return io_u

    def send_io_read(self, qpair, slba=None, lbacnt=None, elba=0, cdw2=0, cdw3=0, cdw13=0, cdw14=0, cdw15=0, limitedRetry=0, fua=0, prinfo=0, dtype=0,
                     sector_size=512, meta_sector_size=0, reap_type=0, qdepth=0, nsid=1, timeout=None, readbuf_list=None, status_check=True, io_check_type=1,
                     writebuf_list=None, limit_iops_count=0, limit_io_count=0, microseconds_delay=0, wait_completed=1, pi_type=0, psdt=0):
        timeout = self.io_cmds_timeout if timeout is None else timeout
        self.device_inst.send_io_read(qpair=qpair, slba=slba, lbacnt=lbacnt, elba=elba, cdw2=cdw2, cdw3=cdw3, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15,
                                      limitedRetry=limitedRetry, fua=fua, prinfo=prinfo, dtype=dtype, sector_size=sector_size, meta_sector_size=meta_sector_size,
                                      reap_type=reap_type, qdepth=qdepth, nsid=nsid, timeout=timeout, readbuf_list=readbuf_list, status_check=status_check,
                                      io_check_type=io_check_type, writebuf_list=writebuf_list, limit_iops_count=limit_iops_count, limit_io_count=limit_io_count,
                                      microseconds_delay=microseconds_delay, wait_completed=wait_completed, pi_type=pi_type, psdt=psdt)

    def send_io_write(self, qpair, slba=None, lbacnt=None, elba=0, cdw2=0, cdw3=0, cdw13=0, cdw14=0, cdw15=0, limitedRetry=0, fua=0, prinfo=0, dtype=0, sector_size=512,
                      meta_sector_size=0, reap_type=0, qdepth=0, nsid=1, timeout=None, status_check=True, limit_iops_count=0, limit_io_count=0, microseconds_delay=0,
                      io_tailer_flag=0, wait_completed=1, writebuf_list=None, pi_type=0, psdt=0):
        timeout = self.io_cmds_timeout if timeout is None else timeout
        self.device_inst.send_io_write(qpair=qpair, slba=slba, lbacnt=lbacnt, elba=elba, cdw2=cdw2, cdw3=cdw3, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15,
                                       limitedRetry=limitedRetry, fua=fua, prinfo=prinfo, dtype=dtype, sector_size=sector_size, meta_sector_size=meta_sector_size,
                                       reap_type=reap_type, qdepth=qdepth, nsid=nsid, timeout=timeout, status_check=status_check, limit_iops_count=limit_iops_count,
                                       limit_io_count=limit_io_count, microseconds_delay=microseconds_delay, io_tailer_flag=io_tailer_flag, wait_completed=wait_completed,
                                       writebuf_list=writebuf_list, pi_type=pi_type, psdt=psdt)

    def send_io_sequences(self, qpair, io_sequences, psdt=0, bs=8, qdepth=1, slba=0, elba=None, size=0, random_mode=True, mix_write=100, runTime=0, writebuf_list=[],
                          readbuf_list=[], sector_size=512, meta_sector_size=0, nsid=1, pi_type=0, timeout=100000, checkPass=1, aligned=1, cdw2=0, cdw3=0, cdw13=0,
                          cdw14=0, cdw15=0, reap_type=0, io_tailer_flag=0, io_check_type=1, lcg_radom=1, reset_lcg=0):
        timeout = self.io_cmds_timeout if timeout is None else timeout
        elba = elba if elba is not None else self.ns[nsid].max_lba
        self.device_inst.send_io_sequences(qpair=qpair, io_sequences=io_sequences, psdt=psdt, bs=bs, qdepth=qdepth, slba=slba, elba=elba, size=size, random_mode=random_mode,
                                           mix_write=mix_write, runTime=runTime, writebuf_list=writebuf_list, readbuf_list=readbuf_list, sector_size=sector_size,
                                           meta_sector_size=meta_sector_size, nsid=nsid, pi_type=pi_type, timeout=timeout, checkPass=checkPass, aligned=aligned, cdw2=cdw2,
                                           cdw3=cdw3, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, reap_type=reap_type, io_tailer_flag=io_tailer_flag, io_check_type=io_check_type,
                                           lcg_radom=lcg_radom, reset_lcg=reset_lcg)

    def send_random_write_full(self, qpair, psdt=0, bs=8, qdepth=1, slba=0, elba=None, sector_size=512, meta_sector_size=0, nsid=1, timeout=None, checkPass=1, pi_type=0,
                               writebuf_list=None, rand_reset=0, reap_type=0, io_tailer_flag=0, cdw2=0, cdw3=0, cdw13=0, cdw14=0, cdw15=0, reset_lcg=0):
        timeout = self.io_cmds_timeout if timeout is None else timeout
        elba = elba if elba is not None else self.ns[nsid].max_lba
        self.device_inst.send_random_write_full(qpair=qpair, psdt=psdt, bs=bs, qdepth=qdepth, slba=slba, elba=elba, sector_size=sector_size, meta_sector_size=meta_sector_size,
                                                nsid=nsid, timeout=timeout, checkPass=checkPass, pi_type=pi_type, writebuf_list=writebuf_list, rand_reset=rand_reset,
                                                reap_type=reap_type, io_tailer_flag=io_tailer_flag, cdw2=cdw2, cdw3=cdw3, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15,
                                                reset_lcg=reset_lcg)

    def send_random_read_full(self, qpair, psdt=0, bs=8, qdepth=1, slba=0, elba=None, sector_size=512, meta_sector_size=0, nsid=1, timeout=None, checkPass=1, pi_type=0,
                              writebuf_list=None, readbuf_list=None, rand_reset=0, reap_type=0, io_check_type=1, cdw2=0, cdw3=0, cdw13=0, cdw14=0, cdw15=0, reset_lcg=0):
        timeout = self.io_cmds_timeout if timeout is None else timeout
        elba = elba if elba is not None else self.ns[nsid].max_lba
        self.device_inst.send_random_read_full(qpair=qpair, psdt=psdt, bs=bs, qdepth=qdepth, slba=slba, elba=elba, sector_size=sector_size, meta_sector_size=meta_sector_size,
                                               nsid=nsid, timeout=timeout, checkPass=checkPass, pi_type=pi_type, writebuf_list=writebuf_list, readbuf_list=readbuf_list,
                                               rand_reset=rand_reset, reap_type=reap_type, io_check_type=io_check_type, cdw2=cdw2, cdw3=cdw3, cdw13=cdw13, cdw14=cdw14,
                                               cdw15=cdw15, reset_lcg=reset_lcg)

    def pcie_reset(self, timeout=None, pci_path_check=True):
        timeout = timeout if timeout else self.test_inst.reset_timeout
        self.device_inst.pcie_reset(timeout=timeout, pci_path_check=pci_path_check)
        self.device_fini()
        self.device_reinit()

    def controller_reset(self, timeout=None, pci_path_check=True):
        timeout = timeout if timeout else self.test_inst.reset_timeout
        self.device_inst.controller_reset(timeout=timeout, pci_path_check=pci_path_check)
        self.device_fini()
        self.device_reinit()

    def function_level_reset(self, timeout=None, pci_path_check=True):
        timeout = timeout if timeout else self.test_inst.reset_timeout
        self.device_inst.function_level_reset(timeout=timeout, pci_path_check=pci_path_check)
        self.device_fini()
        self.device_reinit()

    def subsystem_reset(self, timeout=None, timesleep=0, nssr_type=0):
        timeout = timeout if timeout else self.test_inst.reset_timeout
        self.device_inst.subsystem_reset(timeout=timeout, timesleep=timesleep, nssr_type=nssr_type)
        self.device_fini()
        self.device_reinit()

    def link_reset(self, timeout=None, pci_path_check=True):
        timeout = timeout if timeout else self.test_inst.reset_timeout
        self.device_inst.link_reset(timeout=timeout, pci_path_check=pci_path_check)
        self.device_fini()
        self.device_reinit()

    def device_fini(self):
        if self.__device_fini_flag:
            self.device_inst.device_fini()
            self.__device_fini_flag = False
        else:
            self.logger.info("Device %s has been fini"%self.pci_info)
        self.qpair_inst.destroy_io_qpairs()

    def device_reinit(self):
        if not self.__device_fini_flag:
            self.switch_driver()
            self.device_inst.device_reinit()
            self.__device_fini_flag = True
        else:
            self.logger.info("Device %s has been reinit"%self.pci_info)
        self.qpair_inst.reinit_io_queues()

    def set_io_histogram(self, enable=1):
        if enable:
            self.device_inst.enable_io_histogram()
        else:
            self.device_inst.disable_io_histogram()
    def show_io_histogram(self, latency_summary=1, latency_histogram=1):
        self.device_inst.print_io_histogram(latency_summary, latency_histogram)

    def reset_io_histogram(self):
        self.device_inst.reset_io_histogram()

class NameSpace(object):
    def __init__(self, device, nsid, id_ns_raws):
        self.device = device
        self.pci_info = self.device.pci_info
        self.nsid = nsid
        self.block_device = self.get_block_device()
        self.id_ns = IdentifyNamespace(self.device, self.nsid, id_ns_raws)
        self.update_id_namespace()
        self.flbas = self.id_ns.flbas
        self.sector_size = 2 ** self.id_ns.id_ns.lbaf[self.flbas].ds if self.id_ns.id_ns.lbaf[self.flbas].ds else 512
        self.md_size = self.id_ns.id_ns.lbaf[self.flbas].ms
        self.max_md_size = self.md_size
        for item in self.id_ns.id_ns.lbaf:
            if item.ms > self.max_md_size:
                self.max_md_size = item.ms
    def get_block_device(self):
        if 'nvme' in self.device.driver:
            if self.check_block_device():
                return self.block_device
            if hasattr(self, "block_device") and os.path.exists(self.block_device):
                block_device_path = os.path.join("/sys/block", self.block_device.strip(os.path.sep)[-1], "nsid")
                if self.check_nsid(block_device_path):
                    return self.block_device
            ctrl_device = self.device.get_ctrl_device()
            if ctrl_device:
                probe_timeout = self.device.test_inst.probe_timeout // 1000000 if self.device.test_inst.probe_timeout else 60
                block_base_path = os.path.join(self.device.pcie_path, "nvme/%s"%ctrl_device)
                block_device_pattern = re.compile("nvme[0-9]{1,}n[0-9]{1,}")
                stime = time.time()
                while time.time() - stime < probe_timeout:
                    if os.path.exists(block_base_path) and os.path.isdir(block_base_path) and len(os.listdir(block_base_path)):
                        with os.scandir(block_base_path) as entries:
                            for entry in entries:
                                if entry.is_dir() and block_device_pattern.search(entry.name):
                                    block_device_path = os.path.join(block_base_path, entry.name)
                                    if self.check_nsid(block_device_path):
                                        return "/dev/%s"%entry.name
                else:
                    return None
            else:
                return None

    def check_nsid(self, block_device_path):
        with open(block_device_path, "r") as f:
            cont = f.read()
            return True if self.nsid == int(cont) else False
    def check_block_device(self):
        if hasattr(self, "block_device") and os.path.exists(self.block_device):
            block_device_path = os.path.join("/sys/block", self.block_device.strip(os.path.sep)[-1], "nsid")
            if self.check_nsid(block_device_path):
                return self.block_device
        else:
            return None

    def __str__(self):
        if self.check_block_device():
            return self.block_device.strip(os.path.sep)[-1]
        else:
            return None

    def __repr__(self):
        if self.check_block_device():
            return self.block_device.strip(os.path.sep)[-1]
        else:
            return None

    def update_id_namespace(self, id_ns_raws=None):
        if id_ns_raws:
            self.id_ns.update_record_struct(id_ns_raws)
        else:
            self.id_ns.update_info()
        self.flbas = self.id_ns.flbas
        self.sector_size = 2 ** self.id_ns.id_ns.lbaf[self.flbas].ds
        self.md_size = self.id_ns.id_ns.lbaf[self.flbas].ms
        self.pi_type = None
        self.sector_per_4k = 1024 * 4 // self.sector_size
        self.sector_per_8k = 1024 * 8 // self.sector_size
        self.sector_per_16k = 1024 * 16 // self.sector_size
        self.sector_per_32k = 1024 * 32 // self.sector_size
        self.sector_per_64k = 1024 * 64 // self.sector_size
        self.sector_per_128k = 1024 * 128 // self.sector_size
        self.sector_per_256k = 1024 * 256 // self.sector_size
        self.sector_per_512k = 1024 * 512 // self.sector_size
        self.sector_per_1M = 1024 * 1024 // self.sector_size
        self.sector_per_2M = 1024 * 1024 * 2 // self.sector_size
        self.sector_per_1G = 1024 * 1024 * 1024 // self.sector_size
        if self.id_ns.nsze == 0 and "0000:00:00.0":
            self.max_lba = 0x10000000 - 1
        else:
            self.max_lba = self.id_ns.nsze - 1

if __name__ == '__main__':
    device = NvmeDevice()

