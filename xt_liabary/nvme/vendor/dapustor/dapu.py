#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from .dapu_struct import *

class VendorCommands(object):
    def __init__(self, device):
        self.device = device
        self.nvme_spec_module = self.device.nvme_spec_module
        self.default_buffer = self.device.buffer.create_buffer(buf_length=self.device.admin_max_data_transfer_size)


    def dapu_get_additional_smart_log(self, buffer=None, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        additional_smart_log = dapu_nvme_additional_smart_log()
        length = len(additional_smart_log)
        self.device.nvme_commands.admin_get_log_page(buffer=buffer, lid=0xca, data_len=length, nsid=0xffffffff, lpo=0, lsp=0, lsi=0, rsvd=0, csi=0,
                                                     ot=0, timeout=timeout)
        additional_smart_log.fields_from_buf(buffer)
        return additional_smart_log

    def dapu_get_extended_additional_smart_log(self, buffer=None, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        extended_additional_smart_log = dapu_nvme_extended_additional_smart_log()
        length = len(extended_additional_smart_log)
        self.device.nvme_commands.admin_get_log_page(buffer=buffer,lid=0xcb, data_len=length, nsid=0xffffffff, lpo=0, lsp=0, lsi=0, rsvd=0, csi=0,
                                                     ot=0, timeout=timeout)
        extended_additional_smart_log.fields_from_buf(buffer)
        return extended_additional_smart_log