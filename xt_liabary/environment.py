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
from datetime import datetime
import platform
import psutil
import socket
import re
import subprocess
import json
import pathlib
project_path = str(pathlib.Path(__file__).parent.parent)
if project_path not in sys.path:
    sys.path.append(project_path)
from xt_include.python import distro

class Environment(object):
    """
    Environment information collection class, used to obtain system, network, hardware information and parse dmidecode information
    This class will automatically collect relevant information when initialized, and determine whether it is a server environment based on server characteristics
    """
    def __init__(self):
        """
        Initialization method, automatically called when the object is created
        Used to collect system, network, hardware and dmidecode information, and determine whether it is a server environment
        """
        # Initialize system information by calling get_basic_system_info method
        self.system_info_dict = self.get_basic_system_info()

        # Retrieve network interface information
        self.network_info = self.get_network_info()

        # Obtain hardware details using lshw command and parse the output
        self.hardware_info = self.get_hardware_info()

        # Parse DMI (Desktop Management Interface) decode information using dmidecode command
        self.dmidecode_info = self.parse_dmidecode()

        # Determine if the system is a server by checking the existence of /dev/ipmi0 device file
        self.server_flag = True if os.path.exists("/dev/ipmi0") else False

        
    def get_basic_system_info(self):
        """
        Retrieves basic system information and returns it as a dictionary.

        Returns:
            dict: A dictionary containing system-related metadata such as:
                - architecture (str): System architecture (e.g., '64bit').
                - machine (str): Machine type (e.g., 'x86_64').
                - release (str): OS release string.
                - system (str): Operating system name (e.g., 'Linux').
                - version (str): OS version details.
                - node (str): Hostname of the machine.
                - platform (str): Full platform string.
                - processor (str): Processor model.
                - boot_time (datetime): Time when the system was booted.
                - boot_uptime (str): Uptime in "H:MM" format.
                - os (str): Pretty-printed OS name and version.
        """
        system_info_dict = {}
        system_info_dict['architecture'] = platform.architecture()[0]
        system_info_dict['machine'] = platform.machine()
        system_info_dict['release'] = platform.release()
        system_info_dict['system'] = platform.system()
        system_info_dict['version'] = platform.version()
        system_info_dict['node'] = platform.node()
        system_info_dict['platform'] = platform.platform()
        system_info_dict['processor'] = platform.processor()
        system_info_dict['boot_time'] = datetime.fromtimestamp(psutil.boot_time())

        if os.path.exists("/proc/uptime"):
            with open("/proc/uptime", "r") as f:
                uptime = f.read().split(" ")[0].strip()
            uptime = int(float(uptime))
            uptime_hours = uptime // 3600
            uptime_minutes = (uptime % 3600) // 60
            system_info_dict['boot_uptime'] = str(uptime_hours) + ":" + str(uptime_minutes)
        else:
            system_info_dict['boot_uptime'] = None

        if system_info_dict['system'] == 'Linux':
            system_info_dict['os'] = distro.name(pretty=True) + " " + distro.version()
        else:
            system_info_dict['os'] = distro.LinuxDistribution().name(pretty=True)

        return system_info_dict

    def __getitem__(self, key):
        """
        Access system/hardware/network/dmidecode info using dictionary-style access.

        Args:
            key (str): The desired field to retrieve.

        Returns:
            mixed: Returns value associated with the key from one of the data sources:
                   - system_info_dict
                   - hardware_info
                   - network interface IP address (ipv4)
                   - dmidecode section matching the key
            None: If no match is found.
        """
        if key in self.system_info_dict.keys():
            return self.system_info_dict[key]
        elif key.lower() in self.hardware_info.keys():
            return self.hardware_info[key]
        elif key.lower() in ('local', 'lo'):
            for interface in self.network_info:
                if interface['interface'].lower() == key.lower():
                    return interface['ipv4'][0]['address']
        elif key.lower() in ('network', 'host_ip', 'ipv4'):
            for interface in self.network_info:
                if interface['interface'].lower() in ('lo', 'local'):
                    continue
                else:
                    return interface['ipv4'][0]['address']
        else:
            for interface in self.dmidecode_info:
                if key.lower() in interface['description'].lower():
                    return interface
            return None

    def get_network_info(self):
        """
        Collects and structures network interface information including IPv4 and IPv6 addresses.

        Returns:
            list: A list of dictionaries, each representing a network interface with:
                - interface (str): Interface name (e.g., 'eth0').
                - ipv4 (list): List of IPv4 addresses with address, netmask, and broadcast.
                - ipv6 (list): List of IPv6 addresses with address and netmask.
        """
        interfaces = []
        for name, addrs in psutil.net_if_addrs().items():
            iface_info = {'interface': name, 'ipv4': [], 'ipv6': []}
            for addr in addrs:
                if addr.family == socket.AF_INET:  # IPv4
                    iface_info['ipv4'].append({
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    })
                elif addr.family == socket.AF_INET6:  # IPv6
                    iface_info['ipv6'].append({
                        'address': addr.address,
                        'netmask': addr.netmask
                    })
            interfaces.append(iface_info)
        return interfaces

    def set_sub_hardware_info(self, data, hardware_info):
        """
        Recursively extracts and organizes hardware component information.

        Args:
            data (dict or list): Raw hardware data from `lshw`.
            hardware_info (dict): Target dictionary to populate with parsed values.

        Supported Components:
            - CPU
            - Memory
            - System (Machine Model)
            - Motherboard
            - Network
            - GPU
            - BIOS
        """
        data = data if isinstance(data, list) else [data]
        for item in data:
            if type(item) is not dict:
                continue
            if item.get("class") == "processor":
                hardware_info["cpu"].append({
                    "model": item.get("product"),
                    "cores": item.get("configuration", {}).get("cores"),
                    "frequency": item.get("size", {})
                })
            elif item.get("class") == "memory" and "bank" in item.get("id", "").lower():
                hardware_info["memory"].append({
                    "size": item.get("size", {}),
                    "type": item.get("description"),
                    "slot": item.get("slot")
                })
            elif item.get("class") == "system":
                if not hardware_info.get("machine_model", ""):
                    hardware_info["machine_model"] = item.get("product")
            elif "motherboard" in item.get("description", "").lower():
                hardware_info["motherboard"] = item.get("product")
            elif item.get("class") == "network":
                hardware_info["network"].append({
                    "model": item.get("product"),
                    "mac": item.get("serial"),
                    "driver": item.get("configuration", {}).get("driver"),
                    "ip": item.get("configuration", {}).get("ip", "")
                })
            elif item.get("class") == "display":
                hardware_info["gpu"].append({
                    "model": item.get("product"),
                    "vram": item.get("size", {}).get("value")
                })
            elif "bios" in item.get("description", "").lower():
                hardware_info["bios"] = {
                    "version": item.get("version"),
                    "date": item.get("date")
                }
            if type(item) is dict and item.get("children"):
                child_data = item.get("children")
                self.set_sub_hardware_info(child_data, hardware_info)
            elif type(item) is list:
                self.set_sub_hardware_info(item, hardware_info)

    def get_hardware_info(self):
        """
        Executes the `lshw` command to gather structured hardware information.

        Returns:
            dict: Hardware metadata including:
                - cpu (list): CPU(s) present in the system.
                - memory (list): RAM modules with size, type, and slot.
                - machine_model (str): System product name.
                - motherboard (str): Product name of the motherboard.
                - network (list): Network adapters with model, MAC, driver, and IP.
                - gpu (list): Graphics cards with model and VRAM.
                - bios (dict): BIOS version and date.
        """
        cmd = ["lshw", "-json"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data = json.loads(result.stdout)

        hardware_info = {
            "cpu": [],
            "memory": [],
            "machine_model": "",
            "motherboard": "",
            "network": [],
            "gpu": [],
            "bios": {},
        }

        self.set_sub_hardware_info(data, hardware_info)

        if hardware_info["memory"]:
            total_size, slot_list = 0, []
            for slot, item in enumerate(hardware_info["memory"]):
                if item["size"]:
                    total_size += int(item["size"])
                    slot_list.append(slot)
            hardware_info["memory"].insert(0, {"total_size": total_size, "slot_list": slot_list})

        return hardware_info

    def parse_dmidecode(self):
        """
        Parses the output of the `dmidecode` command into structured DMI sections.

        Returns:
            list: A list of dictionaries, each representing a DMI section with:
                - handle (str): Unique identifier of the section.
                - type (int): DMI type number.
                - size (int): Size of the DMI block in bytes.
                - description (str): Description of the DMI entry.
                - attributes (dict): Additional key-value pairs describing the section.
        """
        sections = []
        current_section = {}
        handle_pattern = re.compile(r'^Handle (0x[0-9A-Fa-f]+), DMI type (\d+), (\d+) bytes$')
        in_block = False

        output = subprocess.check_output(['dmidecode'], stderr=subprocess.STDOUT).decode('utf-8', errors='ignore')

        for line in output.splitlines():
            line = line.rstrip()
            handle_match = handle_pattern.match(line)
            if handle_match:
                if current_section:
                    sections.append(current_section)
                current_section = {
                    'handle': handle_match.group(1),
                    'type': int(handle_match.group(2)),
                    'size': int(handle_match.group(3)),
                    'description': '',
                    'attributes': {}
                }
                in_block = True
                continue
            if in_block:
                if not line:
                    in_block = False
                    continue
                if not current_section['description']:
                    current_section['description'] = line.strip()
                    continue
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    current_section['attributes'][key.strip()] = value.strip()
                else:
                    last_key = list(current_section['attributes'].keys())[-1] if current_section['attributes'] else None
                    if last_key:
                        current_section['attributes'][last_key] += '\n' + line.strip()

        if current_section:
            sections.append(current_section)

        return sections

    def to_size(self, chars):
        """
        Converts human-readable size strings (e.g., '2G') into byte values.

        Args:
            chars (str or list): Input string or list of strings to convert.

        Returns:
            int or list: Converted byte value or list of values.
        """
        char_count_list = []
        chars_list = chars if type(chars) is list else [chars]
        bytes_map = {
            'K': 1024,
            'M': 1024 ** 2,
            'G': 1024 ** 3,
            'T': 1024 ** 4,
            'P': 1024 ** 5,
            'E': 1024 ** 6,
            'Z': 1024 ** 7,
            'Y': 1024 ** 8
        }

        for _char in chars_list:
            char_count, count, _char = 0, '', _char.upper()
            for char in chars:
                if char.isalpha() and char != ' ':
                    char_count, count = int(count) * bytes_map[char] + char_count, ''
                elif char == ' ':
                    continue
                else:
                    count += char
            char_count_list.append(char_count) if count == '' else char_count_list.append(char_count + int(count))

        return char_count_list if type(chars) is list else char_count_list[0]


if __name__ == '__main__':
    env = Environment()