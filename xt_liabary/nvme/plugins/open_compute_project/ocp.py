class OCPCommands(object):
    def __init__(self, device):
        self.device = device
        self.logger = self.device.logger