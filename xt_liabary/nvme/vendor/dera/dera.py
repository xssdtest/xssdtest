#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from .dera_struct import *

class VendorCommands(object):
    def __init__(self, device):
        self.device = device
        self.nvme_spec_module = self.device.nvme_spec_module
        self.default_buffer = self.device.buffer.create_buffer(buf_length=self.device.admin_max_data_transfer_size)


    def dera_get_stats(self, buffer=None, timeout=None):
        buffer = buffer  if buffer else self.default_buffer
        smart_info = dera_nvme_smart_info_log()
        length = len(smart_info)
        self.device.nvme_commands.admin_get_log_page(buffer=buffer, lid=0xc0, nsid=0xffffffff, data_len=length, lpo=0, lsp=0, lsi=0, rsvd=0,
                                                     csi=0, ot=0, timeout=timeout)
        smart_info.fields_from_buf(buffer)
        return smart_info

    def dera_get_device_status(self, timeout=None):
        ret = self.device.nvme_commands.admin_passthru(opcode=0xc0, buf=None, cdw12=0x104, buf_size=0, timeout=timeout)
        return ret

