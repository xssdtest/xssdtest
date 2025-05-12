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
from xt_module.xt_devmem import *
class NvmeBar(DevMem):
    """
    The NvmeBar class represents the BAR (Base Address Register) memory region of an NVMe device.

    This class inherits from DevMem and provides access to the BAR memory region of a PCIe device.

    Attributes:
        pcie_path (str): The system path of the PCIe device.
        resource_path (str): The path to the resource file of the PCIe device.
        bar_num (int): The BAR number, default is 0.
        base_addr (int): The base address of the BAR.
        size (int): The size of the BAR.

    Args:
        pcie_addr (str): The address of the PCIe device, used to construct the device path.
        bar_num (int, optional): The BAR number to access, default is 0.
    """
    def __init__(self, pcie_addr, bar_num=0):
        # Construct the system path and resource file path of the PCIe device
        self.pcie_path = os.path.join("/sys/bus/pci/devices", pcie_addr)
        self.resource_path = os.path.join(self.pcie_path, "resource")

        # Set the BAR number
        self.bar_num = bar_num

        # Retrieve the base address and size of the specified BAR
        self.base_addr, self.size = self.get_bar_address(bar_num)

        # Verify that the base address is page-aligned
        assert not (self.base_addr & (page_size - 1)), print("base_addr is page(0x%x)align" % (page_size))

        # Initialize the parent class DevMem with the base address and size
        super(NvmeBar, self).__init__(self.base_addr, self.size)

    def get_bar_address(self, bar_num=None):
        """
        Retrieves the base address and size of the specified BAR (Base Address Register).

        Parameters:
        - bar_num (int, optional): The BAR number to retrieve. If not provided, the default BAR number from the class instance is used.

        Returns:
        - tuple: A tuple containing two elements:
            - base_addr (int): The base address of the BAR.
            - size (int): The size of the BAR.

        Raises:
        - AssertionError: If the resource path does not exist, an assertion error is raised with an error message.
        """
        # Use the provided bar_num or default to the instance's bar_num
        bar_num = bar_num if bar_num is not None else self.bar_num

        # Check if the resource path exists
        if os.path.exists(self.resource_path):
            # Open the resource file and read the specified line
            with open(self.resource_path, "r") as f:
                addr_list = f.readlines()[bar_num].strip()
                # Parse the base address and size from the file
                base_addr = int(addr_list[0], 16)
                size = int(addr_list[1], 16) - base_addr + 1
                return base_addr, size
        else:
            # Raise an assertion error if the resource path does not exist
            assert False, print("resource path does not exist:%s" % self.resource_path)

    def update_bar_address(self, bar_num=None):
        """
        Updates the address information of the BAR (Base Address Register).

        This function reads the address information of the specified BAR from the resource file
        and updates the object's `base_addr` and `size` attributes. If `base_addr` or `size` changes,
        it also updates the memory mapping.

        Parameters:
            bar_num (int, optional): The BAR number to update. If not provided, the object's `bar_num` attribute is used.

        Returns:
            None
        """
        # If bar_num is not provided, use the object's bar_num attribute
        bar_num = bar_num if bar_num is not None else self.bar_num

        # Check if the resource path exists; if not, raise an assertion error
        assert os.path.exists(self.resource_path), print("resource path does not exist:%s" % self.resource_path)

        # Open the resource file and read the address information of the specified BAR
        with open(self.resource_path, "r") as f:
            addr_list = f.readlines()[bar_num].strip()
            base_addr = int(addr_list[0], 16)
            size = int(addr_list[1], 16) - base_addr + 1

            # If base_addr or size changes, update the object's attributes and check if base_addr is page-aligned
            if self.base_addr != base_addr or self.size != size:
                self.base_addr, self.size = base_addr, size
                assert not (self.base_addr & (page_size - 1)), print("base_addr is page(0x%x)align" % (page_size))
                self.update_mem_map()



if __name__ == "__main__":
    pass