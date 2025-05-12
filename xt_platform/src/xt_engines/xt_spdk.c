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
SPDK_LOG_REGISTER_COMPONENT("spdk", XT_SPDK_LOG)

struct cb_ctx {
  struct spdk_nvme_transport_id* trid;
  struct spdk_nvme_ctrlr* ctrlr;
};

struct ctrlr_entry {
  struct spdk_nvme_ctrlr  *ctrlr;
  STAILQ_ENTRY(ctrlr_entry) next;
};

STAILQ_HEAD(, ctrlr_entry) g_controllers = STAILQ_HEAD_INITIALIZER(g_controllers);

static bool spdk_engines_completed_io_check(cmds_u* io_u){
    xt_io_qpair *qinfo = io_u->qpair_info;
    unsigned int io_check_type = qinfo->io_check_type;
    bool check_status = true;
    /*  0 not check;  bit 1 check status code and status code type; */
    /*  bit 2 read command check data include empty buffer  */
    /*  bit 3 read command check data with excepted write buffer  */
    /*  bit 4 read command check data with buffer tailer  */
    /*  bit 5 read command only check buffer tailer (quickly performance check)*/
    /*  other bits resevered*/
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

static cmds_u *spdk_engines_prepare_io_unit(xt_io_qpair *qinfo)
{
    cmds_u * io_unit;
    io_unit = xt_prepare_io_unit_with_engine(qinfo);
    if (NULL == io_unit){
        SPDK_ERRLOG("Get io unit is NULL \n");
        assert(0);
    }
    return io_unit;
}

static void get_io_cmd_completion(void *cb_arg, const struct spdk_nvme_cpl *cpl){
    cmds_u *io_u = (cmds_u *)cb_arg;
    xt_io_qpair *qinfo = io_u->qpair_info; 
    unsigned int block_size;
    // io_u->complete_time = spdk_get_ticks() - io_u->start_time;
    io_u->complete_time = spdk_get_ticks() - io_u->issue_time;
    io_u->cpl_cdw0  = cpl->cdw0;
    io_u->cpl_rsvd1 = cpl->rsvd1;
    io_u->cpl_sqhd  = cpl->sqhd;
    io_u->cpl_sqid  = cpl->sqid;
    io_u->cpl_cid   = cpl->cid;
    io_u->cpl_status.p = cpl->status.p;
    io_u->cpl_status.sc = cpl->status.sc;
    io_u->cpl_status.sct = cpl->status.sct;
    io_u->cpl_status.rsvd2 = cpl->status.rsvd2;
    io_u->cpl_status.m = cpl->status.m;
    io_u->cpl_status.dnr = cpl->status.dnr; 
    block_size = (io_u->cdw12 & 0xFFFF) + 1;
    xt_io_completed_recover_update(qinfo, io_u, block_size);
    // SPDK_NOTICELOG("qpair_completions in spdk: %lld \n", qinfo->qpair_completions);
}

static int spdk_engines_wait_qpair_all_submission_io_completion(xt_io_qpair *qinfo){
    // SPDK_NOTICELOG("init submit_count: 0x%lx  last_submit_count: 0x%lx qpair_completions: 0x%lx \n", qinfo->submit_count, qinfo->last_submit_count, qinfo->qpair_completions);
    cmds_u * io_u;
    if (qinfo->submit_count - qinfo->last_submit_count != qinfo->qpair_completions){
        unsigned long long init_tick;
        unsigned long long totaltimeout = qinfo->timeout * qinfo->current_iodepth_count;
        init_tick = spdk_get_ticks();
        unsigned int completed_check_index = qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1);
        while (spdk_get_ticks() - init_tick < totaltimeout){
            spdk_nvme_qpair_process_completions(qinfo->qpair, 0);
            if (qinfo->submit_count - qinfo->last_submit_count == qinfo->qpair_completions){
                break;
            }
            if (NULL != qinfo->completed_cmds_u_ring->ring[completed_check_index] && 
                qinfo->completed_cmds_u_ring->ring[completed_check_index]->cmd_status == XT_CMD_UNIT_COMPLETED ){
                spdk_engines_completed_io_check(qinfo->completed_cmds_u_ring->ring[completed_check_index]);
                completed_check_index = qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1);
            }
        }
        if (qinfo->submit_count - qinfo->last_submit_count != qinfo->qpair_completions){
            SPDK_ERRLOG("wait all command timeout, submission count %lld, completed count %lld\n ",(qinfo->submit_count - qinfo->last_submit_count), qinfo->qpair_completions);
            assert(0);
        }
        // SPDK_NOTICELOG("totaltimeout: 0x%llx qinfo->timeout: 0x%llx qinfo->current_iodepth_count: 0x%llx totaltimeout:0x%llx \n", totaltimeout, qinfo->timeout, qinfo->current_iodepth_count, qinfo->timeout * qinfo->current_iodepth_count);
        // SPDK_NOTICELOG("init submit_count: 0x%lx  last_submit_count: 0x%lx qpair_completions: 0x%lx timeout:0x%lx current_iodepth_count: %lx\n", qinfo->submit_count, qinfo->last_submit_count, qinfo->qpair_completions, qinfo->timeout, qinfo->current_iodepth_count);
        // SPDK_NOTICELOG("submit_count: 0x%lx  last_submit_count: 0x%lx qpair_completions: 0x%lx\n", qinfo->submit_count, qinfo->last_submit_count, qinfo->qpair_completions);
        // SPDK_NOTICELOG("qinfo->completed_cmds_u_ring->head: %d\n", qinfo->completed_cmds_u_ring->head);
        // SPDK_NOTICELOG("qinfo->completed_cmds_u_ring->ring[qinfo->completed_cmds_u_ring->head]: %p\n", qinfo->completed_cmds_u_ring->ring[qinfo->completed_cmds_u_ring->head]);
        // SPDK_NOTICELOG("qinfo->completed_cmds_u_ring->head: %d command status %d \n", qinfo->completed_cmds_u_ring->head, qinfo->completed_cmds_u_ring->ring[qinfo->completed_cmds_u_ring->head]->cmd_status);
        // while ((qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1)) != qinfo->completed_cmds_u_ring->head){
        //     spdk_engines_completed_io_check(qinfo->completed_cmds_u_ring->ring[qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1)]);
        //     // SPDK_NOTICELOG("last completed_check_index: %d command status %d \n", (qinfo->completed_check_index - 1) & (qinfo->completed_cmds_u_ring->max - 1), qinfo->completed_cmds_u_ring->ring[(qinfo->completed_check_index - 1) & (qinfo->completed_cmds_u_ring->max - 1)]->cmd_status);
        //     // SPDK_NOTICELOG("completed_check_index: %d command status %d \n", qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1), qinfo->completed_cmds_u_ring->ring[qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1)]->cmd_status);
        //     // spdk_delay_us(100000);
        // }
        // if(NULL != qinfo->completed_cmds_u_ring->ring[qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1)]){
        //     spdk_engines_completed_io_check(qinfo->completed_cmds_u_ring->ring[qinfo->completed_check_index & (qinfo->completed_cmds_u_ring->max - 1)]);
        // }
        io_u = cmds_u_get_ring_next( qinfo->completed_cmds_u_ring, true);
        while(io_u){
            if(io_u->cmd_status == XT_CMD_UNIT_COMPLETED){
                spdk_engines_completed_io_check(io_u);
            }
            io_u = cmds_u_get_ring_next(qinfo->completed_cmds_u_ring, false);
        }
        // SPDK_NOTICELOG("completed_check_index: %d head %d \n", qinfo->completed_check_index, qinfo->completed_cmds_u_ring->head);
    }else{
        io_u = cmds_u_get_ring_next( qinfo->completed_cmds_u_ring, true);
        while(io_u){
            if(io_u->cmd_status == XT_CMD_UNIT_COMPLETED){
                spdk_engines_completed_io_check(io_u);
            }
            io_u = cmds_u_get_ring_next(qinfo->completed_cmds_u_ring, false);
        }
    }
    qinfo->last_submit_count = qinfo->submit_count;
    qinfo->qpair_completions = 0;
    return true;
}

static void spdk_engines_submit_io_cmd(xt_io_qpair *qinfo, xt_buffer *buf, cmds_u *io_unit, unsigned int length, unsigned int lbacnt){
    void * buffer = (buf->buf + io_unit->xt_buffer_offset);
    // struct spdk_nvme_cmd * cmds = (struct spdk_nvme_cmd *)io_unit;
    if (io_unit->opc == 1 && io_unit->io_tailer_flag){
        xt_io_tailer_prepare(buf, io_unit, buffer, lbacnt);
    }
    if(io_unit->opc == 2)
        *((unsigned long long *)buffer) = XT_MAGIC_NUMBER;
    qinfo->submit_count ++;
    io_unit->issue_time = spdk_get_ticks(); 
    // SPDK_NOTICELOG("io_unit data: opc 0x%x nsid 0x%x cdw2 0x%x cdw3 0x%x  cdw4-5 0x%lx cdw6-7 0x%lx  cdw8-9 0x%lx cdw10 0x%lx cdw11 0x%x cdw12 0x%x cdw13 0x%x cdw14 0x%x cdw15 0x%x\n",
    //                 io_unit->opc, io_unit->nsid, io_unit->cdw2, io_unit->cdw3, io_unit->mptr, io_unit->prp1, io_unit->prp2, io_unit->cdw10, io_unit->cdw11, io_unit->cdw12, io_unit->cdw13,
    //                 io_unit->cdw14, io_unit->cdw15);
    // unsigned long long index = 0;
    // unsigned long long init_tick = 0;
    // unsigned long long timeout = spdk_get_ticks_hz() * 100000000;
    // while (1)
    // {
    //     index += 1;
    //     io_unit->rc = spdk_nvme_ctrlr_cmd_io_raw(qinfo->aqinfo->ctrlr, qinfo->qpair, (struct spdk_nvme_cmd *)io_unit, buffer, length, get_io_cmd_completion, io_unit);
    //     if(index % 1024 == 0){
    //         init_tick = spdk_get_ticks();
    //         while (spdk_get_ticks() - init_tick < timeout){
    //             spdk_nvme_qpair_process_completions(qinfo->qpair, 0);
    //             if (qinfo->submit_count - qinfo->last_submit_count == qinfo->qpair_completions){
    //                 qinfo->last_submit_count = qinfo->submit_count;
    //                 qinfo->qpair_completions = 0;
    //                 break;
    //             }
    //         }
    //         if (qinfo->submit_count - qinfo->last_submit_count != qinfo->qpair_completions){
    //             SPDK_NOTICELOG("qinfo->submit_count 0x%x qinfo->last_submit_count 0x%x qinfo->qpair_completions 0x%x\n", qinfo->submit_count, qinfo->last_submit_count, qinfo->qpair_completions);
    //         }
    //     }
    // }
    if(buf->io_tracker != NULL && io_unit->xt_buffer_offset == 0){
        io_unit->prp1 = (unsigned long long)buf->buf;
        io_unit->prp2 = (unsigned long long)buf->io_tracker;

    }
    io_unit->rc = spdk_nvme_ctrlr_cmd_io_raw(qinfo->aqinfo->ctrlr, qinfo->qpair, (struct spdk_nvme_cmd *)io_unit, buffer, length, get_io_cmd_completion, io_unit);
    if(io_unit->rc != 0){
        SPDK_ERRLOG("submit io command failed with %p\n", io_unit);
    }
    if (qinfo->microseconds_delay){
        spdk_delay_us(qinfo->microseconds_delay);
    }
}

static int spdk_engines_wait_completion_io(xt_io_qpair *qinfo, unsigned int max_completions){
    return spdk_nvme_qpair_process_completions(qinfo->qpair, max_completions);
}

static bool spdk_engines_completed_admin_check(cmds_u* _cmds_u){
    if ((_cmds_u->io_status_code_expected != _cmds_u->cpl_status.sc) | (_cmds_u->io_status_code_type_expected != _cmds_u->cpl_status.sct)){
        _cmds_u->cmd_status = XT_CMD_UNIT_FREE;
        return false;
    }
    return true;
}

static cmds_u *spdk_engines_prepare_admin_unit(xt_admin_qpair *aqinfo)
{
    cmds_u * _cmds_u;
    _cmds_u = xt_prepare_admin_unit_with_engine(aqinfo);
    if (NULL == _cmds_u){
        SPDK_ERRLOG("Get io unit is NULL \n");
        assert(0);
    }
    return _cmds_u;
}

static void get_admin_cmd_completion(void *cb_arg, const struct spdk_nvme_cpl *cpl)
{
    cmds_u *admin_u = (cmds_u *)cb_arg;
    admin_u->cpl_cdw0  = cpl->cdw0;
    admin_u->cpl_rsvd1 = cpl->rsvd1;
    admin_u->cpl_sqhd  = cpl->sqhd;
    admin_u->cpl_sqid  = cpl->sqid;
    admin_u->cpl_cid   = cpl->cid;
    admin_u->cpl_status.p = cpl->status.p;
    admin_u->cpl_status.sc = cpl->status.sc;
    admin_u->cpl_status.sct = cpl->status.sct;
    admin_u->cpl_status.rsvd2 = cpl->status.rsvd2;
    admin_u->cpl_status.m = cpl->status.m;
    admin_u->cpl_status.dnr = cpl->status.dnr; 
    admin_u->complete_time = spdk_get_ticks() - admin_u->start_time;
    admin_u->cmd_status = XT_CMD_UNIT_COMPLETED;
    cmds_u_rpush((cmds_u_ring *)admin_u->completed_cmds_u_ring, admin_u);
}


static void spdk_engines_submit_admin_cmd(xt_admin_qpair *aqinfo, xt_buffer *buf, cmds_u *admin_unit, unsigned int length){
    admin_unit->start_time = spdk_get_ticks(); 
    admin_unit->rc = spdk_nvme_ctrlr_cmd_admin_raw(aqinfo->ctrlr, (struct spdk_nvme_cmd *)admin_unit, (void *)(buf->buf + admin_unit->xt_buffer_offset), length, get_admin_cmd_completion, admin_unit);
    if(admin_unit->rc != 0){
        SPDK_ERRLOG("submit admin command failed with %p\n", admin_unit);
    }
}

static int spdk_engines_wait_completion_admin(xt_admin_qpair *aqinfo){
    return spdk_nvme_ctrlr_process_admin_completions(aqinfo->ctrlr);
}

static int spdk_engines_env_init(xt_admin_qpair *aqinfo){
    SPDK_NOTICELOG("spdk engine environment init\n");
    return 0;
}

static int spdk_engines_env_fini(xt_admin_qpair *aqinfo){
    /* clear global shared data */ 
    SPDK_NOTICELOG("spdk engine environment finish\n");
    if (spdk_process_is_primary()){
        spdk_env_fini();
    }
    return 0;
}

static void spdk_engines_device_destory(xt_admin_qpair *aqinfo){
    int ref = 0;
    spdk_pci_device_detach(aqinfo->pcie_info);
    ref = spdk_nvme_detach(aqinfo->ctrlr);
    if (ref == -1)
        SPDK_NOTICELOG("detach ctrl %p failed\n", aqinfo->ctrlr);
}

static bool probe_cb(void *cb_ctx, const struct spdk_nvme_transport_id *trid,
                     struct spdk_nvme_ctrlr_opts *opts)
{
    if (trid->trtype == SPDK_NVME_TRANSPORT_PCIE){
        struct spdk_nvme_transport_id* target = ((struct cb_ctx*)cb_ctx)->trid;
        if (0 != spdk_nvme_transport_id_compare(target, trid)){
            SPDK_NOTICELOG("Wrong address %s\n", trid->traddr);
            return false;
        }
        SPDK_INFOLOG(XT_SPDK_LOG,"attaching to pcie device: %s ctrlr %p \n", trid->traddr, ((struct cb_ctx*)cb_ctx)->ctrlr);
    }else{
        SPDK_INFOLOG(XT_SPDK_LOG,"attaching to NVMe over Fabrics controller at %s:%s: %s\n", trid->traddr, trid->trsvcid, trid->subnqn);
    }
    return true;
}

static void attach_cb(void *cb_ctx, const struct spdk_nvme_transport_id *trid,
                      struct spdk_nvme_ctrlr *ctrlr, const struct spdk_nvme_ctrlr_opts *opts)
{
    ((struct cb_ctx*)cb_ctx)->ctrlr = ctrlr;
    SPDK_INFOLOG(XT_SPDK_LOG,"Attached to %s ctrl address %p\n", trid->traddr, ctrlr);
}

static void remove_cb(void *cb_ctx, struct spdk_nvme_ctrlr *ctrlr)
{
    SPDK_INFOLOG(XT_SPDK_LOG,"probe function call remove call back %p \n", ctrlr);
	spdk_nvme_detach(ctrlr);
}


static void xt_unused timeout_cb(void *cb_arg, struct spdk_nvme_ctrlr *ctrlr, struct spdk_nvme_qpair *qpair, uint16_t cid)
{
	/* leave hotplug monitor loop, use the timeout_cb to monitor the hotplug */
	if (spdk_nvme_probe(NULL, NULL, probe_cb, attach_cb, remove_cb) != 0) {
		fprintf(stderr, "spdk_nvme_probe() failed\n");
	}
}

static struct spdk_nvme_ctrlr* nvme_probe(char *traddr)
{
    struct spdk_nvme_transport_id trid;
    struct cb_ctx cb_ctx;
    int rc = 0;
    memset(&trid, 0, sizeof(trid));
    spdk_nvme_trid_populate_transport(&trid, SPDK_NVME_TRANSPORT_PCIE);
    snprintf(trid.subnqn, sizeof(trid.subnqn), "%s", SPDK_NVMF_DISCOVERY_NQN);

    trid.trtype = SPDK_NVME_TRANSPORT_PCIE;
    strncpy(trid.traddr, traddr, SPDK_NVMF_TRADDR_MAX_LEN);

    cb_ctx.trid = &trid;
    cb_ctx.ctrlr = NULL;

    rc = spdk_nvme_probe(&trid, &cb_ctx, probe_cb, attach_cb, remove_cb);
    // cb_ctx.ctrlr = spdk_nvme_connect(&trid, NULL, 0);
    if (rc != 0 || cb_ctx.ctrlr == NULL){
        SPDK_ERRLOG("not found device: %s, rc %d, cb_ctx.ctrlr %p\n",trid.traddr, rc, cb_ctx.ctrlr);
        return NULL;
    }
    SPDK_NOTICELOG("nvme probe: %s, rc %d, cb_ctx.ctrlr %p\n",trid.traddr, rc, cb_ctx.ctrlr);
    SPDK_INFOLOG(XT_SPDK_LOG,"nvme probe: %s, rc %d, cb_ctx.ctrlr %p\n",trid.traddr, rc, cb_ctx.ctrlr);
    return cb_ctx.ctrlr;
} 

static int spdk_engines_nvme_init(xt_admin_qpair *aqinfo){
    struct spdk_nvme_ctrlr* ctrlr;
    spdk_log_set_flag("nvme");
    ctrlr = nvme_probe(aqinfo->traddr);
    if (ctrlr == NULL){
        SPDK_ERRLOG("Nvme probe failed in spdk engine: %s\n", aqinfo->traddr);
        return -1;
    }
    if (spdk_process_is_primary()){
        struct ctrlr_entry *entry;
        struct ctrlr_entry* tmp;
        STAILQ_FOREACH_SAFE(entry, &g_controllers, next, tmp){
            if(entry->ctrlr == ctrlr){
                aqinfo->ctrlr = ctrlr;
                return 0;
            }
        }
        entry = malloc(sizeof(struct ctrlr_entry));
        entry->ctrlr = ctrlr;
        spdk_nvme_ctrlr_register_aer_callback(ctrlr, NULL, NULL);
        STAILQ_INSERT_TAIL(&g_controllers, entry, next);
    }
    aqinfo->ctrlr = ctrlr;
    return 0;
}

static int spdk_engines_nvme_fini(xt_admin_qpair *aqinfo){
    struct spdk_nvme_qpair  *qpair;
    //spdk_nvme_probe(NULL, NULL, probe_cb, attach_cb, remove_cb);
    spdk_nvme_ctrlr_fail(aqinfo->ctrlr);
    TAILQ_FOREACH(qpair, &aqinfo->ctrlr->active_io_qpairs, tailq)
    {
        spdk_nvme_ctrlr_free_io_qpair(qpair);
        SPDK_INFOLOG(XT_SPDK_LOG,"free qpair: %d the address %p \n", qpair->id, qpair);
    }
    //remove ctrlr from list
    struct ctrlr_entry* e;
    struct ctrlr_entry* tmp;
    STAILQ_FOREACH_SAFE(e, &g_controllers, next, tmp){
        if (e->ctrlr == aqinfo->ctrlr){
            STAILQ_REMOVE(&g_controllers, e, ctrlr_entry, next);
            free(e);
            break;
        }
    }
    SPDK_INFOLOG(XT_SPDK_LOG,"Nvme detach %p \n", aqinfo->ctrlr);
//        spdk_pci_device_detach(pcie);
    return spdk_nvme_detach(aqinfo->ctrlr);

}

static int spdk_engines_qpair_create(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, int qprio, int qdepth){
    struct spdk_nvme_qpair *qpair;
    struct spdk_nvme_io_qpair_opts opts;
    memset(&opts, 0, sizeof(opts));
    opts.qprio = qprio;
    opts.io_queue_size = qdepth;
    opts.io_queue_requests = qdepth;
    opts.delay_pcie_doorbell = false;

    qpair = spdk_nvme_ctrlr_alloc_io_qpair(aqinfo->ctrlr, &opts, sizeof(opts));
    if (qpair == NULL) {
        SPDK_ERRLOG("create io qpair fail ctrlr %p \n", aqinfo->ctrlr);
        return -1;
    }

    // no need to abort commands in test
    qpair->no_deletion_notification_needed = 1;
    qinfo->qpair = qpair;
    qinfo->qpair_id = qpair->id;
    SPDK_INFOLOG(XT_SPDK_LOG,"created qpair %d %d\n", qpair->id, qpair->qprio);
    return 0;
}

static int spdk_engines_qpair_free(xt_io_qpair *qinfo){
    if ( NULL == qinfo->qpair) {
        SPDK_INFOLOG(XT_SPDK_LOG,"there's no qpair to be free\n");
        return 0;
    }
    SPDK_INFOLOG(XT_SPDK_LOG,"free qpair: %d the address %p \n", qinfo->qpair_id, qinfo->qpair);
    return spdk_nvme_ctrlr_free_io_qpair(qinfo->qpair);
}

static void spdk_engines_qpair_destroy(xt_io_qpair *qinfo){
    nvme_pcie_qpair_destroy(qinfo->qpair);
}

static xt_engine_ops xt_unused spdk_engine_ops = {
    .name                                              = "spdk_nvme",
    .version                                           = XT_IOOPS_VERSION,
    .xt_engine_env_init                                = spdk_engines_env_init,
    .xt_engine_env_fini                                = spdk_engines_env_fini,
    .xt_engine_device_destory                          = spdk_engines_device_destory,
    .xt_engine_device_init                             = spdk_engines_nvme_init,
    .xt_engine_device_fini                             = spdk_engines_nvme_fini,
    .xt_engine_qpair_create                            = spdk_engines_qpair_create,
    .xt_engine_qpair_free                              = spdk_engines_qpair_free,
    .xt_engine_qpair_destroy                           = spdk_engines_qpair_destroy, 
    .xt_engine_completed_io_check                      = spdk_engines_completed_io_check,
    .xt_engine_prepare_io_unit                         = spdk_engines_prepare_io_unit,
    .xt_engine_submit_io_cmd                           = spdk_engines_submit_io_cmd,
    .xt_engine_wait_completion_io                      = spdk_engines_wait_completion_io,
    .xt_engine_wait_qpair_all_submission_io_completion = spdk_engines_wait_qpair_all_submission_io_completion,
    .xt_engines_completed_admin_check                  = spdk_engines_completed_admin_check,
    .xt_engine_prepare_admin_unit                      = spdk_engines_prepare_admin_unit,
    .xt_engine_submit_admin_cmd                        = spdk_engines_submit_admin_cmd,
    .xt_engine_wait_completion_admin                   = spdk_engines_wait_completion_admin,
};

static void xt_init xt_spdk_nvme_register(void){
	xt_register_engine(&spdk_engine_ops);
}
