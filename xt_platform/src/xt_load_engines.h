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
#ifndef XT_LOAD_ENGINES_H
#define XT_LOAD_ENGINES_H
#include "spdk/stdinc.h"
#include "xt_compiler/xt_compiler.h"
#include "xt_include/xt_flist.h"

#define XT_ENGINE_NAME_SIZE 32
#define XT_ENGINE_NAME_COUNT 64

typedef struct _cmds_u cmds_u;
typedef struct _cmds_u_ring cmds_u_ring;
typedef struct _xt_engine_ops xt_engine_ops;
typedef struct _xt_admin_qpair xt_admin_qpair;
typedef struct _xt_io_qpair xt_io_qpair;
typedef struct _xt_buffer xt_buffer;
typedef struct _xt_commands_logger xt_commands_logger;

typedef struct _xt_engine_ops {
    struct flist_head list;
	const char *name;
	int version;
    unsigned int io_sync_flag;
    unsigned int admin_sync_flag;
    int (*xt_engine_env_init)(xt_admin_qpair *);
    int (*xt_engine_env_fini)(xt_admin_qpair *);
    void (*xt_engine_device_destory)(xt_admin_qpair *);
    int (*xt_engine_device_init)(xt_admin_qpair *);
    int (*xt_engine_device_fini)(xt_admin_qpair *);
    int (*xt_engine_qpair_create)(xt_admin_qpair *, xt_io_qpair *, int , int );
    int (*xt_engine_qpair_free)(xt_io_qpair *);
    void (*xt_engine_qpair_destroy)(xt_io_qpair *);
    bool (*xt_engine_completed_io_check)(cmds_u* );
    cmds_u *(*xt_engine_prepare_io_unit)(xt_io_qpair *);
    void (*xt_engine_submit_io_cmd)(xt_io_qpair *, xt_buffer *, cmds_u *, unsigned int, unsigned int);
    int (*xt_engine_wait_completion_io)(xt_io_qpair *, unsigned int );
    int (*xt_engine_wait_qpair_all_submission_io_completion)(xt_io_qpair *);
    bool (*xt_engines_completed_admin_check)(cmds_u* );   
    cmds_u *(*xt_engine_prepare_admin_unit)(xt_admin_qpair *);
    void (*xt_engine_submit_admin_cmd)(xt_admin_qpair *, xt_buffer *, cmds_u *, unsigned int );
    int (*xt_engine_wait_completion_admin)(xt_admin_qpair *);
}xt_engine_ops;

typedef struct _xt_engines{
    char engine_names[XT_ENGINE_NAME_COUNT][XT_ENGINE_NAME_SIZE];
    unsigned int engines_count;
    unsigned int index;
}xt_engines;

extern xt_engines g_engines_list;

extern void xt_register_engine(xt_engine_ops *engine_ops);

extern xt_engine_ops *xt_find_engine(const char *name);

extern char* get_engine_names(void);

extern unsigned int reload_engine_check(const char *src_engine, const char *dest_engine);

#endif