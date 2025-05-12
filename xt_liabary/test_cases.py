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
"""
This script initializes the environment and performs necessary setup for a project
that interacts with NVMe devices and PCIe interfaces. It ensures required shared
libraries and hugepage files are available, sets up paths, and defines regex patterns
for PCIe and NVMe device identification.
"""

import os
import sys
import random
import pathlib
import glob

# Get the current working directory and project path
current_path = os.getcwd()
project_path = str(pathlib.Path(__file__).parent.parent)

# Add the project path to sys.path if not already present
if project_path not in sys.path:
    sys.path.append(project_path)

# Add the platform-specific path to sys.path if not already present
platform_path = os.path.join(project_path, "xt_platform")
if platform_path not in sys.path:
    sys.path.append(platform_path)

# Check for the presence of shared object (.so) files and build them if missing
matched_so_files = glob.glob(os.path.join(platform_path, "xt_interface.*.so"))
if len(matched_so_files) == 0:
    # Build the Cython files if no matching .so files are found
    assert os.system(f"cd {platform_path};./build.sh") == 0, print("build cython files failed")

# Check for hugepage files and set them up if missing
matched_huge_files = glob.glob(os.path.join(os.popen("mount | grep ' type hugetlbfs ' | awk '{ print $3 }'").read().strip(), "spdk*map_*"))
if len(matched_huge_files) == 0:
    # Run the setup script to configure hugepages if none are found
    assert os.system(f"cd {project_path};./setup.sh config 0000:00:00.0") == 0, print("setup config failed")

# Restore the original working directory
os.chdir(current_path)

# Import necessary modules from the project
from xt_parse_args import *
from xt_liabary.nvme_device import *
from xt_liabary.environment import *
from xt_module.xt_import import PathImport

# Define regex patterns for PCIe and NVMe device identification
pcie_pattern = re.compile('[0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}.[0-9a-fA-F]{1}')
pcie_short_pattern = re.compile('[0-9a-fA-F]{2}:[0-9a-fA-F]{2}.[0-9a-fA-F]{1}')
pcie_bus_pattern = re.compile('[0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}.[0-9a-fA-F]{1}')
nvme_block_name_pattern = re.compile("nvme[0-9]{1,}n[0-9]{1,}")
nvme_block_path_name_pattern = re.compile("/dev/nvme[0-9]{1,}n[0-9]{1,}")
nvme_ctrl_name_pattern = re.compile("nvme[0-9]{1,}")
nvme_ctrl_path_name_pattern = re.compile("/dev/nvme[0-9]{1,}")

# Initialize a dictionary for storing PCIe link speed information
INITLINKSPEEDDICT = {}

# Retrieve a list of PCIe devices supporting Non-Volatile memory
pcie_list = os.popen("lspci -D | grep 'Non-Volatile' | awk '{print $1}'").read().split()

class TestCase(object):
    """
    The `TestCase` class is responsible for initializing and managing the configuration,
    environment setup, and device handling required for NVMe testing. It consolidates all
    necessary parameters and ensures that the test environment is correctly configured
    before executing any test cases.

    Key Responsibilities:
    - Initialize project paths, random seeds, and environment configurations.
    - Parse and validate PCIe/NVMe device information.
    - Configure logging, timeouts, and other test-related parameters.
    - Perform pre-test checks such as Git branch validation and code updates.
    - Create and manage device objects based on the specified engine type.

    Attributes:
        project_path (str): Root directory of the project.
        seed (int): Random seed for reproducibility in tests.
        path_import (PathImport): Utility for dynamic path management.
        environment (Environment): Environment configuration handler.
        logger (Logger): Logging utility for test execution.
        device_list (list): List of initialized [NvmeDevice] objects.
        default_device (NvmeDevice): Default device selected for testing.
        pcie_list (list): List of PCIe addresses for NVMe devices.
        ... (Other attributes related to test configuration and device properties)
    """

    def __init__(self):
        """
        Constructor for the [TestCase] class. Initializes all necessary configurations
        and sets up the test environment by loading parameters from global variables
        and performing pre-test validations.

        Initialization Steps:
        1. **Project Setup**:
           - Sets the project root path and appends it to `sys.path`.
           - Initializes a random seed for consistent test behavior.

        2. **Environment Configuration**:
           - Loads environment settings and initializes utility classes like [PathImport]
             and [Environment].

        3. **Device Parsing**:
           - Parses PCIe or NVMe device information using helper methods like
             [parse_arge_device()] and validates the input format.

        4. **Logging and Debugging**:
           - Configures logging based on user-defined parameters ([log_path], [log_name], etc.).
           - Enables or disables specific debugging features like command tracing.

        5. **Code and Branch Management**:
           - Performs Git branch validation to ensure the correct branch is being used.
           - Optionally updates submodules and compiles code if required.

        6. **PCIe/NVMe Validation**:
           - Checks PCIe link speed and width against expected values.
           - Ensures compatibility with specified PCIe and NVMe versions.

        7. **Device Object Creation**:
           - Creates a list of [NvmeDevice] objects based on the parsed PCIe information.
           - Selects a default device for testing.

        8. **Timeouts and Performance Parameters**:
           - Configures various timeout values for admin commands, I/O operations, etc.
           - Sets performance-related parameters like compression, sector size, and alignment.

        Note: This method relies on global variables ([project_path]) and assumes
        they are properly initialized before this class is instantiated.
        """
        # Project and Random Seed Initialization
        self.project_path = project_path
        self.seed = random.randint(0, 100000000) if args.seed is None else args.seed
        random.seed(self.seed)

        # Path and Environment Setup
        self.path_import = PathImport(project_path)
        self.environment = Environment()

        # Test Configuration Parameters
        self.test_level = args.test_level
        self.product_name = args.product_name
        self.run_type = args.run_type
        self.hugepage = args.hugepage
        self.disable_multi_card = args.disable_multi_card

        # Logging and Debugging Configuration
        self.jenkins_info = args.jenkins_info
        self.runid = args.runid
        self.dev_info = args.dev_info
        self.log_path = args.log_path
        self.log_name = args.log_name
        self.logger = self.create_log()

        # Git Branch and Code Update Management
        self.branch_name = args.branch_name
        self.git_branch_check()
        self.code_update = args.code_update
        self.submodule_update = args.submodule_update
        self.code_compile = args.code_compile

        # Device Parsing and PCIe/NVMe Configuration
        self.engine_type = args.engine_type
        self.pcie_list = self.parse_arge_device()
        self.dev_num = args.dev_num
        self.default_pcie_info = self.pcie_list[self.dev_num]
        self.pcie_version = args.pcie_version
        self.nvme_version = args.nvme_version
        self.nvme_mi_version = args.nvme_mi_version

        # Test Behavior and Safety Switches
        self.spdk_debug_log = args.spdk_debug_log
        self.disable_logger = args.disable_logger
        self.process_trace = args.process_trace
        self.enable_cmd_trace = args.enable_cmd_trace
        self.disable_admin_passthru = args.disable_admin_passthru
        self.disable_io_passthru = args.disable_io_passthru

        # Firmware and Abnormal Status Handling
        self.power_cycle = args.power_cycle
        self.auto_code_update()
        self.fw_slot = args.fw_slot
        self.base_fw_img = args.base_fw_img
        self.abnormal_status_check = args.abnormal_status_check

        # PCIe Speed and Width Validation
        self.pcie_speed = args.pcie_speed
        self.pcie_width = args.pcie_width
        self.pcie_speed_check()

        # Storage Performance Parameters
        self.compression = args.compression
        self.sector_size = args.sector_size
        self.alignedio = args.alignedio
        self.io_buffer = args.io_buffer

        # Toolchain and Timeout Configuration
        self.nvme_cli_path = args.nvme_cli_path
        self.nvme_cli_version = args.nvme_cli_version
        self.fio_path = args.fio_path
        self.fio_version = args.fio_version
        self.admin_cmds_timeout = args.admin_cmds_timeout
        self.shutdown_timeout = args.shutdown_timeout

        # Device Object Creation
        if ("nvme" in self.engine_type or "null" in self.engine_type) and (not self.engine_type.endswith("tbd")):
            self.device_list = [NvmeDevice(pcie_info, self) for pcie_info in self.pcie_list]
        else:
            assert False, self.logger.error("get a invalid or not implemented engine type {engine_type}".format(engine_type=self.engine_type))
        self.default_device = self.device_list[self.dev_num]

    def create_log(self):
        """
        Creates and returns a logger instance based on the specified conditions.

        Functionality:
        - If logging is not disabled (`self.disable_logger` is False), it checks
          whether the log directory exists. If not, it creates the directory.
        - Initializes the logger with parameters such as log filename, path,
          process tracing, and PCIe information.
        - If logging is disabled, it initializes a logger instance with logging
          turned off.

        Parameters (implicitly used):
        - self.disable_logger (bool): If True, disables the logger; otherwise,
          enables it.
        - self.log_path (str): The directory where log files will be stored. Created
          if it does not exist.
        - self.log_name (str): The name of the log file.
        - self.process_trace (bool): Whether to enable process tracing for debugging.
        - self.default_pcie_info (str): Default PCIe information passed to the logger.

        Returns:
        - logger: An instance of `xt.Logger`. If logging is disabled, the logger
          will have no active logging functionality.
        """
        if not self.disable_logger:
            if not os.path.exists(self.log_path):
                os.makedirs(self.log_path)
            logger = xt.Logger(filename=self.log_name, log_path=self.log_path, process_trace=self.process_trace, disable_logger=False, pci_info=self.default_pcie_info)
        else:
            logger = xt.Logger(disable_logger=True)
        return logger


    def parse_arge_device(self):
        """
        Parses device information and returns a list of corresponding PCIe addresses.

        Functionality:
        - If `self.dev_info` is None, it checks the engine type. For "null" or
          "simulator_nvme", it returns a default PCIe address ["0000:00:00.0"].
          Otherwise, it raises an assertion error for invalid device info.
        - If `self.dev_info` is provided, it matches the input against various regex
          patterns to extract PCIe addresses in different formats:
          1. Full PCIe address format (e.g., "0000:01:00.0").
          2. Short PCIe format (e.g., "01:00.0") by searching within [pcie_list]
          3. NVMe block device names (e.g., "nvme0n1") using [block_name_to_pcie]
          4. NVMe block device path names (e.g., "/dev/nvme0n1") using [block_name_path_to_pcie]
          5. PCIe bus format (partial match) by searching within [pcie_list]

        Parameters (implicitly used):
        - self.dev_info: A string containing device information (PCIe addresses,
          block device names, or other formats).
        - self.engine_type: The type of engine being used (e.g., "null", "nvme").
        - pcie_pattern, pcie_short_pattern, nvme_block_name_pattern,
          nvme_block_path_name_pattern, pcie_bus_pattern: Regex patterns for matching
          different device formats.
        - pcie_list: A global list of full PCIe addresses for reference.

        Returns:
        - list: A list of parsed PCIe addresses. If the input doesn't match any valid
          format, it raises an assertion error.
        """
        # Handle case where device info is not provided
        if self.dev_info is None:
            if self.engine_type in ["null", "simulator_nvme"]:
                return ["0000:00:00.0"]
            assert False, print("get a invalid device info {dev_info} engine type {engine_type}".format(dev_info=self.dev_info, engine_type=self.engine_type))
        else:
            input_pcie_list = []

            # Parse full PCIe address format
            if pcie_pattern.search(self.dev_info):
                return [item.strip() for item in self.dev_info.split(",")]

            # Parse short PCIe format by matching with global `pcie_list`
            elif pcie_short_pattern.search(self.dev_info):
                pcie_short_list = [item.strip() for item in self.dev_info.split(",")]
                for item in pcie_short_list:
                    for pcie_item in pcie_list:
                        if item in pcie_item:
                            input_pcie_list.append(pcie_item)
                            break
                return input_pcie_list

            # Parse NVMe block device names (e.g., "nvme0n1")
            elif nvme_block_name_pattern.search(self.dev_info):
                block_names = [item.strip() for item in self.dev_info.split(",")]
                return [self.block_name_to_pcie(item) for item in block_names]

            # Parse NVMe block device path names (e.g., "/dev/nvme0n1")
            elif nvme_block_path_name_pattern.search(self.dev_info):
                block_name_paths = [item.strip() for item in self.dev_info.split(",")]
                return [self.block_name_path_to_pcie(item) for item in block_name_paths]

            # Parse PCIe bus format (partial match within `pcie_list`)
            elif pcie_bus_pattern.search(self.dev_info):
                pcie_bus_list = [item.strip() for item in self.dev_info.split(",")]
                for item in pcie_bus_list:
                    for pcie_item in pcie_list:
                        if item in pcie_item[5:7]:
                            input_pcie_list.append(pcie_item)
                return input_pcie_list

            # Raise assertion error for invalid device info
            else:
                assert False, print("get a invalid device info {dev_info}".format(dev_info=self.dev_info))


    def block_name_to_pcie(self, block_name):
        """
        Converts a block device name to its corresponding PCIe device identifier.

        Parameters:
        - block_name (str): The name of the block device (e.g., "nvme0n1").

        Returns:
        - str: The PCIe device identifier extracted from the block device's path.

        Functionality:
        - Constructs the device path for the given block device name.
        - Verifies that the constructed path exists; if not, raises an assertion error.
        - Resolves the real path of the block device and extracts the PCIe identifier
          from the path structure (specifically, the third-to-last segment of the path).
        """
        # Construct the device path for the block device
        block_name_path = f"/sys/block/{block_name}/device".format(block_name=block_name)

        # Assert that the device path exists; otherwise, print an error message
        assert os.path.exists(block_name_path), print("block_name_path {block_name_path} is not exist".format(block_name_path=block_name_path))

        # Resolve the real path of the block device
        block_path = os.path.realpath(block_name_path)

        # Extract and return the PCIe device identifier from the resolved path
        return block_path.split(os.path.sep)[-3]


    def block_name_path_to_pcie(self, block_name_path):
        """
        Converts a full block device path to its corresponding PCIe address.

        Parameters:
        - block_name_path (str): The complete path string containing the block device name,
          with path components separated by the operating system's path separator.

        Returns:
        - str: The PCIe address string returned by invoking self.block_name_to_pcie().

        Functionality:
        - Extracts the block device name from the given path (last component of the path).
        - Calls self.block_name_to_pcie() to convert the extracted block name into the
          corresponding PCIe address.
        """
        # Extract the last part of the path as the block device name
        block_name = block_name_path.split(os.path.sep)[-1]
        return self.block_name_to_pcie(block_name)


    def auto_code_update(self):
        """
        Automatically updates the codebase and performs compilation if required.

        Functionality:
        - Checks whether the system is in a power cycle state. If not, it proceeds
          to perform Git-related operations (pull and submodule update).
        - Executes the build script (`./build.sh`) if either code compilation is
          explicitly enabled or submodules have been updated.
        - Restores the original working directory after completing the operations.

        Parameters (implicitly used):
        - self.power_cycle (bool): If True, skips all update operations (code update
          and submodule update).
        - self.code_update (bool): If True and not in a power cycle, executes `git pull`.
        - self.submodule_update (bool): If True and not in a power cycle, updates
          Git submodules recursively.
        - self.code_compile (bool): If True, triggers the build process by running
          the [./build.sh](file:xssdtest/xt_platform/build.sh) script.
        - self.project_path (str): The root project path, used to locate the build
          script directory.

        Returns:
        - None: This function does not return any value but performs necessary
          environment setup.
        """
        # Initialize a flag for submodule building
        submodule_build = False

        # Perform Git pull if not in a power cycle and code update is requested
        if not self.power_cycle and self.code_update:
            os.system("git pull >> /dev/null 2>&1")

        # Update Git submodules if not in a power cycle and submodule update is requested
        if not self.power_cycle and self.submodule_update:
            os.system("git submodule update --init --recursive")
            submodule_build = True

        # Execute the build script if code compilation is required or submodules were updated
        if self.code_compile or submodule_build:
            build_path = os.path.join(self.project_path, "xt_platform")
            current_path = os.getcwd()
            os.chdir(build_path)
            os.system("./build.sh")
            os.chdir(current_path)

    def git_branch_check(self):
        """
        Checks whether the current Git branch matches the expected branch name.

        Functionality:
        - If `self.branch_name` is set, this function retrieves the current Git branch name
          using the command `git rev-parse --abbrev-ref HEAD`.
        - It performs an assertion to verify that `self.branch_name` is a substring of the
          current branch name. If not, it logs an error message and raises an AssertionError.

        Parameters (implicitly used):
        - self.branch_name (str): The expected branch name configured in the instance.
        - self.logger (Logger): Logger object used to log error messages if the branch
          check fails.

        Returns:
        - None: This function does not return a value. If the branch does not match,
          an AssertionError is raised.
        """
        # Only perform branch check if a specific branch name is provided
        if self.branch_name:
            # Execute Git command to get current branch name
            current_branch = os.popen("git rev-parse --abbrev-ref HEAD").read()
            # Assert that the expected branch name is a substring of the current branch name
            assert self.branch_name in current_branch, self.logger.error(
                "current branch is {current_branch}, but branch_name is {branch_name}".
                format(current_branch=current_branch, branch_name=self.branch_name))


    def update_pcie_speed(self, pcie_info=None):
        """
        Updates the PCIe link speed and width information for specified or default PCIe ports.

        Functionality:
        - If no PCIe info is provided, it defaults to `self.pcie_list`.
        - Ensures input is always a list of PCIe addresses.
        - For each valid PCIe port (excluding placeholder "0000:00:00.0"):
          1. Runs `lspci` to get detailed PCIe capabilities.
          2. Parses the output to extract negotiated link speed (GT/s) and width (xN).
          3. Stores the result in [INITLINKSPEEDDICT](file:xssdtest/xt_liabary/test_cases.py) for later use in validation.
          4. Prints current link speed and width for visibility.

        Parameters:
        - pcie_info (str or list): Optional. A single PCIe address or list of addresses to query.
          If None, uses `self.pcie_list`.

        Side Effects:
        - Modifies global dictionary [INITLINKSPEEDDICT](file:xssdtest/xt_liabary/test_cases.py) with parsed speed and width data.
        - Prints progress and discovered PCIe configuration to stdout.
        """
        # Normalize pcie_info as a list
        pcie_info = pcie_info if pcie_info else self.pcie_list
        pcie_info = pcie_info if isinstance(pcie_info, list) else [pcie_info]

        for pcie_port in pcie_info:
            if "0000:00:00.0" not in pcie_port:
                try:
                    # Query PCIe capability using lspci
                    speed_info = os.popen("sudo lspci -s %s -vvvxxx |grep 'Speed'" % pcie_port).readlines()[1]
                    # Parse speed and width values from output
                    info = re.split(":|,", speed_info)
                    speed = float(re.split(" |G", info[1])[1])
                    width = int(re.split(" |x", info[2])[3])
                    # Store result in global dict
                    INITLINKSPEEDDICT["%s" % pcie_port] = [speed, width]
                    # Print detected PCIe link speed and width
                    print("PCI info %s current speed is %sGT/s, width is x%s" % (pcie_port, speed, width))
                except:
                    print("Get a invalid PCI info in %s" % pcie_port)


def pcie_speed_check(self, pcie_info=None, report_error=True):
    """
    Checks whether the current PCIe link speed and width match the expected values.

    Functionality:
    - Uses `pcie_speed` and `pcie_width` from the instance to perform validation.
    - First calls `update_pcie_speed()` to fetch current PCIe link information.
    - For each specified PCIe port, compares actual speed/width with expected values.
    - Logs mismatches using `self.logger.error()` and optionally raises an assertion error.

    Parameters:
    - pcie_info (str or list): Optional. PCIe address or list of addresses to validate.
      If None, uses `self.pcie_list`.
    - report_error (bool): If True, raises an AssertionError on mismatch. If False,
      only logs the discrepancy without failing.

    Side Effects:
    - Modifies global dictionary [INITLINKSPEEDDICT](file:xssdtest/xt_liabary/test_cases.py) by calling [update_pcie_speed()](file:xssdtest/xt_liabary/test_cases.py).
    - May raise an `AssertionError` if speed or width does not match and `report_error` is True.
    - Logs detailed error messages about mismatches via `self.logger.error()`.

    Example:
        >>> test_case.pcie_speed = 8.0
        >>> test_case.pcie_width = 4
        >>> test_case.pcie_speed_check()
        # Will pass if all devices are running at PCIe Gen4 x4 (8.0GT/s x4)
    """

    # Normalize pcie_info as a list
    pcie_info = pcie_info if pcie_info else self.pcie_list
    pcie_info = pcie_info if isinstance(pcie_info, list) else [pcie_info]

    # Initial update of PCIe link speeds
    self.update_pcie_speed(pcie_info=pcie_info)

    # Only proceed if expected PCIe speed and width are defined
    if self.pcie_speed and self.pcie_width:
        # Re-update PCIe speed info to ensure fresh data before final validation
        self.update_pcie_speed(pcie_info)

        for pcie_port in pcie_info:
            # Retrieve the current speed and width from shared state
            speed, width = INITLINKSPEEDDICT["%s" % pcie_port]

            # Check if actual values match expected ones
            if speed != self.pcie_speed or width != self.pcie_width:
                self.logger.error("PCIe port %s current width is x%s, but pcie_width is x%s" %(pcie_port, width, self.pcie_width))
                self.logger.error("PCIe port %s current speed is %sGT/s, but pcie_speed is %sGT/s" % (pcie_port, speed, self.pcie_speed))
                assert not report_error, "PCIe speed or width mismatch detected"


if __name__ == '__main__':
    test_case = TestCase()


