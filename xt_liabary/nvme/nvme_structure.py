#! /usr/bin/python3
###############################################################################
 #    BSD LICENSE
 #
 #    Copyright (c) Saul Han <2573789168@qq.com>
 #
 #    Redistribution and use in source and binary forms, with or without
 #    modification, are permitted provided that the following conditions
 #    are met:
 #
 #       Redistributions of source code must retain the above copyright
 #        notice, this list of conditions and the following disclaimer.
 #       Redistributions in binary form must reproduce the above copyright
 #        notice, this list of conditions and the following disclaimer in
 #        the documentation and/or other materials provided with the
 #        distribution.
 #
 #    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 #    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 #    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 #    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 #    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 #    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 #    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 #    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 #    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 #    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 #    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################
import sys
import os
import time
from xt_module.xt_structure import *
class CtrlRegister(object):
    def __init__(self, device, raw_data=None, update=True):
        self.device = device
        self.ctrl_reg_size = 4096
        self._data_struct = self.get_data_struct()
        self.ctrl_reg = self._data_struct()
        self.offset_map = self.ctrl_reg.get_self_fields_offset_map()
        assert len(self.ctrl_reg) == self.ctrl_reg_size, self.device.logger.error('nvme_id_ns size mismatch {} != {}'.format(len(self.ctrl_reg), self.ctrl_reg_size))
        self.update_record_struct(raw_data)
        if update:
            self.update_info()

    def update_record_struct(self, raw_data):
        if raw_data:
            self.ctrl_reg.decode(raw_data)
            if self.ctrl_reg._first_inst is None:
                self.ctrl_reg._first_inst = self._data_struct()
                self.ctrl_reg._first_inst.decode(self.ctrl_reg.encode())
            if self.ctrl_reg._last_inst is None:
                self.ctrl_reg._last_inst = self._data_struct()
            self.ctrl_reg._last_inst.decode(self.ctrl_reg.encode())

    def get_data_struct(self):
        if hasattr(self.device.vendor_module, 'load_nvme_register'):
            _data_struct = self.device.vendor_module.load_nvme_register()
            if _data_struct:
                return _data_struct
        return self.device.nvme_spec_module.NvmeRegister

    def __getattr__(self, name):
        if name != "ctrl_reg" and hasattr(self, 'ctrl_reg') and hasattr(self.ctrl_reg, name):
            length = sizeof(getattr(self.ctrl_reg, name))
            offset = self.offset_map[name] // 8
            return self.device.device_inst.get_nvme_register(offset, length)
        else:
            super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name != "ctrl_reg" and hasattr(self, 'ctrl_reg') and hasattr(self.ctrl_reg, name):
            length = sizeof(getattr(self.ctrl_reg, name))
            offset = self.offset_map[name] // 8
            self.device.device_inst.set_nvme_register(offset, length)
        else:
            super().__setattr__(name, value)
    def update_info(self):
        nvme_register_raws = self.device.device_inst.get_nvme_register_raws()
        self.update_record_struct(nvme_register_raws)


class IdentifyNamespace(object):
    def __init__(self, device, nsid, raw_data=None, update=True):
        self.device = device
        self.nsid = nsid
        self.id_ns_size = 4096
        self.id_ns_buffer = self.device.buffer.create_buffer(self.id_ns_size)
        self._data_struct = self.get_data_struct()
        self.id_ns = self._data_struct()
        assert len(self.id_ns) == self.id_ns_size, self.device.logger.error('nvme_id_ns size mismatch {} != {}'.format(len(self.id_ns), self.id_ns_size))
        self.update_record_struct(raw_data)
        if update:
            self.update_info()
        self._lbaf = self.id_ns.flbas
        self.sector_size = 2 ** self.id_ns.lbaf[self._lbaf].ds
        self.md_size = self.id_ns.lbaf[self._lbaf].ms

    def update_record_struct(self, raw_data):
        if raw_data:
            self.id_ns.decode(raw_data)
            if self.id_ns._first_inst is None:
                self.id_ns._first_inst = self._data_struct()
                self.id_ns._first_inst.decode(self.id_ns.encode())
            if self.id_ns._last_inst is None:
                self.id_ns._last_inst = self._data_struct()
            self.id_ns._last_inst.decode(self.id_ns.encode())

    def get_data_struct(self):
        if hasattr(self.device.vendor_module, 'load_nvme_id_ns'):
            _data_struct = self.device.vendor_module.load_nvme_id_ns()
            if _data_struct:
                return _data_struct
        return self.device.nvme_spec_module.nvme_id_ns

    def __getattr__(self, name):
        if name != "id_ns" and hasattr(self, 'id_ns') and hasattr(self.id_ns, name):
            return getattr(self.id_ns, name)
        else:
            super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name != "id_ns" and hasattr(self, 'id_ns') and hasattr(self.id_ns, name):
            self.id_ns.__setattr__(name, value)
        else:
            super().__setattr__(name, value)

    def update_info(self):
        self.device.nvme_commands.admin_identify_ns(buf=self.id_ns_buffer, nsid=self.nsid, buf_size=self.id_ns_size)
        self.update_record_struct(self.id_ns_buffer.encode(0, self.id_ns_size))

class IdentifyCtrl(object):
    def __init__(self, device, raw_data=None, update=True):
        self.device = device
        self.id_ctrl_size = 4096
        self.id_ctrl_buffer = self.device.buffer.create_buffer(self.id_ctrl_size)
        self._data_struct = self.get_data_struct()
        self.id_ctrl = self._data_struct()
        assert len(self.id_ctrl) == self.id_ctrl_size, self.device.logger.error('nvme_id_ctrl size mismatch {} != {}'.format(len(self.id_ctrl), self.id_ctrl_size))
        self.update_record_struct(raw_data)
        if update:
            self.update_info()

    def get_data_struct(self):
        if hasattr(self.device.vendor_module, 'load_nvme_id_ctrl'):
            _data_struct = self.device.vendor_module.load_nvme_id_ctrl()
            if _data_struct:
                return _data_struct
        return self.device.nvme_spec_module.nvme_id_ctrl

    def update_record_struct(self, raw_data):
        if raw_data:
            self.id_ctrl.decode(raw_data)
            if self.id_ctrl._first_inst is None:
                self.id_ctrl._first_inst = self._data_struct()
                self.id_ctrl._first_inst.decode(self.id_ctrl.encode())
            if self.id_ctrl._last_inst is None:
                self.id_ctrl._last_inst = self._data_struct()
            self.id_ctrl._last_inst.decode(self.id_ctrl.encode())

    def __getattr__(self, name):
        if name != "id_ctrl" and hasattr(self, 'id_ctrl') and hasattr(self.id_ctrl, name):
            return getattr(self.id_ctrl, name)
        else:
            super().__getattribute__(name)

    def update_info(self):
        self.device.nvme_commands.admin_identify_ctrl(buf=self.id_ctrl_buffer, nsid=0, buf_size=self.id_ctrl_size)
        self.update_record_struct(self.id_ctrl_buffer.encode(0, self.id_ctrl_size))


class SmartLog(object):
    def __init__(self, device, nsid=0, raw_data=None, update=True):
        self.device = device
        self.nsid = nsid
        self.smart_log_size = 512
        self.smart_log_buffer = self.device.buffer.create_buffer(self.smart_log_size)
        self._data_struct = self.get_data_struct()
        self.smart_log = self._data_struct()
        # assert len(self.smart_log) == self.smart_log_size, self.device.logger.error('nvme_smart_log size mismatch {} != {}'.format(len(self.smart_log), self.smart_log_size))
        self.update_record_struct(raw_data)
        if update:
            self.update_info()

    def get_data_struct(self):
        if hasattr(self.device.vendor_module, 'load_nvme_smart_log'):
            _data_struct = self.device.vendor_module.load_nvme_smart_log()
            if _data_struct:
                return _data_struct
        return self.device.nvme_spec_module.nvme_smart_log

    def update_record_struct(self, raw_data):
        if raw_data:
            self.smart_log.decode(raw_data)
            if self.smart_log._first_inst is None:
                self.smart_log._first_inst = self._data_struct()
                self.smart_log._first_inst.decode(self.smart_log.encode())
            if self.smart_log._last_inst is None:
                self.smart_log._last_inst = self._data_struct()
            self.smart_log._last_inst.decode(self.smart_log.encode())

    def __getattr__(self, name):
        if name != "smart_log" and hasattr(self, 'smart_log') and hasattr(self.smart_log, name):
            return getattr(self.smart_log, name)
        else:
            super().__getattribute__(name)

    def update_info(self):
        self.device.nvme_commands.admin_get_log_smart(buf=self.smart_log_buffer, nsid=self.nsid, data_len=self.smart_log_size)
        self.update_record_struct(self.smart_log_buffer.encode(0, self.smart_log_size))


class SmartLogAdd(object):
    def __init__(self, device, nsid=0, raw_data=None, update=True):
        self.device = device
        self.nsid = nsid
        self.smart_log_add_size = 512
        self.smart_log_add_buffer = self.device.buffer.create_buffer(self.smart_log_add_size)
        self._data_struct = self.get_data_struct()
        if self._data_struct:
            self.smart_log_add = self._data_struct()
            # assert len(self.smart_log_add) == self.smart_log_add_size, self.device.logger.error('nvme_smart_log_add size mismatch {} != {}'.format(len(self.smart_log_add), self.smart_log_add_size))
            self.update_record_struct(raw_data)
            if update:
                self.update_info()

    def get_data_struct(self):
        if hasattr(self.device.vendor_module, 'load_nvme_smart_log_add'):
            _data_struct = self.device.vendor_module.load_nvme_smart_log_add()
            if _data_struct:
                return _data_struct
        if hasattr(self.device.nvme_spec_module, 'nvme_smart_log_add'):
            return self.device.nvme_spec_module.nvme_smart_log_add

    def update_record_struct(self, raw_data):
        if raw_data:
            self.smart_log_add.decode(raw_data)
            if self.smart_log_add._first_inst is None:
                self.smart_log_add._first_inst = self._data_struct()
                self.smart_log_add._first_inst.decode(self.smart_log_add.encode())
            if self.smart_log_add._last_inst is None:
                self.smart_log_add._last_inst = self._data_struct()
            self.smart_log_add._last_inst.decode(self.smart_log_add.encode())

    def __getattr__(self, name):
        if name != "smart_log_add" and hasattr(self, 'smart_log_add') and hasattr(self.smart_log_add, name):
            return getattr(self.smart_log_add, name)
        else:
            super().__getattribute__(name)

    def update_info(self):
        self.device.nvme_commands.admin_get_log_page(buf=self.smart_log_add_buffer, nsid=self.nsid, lid=0xCA, data_len=self.smart_log_add_size)
        self.update_record_struct(self.smart_log_add_buffer.encode(0, self.smart_log_add_size))

class DeviceSelfTest(object):
    def __init__(self, device):
        self.device = device
        self.dst_log_size = 4096
        self.dst_log_buffer = self.device.buffer.create_buffer(self.dst_log_size)
        self._data_struct = self.get_data_struct()
        self.dst_log = self._data_struct()

    def get_data_struct(self):
        if hasattr(self.device.vendor_module, 'load_nvme_self_test_log'):
            _data_struct = self.device.vendor_module.load_nvme_self_test_log()
            if _data_struct:
                return _data_struct
        return self.device.nvme_spec_module.nvme_self_test_log

    def __getattr__(self, name):
        if name != "dst_log" and hasattr(self, 'dst_log') and hasattr(self.dst_log, name):
            return getattr(self.dst_log, name)
        else:
            super().__getattribute__(name)

    def update_record_struct(self, raw_data):
        if raw_data:
            self.dst_log.decode(raw_data)
            if self.dst_log._first_inst is None:
                self.dst_log._first_inst = self._data_struct()
                self.dst_log._first_inst.decode(self.dst_log.encode())
            if self.dst_log._last_inst is None:
                self.dst_log._last_inst = self._data_struct()
            self.dst_log._last_inst.decode(self.dst_log.encode())

    def update_info(self, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, wait_completed=1):
        self.device.nvme_commands.admin_get_log_device_self_test(buf=self.dst_log_buffer, nsid=0xFFFFFFFF, data_len=self.dst_log_size, rae=rae, lsp=lsp,
                                                                 lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx, wait_completed=wait_completed)
        self.update_record_struct(self.dst_log_buffer.encode(0, self.dst_log_size))


    def short_dst(self, dstp=0, wait_completed=1):
        self.dst_log_buffer.mem_reset()
        self.device.nvme_commands.admin_device_self_test(buf=self.dst_log_buffer, stc=1, nsid=0xFFFFFFFF, data_len=self.dst_log_size, dstp=dstp, wait_completed=wait_completed)

    def extend_dst(self, dstp=0, wait_completed=1):
        self.dst_log_buffer.mem_reset()
        self.device.nvme_commands.admin_device_self_test(buf=self.dst_log_buffer, stc=2, nsid=0xFFFFFFFF, data_len=self.dst_log_size, dstp=dstp, wait_completed=wait_completed)

    def abort_dst(self, dstp=0, wait_completed=1):
        self.dst_log_buffer.mem_reset()
        self.device.nvme_commands.admin_device_self_test(buf=self.dst_log_buffer, stc=0x0f, nsid=0xFFFFFFFF, data_len=self.dst_log_size, dstp=dstp, wait_completed=wait_completed)

class LBAStatus(object):
    def __init__(self, device):
        self.device = device
        self.lba_status_header_size = 16
        self.lba_status_element_head_size = 16
        self.lba_status_element_lba_rd_size = 16
        self.lba_status_size = self.device.admin_max_data_transfer_size
        self.lba_status_buffer = self.device.buffer.create_buffer(self.lba_status_size)
        self._data_struct = self.get_data_struct()
        self.lba_status = self._data_struct()

    def get_data_struct(self):
        if hasattr(self.device.vendor_module, 'load_nvme_lba_status_log'):
            _data_struct = self.device.vendor_module.load_nvme_lba_status_log()
            if _data_struct:
                return _data_struct
        return self.device.nvme_spec_module.nvme_lba_status_log


    def lba_status_log(self, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, wait_completed=1):
        if hasattr(self.device.vendor_commands, "lba_status_log"):
            self.device.vendor_commands.lba_status_log(rae=rae, lsp=lsp, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx)
        else:
            self.device.nvme_commands.admin_get_log_lba_status(buf=self.lba_status_buffer, nsid=0xFFFFFFFF, data_len=self.lba_status_header_size, rae=True, lsp=lsp,
                                                               lsi=lsi, lpo=0, csi=csi, ot=ot, uidx=uidx, wait_completed=wait_completed)
            lslplen = self.lba_status_buffer.get_uint32(offset=0)
            lba_status_raws = bytearray()
            block_count = lslplen // self.lba_status_size
            for offset in range(0, block_count):
                lpo = offset * self.lba_status_size
                self.device.nvme_commands.admin_get_log_lba_status(buf=self.lba_status_buffer, nsid=0xFFFFFFFF, data_len=self.lba_status_size, rae=rae, lsp=lsp,
                                                                    lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx, wait_completed=wait_completed)
                raw_data = self.lba_status_buffer.encode(0, self.lba_status_size)
                lba_status_raws = lba_status_raws + bytearray(raw_data)
            else:
                lpo = block_count * self.lba_status_size
                data_len = lslplen - block_count * self.lba_status_size
                if data_len:
                    self.device.nvme_commands.admin_get_log_lba_status(buf=self.lba_status_buffer, nsid=0xFFFFFFFF, data_len=data_len, rae=rae, lsp=lsp,
                                                                        lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx, wait_completed=wait_completed)
                    raw_data = self.lba_status_buffer.encode(0, data_len)
                    lba_status_raws = lba_status_raws + bytearray(raw_data)
            self.lba_status.decode(lba_status_raws, self.lba_status_header_size)
            offset, num_elements = self.lba_status_header_size, self.lba_status.nlslne
            if num_elements:
                elements_pointer_info = self.lba_status.get_pointer_info_by_field(self.lba_status, 'elements')
                elements = (elements_pointer_info[0].elem_type * num_elements)()
                lba_rds_pointer_info = self.lba_status.get_pointer_info_by_field(elements_pointer_info[0].elem_type(),"lba_rd")
                for ele in range(0, num_elements):
                    ele_inst = elements_pointer_info[0].elem_type
                    elements[ele].decode(lba_status_raws[offset:offset + self.lba_status_element_head_size])
                    offset = offset + self.lba_status_element_head_size
                    num_lba_desc = ele_inst.nlrd
                    lba_rds = (lba_rds_pointer_info[0].elem_type * num_lba_desc)()
                    for lba_rd in range(0, num_lba_desc):
                        lba_rds[lba_rd].decode(lba_status_raws[offset:offset + self.lba_status_element_lba_rd_size])
                        offset += self.lba_status_element_lba_rd_size
                    elements.lba_rd = lba_rds
                self.lba_status.elements = elements

class TelemetryLog(object):
    def __init__(self, device):
        self.device = device
        self.telemetry_log_header_size = 512
        self.single_block_size = 512
        self.telemetry_log_size = self.device.admin_max_data_transfer_size
        self.telemetry_log_header_buffer = self.device.buffer.create_buffer(self.telemetry_log_header_size)
        self.telemetry_log_buffer = self.device.buffer.create_buffer(self.telemetry_log_size)
        self._data_struct = self.get_data_struct()
        self.host_telemetry_log_header = self._data_struct()
        self.controller_telemetry_log_header = self._data_struct()

    def get_data_struct(self):
        if hasattr(self.device.vendor_module, 'load_nvme_telemetry_log'):
            _data_struct = self.device.vendor_module.load_nvme_telemetry_log()
            if _data_struct:
                return _data_struct
        return self.device.nvme_spec_module.nvme_telemetry_log

    def update_host_header_info(self, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, wait_completed=1):
        self.device.nvme_commands.admin_get_log_telemetry_host(buf=self.telemetry_log_header_buffer, nsid=0xFFFFFFFF, rae=rae, lsp=lsp, lsi=lsi, lpo=lpo, csi=csi,
                                                               ot=ot, uidx=uidx, data_len=self.telemetry_log_header_size,wait_completed=wait_completed)
        raw_data = self.telemetry_log_header_buffer.encode(0, self.telemetry_log_header_size)
        self.host_telemetry_log_header.decode(raw_data)
        if self.host_telemetry_log_header._first_inst is None:
            self.host_telemetry_log_header._first_inst = self._data_struct()
            self.host_telemetry_log_header._first_inst.decode(self.host_telemetry_log_header.encode())
        if self.host_telemetry_log_header._last_inst is None:
            self.host_telemetry_log_header._last_inst = self._data_struct()
        self.host_telemetry_log_header._last_inst.decode(self.host_telemetry_log_header.encode())

    def update_controller_header_info(self, rae=0, lsp=0, lsi=0, lpo=0, csi=0, ot=0, uidx=0, wait_completed=1):
        self.device.nvme_commands.admin_get_log_telemetry_ctrl(buf=self.telemetry_log_header_buffer, nsid=0xFFFFFFFF, rae=rae, lsp=lsp, lsi=lsi, lpo=lpo, csi=csi, ot=ot, uidx=uidx,
                                                               data_len=self.telemetry_log_header_size,wait_completed=wait_completed)
        raw_data = self.telemetry_log_header_buffer.encode(0, self.telemetry_log_header_size)
        self.host_telemetry_log_header.decode(raw_data)
        if self.host_telemetry_log_header._first_inst is None:
            self.host_telemetry_log_header._first_inst = self._data_struct()
            self.host_telemetry_log_header._first_inst.decode(self.host_telemetry_log_header.encode())
        if self.host_telemetry_log_header._last_inst is None:
            self.host_telemetry_log_header._last_inst = self._data_struct()
        self.host_telemetry_log_header._last_inst.decode(self.host_telemetry_log_header.encode())


    def telemetry_log(self, dir_path=None, telemetry_type="host", rae=0, lsp=0, lsi=0, csi=0, ot=0, uidx=0, wait_completed=1):
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        else:
            dir_path = os.path.dirname(os.path.abspath(__file__))
        if hasattr(self.device.vendor_commands, "telemetry_log"):
            self.device.vendor_commands.telemetry_log(rae=rae, lsp=lsp, lsi=lsi, csi=csi, ot=ot, uidx=uidx)
        else:
            start_time = time.time()
            _time_str = time.strftime("%Y-%m-%d_%H-%M-%S-%d_", time.localtime()) + '.%s' %((start_time - int(start_time)) * 1000)
            file_name = telemetry_type + '_telemetry_area1' + _time_str + '.bin'
            if "host" in telemetry_type:
                self.update_host_header_info()
            else:
                self.update_controller_header_info()
            block_count = self.telemetry_log_size // self.single_block_size
            header_info = self.host_telemetry_log_header if "host" in telemetry_type else self.controller_telemetry_log_header
            with open(os.path.join(dir_path, file_name), 'wb') as f:
                f.write(header_info.encode())
                dalb1 = header_info.dalb1
                for offset in range(0, dalb1, block_count):
                    lpo = self.telemetry_log_header_size + offset * self.single_block_size
                    if "host" in telemetry_type:
                        self.device.nvme_commands.admin_get_log_telemetry_host(buf=self.telemetry_log_buffer, nsid=0xFFFFFFFF, rae=rae, lsp=lsp, lsi=lsi, lpo=lpo, csi=csi,
                                                                               ot=ot, uidx=uidx, data_len=self.telemetry_log_size, wait_completed=wait_completed)
                    else:
                        self.device.nvme_commands.admin_get_log_telemetry_ctrl(buf=self.telemetry_log_buffer, nsid=0xFFFFFFFF, rae=rae, lsp=lsp, lsi=lsi, lpo=lpo, csi=csi,
                                                                               ot=ot, uidx=uidx, data_len=self.telemetry_log_size, wait_completed=wait_completed)
                    f.write(self.telemetry_log_buffer.encode())
                else:
                    if (dalb1 % block_count):
                        lpo = self.telemetry_log_header_size + (dalb1 - dalb1 % block_count)
                        data_len = (dalb1 % block_count) * self.single_block_size
                        if "host" in telemetry_type:
                            self.device.nvme_commands.admin_get_log_telemetry_host(buf=self.telemetry_log_buffer, nsid=0xFFFFFFFF, rae=rae, lsp=lsp, lsi=lsi, lpo=lpo, csi=csi,
                                                                                   ot=ot, uidx=uidx, data_len=data_len, wait_completed=wait_completed)
                        else:
                            self.device.nvme_commands.admin_get_log_telemetry_ctrl(buf=self.telemetry_log_buffer, nsid=0xFFFFFFFF, rae=rae, lsp=lsp, lsi=lsi, lpo=lpo, csi=csi,
                                                                                   ot=ot, uidx=uidx, data_len=data_len, wait_completed=wait_completed)
                        f.write(self.telemetry_log_buffer.encode(offset=0, length=data_len))
            start_time = time.time()
            _time_str = time.strftime("%Y-%m-%d_%H-%M-%S-%d_", time.localtime()) + '.%s' %((start_time - int(start_time)) * 1000)
            file_name = telemetry_type + '_telemetry_area2' + _time_str + '.bin'
            with open(os.path.join(dir_path, file_name), 'wb') as f:
                f.write(header_info.encode())
                dalb1, dalb2 = header_info.dalb1, header_info.dalb2
                for offset in range(dalb1, dalb2, block_count):
                    lpo = self.telemetry_log_header_size + offset * self.single_block_size
                    if "host" in telemetry_type:
                        self.device.nvme_commands.admin_get_log_telemetry_host(buf=self.telemetry_log_buffer, nsid=0xFFFFFFFF, rae=rae, lsp=lsp, lsi=lsi, lpo=lpo, csi=csi,
                                                                               ot=ot, uidx=uidx, data_len=self.telemetry_log_size, wait_completed=wait_completed)
                    f.write(self.telemetry_log_buffer.encode())
                else:
                    if ((dalb2 - dalb1) % block_count):
                        lpo = self.telemetry_log_header_size + (dalb2 - (dalb2 - dalb1) % block_count)
                        data_len = ((dalb2 - dalb1) % block_count) * self.single_block_size
                        if "host" in telemetry_type:
                            self.device.nvme_commands.admin_get_log_telemetry_host(buf=self.telemetry_log_buffer, nsid=0xFFFFFFFF, rae=rae, lsp=lsp, lsi=lsi, lpo=lpo, csi=csi,
                                                                                   ot=ot, uidx=uidx, data_len=data_len, wait_completed=wait_completed)
                        else:
                            self.device.nvme_commands.admin_get_log_telemetry_ctrl(buf=self.telemetry_log_buffer, nsid=0xFFFFFFFF, rae=rae, lsp=lsp, lsi=lsi, lpo=lpo, csi=csi,
                                                                                   ot=ot, uidx=uidx, data_len=data_len, wait_completed=wait_completed)
                        f.write(self.telemetry_log_buffer.encode(offset=0, length=data_len))
            start_time = time.time()
            _time_str = time.strftime("%Y-%m-%d_%H-%M-%S-%d_", time.localtime()) + '.%s' %((start_time - int(start_time)) * 1000)
            file_name = telemetry_type + '_telemetry_area3' + _time_str + '.bin'
            with open(os.path.join(dir_path, file_name), 'wb') as f:
                f.write(header_info.encode())
                dalb2, dalb3 = header_info.dalb2, header_info.dalb3
                for offset in range(dalb2, dalb3, block_count):
                    lpo = self.telemetry_log_header_size + offset * self.single_block_size
                    if "host" in telemetry_type:
                        self.device.nvme_commands.admin_get_log_telemetry_host(buf=self.telemetry_log_buffer, nsid=0xFFFFFFFF, rae=rae, lsp=lsp, lsi=lsi, lpo=lpo, csi=csi,
                                                                               ot=ot, uidx=uidx, data_len=self.telemetry_log_size, wait_completed=wait_completed)
                    else:
                        self.device.nvme_commands.admin_get_log_telemetry_ctrl(buf=self.telemetry_log_buffer, nsid=0xFFFFFFFF, rae=rae, lsp=lsp, lsi=lsi, lpo=lpo, csi=csi,
                                                                                   ot=ot, uidx=uidx, data_len=self.telemetry_log_size, wait_completed=wait_completed)
                    f.write(self.telemetry_log_buffer.encode())
                else:
                    if ((dalb3 - dalb2) % block_count):
                        lpo = self.telemetry_log_header_size + (dalb3 - (dalb3 - dalb2) % block_count)
                        data_len = ((dalb3 - dalb2) % block_count) * self.single_block_size
                        if "host" in telemetry_type:
                            self.device.nvme_commands.admin_get_log_telemetry_host(buf=self.telemetry_log_buffer, nsid=0xFFFFFFFF, rae=rae, lsp=lsp, lsi=lsi, lpo=lpo, csi=csi,
                                                                                   ot=ot, uidx=uidx, data_len=data_len, wait_completed=wait_completed)
                        else:
                            self.device.nvme_commands.admin_get_log_telemetry_ctrl(buf=self.telemetry_log_buffer, nsid=0xFFFFFFFF, rae=rae, lsp=lsp, lsi=lsi, lpo=lpo, csi=csi,
                                                                                   ot=ot, uidx=uidx, data_len=data_len, wait_completed=wait_completed)
                        f.write(self.telemetry_log_buffer.encode(offset=0, length=data_len))

class PersistentEventLog(object):
    def __init__(self, device, update=True):
        pass

#

class ErrorLog(object):
    def __init__(self, device, raw_data=None, update=True):
        self.device = device
        self.next_index = None
        self.last_index = None
        self.entry_count = self.device.id_ctrl.elpe + 1
        self.error_log_size = self.entry_count * 64
        self.error_log_buffer = self.device.buffer.create_buffer(self.error_log_size)
        self._data_struct = self.get_data_struct()
        self.error_logs = [self._data_struct() for _ in range(self.entry_count)]
        self.update_record_struct(raw_data)
        if update:
            self.update_info()
    def get_data_struct(self):
        if hasattr(self.device.vendor_module, 'load_nvme_error_log_page'):
            _data_struct = self.device.vendor_module.load_nvme_error_log_page()
            if _data_struct:
                return _data_struct
        return self.device.nvme_spec_module.nvme_error_log_page

    def update_record_struct(self, raw_data):
        if raw_data:
            for i in range(self.entry_count):
                self.error_logs[i].decode(raw_data[i * 64:(i + 1) * 64])
                if self.error_logs[i]._first_inst is None:
                    self.error_logs[i]._first_inst = self._data_struct()
                    self.error_logs[i]._first_inst.decode(self.error_logs[i].encode())
                if self.error_logs[i]._last_inst is None:
                    self.error_logs[i]._last_inst = self._data_struct()
                self.error_logs[i]._last_inst.decode(self.error_logs[i].encode())
            self.update_error_log_next_index()
    def update_info(self):
        self.device.nvme_commands.admin_get_log_error_info(buf=self.error_log_buffer, nsid=0xFFFFFFFF, data_len=self.error_log_size)
        self.update_record_struct(self.error_log_buffer.encode(0, self.error_log_size))
        self.update_error_log_next_index()

    def update_error_log_next_index(self):
        if self.next_index is not None:
            self.last_index = self.next_index
        for i in range(self.entry_count):
            if self.next_index is None or self.next_index < self.error_logs[i].error_count:
                self.next_index = self.error_logs[i].error_count
        if self.last_index is None:
            self.last_index = self.next_index

    def get_updated_error_log(self):
        if self.last_index == self.next_index:
            return None
        else:
            assert self.last_index <= self.next_index, self.device.logger.error('last_index {} > next_index {}'.format(self.last_index, self.next_index))
            error_log_list = []
            for i in range(self.last_index, self.next_index):
                error_log_list.append(self.error_logs[(self.next_index - i) % self.entry_count])

class EffectLog(object):
    def __init__(self, device, raw_data=None, update=True):
        self.device = device
        if self.device.nvme_version < 0x00020000:
            self.device.logger.info('Effect log is not supported in NVMe Spec 1.4')
            update = False
        self.effect_log_size = 4096
        self.effect_log_buffer = self.device.buffer.create_buffer(self.effect_log_size)
        self._data_struct = self.get_data_struct()
        self._entry_data_struct = self.device.nvme_spec_module.nvme_cmd_effects_log_entry
        self.effect_log = self._data_struct()
        assert len(self.effect_log) == self.effect_log_size, self.device.logger.error('nvme_cmd_effects_log size mismatch {} != {}'.format(len(self.effect_log), self.effect_log_size))
        self.update_record_struct(raw_data)
        if update:
            self.update_info()
    def get_data_struct(self):
        if hasattr(self.device.vendor_module, 'load_nvme_cmd_effects_log'):
            _data_struct = self.device.vendor_module.load_nvme_cmd_effects_log()
            if _data_struct:
                return _data_struct
        return self.device.nvme_spec_module.nvme_cmd_effects_log

    def update_record_struct(self, raw_data):
        if raw_data:
            self.effect_log.decode(raw_data)
            if self.effect_log._first_inst is None:
                self.effect_log._first_inst = self._data_struct()
                self.effect_log._first_inst.decode(self.effect_log.encode())
            if self.effect_log._last_inst is None:
                self.effect_log._last_inst = self._data_struct()
            self.effect_log._last_inst.decode(self.effect_log.encode())

    def __getattr__(self, name):
        if name != "effect_log" and hasattr(self, 'effect_log') and hasattr(self.effect_log, name):
            return getattr(self.effect_log, name)
        else:
            super().__getattribute__(name)

    def parse_value(self, value):
        _value = value.to_bytes(4, sys.byteorder, signed=False)
        entry = self._entry_data_struct()
        entry.decode(_value)
        return entry

    def show_effect_log(self):
        print("Admin opcode", "\t\t".join([field[0] for field in self._entry_data_struct._fields_]))
        for opcode, value in enumerate(self.effect_log.acs):
            entry = self.parse_value(value)
            print(opcode, "\t\t".join([getattr(entry, field[0]) for field in entry._fields_]))
        print("IO opcode   ", "\t\t".join([field[0] for field in self._entry_data_struct._fields_]))
        for opcode, value in enumerate(self.effect_log.iocs):
            entry = self.parse_value(value)
            print(opcode, "\t\t".join([getattr(entry, field[0]) for field in entry._fields_]))
    def update_info(self):
        self.device.nvme_commands.admin_get_log_error_info(buf=self.effect_log_buffer, nsid=0xFFFFFFFF, data_len=self.effect_log_size)
        self.update_record_struct(self.effect_log_buffer.encode(0, self.effect_log_size))

class NamespaceManager(object):
    def __init__(self, device):
        self.device = device
        self.ns_buffer_size = 4096
        self.ns_buffer = self.device.buffer.create_buffer(self.ns_buffer_size)

    def delete_namespace(self, idnum, ctrlid, nsid=1, wait_completed=1):
        nsid_list = [nsid] if type(nsid) is int else nsid
        for nsid in nsid_list:
            self.ns_buffer.mem_reset()
            self.ns_buffer.set_uint16(offset=0, value=idnum)
            self.ns_buffer.set_uint16(offset=2, value=ctrlid)
            self.device.nvme_commands.admin_namespace_attachment(buf=self.ns_buffer, nsid=nsid, sel=1, wait_completed=wait_completed, buf_size=self.ns_buffer_size)
            self.device.update_max_lba_and_sector_size(nsid=nsid)

    def create_namespace(self, nsze=0, ncap=0,  dps=0, nmic=0, anagrpid=0, nvmsetid=0, flbas=0, nsid=0, csi=0, wait_completed=1):
        self.ns_buffer.mem_reset()
        self.ns_buffer.set_uint32(offset=0, value=nsze & 0xffffffff)
        self.ns_buffer.set_uint32(offset=4, value=(nsze >> 32) & 0xffffffff)
        self.ns_buffer.set_uint32(offset=8, value=ncap & 0xffffffff)
        self.ns_buffer.set_uint32(offset=12, value=ncap & 0xffffffff)
        self.ns_buffer.set_uint8(offset=26, value=flbas)
        self.ns_buffer.set_uint8(offset=29, value=dps)
        self.ns_buffer.set_uint8(offset=30, value=nmic)
        self.ns_buffer.set_uint32(offset=92, value=anagrpid)
        self.ns_buffer.set_uint16(offset=100, value=nvmsetid)
        self.device.nvme_commands.admin_create_namespace(buf=self.ns_buffer, nsid=nsid, csi=csi, sel=0, wait_completed=wait_completed, buf_size=self.ns_buffer_size)

    def attach_namespace(self, idnum, ctrlid, nsid=1, wait_completed=1):
        nsid_list = [nsid] if type(nsid) is int else nsid
        for nsid in nsid_list:
            self.ns_buffer.mem_reset()
            self.ns_buffer.set_uint16(offset=0, value=idnum)
            self.ns_buffer.set_uint16(offset=2, value=ctrlid)
            self.device.nvme_commands.admin_namespace_attachment(buf=self.ns_buffer, nsid=nsid, sel=0, wait_completed=wait_completed, buf_size=self.ns_buffer_size)
            self.device.update_max_lba_and_sector_size(nsid=nsid)

    def detach_namespace(self, idnum, ctrlid, nsid=1, wait_completed=1):
        nsid_list = [nsid] if type(nsid) is int else nsid
        for nsid in nsid_list:
            self.ns_buffer.mem_reset()
            self.ns_buffer.set_uint16(offset=0, value=idnum)
            self.ns_buffer.set_uint16(offset=2, value=ctrlid)
            self.device.nvme_commands.admin_namespace_attachment(buf=self.ns_buffer, nsid=nsid, sel=1, wait_completed=wait_completed, buf_size=self.ns_buffer_size)
            self.device.update_max_lba_and_sector_size(nsid=nsid)

class FirmwareManager(object):
    def __init__(self, device):
        self.device = device
        self.fw_log_size = 512
        self.fw_buffer_size = self.device.admin_max_data_transfer_size
        self.fw_log_buffer = self.device.buffer.create_buffer(self.fw_log_size)
        self._data_struct = self.get_data_struct()
        self.fw_log = self._data_struct()
        assert len(self.fw_log) == self.fw_log_size, self.device.logger.error('nvme_firmware_log size mismatch {} != {}'.format(len(self.fw_log), self.fw_log_size))
    def get_data_struct(self):
        if hasattr(self.device.vendor_module, 'load_nvme_firmware_log'):
            _data_struct = self.device.vendor_module.load_nvme_firmware_log()
            if _data_struct:
                return _data_struct
        return self.device.nvme_spec_module.nvme_firmware_log

    def update_record_struct(self, raw_data):
        if raw_data:
            self.fw_log.decode(raw_data)
            if self.fw_log._first_inst is None:
                self.fw_log._first_inst = self._data_struct()
                self.fw_log._first_inst.decode(self.fw_log.encode())
            if self.fw_log._last_inst is None:
                self.fw_log._last_inst = self._data_struct()
            self.fw_log._last_inst.decode(self.fw_log.encode())

    def __getattr__(self, name):
        if name != "fw_log" and hasattr(self, 'fw_log') and hasattr(self.fw_log, name):
            return getattr(self.fw_log, name)
        else:
            super().__getattribute__(name)

    def fw_download(self, fw_file, offset=0, data_len=None, wait_completed=1):
        assert os.path.exists(fw_file), print("fw_download: {} does not exist".format(fw_file))
        fw_size = os.path.getsize(fw_file)
        assert fw_size & 0x03, print("The fw image must 4 byte align")
        if 'nvme' in self.device.driver:
            fw_buffer = self.device.buffer.create_buffer(fw_size)
            data_len = fw_size if data_len is None else data_len
            self.device.nvme_commands.admin_fw_image_download(buf=fw_buffer, data_len=data_len, offset=offset, nsid=0xFFFFFFFF, wait_completed=wait_completed)
        else:
            (entries, image_remainder) = divmod(fw_size, self.fw_buffer_size)
            fw_buffer = self.device.buffer.create_buffer(self.fw_buffer_size)
            with open(fw_file, 'rb') as f:
                cont = f.read()
                for entry in range(entries):
                    fw_buffer[0:self.fw_buffer_size] = cont[entry * self.fw_buffer_size:(entry + 1) * self.fw_buffer_size]
                    self.device.nvme_commands.admin_fw_image_download(buf=fw_buffer, data_len=self.fw_log_size, offset=entry * self.fw_buffer_size, nsid=0xFFFFFFFF,
                                                                      wait_completed=wait_completed)
                else:
                    if image_remainder:
                        fw_buffer[0:image_remainder] = cont[entries * self.fw_buffer_size:fw_size]
                        self.device.nvme_commands.admin_fw_image_download(buf=fw_buffer, data_len=image_remainder, offset=entries * self.fw_buffer_size, nsid=0xFFFFFFFF,
                                                                          wait_completed=wait_completed)

    def fw_commit(self, bpid=0, ca=0, fs=0, wait_completed=1, update_vu=False):
        self.device.nvme_commands.admin_fw_commit(bpid=bpid, ca=ca, fs=fs, wait_completed=wait_completed)
        if update_vu and wait_completed:
            origin_fw_version = self.device.fw_version
            self.device.id_ctrl.update_info()
            if origin_fw_version != self.device.id_ctrl.id_ctrl.fr:
                self.device.logger.info("Firmware version changed from {} to {}".format(origin_fw_version, self.device.id_ctrl.id_ctrl.fr))
                self.device.fw_version = self.device.id_ctrl.id_ctrl.fr
                self.device.vu_command = self.vendor_commands.load_vendor_unique_command() if self.device.vu_command else None

    def fw_log(self):
        self.device.nvme_commands.admin_get_log_fw_slot(buf=self.fw_log_buffer, nsid=0xFFFFFFFF, buf_size=self.fw_log_size)
        self.update_record_struct(self.fw_log_buffer.encode(0, self.fw_log_size))
