#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from .intel_struct import *

class VendorCommands(object):
    def __init__(self, device):
        self.device = device
        self.nvme_spec_module = self.device.nvme_spec_module
        self.default_buffer = self.device.buffer.create_buffer(buf_length=self.device.admin_max_data_transfer_size)

    def load_nvme_id_ctrl(self):
        nvme_id_psd = self.nvme_spec_module.nvme_id_psd
        filds = self.nvme_spec_module.nvme_id_ctrl._fields_[:-1] + [
            ('rsvd8', c_uint8 * 3),
            ("ss", c_uint8),
            ('health', c_char * 20),
            ('cls', c_uint8),
            ('nlw', c_uint8),
            ('scap', c_uint8),
            ('sstat', c_uint8),
            ('bl', c_char * 8),
            ('rsvd9', c_uint8 * 38),
            ('ww', c_char * 8),
            ('mic_bl', c_char * 4),
            ('mic_fw', c_char * 4),
            ('rsvd10', c_uint8 * 934),
        ]
        return type("vendor_nvme_id_ctrl", (Structure,), {'_fields_': filds})


    def intel_get_lat_stats_log(self, buffer=None, write=False, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        lid = 0xC2 if write else 0xC1
        self.device.nvme_commands.admin_get_log_page(buffer=buffer, lid=lid, nsid=0xffffffff, data_len=NAND_LAT_STATS_LEN, lpo=0, lsp=0,
                                                     lsi=0, rsvd=0, csi=0, ot=0, timeout=timeout)

    def intel_set_lat_stats_thresholds(self, buffer=None,  write=False, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        cwd11 = 0x1 if write else 0x0
        self.device.nvme_commands.admin_set_features(buffer=buffer, fid=0xF7, nsid=0, data_len=32, cdw11=cwd11, lpo=0, lsp=0, lsi=0,
                                                     rsvd=0, csi=0, ot=0, timeout=timeout)

    def intel_enable_lat_stats_tracking(self, buffer=None, enable=False, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        cwd11 = 0x1 if enable else 0x0
        self.device.nvme_commands.admin_set_features(buffer=buffer, fid=0xe2, nsid=0, data_len=32, cdw11=cwd11, lpo=0, lsp=0, lsi=0,
                                                     rsvd=0, csi=0, ot=0, timeout=timeout)

    def intel_get_market_log(self, buffer=None, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        self.device.nvme_commands.admin_get_log_page(buffer=buffer, lid=0xdd, nsid=0xffffffff, data_len=512, lpo=0, lsp=0, lsi=0,
                                                     rsvd=0, csi=0, ot=0, timeout=timeout)

    def intel_get_additional_smart_log(self, buffer=None, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        smart_log = intel_nvme_additional_smart_log()
        self.device.nvme_commands.admin_get_log_page(buffer=buffer, lid=0xCA, nsid=0xffffffff, data_len=512, lpo=0, lsp=0, lsi=0,
                                                     rsvd=0, csi=0, ot=0, timeout=timeout)
        smart_log.fields_from_buf(buffer)
        return smart_log

    def intel_get_temp_stats_log(self, buffer=None, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        temp_stats = intel_temp_stats()
        self.device.nvme_commands.admin_get_log_page(buffer=buffer, lid=0xC5, nsid=0xffffffff, data_len=512, lpo=0, lsp=0, lsi=0,
                                                     rsvd=0, csi=0, ot=0, timeout=timeout)
        temp_stats.fields_from_buf(buffer)
        return temp_stats



