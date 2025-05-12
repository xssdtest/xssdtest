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
import argparse
path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(path)))
from xt_module.xt_devmem import *
nvme_ver_dict = {"1.0": 0x00010000, "1.1": 0x00010100, "1.2": 0x00010200, "1.2.1": 0x00010201,
                 "1.3": 0x00010300, "1.4": 0x00010400, "2.0": 0x00020000, "2.1": 0x00020100}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="xSSD Test Device Memory")
    parser.add_argument("-p", "--pcie_addr", type=str, dest="pcie_addr", default=None, help="pcie match [0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{1}")
    parser.add_argument("-b", "--bar_num", type=int, dest="bar_num", default=0, help="pcie barnum default is 0")
    parser.add_argument("-o", "--offset", type=int, dest="offset", default=0, help="pcie bar offset default is 0")
    parser.add_argument("-l", "--length", type=int, dest="length", default=1, help="pcie bar length default is 1. 1 bytes 2 short, 4 int, 8 long int")
    parser.add_argument("-m", "--mode", type=int, dest="mode", default=0, help="memmap mode default is 1. 0 is read 1 is write")
    parser.add_argument("-v", "--value", type=int, dest="value", default=0, help="memmap value default is 0, value is for write")
    parser.add_argument("-f", "--field", type=str, dest="field", default=None, help="nvme register field default is None")
    args = parser.parse_args()
    pcie_path = os.path.join("/sys/bus/pci/devices", args.pcie_addr)
    resource_path = os.path.join(pcie_path, "resource")
    bar_num = args.bar_num
    base_addr, size = 0, 0
    if os.path.exists(resource_path):
        # Open the resource file and read the specified line
        with open(resource_path, "r") as f:
            addr_list = f.readlines()[bar_num].strip()
            # Parse the base address and size from the file
            base_addr = int(addr_list[0], 16)
            size = int(addr_list[1], 16) - base_addr + 1
    assert base_addr != 0 and size != 0, "Invalid PCIe address or bar number"
    devmem = DevMem(base_addr, size)
    if args.field is None:
        if args.mode:
            devmem.set_value(args.offset, args.value, args.length)
            value = devmem.get_value(args.offset, args.length)
            print("physic memery 0x%x offset 0x%x write value: 0x%x current value is 0x%x" % (base_addr, args.offset, args.value, value))
        else:
            value = devmem.get_value(args.offset, args.length)
            print("physic memery 0x%x offset 0x%x read value: 0x%x" % (base_addr, args.offset, value))
    else:
        if args.bar_num == 0:
            nvme_ver = devmem.get_int_value(0x8)
            if nvme_ver <= nvme_ver_dict["1.4"]:
                from xt_liabary.nvme.nvme_spec_v1_4 import *
                nvme_registers = NvmeRegister()
            else:
                from xt_liabary.nvme.nvme_spec_v2_0 import *
                nvme_registers = NvmeRegister()
            offset_map = nvme_registers.get_offset_map()
            offset, length = None, None
            for field in nvme_registers._fields_:
                if field[0].lower() == args.field.lower():
                    offset = offset_map[field[0]]
                    length = sizeof(field[1])
                    break
            assert offset is not None, "Invalid field '%s' field value: %s " % (args.field, nvme_registers._fields_)
            if args.mode:
                devmem.set_value(offset, args.value, length)
                value = devmem.get_value(offset, length)
                print("physic memery 0x%x filed %s write value: 0x%x current value is 0x%x" % (base_addr, args.field, args.value, value))
            else:
                if args.length > 16:
                    nvme_registers.to_encode(devmem[0:len(nvme_registers)])
                    nvme_registers.show_info()
                else:
                    value = devmem.get_value(args.offset, args.length)
                    print("physic memery 0x%x filed %s read value: 0x%x" % (base_addr, args.field, value))
        else:
            print("Bar number is %s doesn't support field %s" % (args.bar_num, args.field))


