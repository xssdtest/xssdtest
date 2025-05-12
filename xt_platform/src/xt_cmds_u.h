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
#ifndef XT_CMDS_U_H
#define XT_CMDS_U_H
#include <libaio.h>
#include "spdk/stdinc.h"
#include "spdk_internal/log.h"
#include "xt_compiler/xt_compiler.h"
#include "xt_memory.h"
#include "xt_io_qpair.h"
#include "xt_cmds_log.h"
#include "xt_rand.h"
#include "xt_load_engines.h"

typedef struct iocb xt_iocb;
typedef struct _cmds_u cmds_u;
typedef struct _cmds_u_ring cmds_u_ring;
typedef struct _xt_engine_ops xt_engine_ops;
typedef struct _xt_admin_qpair xt_admin_qpair;
typedef struct _xt_io_qpair xt_io_qpair;
typedef struct _xt_buffer xt_buffer;
typedef union _xt_verify_tailer xt_verify_tailer;
typedef struct _xt_commands_logger xt_commands_logger;

enum {
	XT_CMD_UNIT_FREE 		 = 0,   // CMD UNIT FREE
	XT_CMD_UNIT_BUSY 		 = 1,   // CMD UNIT BUSY
	XT_CMD_UNIT_COMPLETED    = 2,   // CMD UNIT COMPLETED
	/*  FREE -->  BUSY --> COMPLETED  --> FREE*/
};

struct xt_nvme_status {
	union 
	{
		uint16_t raw;
		struct {
			uint16_t p	:  1;	/* phase tag */
			uint16_t sc	:  8;	/* status code */
			uint16_t sct	:  3;	/* status code type */
			uint16_t rsvd2	:  2;
			uint16_t m	:  1;	/* more */
			uint16_t dnr	:  1;	/* do not retry */
		};
	};
};

typedef struct _cmds_u_ring {
	unsigned int head;
	unsigned int tail;
	unsigned int max;
	unsigned int nr;
	unsigned int ring_next;
	unsigned int io_u_next;
	cmds_u **ring;
}cmds_u_ring;

typedef struct _cmds_u {
		/* dword 0 */
	uint8_t opc;        	/* opcode */
	union{
		uint8_t flags;
		struct {
			uint8_t fuse	:  2;	/* fused operation */
			uint8_t rsvd1	:  4;
			uint8_t psdt	:  2;
		};
	};
	
	uint16_t cid;		/* command identifier */

	/* dword 1 */
	uint32_t nsid;		/* namespace identifier */

	/* dword 2-3 */
	uint32_t cdw2;
	uint32_t cdw3;

	/* dword 4-5 */
	union{
	    uint64_t mptr;		/* metadata pointer */
	    struct{
	    	uint32_t cdw4;
	        uint32_t cdw5;
	    };
    };
	/* dword 6-9: data pointer */

    union{
        struct {
            uint64_t prp1;		/* prp entry 1 */
            uint64_t prp2;		/* prp entry 2 */
        } ;
         struct {
	    	uint32_t cdw6;
	        uint32_t cdw7;
	    	uint32_t cdw8;
	        uint32_t cdw9;
        };
		struct{
			uint64_t addr;
			uint32_t metadata_len;
			uint32_t data_len;
		};
    };

    union{
		uint64_t slba;
		struct{
			uint32_t cdw10;
			uint32_t cdw11;
		};
	};
	/* dword 12-15 */
	uint32_t cdw12;		/* command-specific */
	uint32_t cdw13;		/* command-specific */
	uint32_t cdw14;		/* command-specific */
	uint32_t cdw15;		/* command-specific */

	uint32_t   timeout_ms;
	uint32_t   rsvd4;
	uint64_t   result;  // command return value
	uint64_t   cb_func; // call back function

		/* dword 0 */
	uint32_t		cpl_cdw0;	/* command-specific */

	/* dword 1 */
	uint32_t		cpl_rsvd1;

	/* dword 2 */
	uint16_t		cpl_sqhd;	/* submission queue head pointer */
	uint16_t		cpl_sqid;	/* submission queue identifier */

	/* dword 3 */
	uint16_t		cpl_cid;	/* command identifier */
	struct xt_nvme_status	cpl_status;
	cmds_u_ring *  completed_cmds_u_ring;  // completed cmd_u ring

	uint64_t start_time;
	uint64_t issue_time;
	uint64_t complete_time;
	uint64_t submit_index;
	xt_io_qpair * qpair_info;
	volatile uint32_t cmd_status;
	uint32_t io_status_code_expected;
	uint32_t io_status_code_type_expected;
	uint32_t sector_size;
	uint32_t meta_sector_size;
	uint32_t io_tailer_flag;
	uint32_t pi_type;

	int rc;

	xt_buffer * io_buffer;
	uint32_t excepted_write_check;
	uint32_t excepted_write_buffer_index;
	uint32_t xt_buffer_offset;

	/*  Initial seed for generating the buffer contents  */
	xt_iocb *iocb;
} __attribute__((__packed__)) __attribute__((aligned(128))) cmds_u;

// # opcode, _slba, _lbacnt, nsid, buf_index, sector_size, meta_sector_size = item[0], item[1], item[2], item[3], item[4], item[5], item[6]
typedef struct _random_io_entry{
	unsigned long long slba;
	unsigned int lbacnt;
	unsigned int nsid;
	unsigned int sector_size;
	unsigned int meta_sector_size;
	unsigned int buf_index;
	unsigned char opcode;
}__attribute__((__packed__)) __attribute__((aligned(32)))random_io_entry;

#define cmds_u_qiter(q, cmds_u, i) for (i = 0; i < (q)->nr && (cmds_u = (q)->cmds_us[i]); i++)

extern random_io_entry *xt_io_entry_init(unsigned int count);

extern void xt_io_entry_fini(random_io_entry *io_entrys);

extern void xt_io_entry_shuffle(random_io_entry *io_entrys, unsigned int count, unsigned int reset_seed);

extern int cmds_u_rempty(cmds_u_ring *ring);

extern cmds_u *cmds_u_rpop(cmds_u_ring *r);

extern cmds_u *cmds_u_get_ring_next(cmds_u_ring *r, unsigned int init_next);

extern cmds_u *cmds_u_get_io_u_next(cmds_u_ring *r, unsigned int init_next);

extern void cmds_u_rpush(cmds_u_ring *r, cmds_u *cmd_u);

extern int cmds_u_rinit(cmds_u_ring *ring, unsigned int nr);

extern void cmds_u_rexit(cmds_u_ring *ring);

extern void cmds_u_rreset(cmds_u_ring *ring);

extern int xt_read_data_verify(cmds_u* io_u);

extern cmds_u *xt_prepare_io_unit_with_engine(xt_io_qpair *qinfo);

extern cmds_u *xt_prepare_admin_unit_with_engine(xt_admin_qpair *aqinfo);

extern void xt_dump_io_unit(xt_io_qpair *qinfo);

static inline void xt_unused xt_delay_ns(unsigned long long nsec) {
    struct timespec req, rem;
    req.tv_sec = 0;
    req.tv_nsec = nsec;
    while (nanosleep(&req, &rem) < 0) {
        req.tv_nsec = rem.tv_nsec;
    }
}

static inline void __cmd_u_mark_map(unsigned long long *map, unsigned int nr)
{
	int idx = 0;

	switch (nr) {
        default:
            idx = 6;
            break;
        case 33 ... 64:
            idx = 5;
            break;
        case 17 ... 32:
            idx = 4;
            break;
        case 9 ... 16:
            idx = 3;
            break;
        case 5 ... 8:
            idx = 2;
            break;
        case 1 ... 4:
            idx = 1;
        case 0:
            break;
	}
	map[idx]++;
}

static inline void cmd_u_mark_submit(xt_io_qpair *qinfo, unsigned int nr)
{
	__cmd_u_mark_map(qinfo->io_u_submit_map, nr);
}

static inline void cmd_u_mark_complete(xt_io_qpair *qinfo, unsigned int nr)
{
	__cmd_u_mark_map(qinfo->io_u_complete_map, nr);
}



#endif
