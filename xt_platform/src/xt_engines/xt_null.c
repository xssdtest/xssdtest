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
#include "../xssdtest.h"
#include "../../spdk/lib/nvme/nvme_internal.h"
SPDK_LOG_REGISTER_COMPONENT("null", XT_NULL_LOG)
extern xt_commands_logger* g_xt_cmd_log;
extern uint64_t g_tsc_rate;
extern int  g_pid;
extern int g_shmid;

static int null_engines_env_init(xt_admin_qpair *aqinfo){
    aqinfo->submit_cmds_u_ring = malloc(sizeof(cmds_u_ring));
    cmds_u_rinit(aqinfo->submit_cmds_u_ring, aqinfo->qpair_iodepth);
    SPDK_INFOLOG(XT_NULL_LOG,"null engine create admin qpair: submit_cmds_u_ring %p\n", aqinfo->submit_cmds_u_ring);
    return 0;
}

static int null_engines_env_fini(xt_admin_qpair *aqinfo){
    cmds_u_rexit(aqinfo->submit_cmds_u_ring);
    free(aqinfo->submit_cmds_u_ring);
    SPDK_INFOLOG(XT_NULL_LOG,"null engine free admin qpair: submit_cmds_u_ring %p;\n",aqinfo->submit_cmds_u_ring);
    return 0;
}

static int null_engines_qpair_create(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, int qprio, int qdepth){
    qinfo->qpair = NULL;
    qinfo->submit_cmds_u_ring = malloc(sizeof(cmds_u_ring));
    cmds_u_rinit(qinfo->submit_cmds_u_ring, qdepth);
    SPDK_INFOLOG(XT_NULL_LOG,"null engine create io qpair: submit_cmds_u_ring %p;\n", qinfo->submit_cmds_u_ring);
    return 0;
}

static int null_engines_qpair_free(xt_io_qpair *qinfo){
    cmds_u_rexit(qinfo->submit_cmds_u_ring);
    free(qinfo->submit_cmds_u_ring);
    SPDK_INFOLOG(XT_NULL_LOG,"null engine free io qpair: submit_cmds_u_ring %p;\n",qinfo->submit_cmds_u_ring);
    return 0;
}

static void null_engines_qpair_destroy(xt_io_qpair *qinfo){
    SPDK_INFOLOG(XT_NULL_LOG,"null engine return directly \n");
}

static bool null_engines_completed_io_check(cmds_u* io_u){
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

static cmds_u *null_engines_prepare_io_unit(xt_io_qpair *qinfo){
    cmds_u * io_unit;
    io_unit = xt_prepare_io_unit_with_engine(qinfo);
    if (NULL == io_unit){
        SPDK_ERRLOG("Get io unit is NULL \n");
        assert(0);
    }
    return io_unit;
}

static void null_engines_submit_io_cmd(xt_io_qpair *qinfo, xt_buffer *buf, cmds_u *io_unit, unsigned int length, unsigned int lbacnt){
    void * buffer =  (buf->buf + io_unit->xt_buffer_offset);
    unsigned long long offset = io_unit->cdw11;
    unsigned int block_size = (io_unit->cdw12 & 0xFFFF) + 1;
    offset = (offset << 32 | io_unit->cdw10) * (io_unit->sector_size + io_unit->meta_sector_size);
    if (io_unit->opc == 1 && io_unit->io_tailer_flag){
        xt_io_tailer_prepare(buf, io_unit, buffer, lbacnt);
    }
    if(io_unit->opc == 2)
        *((unsigned long long *)buffer) = XT_MAGIC_NUMBER;
    io_unit->addr = (unsigned long long)buffer;
    io_unit->data_len = block_size * io_unit->sector_size;
    qinfo->submit_count ++;
    io_unit->issue_time = spdk_get_ticks(); 
    cmds_u_rpush(qinfo->submit_cmds_u_ring, io_unit);
    io_unit->rc = 0;
    if (qinfo->microseconds_delay){
        spdk_delay_us(qinfo->microseconds_delay);
    }
}

static int null_engines_wait_completion_io(xt_io_qpair *qinfo, unsigned int max_completions){
    if (cmds_u_rempty(qinfo->submit_cmds_u_ring)){
        return 0;
    }else{
        cmds_u *io_u;
        unsigned int block_size;
        unsigned int variable_assignment = 0;
        io_u = cmds_u_rpop(qinfo->submit_cmds_u_ring);
        // io_u->complete_time = spdk_get_ticks() - io_u->start_time;
        io_u->complete_time = spdk_get_ticks() - io_u->issue_time;
        io_u->cpl_cdw0  = variable_assignment; 
        io_u->cpl_rsvd1 = variable_assignment; 
        io_u->cpl_sqhd  = variable_assignment; 
        io_u->cpl_sqid  = variable_assignment; 
        io_u->cpl_cid   = variable_assignment; 
        io_u->cpl_status.p = variable_assignment; 
        io_u->cpl_status.sc = variable_assignment; 
        io_u->cpl_status.sct = variable_assignment; 
        io_u->cpl_status.rsvd2 = variable_assignment;
        io_u->cpl_status.m = variable_assignment;
        io_u->cpl_status.dnr = variable_assignment; 
        block_size = (io_u->cdw12 & 0xFFFF) + 1;
        xt_io_completed_recover_update(qinfo, io_u, block_size);
    }
    return 0;
}

static int null_engines_wait_qpair_all_submission_io_completion(xt_io_qpair *qinfo){
    while(cmds_u_rempty(qinfo->submit_cmds_u_ring)){
        null_engines_wait_completion_io(qinfo, 0);
    }
    return 0;
}

static bool null_engines_completed_admin_check(cmds_u* _cmds_u){
    if ((_cmds_u->io_status_code_expected != _cmds_u->cpl_status.sc) | (_cmds_u->io_status_code_type_expected != _cmds_u->cpl_status.sct)){
        _cmds_u->cmd_status = XT_CMD_UNIT_FREE;
        return false;
    }
    return true;    
}


static cmds_u *null_engines_prepare_admin_unit(xt_admin_qpair *aqinfo){
    cmds_u * _cmds_u;
    _cmds_u = xt_prepare_admin_unit_with_engine(aqinfo);
    if (NULL == _cmds_u){
        SPDK_ERRLOG("Get io unit is NULL \n");
        assert(0);
    }
    return _cmds_u;
}

static void null_engines_submit_admin_cmd(xt_admin_qpair *aqinfo, xt_buffer *buf, cmds_u *admin_unit, unsigned int length){
    void * buffer =  (buf->buf + admin_unit->xt_buffer_offset);
    admin_unit->addr = (unsigned long long) buffer;
    admin_unit->data_len = admin_unit->cdw10 << 2;
    admin_unit->start_time = spdk_get_ticks(); 
    admin_unit->cmd_status = XT_CMD_UNIT_BUSY;
    cmds_u_rpush(aqinfo->submit_cmds_u_ring, admin_unit);
    admin_unit->rc = 0;
}

static int null_engines_wait_completion_admin(xt_admin_qpair *aqinfo){
    if (cmds_u_rempty(aqinfo->submit_cmds_u_ring)){
        return 0;
    }else{
        cmds_u *admin_u;
        unsigned int variable_assignment = 0;
        admin_u = cmds_u_rpop(aqinfo->submit_cmds_u_ring);
        admin_u->complete_time = spdk_get_ticks() - admin_u->start_time;
        admin_u->cpl_cdw0  = variable_assignment; 
        admin_u->cpl_rsvd1 = variable_assignment; 
        admin_u->cpl_sqhd  = variable_assignment; 
        admin_u->cpl_sqid  = variable_assignment; 
        admin_u->cpl_cid   = variable_assignment; 
        admin_u->cpl_status.p = variable_assignment; 
        admin_u->cpl_status.sc = variable_assignment; 
        admin_u->cpl_status.sct = variable_assignment; 
        admin_u->cpl_status.rsvd2 = variable_assignment;
        admin_u->cpl_status.m = variable_assignment;
        admin_u->cpl_status.dnr = variable_assignment; 
        admin_u->cmd_status = XT_CMD_UNIT_COMPLETED;
        cmds_u_rpush(admin_u->completed_cmds_u_ring, admin_u);
    }
    return 0;
}

static void null_engines_device_destory(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("null engines: device destory return directly\n");
}

static int null_engines_nvme_init(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("null engines: nvme init return 0 directly\n");
    return 0;
}

static int null_engines_nvme_fini(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("null engines: nvme fini return directly\n");
    return 0;
}

static xt_engine_ops xt_unused null_engine_ops = {
    .name                                              = "null",
    .version                                           = XT_IOOPS_VERSION,
    .io_sync_flag                                      = 0,
    .admin_sync_flag                                   = 1,
    .xt_engine_env_init                                = null_engines_env_init,
    .xt_engine_env_fini                                = null_engines_env_fini,
    .xt_engine_device_destory                          = null_engines_device_destory,
    .xt_engine_device_init                             = null_engines_nvme_init,
    .xt_engine_device_fini                             = null_engines_nvme_fini,
    .xt_engine_qpair_create                            = null_engines_qpair_create,
    .xt_engine_qpair_free                              = null_engines_qpair_free,
    .xt_engine_qpair_destroy                           = null_engines_qpair_destroy, 
    .xt_engine_completed_io_check                      = null_engines_completed_io_check,
    .xt_engine_prepare_io_unit                         = null_engines_prepare_io_unit,
    .xt_engine_submit_io_cmd                           = null_engines_submit_io_cmd,
    .xt_engine_wait_completion_io                      = null_engines_wait_completion_io,
    .xt_engine_wait_qpair_all_submission_io_completion = null_engines_wait_qpair_all_submission_io_completion,
    .xt_engines_completed_admin_check                  = null_engines_completed_admin_check,
    .xt_engine_prepare_admin_unit                      = null_engines_prepare_admin_unit,
    .xt_engine_submit_admin_cmd                        = null_engines_submit_admin_cmd,
    .xt_engine_wait_completion_admin                   = null_engines_wait_completion_admin,
};

static void xt_init xt_null_register(void){
	xt_register_engine(&null_engine_ops);
}
