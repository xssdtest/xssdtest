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
import inspect

nvme_cli_common_para_dict = {"verbose": None, "timeout": None}
nvme_cli_common_para_dict_1 = {"output-format": None, "vendor-specific": None, "raw-binary": None, "human-readable": None, **nvme_cli_common_para_dict}
nvme_cli_common_para_dict_2 = {"output-format": None, **nvme_cli_common_para_dict}
nvme_cli_common_para_dict_3 = {"output-format": None, "human-readable": None, **nvme_cli_common_para_dict}
nvme_cli_common_para_dict_4 = {"output-format": None, "raw-binary": None, **nvme_cli_common_para_dict}
nvme_cli_common_para_dict_5 = {"output-format": None, "raw-binary": None, "human-readable": None, **nvme_cli_common_para_dict}

nvme_cli_cmds_para_dict = {
                "id-ctrl":                      nvme_cli_common_para_dict_1,
                "id-ns":                        {"namespace-id": None, **nvme_cli_common_para_dict_1},
                "id-ns-granularity":            nvme_cli_common_para_dict_2,
                "id-ns-lba-format":             {"lba-format-index": None, "uuid-index": None, **nvme_cli_common_para_dict_2},
                "list-ns":                      {"namespace-id": None, "csi":None, "all": None, **nvme_cli_common_para_dict_2},
                "list-ctrl":                    {"cntid": None,"namespace-id": None, **nvme_cli_common_para_dict_2},
                "nvm-id-ctrl":                  nvme_cli_common_para_dict_2,
                "nvm-id-ns":                    {"namespace-id": None, "uuid-index": None, **nvme_cli_common_para_dict_2},
                "nvm-id-ns-lba-format":         {"lba-format-index": None, "uuid-index": None, **nvme_cli_common_para_dict_2},
                "primary-ctrl-caps":            {"cntlid": None, **nvme_cli_common_para_dict_3},
                "list-secondary":               {"cntid": None, "num-entries": None, **nvme_cli_common_para_dict_2},
                "cmdset-ind-id-ns":             nvme_cli_common_para_dict_1,
                "ns-descs":                     {"namespace-id": None, **nvme_cli_common_para_dict_4},
                "id-nvmset":                    {"nvmset_id": None, **nvme_cli_common_para_dict_2},
                "id-uuid":                      nvme_cli_common_para_dict_5,
                "id-iocs":                      {"controller-id":None, **nvme_cli_common_para_dict_2},
                "id-domain":                    {"dom-id":None, **nvme_cli_common_para_dict_2},
                "list-endgrp":                  {"endgrp-id":None, **nvme_cli_common_para_dict_2},
                "create-ns":                    {"nsze": None, "ncap": None, "flbas": None, "dps": None, "nmic": None, "anagrp-id": None, "nvmset-id": None,
                                                 "endg-id": None, "block-size": None, "csi": None, "lbstm": None, "nphndls":None, "nsze-si": None, "ncap-si":None,
                                                 "azr": None, "rar":None, "ror":None, "rnumzrwa":None, "phndls":None, **nvme_cli_common_para_dict_2},
                "delete-ns":                    {"namespace-id": None, **nvme_cli_common_para_dict_2},
                "attach-ns":                    {"namespace-id": None, "controllers": None, **nvme_cli_common_para_dict_2},
                "detach-ns":                    {"namespace-id": None, "controllers": None, **nvme_cli_common_para_dict_2},
                "get-ns-id":                    nvme_cli_common_para_dict_2,
                "get-log":                      {"namespace-id": None, "log-id": None, "log-len": None, "aen": None, "lpo": None, "lsp": None, "lsi": None,
                                                 "rae": None, "uuid-index":None, "csi": None, "ot":None, "xfer-len":None, **nvme_cli_common_para_dict_4},
                "telemetry-log":                {"output-file": None, "host-generate": None, "controller-init": None, "data-area": None, "rae": None,
                                                 **nvme_cli_common_para_dict_2},
                "fw-log":                       nvme_cli_common_para_dict_4,
                "changed-ns-list-log":          nvme_cli_common_para_dict_4,
                "smart-log":                    {"namespace-id":None, **nvme_cli_common_para_dict_5},
                "ana-log":                      {"groups":None, **nvme_cli_common_para_dict_2},
                "error-log":                    {"log-entries":None, **nvme_cli_common_para_dict_4},
                "effects-log":                  {"csi":None, **nvme_cli_common_para_dict_5},
                "endurance-log":                {"group-id": None, **nvme_cli_common_para_dict_2},
                "predictable-lat-log":          {"nvmset-id": None, **nvme_cli_common_para_dict_4},
                "pred-lat-event-agg-log":       {"log-entries": None, "rae": None, **nvme_cli_common_para_dict_4},
                "persistent-event-log":         {"action":None, "log_len":None, **nvme_cli_common_para_dict_4},
                "endurance-event-agg-log":      {"log-entries": None, "rae": None, **nvme_cli_common_para_dict_4},
                "lba-status-log":               {"rae":None, **nvme_cli_common_para_dict_2},
                "resv-notif-log":               nvme_cli_common_para_dict_2,
                "boot-part-log":                {"output-file":None, "lsp":None, **nvme_cli_common_para_dict_2},
                "phy-rx-eom-log":               {"controller":None, "lsp":None, **nvme_cli_common_para_dict_2},
                "get-feature":                  {"feature-id": None, "namespace-id": None, "sel": None, "data-len": None, "cdw11": None, "uuid-index": None,
                                                 "changed": None, **nvme_cli_common_para_dict_5},
                "device-self-test":             {"namespace-id":None, "self-test-code":None, "wait":None, **nvme_cli_common_para_dict_2},
                "self-test-log":                {"dst-entries":None, **nvme_cli_common_para_dict_2},
                "supported-log-pages":          nvme_cli_common_para_dict_2,
                "fid-support-effects-log":      nvme_cli_common_para_dict_3,
                "mi-cmd-support-effects-log":   nvme_cli_common_para_dict_3,
                "media-unit-stat-log":          {"domain-id":None, **nvme_cli_common_para_dict_4},
                "supported-cap-config-log":     {"domain-id":None, **nvme_cli_common_para_dict_4},
                "set-feature":                  {"namespace-id": None, "feature-id": None, "value": None, "cdw12": None, "uuid-index": None, "data-len": None, "data": None, "save":
                                                None, **nvme_cli_common_para_dict_2},
                "set-property":                 {"offset": None, "value": None, **nvme_cli_common_para_dict_2},
                "get-property":                 {"offset": None, **nvme_cli_common_para_dict_3},
                "format":                       {"namespace-id": None, "lbaf": None, "ses": None, "pi": None, "pil": None, "ms": None, "reset": None, "block-size": None,
                                                 **nvme_cli_common_para_dict_2},
                "fw-commit":                    {"slot": None, "action": None, "bpid": None, **nvme_cli_common_para_dict_2},
                "fw-download":                  {"fw": None, "offset": None, "xfer": None, "progress":None, "ignore-ovr": None, **nvme_cli_common_para_dict_2},
                "admin-passthru":               {"opcode": None, "flags": None, "prefill": None, "rsvd": None, "namespace-id": None, "data-len": None, "metadata-len": None, "cdw2":
                                                 None, "cdw3": None, "cdw10": None, "cdw11": None, "cdw12": None, "cdw13": None, "cdw14": None, "cdw15": None, "input-file":None,
                                                 "metadata":None, "show-command": None, "dru-run": None, "read": None, "write": None, "latency": None, **nvme_cli_common_para_dict_4},
                "io-passthru":                  {"opcode": None, "flags": None, "prefill": None, "rsvd": None, "namespace-id": None, "data-len": None, "metadata-len": None, "cdw2":
                                                 None, "cdw3": None, "cdw10": None, "cdw11": None, "cdw12": None, "cdw13": None, "cdw14": None, "cdw15": None, "input-file":None,
                                                 "metadata":None, "show-command": None, "dru-run": None, "read": None, "write": None, "latency": None, **nvme_cli_common_para_dict_4},
                "security-send":                {"namespace-id":None, "file":None, "nssf":None, "secp":None, "spsp":None, "tl":None, **nvme_cli_common_para_dict_2},
                "security-recv":                {"namespace-id":None, "size":None, "nssf":None, "secp":None, "spsp":None, "al":None, **nvme_cli_common_para_dict_4},
                "get-lba-status":               {"namespace-id": None, "start-lba": None, "max-dw":None, "action":None, "range-len": None, **nvme_cli_common_para_dict_2},
                "capacity-mgmt":                {"operation":None, "element-id":None, "cap-lower":None, "cap-upper":None, **nvme_cli_common_para_dict_2},
                "resv-acquire":                 {"namespace-id": None, "crkey": None, "prkey": None, "rtype": None, "racqa": None, "iekey": None, **nvme_cli_common_para_dict_2},
                "resv-register":                {"namespace-id": None, "crkey": None, "nrkey": None, "rrega": None, "cptpl": None, "iekey": None, **nvme_cli_common_para_dict_2},
                "resv-release":                 {"namespace-id": None, "crkey": None, "rtype": None, "rrela": None, "iekey": None, **nvme_cli_common_para_dict_2},
                "resv-report":                  {"namespace-id": None, "numd": None, "eds": None, **nvme_cli_common_para_dict_4},
                "dsm":                          {"namespace-id": None, "ctx-attrs": None, "blocks": None, "slba": None, "ad": None, "idw":None, "idr":None, "cwd11":None,
                                                 **nvme_cli_common_para_dict_2},
                "copy":                         {"namespace-id":None, "sdlba":None, "slbs":None, "blocks":None, "snsids":None, "sopts":None, "limited-retry":None, "force-unit-access":
                                                 None, "prinfow":None, "ref-tag":None, "expected-ref-tags":None, "app-tag":None, "expected-app-tags":None, "app-tag-mask":None,
                                                 "expected-app-tag-masks":None, "dir-type":None, "dir-spec":None, "format":None, **nvme_cli_common_para_dict_2},
                "flush":                        {"namespace-id":None, **nvme_cli_common_para_dict_2},
                "compare":                      {"namespace-id": None, "block-count": None, "data-size": None, "metadata-size": None, "ref-tag": None, "data":None, "metadata":None,
                                                 "prinfo":None, "app-tag-mask":None, "app-tag":None, "storage-tag":None, "limited-retry":None, "force-unit-access":None, "storage-tag-check"
                                                 :None, "dir-type":None, "dir-spec":None, "dsm":None, "show-command":None, "dry-run":None, "latency":None, **nvme_cli_common_para_dict_2},
                "read":                         {"namespace-id": None, "start-block":None, "block-count": None, "data-size": None, "metadata-size": None, "ref-tag": None, "data":None,
                                                 "metadata":None, "prinfo":None, "app-tag-mask":None, "app-tag":None, "storage-tag":None, "limited-retry":None, "force-unit-access":None,
                                                 "storage-tag-check":None, "dir-type":None, "dir-spec":None, "dsm":None, "show-command":None, "dry-run":None, "latency":None,
                                                 **nvme_cli_common_para_dict_2},
                "write":                        {"namespace-id": None, "start-block":None, "block-count": None, "data-size": None, "metadata-size": None, "ref-tag": None, "data":None,
                                                 "metadata":None, "prinfo":None, "app-tag-mask":None, "app-tag":None, "storage-tag":None, "limited-retry":None, "force-unit-access":None,
                                                 "storage-tag-check":None, "dir-type":None, "dir-spec":None, "dsm":None, "show-command":None, "dry-run":None, "latency":None,
                                                 **nvme_cli_common_para_dict_2},
                "write-zeroes":                 {"namespace-id": None, "start-block":None, "block-count": None, "dir-type": None, "deac": None, "limited-retry":None, "force-unit-access"
                                                 :None, "prinfo":None, "ref-tag":None, "app-tag-mask":None, "app-tag":None, "storage-tag":None, "storage-tag-check":None, "dir-spec":
                                                 None, **nvme_cli_common_para_dict_2},
                "write-uncor":                  {"namespace-id": None, "start-block":None, "block-count": None, "dir-type": None, "dir-spec":None, **nvme_cli_common_para_dict_2},
                "verify":                       {"namespace-id": None, "start-block":None, "block-count": None, "limited-retry":None, "force-unit-access":None, "prinfo":None, "ref-tag":
                                                 None, "app-tag-mask":None, "app-tag":None, "storage-tag":None, "storage-tag-check":None, **nvme_cli_common_para_dict_2},
                "sanitize":                     {"no-dealloc": None, "oipbp":None, "owpass":None, "ause":None, "sanact":None, "ovrpat":None, "emvs":None, **nvme_cli_common_para_dict_2},
                "sanitize-log":                 {"rae":None, **nvme_cli_common_para_dict_5},
                "ns-rescan":                    nvme_cli_common_para_dict_2,
                "gen-dhchap-key":               {"secret":None, "key-length":None, "nqn":None, "hmac":None, **nvme_cli_common_para_dict_2},
                "check-dhchap-key":             {"key":None, **nvme_cli_common_para_dict_2},
                "gen-tls-key":                  {"keyring":None, "keytype":None, "hostnqn":None, "subsysnqn":None, "secret":None, "keyfile":None, "hmac":None, "identity":None,
                                                 "insert":None, **nvme_cli_common_para_dict_2},
                "check-tls-key":                {"keyring":None, "keytype":None, "hostnqn":None, "subsysnqn":None, "keydata":None, "keyfile":None, "identity":None, "insert":None, 
                                                 **nvme_cli_common_para_dict_2} ,
                "tls-key":                      {"keyring":None, "keytype":None, "keyfile":None, "import":None, "export":None, "revoke":None, **nvme_cli_common_para_dict_2},
                "dir-receive":                  {"namespace-id":None, "data-len":None, "dir-type":None, "dir-spec":None, "dir-oper":None, "dreq-resource":None,
                                                 **nvme_cli_common_para_dict_3} ,
                "dir-send":                     {"namespace-id":None, "data-len":None, "dir-type":None, "target-dir":None, "dir-spec":None, "dir-oper":None, "endir":None, "input-file"
                                                 :None, **nvme_cli_common_para_dict_5},
                "virt-mgmt":                    {"cntlid":None, "rt":None, "act":None, "nr":None, **nvme_cli_common_para_dict_2},
                "rpmb":                         {"cmd":None, "msgfile":None, "keyfile":None, "key":None, "address":None, "msg":None, "blocks":None, "target":None},
                "lockdown":                     {"ofi":None, "ifc":None, "prhbt":None, "scp":None, "uuid":None, **nvme_cli_common_para_dict_2},
                "dim":                          {"nqn":None, "device":None, "task":None, "verbose":None},
                "show-topology":                {"ranking":None, **nvme_cli_common_para_dict_2},
                "io-mgmt-recv":                 {"namespace-id":None, "mos":None, "mo":None, "data":None, "data-len":None, **nvme_cli_common_para_dict_2},
                "io-mgmt-send":                 {"namespace-id":None, "mos":None, "mo":None, "data":None, "data-len":None, **nvme_cli_common_para_dict_2},
                "nvme-mi-recv":                 {"opcode":None, "namespace-id":None, "data-len":None, "nmimt":None, "nmd0":None, "nmd1":None, "input-file":None,
                                                **nvme_cli_common_para_dict_2},
                "nvme-mi-send":                 {"opcode":None, "namespace-id":None, "data-len":None, "nmimt":None, "nmd0":None, "nmd1":None, "input-file":None,
                                                **nvme_cli_common_para_dict_2},
                "discover" :                    {"transport":None, "nqn":None, "traddr":None, "trsvcid":None, "host-traddr":None, "host-iface":None, "hostnqn":None, "hostid":None,
                                                 "dhchap-secret":None, "keyring":None, "tls-key":None, "tls-key-identity":None, "nr-io-queues":None, "nr-write-queues":None,
                                                 "nr-poll-queues":None, "queue-size":None, "keep-alive-tmo":None, "reconnect-delay":None, "ctrl-loss-tmo":None, "fast_io_fail_tmo":None,
                                                 "tos":None, "tls_key":None, "duplicate-connect":None, "disable-sqflow":None, "hdr-digest":None, "data-digest":None, "tls":None,
                                                 "concat":None, "device":None, "persistent":None, "raw":None, "quiet":None, "config":None, "nbft":None, "no-nbft":None, "nbft-path":
                                                 None, "context":None, **nvme_cli_common_para_dict_2},
                "connect-all":                  {"transport":None, "nqn":None, "traddr":None, "trsvcid":None, "host-traddr":None, "host-iface":None, "hostnqn":None, "hostid":None,
                                                 "dhchap-secret":None, "keyring":None, "tls-key":None, "tls-key-identity":None, "nr-io-queues":None, "nr-write-queues":None,
                                                 "nr-poll-queues":None, "queue-size":None, "keep-alive-tmo":None, "reconnect-delay":None, "ctrl-loss-tmo":None, "fast_io_fail_tmo":None,
                                                 "tos":None, "tls_key":None, "duplicate-connect":None, "disable-sqflow":None, "hdr-digest":None, "data-digest":None, "tls":None,
                                                 "concat":None, "device":None, "persistent":None, "raw":None, "quiet":None, "config":None, "nbft":None, "no-nbft":None, "nbft-path":
                                                 None,"context":None , "dump-config":None, **nvme_cli_common_para_dict_2},
                "connect":                      {"transport":None, "nqn":None, "traddr":None, "trsvcid":None, "host-traddr":None, "host-iface":None, "hostnqn":None, "hostid":None,
                                                 "dhchap-secret":None, "keyring":None, "tls-key":None, "tls-key-identity":None, "nr-io-queues":None, "nr-write-queues":None,
                                                 "nr-poll-queues":None, "queue-size":None, "keep-alive-tmo":None, "reconnect-delay":None, "ctrl-loss-tmo":None, "fast_io_fail_tmo":None,
                                                 "tos":None, "tls_key":None, "duplicate-connect":None, "disable-sqflow":None, "hdr-digest":None, "data-digest": None, "tls": None,
                                                 "concat": None, "dump-config":None, "config":None, "context":None, **nvme_cli_common_para_dict_2},
                "disconnect":                   {"nqn":None, "device":None, "verbose":None, **nvme_cli_common_para_dict_2},
                "disconnect-all":               {"transport":None, "verbose":None, **nvme_cli_common_para_dict_2},
                "config":                       {"transport":None, "nqn":None, "traddr":None, "trsvcid":None, "host-traddr":None, "host-iface":None, "hostnqn":None, "hostid":None,
                                                 "dhchap-secret":None, "keyring":None, "tls-key":None, "tls-key-identity":None, "nr-io-queues":None, "nr-write-queues":None,
                                                 "nr-poll-queues":None, "queue-size":None, "keep-alive-tmo":None, "reconnect-delay": None, "ctrl-loss-tmo": None, "fast_io_fail_tmo":
                                                 None, "tos": None, "tls_key": None, "duplicate-connect": None, "disable-sqflow": None, "hdr-digest": None, "data-digest": None,
                                                 "tls": None, "concat": None, "dhchap-ctrl-secret":None, "config": None, "verbose":None, "scan":None, "modify":None, "dump":None,
                                                 "update":None},
            }

# base on nvme-cli v2.11 libnvme1.12 source code
class NvmeCommands(object):
    def __init__(self, device=None):
        self.device = device
        self.logger = self.device.logger
        self.system_cmds = self.device.system_cmds
        self.vendor_commands = self.device.vendor_commands
        self.nvme_cli_path = self.device.test_inst.nvme_cli_path if self.device.test_inst.nvme_cli_path else "nvme"
        self.default_buffer = self.device.buffer.create_buffer(buf_length=self.device.admin_max_data_transfer_size)
        self.admin_cmds_timeout = self.device.admin_cmds_timeout
        self.io_cmds_timeout = self.device.io_cmds_timeout
        self.dsm_cmds_timeout = self.device.dsm_cmds_timeout
        self.fw_active_cmds_timeout = self.device.fw_active_cmds_timeout
        self.vu_timeout = self.device.vu_timeout
        self.format_timeout = self.device.format_timeout
        self.sanitize_timeout = self.device.sanitize_timeout

    def run_nvme_cli_cmd(self, cmd_info, show_log, *args, **kwargs):
        cmd_para_dict = nvme_cli_cmds_para_dict.get(cmd_info, None)
        assert cmd_para_dict is not None, self.logger.error("nvme_cli_cmds_para_dict has no cmd_info: %s" % cmd_info)
        params = "cmd_info"
        for key in kwargs.keys():
            params += " --%s=%s"%(key, kwargs[key])
        for arg in args:
            params += " %s "%arg
        assert self.nvme_cli_path, self.logger.error("nvme_cli_path is None")
        cmdline = "%s %s %s"%(self.nvme_cli_path, self.device.dev_info, params)
        if show_log:
            self.logger.info("%s: cmdline: %s" %(cmd_info, cmdline))
        return self.system_cmds.send_cmd(cmdline)

    def __getattr__(self, name):
        return getattr(self.vendor_commands, name)

    def show_func_local_param(self, _func, passthru_type=1):
        if self.device.test_inst.disable_admin_passthru and passthru_type:
            return
        if self.device.test_inst.disable_io_passthru and not passthru_type == 0:
            return
        sig = inspect.signature(_func)
        param_names = list(sig.parameters.keys())
        local_vars = locals()
        log_info = " ".join(["%s:%s "%(name, local_vars.get(name)) for name in param_names])
        if passthru_type:
            self.logger.info("admin-passthru: %s" % log_info)
        else:
            self.logger.info("io-passthru: %s" % log_info)

    def admin_passthru(self, opcode, buf, fuse=0, psdt=0, nsid=1, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                       wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                       **kwargs):
        if hasattr(self.vendor_commands, "admin_passthru"):
            return self.vendor_commands.admin_passthru(opcode, buf, fuse, psdt, nsid, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size, wait_completed,
                                                       rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            if app_type is not None:
                return self.run_nvme_cli_cmd("admin-passthru", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                if show_log:
                    self.show_func_local_param(self.admin_passthru)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, nsid=nsid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11
                                                    =cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size, wait_completed=wait_completed, rtn_cmds_u_addr=
                                                    rtn_cmds_u_addr, timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=
                                                    io_status_code_type_expected)


    def io_passthru(self, opcode, buf=None, qpair=None, fuse=0, psdt=0, cid=0, nsid=1, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0,
                    wait_completed=1, sector_size=512, meta_sector_size=0, rtn_io_u_addr=True, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, io_tailer_flag
                    =0, pi_type=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_passthru"):
            return self.vendor_commands.io_passthru(opcode, buf, qpair, fuse, psdt, cid, nsid, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, wait_completed,
                                                    sector_size, meta_sector_size, rtn_io_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, io_tailer_flag,
                                                    pi_type, show_log, *args, **kwargs)
        else:
            if app_type is not None:
                return self.run_nvme_cli_cmd("io-passthru", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                if show_log:
                    self.show_func_local_param(self.io_passthru, passthru_type=0)
                return self.device.send_io_cmds(opcode=opcode, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, nsid=nsid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2,
                                                cdw10=cdw10, cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, wait_completed=wait_completed, sector_size=sector_size,
                                                meta_sector_size=meta_sector_size, rtn_io_u_addr=rtn_io_u_addr, timeout=timeout, pi_type=pi_type, io_status_code_expected=
                                                io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, io_tailer_flag=io_tailer_flag)

    def io_flush(self, qpair=None, nsid=0xFFFFFFFF, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, wait_completed=1,
                 timeout=None, rtn_io_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_flush"):
            return self.vendor_commands.io_flush(qpair, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, wait_completed, timeout,
                                                 rtn_io_u_addr, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            if app_type is not None:
                return self.run_nvme_cli_cmd("flush", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                if show_log:
                    self.show_func_local_param(self.io_flush)
                return self.device.send_io_cmds(opcode=0x0, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=
                                                cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr,
                                                io_status_code_expected=io_status_code_expected, timeout=timeout, io_status_code_type_expected=io_status_code_type_expected)

    def __combine_pi_info(self, nsid, storage_tag, reftag, prinfo, storage_tag_size):
        cdw14, cdw3, cdw2 = 0, 0, 0
        if self.device.ns[nsid].pi_format:
            if self.device.nvme_version == 1.4:
                cdw2 = storage_tag & 0xffffffff
                cdw3 = (storage_tag >> 32) & 0xffff
                cdw14 = reftag
            else:
                if prinfo == 0:
                    cdw14 = reftag & 0xffffffff
                    cdw14 |= ((storage_tag << (32 - storage_tag_size)) & 0xffffffff)
                elif prinfo == 1:
                    cdw14 = reftag & 0xffffffff
                    cdw3 = reftag >> 32
                    cdw14 |= ((storage_tag << (80 - storage_tag_size)) & 0xffff0000)
                    if (storage_tag_size >= 48):
                        cdw3 |= ((storage_tag >> (storage_tag_size - 48)) & 0xffffffff)
                    else:
                        cdw3 |= ((storage_tag << (48 - storage_tag_size)) & 0xffffffff)
                        cdw2 = (storage_tag >> (storage_tag_size - 16)) & 0xffff
                elif prinfo == 2:
                    cdw14 = reftag & 0xffffffff
                    cdw3 = (reftag >> 32) & 0xffff
                    cdw14 |= ((storage_tag << (48 - storage_tag_size)) & 0xffffffff)
                    if (storage_tag_size >= 16):
                        cdw3 |= ((storage_tag >> (storage_tag_size - 16)) & 0xffff)
                    else:
                        cdw3 |= ((storage_tag << (16 - storage_tag_size)) & 0xffff)
                else:
                    assert False, self.logger.error("Unsupported Protection Information Format")
        else:
            cdw2  = storage_tag & 0xffffffff
            cdw3  = (storage_tag >> 32) & 0xffff
            cdw14 = reftag
        return cdw14, cdw3, cdw2


    def io_write(self, buf=None, qpair=None, slba=0, lbacnt=None, nsid=None, fuse=0, psdt=0, cid=0, storage_tag=0, mptr=0, prp1=0, prp2=0, limited_retry=0, force_unit=0, prinfo=0, 
                 dir_type=0, storage_tag_check=0, cmd_extension_type=0, dsm=0, cmd_extension_value=0, dir_spec=0, reftag=0, storage_tag_size=0, appmask=0, apptag=0, wait_completed=1, 
                 timeout=None, rtn_io_u_addr=False, io_tailer_flag=0, pi_type=0, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args, 
                 **kwargs):
        if hasattr(self.vendor_commands, "io_write"):
            return self.vendor_commands.io_write(buf, qpair, slba, lbacnt, nsid, fuse, psdt, cid, storage_tag, mptr, prp1, prp2, limited_retry, force_unit, prinfo, dir_type, 
                                                 storage_tag_check, cmd_extension_type, dsm, cmd_extension_value, dir_spec, reftag, storage_tag_size, appmask, apptag, wait_completed, 
                                                 timeout, rtn_io_u_addr, io_tailer_flag, pi_type, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, 
                                                 **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("write", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                cdw10 = slba & 0xffffffff
                cdw11 = (slba >> 32) & 0xffffffff
                cdw12 = limited_retry << 31 | force_unit << 30 | prinfo << 26 | storage_tag_check << 24 |dir_type << 20 | cmd_extension_type << 16 | (lbacnt - 1)  # 0's base value
                if cmd_extension_type == 0:
                    cdw13 = dsm | (dir_spec << 16)
                else:
                    cdw13 = cmd_extension_value | (dir_spec << 16)
                cdw15 = appmask << 16 | apptag
                cdw14, cdw3, cdw2 = self.__combine_pi_info(nsid, storage_tag, reftag, prinfo, storage_tag_size)
                if show_log:
                    self.show_func_local_param(self.io_write)
                return self.device.send_io_cmds(opcode=0x01, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10,
                                                cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, io_status_code_expected=
                                                io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, rtn_io_u_addr=rtn_io_u_addr, io_tailer_flag=
                                                io_tailer_flag, pi_type=pi_type, timeout=timeout)

    def io_read(self, buf=None, qpair=None, slba=0, lbacnt=None, nsid=None, fuse=0, psdt=0, cid=0, storage_tag=0, mptr=0, prp1=0, prp2=0, limited_retry=0, force_unit=0, prinfo=0, 
                dir_type=0, storage_tag_check=0, cmd_extension_type=0, dsm=0, cmd_extension_value=0, dir_spec=0, reftag=0, storage_tag_size=0, appmask=0, apptag=0, wait_completed=1,
                timeout=None, rtn_io_u_addr=False, io_tailer_flag=0, pi_type=0, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args, 
                **kwargs):
        if hasattr(self.vendor_commands, "io_read"):
            return self.vendor_commands.io_read(buf, qpair, slba, lbacnt, nsid, fuse, psdt, cid, storage_tag, mptr, prp1, prp2, limited_retry, force_unit, prinfo, dir_type, 
                                                storage_tag_check, cmd_extension_type, dsm, cmd_extension_value, dir_spec, reftag, storage_tag_size, appmask, apptag, wait_completed, 
                                                timeout, rtn_io_u_addr, io_tailer_flag, pi_type, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, 
                                                **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("read", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                cdw10 = slba & 0xffffffff
                cdw11 = (slba >> 32) & 0xffffffff
                cdw12 = limited_retry << 31 | force_unit << 30 | prinfo << 26 | storage_tag_check << 24 |dir_type << 20 | cmd_extension_type << 16 | (lbacnt - 1)  # 0's base value
                if cmd_extension_type == 0:
                    cdw13 = dsm | (dir_spec << 16)
                else:
                    cdw13 = cmd_extension_value | (dir_spec << 16)
                cdw15 = appmask << 16 | apptag
                cdw14, cdw3, cdw2 = self.__combine_pi_info(nsid, storage_tag, reftag, prinfo, storage_tag_size)
                if show_log:
                    self.show_func_local_param(self.io_read)
                return self.device.send_io_cmds(opcode=0x02, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, 
                                                cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, io_status_code_expected=
                                                io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, rtn_io_u_addr=rtn_io_u_addr, io_tailer_flag=
                                                io_tailer_flag, pi_type=pi_type, timeout=timeout)


    def io_write_uncor(self, qpair=None, slba=0, lbacnt=None, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw13=0, cdw14=0, cdw15=0, wait_completed=1, 
                       timeout=None, rtn_io_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_write_uncor"):
            return self.vendor_commands.io_write_uncor(qpair, slba, lbacnt, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw13, cdw14, cdw15, wait_completed, timeout, 
                                                       rtn_io_u_addr, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("write-uncor", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                cdw10 = slba & 0xffffffff
                cdw11 = (slba >> 32) & 0xffffffff
                cdw12 = (lbacnt - 1) & 0xffff  # 0's based value
                if show_log:
                    self.show_func_local_param(self.io_write_uncor)
                return self.device.send_io_cmds(opcode=0x04, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=
                                                cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr,
                                                io_status_code_expected=io_status_code_expected, timeout=timeout, io_status_code_type_expected=io_status_code_type_expected)

    def io_compare(self, buf=None, qpair=None, slba=0, lbacnt=None, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, limited_retry=0, force_unit=0, prinfo
                   =0, cdw13=0, expect_inital_blk_tag=0, expect_blk_tag_mask=0, expect_blk_apptag=0, wait_completed=1, timeout=None, rtn_io_u_addr=False, io_status_code_expected=0, 
                   io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_compare"):
                return self.vendor_commands.io_compare(buf, qpair, slba, lbacnt, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, limited_retry, force_unit, prinfo, cdw13, 
                                                       expect_inital_blk_tag, expect_blk_tag_mask, expect_blk_apptag, wait_completed, timeout, rtn_io_u_addr, io_status_code_expected,
                                                       io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("compare", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = slba & 0xffffffff
                cdw11 = (slba >> 32) & 0xffffffff
                cdw12 = limited_retry << 31 | force_unit << 30 | prinfo << 26 | (lbacnt - 1)  # 0's base value
                cdw14 = expect_inital_blk_tag
                cdw15 = expect_blk_tag_mask << 16 | expect_blk_apptag
                if show_log:
                    self.show_func_local_param(self.io_compare)
                return self.device.send_io_cmds(opcode=0x05, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10,
                                                cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr,
                                                io_status_code_expected=io_status_code_expected, timeout=timeout, io_status_code_type_expected=io_status_code_type_expected)

    def io_write_zeros(self, qpair=None, slba=0, lbacnt=None, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, limited_retry=0, force_unit=0, prinfo=0, deallocate
                       =0, cdw13=0, expect_inital_blk_tag=0, expect_blk_tag_mask=0, expect_blk_apptag=0, wait_completed=1, timeout=None, rtn_io_u_addr=False, io_status_code_expected=0, 
                       io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_write_zeros"):
            return self.vendor_commands.io_write_zeros(qpair, slba, lbacnt, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, limited_retry, force_unit, prinfo, deallocate, cdw13,
                                                       expect_inital_blk_tag, expect_blk_tag_mask, expect_blk_apptag, wait_completed, timeout, rtn_io_u_addr, io_status_code_expected, 
                                                       io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("write-zeroes", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                cdw10 = slba & 0xffffffff
                cdw11 = (slba >> 32) & 0xffffffff
                cdw12 = limited_retry << 31 | force_unit << 30 | prinfo << 26 | deallocate << 25 | (lbacnt - 1)  # 0's base value
                cdw14 = expect_inital_blk_tag
                cdw15 = expect_blk_tag_mask << 16 | expect_blk_apptag
                if show_log:
                    self.show_func_local_param(self.io_write_zeros)
                return self.device.send_io_cmds(opcode=0x08, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=
                                                cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr, 
                                                io_status_code_expected=io_status_code_expected, timeout=timeout, io_status_code_type_expected=io_status_code_type_expected)

    def io_dsm(self, buf=None, qpair=None, slba=0, lbacnt=None, nsid=None, fuse=0, psdt=0, cid=0, deallocate=1, dataset_for_write=0, dataset_for_read=0, context_attributes=0x4,
               cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, rtn_io_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, 
               wait_completed=1, timeout=None, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_dsm"):
            return self.vendor_commands.io_dsm(buf, qpair, slba, lbacnt, nsid, fuse, psdt, cid, deallocate, dataset_for_write, dataset_for_read, context_attributes, cdw2, cdw3, mptr,
                                               prp1, prp2, cdw12, cdw13, cdw14, cdw15, rtn_io_u_addr, io_status_code_expected, io_status_code_type_expected, wait_completed, timeout, 
                                               app_type, show_log, *args, **kwargs)
        else:
            if app_type is not None:
                return self.run_nvme_cli_cmd("dsm", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.dsm_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                if show_log:
                    self.show_func_local_param(self.io_dsm)
                lba, cnt, lba_ranges, max_range, start_offset = slba, 0, [], 0xFFFFFFFF, 0
                lbacnt = lbacnt if lbacnt else self.device.dev_info.ns[nsid].maxLba + 1
                ranges, reminder = divmod(lbacnt, max_range)
                ranges = ranges + 1 if reminder > 0 else ranges
                while cnt < ranges - 1:
                    lba_ranges.append([lba, max_range])
                    lba += max_range
                    cnt += 1
                left_lbas = lbacnt - cnt * max_range
                lba_ranges.append([lba, left_lbas])
                cdw10 = len(lba_ranges) - 1  # 0's based value
                cdw11 = deallocate << 2 | dataset_for_write << 1 | dataset_for_read
                for lbaRange in lba_ranges:
                    buf.set_uint32(value=context_attributes, offset=start_offset)
                    start_offset += 4
                    buf.set_uint32(value=lbaRange[1], offset=start_offset)
                    start_offset += 4
                    buf.set_uint64(value=lbaRange[0], offset=start_offset)
                    start_offset += 8
                return self.device.send_io_cmds(opcode=0x9, buf=buf, qpair=qpair, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2,
                                                cdw10=cdw10, cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr,
                                                timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)

    def io_verify(self, buf=None, qpair=None, slba=0, lbacnt=None, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, limited_retry=0, force_unit=0, prinfo=0,
                   cdw13=0, expect_inital_blk_tag=0, expect_blk_tag_mask=0, expect_blk_apptag=0, wait_completed=1, timeout=None, rtn_io_u_addr=False, io_status_code_expected=0,
                   io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_verify"):
            return self.vendor_commands.io_verify(buf, qpair, slba, lbacnt, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, limited_retry, force_unit, prinfo, cdw13, 
                                                  expect_inital_blk_tag, expect_blk_tag_mask, expect_blk_apptag, wait_completed, timeout, rtn_io_u_addr, io_status_code_expected, 
                                                  io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("verify", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = slba & 0xffffffff
                cdw11 = (slba >> 32) & 0xffffffff
                cdw12 = limited_retry << 31 | force_unit << 30 | prinfo << 26 | (lbacnt - 1)  # 0's base value
                cdw14 = expect_inital_blk_tag
                cdw15 = expect_blk_tag_mask << 16 | expect_blk_apptag
                if show_log:
                    self.show_func_local_param(self.io_verify)
                return self.device.send_io_cmds(opcode=0x0C, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, 
                                                cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr
                                                , timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)

    def io_resv_register(self, buf=None, qpair=None, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, crkey=0, nrkey=0, rrega=0, cptpl=0, iekey=0, cdw11=0,
                         cdw12=0, cdw13=0, cdw14=0, cdw15=0, wait_completed=1, timeout=None, rtn_io_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type
                         =None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_resv_register"):
            return self.vendor_commands.io_resv_register(buf, qpair, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, crkey, nrkey, rrega, cptpl, iekey, cdw11, cdw12, cdw13,
                                                         cdw14, cdw15, wait_completed, timeout, rtn_io_u_addr, io_status_code_expected, io_status_code_type_expected, app_type, 
                                                         show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("resv-register", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (rrega & 0x7) | (cptpl << 30)
                if iekey:
                    cdw10 |= 1 << 3
                    buf.set_uint64(value=crkey, offset=0)
                    buf.set_uint64(value=nrkey, offset=8)
                if show_log:
                    self.show_func_local_param(self.io_resv_register)
                return self.device.send_io_cmds(opcode=0x0D, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10,
                                                cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr
                                                , timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)

    def io_resv_report(self, buf=None, qpair=None, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, numd=0, eds=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0,
                       wait_completed=1, timeout=None, rtn_io_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_resv_report"):
            return self.vendor_commands.io_resv_report(buf, qpair, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, numd, eds, cdw12, cdw13, cdw14, cdw15, wait_completed, timeout,
                                                       rtn_io_u_addr, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("resv-report", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                if numd == 0 or numd >= (0x400):
                    cdw10 = 0x400 - 1
                else:
                    cdw10 = 3 if numd < 3 else numd
                cdw11 = 1 if eds else 0
                if show_log:
                    self.show_func_local_param(self.io_resv_report)
                return self.device.send_io_cmds(opcode=0x0e, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10,
                                                cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr,
                                                timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)

    def io_resv_acquire(self, buf=None, qpair=None, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, crkey=0, prkey=0, rtype=0, racqa=0, iekey=0, cdw11=0,
                        cdw12=0, cdw13=0, cdw14=0, cdw15=0, wait_completed=1, timeout=None, rtn_io_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type
                        =None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_resv_acquire"):
            return self.vendor_commands.io_resv_acquire(buf, qpair, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, crkey, prkey, rtype, racqa, iekey, cdw11, cdw12, cdw13, cdw14
                                                        , cdw15, wait_completed, timeout, rtn_io_u_addr, io_status_code_expected, io_status_code_type_expected, app_type, show_log,
                                                        *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("resv-acquire", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (racqa & 0x7) | (rtype << 8)
                if iekey:
                    cdw10 |= 1 << 3
                    buf.set_uint64(value=crkey, offset=0)
                    buf.set_uint64(value=prkey, offset=8)
                if show_log:
                    self.show_func_local_param(self.io_resv_register)
                return self.device.send_io_cmds(opcode=0x11, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10,
                                                cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr
                                                , timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)

    def io_mgmt_resv(self, buf=None, qpair=None, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, mos=0, mo=0, data_len=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0,
                     wait_completed=1, timeout=None, rtn_io_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_mgmt_resv"):
            return self.vendor_commands.io_mgmt_resv(buf, qpair, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, mos, mo, data_len, cdw12, cdw13, cdw14, cdw15, wait_completed,
                                                     timeout, rtn_io_u_addr, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("io-mgmt-recv", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = mo | (mos << 16)
                cdw11 = (data_len >> 2) - 1
                if show_log:
                    self.show_func_local_param(self.io_mgmt_resv)
                return self.device.send_io_cmds(opcode=0x12, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10,
                                                cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr
                                                , timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)

    def io_resv_release(self, buf=None, qpair=None, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, crkey=0, rtype=0, rrela=0, iekey=0, cdw11=0, cdw12=0,
                        cdw13=0, cdw14=0, cdw15=0, wait_completed=1, timeout=None, rtn_io_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                        show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_resv_release"):
            return self.vendor_commands.io_resv_release(buf, qpair, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, crkey, rtype, rrela, iekey, cdw11, cdw12, cdw13, cdw14, cdw15,
                                                        wait_completed, timeout, rtn_io_u_addr, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args,
                                                        **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("resv-release", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (rrela & 0x7) | (rtype << 8)
                if iekey:
                    cdw10 |= 1 << 3
                    buf.set_uint64(value=crkey, offset=0)
                if show_log:
                    self.show_func_local_param(self.io_mgmt_resv)
                return self.device.send_io_cmds(opcode=0x15, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10,
                                                cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr,
                                                timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)

    def __fill_copy_ranges(self, buf, desc_format, snsids, slbas, read_paras, cevs, sopts, elbts, elbats, elbatms):
        offset = 0
        for i in range(len(read_paras)):
            if desc_format == 0 or desc_format == 1:
                buf.set_uint64(value=0, offset=offset)
                offset += 8
            else:
                if (desc_format == 2 or desc_format == 3) and snsids:
                    buf.set_uint32(value=snsids[i], offset=offset)
                    offset += 4
                buf.set_uint32(value=0, offset=offset)
                offset += 4
            buf.set_uint64(value=slbas[i], offset=offset)
            offset += 8
            buf.set_uint32(value=read_paras[i], offset=offset)
            offset += 4
            if cevs is None:
                buf.set_uint16(value=0, offset=offset)
            else:
                buf.set_uint16(value=cevs[i], offset=offset)
            offset += 2
            if sopts is not None:
                buf.set_uint16(value=0, offset=offset)
            else:
                buf.set_uint16(value=sopts[i], offset=offset)
            offset += 2
            if desc_format == 0 or desc_format == 2 :
                if elbts is not None:
                    buf.set_uint32(value=0, offset=offset)
                else:
                    buf.set_uint32(value=elbts[i], offset=offset)
                offset += 4
            else:
                if elbts is not None:
                    buf.fill_stream(value=bytes(10), offset=offset, lenth=10)
                else:
                    value = elbts[i].to_bytes(10, byteorder=sys.byteorder)
                    buf.fill_stream(value=value, offset=offset, lenth=10)
                offset += 10
            if elbats is not None:
                buf.set_uint16(value=0, offset=offset)
            else:
                buf.set_uint16(value=elbats[i], offset=offset)
            offset += 2
            if elbatms is not None:
                buf.set_uint16(value=0, offset=offset)
            else:
                buf.set_uint16(value=elbatms[i], offset=offset)
            offset += 2
    def io_copy(self, buf=None, qpair=None, slba=0, slbas=None, read_paras=None, cevs=None, snsids=None, sopts=None, elbts=None, elbats=None, elbatms=None, nsid=None, fuse=0, psdt=0,
                cid=0, cdw2=0, mptr=0, prp1=0, prp2=0, limited_retry=0, force_unit=0, prinfow=0, prinfor=0, reftag=0, apptag=0, appmask=0, dir_type=0, dir_spec=0, desc_format=0,
                wait_completed=1, timeout=None, rtn_io_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_copy"):
            return self.vendor_commands.io_copy(buf, qpair, slba, slbas, read_paras, cevs, snsids, sopts, elbts, elbats, elbatms, nsid, fuse, psdt, cid, cdw2, mptr, prp1, prp2,
                                                limited_retry, force_unit, prinfow, prinfor, reftag, apptag, appmask, dir_type, dir_spec, desc_format, wait_completed, timeout,
                                                rtn_io_u_addr, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("copy", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = slba & 0xffffffff
                cdw11 = slba >> 32
                self.__fill_copy_ranges(buf, desc_format, snsids, slbas, read_paras, cevs, sopts, elbts, elbats, elbatms)
                cdw12 = ((len(read_paras) & 0xf)| ((desc_format & 0xf) << 8) | ((prinfor & 0xf) << 12) | ((dir_type & 0xf) << 20) | ((prinfow & 0xf) << 26) | ((force_unit & 0x1) << 30)
                         | ((limited_retry & 0x1) << 31))
                cdw13 = (dir_spec & 0xffff) << 16,
                if self.device.nvme_version == 1.4:
                    cdw3 = 0
                    cdw14 = reftag
                else:
                    cdw3 = (reftag >> 32) & 0xffffffff
                    cdw14 = reftag & 0xffffffff
                cdw15 = appmask << 16 | apptag

                if show_log:
                    self.show_func_local_param(self.io_copy)
                return self.device.send_io_cmds(opcode=0x19, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10,
                                                cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr,
                                                timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)

    def io_mgmt_send(self, buf=None, qpair=None, mos=0, mo=0, data_len=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0,
                     wait_completed=1, timeout=None, rtn_io_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_mgmt_send"):
            return self.vendor_commands.io_mgmt_send(buf, qpair, mos, mo, data_len, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw14, cdw15, wait_completed,
                                                     timeout, rtn_io_u_addr, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("io-mgmt-send", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = mo | (mos << 16)
                cdw11 = (data_len >> 2) - 1
                if show_log:
                    self.show_func_local_param(self.io_mgmt_resv)
                return self.device.send_io_cmds(opcode=0x1d, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10,
                                                cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr,
                                                timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)

    def io_cancel(self, qpair=None, nsid=None, cid=0, sqid=0, action_code=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, wait_completed=1, timeout=None,
                  rtn_io_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_cancel"):
            return self.vendor_commands.io_cancel(qpair, nsid, cid, sqid, action_code, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw14, cdw15, wait_completed, timeout, rtn_io_u_addr,
                                                      io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("cancel", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                cdw10 = (sqid) | (cid << 16)
                cdw11 = action_code
                if show_log:
                    self.show_func_local_param(self.io_cancel)
                return self.device.send_io_cmds(opcode=0x1d, buf=None, qpair=qpair, fuse=0, psdt=0, cid=0, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11
                                                =cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr,
                                                timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)

    def io_zns_mgmt_send(self, buf=None, qpair=None, slba=0, zm=0, zsaso=0, select_all=0, zsa=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                         cdw14=0, cdw15=0, wait_completed=1, timeout=None, rtn_io_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                         *args, **kwargs):
        if hasattr(self.vendor_commands, "io_zns_mgmt_send"):
            return self.vendor_commands.io_zns_mgmt_send(buf, qpair, slba, zm, zsaso, select_all, zsa, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw14, cdw15,
                                                         wait_completed, timeout, rtn_io_u_addr, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args,
                                                         **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("zns zone-mgmt-send", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = slba & 0xffffffff
                cdw11 = slba >> 32
                cdw13 = (zsa & 0xff) | ((select_all & 1) << 8) | ((zsaso & 1) << 9) |(( zm & 0xff) << 16)
                if show_log:
                    self.show_func_local_param(self.io_zns_mgmt_send)
                return self.device.send_io_cmds(opcode=0x79, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10,
                                                cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr,
                                                timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)

    def io_zns_mgmt_recv(self, buf=None, qpair=None, slba=0, lbacnt=0, zraspf=0, zras=0, zra=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw14=0,
                         cdw15=0, wait_completed=1, timeout=None, rtn_io_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                         *args, **kwargs):
        if hasattr(self.vendor_commands, "io_zns_mgmt_recv"):
            return self.vendor_commands.io_zns_mgmt_recv(buf, qpair, slba, lbacnt, zraspf, zras, zra, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw14, cdw15, wait_completed,
                                                         timeout, rtn_io_u_addr, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("zns zone-mgmt-recv", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = slba & 0xffffffff
                cdw11 = slba >> 32
                cdw12 = lbacnt
                cdw13 = (zra & 0xff) | ((zras & 0xff) << 8) | ((zraspf & 1) << 16)
                if show_log:
                    self.show_func_local_param(self.io_zns_mgmt_send)
                return self.device.send_io_cmds(opcode=0x7a, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10,
                                                cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr,
                                                timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)

    def io_zns_append(self, buf=None, qpair=None, slba=0, lbacnt=0, nsid=None, fuse=0, psdt=0, cid=0, lbtu=0, mptr=0, prp1=0, prp2=0, limited_retry=0, force_unit=0, prinfo=0,
                      prinfo_remap=0, storage_tag_check=0, dir_type=0, cmd_extension_type=0, dir_spec=0, cmd_extension_value=0, lbtl=0, lbatm=0, lbat=0, wait_completed=1, timeout=None,
                      rtn_io_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "io_zns_append"):
            return self.vendor_commands.io_zns_append(buf, qpair, slba, lbacnt, nsid, fuse, psdt, cid, lbtu, mptr, prp1, prp2, limited_retry, force_unit, prinfo, prinfo_remap,
                                                      storage_tag_check, dir_type, cmd_extension_type, dir_spec, cmd_extension_value, lbtl, lbatm, lbat, wait_completed, timeout,
                                                      rtn_io_u_addr, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("zns zone-append", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.io_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw2 = lbtu & 0xffffffff
                cdw3 = (lbtu << 32) & 0xffff
                cdw10 = slba & 0xffffffff
                cdw11 = slba >> 32
                cdw12 = (lbacnt | ((cmd_extension_type & 0xF) << 16) | ((dir_type & 0xf) << 20) | ((storage_tag_check & 1 ) << 24) | ((prinfo_remap & 1 ) << 25)
                         | ((prinfo & 0xf ) << 26) | ((force_unit & 1 ) << 30) | ((limited_retry & 0x1) << 31))
                if cmd_extension_type == 0:
                    cdw13 = (dir_spec & 0xff) << 16
                else:
                    cdw13 = (dir_spec & 0xff) << 16 | (cmd_extension_value & 0xff)
                cdw14 = lbtl
                cdw15 = lbatm << 16 | lbat
                return self.device.send_io_cmds(opcode=0x7d, buf=buf, qpair=qpair, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10,
                                                cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_io_u_addr=rtn_io_u_addr,
                                                timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)
    def admin_delete_io_sq(self, buf=None, fuse=0, psdt=0, nsid=1, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                           wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                           **kwargs):
        if hasattr(self.vendor_commands, "admin_delete_io_sq"):
            return self.vendor_commands.admin_delete_io_sq(buf, fuse, psdt, nsid, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size, wait_completed,
                                                           rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            self.admin_passthru(opcode=0x00, buf=buf, fuse=fuse, psdt=psdt, nsid=nsid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12,
                                cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                *args, **kwargs)
    def admin_create_io_sq(self, buf=None, fuse=0, psdt=0, nsid=1, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                           wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                           **kwargs):
        if hasattr(self.vendor_commands, "admin_create_io_sq"):
            return self.vendor_commands.admin_create_io_sq(buf, fuse, psdt, nsid, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size, wait_completed,
                                                           rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            self.admin_passthru(opcode=0x01, buf=buf, fuse=fuse, psdt=psdt, nsid=nsid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12,
                                cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                *args, **kwargs)

    def admin_get_log_page(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lid=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                           cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                           *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_page"):
            return self.vendor_commands.admin_get_log_page(buf, nsid, fuse, psdt, data_len, rae, lsp, lid, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                           wait_completed, timeout, rtn_cmds_u_addr,io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args,
                                                           **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("get-log", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                numd = (data_len >> 2) - 1
                cdw10 = ((numd & 0xffff) << 16) | ((rae & 1) << 15) | ((lsp & 0x7f) << 8) | (lid & 0xff)
                cdw11 = (numd >> 16) | ((lsi & 0xff) << 16)
                cdw12 = lpo & 0xffffffff
                cdw13 = lpo >> 32
                cdw14 = (uidx & 0x7f) | ((ot & 0x1) << 23) | ((csi & 0x7f) << 24)
                if show_log:
                    self.show_func_local_param(self.admin_get_log_page)
                return self.device.send_admin_cmds(opcode=0x02, buf=buf, fuse=fuse, psdt=psdt, nsid=nsid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10,
                                                   cdw11= cdw11, cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=data_len, wait_completed=wait_completed,
                                                   rtn_cmds_u_addr=rtn_cmds_u_addr, timeout= timeout, io_status_code_expected=io_status_code_expected,
                                                   io_status_code_type_expected=io_status_code_type_expected)

    def admin_get_log_supported_log_page(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0,
                                         prp2=0, cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                         app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_supported_log_page"):
            return self.vendor_commands.admin_get_log_supported_log_page(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                         wait_completed, timeout, rtn_cmds_u_addr,io_status_code_expected, io_status_code_type_expected,
                                                                         app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "supported_log_page"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x0, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_error_info(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                 cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                 show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_error_info"):
            return self.vendor_commands.admin_get_log_error_info(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                 wait_completed, timeout, rtn_cmds_u_addr,io_status_code_expected, io_status_code_type_expected, app_type, show_log,
                                                                 *args, **kwargs)
        else:
            app_type = app_type if not app_type else "error-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x01, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_smart(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw15=0,
                            wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                            *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_smart"):
            return self.vendor_commands.admin_get_log_smart(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15, wait_completed,
                                                            timeout, rtn_cmds_u_addr,io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "smart-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x02, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr= rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_fw_slot(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw15=0,
                              wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                              *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_fw_slot"):
            return self.vendor_commands.admin_get_log_fw_slot(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,  wait_completed,
                                                              timeout, rtn_cmds_u_addr,io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "fw-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x03, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr= rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_changed_ns(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                 cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                 show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_changed_ns"):
            return self.vendor_commands.admin_get_log_changed_ns(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                 wait_completed, timeout, rtn_cmds_u_addr,io_status_code_expected, io_status_code_type_expected, app_type, show_log,
                                                                 *args, **kwargs)
        else:
            app_type = app_type if not app_type else "changed-ns-list-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x04, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_cmd_effects(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                  cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                  show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_cmd_effects"):
            return self.vendor_commands.admin_get_log_cmd_effects(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                  wait_completed, timeout, rtn_cmds_u_addr,io_status_code_expected, io_status_code_type_expected, app_type, show_log,
                                                                  *args, **kwargs)
        else:
            app_type = app_type if not app_type else "effects-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x05, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_device_self_test(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                       cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                       app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_device_self_test"):
            return self.vendor_commands.admin_get_log_device_self_test(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                       wait_completed, timeout, rtn_cmds_u_addr,io_status_code_expected, io_status_code_expected, app_type, show_log,
                                                                       *args, **kwargs)
        else:
            app_type = app_type if not app_type else "self-test-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x06, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_telemetry_host(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                     cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                     app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_telemetry_host"):
            return self.vendor_commands.admin_get_log_telemetry_host(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                     wait_completed, timeout, rtn_cmds_u_addr,io_status_code_expected, io_status_code_type_expected, app_type,
                                                                     show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "telemetry-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x07, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_telemetry_ctrl(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                     cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                     app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_telemetry_ctrl"):
            return self.vendor_commands.admin_get_log_telemetry_ctrl(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                     wait_completed, timeout, rtn_cmds_u_addr,io_status_code_expected, io_status_code_type_expected, app_type,
                                                                     show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "telemetry-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x08, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_endurance_group(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                      cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                      app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_endurance_group"):
            return self.vendor_commands.admin_get_log_endurance_group(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                      wait_completed, timeout, rtn_cmds_u_addr,io_status_code_expected, io_status_code_type_expected, app_type,
                                                                      show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "endurance-group-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x09, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_predictable_lat_nvmset(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0,
                                             prp2=0, cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0,
                                             io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_predictable_lat_nvmset"):
            return self.vendor_commands.admin_get_log_predictable_lat_nvmset(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                             wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "predictable-lat-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x0a, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_predictable_lat_agg(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0,
                                          prp2=0, cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                          app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_predictable_lat_agg"):
            return self.vendor_commands.admin_get_log_predictable_lat_agg(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                          wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "pred-lat-event-agg-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x0b, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_ana(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw15=0,
                          wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                          **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_ana"):
            return self.vendor_commands.admin_get_log_ana(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,  wait_completed,
                                                          timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "ana-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x0c, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_persistent_event(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                       cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                       app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_persistent_event"):
            return self.vendor_commands.admin_get_log_persistent_event(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                       wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "persistent-event-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x0d, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_lba_status(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                 cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                 show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_lba_status"):
            return self.vendor_commands.admin_get_log_lba_status(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                 wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "lba-status-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x0e, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_endurance_grp_evt(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                        cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                        app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_endurance_grp_evt"):
            return self.vendor_commands.admin_get_log_endurance_grp_evt(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                        wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "endurance-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x0f, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_media_unit_status(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                        cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                        show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_media_unit_status"):
            return self.vendor_commands.admin_get_log_media_unit_status(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                        wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "media-unit-status"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x10, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_supported_cap_cfg_list(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0,
                                             prp2=0, cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                             app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_supported_cap_cfg_list"):
            return self.vendor_commands.admin_get_log_supported_cap_cfg_list(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                             wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args,
                                                                             **kwargs)
        else:
            app_type = app_type if not app_type else "supported-cap-cfg-list"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x11, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_fid_supported_effects(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0,
                                            prp2=0, cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                            app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_fid_supported_effects"):
            return self.vendor_commands.admin_get_log_fid_supported_effects(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                            wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args,
                                                                            **kwargs)
        else:
            app_type = app_type if not app_type else "fid-support-effects-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x12, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_mi_cmd_supported_effects(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0,
                                               prp2=0, cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                               app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_mi_cmd_supported_effects"):
            return self.vendor_commands.admin_get_log_mi_cmd_supported_effects(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                               wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args,
                                                                               **kwargs)
        else:
            app_type = app_type if not app_type else "mi-cmd-supported-effects"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x13, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_cmd_feature_lockdown(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0,
                                           prp2=0, cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0,
                                           io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_cmd_feature_lockdown"):
            return self.vendor_commands.admin_get_log_cmd_feature_lockdown(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                           wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "get-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x14, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)


    def admin_get_log_boot_partition(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                     cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                     show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_boot_partition"):
            return self.vendor_commands.admin_get_log_boot_partition(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                     wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "boot-part-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x15, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_rotational_media_info(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0,
                                            prp2=0, cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                            app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_rotational_media_info"):
            return self.vendor_commands.admin_get_log_rotational_media_info(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                            wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args,
                                                                            **kwargs)
        else:
            app_type = app_type if not app_type else "get-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x16, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_dispersed_ns_participating_nvm_subsystems(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0,
                                                                mptr=0, prp1=0, prp2=0, cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0,
                                                                io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_dispersed_ns_participating_nvm_subsystems"):
            return self.vendor_commands.admin_get_log_dispersed_ns_participating_nvm_subsystems(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr,
                                                                                                prp1, prp2, cdw15, wait_completed, timeout, rtn_cmds_u_addr,
                                                                                                io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "get-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x17, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)
    def admin_get_log_mgmt_addr_list(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                     cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                     show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_mgmt_addr_list"):
            return self.vendor_commands.admin_get_log_mgmt_addr_list(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                     wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "get-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x18, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_phy_rx_eom(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                 cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                 show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_phy_rx_eom"):
            return self.vendor_commands.admin_get_log_phy_rx_eom(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                 wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "get-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x19, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_fdp_configs(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                  cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                  show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_fdp_configs"):
            return self.vendor_commands.admin_get_log_fdp_configs(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                  wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "get-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x20, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_fdp_ruh_usage(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                    cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                    app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_fdp_ruh_usage"):
            return self.vendor_commands.admin_get_log_fdp_ruh_usage(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                    wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "get-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x21, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_fdp_stats(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw15=0,
                                wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                                *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_fdp_stats"):
            return self.vendor_commands.admin_get_log_fdp_stats(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "get-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x22, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_fdp_event(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw15=0,
                                wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                                *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_fdp_event"):
            return self.vendor_commands.admin_get_log_fdp_event(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "get-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x23, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_discover(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw15=0,
                               wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                               show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_discover"):
            return self.vendor_commands.admin_get_log_discover(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                               wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "get-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x70, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr,io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_reservation_notification(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0,
                                               prp2=0, cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                               app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_reservation_notification"):
            return self.vendor_commands.admin_get_log_reservation_notification(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                               wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args,
                                                                               **kwargs)
        else:
            app_type = app_type if not app_type else "resv-notif-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x80, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_sanitize(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw15=0,
                               wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                               **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_sanitize"):
            return self.vendor_commands.admin_get_log_sanitize(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                               wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "sanitize-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0x81, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)

    def admin_get_log_zns_changed_zones(self, buf=None, nsid=None, fuse=0, psdt=0, data_len=0, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                        cdw15=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                        show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_log_zns_changed_zones"):
            return self.vendor_commands.admin_get_log_zns_changed_zones(buf, nsid, fuse, psdt, data_len, rae, lsp, lsi, lpo, csi, ot, uidx, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                        wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "get-log"
            return self.admin_get_log_page(buf=buf, nsid=nsid, fuse=fuse, psdt=psdt, data_len=data_len, rae=rae, lsp=lsp, lid=0xbf, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                           cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout,
                                           rtn_cmds_u_addr=rtn_cmds_u_addr, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                           app_type=app_type, show_log=show_log, *args, **kwargs)


    def admin_delete_io_cq(self, buf=None, fuse=0, psdt=0, nsid=1, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                           wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                           **kwargs):
        if hasattr(self.vendor_commands, "admin_delete_io_cq"):
            return self.vendor_commands.admin_delete_io_cq(buf, fuse, psdt, nsid, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size, wait_completed,
                    timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            self.admin_passthru(opcode=0x04, buf=buf, fuse=fuse, psdt=psdt, nsid=nsid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12,
                                cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                *args, **kwargs)

    def admin_create_io_cq(self, buf=None, fuse=0, psdt=0, nsid=1, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                           wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                           **kwargs):
        if hasattr(self.vendor_commands, "admin_create_io_cq"):
            return self.vendor_commands.admin_create_io_cq(buf, fuse, psdt, nsid, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size, wait_completed,
                    timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            self.admin_passthru(opcode=0x05, buf=buf, fuse=fuse, psdt=psdt, nsid=nsid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12,
                                cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                *args, **kwargs)

    def admin_identify(self, buf=None, cntid=0, cns=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw15=0,
                       buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                       *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify"):
            return self.vendor_commands.admin_identify(buf, cntid, cns, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                       wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                cdw10 = (cntid & 0xffff) | cns
                cdw11 = (csi & 0xff) << 24 | (cnssid & 0xffff)
                cdw14 = uidx
                if show_log:
                    self.show_func_local_param(self.admin_identify_ns)
                return self.device.send_admin_cmds(opcode=0x06, buf=buf, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10,
                                                   cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,cdw14=cdw14,
                                                   cdw15=cdw15, io_status_code_type_expected=io_status_code_type_expected, io_status_code_expected=io_status_code_expected,
                                                   buf_size=buf_size, timeout=timeout)
    def admin_identify_ns(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw15=0,
                          buf_size=0 ,wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                          *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_ns"):
            return self.vendor_commands.admin_identify_ns(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                          wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "id-ns"
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x0, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, buf_size=buf_size,
                                       app_type=app_type, show_log=show_log,*args, **kwargs)

    def admin_identify_ctrl(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw15=0,
                            buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                            *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_ctrl"):
            return self.vendor_commands.admin_identify_ctrl(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                            wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else "id-ctrl"
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x01, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size, *args, **kwargs)

    def admin_identify_ns_active_list(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                      cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                      app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_ns_active_list"):
            return self.vendor_commands.admin_identify_ns_active_list(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                      wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x02, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_ns_desc_list(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw15=0,
                                    buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                    show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_ns_desc_list"):
            return self.vendor_commands.admin_identify_ns_desc_list(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                    wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x03, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size, *args, **kwargs)

    def admin_identify_nvmeset_list(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                    cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                    app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_nvmeset_list"):
            return self.vendor_commands.admin_identify_nvmeset_list(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                    wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x04, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_csi_ns(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw15=0,
                              buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                              show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_csi_ns"):
            return self.vendor_commands.admin_identify_csi_ns(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                              wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x05, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_csi_ctrl(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw15=0,
                                buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_csi_ctrl"):
            return self.vendor_commands.admin_identify_csi_ctrl(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x06, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_csi_ns_active_list(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                          cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                          app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_csi_ns_active_list"):
            return self.vendor_commands.admin_identify_csi_ns_active_list(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                          buf_size, wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args,
                                                                          **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x07, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_csi_independent_id_ns(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                             cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                             app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_csi_independent_id_ns"):
            return self.vendor_commands.admin_identify_csi_independent_id_ns(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                             buf_size, wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log,
                                                                             *args, **kwargs)
        else:
            app_type = app_type if not app_type else "cmdset-ind-id-ns"
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x08, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_ns_user_data_format(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                           cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                           app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_ns_user_data_format"):
            return self.vendor_commands.admin_identify_ns_user_data_format(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                           buf_size, wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log,
                                                                           *args, **kwargs)
        else:
            app_type = app_type if not app_type else "id-ns-lba-format"
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x09, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_csi_ns_user_data_format(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                               cdw13=0, cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0,
                                               io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_csi_ns_user_data_format"):
            return self.vendor_commands.admin_identify_csi_ns_user_data_format(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                               buf_size, wait_completed, timeout,rtn_cmds_u_addr,io_status_code_expected, io_status_code_type_expected,
                                                                               app_type, show_log, *args, **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x0a, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)
    def admin_identify_allocated_ns_id_list(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                            cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                            app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_allocated_ns_id_list"):
            return self.vendor_commands.admin_identify_allocated_ns_id_list(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                            buf_size, wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log,
                                                                            *args, **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x10, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size, *args, **kwargs)

    def admin_identify_allocated_ns(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                    cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                    app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_allocated_ns"):
            return self.vendor_commands.admin_identify_allocated_ns(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                    wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x11, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_ns_ctrl_list(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                    cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                    app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_ns_ctrl_list"):
            return self.vendor_commands.admin_identify_ns_ctrl_list(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                    wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x12, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_ctrl_list(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw15=0,
                                 buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                 show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_ctrl_list"):
            return self.vendor_commands.admin_identify_ctrl_list(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                 wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x13, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_primary_ctrl_cap(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                        cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                        app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_primary_ctrl_cap"):
            return self.vendor_commands.admin_identify_primary_ctrl_cap(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                        buf_size, wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args,
                                                                        **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x14, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_secondary_ctrl_list(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                           cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                           app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_secondary_ctrl_list"):
            return self.vendor_commands.admin_identify_secondary_ctrl_list(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                           buf_size, wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args,
                                                                           **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x15, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_ns_granularity(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                      cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                      app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_ns_granularity"):
            return self.vendor_commands.admin_identify_ns_granularity(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                      wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else 'id-ns-granularity'
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x16, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_uuid_list(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw15=0,
                                 buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                 show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_uuid_list"):
            return self.vendor_commands.admin_identify_uuid_list(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                 wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else 'id-uuid'
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x17, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)
    def admin_identify_domain_list(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                   cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                   app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_domain_list"):
            return self.vendor_commands.admin_identify_domain_list(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                   wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            app_type = app_type if not app_type else 'id-domain'
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x18, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_endurance_group_id(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                          cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                          app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_endurance_group_id"):
            return self.vendor_commands.admin_identify_endurance_group_id(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                          buf_size, wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args,
                                                                          **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x19, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)

    def admin_identify_csi_allocated_ns_list(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                             cdw13=0, cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0,
                                             io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_csi_allocated_ns_list"):
            return self.vendor_commands.admin_identify_csi_allocated_ns_list(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                             buf_size, wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log,
                                                                             *args, **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x1a, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)
    def admin_identify_csi_id_ns(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw15=0,
                                 buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                 show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_csi_id_ns"):
            return self.vendor_commands.admin_identify_csi_id_ns(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                 wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x1b, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size, *args, **kwargs)

    def admin_identify_cmd_set_structure(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                         cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                         app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_cmd_set_structure"):
            return self.vendor_commands.admin_identify_cmd_set_structure(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                         buf_size, wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log, *args,
                                                                         **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x1c, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size, *args, **kwargs)

    def admin_identify_csi_allocated_ns(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                        cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0,
                                        app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_csi_allocated_ns"):
                return self.vendor_commands.admin_identify_csi_allocated_ns(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                            buf_size, wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type, show_log,
                                                                            *args, **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x1f, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)
    def admin_identify_supported_ctrl_state_format(self, buf=None, cntid=0, csi=0, cnssid=0, uidx=0, nsid=None, fuse=0, psdt=0, cid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                                   cdw13=0, cdw15=0, buf_size=0, wait_completed=1, timeout=None, rtn_cmds_u_addr=False, io_status_code_expected=0,
                                                   io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_identify_supported_ctrl_state_format"):
            return self.vendor_commands.admin_identify_supported_ctrl_state_format(buf, cntid, csi, cnssid, uidx, nsid, fuse, psdt, cid, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13,
                                                                                   cdw15, buf_size, wait_completed, timeout, rtn_cmds_u_addr,io_status_code_type_expected, app_type,
                                                                                   show_log, *args, **kwargs)
        else:
            return self.admin_identify(buf=buf, cntid=cntid, cns=0x20, csi=csi, cnssid=cnssid, uidx=uidx, nsid=nsid, fuse=fuse, psdt=psdt, cid=cid, cdw2=cdw2, cdw3=cdw3, mptr=mptr,
                                       prp1=prp1, prp2=prp2, cdw12=cdw12, cdw13=cdw13, cdw15=cdw15, wait_completed=wait_completed, timeout=timeout, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                       io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                       buf_size=buf_size,*args, **kwargs)
    def amind_abort(self, nsid=None, cid=0, sqid=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0, wait_completed=1, timeout=None,
                    rtn_cmds_u_addr=False, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "amind_abort"):
            return self.vendor_commands.amind_abort(nsid, cid, sqid, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size, wait_completed, timeout,
                                                    rtn_cmds_u_addr, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("abort", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                cdw10 = (sqid) | (cid << 16)
                if show_log:
                    self.show_func_local_param(self.amind_abort)
                return self.device.send_admin_cmds(opcode=0x08, buf=None, fuse=0, psdt=0, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12,
                                                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)

    def admin_set_features(self, buf=None, sv=0, fid=0, uidx=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw15=0, buf_size=0,
                           wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                           **kwargs):
        if hasattr(self.vendor_commands, "admin_set_features"):
            return self.vendor_commands.admin_set_features(buf, sv, fid, uidx, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw15, buf_size, wait_completed,
                                                           rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("set-feature", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | (fid & 0xff)
                cdw14 = uidx
                if show_log:
                    self.show_func_local_param(self.admin_set_features)
                return self.device.send_admin_cmds(opcode=0x09, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size, nsid=nsid, wait_completed=wait_completed,
                                                   rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout, io_status_code_expected=io_status_code_expected,
                                                   io_status_code_type_expected=io_status_code_type_expected)

    def admin_feature_arbitration(self, feature_type=0, buf=None, sv=0, uidx=0, hpw=0, mpw=0, lpw=0, ab=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                  cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                  app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_arbitration"):
            return self.vendor_commands.admin_feature_arbitration(feature_type, buf, sv, uidx, hpw, mpw, lpw, ab, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                  buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type,
                                                                  show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 1
                cdw11 = ab & 0x3 | (lpw & 0xff) << 8 | (mpw & 0xff) << 16 | (hpw & 0xff) << 24
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_arbitration)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_power_mgmt(self, feature_type=0, buf=None, sv=0, uidx=0, wh=0, ps=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw15=0,
                                 buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                 show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_power_mgmt"):
            return self.vendor_commands.admin_feature_power_mgmt(feature_type, buf, sv, uidx, wh, ps, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                 wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,io_status_code_type_expected, app_type, show_log,
                                                                 *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 2
                cdw11 = ps & 0xf | (wh & 0xf) << 5
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_power_mgmt)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)


    def admin_feature_temperature_threshold(self, feature_type=0, buf=None, sv=0, uidx=0, tmpthh=0, thsel=0, tmpsel=0, tmph=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0,
                                            prp1=0, prp2=0, cdw12=0, cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                            io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_temperature_threshold"):
                return self.vendor_commands.admin_feature_temperature_threshold(feature_type, buf, sv, uidx, tmpthh, thsel, tmpsel, tmph, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1,
                                                                                prp2, cdw12, cdw13, cdw15, buf_size, wait_completed, rtn_cmds_u_addr,timeout, io_status_code_expected,
                                                                                io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 4
                cdw11 = tmph & 0xffff | (tmpsel & 0xf) << 16 | (thsel & 0x3) << 20 | (tmpthh & 0x7) << 22
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_temperature_threshold)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)


    def admin_feature_volstile_write_cache(self, feature_type=0, buf=None, sv=0, uidx=0, wce=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                           cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                           app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_volstile_write_cache"):
                return self.vendor_commands.admin_feature_volstile_write_cache(feature_type, buf, sv, uidx, wce, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                               buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                               io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 6
                cdw11 = wce
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_volstile_write_cache)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)



    def admin_feature_number_of_queues(self, feature_type=0, buf=None, sv=0, uidx=0, ncqr=0, nsqr=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                       cdw13=0, cdw14=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                       io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_number_of_queues"):
                return self.vendor_commands.admin_feature_number_of_queues(feature_type, buf, sv, uidx, ncqr, nsqr, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13,
                                                                           cdw14, cdw15, buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                           io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 7
                cdw11 = ncqr | (nsqr & 0xffff) << 16
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_number_of_queues)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_interrupt_coalescing(self, feature_type=0, buf=None, sv=0, uidx=0, time=0, thr=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                           cdw13=0, cdw14=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                           io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_interrupt_coalescing"):
            return self.vendor_commands.admin_feature_interrupt_coalescing(feature_type, buf, sv, uidx, time, thr, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13,
                                                                           cdw14, cdw15, buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                           io_status_code_type_expected, app_type, show_log, *args, **kwargs)
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 8
                cdw11 = (thr & 0xff) | (time & 0xff) << 8
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_interrupt_coalescing)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_interrupt_vector_config(self, feature_type=0, buf=None, sv=0, uidx=0, cd=0, iv=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                              cdw13=0, cdw14=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                              io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_interrupt_vector_config"):
            return self.vendor_commands.admin_feature_interrupt_vector_config(feature_type, buf, sv, uidx, cd, iv, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw14,
                                                                              cdw15, buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                              io_status_code_type_expected, app_type, show_log, *args, **kwargs)
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 9
                cdw11 = (iv & 0xffff) | (cd & 0x1) << 16
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_interrupt_vector_config)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)



    def admin_feature_async_event_cfg(self, feature_type=0, buf=None, sv=0, uidx=0, dlpcn=0, hdlpcn=0, adlpcn=0, pmdrlpcn=0, zdcn=0, ansan=0, rgrp0=0, rassn=0, tthry=0, nnsshdn=0,
                                      egealcn=0, lsian=0, plealcn=0, anacn=0, tln=0, fan=0, nan=0, shcw=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                      cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                      app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_async_event_cfg"):
            return self.vendor_commands.admin_feature_async_event_cfg(feature_type, buf, sv, uidx, dlpcn, hdlpcn, adlpcn, pmdrlpcn, zdcn, ansan, rgrp0, rassn, tthry, nnsshdn, egealcn,
                                                                      lsian, plealcn, anacn, tln, fan, nan, shcw, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                      buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,
                                                                      app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0xB
                cdw11 = (shcw & 0xff | nan << 8 | fan << 9 | tln << 10 | anacn << 11 | plealcn << 12 | lsian << 13 | egealcn << 14 |
                         nnsshdn << 15 | tthry << 16 | rassn << 17 | rgrp0 << 18 | ansan << 19 | zdcn << 27 | pmdrlpcn << 28 |
                         adlpcn << 29 | hdlpcn << 30 | dlpcn << 31)
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_async_event_cfg)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_auto_power_state_transition(self, feature_type=0, buf=None, sv=0, uidx=0, apste=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                                  cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                                  io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_auto_power_state_transition"):
            return self.vendor_commands.admin_feature_auto_power_state_transition(feature_type, buf, sv, uidx, apste, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13,
                                                                                  cdw15, buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                                  io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0xc
                cdw11 = apste
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_auto_power_state_transition)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_host_mem_buffer(self, feature_type=0, buf=None, sv=0, uidx=0, nsid=None, ctz=0, hmnare=0, mr=0, ehm=0, hsize=0, hmdlla=0, hmdlua=0, hmdlec=0, fuse=0,
                                      psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                      io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_host_mem_buffer"):
            return self.vendor_commands.admin_feature_host_mem_buffer(feature_type, buf, sv, uidx, nsid, ctz, hmnare, mr, ehm, hsize, hmdlla, hmdlua, hmdlec, fuse, psdt, cdw2, cdw3,
                                                                      mptr, prp1, prp2, buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                      io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0xd
                cdw11 = (ehm & 0x1) | ((mr & 0x1) << 1) | ((hmnare & 0x1) << 2) | ((ctz & 0x1) << 3)
                cdw12 = hsize
                cdw13 = hmdlla
                cdw14 = hmdlua
                cdw15 = hmdlec
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_host_mem_buffer)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)


    def admin_feature_timestamp(self, feature_type=0, buf=None, sv=0, uidx=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw15=0,
                                buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_timestamp"):
            return self.vendor_commands.admin_feature_timestamp(feature_type, buf, sv, uidx, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw15, buf_size,
                                                                wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log,
                                                                *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0xe
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_timestamp)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)


    def admin_feature_keep_alive_timer(self, feature_type=0, buf=None, sv=0, uidx=0, kato=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                       cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                       app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_keep_alive_timer"):
            return self.vendor_commands.admin_feature_keep_alive_timer(feature_type, buf, sv, uidx, kato, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                       wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type,
                                                                       show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0xf
                cdw11 = kato
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_set_features)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_host_ctrl_thermal_mgmt(self, feature_type=0, buf=None, sv=0, uidx=0, tmt=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                             cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                             app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_host_ctrl_thermal_mgmt"):
            return self.vendor_commands.admin_feature_host_ctrl_thermal_mgmt(feature_type, buf, sv, uidx, tmt, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                             buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,
                                                                             app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x10
                cdw11 = tmt
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_host_ctrl_thermal_mgmt)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_non_operational_power_state_cfg(self, feature_type=0, buf=None, sv=0, uidx=0, noppme=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                                      cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                                      io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_non_operational_power_state_cfg"):
            return self.vendor_commands.admin_feature_non_operational_power_state_cfg(feature_type, buf, sv, uidx, noppme, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13,
                                                                                      cdw15, buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                                      io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x11
                cdw11 = noppme
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_non_operational_power_state_cfg)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)


    def admin_feature_read_recovery_level_cfg(self, feature_type=0, buf=None, sv=0, uidx=0, nvmsetid=0, rrl=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                              cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                              io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_read_recovery_level_cfg"):
            return self.vendor_commands.admin_feature_read_recovery_level_cfg(feature_type, buf, sv, uidx, nvmsetid, rrl, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw13, cdw15,
                                                                              buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,
                                                                              app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x12
                cdw11 = nvmsetid
                cdw12 = rrl
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_read_recovery_level_cfg)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_predictable_latency_mode_cfg(self, feature_type=0, buf=None, sv=0, uidx=0, nvmsetid=0, lpe=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                                   cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                                   io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_predictable_latency_mode_cfg"):
            return self.vendor_commands.admin_feature_predictable_latency_mode_cfg(feature_type, buf, sv, uidx, nvmsetid, lpe, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw13,
                                                                                   cdw15, buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                                   io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x13
                cdw11 = nvmsetid
                cdw12 = lpe
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_predictable_latency_mode_cfg)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_predictable_latency_mode_window(self, feature_type=0, buf=None, sv=0, uidx=0, nvmsetid=0, wsel=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0,
                                                      prp2=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                                      io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_predictable_latency_mode_window"):
            return self.vendor_commands.admin_feature_predictable_latency_mode_window(feature_type, buf, sv, uidx, nvmsetid, wsel, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2,
                                                                                      cdw13, cdw14, cdw15, buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                                      io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x13
                cdw11 = nvmsetid & 0xffff
                cdw12 = wsel & 0x7
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_predictable_latency_mode_window)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_host_behavior_support(self, feature_type=0, buf=None, sv=0, uidx=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0,
                                            cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                            app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_host_behavior_support"):
            return self.vendor_commands.admin_feature_host_behavior_support(feature_type, buf, sv, uidx, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw15,
                                                                            buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,
                                                                            app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x16
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_host_behavior_support)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_sanitize_cfg(self, feature_type=0, buf=None, sv=0, uidx=0, nodrm=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw15=0,
                                   buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                   show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_sanitize_cfg"):
            return self.vendor_commands.admin_feature_sanitize_cfg(feature_type, buf, sv, uidx, nodrm, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                   wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log,
                                                                   *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x17
                cdw11 = nodrm
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_sanitize_cfg)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)


    def admin_feature_endurance_group_event_cfg(self, feature_type=0, buf=None, sv=0, uidx=0, egcw=0, endgid=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                                cdw12=0, cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                                io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_endurance_group_event_cfg"):
            return self.vendor_commands.admin_feature_endurance_group_event_cfg(feature_type, buf, sv, uidx, egcw, endgid, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13,
                                                                                cdw15, buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                                io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x18
                cdw11 = endgid & 0xffff | (egcw & 0xff) << 18
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_endurance_group_event_cfg)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_io_cmd_set_profile(self, feature_type=0, buf=None, sv=0, uidx=0, iocsci=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                         cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                         show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_io_cmd_set_profile"):
            return self.vendor_commands.admin_feature_io_cmd_set_profile(feature_type, buf, sv, uidx, iocsci, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                         buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,
                                                                         app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x19
                cdw11 = iocsci
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_io_cmd_set_profile)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_spinup_ctrl(self, feature_type=0, buf=None, sv=0, uidx=0, iocsci=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw15=0,
                                  buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                  show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_spinup_ctrl"):
            return self.vendor_commands.admin_feature_spinup_ctrl(feature_type, buf, sv, uidx, iocsci, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                  wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log,
                                                                  *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x1a
                cdw11 = iocsci
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_spinup_ctrl)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_power_loss_signaling_cfg(self, feature_type=0, buf=None, sv=0, uidx=0, plsm=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                               cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                               io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_power_loss_signaling_cfg"):
            return self.vendor_commands.admin_feature_power_loss_signaling_cfg(feature_type, buf, sv, uidx, plsm, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                               buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                               io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x1b
                cdw11 = plsm
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_power_loss_signaling_cfg)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)
    def admin_feature_flexibe_data_pacement(self, feature_type=0, buf=None, sv=0, uidx=0, endgid=0, fdpcidx=0, fdpe=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0,
                                            prp2=0, cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                            io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_flexibe_data_pacement"):
            return self.vendor_commands.admin_feature_flexibe_data_pacement(feature_type, buf, sv, uidx, endgid, fdpcidx, fdpe, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw13,
                                                                            cdw15, buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                            io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x1d
                cdw11 = endgid
                cdw12 = (fdpcidx & 0xff) << 8| fdpe
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_flexibe_data_pacement)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_flexibe_data_pacement_event(self, feature_type=0, buf=None, sv=0, uidx=0, noet=0, phndl=0, fdpee=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0,
                                                  prp2=0, cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=0, timeout=None, io_status_code_expected=0,
                                                  io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_flexibe_data_pacement_event"):
            return self.vendor_commands.admin_feature_flexibe_data_pacement_event(feature_type, buf, sv, uidx, noet, phndl, fdpee, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw13,
                                                                                  cdw15, buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                                  io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x1e
                cdw11 = (phndl & 0xffff) | (noet & 0xff) << 16
                cdw12 = fdpee
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_flexibe_data_pacement_event)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_namespace_admin_label(self, feature_type=0, buf=None, sv=0, uidx=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0,cdw13=0,
                                            cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                            app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_namespace_admin_label"):
            return self.vendor_commands.admin_feature_namespace_admin_label(feature_type, buf, sv, uidx, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw15, 
                                                                            buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,
                                                                            app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x1f
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_namespace_admin_label)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_ctrl_data_queue(self, feature_type=0, buf=None, sv=0, uidx=0, nsid=None, etpt=0, cdqid=0, hp=0, tpt=0, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                      cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                      app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_ctrl_data_queue"):
            return self.vendor_commands.admin_feature_ctrl_data_queue(feature_type, buf, sv, uidx, nsid, etpt, cdqid, hp, tpt, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw15,
                                                                      buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,
                                                                      app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x21
                cdw11 = (etpt & 0x1) << 31 | (cdqid & 0xffff)
                cdw12 = hp
                cdw13 = tpt
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_ctrl_data_queue)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_embedded_mgmt_ctrl_addr(self, feature_type=0, buf=None, sv=0, uidx=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, 
                                              cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                              app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_embedded_mgmt_ctrl_addr"):
            return self.vendor_commands.admin_feature_embedded_mgmt_ctrl_addr(feature_type, buf, sv, uidx, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw15,
                                                                              buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,
                                                                              app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x78
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_embedded_mgmt_ctrl_addr)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_host_mgmt_agent_addr(self, feature_type=0, buf=None, sv=0, uidx=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, 
                                           cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                           app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_host_mgmt_agent_addr"):
            return self.vendor_commands.admin_feature_host_mgmt_agent_addr(feature_type, buf, sv, uidx, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw15,
                                                                           buf_size, wait_completed, rtn_cmds_u_addr, timeout,io_status_code_expected, io_status_code_type_expected,
                                                                           app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x79
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_host_mgmt_agent_addr)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_host_metadata(self, feature_type=0, buf=None, sv=0, uidx=0, ea=0, gdhm=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                    cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                    app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_host_metadata"):
            return self.vendor_commands.admin_feature_host_metadata(feature_type, buf, sv, uidx, ea, gdhm, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                    buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,
                                                                    app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x7d
                cdw11 = (ea & 0x1) << 13 if feature_type else gdhm & 0x1
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_host_metadata)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)


    def admin_feature_host_ctrl_metadata(self, feature_type=0, buf=None, sv=0, uidx=0, ea=0, gdhm=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                         cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                         app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_host_ctrl_metadata"):
            return self.vendor_commands.admin_feature_host_ctrl_metadata(feature_type, buf, sv, uidx, ea, gdhm, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                         buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,
                                                                         app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x7e
                cdw11 = (ea & 0x1) << 13 if feature_type else gdhm & 0x1
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_host_ctrl_metadata)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_host_ns_metadata(self, feature_type=0, buf=None, sv=0, uidx=0, ea=0, gdhm=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                       cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                       app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_host_ns_metadata"):
            return self.vendor_commands.admin_feature_host_ns_metadata(feature_type, buf, sv, uidx, ea, gdhm, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                       buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,
                                                                       app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x7f
                cdw11 = (ea & 0x1) << 13 if feature_type else gdhm & 0x1
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_host_ns_metadata)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_software_progress_marker(self, feature_type=0, buf=None, sv=0, uidx=0, pbslc=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                               cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                               io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_software_progress_marker"):
            return self.vendor_commands.admin_feature_software_progress_marker(feature_type, buf, sv, uidx, pbslc, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                               buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                               io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x80
                cdw11 = (pbslc & 0xff) << 13
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_software_progress_marker)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_host_identifier(self, feature_type=0, buf=None, sv=0, uidx=0, exhid=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                      cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                      app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_host_identifier"):
            return self.vendor_commands.admin_feature_host_identifier(feature_type, buf, sv, uidx, exhid, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15, buf_size,
                                                                      wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type,
                                                                      show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x81
                cdw11 = (exhid & 0x1)
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_host_identifier)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_reservation_notification_mask(self, feature_type=0, buf=None, sv=0, uidx=0, regpre=0, resrel=0, respre=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0,
                                                    prp1=0, prp2=0, cdw12=0,cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None,
                                                    io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_reservation_notification_mask"):
            return self.vendor_commands.admin_feature_reservation_notification_mask(feature_type, buf, sv, uidx, regpre, resrel, respre, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2,
                                                                                    cdw12, cdw13, cdw15, buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                                    io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x82
                cdw11 = (respre & 0x1) << 3 | (resrel & 0x1) << 2 | (regpre & 0x1) << 1
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_reservation_notification_mask)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_reservation_persistence(self, feature_type=0, buf=None, sv=0, uidx=0, ptpl=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                              cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                              io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_reservation_persistence"):
            return self.vendor_commands.admin_feature_reservation_persistence(feature_type, buf, sv, uidx, ptpl, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                              buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,
                                                                              app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x83
                cdw11 = (ptpl & 0x1)
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_reservation_persistence)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_ns_write_protection_cfg(self, feature_type=0, buf=None, sv=0, uidx=0, wps=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0,
                                              cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                              app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_ns_write_protection_cfg"):
            return self.vendor_commands.admin_feature_ns_write_protection_cfg(feature_type, buf, sv, uidx, wps, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw15,
                                                                              buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,
                                                                              app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x84
                cdw11 = (wps & 0x1)
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_ns_write_protection_cfg)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_feature_boot_partition_write_protection_cfg(self, feature_type=0, buf=None, sv=0, uidx=0, bpwps=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                                                          cdw13=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0,
                                                          io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_feature_boot_partition_write_protection_cfg"):
            return self.vendor_commands.admin_feature_boot_partition_write_protection_cfg(feature_type, buf, sv, uidx, bpwps, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12,
                                                                                          cdw13, cdw15, buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,
                                                                                          io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                app_type = "set-feature" if feature_type else "get-feature"
                return self.run_nvme_cli_cmd(app_type, show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sv & 0x1) << 31) | 0x85
                cdw11 = (bpwps & 0x3f)
                cdw14 = uidx
                opcode = 0x09 if feature_type else 0x0A
                if show_log:
                    self.show_func_local_param(self.admin_feature_boot_partition_write_protection_cfg)
                return self.device.send_admin_cmds(opcode=opcode, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_get_features(self, buf=None, sel=0, fid=0, uidx=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw15=0, buf_size=0,
                           wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                           **kwargs):
        if hasattr(self.vendor_commands, "admin_get_features"):
            return self.vendor_commands.admin_get_features(buf, sel, fid, uidx, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw15, buf_size, wait_completed,
                                                           rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("get-feature", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = ((sel & 0x7) << 8) | (fid & 0xff)
                cdw14 = uidx
                if show_log:
                    self.show_func_local_param(self.admin_get_features)
                return self.device.send_admin_cmds(opcode=0x0a, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)
    def admin_async_event_request(self, fuse=0, psdt=0, nsid=None, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                                  wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                                  *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_async_event_request"):
            return self.vendor_commands.admin_async_event_request(fuse, psdt, nsid, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size,wait_completed,
                                                                  rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("aer", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                if show_log:
                    self.show_func_local_param(self.admin_async_event_request)
                return self.device.send_admin_cmds(opcode=0x0c, buf=None, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_namespace_management(self, buf=None, nsid=None, sel=0, csi=0, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                                   wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                                   *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_namespace_management"):
            return self.vendor_commands.admin_namespace_management(buf, nsid, sel, csi, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw14, cdw15, buf_size,
                                                                   wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log,
                                                                   *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                if sel == 0:
                    return self.run_nvme_cli_cmd("create-ns", show_log, *args, **kwargs)
                else:
                    return self.run_nvme_cli_cmd("delete-ns", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = sel
                cdw11 = (csi & 0xff) << 24
                if show_log:
                    self.show_func_local_param(self.admin_namespace_management)
                return self.device.send_admin_cmds(opcode=0x0d, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)
    def admin_fw_commit(self, nsid=None, bpid=0, ca=0, fs=0, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                        wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                        **kwargs):
        if hasattr(self.vendor_commands, "admin_fw_commit"):
            return self.vendor_commands.admin_fw_commit(nsid, bpid, ca, fs, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size, wait_completed,
                                                        rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("fw-commit", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                cdw10 = fs | (ca & 0x07) << 3 | bpid << 31
                if show_log:
                    self.show_func_local_param(self.admin_fw_commit)
                return self.device.send_admin_cmds(opcode=0x10, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12,
                                                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                                   io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, buf_size=buf_size)

    def admin_fw_image_download(self, buf=None, data_len=0, offset=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0,
                                wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                                **kwargs):
        if hasattr(self.vendor_commands, "admin_fw_image_download"):
            return self.vendor_commands.admin_fw_image_download(buf, data_len, offset, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw14, cdw15, wait_completed,
                                                                rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("fw-download", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (data_len >> 2) - 1
                cdw11 = offset
                if show_log:
                    self.show_func_local_param(self.admin_fw_commit)
                return self.device.send_admin_cmds(opcode=0x11, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=data_len)
    def admin_device_self_test(self, stc=0, dstp=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, buf_size=0, wait_completed=1,
                               rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_device_self_test"):
            return self.vendor_commands.admin_device_self_test(stc, dstp, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw14, buf_size, wait_completed,
                                                               rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("device-self-test", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                cdw10 = stc
                cdw15 = dstp
                if show_log:
                    self.show_func_local_param(self.admin_device_self_test)
                return self.device.send_admin_cmds(opcode=0x14, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,cdw12=cdw12,
                                                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                                   io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, buf_size=buf_size)

    def admin_namespace_attachment(self, buf, sel=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                                   wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                                   *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_namespace_attachment"):
            return self.vendor_commands.admin_namespace_attachment(sel, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size, wait_completed,
                                                                   rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                if sel == 0:
                    return self.run_nvme_cli_cmd("attach-ns", show_log, *args, **kwargs)
                else:
                    return self.run_nvme_cli_cmd("detach-ns", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                cdw10 = sel
                if show_log:
                    self.show_func_local_param(self.admin_namespace_attachment)
                return self.device.send_admin_cmds(opcode=0x15, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size, nsid=nsid, wait_completed=wait_completed,
                                                   rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout, io_status_code_expected=io_status_code_expected,
                                                   io_status_code_type_expected=io_status_code_type_expected)
    def admin_keep_alive(self, ofi=0, ifc=0, prhbt=0, scp=0, uidx=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                         wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                         **kwargs):
        if hasattr(self.vendor_commands, "admin_keep_alive"):
            return self.vendor_commands.admin_keep_alive(ofi, ifc, prhbt, scp, uidx, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw14, cdw15, buf_size,
                                                         wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args,
                                                         **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("keep-alive", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                cdw10 = scp | ((prhbt & 0x1) << 4) | ((ifc & 0x3) << 5) | ((ofi & 0xff) << 8)
                cdw11 = uidx
                if show_log:
                    self.show_func_local_param(self.admin_keep_alive)
                return self.device.send_admin_cmds(opcode=0x18, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,cdw12=cdw12,
                                                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                                   io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, buf_size=buf_size)

    def admin_directive_send(self, buf=None, data_len=0, dspec=0, dtype=0, doper=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw14=0,
                             cdw15=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                             *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_directive_send"):
            return self.vendor_commands.admin_directive_send(buf, data_len, dspec, dtype, doper, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw14, cdw15,
                                                             wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,io_status_code_type_expected, app_type, show_log, *args,
                                                             **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("dir-send", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (data_len >> 2) - 1
                cdw11 = (doper & 0xff) | ((dtype & 0xff) << 8) | ((dspec & 0xff) << 16)
                if show_log:
                    self.show_func_local_param(self.admin_directive_send)
                return self.device.send_admin_cmds(opcode=0x19, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=data_len)
    def admin_directive_receive(self, buf=None, data_len=0, dspec=0, dtype=0, doper=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw14=0,
                                cdw15=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                                *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_directive_receive"):
            return self.vendor_commands.admin_directive_receive(buf, data_len, dspec, dtype, doper, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw14, cdw15,
                                                                wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,io_status_code_type_expected, app_type, show_log,
                                                                *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("dir-receive", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (data_len >> 2) - 1
                cdw11 = (doper & 0xff) | ((dtype & 0xff) << 8) | ((dspec & 0xff) << 16)
                if show_log:
                    self.show_func_local_param(self.admin_directive_receive)
                return self.device.send_admin_cmds(opcode=0x1a, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=data_len)

    def admin_virtual_media_manage(self, cntlid=0, rt=0, act=0, nr=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                                   wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                                   *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_virtual_media_manage"):
            return self.vendor_commands.admin_virtual_media_manage(cntlid, rt, act, nr, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw14, cdw15, buf_size,
                                                                   wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,io_status_code_type_expected, app_type, show_log,
                                                                   *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("virt-mgmt", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                cdw10 = (act & 0xf) | ((rt & 0x7) << 8) | ((cntlid & 0xffff) << 16)
                cdw11 = nr
                if show_log:
                    self.show_func_local_param(self.admin_virtual_media_manage)
                return self.device.send_admin_cmds(opcode=0x1c, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,cdw12=cdw12,
                                                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                                   io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, buf_size=buf_size)
    def admin_nvme_mi_send(self, buf=None, fuse=0, psdt=0, nsid=1, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                           wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                           **kwargs):
        if hasattr(self.vendor_commands, "admin_nvme_mi_send"):
            return self.vendor_commands.admin_nvme_mi_send(buf, fuse, psdt, nsid, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size, wait_completed,
                                                           rtn_cmds_u_addr, timeout, io_status_code_expected,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            self.admin_passthru(opcode=0x1d, buf=buf, fuse=fuse, psdt=psdt, nsid=nsid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12,
                                cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                *args, **kwargs)

    def admin_nvme_mi_receive(self, buf=None, fuse=0, psdt=0, nsid=1, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                              wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                              **kwargs):
        if hasattr(self.vendor_commands, "admin_nvme_mi_receive"):
            return self.vendor_commands.admin_nvme_mi_receive(buf, fuse, psdt, nsid, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size, wait_completed,
                                                              rtn_cmds_u_addr, timeout, io_status_code_expected,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            self.admin_passthru(opcode=0x1e, buf=buf, fuse=fuse, psdt=psdt, nsid=nsid, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12,
                                cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, app_type=app_type, show_log=show_log,
                                *args, **kwargs)
    def admin_capacity_management(self, elid=0, oper=0, capl=0, capu=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                                  wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                                  *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_capacity_management"):
            return self.vendor_commands.admin_capacity_management(elid, oper, capl, capu, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw13, cdw14, cdw15, buf_size, wait_completed,
                                                                  rtn_cmds_u_addr, timeout, io_status_code_expected,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("capacity-mgmt", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                cdw10 = (oper & 0xf) | ((elid & 0xffff) << 16)
                cdw11 = capl
                cdw12 = capu
                if show_log:
                    self.show_func_local_param(self.admin_capacity_management)
                return self.device.send_admin_cmds(opcode=0x20, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,cdw12=cdw12,
                                                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                                   io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, buf_size=buf_size)
    def admin_discovery_info_management(self, buf=None, tas=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0,
                                        buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                        show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_discovery_info_management"):
            return self.vendor_commands.admin_discovery_info_management(buf, tas, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size,
                                                                        wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,io_status_code_type_expected, app_type,
                                                                        show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("dim", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = tas
                if show_log:
                    self.show_func_local_param(self.admin_discovery_info_management)
                return self.device.send_admin_cmds(opcode=0x21, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_fabric_zone_receive(self, buf=None, zdk=0, zdo=0, zdkc=0, data_len=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw13=0, cdw14=0, cdw15=0,
                                  wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                                  *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_fabric_zone_receive"):
            return self.vendor_commands.admin_fabric_zone_receive(buf, zdk, zdo, zdkc, data_len, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw13, cdw14, cdw15, wait_completed,
                                                                  rtn_cmds_u_addr, timeout, io_status_code_expected,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("fabric-zoning-recv", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = zdk
                cdw11 = zdo
                cdw12 = ((zdkc & 0x1) << 28) | ((data_len >> 2) - 1)
                if show_log:
                    self.show_func_local_param(self.admin_fabric_zone_receive)
                return self.device.send_admin_cmds(opcode=0x22, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=data_len)
    def admin_lockdown(self, ofi=0, ifc=0, prhbt=0, scp=0, uidx=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw15=0, buf_size=0,
                       wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_lockdown"):
            return self.vendor_commands.admin_lockdown(ofi, ifc, prhbt, scp, uidx, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw15, buf_size, wait_completed,
                                                       rtn_cmds_u_addr, timeout, io_status_code_expected,io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("lockdown", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                cdw10 = scp | (prhbt & 0x1) << 4 | (ifc & 0x3) << 5 | (ofi & 0xff) << 8
                cdw14 = uidx
                if show_log:
                    self.show_func_local_param(self.admin_lockdown)
                return self.device.send_admin_cmds(opcode=0x24, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12,
                                                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                                   io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, buf_size=buf_size)

    def admin_fabric_zoning_lookup(self, buf=None, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                                   wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                                   *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_fabric_zoning_lookup"):
            return self.vendor_commands.admin_fabric_zoning_lookup(buf, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size,
                                                                   wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,io_status_code_type_expected, app_type, show_log,
                                                                   buf_size,*args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("fabric-zoning-lookup", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                if show_log:
                    self.show_func_local_param(self.admin_fabric_zoning_lookup)
                return self.device.send_admin_cmds(opcode=0x25, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)
    def admin_clear_exported_nvm_resource_cfg(self, buf=None, ra=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0,
                                              buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                              app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_clear_exported_nvm_resource_cfg"):
            return self.vendor_commands.admin_clear_exported_nvm_resource_cfg(buf, ra, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size,
                                                                              wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,io_status_code_type_expected, app_type,
                                                                              show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("clear-exported-nvm-resource-cfg", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (ra & 0x1) << 8
                if show_log:
                    self.show_func_local_param(self.admin_fabric_zoning_lookup)
                return self.device.send_admin_cmds(opcode=0x26, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)
    def admin_fabric_zoning_send(self, buf=None, zdk=0, zdo=0, lf=0, zdkc=0, data_len=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw13=0, cdw14=0, cdw15=0,
                                 wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                                 **kwargs):
        if hasattr(self.vendor_commands, "admin_fabric_zoning_send"):
                return self.vendor_commands.admin_fabric_zoning_send(buf, zdk, zdo, lf, zdkc, data_len, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw13, cdw14, cdw15,
                                                                     wait_completed, rtn_cmds_u_addr, timeout,io_status_code_expected, io_status_code_type_expected, app_type, show_log,
                                                                     *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("clear-exported-nvm-resource-cfg", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = zdk
                cdw11 = zdo
                cdw12 = (lf << 31) | ((zdkc & 0x1) << 28) | (data_len >> 2 - 1)
                if show_log:
                    self.show_func_local_param(self.admin_fabric_zoning_send)
                return self.device.send_admin_cmds(opcode=0x26, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=data_len)

    def admin_create_exported_nvm_subsystem(self, buf=None, ra=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0,
                                            buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                            app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_create_exported_nvm_subsystem"):
            return self.vendor_commands.admin_create_exported_nvm_subsystem(buf, ra, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size,
                                                                            wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected,io_status_code_type_expected, app_type,
                                                                            show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("create-exported-nvm-subsystem", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (ra & 0x1) << 8
                if show_log:
                    self.show_func_local_param(self.admin_create_exported_nvm_subsystem)
                return self.device.send_admin_cmds(opcode=0x2a, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size,nsid=nsid, wait_completed=wait_completed,
                                                   rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout, io_status_code_expected=io_status_code_expected,
                                                   io_status_code_type_expected=io_status_code_type_expected)

    def admin_manage_exported_nvm_subsystem(self, buf=None, mos=0, sel=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0,
                                            cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                            app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_manage_exported_nvm_subsystem"):
            return self.vendor_commands.admin_manage_exported_nvm_subsystem(buf, mos, sel, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15,
                                                                            buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,
                                                                            app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("create-exported-nvm-subsystem", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (sel & 0xff) | ((mos & 0xff) << 8)
                if show_log:
                    self.show_func_local_param(self.admin_create_exported_nvm_subsystem)
                return self.device.send_admin_cmds(opcode=0x2d, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size, nsid=nsid, wait_completed=wait_completed,
                                                   rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout, io_status_code_expected=io_status_code_expected,
                                                   io_status_code_type_expected=io_status_code_type_expected)
    def admin_manager_exported_namespace(self, buf=None, sel=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0,
                                         buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                         show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_manager_exported_namespace"):
            return self.vendor_commands.admin_manager_exported_namespace(buf, sel, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size,
                                                                         wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type,
                                                                         show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("manager-exported-namespace", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (sel & 0xff)
                if show_log:
                    self.show_func_local_param(self.admin_manager_exported_namespace)
                return self.device.send_admin_cmds(opcode=0x31, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size, nsid=nsid, wait_completed=wait_completed,
                                                   rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout, io_status_code_expected=io_status_code_expected,
                                                   io_status_code_type_expected=io_status_code_type_expected)

    def admin_manager_exported_port(self, buf=None, mos=0, sel=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0,
                                    buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                    show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_manager_exported_port"):
            return self.vendor_commands.admin_manager_exported_port(buf, mos, sel, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size,
                                                                    wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type,
                                                                    show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("manager-exported-port", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (sel & 0xff) | ((mos & 0xff) << 8)
                if show_log:
                    self.show_func_local_param(self.admin_manager_exported_port)
                return self.device.send_admin_cmds(opcode=0x35, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=buf_size, nsid=nsid, wait_completed=wait_completed,
                                                   rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout, io_status_code_expected=io_status_code_expected,
                                                   io_status_code_type_expected=io_status_code_type_expected)

    def admin_send_discovery_log_page(self, buf=None, rlps=0, sct=0, sc=0, tlsp=0, tlid=0, data_len=0, tlpo=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0,
                                      cdw14=0, cdw15=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                                      app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_send_discovery_log_page"):
            return self.vendor_commands.admin_send_discovery_log_page(buf, rlps, sct, sc, tlsp, tlid, data_len, tlpo, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw14, cdw15,
                                                                      wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type,
                                                                      show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("send-discovery-log-page", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (tlid & 0xff) | ((tlsp & 0x7f) << 8) | (sc & 0xff) << 17 | (sct & 0x7) << 25 | (rlps & 0x3) << 30
                cdw11 = (data_len >> 2) - 1
                cdw12 = tlpo & 0xffffffff
                cdw13 = tlpo >> 32
                if show_log:
                    self.show_func_local_param(self.admin_send_discovery_log_page)
                return self.device.send_admin_cmds(opcode=0x39, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=data_len)
    def admin_track_send(self, mos=0, sel=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                         wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                         **kwargs):
        if hasattr(self.vendor_commands, "admin_track_send"):
            return self.vendor_commands.admin_track_send(mos, sel, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size, wait_completed,
                                                         rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("track-send", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                cdw10 = (sel & 0xff) | ((mos & 0xff) << 16)
                if show_log:
                    self.show_func_local_param(self.admin_track_send)
                return self.device.send_admin_cmds(opcode=0x3D, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12,
                                                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                                   io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, buf_size=buf_size)
    def admin_track_receive(self, buf=None, sel=0, data_len=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0,
                            wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                            **kwargs):
        if hasattr(self.vendor_commands, "admin_track_receive"):
            return self.vendor_commands.admin_track_receive(buf, sel, data_len, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw14, cdw15, wait_completed,
                                                            rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("track-rev", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (sel & 0xff)
                cdw11 = (data_len >> 2) - 1
                if show_log:
                    self.show_func_local_param(self.admin_track_receive)
                return self.device.send_admin_cmds(opcode=0x3E, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, buf_size=data_len, nsid=nsid, wait_completed=wait_completed,
                                                   rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout, io_status_code_expected=io_status_code_expected,
                                                   io_status_code_type_expected=io_status_code_type_expected)
    def admin_migration_send(self, mos=0, sel=0, uidx=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw15=0, buf_size=0,
                             wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                             **kwargs):
        if hasattr(self.vendor_commands, "admin_migration_send"):
            return self.vendor_commands.admin_migration_send(mos, sel, uidx, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw15, buf_size, wait_completed,
                                                             rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("migration-send", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                cdw10 = (sel & 0xff) | (mos & 0xffff) << 16
                cdw14 = uidx
                if show_log:
                    self.show_func_local_param(self.admin_migration_send)
                return self.device.send_admin_cmds(opcode=0x41, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12,
                                                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                                   io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, buf_size=buf_size)

    def admin_migration_receive(self, buf=None, mos=0, sel=0, offset=0, uidx=0, data_len=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0,
                                wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                                **kwargs):
        if hasattr(self.vendor_commands, "admin_migration_receive"):
            return self.vendor_commands.admin_migration_receive(buf, mos, sel, offset, uidx, data_len, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, wait_completed,
                                                                rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected,app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("track-send", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (sel & 0xff) | (mos & 0xffff) << 16
                cdw12 = offset & 0xffffffff
                cdw13 = offset >> 32
                cdw14 = uidx
                cdw15 = (data_len >> 2) - 1
                if show_log:
                    self.show_func_local_param(self.admin_migration_send)
                return self.device.send_admin_cmds(opcode=0x42, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=data_len)
    def admin_ctrl_data_queue(self, mos=0, sel=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                              wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                              **kwargs):
        if hasattr(self.vendor_commands, "admin_ctrl_data_queue"):
            return self.vendor_commands.admin_ctrl_data_queue(mos, sel, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size, wait_completed,
                                                              rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("ctrl-data-queue", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                cdw10 = (sel & 0xff) | (mos & 0xffff) << 16
                if show_log:
                    self.show_func_local_param(self.admin_ctrl_data_queue)
                return self.device.send_admin_cmds(opcode=0x45, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12,
                                                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                                   io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected, buf_size=buf_size)
    def admin_doorbell_buffer_cfg(self, buf=None, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                                  wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                                  *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_doorbell_buffer_cfg"):
            return self.vendor_commands.admin_doorbell_buffer_cfg(buf, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size,
                                                                  wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log,
                                                                  *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("doorbell-buffer-cfg", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                if show_log:
                    self.show_func_local_param(self.admin_doorbell_buffer_cfg)
                return self.device.send_admin_cmds(opcode=0x7c, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)
    def admin_fabrics_cmd(self, fuse=0, psdt=0, cid=0, fctype=0, attrib=0, offset=0, value=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, app_type=None, show_log=True,
                          *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_fabrics_cmd"):
                return self.vendor_commands.admin_fabrics_cmd(fuse, psdt, cid, fctype, attrib, offset, value, wait_completed, rtn_cmds_u_addr, timeout, app_type, show_log, *args, **kwargs)
        else:
            if app_type is not None:
                return self.run_nvme_cli_cmd("fabrics_cmd", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                if show_log:
                    self.show_func_local_param(self.admin_doorbell_buffer_cfg)
            # To be implemented opcode = 0x7f

    def admin_format_nvm(self, lbaf=0, see=0, pil=0, pi=0, mset=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0,
                         wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                         **kwargs):
        if hasattr(self.vendor_commands, "admin_format_nvm"):
            return self.vendor_commands.admin_format_nvm(lbaf, see, pil, pi, mset, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw11, cdw12, cdw13, cdw14, cdw15, wait_completed,
                                                         rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("format", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                cdw10 = (lbaf & 0xf) | (mset << 4) | (pi << 5) | (pil << 8) | (see << 9) | (lbaf & 0x3) << 12
                if show_log:
                    self.show_func_local_param(self.admin_format_nvm)
                return self.device.send_admin_cmds(opcode=0x7c, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11, cdw12=cdw12,
                                                   cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr, timeout=timeout,
                                                   io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected)
    def admin_security_send(self, buf=None, secp=0, spsp0=0, spsp1=0, nssf=0, tl=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw14=0,
                            cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                            show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_security_send"):
            return self.vendor_commands.admin_security_send(buf, secp, spsp0, spsp1, nssf, tl, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw14, cdw15, buf_size,
                                                            wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args,
                                                            **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("security-send", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (nssf & 0xff) | ((spsp0 & 0xff) << 8) | ((spsp1 & 0xff) << 16) | ((secp & 0xff) << 24)
                cdw11 = tl
                if show_log:
                    self.show_func_local_param(self.admin_security_send)
                return self.device.send_admin_cmds(opcode=0x81, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)
    def admin_security_receive(self, buf=None, secp=0, spsp0=0, spsp1=0, nssf=0, al=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0, cdw13=0, cdw14=0,
                               cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                               show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_security_receive"):
            return self.vendor_commands.admin_security_receive(buf, secp, spsp0, spsp1, nssf, al, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw14, cdw15, buf_size,
                                                               wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log,
                                                               *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("security-recv", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (nssf & 0xff) | ((spsp0 & 0xff) << 8) | ((spsp1 & 0xff) << 16) | ((secp & 0xff) << 24)
                cdw11 = al
                if show_log:
                    self.show_func_local_param(self.admin_security_receive)
                return self.device.send_admin_cmds(opcode=0x82, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)
    def admin_sanitize(self, buf=None, emvs=0, ndas=0, oipbp=0, owpass=0, ause=0, sanact=0, ovrpat=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw12=0,
                       cdw13=0, cdw14=0, cdw15=0, buf_size=0, wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0,
                       app_type=None, show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_sanitize"):
            return self.vendor_commands.admin_sanitize(buf, emvs, ndas, oipbp, owpass, ause, sanact, ovrpat, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw12, cdw13, cdw14,
                                                       cdw15, buf_size, wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type,
                                                       show_log, *args, **kwargs)
        else:
            nsid = nsid if nsid is not None else self.device.default_nsid
            if app_type is not None:
                return self.run_nvme_cli_cmd("security-recv", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = (sanact & 0x7) | ((ause & 0x1) << 3) | ((owpass & 0xf) << 4) | ((oipbp & 0x1) << 8) | ((ndas & 0x1) << 9) | ((emvs & 0x1) << 10)
                cdw11 = ovrpat
                if show_log:
                    self.show_func_local_param(self.admin_sanitize)
                return self.device.send_admin_cmds(opcode=0x84, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)
    def admin_load_program(self,buf, fuse=0, psdt=0, nsid=1, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                           wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True, *args,
                           **kwargs):
        if hasattr(self.vendor_commands, "admin_load_program"):
            return self.vendor_commands.admin_load_program(buf, fuse, psdt, nsid, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size, wait_completed,
                                                           rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            if app_type is not None:
                return self.run_nvme_cli_cmd("fabrics_cmd", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                # To be implemented opcode = 0x7f
                if show_log:
                    self.show_func_local_param(self.admin_load_program)
                return self.device.send_admin_cmds(opcode=0x7f, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12 =cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)

    def admin_get_lba_status(self, buf=None, slba=0, mndw=0, rl=0, atype=0, nsid=None, fuse=0, psdt=0, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw14=0, cdw15=0, buf_size=0,
                             wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                             *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_get_lba_status"):
            return self.vendor_commands.admin_get_lba_status(buf, slba, mndw, rl, atype, nsid, fuse, psdt, cdw2, cdw3, mptr, prp1, prp2, cdw14, cdw15, buf_size, wait_completed,
                                                             rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type, show_log, *args, **kwargs)
        else:
            if app_type is not None:
                return self.run_nvme_cli_cmd("get-lba-status", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                cdw10 = slba & 0xffffffff
                cdw11 = slba >> 32
                cdw12 = mndw
                cdw13 = rl & 0xffff | ((atype & 0xff) << 16)
                if show_log:
                    self.show_func_local_param(self.admin_get_lba_status)
                return self.device.send_admin_cmds(opcode=0x86, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)
    def admin_program_activation_management(self,buf, fuse=0, psdt=0, nsid=1, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0,  cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                                            wait_completed=1, rtn_cmds_u_addr=False, timeout=None, io_status_code_expected=0, io_status_code_type_expected=0, app_type=None,
                                            show_log=True, *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_program_activation_management"):
            return self.vendor_commands.admin_program_activation_management(buf, fuse, psdt, nsid, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size,
                                                                            wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type,
                                                                            show_log, *args, **kwargs)
        else:
            if app_type is not None:
                return self.run_nvme_cli_cmd("fabrics_cmd", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                # To be implemented opcode = 0x88
                if show_log:
                    self.show_func_local_param(self.admin_program_activation_management)
                return self.device.send_admin_cmds(opcode=0x88, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)
    def admin_memory_range_set_management(self,buf, fuse=0, psdt=0, nsid=1, cdw2=0, cdw3=0, mptr=0, prp1=0, prp2=0, cdw10=0, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buf_size=0,
                                          wait_completed=1, rtn_cmds_u_addr=False, timeout=None,io_status_code_expected=0, io_status_code_type_expected=0, app_type=None, show_log=True,
                                          *args, **kwargs):
        if hasattr(self.vendor_commands, "admin_memory_range_set_management"):
            return self.vendor_commands.admin_memory_range_set_management(buf, fuse, psdt, nsid, cdw2, cdw3, mptr, prp1, prp2, cdw10, cdw11, cdw12, cdw13, cdw14, cdw15, buf_size,
                                                                          wait_completed, rtn_cmds_u_addr, timeout, io_status_code_expected, io_status_code_type_expected, app_type,
                                                                          show_log, *args, **kwargs)
        else:
            if app_type is not None:
                return self.run_nvme_cli_cmd("fabrics_cmd", show_log, *args, **kwargs)
            else:
                timeout = timeout if timeout is not None else self.admin_cmds_timeout
                buf = self.default_buffer if buf is None else buf
                # To be implemented opcode = 0x89
                if show_log:
                    self.show_func_local_param(self.admin_memory_range_set_management)
                return self.device.send_admin_cmds(opcode=0x89, buf=buf, fuse=fuse, psdt=psdt, cdw2=cdw2, cdw3=cdw3, mptr=mptr, prp1=prp1, prp2=prp2, cdw10=cdw10, cdw11=cdw11,
                                                   cdw12=cdw12, cdw13=cdw13, cdw14=cdw14, cdw15=cdw15, nsid=nsid, wait_completed=wait_completed, rtn_cmds_u_addr=rtn_cmds_u_addr,
                                                   timeout=timeout, io_status_code_expected=io_status_code_expected, io_status_code_type_expected=io_status_code_type_expected,
                                                   buf_size=buf_size)
