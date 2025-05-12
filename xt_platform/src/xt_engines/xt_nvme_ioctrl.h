/*-
 *   BSD LICENSE
 *
 *   Copyright (c) Saul Han <2573789168@qq.com>
 *   All rights reserved.
 *
 *   Redistribution and use in source and binary forms, with or without
 *   modification, are permitted provided that the following conditions
 *   are met:
 *
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in
 *       the documentation and/or other materials provided with the
 *       distribution.
 *
 *   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 *   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 *   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 *   OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 *   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 *   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 *   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 *   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 *   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 *   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
#ifndef XT_IOCTRL_H
#define XT_IOCTRL_H
#include <linux/types.h>
#include <sys/ioctl.h>
#include <stddef.h>
#include "../xssdtest.h"
/**
 * DOC: ioctl.h
 *
 * Linux NVMe ioctl interface functions
 */

/* '0' is interpreted by the kernel to mean 'apply the default timeout' */
#define NVME_DEFAULT_IOCTL_TIMEOUT 0

/*
 * 4k is the smallest possible transfer unit, so restricting to 4k
 * avoids having to check the MDTS value of the controller.
 */
#define NVME_LOG_PAGE_PDU_SIZE 4096

/**
 * struct nvme_passthru_cmd64 - 64-bit nvme passthrough command structure
 * @opcode:	Operation code, see &enum nvme_io_opcodes and &enum nvme_admin_opcodes
 * @flags:	Not supported: intended for command flags (eg: SGL, FUSE)
 * @rsvd1:	Reserved for future use
 * @nsid:	Namespace Identifier, or Fabrics type
 * @cdw2:	Command Dword 2 (no spec defined use)
 * @cdw3:	Command Dword 3 (no spec defined use)
 * @metadata:	User space address to metadata buffer (NULL if not used)
 * @addr:	User space address to data buffer (NULL if not used)
 * @metadata_len: Metadata buffer transfer length
 * @data_len:	Data buffer transfer length
 * @cdw10:	Command Dword 10 (command specific)
 * @cdw11:	Command Dword 11 (command specific)
 * @cdw12:	Command Dword 12 (command specific)
 * @cdw13:	Command Dword 13 (command specific)
 * @cdw14:	Command Dword 14 (command specific)
 * @cdw15:	Command Dword 15 (command specific)
 * @timeout_ms:	If non-zero, overrides system default timeout in milliseconds
 * @rsvd2:	Reserved for future use (and fills an implicit struct pad
 * @result:	Set on completion to the command's CQE DWORD 0-1 controller response
 */
struct nvme_passthru_cmd64 {
	unsigned char        opcode;
	unsigned char        flags;
	unsigned short       rsvd1;
	unsigned int         nsid;
	unsigned int         cdw2;
	unsigned int         cdw3;
	unsigned long long   metadata;
	unsigned long long   addr;
	unsigned int         metadata_len;
	unsigned int         data_len;
	unsigned int         cdw10;
	unsigned int         cdw11;
	unsigned int         cdw12;
	unsigned int         cdw13;
	unsigned int         cdw14;
	unsigned int         cdw15;
	unsigned int         timeout_ms;
	unsigned int         rsvd2;
	unsigned long long   result;
};

/**
 * struct nvme_uring_cmd - nvme uring command structure
 * @opcode:	Operation code, see &enum nvme_io_opcodes and &enum nvme_admin_opcodes
 * @flags:	Not supported: intended for command flags (eg: SGL, FUSE)
 * @rsvd1:	Reserved for future use
 * @nsid:	Namespace Identifier, or Fabrics type
 * @cdw2:	Command Dword 2 (no spec defined use)
 * @cdw3:	Command Dword 3 (no spec defined use)
 * @metadata:	User space address to metadata buffer (NULL if not used)
 * @addr:	User space address to data buffer (NULL if not used)
 * @metadata_len: Metadata buffer transfer length
 * @data_len:	Data buffer transfer length
 * @cdw10:	Command Dword 10 (command specific)
 * @cdw11:	Command Dword 11 (command specific)
 * @cdw12:	Command Dword 12 (command specific)
 * @cdw13:	Command Dword 13 (command specific)
 * @cdw14:	Command Dword 14 (command specific)
 * @cdw15:	Command Dword 15 (command specific)
 * @timeout_ms:	If non-zero, overrides system default timeout in milliseconds
 * @rsvd2:	Reserved for future use (and fills an implicit struct pad
 */
struct nvme_uring_cmd {
	unsigned char	    opcode;
	unsigned char	    flags;
	unsigned short	    rsvd1;
	unsigned int	    nsid;
	unsigned int	    cdw2;
	unsigned int	    cdw3;
	unsigned long long	metadata;
	unsigned long long	addr;
	unsigned int	    metadata_len;
	unsigned int	    data_len;
	unsigned int	    cdw10;
	unsigned int	    cdw11;
	unsigned int	    cdw12;
	unsigned int	    cdw13;
	unsigned int	    cdw14;
	unsigned int	    cdw15;
	unsigned int	    timeout_ms;
	unsigned int        rsvd2;
};

extern cmds_u *io_ctrl_nvme_engines_prepare_admin_unit(xt_admin_qpair *aqinfo);

extern void io_ctrl_nvme_engines_submit_admin_cmd(xt_admin_qpair *aqinfo, xt_buffer *buf, cmds_u *admin_unit, unsigned int length);

extern int io_ctrl_nvme_engines_wait_completion_admin(xt_admin_qpair *aqinfo);

extern bool io_ctrl_nvme_engines_completed_admin_check(cmds_u* _cmds_u);

bool io_ctrl_nvme_engines_completed_io_check(cmds_u* io_u);

#endif