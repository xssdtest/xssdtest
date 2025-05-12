#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from .huawei_struct import *

class VendorCommands(object):
    def __init__(self, device):
        self.device = device
        self.nvme_spec_module = self.device.nvme_spec_module

    def load_nvme_id_ctrl(self):
        nvme_id_psd = self.nvme_spec_module.nvme_id_psd
        filds = self.nvme_spec_module.nvme_id_ctrl._fields_[:-1] + [
            ('array_name', c_int8 * 80),
            ("rsvd8", c_uint8 * 944),
        ]
        return type("vendor_nvme_id_ctrl", (Structure,), {'_fields_': filds})