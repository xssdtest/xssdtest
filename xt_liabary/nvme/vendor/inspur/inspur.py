#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from .inspur_struct import *

class VendorCommands(object):
    def __init__(self, device):
        self.device = device
        self.nvme_spec_module = self.device.nvme_spec_module
        self.default_buffer = self.device.buffer.create_buffer(buf_length=self.device.admin_max_data_transfer_size)


    def inspur_get_vendor_log(self, buffer=None, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        vendor_log = inspur_r1_cli_vendor_log()
        self.device.nvme_commands.admin_get_log_page(buffer=buffer, lid=VENDOR_SMART_LOG_PAGE, nsid=1, data_len=4096, lpo=0, lsp=0, lsi=0, rsvd=0,
                                                     csi=0, ot=0, timeout=timeout)
        vendor_log.fields_from_buf(buffer)
        return vendor_log
