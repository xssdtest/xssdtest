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
VERSION = "1.0"
DISK_SEARCH_NAME = "Non-Volatile"
import argparse
import sys
import os
import yaml
import pathlib
project_path = str(pathlib.Path(__file__).parent)
if project_path not in sys.path:
    sys.path.append(project_path)

def create_opt_parser():
    parser = argparse.ArgumentParser(description="xSSD Test Scripts Run")
    parser.add_argument("-s", "--seed", type=int, dest="seed", default=None, help="seed for random")
    parser.add_argument("-tl", "--test_level", type=float, dest="test_level", default=1.0, help="Feature Id to get running time or loop")
    parser.add_argument("-pn", "--product_name", type=str, dest="product_name", default="xssdtest", help="Product name, default is xssdtest")
    parser.add_argument("-rt", "--run_type", type=str, dest="run_type", default="offLine", choices=["offLine", "Daily", "Feature", "Release Regression"], help="can set offLine, Daily/Feature/Release Regression")
    parser.add_argument("-hp", "--hugepage", type=int, dest="hugepage", default=512, help="spdk memory size default is 256M")
    parser.add_argument("-dmc", "--disable_multi_card", type=int, choices=[0, 1], dest="disable_multi_card", default=0, help="set 1 if want to disable must using multiple cards for raid test")
    parser.add_argument("-ji", "--jenkins_info", type=str, dest="jenkins_info", default="", help="jenkins info for record, default is empty string")
    parser.add_argument("-rid", "--runid", type=str, dest="runid", default=None, help="test ID for multi-card test simulator/haps")

    # Device Info
    parser.add_argument("-d", "--dev_info", type=str, dest="dev_info", default=None, help="the pci port to be tested")
    parser.add_argument("-et", "--engine_type", type=str, dest="engine_type", default="null", choices=['io_uring_nvme_tbd', 'libaio_nvme', 'null', 'ioctrl_nvme',
                        'sata_tbd', 'sde_xx_tbd', 'simulator_nvme', 'spdk_nvme', 'sync_nvme'], help="default is null")
    parser.add_argument("-dn", "--dev_num", type=int, dest="dev_num", default=0, help="Choice one device for init default value")
    parser.add_argument("-pv", "--pcie_version", type=str, dest="pcie_version", default=None, help="PCIE Version")
    parser.add_argument("-nv", "--nvme_version", type=str, dest="nvme_version", default=None, help="nvme version, default is None")
    parser.add_argument("-nmi", "--nvme_mi_version", type=str, dest="nvme_mi_version", default=None, help="nvme mi version, default is None")
    parser.add_argument("-vn", "--vendor_name", type=str, dest="vendor_name", default=None, help="vendor name, default is None ")
    parser.add_argument("-pwl", "--pci_whitelist", type=str, dest="pci_whitelist", default=None, help="pci white list default is None")
    parser.add_argument("-as", "--admin_max_data_transfer_size", type=int, dest="admin_max_data_transfer_size", default=None, help="admin max data transfer size, "
                        "default is None")
    parser.add_argument("-dns", "--default_nsid", type=int, dest="default_nsid", default=None, help="default nsid, default is None")

    # Code Compile
    parser.add_argument("-cu", "--code_update", type=int, choices=[0, 1], dest="code_update", default=0, help="the xssd test code update flag, default is 0")
    parser.add_argument("-su", "--submodule_update", type=int, choices=[0, 1], dest="submodule_update", default=0, help="the xssd test submodule update flag, "
                        "default is 0")
    parser.add_argument("-cc", "--code_compile", type=int, choices=[0, 1], dest="code_compile", default=0, help="code compile flag, default is 0")
    parser.add_argument("-sdl", "--spdk_debug_log", type=int, choices=[0, 1], dest="spdk_debug_log", default=0, help="show spdk debug info, default is 0")
    parser.add_argument("-bn", "--branch_name", type=str, dest="branch_name", default=None, help="get branch name for feature regression, default is None")


    # Log Setting
    parser.add_argument("-dl", "--disable_logger", type=int, choices=[0, 1], dest="disable_logger", default=0, help="disable logger print")
    parser.add_argument("-lp", "--log_path", type=str, dest="log_path", default="/home/xt_log/", help="the path test logs saved")
    parser.add_argument("-ln", "--log_name", type=str, dest="log_name", default=None, help="the logName for test case")
    parser.add_argument("-pt", "--process_trace", type=int, choices=[0, 1], dest="process_trace", default=None, help="show process&thread info")
    parser.add_argument("-ect", "--enable_cmd_trace", type=int, choices=[0, 1], dest="enable_cmd_trace", default=None, help="enable cmd trace, default is 0")
    parser.add_argument("-dap", "--disable_admin_passthru", type=int, choices=[0, 1], dest="disable_admin_passthru", default=1, help="disable admin passthru, default is 1")
    parser.add_argument("-diop", "--disable_io_passthru", type=int, choices=[0, 1], dest="disable_io_passthru", default=0, help="disable io passthru, default is 0")

    # FW Image Update
    parser.add_argument("-fs", "--fw_slot", type=int,  choices=[0, 1, 2, 3, 4, 5, 6, 7], dest="fw_slot", default=1, help="the fw slot to be commit")
    parser.add_argument("-bfi", "--base_fw_img", type=str, dest="base_fw_img", default=None, help="base FW Image")
    parser.add_argument("-bfv", "--base_fw_ver", type=str, dest="base_fw_ver", default=None, help="base FW Version")
    parser.add_argument("-nfi", "--new_fw_img", type=str, dest="new_fw_img", default=None, help="new FW Image")

    # Status Check
    parser.add_argument("-dc", "--disable_check", type=int, choices=[0, 1], dest="disable_check", default=0, help="1: disable info check, 0: enable info check, default is 0")
    parser.add_argument("-dvc", "--disable_vu_check", type=int, choices=[0, 1], dest="disable_vu_check", default=0, help="1: disable vu check, 1: enable vu check, default is 0")
    parser.add_argument("-asc", "--abnormal_status_check", type=int, choices=[0, 1], dest="abnormal_status_check", default=1, help="Abnormal status check 0 is disable 1 is enable, default is 1")
    parser.add_argument("-ps", "--pcie_speed", type=int, dest="pcie_speed", default=None, help="pcie speed check value, default None")
    parser.add_argument("-pw", "--pcie_width", type=int, dest="pcie_width", default=None, help="pcie width check value, default None")


    # Part Scripts Config
    parser.add_argument("-pc", "--power_cycle", type=int, choices=[0, 1], dest="power_cycle", default=None, help="power cycle flag, didn't input")
    parser.add_argument("-pf", "--power_file", type=str, dest="power_file", default=None, help="get a power file after power cycle, default value is None")
    parser.add_argument("-pot", "--power_type", type=int, choices=[1, 2, 3, 4, 5, 6], dest="power_type", default=None, help="power cycle flag 1 power switch, 2 ipmi, 3 relay, 4 reboot, 5 quarchpy, 6 ipmi power reset")
    parser.add_argument("-mip", "--masterip", type=str, dest="masterip", default=None, help="Master/Salve, System PF Case")
    parser.add_argument("-c", "--compression", type=float, dest="compression", default=None, help="compression 0 all, 1 incom, 2 half, 3 third, 4 quarter, 8 eighth")
    parser.add_argument("-ss", "--sector_size", type=int, dest="sector_size", default=None, help="sectorSize 0--512, 1--4096")
    parser.add_argument("-cac", "--capacity_change", type=float, dest="capacity_change", default=None, help="capacityChange 0~8 origin capacity*n")
    parser.add_argument("-alio", "--alignedio", type=int, choices=[0, 1, 2], default=2, help="0: enable big map unit, 1: case self align, 2: random")
    parser.add_argument("-st", "--set_timestamp", type=int, choices=[0, 1], dest="set_timestamp", default=1, help="1-set timeStamp for eventlog debug, 0-for test")
    parser.add_argument("-gvf", "--get_vu_file", type=str, dest="get_vu_file", default=None, help="Get VU File in local file、 network Files、 fw、 none. default is None")

    # constant
    parser.add_argument("-iob", "--io_buffer", type=int, dest="io_buffer", default=None, help="io buffer size, default is none")

    # app info
    parser.add_argument("-ncp", "--nvme_cli_path", type=str, dest="nvme_cli_path", default=None, help="nvme-cli path, default is none")
    parser.add_argument("-ncv", "--nvme_cli_version", type=str, dest="nvme_cli_version", default=None, help="nvme-cli version, default is none")
    parser.add_argument("-fp", "--fio_path", type=str, dest="fio_path", default=None, help="fio path, default is none")
    parser.add_argument("-fv", "--fio_version", type=str, dest="fio_version", default=None, help="fio version, default is none")

    # timeout set
    parser.add_argument("-act", "--admin_cmds_timeout", type=int, dest="admin_cmds_timeout", default=None, help="admin command timeout/ms, default is none")
    parser.add_argument("-ict", "--io_cmds_timeout", type=int, dest="io_cmds_timeout", default=None, help="io command timeout/ms, default is none")
    parser.add_argument("-dsmt", "--dsm_cmds_timeout", type=int, dest="dsm_cmds_timeout", default=None, help="dsm command timeout/ms, default is none")
    parser.add_argument("-fawt", "--fw_active_cmds_timeout", type=int, dest="fw_active_cmds_timeout", default=None, help="fw active command timeout/ms, default is none")
    parser.add_argument("-vut", "--vu_timeout", type=int, dest="vu_timeout", default=None, help="vu command timeout/ms, default is none")
    parser.add_argument("-fmt", "--format_timeout", type=int, dest="format_timeout", default=None, help="format command timeout/ms, default is none")
    parser.add_argument("-stn", "--sanitize_timeout", type=int, dest="sanitize_timeout", default=None, help="sanitize command timeout/ms, default is none")
    parser.add_argument("-sot", "--shutdown_timeout", type=int, dest="shutdown_timeout", default=None, help="shutdown timeout/ms, default is none")
    parser.add_argument("-pft", "--power_failed_timeout", type=int, dest="power_failed_timeout", default=None, help="power ailed timeout/ms, default is none")
    parser.add_argument("-prt", "--probe_timeout", type=int, dest="probe_timeout", default=None, help="probe timeout/ms, default is none")
    parser.add_argument("-rst", "--reset_timeout", type=int, dest="reset_timeout", default=None, help="reset timeout/ms, default is none")

    # xssd test config
    parser.add_argument("-xtc", "--xt_config", type=str, dest="xt_config", default=None, help="xt config file, default is none")

    return parser

parser = create_opt_parser()
args = parser.parse_args()
xt_config = "xt_config.yaml" if args.xt_config is None else args.xt_config
if os.path.exists(xt_config) and os.path.getsize(xt_config):
    type_mapping = {'int': int, 'float': float, 'str': str}
    with open(xt_config) as f:
        config = yaml.safe_load(f)
        for yaml_arg in config['arguments']:
            value = None if yaml_arg['value'] == 'None' else type_mapping[yaml_arg['type']](yaml_arg['value'])
            if yaml_arg['type'] and yaml_arg['type'] != 'None':
                value = type_mapping[yaml_arg['type']](yaml_arg['value'])
            else:
                value = yaml_arg['value'] if yaml_arg['value'] != 'None' else None
            setattr(args, yaml_arg['name'], value)

if __name__ == "__main__":
    def argparse_to_yaml(parser, output_file):
        """
        Converts the argument information from an argparse parser into YAML format and saves it to a specified file.

        Parameters:
        - parser: An argparse.ArgumentParser object containing the argument information to be converted.
        - output_file: A string representing the path to the output YAML file.

        Returns:
        No return value. The function writes the generated YAML data to the specified file.
        """
        args_info = []
        # Iterate through all actions in the parser
        for action in parser._actions:
            # Skip the help action
            if isinstance(action, argparse._HelpAction):
                continue
            arg_dict = {}
            arg_dict['name'] = action.dest if action.dest else action.metavar
            if hasattr(action, "action") and action.action != 'store':
                arg_dict['action'] = action.action
            # Handle the argument's default value
            if hasattr(action, "default") and action.default != argparse.SUPPRESS:
                arg_dict['value'] = action.default
            # Handle the argument's type
            if hasattr(action, "type") and action.type:
                arg_dict['type'] = action.type.__name__ if callable(action.type) else str(action.type)
            # Handle the argument's nargs setting
            if hasattr(action, "nargs") and action.nargs not in [None, argparse.OPTIONAL]:
                arg_dict['nargs'] = action.nargs if not isinstance(action.nargs, int) else str(action.nargs)
            # Add the processed argument information to the list
            args_info.append(arg_dict)
        # Write the argument information to the YAML file
        with open(output_file, 'w') as f:
            yaml.dump({'arguments': args_info}, f, sort_keys=False, default_flow_style=False)
    argparse_to_yaml(parser, 'xt_cfg.yaml')