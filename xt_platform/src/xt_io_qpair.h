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
#ifndef XT_IO_QPAIR_H
#define XT_IO_QPAIR_H

#include <libaio.h>
#include "spdk/stdinc.h"
#include "xt_compiler/xt_compiler.h"
#include "xt_include/xt_histogram.h"
#include "spdk/env.h"
#include "spdk/vmd.h"
#include "spdk/rpc.h"
#include "spdk/nvme.h"
#include "spdk/nvme_spec.h"
#include "spdk_internal/log.h"
#include "xt_load_engines.h"
#include "xt_rand.h"

#define XT_DEVICE_NAME_SIZE	            64
#define XT_DEVICE_MAX_OPEN_COUNT	    512


typedef struct spdk_nvme_qpair xt_qpair;
typedef struct spdk_nvme_ctrlr xt_ctrlr;
typedef struct spdk_nvme_ns xt_namespace;
typedef struct spdk_pci_device xt_pcie;
typedef struct _xt_histogram_data xt_histogram_data;
typedef struct spdk_pci_addr xt_pci_addr;
typedef struct _cmds_u cmds_u;
typedef struct _cmds_u_ring cmds_u_ring;
typedef struct _xt_buffer xt_buffer;
typedef struct _xt_io_qpair xt_io_qpair;
typedef struct _xt_admin_qpair xt_admin_qpair;
typedef struct _xt_engines xt_engines;
typedef struct spdk_nvme_qpair xt_qpair;
typedef struct spdk_nvme_ns_data xt_ns_data;
typedef struct spdk_nvme_ctrlr_data xt_ctrlr_data;
typedef struct _xt_engines xt_engines;

typedef struct _xt_block_device_info{
    char block_device_name[XT_DEVICE_NAME_SIZE];
    unsigned int nsid;
    unsigned int next_open_index;
    int device_fids[XT_DEVICE_MAX_OPEN_COUNT];
	unsigned int sector_size;
	/*
	 * Size of data transferred as part of each block,
	 * including metadata if FLBAS indicates the metadata is transferred
	 * as part of the data buffer at the end of each LBA.
	 */
	unsigned int extended_lba_size;
	unsigned int md_size;
	unsigned int pi_type;
	unsigned int sectors_per_max_io;
	unsigned int sectors_per_stripe;
	unsigned short flags;
	/* Namespace Identification Descriptor List (CNS = 03h) */
    union{
       unsigned char id_desc_list[4096];
       xt_ns_data ns_data;
    };
    
}xt_block_device_info;


typedef struct _xt_char_device_info{
    char char_device_name[XT_DEVICE_NAME_SIZE];
    int admin_handle_id;
    unsigned int nsid_count;
    xt_block_device_info* block_devices;
    xt_ctrlr_data ctrl_data;
    unsigned int max_io_xfer_size;
    unsigned int max_metadata_size;
}xt_char_device_info;

typedef struct _xt_admin_qpair{
    cmds_u * admin_units;
    cmds_u_ring * completed_cmds_u_ring;  // completed cmd_u ring
    cmds_u_ring * submit_cmds_u_ring;     // recover submit io info
    xt_engine_ops   *engine_ops;
    // unsigned int    engine_type;
    int             pid;
    unsigned long long sys_tick_hz;
    unsigned long long timeout;
    unsigned int qpair_iodepth;

    /*xt  opt for nvme */
    xt_pci_addr *   pci_whitelist;
    unsigned int    spdk_mem_size;
    //	int			    shm_id;
	// unsigned char	no_pci;
	// unsigned char	hugepage_single_segments;
	// unsigned char	unlink_hugepage;
	// unsigned char	num_pci_addr;
	// const char		*hugedir;
	// int			    mem_channel;
	// int			    master_core;

    /*for pcie ssd*/
    xt_ctrlr *ctrlr;
    xt_pcie *pcie_info;
    char traddr[XT_DEVICE_NAME_SIZE];
    volatile void * nvme_regs;
    unsigned int    bir;
    volatile void * bar_address;
    unsigned long long   bar_size;
    unsigned long long   bar_phys_addr;
    unsigned int io_unit_clear_size;
    
    /* histogram  recover */
    unsigned int histogram_flag;
    xt_histogram_data	*read_histogram;
    xt_histogram_data	*write_histogram;
    struct timespec spec_timeout;
    xt_char_device_info device_info;
    xt_engines *engine_names;


}xt_admin_qpair;

typedef struct _xt_io_qpair{
    xt_qpair *qpair;
    xt_admin_qpair * aqinfo;
    unsigned int qpair_id;
    int reap_type;
    /* type 0 async submit ensure that the queue is as full as possible */
    /* type 1 submit iodepth x once, wait x command return */
    /* type 2 limit iops*/
    /* type 3 limit bw*/
    /* type 4 add delay time(us) in type 1*/
    unsigned int io_check_type;
    /*  0 not check;  bit 1 check status code and status code type; */
    /*  bit 2 read command check data include empty buffer  */
    /*  bit 3 read command check data with excepted write buffer  */
    /*  bit 4 read command check data with buffer tailer  */
    /*  bit 5 read command only check buffer tailer (quickly performance check)*/
    /*  other bits resevered*/
    volatile unsigned int current_iodepth_count;
    unsigned int qpair_iodepth;
    unsigned int qpair_is_pow2;
    volatile unsigned long long timeout;
    volatile unsigned long long last_tick_recover;
    volatile unsigned long long completed_check_index;
    volatile unsigned long long qpair_completions;
    volatile unsigned long long submit_count;
    volatile unsigned long long last_submit_count;
    volatile unsigned long long limit_iops_count;
    volatile unsigned long long last_second_iops_count;
    volatile unsigned long long limit_io_count;
    volatile unsigned long long last_second_total_io_count;
    volatile unsigned long long last_second_total_tick;
    volatile unsigned int microseconds_delay;
    cmds_u * io_units;
    cmds_u_ring * completed_cmds_u_ring;  // completed cmd_u ring
    cmds_u_ring * submit_cmds_u_ring;     // recover submit io info
    unsigned long long io_u_submit_map[8];
    unsigned long long io_u_complete_map[8];

    
    xt_buffer ** write_buf_addr_list;
    xt_lcg_random *io_lcg;
    xt_lcg_random *write_lcg;
    xt_lcg_random *read_lcg;

    /*for open block devices */
    int fid;
    unsigned int nsid;
    struct timespec spec_timeout;
    io_context_t aio_ctx;
	struct io_event *aio_events;
    struct iocb *iocbs;
    void (* wait_submit_command_function) (void *);
    void * wait_submit_command_args;
}xt_io_qpair;

extern void xt_io_qpair_init(xt_io_qpair *qinfo, unsigned int qpair_iodepth, cmds_u * io_units, cmds_u_ring * completed_cmds_u_ring, 
                             unsigned long long completed_check_index, unsigned long long submit_count, unsigned long long qpair_completions);

extern void xt_set_io_qpair_polling_status(xt_io_qpair *qinfo, xt_admin_qpair * aqinfo, int reap_type, unsigned int io_check_type, 
                                           unsigned int current_iodepth_count, unsigned long long timeout, unsigned long long limit_iops_count, 
                                           unsigned long long limit_io_count, unsigned int microseconds_delay);

extern void xt_io_qpair_lcg_init(xt_io_qpair *qinfo, unsigned int x0, unsigned long long m_modulus, unsigned long long c_increment, 
                                 unsigned long long a_multiplier, unsigned long long offset, unsigned long long max_value,
                                unsigned int step, unsigned int lcg_type);

extern void xt_io_qpair_lcg_fini(xt_io_qpair *qinfo);

extern void xt_char_device_info_init(xt_admin_qpair * aqinfo, const char * char_device_name, unsigned int size, unsigned int nsid_count);

extern void xt_char_device_update_info(xt_admin_qpair * aqinfo, const char * char_device_name, unsigned int size);

extern void xt_update_ctrl_data(xt_admin_qpair * aqinfo, void * ctrl_data);

extern unsigned int xt_get_mdts(xt_admin_qpair * aqinfo);

extern void xt_update_ns_data(xt_admin_qpair * aqinfo, void * ns_data, unsigned int nsid);

extern unsigned int xt_get_ns_sector_size(xt_admin_qpair * aqinfo, unsigned int nsid);

extern unsigned int xt_get_ns_meta_data_size(xt_admin_qpair * aqinfo, unsigned int nsid);

extern void xt_block_device_update_info(xt_admin_qpair * aqinfo, const char * block_device_name, unsigned int size, unsigned int nsid, unsigned int clear_next_open_index);

extern int xt_device_open(xt_admin_qpair * aqinfo, const char* path, unsigned int nsid);

extern void xt_device_close(xt_admin_qpair * aqinfo);

extern void xt_char_device_info_fini(xt_admin_qpair * aqinfo);

extern void xt_io_qpair_reset(xt_io_qpair *qinfo, unsigned long long qpair_completions, unsigned long long submit_count,
                              unsigned long long completed_check_index);

extern void xt_io_qpair_timeout(xt_io_qpair *qinfo, unsigned long long timeout);

extern int xt_check_qpair_completioned(xt_io_qpair *qinfo);

extern unsigned long long xt_io_qpair_get_qpair_completions(xt_io_qpair *qinfo);

extern void xt_io_qpair_reset_qpair_completions(xt_io_qpair *qinfo);

extern void xt_io_qpair_init_write_buffer_addr_list(xt_io_qpair *qinfo, xt_buffer ** write_buf_addr_list);

extern unsigned int xt_get_io_qpair_id(xt_io_qpair *qinfo);

extern cmds_u_ring * xt_io_qpair_get_completed_cmds_u_ring(xt_io_qpair *qinfo);

#endif