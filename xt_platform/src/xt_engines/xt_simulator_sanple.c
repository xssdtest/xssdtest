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


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// the common data structure definition with simulator and xssdtest interface
//
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

static bool simulator_engines_completed_io_check(cmds_u* io_u){
	return 0;
}

static cmds_u *simulator_engines_prepare_io_unit(xt_io_qpair *qinfo){
	return NULL;
}


static int simulator_engines_wait_completion_io(xt_io_qpair *qinfo, unsigned int max_completions){
	return 0;
}

static void simulator_engines_submit_io_cmd(xt_io_qpair *qinfo, xt_buffer *buf, cmds_u *io_unit, unsigned int length, unsigned int lbacnt){
}

static int simulator_engines_wait_qpair_all_submission_io_completion(xt_io_qpair *qinfo){
    return 0;
}


static bool simulator_engines_completed_admin_check(cmds_u* _cmds_u){
    return true;
}

static cmds_u *simulator_engines_prepare_admin_unit(xt_admin_qpair *aqinfo){
    return NULL;
}

static void simulator_engines_submit_admin_cmd(xt_admin_qpair *aqinfo, xt_buffer *buf, cmds_u *admin_unit, unsigned int length){
}

static int simulator_engines_env_init(xt_admin_qpair *aqinfo){
    return 0;
}

static int simulator_engines_env_fini(xt_admin_qpair *aqinfo){
  return 0;
}


static void simulator_engines_device_destory(xt_admin_qpair *aqinfo){
}

static int simulator_engines_nvme_init(xt_admin_qpair *aqinfo){
    return 0;
}

static int simulator_engines_nvme_fini(xt_admin_qpair *aqinfo){
    return 0;
}


static int simulator_engines_qpair_create(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, int qprio, int qdepth){
    return 0;
}

static int simulator_engines_qpair_free(xt_io_qpair *qinfo){
    return 0;
}


static void simulator_engines_qpair_destroy(xt_io_qpair *qinfo){
}

static int simulator_engines_wait_completion_admin(xt_admin_qpair *aqinfo){
	return 0;
}

static xt_engine_ops xt_unused simulator_engine_ops = {
    .name                                              = "simulator_nvme_xssdtest",
    .version                                           = XT_IOOPS_VERSION,
    .io_sync_flag                                      = 0,
    .admin_sync_flag                                   = 0,
    .xt_engine_env_init                                = simulator_engines_env_init,
    .xt_engine_env_fini                                = simulator_engines_env_fini,
    .xt_engine_device_destory                          = simulator_engines_device_destory,
    .xt_engine_device_init                             = simulator_engines_nvme_init,
    .xt_engine_device_fini                             = simulator_engines_nvme_fini,
    .xt_engine_qpair_create                            = simulator_engines_qpair_create,
    .xt_engine_qpair_free                              = simulator_engines_qpair_free,
    .xt_engine_qpair_destroy                           = simulator_engines_qpair_destroy,
    .xt_engine_completed_io_check                      = simulator_engines_completed_io_check,
    .xt_engine_prepare_io_unit                         = simulator_engines_prepare_io_unit,
    .xt_engine_submit_io_cmd                           = simulator_engines_submit_io_cmd,
    .xt_engine_wait_completion_io                      = simulator_engines_wait_completion_io,
    .xt_engine_wait_qpair_all_submission_io_completion = simulator_engines_wait_qpair_all_submission_io_completion,
    .xt_engines_completed_admin_check                  = simulator_engines_completed_admin_check,
    .xt_engine_prepare_admin_unit                      = simulator_engines_prepare_admin_unit,
    .xt_engine_submit_admin_cmd                        = simulator_engines_submit_admin_cmd,
    .xt_engine_wait_completion_admin                   = simulator_engines_wait_completion_admin,
};

static void xt_init xt_simulator_nvme_register(void){
	xt_register_engine(&simulator_engine_ops);
}