#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from .netapp_struct import *
class VendorCommands(object):
    def __init__(self, device):
        self.device = device
        self.nvme_spec_module = self.device.nvme_spec_module


    def load_netapp_smdevice_info(self):
        nvme_id_ctrl = self.nvme_spec_module.nvme_id_ctrl
        nvme_id_ns = self.nvme_spec_module.nvme_id_ns
        fields = [
            ('nsid', c_uint32),
            ('ctrl', nvme_id_ctrl),
            ('ns', nvme_id_ns),
            ('dev', c_char * ONTAP_NS_PATHLEN),
        ]
        return type("netapp_smdevice_info", (StructureBase,), {"_fields_":fields})

    def load_netapp_device_info(self):
        nvme_id_ctrl = self.nvme_spec_module.nvme_id_ctrl
        nvme_id_ns = self.nvme_spec_module.nvme_id_ns
        fields = [
            ('nsid', c_uint32),
            ('ctrl', nvme_id_ctrl),
            ('ns', nvme_id_ns),
            ('uuid', c_char * 16),
            ('log_data', c_char * ONTAP_C2_LOG_SIZE),
            ('dev', c_char * 265),
        ]
        return type("netapp_device_info", (StructureBase,), {"_fields_":fields})