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
SPDK_LOG_REGISTER_COMPONENT("io_ctrl_nvme", XT_IO_CTRL_NVME_LOG)
extern xt_commands_logger* g_xt_cmd_log;
extern uint64_t g_tsc_rate;
extern int  g_pid;
extern int g_shmid;

static int io_ctrl_nvme_engines_env_init(xt_admin_qpair *aqinfo){
    aqinfo->submit_cmds_u_ring = malloc(sizeof(cmds_u_ring));
    cmds_u_rinit(aqinfo->submit_cmds_u_ring, aqinfo->qpair_iodepth);
    SPDK_INFOLOG(XT_NULL_LOG,"io_ctrl_nvme engine create admin qpair: submit_cmds_u_ring %p\n", aqinfo->submit_cmds_u_ring);
    return 0;
}

static int io_ctrl_nvme_engines_env_fini(xt_admin_qpair *aqinfo){
    cmds_u_rexit(aqinfo->submit_cmds_u_ring);
    free(aqinfo->submit_cmds_u_ring);
    SPDK_INFOLOG(XT_NULL_LOG,"io_ctrl_nvme engine free admin qpair: submit_cmds_u_ring %p;\n",aqinfo->submit_cmds_u_ring);
    return 0;
}

static int io_ctrl_nvme_engines_qpair_create(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, int qprio, int qdepth){
    qinfo->qpair = NULL;
    qinfo->submit_cmds_u_ring = malloc(sizeof(cmds_u_ring));
    cmds_u_rinit(qinfo->submit_cmds_u_ring, qdepth);
    SPDK_INFOLOG(XT_NULL_LOG,"io_ctrl_nvme engine create io qpair: submit_cmds_u_ring %p;\n", qinfo->submit_cmds_u_ring);
    return 0;
}

static int io_ctrl_nvme_engines_qpair_free(xt_io_qpair *qinfo){
    cmds_u_rexit(qinfo->submit_cmds_u_ring);
    free(qinfo->submit_cmds_u_ring);
    SPDK_INFOLOG(XT_NULL_LOG,"io_ctrl_nvme engine free io qpair: submit_cmds_u_ring %p;\n",qinfo->submit_cmds_u_ring);
    return 0;
}

static void io_ctrl_nvme_engines_qpair_destroy(xt_io_qpair *qinfo){
    SPDK_INFOLOG(XT_NULL_LOG,"io_ctrl_nvme engine return directly \n");
}

bool io_ctrl_nvme_engines_completed_io_check(cmds_u* io_u){
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

static cmds_u *io_ctrl_nvme_engines_prepare_io_unit(xt_io_qpair *qinfo){
    cmds_u * io_unit;
    io_unit = cmds_u_rpop(qinfo->completed_cmds_u_ring);
    if (NULL == io_unit){
        SPDK_ERRLOG("Get io unit is NULL \n");
        assert(0);
    }
    return io_unit;
}

static void io_ctrl_nvme_engines_submit_io_cmd(xt_io_qpair *qinfo, xt_buffer *buf, cmds_u *io_unit, unsigned int length, unsigned int lbacnt){
    void * buffer =  (buf->buf + io_unit->xt_buffer_offset);
    unsigned long long offset = io_unit->cdw11;
    offset = (offset << 32 | io_unit->cdw10) * (io_unit->sector_size + io_unit->meta_sector_size);
    if (io_unit->opc == 1 && io_unit->io_tailer_flag){
        xt_io_tailer_prepare(buf, io_unit, buffer, lbacnt);
    }
    if(io_unit->opc == 2)
        *((unsigned long long *)buffer) = XT_MAGIC_NUMBER;
    qinfo->submit_count ++;
    io_unit->addr = (unsigned long long)buffer;
    io_unit->data_len = lbacnt * io_unit->sector_size;
    io_unit->issue_time = spdk_get_ticks(); 
    io_unit->rc = ioctl(qinfo->fid, NVME_IOCTL_IO64_CMD, (struct nvme_passthru_cmd64 *)io_unit);
    io_unit->complete_time = spdk_get_ticks() - io_unit->issue_time;
    if (qinfo->microseconds_delay){
        spdk_delay_us(qinfo->microseconds_delay);
    }
    if(io_unit->rc < 0){
        SPDK_ERRLOG("submit io command failed with %p rc %d  fid %d \n", io_unit, io_unit->rc, qinfo->fid);
        cmds_u_rpush(io_unit->completed_cmds_u_ring, io_unit);
    }else{
        io_ctrl_nvme_engines_completed_io_check(io_unit);
        xt_io_completed_recover_update(qinfo, io_unit, lbacnt);
    }
}

static int io_ctrl_nvme_engines_wait_completion_io(xt_io_qpair *qinfo, unsigned int max_completions){
    return 0;
}

static int io_ctrl_nvme_engines_wait_qpair_all_submission_io_completion(xt_io_qpair *qinfo){
    return 0;
}

bool io_ctrl_nvme_engines_completed_admin_check(cmds_u* _cmds_u){
    _cmds_u->cmd_status = XT_CMD_UNIT_FREE;
    return true;    
}

cmds_u *io_ctrl_nvme_engines_prepare_admin_unit(xt_admin_qpair *aqinfo){
    cmds_u * _cmds_u;
    _cmds_u = cmds_u_rpop(aqinfo->completed_cmds_u_ring);
    if (NULL == _cmds_u){
        SPDK_ERRLOG("Get io unit is NULL \n");
        assert(0);
    }
    return _cmds_u;
}

void io_ctrl_nvme_engines_submit_admin_cmd(xt_admin_qpair *aqinfo, xt_buffer *buf, cmds_u *admin_unit, unsigned int length){
    void * buffer = (buf->buf + admin_unit->xt_buffer_offset);
    admin_unit->addr = (unsigned long long)buffer;
    admin_unit->data_len = length;
    admin_unit->issue_time = spdk_get_ticks(); 
    admin_unit->rc = ioctl(aqinfo->device_info.admin_handle_id, NVME_IOCTL_ADMIN64_CMD, (struct nvme_passthru_cmd64 *)admin_unit);
    admin_unit->complete_time = spdk_get_ticks() - admin_unit->issue_time;
    if(admin_unit->rc < 0){
        SPDK_ERRLOG("submit amdin failed and return %d \n", admin_unit->rc);
    }else{
        admin_unit->cmd_status = XT_CMD_UNIT_COMPLETED;
        io_ctrl_nvme_engines_completed_admin_check(admin_unit);
    }
    cmds_u_rpush(admin_unit->completed_cmds_u_ring, admin_unit);
}

int io_ctrl_nvme_engines_wait_completion_admin(xt_admin_qpair *aqinfo){
    return 0;
}

static void io_ctrl_nvme_engines_device_destory(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("io_ctrl_nvme engines: device destory return directly\n");
}

static int io_ctrl_nvme_engines_nvme_init(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("io_ctrl_nvme engines: nvme init return 0 directly char_device_name %s admin_handle_id %d\n", aqinfo->device_info.char_device_name, aqinfo->device_info.admin_handle_id);
    return 0;
}

static int io_ctrl_nvme_engines_nvme_fini(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("io_ctrl_nvme engines: nvme fini return directly\n");
    return 0;
}

static xt_engine_ops xt_unused io_ctrl_nvme_engine_ops = {
    .name                                              = "ioctrl_nvme",
    .version                                           = XT_IOOPS_VERSION,
    .io_sync_flag                                      = 1,
    .admin_sync_flag                                   = 1,
    .xt_engine_env_init                                = io_ctrl_nvme_engines_env_init,
    .xt_engine_env_fini                                = io_ctrl_nvme_engines_env_fini,
    .xt_engine_device_destory                          = io_ctrl_nvme_engines_device_destory,
    .xt_engine_device_init                             = io_ctrl_nvme_engines_nvme_init,
    .xt_engine_device_fini                             = io_ctrl_nvme_engines_nvme_fini,
    .xt_engine_qpair_create                            = io_ctrl_nvme_engines_qpair_create,
    .xt_engine_qpair_free                              = io_ctrl_nvme_engines_qpair_free,
    .xt_engine_qpair_destroy                           = io_ctrl_nvme_engines_qpair_destroy, 
    .xt_engine_completed_io_check                      = io_ctrl_nvme_engines_completed_io_check,
    .xt_engine_prepare_io_unit                         = io_ctrl_nvme_engines_prepare_io_unit,
    .xt_engine_submit_io_cmd                           = io_ctrl_nvme_engines_submit_io_cmd,
    .xt_engine_wait_completion_io                      = io_ctrl_nvme_engines_wait_completion_io,
    .xt_engine_wait_qpair_all_submission_io_completion = io_ctrl_nvme_engines_wait_qpair_all_submission_io_completion,
    .xt_engines_completed_admin_check                  = io_ctrl_nvme_engines_completed_admin_check,
    .xt_engine_prepare_admin_unit                      = io_ctrl_nvme_engines_prepare_admin_unit,
    .xt_engine_submit_admin_cmd                        = io_ctrl_nvme_engines_submit_admin_cmd,
    .xt_engine_wait_completion_admin                   = io_ctrl_nvme_engines_wait_completion_admin,
};

static void xt_init xt_io_ctrl_nvme_register(void)
{
	xt_register_engine(&io_ctrl_nvme_engine_ops);
}
