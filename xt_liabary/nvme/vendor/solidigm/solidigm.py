#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from .solidigm_struct import *
class VendorCommands(object):
    def __init__(self, device):
        self.device = device
        self.nvme_spec_module = self.device.nvme_spec_module


    def load_nvme_id_ctrl(self):
        nvme_id_psd = self.nvme_spec_module.nvme_id_psd
        filds = self.nvme_spec_module.nvme_id_ctrl._fields_[:-1] + [
            ('rsvd1', c_uint8 * 3),
            ("ss", c_uint8),
            ("health", c_char * 20),
            ("cls", c_uint8),
            ("nlw", c_uint8),
            ("scap", c_uint8),
            ("sstat", c_uint8),
            ("bl", c_char * 8),
            ("rsvd2", c_uint8 * 38),
            ("ww", c_uint64),
            ("mic_bl", c_char * 4),
            ("mic_fw", c_char * 4),
            ("rsvd3", c_uint8 * 678),
            ("signature", c_uint32),
            ("version", c_uint8),
            ("product_type", c_uint8),
            ("nand_type", c_uint8),
            ("form_factor", c_uint8),
            ("fw_status", c_uint32),
            ("p4_revision", c_uint32),
            ("customer_id", c_uint32),
            ("usage_model", c_uint32),
            ("command_set", c_uint32),
        ]
        return type("vendor_nvme_id_ctrl", (Structure,), {'_fields_': filds})
