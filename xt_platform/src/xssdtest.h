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
#ifndef XSSDTEST_H
#define XSSDTEST_H
#include <sys/ipc.h>
#include <sys/shm.h>
#include <fcntl.h>
#include <math.h>
#include "spdk/stdinc.h"
#include "spdk/env.h"
#include "spdk/vmd.h"
#include "spdk/rpc.h"
#include "spdk/nvme.h"
#include "spdk/nvme_spec.h"
#include "spdk_internal/log.h"

#include "xt_compiler/xt_compiler.h"
#include "xt_include/xt_histogram.h"
#include "xt_cmds_u.h"
#include "xt_io_qpair.h"
#include "xt_memory.h"
#include "xt_rand.h"
#include "xt_cmds_log.h"
#include "xt_load_engines.h"


#define XT_IOOPS_VERSION	    1
#define XT_MAGIC_NUMBER			0x7873736474657374
#define XT_SHARE_MEMORY_SIZE	8388608
#define XT_MB_BYTES	            1048576
#define XT_GB_BYTES             1073741824
#define XT_CMD_LOG_ENTRY_SIZE	128
#define XT_ADMIN_DEPTH	        1024
#define XT_PCIE_FUNC_COUNT	    7
#define XT_PCIE_NAME_SIZE	    64
#define XT_CONTAINEROF(ptr, type, member) ((type *)((uintptr_t)ptr - offsetof(type, member)))

#define NVME_IOCTL_ID		_IO('N', 0x40)
#define NVME_IOCTL_RESET	_IO('N', 0x44)
#define NVME_IOCTL_SUBSYS_RESET	_IO('N', 0x45)
#define NVME_IOCTL_RESCAN	_IO('N', 0x46)
#define NVME_IOCTL_ADMIN64_CMD  _IOWR('N', 0x47, struct nvme_passthru_cmd64)
#define NVME_IOCTL_IO64_CMD     _IOWR('N', 0x48, struct nvme_passthru_cmd64)

/* io_uring async commands: */
#define NVME_URING_CMD_IO	_IOWR('N', 0x80, struct nvme_uring_cmd)
#define NVME_URING_CMD_IO_VEC	_IOWR('N', 0x81, struct nvme_uring_cmd)

typedef struct spdk_nvme_qpair xt_qpair;
typedef struct spdk_nvme_ctrlr xt_ctrlr;
typedef struct spdk_nvme_cmd xt_cmd;
typedef struct spdk_nvme_ns xt_namespace;
typedef struct spdk_pci_device xt_pcie;
typedef struct timespec xt_timespec;
typedef struct _xt_histogram_data xt_histogram_data;
typedef struct spdk_pci_addr xt_pci_addr;
typedef struct _cmds_u cmds_u;
typedef struct _cmds_u_ring cmds_u_ring;
typedef struct _xt_engine_ops xt_engine_ops;
typedef struct _xt_buffer xt_buffer;
typedef struct _xt_io_qpair xt_io_qpair;
typedef struct _xt_commands_logger xt_commands_logger;
typedef struct _xt_char_device_info xt_char_device_info;
typedef struct _xt_engines xt_engines;

extern xt_commands_logger* g_xt_cmd_log;
extern xt_engines g_engines_list;
extern uint64_t g_tsc_rate;
extern int  g_pid;
extern int g_shmid;

extern void xt_admin_init(xt_admin_qpair *aqinfo, char * pcie_list,  int pcie_count);


extern unsigned long long xt_admin_get_bar_size(xt_admin_qpair *aqinfo);

extern unsigned long long xt_sys_tick_us(xt_admin_qpair *aqinfo);

extern int xt_env_init(xt_admin_qpair *aqinfo);

extern int xt_env_fini(xt_admin_qpair *aqinfo);

extern void xt_device_destory(xt_admin_qpair *aqinfo);

extern int xt_device_init(xt_admin_qpair *aqinfo);

extern int xt_device_fini(xt_admin_qpair *aqinfo);

extern int xt_nvme_device_subsystem_reset(xt_admin_qpair *aqinfo);

extern int xt_nvme_device_reset(xt_admin_qpair *aqinfo);

extern xt_io_qpair *xt_qpair_create(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, int qprio, int qdepth);

extern int xt_qpair_free(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo);

extern void xt_qpair_destroy(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo);

extern int xt_completed_io_check(xt_admin_qpair *aqinfo, cmds_u* io_unit);

extern cmds_u *xt_prepare_io_unit(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo);

extern void xt_submit_io_cmd(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, xt_buffer *buf, cmds_u *io_unit, unsigned int length, unsigned int lbacnt);

extern int xt_wait_completion_io(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, unsigned int max_completions);

extern int xt_wait_qpair_all_submission_io_completion(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo);

extern int xt_completed_admin_check(xt_admin_qpair *aqinfo, cmds_u* admin_unit); 

extern cmds_u *xt_prepare_admin_unit(xt_admin_qpair *aqinfo);

extern void xt_submit_admin_cmd(xt_admin_qpair *aqinfo, xt_buffer *buf, cmds_u *admin_unit, unsigned int length);

extern int xt_wait_completion_admin(xt_admin_qpair *aqinfo);

extern xt_engine_ops *xt_load_engine(char* engine_ops_name, xt_admin_qpair *aqinfo);

extern unsigned int xt_get_engine_io_sync_flag(xt_admin_qpair *aqinfo);

extern unsigned int xt_get_engine_admin_sync_flag(xt_admin_qpair *aqinfo);

extern unsigned long long get_system_ticks(void);

extern unsigned char xt_pcie_device_config_read8(xt_admin_qpair *aqinfo, unsigned int offset);

extern unsigned short xt_pcie_device_config_read16(xt_admin_qpair *aqinfo, unsigned int offset);

extern unsigned int xt_pcie_device_config_read32(xt_admin_qpair *aqinfo, unsigned int offset);

extern unsigned long long xt_pcie_device_config_read64(xt_admin_qpair *aqinfo, unsigned int offset);

extern void xt_pcie_device_config_write8(xt_admin_qpair *aqinfo, unsigned int offset, unsigned char value);

extern void xt_pcie_device_config_write16(xt_admin_qpair *aqinfo, unsigned int offset, unsigned short value);

extern void xt_pcie_device_config_write32(xt_admin_qpair *aqinfo, unsigned int offset, unsigned int value);

extern void xt_pcie_device_config_write64(xt_admin_qpair *aqinfo, unsigned int offset, unsigned long long value);

extern unsigned char xt_nvme_register_read8(xt_admin_qpair *aqinfo, unsigned int offset);

extern unsigned short xt_nvme_register_read16(xt_admin_qpair *aqinfo, unsigned int offset);

extern unsigned int xt_nvme_register_read32(xt_admin_qpair *aqinfo, unsigned int offset);

extern unsigned long long xt_nvme_register_read64(xt_admin_qpair *aqinfo, unsigned int offset);

extern void xt_nvme_register_write8(xt_admin_qpair *aqinfo, unsigned int offset, unsigned char value);

extern void xt_nvme_register_write16(xt_admin_qpair *aqinfo, unsigned int offset, unsigned short value);

extern void xt_nvme_register_write32(xt_admin_qpair *aqinfo, unsigned int offset, unsigned int value);

extern void xt_nvme_register_write64(xt_admin_qpair *aqinfo, unsigned int offset, unsigned long long value);

extern int xt_pcie_bar_map(xt_admin_qpair *aqinfo, unsigned int bir);

extern int xt_pcie_bar_unmap(xt_admin_qpair *aqinfo, unsigned int bir);

extern void xt_pcie_get_bar_data(xt_admin_qpair *aqinfo, void * bar_addr);

extern void print_latency_histogram(xt_admin_qpair *aqinfo, unsigned int latency_summary, unsigned int latency_histogram);

extern void xt_io_histogram_reset(xt_admin_qpair *aqinfo);

extern void xt_delay_us(unsigned int delay_us);

extern void xt_set_io_timespec_timeout(xt_io_qpair *qinfo, unsigned int timeout);

extern void xt_set_admin_timespec_timeout(xt_admin_qpair *aqinfo, unsigned int timeout);

extern void xt_log_set_print_level(int level);

extern unsigned long long get_total_read_size(void);

extern unsigned long long get_total_write_size(void);

extern unsigned long long get_total_iops_count(void);

extern unsigned long long get_total_io_size(void);

void check_cutoff(void *ctx, uint64_t start, uint64_t end, uint64_t count, uint64_t total, uint64_t so_far);

void print_bucket(void *ctx, uint64_t start, uint64_t end, uint64_t count, uint64_t total, uint64_t so_far);

void xt_init_share_memory(void);

void xt_init_commands_logger(void);

int xt_pcie_init(xt_admin_qpair *aqinfo);

void xt_admin_qpair_check(xt_admin_qpair *aqinfo);

void handle_sigint(int sig);

void bind_cpu_main_thread(void);

static inline bool is_power_of_2(uint64_t val){
	return (val != 0 && ((val & (val - 1)) == 0));
}


static inline void xt_io_tailer_prepare( xt_buffer *buf, cmds_u *io_unit, void * buffer, unsigned int lbacnt){
	// unsigned long long init_tick = spdk_get_ticks();
	xt_verify_tailer * io_tailer;
	buf->buf_status = XT_BUFFER_BUSY;
	unsigned int _step;
	int offset;
	switch (io_unit->pi_type){
		case 0:
		case 2:
			_step = io_unit->sector_size >> 4;
			offset = -1;
			io_tailer = (xt_verify_tailer *)buffer;
			for (unsigned int i = 0; i < lbacnt; i ++){
				offset += _step;
				io_tailer[offset].slba = io_unit->slba + i;
				if(buf->sub_buf_index == 0xF){
					io_tailer[offset].raw[2] = buf->buf_index << 4 | 0xF;
				}else{
					io_tailer[offset].raw[2] = buf->buf_index << 4 | (i & XT_BUFFER_IO_TAILER_MARK);
				}
				io_tailer[offset].raw[3] = io_tailer[offset].raw[0] ^ io_tailer[offset].raw[1] ^ io_tailer[offset].raw[2];
			}
			// init_tick = spdk_get_ticks() - init_tick;
			// SPDK_NOTICELOG("prepare io tailer: %lld pi type %d lbacnt %d\n", init_tick, io_unit->pi_type, lbacnt);
			break;
		case 1:
			_step = io_unit->sector_size;
			offset = -16;
			for (unsigned int i = 0; i < lbacnt; i ++){
				offset += _step;
				io_tailer = (xt_verify_tailer *)(buffer + offset);
				io_tailer[0].slba = io_unit->slba + i;
				if(buf->sub_buf_index == 0xF){
					io_tailer[0].raw[2] = buf->buf_index << 4 | 0xF;
				}else{
					io_tailer[0].raw[2] = buf->buf_index << 4 | (i & XT_BUFFER_IO_TAILER_MARK);
				}
				io_tailer[0].raw[3] = io_tailer[0].raw[0] ^ io_tailer[0].raw[1] ^ io_tailer[0].raw[2];
				offset += io_unit->meta_sector_size;
			}
			break;
		default:
			break;
	}
}

static inline void xt_io_completed_recover_update(xt_io_qpair *qinfo, cmds_u *io_unit, unsigned int block_size){
	io_unit->cmd_status = XT_CMD_UNIT_COMPLETED;
	if (io_unit->opc == 2){
		g_xt_cmd_log->cmds_log_header.total_read_size += block_size * io_unit->sector_size;
		if (qinfo->aqinfo->histogram_flag)
			xt_histogram_data_tally(qinfo->aqinfo->read_histogram, io_unit->complete_time);
		g_xt_cmd_log->cmds_log_header.total_io_size += block_size * io_unit->sector_size;
	}else if(io_unit->opc == 1){
		g_xt_cmd_log->cmds_log_header.total_write_size += block_size * io_unit->sector_size;
		if (qinfo->aqinfo->histogram_flag)
			xt_histogram_data_tally(qinfo->aqinfo->write_histogram, io_unit->complete_time);
		if(io_unit->io_tailer_flag){
			xt_buffer *buf = io_unit->io_buffer;
			// pthread_mutex_unlock(&(buf->buffer_lock));
			buf->buf_status = XT_BUFFER_FREE;
		}
	}
	qinfo->qpair_completions += 1;
    g_xt_cmd_log->cmds_log_header.total_iops_count++;
	cmds_u_rpush(io_unit->completed_cmds_u_ring, io_unit);
}
#endif