#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from .anzn_struct import *

class VendorCommands(object):
    def __init__(self, device):
        self.device = device
        self.nvme_spec_module = self.device.nvme_spec_module
        self.default_buffer = self.device.buffer.create_buffer(buf_length=self.device.admin_max_data_transfer_size)

    def load_nvme_id_ctrl(self):
        nvme_id_psd = self.nvme_spec_module.nvme_id_psd
        filds = self.nvme_spec_module.nvme_id_ctrl._fields_[:-1] + [
            ('bdev', c_char * 32),
            ("rsvd8", c_uint8 * 992),
        ]
        return type("vendor_nvme_id_ctrl", (Structure,), {'_fields_': filds})


    def amzn_get_stats(self, buffer=None, timeout=None):
        buffer = buffer  if buffer else self.default_buffer
        latency_log_page = amzn_latency_log_page()
        length = len(latency_log_page)
        self.device.nvme_commands.admin_get_log_page(buffer=buffer, lid=AMZN_NVME_STATS_LOGPAGE_ID, nsid=1, data_len=length, lpo=0, lsp=0, lsi=0, rsvd=0,
                                                     csi=0, ot=0, timeout=timeout)
        latency_log_page.fields_from_buf(buffer)
        return latency_log_page