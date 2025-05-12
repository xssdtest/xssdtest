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
#include "xt_nvme_ioctrl.h"
#include "../xssdtest.h"
#include "../../spdk/lib/nvme/nvme_internal.h"
SPDK_LOG_REGISTER_COMPONENT("sync", XT_SYNC_LOG)
extern xt_commands_logger* g_xt_cmd_log;
extern uint64_t g_tsc_rate;
extern int  g_pid;
extern int g_shmid;

bool sync_engines_completed_io_check(cmds_u* io_u);

static int sync_engines_env_init(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("sync engines: environment init return directly\n");
    return 0;
}

static int sync_engines_env_fini(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("sync engines: environment fini return directly\n");
    return 0;
}

static int sync_engines_qpair_create(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, int qprio, int qdepth){
    SPDK_NOTICELOG("sync engines: qpair create return directly\n");
    return 0;
}

static int sync_engines_qpair_free(xt_io_qpair *qinfo){
    SPDK_NOTICELOG("sync engines: qpair free return directly\n");
    return 0;
}

static void sync_engines_qpair_destroy(xt_io_qpair *qinfo){
    SPDK_NOTICELOG("sync engines: qpair destory return directly\n");
}

bool sync_engines_completed_io_check(cmds_u* io_u){
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

static cmds_u *sync_engines_prepare_io_unit(xt_io_qpair *qinfo){
    cmds_u * io_unit;
    io_unit = cmds_u_rpop(qinfo->completed_cmds_u_ring);
    if (NULL == io_unit){
        SPDK_ERRLOG("Get io unit is NULL \n");
        assert(0);
    }
    return io_unit;
}

static void sync_engines_submit_io_cmd(xt_io_qpair *qinfo, xt_buffer *buf, cmds_u *io_unit, unsigned int length, unsigned int lbacnt){
    void * buffer = (buf->buf + io_unit->xt_buffer_offset);
    unsigned long long offset = io_unit->cdw11;
    offset = (offset << 32 | io_unit->cdw10) * (io_unit->sector_size);
    if (io_unit->opc == 1 && io_unit->io_tailer_flag){
        xt_io_tailer_prepare(buf, io_unit, buffer, lbacnt);
    }
    qinfo->submit_count ++;
    io_unit->issue_time = spdk_get_ticks(); 
    if(io_unit->opc == 1){
        io_unit->rc = pwrite(qinfo->fid, buffer, length, offset);
    }else{
        *((unsigned long long *)buffer) = XT_MAGIC_NUMBER;
        io_unit->rc = pread(qinfo->fid, buffer, length, offset);
    }
    io_unit->complete_time = spdk_get_ticks() - io_unit->start_time;
    if (qinfo->microseconds_delay){
        spdk_delay_us(qinfo->microseconds_delay);
    }
    if(io_unit->rc < 0){
        SPDK_ERRLOG("submit io command failed with %p\n", io_unit);
    }else{
        xt_io_completed_recover_update(qinfo, io_unit, lbacnt);
    }
}
static int sync_engines_wait_completion_io(xt_io_qpair *qinfo, unsigned int max_completions){
    return 0;
}

static int sync_engines_wait_qpair_all_submission_io_completion(xt_io_qpair *qinfo){
    return 0;
}

static void sync_engines_device_destory(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("sync engines: device destory return directly\n");
}

static int sync_engines_nvme_init(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("sync engines: nvme init return 0 directly\n");
    return 0;
}

static int sync_engines_nvme_fini(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("sync engines: nvme fini return directly\n");
    return 0;
}

static xt_engine_ops xt_unused sync_engine_ops = {
    .name                                              = "sync_nvme",
    .version                                           = XT_IOOPS_VERSION,
    .io_sync_flag                                      = 1,
    .admin_sync_flag                                   = 1,
    .xt_engine_env_init                                = sync_engines_env_init,
    .xt_engine_env_fini                                = sync_engines_env_fini,
    .xt_engine_device_destory                          = sync_engines_device_destory,
    .xt_engine_device_init                             = sync_engines_nvme_init,
    .xt_engine_device_fini                             = sync_engines_nvme_fini,
    .xt_engine_qpair_create                            = sync_engines_qpair_create,
    .xt_engine_qpair_free                              = sync_engines_qpair_free,
    .xt_engine_qpair_destroy                           = sync_engines_qpair_destroy, 
    .xt_engine_completed_io_check                      = sync_engines_completed_io_check,
    .xt_engine_prepare_io_unit                         = sync_engines_prepare_io_unit,
    .xt_engine_submit_io_cmd                           = sync_engines_submit_io_cmd,
    .xt_engine_wait_completion_io                      = sync_engines_wait_completion_io,
    .xt_engine_wait_qpair_all_submission_io_completion = sync_engines_wait_qpair_all_submission_io_completion,
    .xt_engines_completed_admin_check                  = io_ctrl_nvme_engines_completed_admin_check,
    .xt_engine_prepare_admin_unit                      = io_ctrl_nvme_engines_prepare_admin_unit,
    .xt_engine_submit_admin_cmd                        = io_ctrl_nvme_engines_submit_admin_cmd,
    .xt_engine_wait_completion_admin                   = io_ctrl_nvme_engines_wait_completion_admin,
};

static void xt_init xt_sync_nvme_register(void){
	xt_register_engine(&sync_engine_ops);
}