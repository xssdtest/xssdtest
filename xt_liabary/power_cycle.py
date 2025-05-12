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
import time

class PowerCycle(object):
    """
    A class for managing power cycling operations on a device.

    This class provides methods to simulate or trigger power-on, power-off,
    and full power cycle sequences. It supports optional PCIe rescan and removal,
    custom timeouts, and pre/post-cycle callback functions.

    Attributes:
        device (object): Reference to the target device object.
        logger (Logger): Logging utility from the device instance.
        extend_tool (object): Extension tool used for power control (e.g., QuarchPy).
        power_failed_timeout (int): Default timeout in seconds for power recovery detection.
    """

    def __init__(self, device):
        """
        Initializes the PowerCycle instance with device-specific tools and settings.

        Parameters:
            device (object): Device instance that contains logger, extend_tool,
                             pci info, and environment information.
        """
        self.device = device
        self.logger = self.device.logger
        self.extend_tool = self.device.extend_tool
        self.power_failed_timeout = self.device.power_failed_timeout

    def pwon(self, power_type=0, rescan_pcie=False, rescan_wait_time=0):
        """
        Powers on the device using the configured extend tool.

        Optionally triggers PCIe rescan and waits for a specified duration.

        Parameters:
            power_type (int): Type of power operation. 0 indicates default behavior.
            rescan_pcie (bool): Whether to rescan PCIe bus after power-on.
            rescan_wait_time (int): Time in seconds to wait after rescan.
        """
        if power_type == 0:
            self.extend_tool.quarchpy_tool.power_cycle_by_quarchpy(run_type=1)
        else:
            self.logger.error("get a invalid power cycle type")

        # Rescan PCI bus if requested and not in server environment
        if rescan_pcie and not self.device.enviroment.server_flag:
            cmd = "echo 1 > /sys/bus/pci/rescan"
            os.system(cmd)

        time.sleep(rescan_wait_time)

    def pwoff(self, power_type=0, remove_pcie=False, remove_wait_time=0):
        """
        Powers off the device using the configured extend tool.

        Optionally removes the PCIe device from the system.

        Parameters:
            power_type (int): Type of power operation. 0 indicates default behavior.
            remove_pcie (bool): If True, removes the PCIe device node.
            remove_wait_time (int): Time in seconds to wait after powering off.
        """
        if power_type == 0:
            self.extend_tool.quarchpy_tool.power_cycle_by_quarchpy(run_type=0)
        else:
            self.logger.error("get a invalid power cycle type")

        # Remove PCIe device entry if needed and not in server environment
        if remove_pcie and not self.device.enviroment.server_flag:
            cmd = f"echo 1 > /sys/bus/pci/devices/{self.device.pci_info}/remove"
            os.system(cmd)

        time.sleep(remove_wait_time)

    def only_power_cycle(self, power_type=0, remove_pcie=False, remove_wait_time=0, rescan_pcie=False, rescan_wait_time=0, powoff_cb=None,
                         powoff_cb_param: tuple=(), poweron_cb=None, poweron_cb_param: tuple=()):
        """
        Performs a raw power cycle without device initialization/deinitialization steps.

        Executes power-off followed by power-on with optional callbacks before and after.

        Parameters:
            power_type (int): Type of power operation. 0 is default.
            remove_pcie (bool): Whether to remove PCIe device during power-off.
            remove_wait_time (int): Time to wait after power-off actions.
            rescan_pcie (bool): Whether to rescan PCIe bus after power-on.
            rescan_wait_time (int): Time to wait after power-on and rescan.
            powoff_cb (function): Callback function to run after power-off.
            powoff_cb_param (tuple): Parameters for powoff_cb.
            poweron_cb (function): Callback function to run after power-on.
            poweron_cb_param (tuple): Parameters for poweron_cb.
        """
        self.pwoff(power_type=power_type, remove_pcie=remove_pcie, remove_wait_time=remove_wait_time)
        if powoff_cb is not None:
            powoff_cb(*powoff_cb_param)
        self.pwon(power_type=power_type, rescan_pcie=rescan_pcie, rescan_wait_time=rescan_wait_time)
        if poweron_cb is not None:
            poweron_cb(*poweron_cb_param)

    def power_cycle(self, power_type=0, remove_pcie=False, remove_wait_time=0, rescan_pcie=False, rescan_wait_time=0, powoff_cb=None,
                    powoff_cb_param=None, poweron_cb=None, poweron_cb_param=None, probe_timeout=None, probe_time_check=True):
        """
        Performs a complete power cycle including device deinit and reinit.

        Steps:
        1. Optionally waits for command completion queue pairs (for SPDK).
        2. Powers off the device.
        3. Optionally removes PCIe device entry.
        4. Calls post-power-off callback (if provided).
        5. Deinitializes the device.
        6. Powers on the device.
        7. Optionally rescans PCIe bus.
        8. Checks device readiness and measures probe time.
        9. Calls post-power-on callback (if provided).
        10. Reinitializes the device.

        Parameters:
            power_type (int): Type of power operation. 0 is default.
            remove_pcie (bool): Whether to remove PCIe device during power-off.
            remove_wait_time (int): Time to wait after power-off actions.
            rescan_pcie (bool): Whether to rescan PCIe bus after power-on.
            rescan_wait_time (int): Time to wait after PCIe rescan.
            powoff_cb (function): Callback function after power-off.
            powoff_cb_param (tuple): Parameters for powoff_cb.
            poweron_cb (function): Callback function after power-on.
            poweron_cb_param (tuple): Parameters for poweron_cb.
            probe_timeout (int): Timeout for device probing.
            probe_time_check (bool): Whether to enforce probe timeout check.
        """
        self.logger.info("************Power Cycle Start******************")
        if "spdk_nvme" in self.device.engine_opt_name:
            self.device.wait_completion_qpair()

        self.pwoff(power_type=power_type, remove_pcie=remove_pcie, remove_wait_time=remove_wait_time)
        self.logger.info("Remove pci info by echo 1")
        pcie_path = f"/sys/bus/pci/devices/{self.device.pci_info}/remove"
        if os.path.exists(pcie_path):
            self.logger.info(f"pcie remove: echo 1 > {pcie_path}")
            os.system(f"echo 1 > {pcie_path}")
        else:
            self.logger.info(f"Can't find pci info: {pcie_path}")

        if powoff_cb is not None:
            powoff_cb(*powoff_cb_param)

        self.device.device_fini()

        self.pwon(power_type=power_type, rescan_pcie=rescan_pcie, rescan_wait_time=rescan_wait_time)
        recover_start_time = time.time()

        if not os.path.exists(self.device.pcie_path):
            os.system("echo 1 > /sys/bus/pci/rescan")

        self.device.device_inst.device_ready_check()
        probe_time = time.time() - recover_start_time

        if poweron_cb is not None:
            poweron_cb(*poweron_cb_param)

        if probe_time_check:
            probe_timeout = probe_timeout if probe_timeout else self.power_failed_timeout
            if probe_timeout < probe_time:
                assert False, self.logger.error(f"Power Cycle Timeout, probe time: {probe_time}")

        self.device.device_reinit()
        self.logger.info("************Power Cycle End******************")

    def shutdown(self, abrupt=False, timeout=100000, check_status=True, shutdown_cb=None, shutdown_param=None, probe_timeout=None):
        """
        Simulates a clean or abrupt device shutdown.

        If no custom shutdown callback is provided, it falls back to a power cycle.

        Parameters:
            abrupt (bool): Whether to perform an abrupt shutdown.
            timeout (int): Maximum time in seconds to wait for shutdown.
            check_status (bool): Whether to verify the device status after shutdown.
            shutdown_cb (function): Optional callback after shutdown.
            shutdown_param (tuple): Parameters for shutdown_cb.
            probe_timeout (int): Timeout for device probe after fallback power cycle.
        """
        self.logger.info("************Shutdown Start******************")
        self.device.device_inst.shutdown(abrupt=abrupt, timeout=timeout, check_status=check_status)

        if shutdown_cb:
            shutdown_cb(*shutdown_param)
            self.device.device_fini()
            self.device.device_reinit()
        else:
            self.power_cycle(power_type=0, remove_pcie=False, remove_wait_time=0, rescan_pcie=False, rescan_wait_time=0, probe_timeout=probe_timeout)

        self.logger.info("************Shutdown End******************")

