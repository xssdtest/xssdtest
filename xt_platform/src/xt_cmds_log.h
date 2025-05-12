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
#ifndef XT_COMMANDS_LOGGER_H
#define XT_COMMANDS_LOGGER_H
#include <sys/time.h>
#include "spdk/stdinc.h"
#include "spdk_internal/log.h"
#include "xt_compiler/xt_compiler.h"

#ifndef XT_CMD_LOG_ENTRY_SIZE
#define XT_CMD_LOG_ENTRY_SIZE	128
#endif
#ifndef XT_MB_BYTES
#define XT_MB_BYTES	            1048576
#endif
#ifndef XT_GB_BYTES
#define XT_GB_BYTES             1073741824
#endif

typedef struct _xt_commands_logger{
    union
    {
        unsigned char raw[1024];
        struct
        {
            unsigned long long total_read_size;
            unsigned long long total_write_size;
            unsigned long long total_iops_count;
            unsigned long long total_io_size;
            pthread_t ioprint_thread;
            unsigned int ioprint_thread_flag;
            unsigned int ioprint_thread_create_flag;
            int shm_id;
            unsigned int pid;
            pthread_mutex_t log_lock;
            unsigned int cmds_log_header;
            unsigned int cmds_log_tailer;
            unsigned int cmds_log_count;
        };
    }cmds_log_header;
    unsigned char * command_log_rings[XT_CMD_LOG_ENTRY_SIZE];

}xt_commands_logger;

typedef struct _xt_io_second_speed{
    unsigned int read_second_speed;
    unsigned int write_second_speed;
}xt_io_second_speed;

typedef struct _xt_io_speed{
    struct timeval start_time;
    unsigned long long run_time;
    unsigned long long io_speed_count;
    unsigned int avg_msec;
    unsigned int reserved;
    xt_io_second_speed *ios_second_speed;
}xt_io_speed;

extern void start_io_print_thread(void);

extern void stop_io_print_thread(void);
#endif