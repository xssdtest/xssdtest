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
pathList = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)
parPath = os.path.sep.join([item for item in pathList[:-2]])
sys.path.append(parPath)
sys.path.append(os.path.sep.join((parPath, 'xt_platform')))
from xt_platform import xt_interface as xt
if __name__ == '__main__':
    logger = xt.Logger()
    # ['io_uring_nvme_tbd', 'libaio_nvme', 'null', 'ioctrl_nvme', 'sata_tbd', 'sde_xx_tbd', 'simulator_nvme', 'spdk_nvme', 'sync_nvme']
    engine_names = xt.get_engine_names_list()
    for src_engine in engine_names:
        for dest_engine in engine_names:
            xt.verify_reload_engine_check(src_engine, dest_engine)
    # xt.verify_reload_engine_check("io_uring_nvme_tbd", "sata_tbd")
    # io_uring_nvme_tbd -> io_uring_nvme_tbd check 1
    # io_uring_nvme_tbd -> libaio_nvme check 1
    # io_uring_nvme_tbd -> null check 1
    # io_uring_nvme_tbd -> ioctrl_nvme check 1
    # io_uring_nvme_tbd -> sata_tbd check 0
    # io_uring_nvme_tbd -> sde_xx_tbd check 0
    # io_uring_nvme_tbd -> simulator_nvme check 0
    # io_uring_nvme_tbd -> spdk_nvme check 1
    # io_uring_nvme_tbd -> sync_nvme check 1
    # libaio_nvme -> io_uring_nvme_tbd check 1
    # libaio_nvme -> libaio_nvme check 1
    # libaio_nvme -> null check 1
    # libaio_nvme -> ioctrl_nvme check 1
    # libaio_nvme -> sata_tbd check 0
    # libaio_nvme -> sde_xx_tbd check 0
    # libaio_nvme -> simulator_nvme check 0
    # libaio_nvme -> spdk_nvme check 1
    # libaio_nvme -> sync_nvme check 1
    # null -> io_uring_nvme_tbd check 0
    # null -> libaio_nvme check 0
    # null -> null check 1
    # null -> ioctrl_nvme check 0
    # null -> sata_tbd check 0
    # null -> sde_xx_tbd check 0
    # null -> simulator_nvme check 0
    # null -> spdk_nvme check 0
    # null -> sync_nvme check 0
    # ioctrl_nvme -> io_uring_nvme_tbd check 1
    # ioctrl_nvme -> libaio_nvme check 1
    # ioctrl_nvme -> null check 1
    # ioctrl_nvme -> ioctrl_nvme check 1
    # ioctrl_nvme -> sata_tbd check 0
    # ioctrl_nvme -> sde_xx_tbd check 0
    # ioctrl_nvme -> simulator_nvme check 0
    # ioctrl_nvme -> spdk_nvme check 1
    # ioctrl_nvme -> sync_nvme check 1
    # sata_tbd -> io_uring_nvme_tbd check 0
    # sata_tbd -> libaio_nvme check 0
    # sata_tbd -> null check 1
    # sata_tbd -> ioctrl_nvme check 0
    # sata_tbd -> sata_tbd check 1
    # sata_tbd -> sde_xx_tbd check 0
    # sata_tbd -> simulator_nvme check 0
    # sata_tbd -> spdk_nvme check 0
    # sata_tbd -> sync_nvme check 0
    # sde_xx_tbd -> io_uring_nvme_tbd check 0
    # sde_xx_tbd -> libaio_nvme check 0
    # sde_xx_tbd -> null check 1
    # sde_xx_tbd -> ioctrl_nvme check 0
    # sde_xx_tbd -> sata_tbd check 0
    # sde_xx_tbd -> sde_xx_tbd check 1
    # sde_xx_tbd -> simulator_nvme check 0
    # sde_xx_tbd -> spdk_nvme check 0
    # sde_xx_tbd -> sync_nvme check 0
    # simulator_nvme -> io_uring_nvme_tbd check 0
    # simulator_nvme -> libaio_nvme check 0
    # simulator_nvme -> null check 1
    # simulator_nvme -> ioctrl_nvme check 0
    # simulator_nvme -> sata_tbd check 0
    # simulator_nvme -> sde_xx_tbd check 0
    # simulator_nvme -> simulator_nvme check 1
    # simulator_nvme -> spdk_nvme check 0
    # simulator_nvme -> sync_nvme check 0
    # spdk_nvme -> io_uring_nvme_tbd check 1
    # spdk_nvme -> libaio_nvme check 1
    # spdk_nvme -> null check 1
    # spdk_nvme -> ioctrl_nvme check 1
    # spdk_nvme -> sata_tbd check 0
    # spdk_nvme -> sde_xx_tbd check 0
    # spdk_nvme -> simulator_nvme check 0
    # spdk_nvme -> spdk_nvme check 1
    # spdk_nvme -> sync_nvme check 1
    # sync_nvme -> io_uring_nvme_tbd check 1
    # sync_nvme -> libaio_nvme check 1
    # sync_nvme -> null check 1
    # sync_nvme -> ioctrl_nvme check 1
    # sync_nvme -> sata_tbd check 0
    # sync_nvme -> sde_xx_tbd check 0
    # sync_nvme -> simulator_nvme check 0
    # sync_nvme -> spdk_nvme check 1
    # sync_nvme -> sync_nvme check 1
    # driver = xt.XT_DRIVER("0000:01:00.0", "libaio_nvme", logger=logger, pci_whitelist=["0000:01:00.0"])
    # 2024-10-09 23:30:51,316 INFO Load libaio_nvme engines done 0x77ad139e1d60
    # driver = xt.XT_DRIVER("0000:01:00.0", "null", logger=logger, pci_whitelist=["0000:01:00.0"])
    # 2024-10-09 23:31:57,181 INFO Load null engines done 0x7b5fae9e1e40
    # driver = xt.XT_DRIVER("0000:01:00.0", "ioctrl_nvme", logger=logger, pci_whitelist=["0000:01:00.0"])
    # 2024-10-09 23:32:15,219 INFO Load ioctrl_nvme engines done 0x74a1191e1f20
    # driver = xt.XT_DRIVER("0000:01:00.0", "spdk_nvme", logger=logger, pci_whitelist=["0000:01:00.0"])
    # 2024-10-09 23:32:37,857 INFO Load spdk_nvme engines done 0x784e3dfe2240
    # driver = xt.XT_DRIVER("0000:01:00.0", "sync_nvme", logger=logger, pci_whitelist=["0000:01:00.0"])
    # 2024-10-09 23:33:12,320 INFO Load sync_nvme engines done 0x7fee09de2340
    # driver.dump_pcie_header()