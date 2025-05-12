#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from .memblaze_struct import *
class VendorCommands(object):
    def __init__(self, device):
        self.device = device
        self.nvme_spec_module = self.device.nvme_spec_module
        self.default_buffer = self.device.buffer.create_buffer(buf_length=self.device.admin_max_data_transfer_size)

    def memblaze_get_additional_smart_log(self, buffer=None, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        smart_log = memblaze_nvme_smart_log()
        self.device.nvme_commands.admin_get_log_page(buffer=buffer, lid=0xCA, nsid=0xffffffff, data_len=512, lpo=0, lsp=0, lsi=0,
                                                     rsvd=0, csi=0, ot=0, timeout=timeout)
        smart_log.fields_from_buf(buffer)
        return smart_log

    def memblaze_get_powermanager_status(self, timeout=None):
        result = self.device.nvme_commands.admin_get_features(fid=0x02, nsid=0xffffffff, timeout=timeout)
        return result

    def memblaze_set_powermanager_status(self, value=0x00, save=0x00, timeout=None):
        self.device.nvme_commands.admin_set_features(fid=0x02, nsid=0xffffffff, timeout=timeout, cdw11=value, sv=save)

    def memblaze_set_lat_stats(self, buffer=None, enable=0x00, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        cwd11 = 0x1 if enable else 0x0
        self.device.nvme_commands.admin_set_features(buffer=buffer, fid=0xe2, nsid=0, data_len=32, cdw11=cwd11, lpo=0, lsp=0, lsi=0,
                                                     rsvd=0, csi=0, ot=0, timeout=timeout)

    def memblaze_lat_stats_log(self, buffer=None, write=False, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        lid = 0xC2 if write else 0xC1
        self.device.nvme_commands.admin_get_log_page(buffer=buffer, lid=lid, nsid=0xffffffff, data_len=512, lpo=0, lsp=0,
                                                     lsi=0, rsvd=0, csi=0, ot=0, timeout=timeout)

    def memblaze_set_high_latency_log(self, value=0x00, save=0, timeout=None):
        self.device.nvme_commands.admin_set_features(fid=0xE1, nsid=0xffffffff, timeout=timeout, cdw11=value, sv=save)

    def memblaze_high_latency_log(self, buffer=None, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        deadbeef = "deadbeef".encode("utf-8")
        while True:
            self.device.nvme_commands.admin_get_log_page(buffer=buffer, lid=0xC3, nsid=0xffffffff, data_len=0x1000, lpo=0, lsp=0,
                                                          lsi=0, rsvd=0, csi=0, ot=0, timeout=timeout)
            log_bytes = buffer.encode(offset=0, length=0x1000)
            for i in range(0, 0x1000, 4):
                if log_bytes[i:i+4] == deadbeef:
                    return

    def memblaze_clear_error_log(self, timeout=None):
        self.device.nvme_commands.admin_set_features(fid=0xf7, nsid=0, data_len=32, cdw11=0x534d0001, lpo=0, lsp=0, lsi=0, rsvd=0,
                                                     csi=0, ot=0, timeout=timeout)

    def memblaze_set_latency_feature(self, read_threshold=0, write_threshold=0, de_allocate_trim_threshold=0, cmd_mask=0, perf_monitor=0,
                               timeout=None):
        cdw11 = perf_monitor
        cdw12 = cmd_mask
        cdw13 = (read_threshold & 0xff) | ((write_threshold & 0xff) << 8) | ((de_allocate_trim_threshold & 0xff) << 16)
        self.device.nvme_commands.admin_set_features(fid=0xd0, nsid=0, data_len=0, cdw11=cdw11, cdw12=cdw12, cdw13=cdw13, lpo=0, lsp=0,
                                                     lsi=0, rsvd=0, csi=0, ot=0, timeout=timeout)

    def memblaze_get_latency_feature(self, timeout=None):
        ret = self.device.nvme_commands.admin_set_features(fid=0xd0, nsid=0, data_len=0, lpo=0, lsp=0, lsi=0, rsvd=0, csi=0,
                                                           ot=0, timeout=timeout)
        return ret




