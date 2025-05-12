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
#include <libaio.h>
#include "xt_nvme_ioctrl.h"
#include "../xssdtest.h"
#include "../../spdk/lib/nvme/nvme_internal.h"
SPDK_LOG_REGISTER_COMPONENT("libaio", XT_LIBAIO_LOG)
extern xt_commands_logger* g_xt_cmd_log;
extern uint64_t g_tsc_rate;
extern int  g_pid;
extern int g_shmid;

static int libaio_engines_env_init(xt_admin_qpair *aqinfo){
    return 0;
}

static int libaio_engines_env_fini(xt_admin_qpair *aqinfo){
    return 0;
}

static int libaio_engines_qpair_create(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, int qprio, int qdepth){
    qinfo->qpair = NULL;
    qinfo->submit_cmds_u_ring = malloc(sizeof(cmds_u_ring));
    cmds_u_rinit(qinfo->submit_cmds_u_ring, qinfo->qpair_iodepth);
    if(is_power_of_2(qinfo->qpair_iodepth)){
        qinfo->qpair_is_pow2 = qinfo->qpair_iodepth - 1;
    }
    qinfo->aio_events = calloc(qinfo->qpair_iodepth, sizeof(struct io_event));
    qinfo->iocbs = calloc(qdepth, sizeof(struct iocb));
    if(io_setup(qdepth, &qinfo->aio_ctx) < 0){
        SPDK_ERRLOG("Init liaaio context failed\n");
    }
    for(int i = 0; i < qdepth; i++){
        qinfo->io_units[i].iocb = &qinfo->iocbs[i];
    }
    SPDK_INFOLOG(XT_LIBAIO_LOG,"libaio engine create io qpair: submit_cmds_u_ring %p;\n", aqinfo->submit_cmds_u_ring);
    return 0;
}

static int libaio_engines_qpair_free(xt_io_qpair *qinfo){
    int rc = 0;
    rc = io_destroy(qinfo->aio_ctx);
    cmds_u_rexit(qinfo->submit_cmds_u_ring);
    free(qinfo->submit_cmds_u_ring);
    free(qinfo->aio_events);
    free(qinfo->iocbs);
    SPDK_INFOLOG(XT_LIBAIO_LOG,"libaio engine free qpair, io_destroy return %d \n", rc);
    return 0;
}

static void libaio_engines_qpair_destroy(xt_io_qpair *qinfo){
    int rc = 0;
    rc = io_destroy(qinfo->aio_ctx);
    cmds_u_rexit(qinfo->submit_cmds_u_ring);
    free(qinfo->submit_cmds_u_ring);
    free(qinfo->aio_events);
    free(qinfo->iocbs);
    SPDK_INFOLOG(XT_LIBAIO_LOG,"libaio engine destory qpair, io_destroy return %d \n", rc);
}

static bool libaio_engines_completed_io_check(cmds_u* io_u){
    xt_io_qpair *qinfo = io_u->qpair_info;
    unsigned int io_check_type = qinfo->io_check_type;
    bool check_status = true;
    if (io_check_type == 0){
        qinfo->completed_check_index ++;
        io_u->cmd_status = XT_CMD_UNIT_FREE;
        return true;
    }
    if (io_check_type & 0x2){
        if ((io_u->io_status_code_expected != io_u->cpl_status.sc) | (io_u->io_status_code_type_expected != io_u->cpl_status.sct)){
            io_u->cmd_status = XT_CMD_UNIT_FREE;
            qinfo->completed_check_index ++;
            return false;
        }
    }
    if (io_u->opc == 2){
        check_status = xt_read_data_verify(io_u);
    }
    qinfo->completed_check_index ++;
    io_u->cmd_status = XT_CMD_UNIT_FREE;
    return check_status;
}

static cmds_u *libaio_engines_prepare_io_unit(xt_io_qpair *qinfo){
    cmds_u * io_unit;
    io_unit = xt_prepare_io_unit_with_engine(qinfo);
    if (NULL == io_unit){
        SPDK_ERRLOG("Get io unit is NULL \n");
        assert(0);
    }
    return io_unit;
}

static void libaio_engines_submit_io_cmd(xt_io_qpair *qinfo, xt_buffer *buf, cmds_u *io_unit, unsigned int length, unsigned int lbacnt){
    void * buffer =  (buf->buf + io_unit->xt_buffer_offset);
    unsigned long long offset = io_unit->slba * (io_unit->sector_size + io_unit->meta_sector_size);
    if (io_unit->opc == 1 && io_unit->io_tailer_flag){
        xt_io_tailer_prepare(buf, io_unit, buffer, lbacnt);
    }
    qinfo->submit_count ++;
    io_unit->issue_time = spdk_get_ticks();
    if(io_unit->opc == 2){
        *((unsigned long long *)buffer) = XT_MAGIC_NUMBER;
        io_prep_pread(io_unit->iocb, qinfo->fid, buffer, length, offset);
    }else
        io_prep_pwrite(io_unit->iocb, qinfo->fid, buffer, length, offset);
    io_unit->rc = io_submit(qinfo->aio_ctx, 1, &io_unit->iocb);
    if(io_unit->rc != 1){
        SPDK_ERRLOG("submit io command failed with %p rc %d length %d offset %lld\n", io_unit, io_unit->rc, length, offset);
    }
    if (qinfo->microseconds_delay){
        spdk_delay_us(qinfo->microseconds_delay);
    }
}

static int libaio_engines_wait_completion_io(xt_io_qpair *qinfo, unsigned int max_completions){
    int events = 0;
    events = io_getevents(qinfo->aio_ctx, 0, qinfo->qpair_iodepth, qinfo->aio_events, NULL);
    if(events > 0){
        cmds_u *io_u;
        unsigned int block_size = 0;
        unsigned int offset = 0;
        int index = 0;
        for(index=0; index < events; index ++){
            offset = qinfo->aio_events[index].obj - qinfo->iocbs;
            io_u = qinfo->completed_cmds_u_ring->ring[offset];
            io_u->complete_time = spdk_get_ticks() - io_u->issue_time;
            block_size = (io_u->cdw12 & 0xFFFF) + 1;
            xt_io_completed_recover_update(qinfo, io_u, block_size);
        }
    }
    return events;
}

static int libaio_engines_wait_qpair_all_submission_io_completion(xt_io_qpair *qinfo){
    cmds_u * io_u;
    if (qinfo->submit_count - qinfo->last_submit_count != qinfo->qpair_completions){
        unsigned long long init_tick;
        unsigned long long totaltimeout = qinfo->timeout * qinfo->current_iodepth_count;
        int events = 0;
        init_tick = spdk_get_ticks();
        unsigned int completed_check_index = qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1);
        while (spdk_get_ticks() - init_tick < totaltimeout){
            events = io_getevents(qinfo->aio_ctx, 0, qinfo->qpair_iodepth, qinfo->aio_events, NULL);
            if(events > 0){
                cmds_u *io_u;
                unsigned int block_size = 0;
                unsigned int offset = 0;
                int index = 0;
                for(index=0; index < events; index ++){
                    offset = qinfo->aio_events[index].obj - qinfo->iocbs;
                    io_u = qinfo->completed_cmds_u_ring->ring[offset];
                    io_u->complete_time = spdk_get_ticks() - io_u->issue_time;
                    block_size = (io_u->cdw12 & 0xFFFF) + 1;
                    xt_io_completed_recover_update(qinfo, io_u, block_size);
                }
            }
            if (qinfo->submit_count - qinfo->last_submit_count == qinfo->qpair_completions){
                break;
            }
            if (NULL != qinfo->completed_cmds_u_ring->ring[completed_check_index] && 
                qinfo->completed_cmds_u_ring->ring[completed_check_index]->cmd_status == XT_CMD_UNIT_COMPLETED ){
                libaio_engines_completed_io_check(qinfo->completed_cmds_u_ring->ring[completed_check_index]);
                completed_check_index = qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1);
            }
        }
        if (qinfo->submit_count - qinfo->last_submit_count != qinfo->qpair_completions){
            SPDK_ERRLOG("wait all command timeout, submission count %lld, completed count %lld\n ",(qinfo->submit_count - qinfo->last_submit_count), qinfo->qpair_completions);
            assert(0);
        }
        io_u = cmds_u_get_ring_next( qinfo->completed_cmds_u_ring, true);
        while(io_u){
            if(io_u->cmd_status == XT_CMD_UNIT_COMPLETED){
                libaio_engines_completed_io_check(io_u);
            }
            io_u = cmds_u_get_ring_next(qinfo->completed_cmds_u_ring, false);
        }
        // SPDK_NOTICELOG("completed_check_index: %d head %d \n", qinfo->completed_check_index, qinfo->completed_cmds_u_ring->head);
    }else{
        io_u = cmds_u_get_ring_next( qinfo->completed_cmds_u_ring, true);
        while(io_u){
            if(io_u->cmd_status == XT_CMD_UNIT_COMPLETED){
                libaio_engines_completed_io_check(io_u);
            }
            io_u = cmds_u_get_ring_next(qinfo->completed_cmds_u_ring, false);
        }
    }
    qinfo->last_submit_count = qinfo->submit_count;
    qinfo->qpair_completions = 0;
    return true;    


}

static void libaio_engines_device_destory(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("libaio engines: device destory return directly\n");
}

static int libaio_engines_nvme_init(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("libaio engines: nvme init return 0 directly\n");
    return 0;
}

static int libaio_engines_nvme_fini(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("libaio engines: nvme fini return directly\n");
    return 0;
}

static xt_engine_ops xt_unused libaio_engine_ops = {
    .name                                              = "libaio_nvme",
    .version                                           = XT_IOOPS_VERSION,
    .io_sync_flag                                      = 0,
    .admin_sync_flag                                   = 1,
    .xt_engine_env_init                                = libaio_engines_env_init,
    .xt_engine_env_fini                                = libaio_engines_env_fini,
    .xt_engine_device_destory                          = libaio_engines_device_destory,
    .xt_engine_device_init                             = libaio_engines_nvme_init,
    .xt_engine_device_fini                             = libaio_engines_nvme_fini,
    .xt_engine_qpair_create                            = libaio_engines_qpair_create,
    .xt_engine_qpair_free                              = libaio_engines_qpair_free,
    .xt_engine_qpair_destroy                           = libaio_engines_qpair_destroy,
    .xt_engine_completed_io_check                      = libaio_engines_completed_io_check,
    .xt_engine_prepare_io_unit                         = libaio_engines_prepare_io_unit,
    .xt_engine_submit_io_cmd                           = libaio_engines_submit_io_cmd,
    .xt_engine_wait_completion_io                      = libaio_engines_wait_completion_io,
    .xt_engine_wait_qpair_all_submission_io_completion = libaio_engines_wait_qpair_all_submission_io_completion,
    .xt_engines_completed_admin_check                  = io_ctrl_nvme_engines_completed_admin_check,
    .xt_engine_prepare_admin_unit                      = io_ctrl_nvme_engines_prepare_admin_unit,
    .xt_engine_submit_admin_cmd                        = io_ctrl_nvme_engines_submit_admin_cmd,
    .xt_engine_wait_completion_admin                   = io_ctrl_nvme_engines_wait_completion_admin,
};

static void xt_init xt_libaio_nvme_register(void){
	xt_register_engine(&libaio_engine_ops);
}
