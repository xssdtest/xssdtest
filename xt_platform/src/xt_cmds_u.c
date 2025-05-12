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
#include "xt_cmds_u.h"
// SPDK_LOG_REGISTER_COMPONENT("xssdtest", XT_SSD_TEST_LOG)
extern xt_commands_logger* g_xt_cmd_log;
extern uint64_t g_tsc_rate;
extern struct frand_state g_frand_state;
extern int  g_pid;
extern int g_shmid;
static char *g_cmds_unit_status_description[] = {
	"free",
	"busy",
	"completed"
};

static unsigned int g_sub_sector_index[0x10] = {0, 512, 512 * 2, 512 * 3, 512 * 4, 512 * 5, 512 * 6,  512 * 7, 0, 0, 0, 0, 0, 0, 0, 0};


int cmds_u_rinit(cmds_u_ring *ring, unsigned int nr)
{
	ring->max = nr + 1;
	if (ring->max & (ring->max - 1)) {
		ring->max--;
		ring->max |= ring->max >> 1;
		ring->max |= ring->max >> 2;
		ring->max |= ring->max >> 4;
		ring->max |= ring->max >> 8;
		ring->max |= ring->max >> 16;
		ring->max++;
	}

	ring->ring = calloc(ring->max, sizeof(cmds_u *));
	if (!ring->ring)
		return false;
	ring->head = ring->tail = 0;
	ring->nr = nr;
	return true;
}

void cmds_u_rexit(cmds_u_ring *ring)
{
	free(ring->ring);
}
void cmds_u_rreset(cmds_u_ring *ring){
	ring->head = ring->tail = 0;
}

void cmds_u_rpush(cmds_u_ring *r, cmds_u *cmd_u)
{
	if (r->head + 1 != r->tail) {
		r->ring[r->head] = cmd_u;
		r->head = (r->head + 1) & (r->max - 1);
		return;
	}
	assert(0);
}

cmds_u *cmds_u_rpop(cmds_u_ring *r)
{
	if (r->head != r->tail) {
		cmds_u *cmd_u = r->ring[r->tail];
		r->tail = (r->tail + 1) & (r->max - 1);
		return cmd_u;
	}
	return NULL;
}

cmds_u *cmds_u_get_ring_next(cmds_u_ring *r, unsigned int init_next){
    if (init_next){
        r->ring_next = r->tail; 
    }
 	if (r->head != r->ring_next) {
		cmds_u *cmd_u = r->ring[r->ring_next];
		r->ring_next = (r->ring_next + 1) & (r->max - 1);
		return cmd_u;
	}
	return NULL; 
}

cmds_u *cmds_u_get_io_u_next(cmds_u_ring *r, unsigned int init_next){
    if (init_next){
        r->io_u_next = 0; 
    }
 	if (r->io_u_next <= r->max) {
		cmds_u *cmd_u = r->ring[r->io_u_next];
		r->io_u_next = r->io_u_next + 1;
		return cmd_u;
	}
	return NULL; 
}


int cmds_u_rempty(cmds_u_ring *ring)
{
	return ring->head == ring->tail;
}

int xt_read_data_verify(cmds_u* io_u){
    bool check_status = true;
    xt_io_qpair *qinfo = io_u->qpair_info;
    unsigned int io_check_type = qinfo->io_check_type;
    /*  0 not check;  bit 1 check status code and status code type; */
    /*  bit 2 read command check data include empty buffer  */
    /*  bit 3 read command check data with excepted write buffer  */
    /*  bit 4 read command check data with buffer tailer  */
    /*  bit 5 read command only check buffer tailer (quickly performance check)*/
    /*  other bits resevered*/
    if(io_check_type >= 0x8){
        unsigned int lba_block_size = (io_u->cdw12 & 0xFFFF) + 1;
        unsigned long long slba = io_u->slba;
        int compare_rtn = 0;
        unsigned int block_size = io_u->sector_size + io_u->meta_sector_size;
        unsigned int _io_tailer_offset = io_u->sector_size - sizeof(xt_verify_tailer);
        if(io_u->xt_buffer_offset){
            SPDK_ERRLOG("buffer offset isn't 0, don't support to call default data verify function\n");
        }
        unsigned int compare_size;
        unsigned int _buf_cmp_offsert = 0;
        unsigned int _sector_512 = io_u->sector_size == 512;
        xt_verify_tailer * io_tailer;
        unsigned int xor;
        unsigned int buf_index = 0; 
        unsigned int sub_buf_index = 0;
        if(io_u->pi_type == 1){
            compare_size = io_u->sector_size;
        }else{
            compare_size = io_u->sector_size - sizeof(xt_verify_tailer);
        }
        for (unsigned int i =0; i < lba_block_size; i ++){
            io_tailer = (xt_verify_tailer *)(io_u->io_buffer->buf + _io_tailer_offset);
            if(!(io_check_type & 0x10)){
                switch (io_u->pi_type){
                    case 0:
                    case 2: 
                        if(io_u->excepted_write_check){
                            compare_size = lba_block_size * io_u->sector_size;
                            compare_rtn = memcmp(io_u->io_buffer->buf, qinfo->write_buf_addr_list[io_u->excepted_write_buffer_index >> 4]->buf, compare_size);
                            if (compare_rtn != 0){
                                SPDK_ERRLOG("Slba LBA 0x%llx; LBA Count %d; Compare Failed 0x%llx; Expected Write Buffer %d; Memory Compare Failed\n", 
                                            slba, lba_block_size, slba, io_tailer->buf_index);
                                return false;
                            }
                            return true;
                        }
                        break;
                    case 1:
                        if(io_u->excepted_write_check){
                            buf_index = io_u->excepted_write_buffer_index >> 4;
                            sub_buf_index = i & XT_BUFFER_IO_TAILER_MARK;
                        }else{
                            buf_index = io_tailer->buf_index;
                            sub_buf_index = io_tailer->sub_buf_index;
                        }
                        break;
                    default:
                        break;
                }
                if(_sector_512){
                    compare_rtn = memcmp(io_u->io_buffer->buf + _buf_cmp_offsert, (qinfo->write_buf_addr_list[buf_index])->buf + g_sub_sector_index[sub_buf_index], compare_size);
                }else{
                    compare_rtn = memcmp(io_u->io_buffer->buf + _buf_cmp_offsert, (qinfo->write_buf_addr_list[buf_index])->buf, compare_size);
                }
                if (compare_rtn != 0){
                    SPDK_ERRLOG("Slba LBA 0x%llx; LBA Count %d; Compare Failed 0x%llx; Expected Write Buffer %d; Expected Write Sub Buffer %d; Memory Compare Failed\n", 
                                 slba, lba_block_size, slba + i, buf_index, sub_buf_index);
                    SPDK_ERRLOG("io_tailer raw data: %d\t%d\t%d\t%d\t\n", io_tailer->raw[0], io_tailer->raw[1], io_tailer->raw[2], io_tailer->raw[3]);
                    check_status = false;
                    break;
                }
            }
            if(! io_u->excepted_write_check){
                xor = io_tailer->raw[0] ^ io_tailer->raw[1] ^ io_tailer->raw[2];
                if (io_tailer->tailer_xor != xor){
                    SPDK_ERRLOG("Slba LBA 0x%llx; LBA Count %d; Compare Failed 0x%llx Compare Xor Failed: Expected Xor %d Calculate Xor %d\n", slba, lba_block_size, 
                                slba + i, io_tailer->tailer_xor, xor);
                    SPDK_ERRLOG("io_tailer raw data: %d\t%d\t%d\t%d\t \n", io_tailer->raw[0], io_tailer->raw[1], io_tailer->raw[2], io_tailer->raw[3]);
                    check_status = false;
                    break;
                } 
                if (slba + i != io_tailer->slba){
                    if (io_tailer->slba == 0 && (io_check_type & 0x4))
                        continue;
                    SPDK_ERRLOG("Slba LBA 0x%llx; LBA Count %d; Compare Failed 0x%llx Compare Slba Failed \n", slba, lba_block_size, slba + i);
                    check_status = false;
                    break;
                }
            }
            _io_tailer_offset += block_size;
            _buf_cmp_offsert += block_size;
        }
    }
    return check_status;
}

void xt_dump_io_unit(xt_io_qpair *qinfo){
    cmds_u * _io_u;
    SPDK_NOTICELOG("subcommit count %llx, last subcommit count %llx, completions count %llx \n", qinfo->submit_count, qinfo->last_submit_count, qinfo->qpair_completions);
    _io_u = cmds_u_get_ring_next(qinfo->completed_cmds_u_ring, true);
    while(_io_u){
        SPDK_NOTICELOG("io unit %p io unit status %s\n", _io_u, g_cmds_unit_status_description[_io_u->cmd_status]);
        _io_u = cmds_u_get_ring_next(qinfo->completed_cmds_u_ring, false);
    }
}

cmds_u *xt_prepare_io_unit_with_engine(xt_io_qpair *qinfo)
{
    cmds_u * _io_u;
    unsigned long long init_tick;
    // xt_engine_ops *engine_ops = qinfo->aqinfo->engine_ops;
    // SPDK_NOTICELOG("debug qinfo %p, completed_cmds_u_ring %p\n", qinfo, qinfo->completed_cmds_u_ring);
    if (qinfo->reap_type == 0){
        init_tick = spdk_get_ticks();
        do{
            qinfo->aqinfo->engine_ops->xt_engine_wait_completion_io(qinfo, 0);
            _io_u = cmds_u_rpop(qinfo->completed_cmds_u_ring);
            if ( NULL != _io_u){
                if (_io_u->cmd_status ==  XT_CMD_UNIT_FREE){
                    return _io_u;
                }
                if(qinfo->aqinfo->engine_ops->xt_engine_completed_io_check){
                    qinfo->aqinfo->engine_ops->xt_engine_completed_io_check(_io_u);
                }
                return _io_u;
            }
            // xt_delay_ns(50);
        } while (spdk_get_ticks() - init_tick < qinfo->timeout);
        SPDK_ERRLOG("Can't find a valid io_unit after wait %lld \n", qinfo->timeout);
        assert(0); /* timeout get io command */
    }else if ((qinfo->reap_type == 1) | (qinfo->reap_type == 4)){
        // SPDK_DEBUGLOG("qinfo->submit_count 0x%llx qinfo->last_submit_count 0x%llx qinfo->current_iodepth_count 0x%x\n",qinfo->submit_count,  qinfo->last_submit_count, qinfo->current_iodepth_count);
        if (qinfo->submit_count - qinfo->last_submit_count != qinfo->current_iodepth_count){
            _io_u = cmds_u_rpop(qinfo->completed_cmds_u_ring);
			qinfo->aqinfo->engine_ops->xt_engine_wait_completion_io(qinfo, 0);
            if (NULL != _io_u && _io_u->cmd_status ==  XT_CMD_UNIT_FREE){
                return _io_u;
            }else{
                if (NULL == _io_u){
                    SPDK_ERRLOG("Get io unit is null \n");
                }else{
                    SPDK_ERRLOG("Get a invalid io unit status: %d \n", _io_u->cmd_status);
                }
                assert(0); /*expect get a valid */
            }
        }else{
            unsigned long long totaltimeout = qinfo->timeout * qinfo->current_iodepth_count;
            unsigned int completed_io_check_count = 0;
            unsigned int completed_check_index;
            init_tick = spdk_get_ticks();
            while (spdk_get_ticks() - init_tick < totaltimeout){
                qinfo->aqinfo->engine_ops->xt_engine_wait_completion_io(qinfo, 0);
                if (qinfo->qpair_completions == qinfo->current_iodepth_count){
                    break;
                }
                completed_check_index = qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1);
                if (NULL != qinfo->completed_cmds_u_ring->ring[completed_check_index] && qinfo->completed_cmds_u_ring->ring[completed_check_index]->cmd_status == XT_CMD_UNIT_COMPLETED ){
					if(qinfo->aqinfo->engine_ops->xt_engine_completed_io_check){
	                    qinfo->aqinfo->engine_ops->xt_engine_completed_io_check(qinfo->completed_cmds_u_ring->ring[completed_check_index]);
                        completed_io_check_count ++;
					}
                }
            }
            if (qinfo->qpair_completions != qinfo->current_iodepth_count){
                SPDK_ERRLOG("wait all command timeout, submission count %lld, completed count %lld\n ",(qinfo->submit_count - qinfo->last_submit_count), qinfo->qpair_completions);
                assert(0);
            }  
            // Solution 1      
            // while (qinfo->completed_cmds_u_ring->ring[qinfo->completed_cmds_u_ring->head]->cmd_status != XT_CMD_UNIT_FREE){
			// 	if(engine_ops->xt_engine_completed_io_check){
	        //         engine_ops->xt_engine_completed_io_check(qinfo->completed_cmds_u_ring->ring[qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1)]);
			// 	}
            // }

            // Solution 2
            // _io_u = cmds_u_get_ring_next(qinfo->completed_cmds_u_ring, true);
            // while(_io_u){
            //     if(_io_u->cmd_status == XT_CMD_UNIT_COMPLETED){
            //         if(engine_ops->xt_engine_completed_io_check){
	        //             engine_ops->xt_engine_completed_io_check(_io_u);
			// 		}
            //     }
            //     _io_u = cmds_u_get_ring_next(qinfo->completed_cmds_u_ring, false);
            // }
            // Solution 3
            completed_io_check_count = qinfo->current_iodepth_count - completed_io_check_count;
            for(unsigned int index=0; index < completed_io_check_count; index ++){
                if(qinfo->aqinfo->engine_ops->xt_engine_completed_io_check){
                    qinfo->aqinfo->engine_ops->xt_engine_completed_io_check(qinfo->completed_cmds_u_ring->ring[qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1)]);
                }                
            }
            // SPDK_DEBUGLOG(,"completed_check_index: %d head %d \n", qinfo->completed_check_index, qinfo->completed_cmds_u_ring->head);
            _io_u = cmds_u_rpop(qinfo->completed_cmds_u_ring);
            if (NULL == _io_u){
                SPDK_ERRLOG("Get io unit is null in reap type %d\n", qinfo->reap_type);
            }else{
                qinfo->qpair_completions = 0;
                qinfo->last_submit_count = qinfo->submit_count;
                return _io_u;
            }
        }
        SPDK_ERRLOG("Get io unit is null in reap type %d qpair_completions 0x%llx completed_check_index 0x%llx\n", qinfo->reap_type, qinfo->qpair_completions, qinfo->completed_check_index);
        xt_dump_io_unit(qinfo);
        return NULL;
    } else if ((qinfo->reap_type == 2) |  (qinfo->reap_type == 3)){
        /* limit iops */
        if((g_xt_cmd_log->cmds_log_header.total_iops_count - qinfo->last_second_iops_count == qinfo->limit_iops_count) | (g_xt_cmd_log->cmds_log_header.total_io_size - qinfo->last_second_total_io_count == qinfo->limit_io_count)){
            init_tick = spdk_get_ticks();
            while (spdk_get_ticks() - init_tick < g_tsc_rate){
                qinfo->aqinfo->engine_ops->xt_engine_wait_completion_io(qinfo, 0);
                if(qinfo->submit_count - qinfo->last_submit_count == qinfo->qpair_completions)
                    break;
            }
            if (NULL != qinfo->completed_cmds_u_ring->ring[qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1)] &&
                qinfo->completed_cmds_u_ring->ring[qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1)]->cmd_status == XT_CMD_UNIT_COMPLETED ){
				if(qinfo->aqinfo->engine_ops->xt_engine_completed_io_check){
	                qinfo->aqinfo->engine_ops->xt_engine_completed_io_check(qinfo->completed_cmds_u_ring->ring[qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1)]);
				}
            }
            if(qinfo->submit_count - qinfo->last_submit_count == qinfo->qpair_completions){
                SPDK_ERRLOG("subcommit count %llx, last subcommit count %llx, completions count %llx \n", qinfo->submit_count, qinfo->last_submit_count, qinfo->qpair_completions);
                assert(0);
            }
            while (qinfo->completed_cmds_u_ring->ring[qinfo->completed_cmds_u_ring->head]->cmd_status != XT_CMD_UNIT_FREE){
				if(qinfo->aqinfo->engine_ops->xt_engine_completed_io_check){
	                qinfo->aqinfo->engine_ops->xt_engine_completed_io_check(qinfo->completed_cmds_u_ring->ring[qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1)]);
				}
            }
            _io_u = cmds_u_rpop(qinfo->completed_cmds_u_ring);
            if (qinfo->reap_type == 2){
                qinfo->last_second_iops_count = g_xt_cmd_log->cmds_log_header.total_iops_count;
            }else{
                qinfo->last_second_total_io_count = g_xt_cmd_log->cmds_log_header.total_io_size;
            }
            qinfo->last_submit_count = qinfo->submit_count;
            assert(_io_u != NULL);
            init_tick = g_tsc_rate - (spdk_get_ticks() - qinfo->last_tick_recover);
            init_tick = init_tick / g_tsc_rate * 1000000;
            spdk_delay_us(init_tick);
        }else{
            _io_u = cmds_u_rpop(qinfo->completed_cmds_u_ring);
            if (NULL != qinfo->completed_cmds_u_ring->ring[qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1)] &&
                qinfo->completed_cmds_u_ring->ring[qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1)]->cmd_status == XT_CMD_UNIT_COMPLETED ){
				if(qinfo->aqinfo->engine_ops->xt_engine_completed_io_check){
	                qinfo->aqinfo->engine_ops->xt_engine_completed_io_check(qinfo->completed_cmds_u_ring->ring[qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1)]);
				}
            }
            if (NULL != _io_u){
                if (_io_u->cmd_status ==  XT_CMD_UNIT_FREE){
                    return _io_u;
                }
                assert(0); /* timeout get io command */
            }else{
                init_tick = spdk_get_ticks();
                while ( (NULL == _io_u) & (spdk_get_ticks() - init_tick < qinfo->timeout))
                {
                    qinfo->aqinfo->engine_ops->xt_engine_wait_completion_io(qinfo, 0);
                    _io_u = cmds_u_rpop(qinfo->completed_cmds_u_ring);
                    if ( NULL != _io_u){
                        qinfo->aqinfo->engine_ops->xt_engine_completed_io_check(_io_u);
                        return _io_u;
                    }
                }    
            }
            SPDK_ERRLOG("Can't find a valid io_unit after wait %lld \n", qinfo->timeout);
            assert(0); /* timeout get io command */
        }
    }else{
        SPDK_ERRLOG("invalid repall type \n"); /* invalid repall type */
        assert(0);
    }
    SPDK_ERRLOG("Can't find a valid io_unit after wait %lld and return NULL\n", qinfo->timeout);
    xt_dump_io_unit(qinfo);
    return NULL;
}

cmds_u *xt_prepare_admin_unit_with_engine(xt_admin_qpair *aqinfo)
{
    cmds_u * _cmd_u;
    unsigned long long init_tick;
    xt_engine_ops *engine_ops = aqinfo->engine_ops;
    if (aqinfo->completed_cmds_u_ring->head == aqinfo->completed_cmds_u_ring->tail){
        _cmd_u = cmds_u_rpop(aqinfo->completed_cmds_u_ring);
        init_tick = spdk_get_ticks();
        while ( (NULL == _cmd_u) & (spdk_get_ticks() - init_tick < aqinfo->timeout)){
				engine_ops->xt_engine_wait_completion_admin(aqinfo);
                _cmd_u = cmds_u_rpop(aqinfo->completed_cmds_u_ring);
                if ( NULL != _cmd_u){
					if(engine_ops->xt_engines_completed_admin_check){
						if(!engine_ops->xt_engines_completed_admin_check(_cmd_u)){
							SPDK_ERRLOG("admin command check failed \n ");
						}
					}
                    return _cmd_u;
                }
        }
        if (NULL != _cmd_u){
            SPDK_ERRLOG("wait admin command timeout\n");
            assert(0);
        }     
    }else{
        _cmd_u = cmds_u_rpop(aqinfo->completed_cmds_u_ring);
        if(engine_ops->xt_engines_completed_admin_check){
            if(!engine_ops->xt_engines_completed_admin_check(_cmd_u)){
                SPDK_ERRLOG("admin command check failed \n ");
            }
        }
    }
    return _cmd_u;
}


random_io_entry *xt_io_entry_init(unsigned int count){
    random_io_entry *io_entrys = malloc(sizeof(random_io_entry) * (count +1));
    if(io_entrys == NULL){
        SPDK_ERRLOG("alloc buffer failed, return NULL\n ");
    }
    return io_entrys;
}

void xt_io_entry_fini(random_io_entry *io_entrys){
    if(io_entrys != NULL){
        free(io_entrys);
    }
}

void xt_io_entry_shuffle(random_io_entry *io_entrys, unsigned int count, unsigned int reset_seed){
    unsigned int rand_key = 0;
    if(reset_seed == 0){
        init_rand_seed(&g_frand_state, reset_seed, true);
    }
    for(int i=count-1; i >= 0 ; i--){
        rand_key = (unsigned int)rand64() % count;
        memcpy(&io_entrys[count], &io_entrys[i], sizeof(random_io_entry));
        memcpy(&io_entrys[i], &io_entrys[rand_key], sizeof(random_io_entry));
        memcpy(&io_entrys[rand_key], &io_entrys[count], sizeof(random_io_entry));
    }
}