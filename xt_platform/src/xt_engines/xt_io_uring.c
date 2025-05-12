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



static xt_engine_ops xt_unused io_uring_nvme_engine_ops = {
    .name                                              = "io_uring_nvme_tbd",
    .version                                           = XT_IOOPS_VERSION,
    .io_sync_flag                                      = 0,
    .admin_sync_flag                                   = 1,
    .xt_engine_env_init                                = NULL,
    .xt_engine_env_fini                                = NULL,
    .xt_engine_device_destory                          = NULL,
    .xt_engine_device_init                             = NULL,
    .xt_engine_device_fini                             = NULL,
    .xt_engine_qpair_create                            = NULL,
    .xt_engine_qpair_free                              = NULL,
    .xt_engine_qpair_destroy                           = NULL, 
    .xt_engine_completed_io_check                      = NULL,
    .xt_engine_prepare_io_unit                         = NULL,
    .xt_engine_submit_io_cmd                           = NULL,
    .xt_engine_wait_completion_io                      = NULL,
    .xt_engine_wait_qpair_all_submission_io_completion = NULL,
    .xt_engines_completed_admin_check                  = NULL,
    .xt_engine_prepare_admin_unit                      = NULL,
    .xt_engine_submit_admin_cmd                        = NULL,
    .xt_engine_wait_completion_admin                   = NULL,
};

static void xt_init xt_io_uring_nvme_register(void){
	xt_register_engine(&io_uring_nvme_engine_ops);
}
