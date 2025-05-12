#
#  BSD LICENSE
#
#  Copyright (c) Intel Corporation.
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#    * Neither the name of Intel Corporation nor the names of its
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
ifeq ($(wildcard config-host.mak),)
config-host.mak: configure
	@if [ ! -e "$@" ]; then \
		if [ -e "$<" ]; then \
			echo "Running configure..."; \
			./$<; \
			rm -fr $(OBJS); \
			echo "Reinvoking make..."; \
			exec $(MAKE) -C $(CURDIR) -f $(firstword $(MAKEFILE_LIST)); \
		else \
			echo "Error: configure script '$<' not found"; \
			exit 1; \
		fi; \
	fi
endif

SPDK_ROOT_DIR := $(abspath $(CURDIR)/../spdk)
include $(SPDK_ROOT_DIR)/mk/spdk.common.mk

# Source configuration
SRC_DIRS  := xt_engines xt_crc
BASE_SRCS := xssdtest.c xt_cmds_log.c xt_rand.c xt_memory.c \
             xt_io_qpair.c xt_load_engines.c xt_cmds_u.c

# Collect sources with validation
C_SRCS := $(foreach dir,$(SRC_DIRS),$(wildcard $(dir)/*.c)) $(BASE_SRCS)
$(if $(strip $(C_SRCS)),,$(error No source files found))

OBJS := $(C_SRCS:.c=.o)
LIBNAME := xssdtest_interface

include $(SPDK_ROOT_DIR)/mk/spdk.lib.mk

.PHONY: clean-all
clean-all: clean
	$(RM) config-host.mak
	$(RM) -r $(OBJDIR)  # If using object directory


