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

#ifndef XT_SPDK_INTERFACE_H
#define XT_SPDK_INTERFACE_H
#include "spdk/stdinc.h"
#include "spdk/env.h"
#include "spdk/vmd.h"
#include "spdk/rpc.h"
#include "spdk/nvme.h"
#include "spdk/nvme_spec.h"
#include "spdk_internal/log.h"
#include "../../spdk/lib/nvme/nvme_internal.h"
#include "../xt_io_qpair.h"


#define MAX_TRACEKER_ENTRY  1023

typedef struct spdk_nvme_qpair xt_qpair;
typedef struct spdk_nvme_ctrlr xt_ctrlr;
typedef struct spdk_nvme_ns xt_namespace;
typedef struct spdk_pci_device xt_pcie;
typedef struct _xt_histogram_data xt_histogram_data;
typedef struct spdk_pci_addr xt_pci_addr;
typedef struct _xt_buffer xt_buffer;
typedef struct _xt_io_qpair xt_io_qpair;
typedef struct _xt_admin_qpair xt_admin_qpair;
typedef struct spdk_nvme_qpair xt_qpair;
typedef struct spdk_nvme_ns_data xt_ns_data;
typedef struct spdk_nvme_ctrlr_data xt_ctrlr_data;
typedef struct _xt_block_device_info xt_block_device_info;
typedef struct spdk_nvme_registers xt_nvme_registers;


/**
 * Update Namespace flags based on Identify Controller and Identify Namespace.  
 * This can be also used for Namespace Attribute Notice events and Namespace
 * operations such as Attach/Detach.
 */
static void xt_nvme_ns_set_identify_data(xt_admin_qpair * aqinfo, unsigned int nsid)
{
	xt_ns_data	*nsdata;
    xt_ctrlr_data *ctrl_data;
    xt_block_device_info * ns;

    ns = &aqinfo->device_info.block_devices[nsid];
	nsdata = &aqinfo->device_info.block_devices[nsid].ns_data;
    ctrl_data = &aqinfo->device_info.ctrl_data;

	ns->flags = 0x0000;
	ns->sector_size = 1 << nsdata->lbaf[nsdata->flbas.format].lbads;
	ns->extended_lba_size = ns->sector_size;

	ns->md_size = nsdata->lbaf[nsdata->flbas.format].ms;
	if (nsdata->flbas.extended) {
		ns->flags |= SPDK_NVME_NS_EXTENDED_LBA_SUPPORTED;
		ns->extended_lba_size += ns->md_size;
	}
	ns->sectors_per_max_io =  aqinfo->device_info.max_io_xfer_size / ns->extended_lba_size;
	if (nsdata->noiob) {
		ns->sectors_per_stripe = nsdata->noiob;
		SPDK_DEBUGLOG(SPDK_LOG_NVME, "ns %u optimal IO boundary %" PRIu32 " blocks\n", ns->id, ns->sectors_per_stripe);
	} else {
		ns->sectors_per_stripe = 0;
	}

	if (ctrl_data->oncs.dsm) {
		ns->flags |= SPDK_NVME_NS_DEALLOCATE_SUPPORTED;
	}

	if (ctrl_data->oncs.compare) {
		ns->flags |= SPDK_NVME_NS_COMPARE_SUPPORTED;
	}

	if (ctrl_data->vwc.present) {
		ns->flags |= SPDK_NVME_NS_FLUSH_SUPPORTED;
	}

	if (ctrl_data->oncs.write_zeroes) {
		ns->flags |= SPDK_NVME_NS_WRITE_ZEROES_SUPPORTED;
	}

	if (ctrl_data->oncs.write_unc) {
		ns->flags |= SPDK_NVME_NS_WRITE_UNCORRECTABLE_SUPPORTED;
	}

	if (nsdata->nsrescap.raw) {
		ns->flags |= SPDK_NVME_NS_RESERVATION_SUPPORTED;
	}
	ns->pi_type = SPDK_NVME_FMT_NVM_PROTECTION_DISABLE;
	if (nsdata->lbaf[nsdata->flbas.format].ms && nsdata->dps.pit) {
		ns->flags |= SPDK_NVME_NS_DPS_PI_SUPPORTED;
		ns->pi_type = nsdata->dps.pit;
	}
}

static xt_unused int xt_nvme_pcie_prp_list_append(uint64_t *spdk_tracker, void *virt_addr, size_t len, uint32_t page_size)
{
	uintptr_t page_mask = page_size - 1;
	uint64_t phys_addr;
	uint32_t i;

	SPDK_DEBUGLOG(XT_SSD_TEST_LOG, "prp_index:%u virt_addr:%p len:%u\n", *prp_index, virt_addr, (uint32_t)len);

	if (spdk_unlikely(((uintptr_t)virt_addr & 3) != 0)) {
		SPDK_ERRLOG("virt_addr %p not dword aligned\n", virt_addr);
		return -EFAULT;
	}
	while (len) {
		uint32_t seg_len;

		/*
		 * prp_index 0 is stored in prp1, and the rest are stored in the prp[] array,
		 * so prp_index == count is valid.
		 */
		if (spdk_unlikely(i > MAX_TRACEKER_ENTRY)) {
			SPDK_ERRLOG("out of PRP entries\n");
			return -EFAULT;
		}
		phys_addr = spdk_vtophys(virt_addr, NULL);
		if (spdk_unlikely(phys_addr == SPDK_VTOPHYS_ERROR)) {
			SPDK_ERRLOG("vtophys(%p) failed\n", virt_addr);
			return -EFAULT;
		}

		if (i == 0) {
			SPDK_DEBUGLOG(XT_SSD_TEST_LOG, "prp1 = %p\n", (void *)phys_addr);
			seg_len = page_size - ((uintptr_t)virt_addr & page_mask);
		} else {
			if ((phys_addr & page_mask) != 0) {
				SPDK_ERRLOG("PRP %u not page aligned (%p)\n", i, virt_addr);
				return -EFAULT;
			}

			SPDK_DEBUGLOG(XT_SSD_TEST_LOG, "prp[%u] = %p\n", i - 1, (void *)phys_addr);
			spdk_tracker[i - 1] = phys_addr;
			seg_len = page_size;
		}

		seg_len = spdk_min(seg_len, len);
		virt_addr += seg_len;
		len -= seg_len;
		i++;
	}
	return 0;
}


#endif