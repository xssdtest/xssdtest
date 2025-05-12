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
#include "xt_memory.h"
#include "spdk_internal/log.h"
#include "../spdk/lib/nvme/nvme_internal.h"
xt_swap g_xt_swap;

static void xt_buffer_instance_check(xt_buffer *buffer, bool buf_check){
    if (NULL == buffer){
        SPDK_ERRLOG("Buffer instance is NULL\n");
        assert(0);
    }else{
        if(buf_check && NULL == buffer->buf){
            SPDK_ERRLOG("Buffer instance buf is NULL\n");
            assert(0);
        }
    }
}

/* 1 mem alloc; 2 spdk malloc; 3 CMB; 4 cuda; 5 mem share; 0 and other TBD*/
int xt_buffer_init(xt_buffer *buffer, unsigned int buf_length, unsigned int buf_align, unsigned int alloc_type, unsigned int mem_init){
    xt_buffer_instance_check(buffer, false);
    unsigned long long _buf_align = buf_align - 1;
    buffer->buf_align = buf_align;
    buffer->buf_length = buf_length;
    buffer->alloc_type = alloc_type;
    switch (alloc_type)
    {
        case 1:
            buffer->_raw_buf = malloc(buf_length + buf_align); 
            if (NULL != buffer->_raw_buf){
                buffer->buf = (void *)(((unsigned long long)(buffer->_raw_buf + _buf_align)) & (~_buf_align));
                buffer->physic_buf = buffer->buf;
                if(buffer->buf < buffer->_raw_buf){
                    SPDK_ERRLOG("get a invalied aligned buf %p _raw_buf %p\n", buffer->buf, buffer->_raw_buf);
                }
                SPDK_DEBUGLOG(XT_SSD_TEST_LOG, "malloc buffer _raw_buf %p  buf %p physic_buf %p\n", buffer->_raw_buf, buffer->buf, buffer->physic_buf);
                if(mem_init){
                    memset(buffer->physic_buf, 0, buf_length);
                }
                break;
            }
            SPDK_ERRLOG("malloc buffer failed\n");
            return false;
        case 2:
            buffer->_raw_buf = spdk_dma_malloc(buf_length, buf_align, NULL);
            if (NULL != buffer->_raw_buf){
                buffer->buf = buffer->_raw_buf;
                buffer->physic_buf = (void * )spdk_vtophys(buffer->_raw_buf, NULL);
                if(mem_init){
                    memset(buffer->_raw_buf, 0, buf_length);
                }
                SPDK_DEBUGLOG(XT_SSD_TEST_LOG, "malloc buffer _raw_buf %p  buf %p physic_buf %p\n", buffer->_raw_buf, buffer->buf, buffer->physic_buf);
                break;
            }
            SPDK_ERRLOG("spdk_dma_malloc buffer failed\n");
            return false;
        case 3:
            break;
        case 4:
            break;
        case 5:
            break;
        default:
            SPDK_ERRLOG("Get a invalid alloc memory type: %d \n", alloc_type);
            assert(0);
    }
    return true;
}

int xt_buffer_free(xt_buffer *buffer){
    xt_buffer_instance_check(buffer, true);
    switch (buffer->alloc_type)
    {
        SPDK_DEBUGLOG(XT_SSD_TEST_LOG, "free buffer address %p\n", buffer->_raw_buf);
        case 1:
            free(buffer->_raw_buf);
            break;
        case 2:
            spdk_dma_free(buffer->_raw_buf);
            break;
        case 3:
            break;
        case 4:
            break;
        case 5:
            break;
        default:
            SPDK_ERRLOG("Get a invalid alloc memory type: %d \n", buffer->alloc_type);
            assert(0);
    }
    if(buffer->_io_tracker_raw_buf_arrys != NULL){
        for(unsigned int i = 0; i < buffer->io_tracker_length; i++){
            free(buffer->_io_tracker_raw_buf_arrys[i]);
        }
        free(buffer->_io_tracker_raw_buf_arrys);
        free(buffer->io_tracker_arrys);
        buffer->_io_tracker_raw_buf_arrys = NULL;
        buffer->io_tracker_arrys = NULL;
        buffer->io_tracker = NULL;
    }
    buffer->_raw_buf = NULL;
    buffer->buf = NULL;
    buffer->physic_buf = NULL;
    return true;
}

void *xt_buffer_alloc_memory(unsigned int alloc_type, unsigned int buf_length){
    void * _raw_buf = NULL;
    switch (alloc_type)
    {
        case 1:
            _raw_buf = malloc(buf_length);
            if (NULL != _raw_buf){
                memset(_raw_buf, 0, buf_length);
                return _raw_buf;
            }
            break;
        case 2:
            _raw_buf = spdk_dma_malloc(buf_length, 1, NULL);
            if (NULL != _raw_buf){
                memset(_raw_buf, 0, buf_length);
                return _raw_buf; 
            }
        case 3:
            break;
        case 4:
            break;
        case 5:
            break;
        default:
            SPDK_ERRLOG("Get a invalid alloc memory type: %d \n", alloc_type);
            assert(0);
    }
    SPDK_ERRLOG("malloc buffer failed\n");
    return NULL;
}

void xt_buffer_alloc_free(unsigned int alloc_type, void * raw_buf){
    switch (alloc_type)
    {
        case 1:
            free(raw_buf);
            break;
        case 2:
            spdk_dma_free(raw_buf);
        case 3:
            break;
        case 4:
            break;
        case 5:
            break;
        default:
            SPDK_ERRLOG("Get a invalid alloc memory type: %d \n", alloc_type);
            assert(0);
    }
    SPDK_ERRLOG("malloc buffer failed\n");
}

unsigned char xt_buffer_crc8(xt_buffer *buffer, unsigned int buf_offset, unsigned int buf_length){
    xt_buffer_instance_check(buffer, true);
   return xt_crc7(buffer->buf + buf_offset, buf_length);
}

unsigned short xt_buffer_crc16(xt_buffer *buffer, unsigned int buf_offset, unsigned int buf_length){
    xt_buffer_instance_check(buffer, true);
   return xt_crc16(buffer->buf + buf_offset, buf_length);
}

unsigned int xt_buffer_crc32(xt_buffer *buffer, unsigned int buf_offset, unsigned int buf_length){
    xt_buffer_instance_check(buffer, true);
   return xt_crc32(buffer->buf + buf_offset, buf_length);
}

unsigned long long xt_buffer_crc64(xt_buffer *buffer, unsigned int buf_offset, unsigned int buf_length){
    xt_buffer_instance_check(buffer, true);
   return xt_crc64(buffer->buf + buf_offset, buf_length);
}

void xt_buffer_init_crc(xt_buffer *buffer, unsigned int crc_type){
    xt_buffer_instance_check(buffer, true);
    for(unsigned long long index = 0; index < XT_BUFFER_IO_TAILER_COUNT; index ++){
        switch (crc_type)
        {
        case 8:
            buffer->buf_crc512[index] =  xt_buffer_crc8(buffer, index * XT_BUFFER_IO_MIN_SIZE, XT_BUFFER_IO_MIN_SIZE - sizeof(xt_verify_tailer));
            break;
        case 16:
            buffer->buf_crc512[index] = xt_buffer_crc16(buffer, index * XT_BUFFER_IO_MIN_SIZE, XT_BUFFER_IO_MIN_SIZE - sizeof(xt_verify_tailer));
            break;
        case 32:
            buffer->buf_crc512[index] = xt_buffer_crc32(buffer, index * XT_BUFFER_IO_MIN_SIZE, XT_BUFFER_IO_MIN_SIZE - sizeof(xt_verify_tailer));
            break;            
        case 64:
            buffer->buf_crc512[index] = xt_buffer_crc64(buffer, index * XT_BUFFER_IO_MIN_SIZE, XT_BUFFER_IO_MIN_SIZE - sizeof(xt_verify_tailer));
            break;  
        default:
            break;
        }
    }
    switch (crc_type)
    {
    case 8:
        buffer->buf_crc4096 =  xt_buffer_crc8(buffer, 0, 4096 - sizeof(xt_verify_tailer));
        break;
    case 16:
        buffer->buf_crc4096 = xt_buffer_crc16(buffer, 0, 4096 - sizeof(xt_verify_tailer));
        break;
    case 32:
        buffer->buf_crc4096 = xt_buffer_crc32(buffer, 0, 4096 - sizeof(xt_verify_tailer));
        break;            
    case 64:
        buffer->buf_crc4096 = xt_buffer_crc64(buffer, 0, 4096 - sizeof(xt_verify_tailer));
        break;  
    default:
        break;
    }
}


void xt_set_uint8(void *buffer, unsigned int buf_offset, unsigned char value, int type){
    if(type == 1){
        xt_buffer *_buffer = (xt_buffer *)buffer;
        xt_buffer_instance_check(_buffer, true);
        if (_buffer->buf_length >= buf_offset + 1){
            ((unsigned char *)_buffer->buf)[buf_offset] = value;
            if(((unsigned char *)_buffer->buf)[buf_offset] != value){
                SPDK_ERRLOG("Set offset %d faile expect value 0x%2x  actual value 0x%2x\n", buf_offset, ((unsigned char *)_buffer->buf)[buf_offset], value);
            }
        }else{
            SPDK_ERRLOG("Set buffer invalid offset; offset is 0x%x buffer length 0x%x\n", buf_offset, _buffer->buf_length);
            assert(0);
        }
    }else{
        xt_buffer_instance_check(buffer, false);
        ((unsigned char *)buffer)[buf_offset] = value;
        if(*(unsigned char *)(buffer + buf_offset) != value){
            SPDK_ERRLOG("Set offset %d faile expect value 0x%x  actual value 0x%x\n", buf_offset, *(unsigned char *)(buffer + buf_offset), value);
        } 
    }

}

unsigned char xt_get_uint8(void *buffer, unsigned int buf_offset, int type){
    if(type == 1){
        xt_buffer *_buffer = (xt_buffer *)buffer;
        xt_buffer_instance_check(_buffer, true);
        if (_buffer->buf_length >= buf_offset + 1){
            return ((unsigned char *)_buffer->buf)[buf_offset];
        }else{
            SPDK_ERRLOG("Get buffer invalid offset; offset is 0x%x buffer length 0x%x\n", buf_offset, _buffer->buf_length);
            assert(0);
            return -1;
        }
    }else{
        xt_buffer_instance_check(buffer, false);
        return ((unsigned char *)buffer)[buf_offset];
    }

}

void xt_set_uint16(void *buffer, unsigned int buf_offset, unsigned short value, int type){
    if(type == 1){
        xt_buffer *_buffer = (xt_buffer *)buffer;
        xt_buffer_instance_check(_buffer, true);
        if (_buffer->buf_length >= buf_offset + 2){
            *(unsigned short *)(_buffer->buf + buf_offset) = value;
            if(*(unsigned short *)(_buffer->buf + buf_offset) != value){
                SPDK_ERRLOG("Set offset %d faile expect value 0x%4x  actual value 0x%4x\n", buf_offset, *(unsigned short *)(_buffer->buf + buf_offset), value);
            }
        }else{
            SPDK_ERRLOG("Set buffer invalid offset; offset is 0x%x buffer length 0x%x\n", buf_offset, _buffer->buf_length);
            assert(0);
        }
    }else{
        xt_buffer_instance_check(buffer, false);
        *(unsigned short *)(buffer + buf_offset) = value;
        if(*(unsigned short *)(buffer + buf_offset) != value){
            SPDK_ERRLOG("Set offset %d faile expect value 0x%x  actual value 0x%x\n", buf_offset, *(unsigned short *)(buffer + buf_offset), value);
        } 
    }
}

unsigned short xt_get_uint16(void *buffer, unsigned int buf_offset, int type){
    if(type == 1){
        xt_buffer *_buffer = (xt_buffer *)buffer;
        xt_buffer_instance_check(_buffer, true);
        if (_buffer->buf_length >= buf_offset + 2){
            return *(unsigned short *)(_buffer->buf + buf_offset);
        }else{
            SPDK_ERRLOG("Get buffer invalid offset; offset is 0x%x buffer length 0x%x\n", buf_offset, _buffer->buf_length);
            assert(0);
            return -1;
        }
    }else{
        xt_buffer_instance_check(buffer, false);
        return *(unsigned short *)(buffer + buf_offset);
    }
}

void xt_set_uint32(void *buffer, unsigned int buf_offset, unsigned int value, int type){
    if(type == 1){
        xt_buffer *_buffer = (xt_buffer *)buffer;
        xt_buffer_instance_check(_buffer, true);
        if (_buffer->buf_length >= buf_offset + 4){
            *(unsigned int *)(_buffer->buf + buf_offset) = value;
            if(*(unsigned int *)(_buffer->buf + buf_offset) != value){
                SPDK_ERRLOG("Set offset %d faile expect value 0x%x  actual value 0x%x\n", buf_offset, *(unsigned int *)(_buffer->buf + buf_offset), value);
            }
        }else{
            SPDK_ERRLOG("Set buffer invalid offset; offset is 0x%x buffer length 0x%x\n", buf_offset, _buffer->buf_length);
            assert(0);
        }
    }else{
        xt_buffer_instance_check(buffer, false);
        *(unsigned int *)(buffer + buf_offset) = value;
        if(*(unsigned int *)(buffer + buf_offset) != value){
            SPDK_ERRLOG("Set offset %d faile expect value 0x%x  actual value 0x%x\n", buf_offset, *(unsigned int *)(buffer + buf_offset), value);
        } 
    }
}

unsigned int xt_get_uint32(void *buffer, unsigned int buf_offset, int type){
    if(type == 1){
        xt_buffer *_buffer = (xt_buffer *)buffer;
        xt_buffer_instance_check(_buffer, true);
        if (_buffer->buf_length >= buf_offset + 4){
            return *(unsigned int *)(_buffer->buf + buf_offset);
        }else{
            SPDK_ERRLOG("Get buffer invalid offset; offset is 0x%x buffer length 0x%x\n", buf_offset, _buffer->buf_length);
            assert(0);
            return -1;
        }
    }else{
        xt_buffer_instance_check(buffer, false);
        return *(unsigned int *)(buffer + buf_offset);
    }
}

void xt_set_uint64(void *buffer, unsigned int buf_offset, unsigned long long value, int type){
    if(type == 1){
        xt_buffer *_buffer = (xt_buffer *)buffer;
        xt_buffer_instance_check(_buffer, true);
        if (_buffer->buf_length >= buf_offset + 8){
            *(unsigned long long *)(_buffer->buf + buf_offset) = value;
            if(*(unsigned long long *)(_buffer->buf + buf_offset) != value){
                SPDK_ERRLOG("Set offset %d faile expect value 0x%llx  actual value 0x%llx\n", buf_offset, *(unsigned long long *)(_buffer->buf + buf_offset), value);
            }
        }else{
            SPDK_ERRLOG("Set buffer invalid offset; offset is 0x%x buffer length 0x%x\n", buf_offset, _buffer->buf_length);
            assert(0);
        }
    }else{
         xt_buffer_instance_check(buffer, false);
        *(unsigned long long *)(buffer + buf_offset) = value; 
        if(*(unsigned long long *)(buffer + buf_offset) != value){
            SPDK_ERRLOG("Set offset %d faile expect value 0x%llx  actual value 0x%llx\n", buf_offset, *(unsigned long long *)(buffer + buf_offset), value);
        }    
    }
}

unsigned long long xt_get_uint64(void *buffer, unsigned int buf_offset, int type){
    if(type == 1){
        xt_buffer *_buffer = (xt_buffer *)buffer;
        xt_buffer_instance_check(_buffer, true);
        if (_buffer->buf_length >= buf_offset + 8){
            return *(unsigned long long *)(_buffer->buf + buf_offset);
        }else{
            SPDK_ERRLOG("Get buffer invalid offset; offset is 0x%x buffer length 0x%x\n", buf_offset, _buffer->buf_length);
            assert(0);
            return -1;
        }
    }else{
         xt_buffer_instance_check(buffer, false);
        return *(unsigned long long *)(buffer + buf_offset);       
    }
}

void xt_buffer_get_init_io_tailer(xt_buffer *buffer){
    xt_buffer_instance_check(buffer, true);
    xt_verify_tailer *io_tailers = (xt_verify_tailer *)buffer->buf;
    unsigned int _step = XT_BUFFER_IO_MIN_SIZE / sizeof(xt_verify_tailer);
    for(int io_tailer_index = 0; io_tailer_index < XT_BUFFER_IO_TAILER_COUNT; io_tailer_index ++){
        memcpy(&buffer->io_tailers[io_tailer_index], &io_tailers[_step * (io_tailer_index + 1) - 1], XT_VERIFY_TAILER_SIZE);
        // for(int io_tailer_raw_index = 0; io_tailer_raw_index < XT_VERIFY_TAILER_SIZE; io_tailer_raw_index ++){
        //     buffer->io_tailers[io_tailer_index].raw[io_tailer_raw_index] = *(unsigned int *)(buffer->buf + XT_VERIFY_TAILER_SIZE * XT_BUFFER_IO_MIN_SIZE 
        //                                                                   + io_tailer_raw_index * sizeof(unsigned int));
        //     SPDK_DEBUGLOG(XT_MEMORY_LOG, "io tailers raw data[%d]: 0x%x\n", io_tailer_raw_index, buffer->io_tailers[io_tailer_index].raw[io_tailer_raw_index]);
        // }
    }

}

int xt_buffer_reset_init_io_tailer(xt_buffer *buffer){
    xt_buffer_instance_check(buffer, true);
    // int io_tailer_index = 0;
    // int io_tailer_raw_index;
    /* To be supplemented */
    return XT_VERIFY_TAILER_SIZE;
    
}

int xt_buffer_set_io_tracker(xt_buffer *buffer, unsigned int io_tracker_length, unsigned int io_tracker_type){
    xt_buffer_instance_check(buffer, true);
    unsigned long long _buf_align = XT_BUFFER_IO_TRACKER_SIZE - 1;
    buffer->io_tracker_length = io_tracker_length;
    buffer->io_tracker_arrys = malloc(io_tracker_length * sizeof(void *));
    buffer->_io_tracker_raw_buf_arrys = malloc(io_tracker_length * sizeof(void *));
    for(unsigned int  io_tracker_index = 0; io_tracker_index < io_tracker_length; io_tracker_index ++){
        buffer->_io_tracker_raw_buf_arrys[io_tracker_index] = malloc(XT_BUFFER_IO_TRACKER_SIZE * 2);
        if(NULL != buffer->_io_tracker_raw_buf_arrys[io_tracker_index]){
            buffer->io_tracker_arrys[io_tracker_index] = (void *)(((unsigned long long)buffer->_io_tracker_raw_buf_arrys[io_tracker_index]) & (~_buf_align));
        }else{
            return false;
        }
    }
    if(io_tracker_type == 1){
        unsigned int prp_tracker_size = (io_tracker_length * XT_BUFFER_IO_TRACKER_SIZE / sizeof(unsigned long long) - XT_BUFFER_IO_MIN_SIZE + 1) * XT_BUFFER_IO_TRACKER_SIZE;
        if (buffer->buf_length > prp_tracker_size){
            SPDK_ERRLOG("io tracker %d, buffer length: %d \n", prp_tracker_size, buffer->buf_length);
            return false;
        }
        if (NULL != buffer->_raw_buf){
            unsigned int prp1_size = XT_BUFFER_PAGE_SIZE - (unsigned long long)buffer->buf % XT_BUFFER_PAGE_SIZE;
            unsigned int prp_list_size = buffer->buf_length - prp1_size;
            unsigned long long prp_list_address_base = (unsigned long long) (buffer->buf + prp1_size);
            unsigned int prp_list_array_size =  XT_BUFFER_PAGE_SIZE / sizeof(unsigned long long) - 1;
            unsigned int index = 0;
            unsigned int prp_list_address_index = 0;
            while (prp_list_size){
                if (index && index % prp_list_array_size == 0){
                    if (prp_list_address_index > io_tracker_length - 1){
                       SPDK_ERRLOG("prp list address index %d out of range\n", prp_list_address_index);
                       return false;
                    }else{
                       ((unsigned long long *)buffer->io_tracker_arrys[prp_list_address_index])[index] = (unsigned long long)buffer->io_tracker_arrys[prp_list_address_index + 1];
                    }
                    prp_list_address_index += 1;
                    index = 0;
                }else{
                    ((unsigned long long *)buffer->io_tracker_arrys[prp_list_address_index])[index] = prp_list_address_base + XT_BUFFER_PAGE_SIZE * index;
                    if(prp_list_size <= XT_BUFFER_PAGE_SIZE){
                        break;
                    }
                    prp_list_size -= XT_BUFFER_PAGE_SIZE;
                    index += 1;
                }
            }
            buffer->io_tracker = buffer->io_tracker_arrys[0];
        }else{
            return false;
        }
        return true;
    }else{
        // SGL mode
    }
    return true;
}


int xt_buffer_dif_generate(xt_buffer *buffer){
    /* To be supplemented */
    return 1;
}

int xt_buffer_dif_init(xt_buffer *buffer, unsigned int meta_sector_size, unsigned int sector_size){
    if(buffer->meta_sector_size == meta_sector_size && buffer->sector_size == sector_size && buffer->pi_type == 1){
        return 0;
    }
    void * _temp =  malloc(4096);
    if(NULL == _temp){
        SPDK_ERRLOG("malloc memory failed, dif init failed\n");
        return -1;
    }
    unsigned int count = buffer->buf_length / sector_size;
    unsigned int _buffer_offset = 0;
    switch (buffer->pi_type){
        case 0:
        case 2:
            for(unsigned long long offset=1; offset <= XT_BUFFER_IO_TAILER_COUNT; offset++){
                memcpy((buffer->buf + offset * 512 - sizeof(xt_verify_tailer)), &buffer->io_tailers[(offset - 1) & XT_BUFFER_IO_TAILER_MARK], sizeof(xt_verify_tailer));
            }
            memcpy(_temp, buffer->buf, 4096);
            break;
        case 1:
            if(buffer->sector_size == 512){
                for(unsigned long long offset=1; offset <= XT_BUFFER_IO_TAILER_COUNT; offset++){
                    _buffer_offset = offset * (buffer->meta_sector_size + buffer->sector_size) - buffer->meta_sector_size - sizeof(xt_verify_tailer);
                    memcpy((buffer->buf + _buffer_offset), &buffer->io_tailers[offset & XT_BUFFER_IO_TAILER_MARK], sizeof(xt_verify_tailer));
                    memcpy(_temp + (offset - 1) * 512, buffer->buf + (offset - 1) * (buffer->meta_sector_size + buffer->sector_size), 512);
                }
            }else{
                for(unsigned long long offset=0; offset < XT_BUFFER_IO_TAILER_COUNT; offset++){
                    memcpy((buffer->buf + (offset + 1) * 512) - sizeof(xt_verify_tailer), &buffer->io_tailers[(offset - 1) & XT_BUFFER_IO_TAILER_MARK], sizeof(xt_verify_tailer));
                }
                memcpy(_temp, buffer->buf, 4096);
            }
            break;
        default:
            break;
    }
    for(unsigned int offset = 0; offset < count; offset++){
        if(sector_size == 512){
            memcpy(buffer->buf + offset * (meta_sector_size + sector_size), _temp + (offset & XT_BUFFER_IO_TAILER_MARK) * sector_size, sector_size);
        }else{
            memcpy(buffer->buf + offset * (meta_sector_size + sector_size), _temp, sector_size);
        }
    }
    buffer->buf_change = 1;
    buffer->pi_type = 1;
    buffer->meta_sector_size = meta_sector_size;
    if(NULL != _temp){
        free(_temp);
    }
    return 0;
}

int xt_buffer_dix_generate(xt_buffer *buffer){
    /* To be supplemented */
    return 1;
}

int xt_buffer_dix_init(xt_buffer *buffer, unsigned int meta_sector_size){
    unsigned int buf_length;
    unsigned int count = buffer->buf_length / 512;
    if(buffer->meta_sector_size >= meta_sector_size && buffer->pi_type == 2){
        return 0;
    }
    if(meta_sector_size > 16){
        buf_length = 32 * 1024;
    }else{
        buf_length = 8 * 1024;
    }
    if(buffer->buf_type != 2){
        buf_length += 64;
    }
    if(NULL != buffer->_data_integrity_extension_raw){
        xt_buffer_alloc_free(buffer->buf_type, buffer->_data_integrity_extension_raw);
    }
    buffer->_data_integrity_extension_raw = xt_buffer_alloc_memory(buffer->buf_type, buf_length);
    buffer->data_integrity_extension  = (void *)(((unsigned long long)(buffer->_data_integrity_extension_raw + XT_DEFAULT_BUFFER_ALIGN)) & (~XT_DEFAULT_BUFFER_ALIGN));
    if(buffer->buf_change){
        if((buffer->pi_type == 0) | (buffer->pi_type == 2)){
            for(unsigned int offset=1; offset <= count; offset++){
                memcpy((buffer->buf + offset * 512 - sizeof(xt_verify_tailer)), &buffer->io_tailers[offset & XT_BUFFER_IO_TAILER_MARK], sizeof(xt_verify_tailer));
            }
        }else{
            unsigned int _buffer_offset;
            if(buffer->sector_size == 512){
                for(unsigned long long offset=1; offset <= XT_BUFFER_IO_TAILER_COUNT; offset++){
                    _buffer_offset = offset * (buffer->meta_sector_size + buffer->sector_size) - buffer->meta_sector_size - sizeof(xt_verify_tailer);
                    memcpy((buffer->buf + _buffer_offset), &buffer->io_tailers[offset & XT_BUFFER_IO_TAILER_MARK], sizeof(xt_verify_tailer));
                    memcpy((buffer->buf + (offset - 1) * 512), buffer->buf + (offset - 1) * (buffer->meta_sector_size + buffer->sector_size), 512);
                }
            }else{
                for(unsigned long long offset=0; offset < XT_BUFFER_IO_TAILER_COUNT; offset++){
                    memcpy((buffer->buf + (offset + 1) * 512) - sizeof(xt_verify_tailer), &buffer->io_tailers[(offset - 1) & XT_BUFFER_IO_TAILER_MARK], sizeof(xt_verify_tailer));
                }
            }
            count = buffer->buf_length / 4096;
            for(unsigned int offset=1; offset < count; offset++){
                memcpy((buffer->buf + offset * 4096), buffer->buf, 4096);
            }
        }
    }
    buffer->buf_change = 0;
    buffer->pi_type = 2;
    buffer->meta_sector_size = meta_sector_size;
    return 0;
}

unsigned char *get_xt_buffer(xt_buffer *buffer){
    xt_buffer_instance_check(buffer, true);
    return (unsigned char *)buffer->buf;
}

void memory_dump(const void *addr, int length, int step, int dump_file, char * file_name) {
    const unsigned char *buffer = addr;
    for (int i = 0; i < length; i++) {
        if (i % step == 0) {
            if (i != 0)
                printf("\n");
            printf("0x%08X: ", i);
        }
        printf("%02X ", buffer[i]);
    }
    printf("\n");
    if(dump_file && file_name){
        int fid = open(file_name, O_RDWR);
        if(fid > 0){
            SPDK_ERRLOG("open %s failed\n", file_name);
        }
        if(write(fid, addr, length) < 0){
            SPDK_ERRLOG("write data to %s failed\n", file_name);
        }
        close(fid);
    }
}


void* xt_allocate_aligned_memory(unsigned int size, unsigned int alignment) {
    unsigned long long adjusted_alignment = alignment;
    if (adjusted_alignment > 0x100000){
        adjusted_alignment = 0x100000;
    }else{
        if(adjusted_alignment < 8){
            adjusted_alignment = 8;
        }else{
            if (adjusted_alignment & (adjusted_alignment - 1)) {
                adjusted_alignment--;
                adjusted_alignment |= adjusted_alignment >> 1;
                adjusted_alignment |= adjusted_alignment >> 2;
                adjusted_alignment |= adjusted_alignment >> 4;
                adjusted_alignment |= adjusted_alignment >> 8;
                adjusted_alignment |= adjusted_alignment >> 16;
                adjusted_alignment |= adjusted_alignment >> 32;
                adjusted_alignment++;
            }
        }
    }
    void* original = malloc(size + adjusted_alignment - 1 + sizeof(void*));
    if (!original) return NULL;

    unsigned long long raw_address = (unsigned long long)original + sizeof(void*);
    unsigned long long aligned_address = (raw_address + adjusted_alignment - 1) & ~(adjusted_alignment - 1);
    *((void**)(aligned_address - sizeof(void*))) = original;

    return (void*)aligned_address;
}

void xt_free_aligned_memory(void* aligned_ptr) {
    if (aligned_ptr) {
        void* original = *((void**)(aligned_ptr - sizeof(void*)));
        free(original);
    }
}