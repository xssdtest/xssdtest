#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from .innogrit_struct import *
class VendorCommands(object):
    def __init__(self, device):
        self.device = device
        self.nvme_spec_module = self.device.nvme_spec_module
        self.default_buffer = self.device.buffer.create_buffer(buf_length=self.device.admin_max_data_transfer_size)

    def innogrit_get_log(self, buffer=None, lid=0, nsid=0xffffffff, lsp=0, length=4096, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        self.device.nvme_commands.admin_get_log_page(buffer=buffer, lid=lid, nsid=nsid, data_len=length, lpo=0, lsp=lsp, lsi=0, rsvd=0,
                                                     csi=0, ot=0, timeout=timeout)

    def nvme_vucmd(self, opcode, cdw12=0, cdw13=0, cdw14=0, cdw15=0, buffer=None, length=0, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        cdw10 = length // 4
        self.device.nvme_commands.admin_passthru(opcode=opcode, nsid=0xffffffff, cdw2=IGVSC_SIG, cdw10=cdw10, cdw12=cdw12, cdw13=cdw13,
                                                 cdw14=cdw14, cdw15=cdw15, buf=buffer, buf_size=length, timeout=timeout)

    def innogrit_get_eventlog(self, buffer=None, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        self.innogrit_get_log(buffer=buffer, lid=0xcb, nsid=0xffffffff, lsp=0x01, length=4096, timeout=timeout)
        result = self.innogrit_get_log(buffer=buffer, lid=0xcb, nsid=0xffffffff, lsp=0x02, length=4096, timeout=timeout)
        total_size = result * 4096
        for i in range(0, total_size, 4096):
            self.innogrit_get_log(buffer=buffer, lid=0xcb, nsid=0xffffffff, lsp=0x00, length=4096, timeout=timeout)
        ivsctype = self.get_vsc_type(buffer=buffer, timeout=timeout)
        while True:
            if ivsctype == 0:
                self.nvme_vucmd(opcode=NVME_VSC_GET_EVENT_LOG, cdw12=0, cdw13=0x00, cdw14=SRB_SIGNATURE >> 32, cdw15=SRB_SIGNATURE & 0xFFFFFFFF,
                                buffer=buffer, length=4096, timeout=timeout)
            else:
                self.nvme_vucmd(opcode=NVME_VSC_TYPE1_GET, cdw12=0x60, cdw13=0x00, cdw14=0x00, cdw15=0x00, buffer=buffer, length=4096,
                                timeout=timeout)
            # Need to be further supplemented


    def get_vsc_type(self, buffer=None, timeout=None):
        drvinfo_t = innogrit_drvinfo_t()
        self.innogrit_get_log(buffer=buffer, lid=0xe1, nsid=0xffffffff, lsp=0x00, length=4096, timeout=timeout)
        drvinfo_t.fields_from_buf(buffer)
        if drvinfo_t.signature == 0x5A:
            return 1
        self.nvme_vucmd(opcode=0xfe, cdw12=0x82, cdw13=0x03, cdw14=0x00, cdw15=0x00, buffer=buffer, length=4096, timeout=timeout)
        drvinfo_t.fields_from_buf(buffer)
        if drvinfo_t.signature == 0x5A:
            return 1
        return 0

    def innogrit_get_cdump(self, buffer=None, timeout=None):
        buffer = buffer if buffer else self.default_buffer
        cdumpinfo = innogrit_cdumpinfo()
        ivsctype = self.get_vsc_type(buffer=buffer, timeout=timeout)
        if ivsctype == 0:
            self.nvme_vucmd(opcode=NVME_VSC_GET, cdw12=VSC_FN_GET_CDUMP, cdw13=0x00, cdw14=SRB_SIGNATURE >> 32, cdw15=SRB_SIGNATURE & 0xFFFFFFFF,
                            buffer=buffer, length=4096, timeout=timeout)
        else:
            self.nvme_vucmd(opcode=NVME_VSC_TYPE1_GET, cdw12=0x82, cdw13=0x00, cdw14=0x00, cdw15=0x00, buffer=buffer,length=4096, timeout=timeout)
        cdumpinfo.fields_from_buf(buffer)
        ipackindex, ipackcount, itotal, busevsc = 0, 0, 0, False
        if cdumpinfo.signature != 0x5a5b5c5d:
            self.device.nvme_commands.admin_get_log_page(buffer=buffer, lid=0x07, nsid=0xffffffff, data_len=4096, lpo=0, lsp=0, lsi=0, rsvd=0, rae=1,
                                                        csi=0, ot=0, timeout=timeout)
            ipackcount, itotal, busevsc = 1, buffer.get_uint32(), True
            if itotal == 0:
                return 0
        while ipackindex < ipackcount:
            for icur in range(0, itotal, 4096):
                if busevsc:
                    if ivsctype == 0:
                        self.nvme_vucmd(opcode=NVME_VSC_GET, cdw12=VSC_FN_GET_CDUMP, cdw13=0x00, cdw14=SRB_SIGNATURE >> 32, cdw15=SRB_SIGNATURE & 0xFFFFFFFF,
                                        buffer=buffer, length=4096, timeout=timeout)
                    else:
                        self.nvme_vucmd(opcode=NVME_VSC_TYPE1_GET, cdw12=0x82, cdw13=0x00, cdw14=0x00, cdw15=0x00, buffer=buffer,length=4096, timeout=timeout)
                else:
                    self.innogrit_get_log(buffer=buffer, lid=0x07, nsid=0xffffffff, lsp=0x00, length=4096, timeout=timeout)
            ipackindex += 1
            if ipackindex != ipackcount:
                if busevsc:
                    if ivsctype == 0:
                        self.nvme_vucmd(opcode=NVME_VSC_GET, cdw12=VSC_FN_GET_CDUMP, cdw13=0x00, cdw14=SRB_SIGNATURE >> 32, cdw15=SRB_SIGNATURE & 0xFFFFFFFF,
                                        buffer=buffer, length=4096, timeout=timeout)
                    else:
                        self.nvme_vucmd(opcode=NVME_VSC_TYPE1_GET, cdw12=0x82, cdw13=0x00, cdw14=0x00, cdw15=0x00, buffer=buffer,length=4096, timeout=timeout)
                else:
                    self.innogrit_get_log(buffer=buffer, lid=0x07, nsid=0xffffffff, lsp=0x00, length=4096, timeout=timeout)

