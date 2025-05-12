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
import importlib

# Determine the correct module based on Python version
if sys.version_info >= (3, 10):
    setup_tools = importlib.import_module('setuptools')
else:
    setup_tools = importlib.import_module('distutils.core')
from Cython.Build import cythonize

# Use the dynamically imported setup and Extension
setup = setup_tools.setup
Extension = setup_tools.Extension
setup(
    ext_modules=cythonize(
        [
            Extension(
                    "xt_random", ["xt_random.pyx"],
                    include_dirs=['spdk/include'],
                    extra_objects=['./spdk/build/lib/libspdk_xssdtest_interface.a',],
                    ),
            Extension(
                    "xt_interface", ["xt_interface.pyx"],
                    # include paths
                    include_dirs = ['spdk/include', 'spdk/isa-l'],
                    # static libraries
                    libraries=['uuid', 'numa', 'pthread', 'aio', 'ssl', 'fuse3'],
                    extra_compile_args=['-O2', '-D_GNU_SOURCE', '-Wall'],
                    extra_objects=[
                        # spdk static libraries
                        '-Wl,--whole-archive',
                        './spdk/build/lib/libspdk_util.a',
                        './spdk/build/lib/libspdk_nvme.a',
                        './spdk/build/lib/libspdk_conf.a',
                        './spdk/build/lib/libspdk_env_dpdk.a',
                        './spdk/build/lib/libspdk_event.a',
                        './spdk/build/lib/libspdk_event_bdev.a',
                        './spdk/build/lib/libspdk_thread.a',
                        './spdk/build/lib/libspdk_bdev.a',
                        './spdk/build/lib/libspdk_vmd.a',
                        './spdk/build/lib/libspdk_event_vmd.a',
                        './spdk/build/lib/libspdk_notify.a',
                        './spdk/build/lib/libspdk_sock.a',
                        './spdk/build/lib/libspdk_rpc.a',
                        './spdk/build/lib/libspdk_log.a',
                        './spdk/build/lib/libspdk_trace.a',
                        './spdk/build/lib/libspdk_xssdtest_interface.a',
                        './spdk/build/lib/libspdk_json.a',
                        './spdk/build/lib/libspdk_jsonrpc.a',
                        './spdk/build/lib/libspdk_sock_posix.a',
                        # dpdk static libraries
                        './spdk/dpdk/build/lib/librte_eal.a',
                        './spdk/dpdk/build/lib/librte_mbuf.a',
                        './spdk/dpdk/build/lib/librte_ring.a',
                        './spdk/dpdk/build/lib/librte_mempool.a',
                        './spdk/dpdk/build/lib/librte_bus_pci.a',
                        './spdk/dpdk/build/lib/librte_pci.a',
                        './spdk/dpdk/build/lib/librte_kvargs.a',
                        '-Wl,--no-whole-archive',
                    ],
                    ),
        ]
    )
)




