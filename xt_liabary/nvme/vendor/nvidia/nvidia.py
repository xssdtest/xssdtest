#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from .nvidia_struct import *
class VendorCommands(object):
    def __init__(self, device):
        self.device = device
        self.nvme_spec_module = self.device.nvme_spec_module

    def load_nvme_id_ctrl(self):
        nvme_id_psd = self.nvme_spec_module.nvme_id_psd
        filds = self.nvme_spec_module.nvme_id_ctrl._fields_[:-1] + [
            ('json_rpc_2_0_mjr', c_uint16),
            ('json_rpc_2_0_mnr', c_uint16),
            ('json_rpc_2_0_ter', c_uint16),
            ("rsvd8", c_uint8 * 1018),
        ]
        return type("vendor_nvme_id_ctrl", (Structure,), {'_fields_': filds})