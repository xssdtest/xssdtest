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
#include "xt_io_qpair.h"
#include "xt_include/xt_spdk_interface.h"

void xt_io_qpair_init(xt_io_qpair *qinfo, unsigned int qpair_iodepth, cmds_u * io_units, cmds_u_ring * completed_cmds_u_ring, 
                      unsigned long long completed_check_index, unsigned long long submit_count, unsigned long long qpair_completions){
    if(NULL != qinfo){
        qinfo->qpair_iodepth = qpair_iodepth;
        qinfo->io_units = io_units;
        qinfo->completed_cmds_u_ring = completed_cmds_u_ring;
        qinfo->completed_check_index = completed_check_index;
        qinfo->submit_count = submit_count;
        qinfo->qpair_completions = qpair_completions;
    }else{
        SPDK_ERRLOG("Get a invalid io qpair: %p\n", qinfo);
    }
}

void xt_set_io_qpair_polling_status(xt_io_qpair *qinfo, xt_admin_qpair * aqinfo, int reap_type, unsigned int io_check_type, 
                                    unsigned int current_iodepth_count, unsigned long long timeout, unsigned long long limit_iops_count, 
                                    unsigned long long limit_io_count, unsigned int microseconds_delay){
    if(NULL != qinfo){
        qinfo->aqinfo = aqinfo;
        qinfo->reap_type = reap_type;
        qinfo->io_check_type = io_check_type;
        qinfo->current_iodepth_count = current_iodepth_count;
        qinfo->timeout = timeout;
        qinfo->limit_iops_count = limit_iops_count;
        qinfo->limit_io_count = limit_io_count;
        qinfo->microseconds_delay = microseconds_delay;
    }else{
        SPDK_ERRLOG("Get a invalid io qpair: %p\n", qinfo);
    }
}

void xt_io_qpair_lcg_init(xt_io_qpair *qinfo, unsigned int x0, unsigned long long m_modulus, unsigned long long c_increment, 
                         unsigned long long a_multiplier, unsigned long long offset, unsigned long long max_value, 
                         unsigned int step, unsigned int lcg_type){
    if(lcg_type == 1){
        if(NULL == qinfo->write_lcg){
            qinfo->write_lcg = malloc(sizeof(xt_lcg_random));
        }
        memset(qinfo->write_lcg, 0, sizeof(xt_lcg_random));
        init_lcg_random(qinfo->write_lcg, x0, m_modulus, c_increment, a_multiplier, offset, max_value, step, NULL, 0);
    }else{
        if(NULL == qinfo->read_lcg){
            qinfo->read_lcg = malloc(sizeof(xt_lcg_random));
        }
        memset(qinfo->read_lcg, 0, sizeof(xt_lcg_random));
        init_lcg_random(qinfo->read_lcg, x0, m_modulus, c_increment, a_multiplier, offset, max_value, step, NULL, 0);       
    }
}

void xt_io_qpair_lcg_fini(xt_io_qpair *qinfo){
    if(qinfo->write_lcg){
        free(qinfo->write_lcg);
        qinfo->write_lcg = NULL;
    }
    if(qinfo->read_lcg){
        free(qinfo->read_lcg);
        qinfo->read_lcg = NULL;
    } 
}

void xt_char_device_info_init(xt_admin_qpair * aqinfo, const char * char_device_name, unsigned int size, unsigned int nsid_count){
    if (NULL != char_device_name){
        strncpy(aqinfo->device_info.char_device_name, char_device_name, size);
        if(access(aqinfo->device_info.char_device_name, F_OK) == 0){
            aqinfo->device_info.admin_handle_id = open(aqinfo->device_info.char_device_name, O_RDWR);
        }else{
            SPDK_ERRLOG("Get a invalid char device %s\n", aqinfo->device_info.char_device_name);
            aqinfo->device_info.admin_handle_id = -1;
        }
    }
    aqinfo->device_info.block_devices = (xt_block_device_info *) malloc(sizeof(xt_block_device_info) * (nsid_count + 1));
    if(NULL == aqinfo->device_info.block_devices){
        SPDK_ERRLOG("malloc %ld failed \n", sizeof(xt_block_device_info) * (nsid_count + 1));
    }
    memset(aqinfo->device_info.block_devices, 0, sizeof(xt_block_device_info) * (nsid_count + 1));
    aqinfo->device_info.nsid_count = nsid_count + 1;
}

void xt_char_device_update_info(xt_admin_qpair * aqinfo, const char * char_device_name, unsigned int size){
    if (aqinfo->device_info.admin_handle_id > 0){
        close(aqinfo->device_info.admin_handle_id);
    }
    strncpy(aqinfo->device_info.char_device_name, char_device_name, size);
    if(access(aqinfo->device_info.char_device_name, F_OK) == 0){
        aqinfo->device_info.admin_handle_id = open(aqinfo->device_info.char_device_name, O_RDWR);
    }else{
        SPDK_ERRLOG("Get a invalid char device %s\n", aqinfo->device_info.char_device_name);
        aqinfo->device_info.admin_handle_id = -1;
    }   
}

void xt_update_ctrl_data(xt_admin_qpair * aqinfo, void * ctrl_data){
    xt_nvme_registers *nvme_regs;
    memcpy(&aqinfo->device_info.ctrl_data, ctrl_data, sizeof(aqinfo->device_info.ctrl_data));
    if(aqinfo->nvme_regs){
        nvme_regs = (xt_nvme_registers *)aqinfo->nvme_regs;
        aqinfo->device_info.max_io_xfer_size = 1 << (12 + nvme_regs->cap.bits.mpsmin + aqinfo->device_info.ctrl_data.mdts);
    }else{
        if(strcmp("null", aqinfo->engine_ops->name)){
           aqinfo->device_info.max_io_xfer_size = 1 << (12 + aqinfo->device_info.ctrl_data.mdts);
        }else{
            aqinfo->device_info.max_io_xfer_size = 1024 * 1024;
        }
    }
    aqinfo->device_info.max_metadata_size = 0;
}

unsigned int xt_get_mdts(xt_admin_qpair * aqinfo){
    if(aqinfo->device_info.max_io_xfer_size){
        return aqinfo->device_info.max_io_xfer_size;
    }
    SPDK_ERRLOG("Max Data Transfer Size is 0\n");
    return 0;
}

void xt_update_ns_data(xt_admin_qpair * aqinfo, void * ns_data, unsigned int nsid){
    if(nsid > aqinfo->device_info.nsid_count){
        SPDK_ERRLOG("input nsid %d, recover nsid count %d\n", nsid, aqinfo->device_info.nsid_count);
    }
    memcpy(&aqinfo->device_info.block_devices[nsid].ns_data, ns_data, sizeof(xt_ns_data));
    if(strcmp("null", aqinfo->engine_ops->name)){
        xt_nvme_ns_set_identify_data(aqinfo, nsid);
    }else{
        memset(&aqinfo->device_info.block_devices[nsid].ns_data, 0, sizeof(xt_ns_data));
        aqinfo->device_info.block_devices[nsid].sector_size = 512;
        aqinfo->device_info.block_devices[nsid].flags = 0xFFFF;
        aqinfo->device_info.block_devices[nsid].extended_lba_size = 0;
        aqinfo->device_info.block_devices[nsid].md_size = 0;
        aqinfo->device_info.block_devices[nsid].pi_type = 0;
        aqinfo->device_info.block_devices[nsid].sectors_per_max_io = 0;
        aqinfo->device_info.block_devices[nsid].sectors_per_stripe = 0;
    }
    for (unsigned int i = 0; i <= aqinfo->device_info.block_devices[nsid].ns_data.nlbaf; i++){
        if(aqinfo->device_info.max_metadata_size < aqinfo->device_info.block_devices[nsid].ns_data.lbaf[i].ms){
            aqinfo->device_info.max_metadata_size = aqinfo->device_info.block_devices[nsid].ns_data.lbaf[i].ms;
        }
    }
}

unsigned int xt_get_ns_sector_size(xt_admin_qpair * aqinfo, unsigned int nsid){
    return aqinfo->device_info.block_devices[nsid].sector_size;
}

unsigned int xt_get_ns_meta_data_size(xt_admin_qpair * aqinfo, unsigned int nsid){
    return aqinfo->device_info.block_devices[nsid].md_size;
}

void xt_block_device_update_info(xt_admin_qpair * aqinfo, const char * block_device_name, unsigned int size, unsigned int nsid, unsigned int clear_next_open_index){
    unsigned int max_nsid = nsid;
    if(nsid > aqinfo->device_info.nsid_count){
        xt_block_device_info * block_devices;
        if(max_nsid & (max_nsid -1)){
            max_nsid --;
            max_nsid |= max_nsid >> 1;
            max_nsid |= max_nsid >> 2;
            max_nsid |= max_nsid >> 4;
            max_nsid |= max_nsid >> 8;
            max_nsid |= max_nsid >> 16;
            max_nsid ++;
        }else{
            max_nsid += 1;
        }

        block_devices = (xt_block_device_info *) malloc(sizeof(xt_block_device_info) * max_nsid);
        if(NULL == block_devices){
            SPDK_ERRLOG("malloc %ld failed \n", sizeof(xt_block_device_info) * max_nsid);
        }
        memcpy(block_devices, aqinfo->device_info.block_devices, sizeof(xt_block_device_info) * (aqinfo->device_info.nsid_count));
        free(aqinfo->device_info.block_devices);
        aqinfo->device_info.block_devices = block_devices;
        aqinfo->device_info.nsid_count = max_nsid;
    }
    strncpy(aqinfo->device_info.block_devices[nsid].block_device_name, block_device_name, size);
    aqinfo->device_info.block_devices[nsid].nsid = nsid;
    if(clear_next_open_index){
        for(unsigned int index = 0; index < aqinfo->device_info.block_devices[nsid].next_open_index; index++){
            if(aqinfo->device_info.block_devices[nsid].device_fids[aqinfo->device_info.block_devices[nsid].next_open_index] > 0){
                SPDK_ERRLOG("before clear device open index, index %d open fid is %d \n", index, aqinfo->device_info.block_devices[nsid].device_fids[aqinfo->device_info.block_devices[nsid].next_open_index]);
            }
        }
        aqinfo->device_info.block_devices[nsid].next_open_index = 0;
    }
}

int xt_device_open(xt_admin_qpair * aqinfo, const char* path, unsigned int nsid){
    int flag = O_RDWR | O_DIRECT;
    int fid = open(path, flag);
    if (fid < 0){
        SPDK_ERRLOG("open %s with nsid failed 0x%x fid %d \n",path, nsid, fid);
        return -1;
    }
    if(aqinfo->device_info.block_devices[nsid].next_open_index >= XT_DEVICE_MAX_OPEN_COUNT){
        SPDK_ERRLOG("Recover open %s with nsid failed 0x%x, default max open count is %d",path, nsid, XT_DEVICE_MAX_OPEN_COUNT);
        return -1;
    }
    aqinfo->device_info.block_devices[nsid].device_fids[aqinfo->device_info.block_devices[nsid].next_open_index] = fid;
    aqinfo->device_info.block_devices[nsid].next_open_index ++;
    return fid;
}

void xt_device_close(xt_admin_qpair * aqinfo){
    for(unsigned int nsid_index = 0; nsid_index <= aqinfo->device_info.nsid_count; nsid_index++){
        if(aqinfo->device_info.block_devices[nsid_index].next_open_index != 0){
            for(unsigned int next_index = 0; next_index < aqinfo->device_info.block_devices[nsid_index].next_open_index; next_index++){
                close(aqinfo->device_info.block_devices[nsid_index].device_fids[next_index]);
            }
            aqinfo->device_info.block_devices[nsid_index].next_open_index = 0;
        }
    }
    if(aqinfo->device_info.admin_handle_id > 0){
        close(aqinfo->device_info.admin_handle_id);
        aqinfo->device_info.admin_handle_id = -1;
    }
}

void xt_char_device_info_fini(xt_admin_qpair * aqinfo){
    if(NULL != aqinfo->device_info.block_devices){
        free(aqinfo->device_info.block_devices);
    }
    aqinfo->device_info.block_devices = NULL;

}

void xt_io_qpair_reset(xt_io_qpair *qinfo, unsigned long long qpair_completions, unsigned long long submit_count,
                              unsigned long long completed_check_index){
    if(NULL != qinfo){
        qinfo->qpair_completions = qpair_completions;
        qinfo->submit_count = submit_count;
        qinfo->completed_check_index = completed_check_index;
    }else{
        SPDK_ERRLOG("Get a invalid io qpair: %p\n", qinfo);
    }            
}

void xt_io_qpair_timeout(xt_io_qpair *qinfo, unsigned long long timeout){
    if(NULL != qinfo){
        qinfo->timeout = timeout;
    }else{
        SPDK_ERRLOG("Get a invalid io qpair: %p\n", qinfo);
    }   
}

int xt_check_qpair_completioned(xt_io_qpair *qinfo){
    if (qinfo->submit_count - qinfo->last_submit_count == qinfo->qpair_completions)
        return 1;
    return 0;
}


unsigned long long xt_io_qpair_get_qpair_completions(xt_io_qpair *qinfo){
    return qinfo->qpair_completions;
}

void xt_io_qpair_reset_qpair_completions(xt_io_qpair *qinfo){
    qinfo->qpair_completions = 0;
}

void xt_io_qpair_init_write_buffer_addr_list(xt_io_qpair *qinfo, xt_buffer ** write_buf_addr_list){
    qinfo->write_buf_addr_list = write_buf_addr_list;
}

unsigned int xt_get_io_qpair_id(xt_io_qpair *qinfo){
    return qinfo->qpair_id;
}

cmds_u_ring * xt_io_qpair_get_completed_cmds_u_ring(xt_io_qpair *qinfo){
    return qinfo->completed_cmds_u_ring;
}