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
#include "xt_cmds_log.h"

extern xt_commands_logger* g_xt_cmd_log;
extern uint64_t g_tsc_rate;
extern int  g_pid;
extern int g_shmid;
static struct timeval sstime;
static struct timeval basetime;

static void print_io_status_per_second(void){
    unsigned long long base_write_size = 0;
    unsigned long long base_read_size = 0;
    unsigned long long base_iops = 0;
    double write_speed = 0;
    double read_speed = 0;
    double iops_speed = 0;
    long long t_time;
    int sleep_count = 0;
    double take_time;
    while (g_xt_cmd_log->cmds_log_header.total_write_size == 0 && g_xt_cmd_log->cmds_log_header.total_read_size ==0)
    {
        sleep(1);
    }
    gettimeofday(&basetime, NULL);
    base_write_size = g_xt_cmd_log->cmds_log_header.total_write_size;
    base_read_size = g_xt_cmd_log->cmds_log_header.total_read_size;
    while(true){
        if ((g_xt_cmd_log->cmds_log_header.total_write_size - base_write_size > XT_GB_BYTES) || (g_xt_cmd_log->cmds_log_header.total_read_size - base_read_size > XT_GB_BYTES) || sleep_count > 300){
            gettimeofday(&sstime, NULL);
            t_time =1000000 * ( sstime.tv_sec - basetime.tv_sec ) + sstime.tv_usec - basetime.tv_usec;
            take_time = t_time / 1000000;
            write_speed = (g_xt_cmd_log->cmds_log_header.total_write_size - base_write_size) / XT_MB_BYTES / take_time;
            read_speed = (g_xt_cmd_log->cmds_log_header.total_read_size - base_read_size) / XT_MB_BYTES / take_time;
            iops_speed = (g_xt_cmd_log->cmds_log_header.total_iops_count - base_iops) / take_time;
            if(g_xt_cmd_log->cmds_log_header.ioprint_thread_flag)
                printf("this case current IOPS count %-10.2f/s write data 0x%-16llx * 512  current speed is %-6.2fM/s   this case current read data 0x%-16llx * 512   current speed is %-6.2fM/s   take time %-3.2f \n", 
                        iops_speed, g_xt_cmd_log->cmds_log_header.total_write_size, write_speed, g_xt_cmd_log->cmds_log_header.total_read_size, read_speed, take_time);
            base_write_size = g_xt_cmd_log->cmds_log_header.total_write_size;
            base_read_size = g_xt_cmd_log->cmds_log_header.total_read_size;
            base_iops = g_xt_cmd_log->cmds_log_header.total_iops_count;
            gettimeofday(&basetime, NULL);
            sleep_count = 0;
        }
        else{
            sleep(1);
            sleep_count++;
            if(base_read_size == g_xt_cmd_log->cmds_log_header.total_read_size && base_write_size == g_xt_cmd_log->cmds_log_header.total_write_size){
                gettimeofday(&basetime, NULL);
            }
        }
    }
}

void start_io_print_thread(void){
    g_xt_cmd_log->cmds_log_header.ioprint_thread_flag = 1;
    sleep(1);
    if (g_xt_cmd_log->cmds_log_header.ioprint_thread_create_flag == 0){
        pthread_create(&g_xt_cmd_log->cmds_log_header.ioprint_thread, NULL, (void *)&print_io_status_per_second, NULL);
        g_xt_cmd_log->cmds_log_header.ioprint_thread_create_flag = 1;
    }
    SPDK_NOTICELOG("start io print. \n");
}

void stop_io_print_thread(void){
    g_xt_cmd_log->cmds_log_header.ioprint_thread_flag = 0;
    sleep(1);
    SPDK_NOTICELOG("stop io print \n");
}



