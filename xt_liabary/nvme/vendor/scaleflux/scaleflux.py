#! /usr/bin/python3
###############################################################################
# Data From nvme-cli
###############################################################################
from .scaleflux_struct import *
class VendorCommands(object):
    def __init__(self, device):
        self.device = device
        self.nvme_spec_module = self.device.nvme_spec_module

