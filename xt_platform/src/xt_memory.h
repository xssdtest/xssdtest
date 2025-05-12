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
#ifndef XT_MEMORY_H
#define XT_MEMORY_H

#include "spdk/stdinc.h"
#include "xt_compiler/xt_compiler.h"
#include "xt_crc/crc7.h"
#include "xt_crc/crc16.h"
#include "xt_crc/crc32.h"
#include "xt_crc/crc64.h"
#include "xt_crc/md5.h"
#include "xt_crc/murmur3.h"
#include "xt_crc/sha1.h"
#include "xt_crc/sha3.h"
#include "xt_crc/sha256.h"
#include "xt_crc/sha512.h"
#include "xt_crc/xxhash.h"

#ifndef XT_BUFFER_IO_TAILER_COUNT
#define XT_BUFFER_IO_TAILER_COUNT	8
#endif

#ifndef XT_BUFFER_IO_TAILER_MARK
#define XT_BUFFER_IO_TAILER_MARK    7
#endif

#ifndef XT_BUFFER_IO_MIN_SIZE
#define XT_BUFFER_IO_MIN_SIZE	    512
#endif
#ifndef XT_BUFFER_IO_TRACKER_SIZE
#define XT_BUFFER_IO_TRACKER_SIZE	4096
#endif
#ifndef XT_BUFFER_PAGE_SIZE
#define XT_BUFFER_PAGE_SIZE     	4096
#endif
#ifndef XT_MB_BYTES
#define XT_MB_BYTES	            1048576
#endif
#ifndef XT_GB_BYTES
#define XT_GB_BYTES             1073741824
#endif

#ifndef XT_DEFAULT_BUFFER_ALIGN
#define XT_DEFAULT_BUFFER_ALIGN 64
#endif

enum {
	XT_BUFFER_FREE 		 = 0,   // BUFFER FREE
	XT_BUFFER_BUSY 		 = 1,   // BUFFER BUSY
	// XT_BUFFER_COMPLETED  = 2,   // BUFFER COMPLETED
	/*  FREE -->  BUSY --> COMPLETED  --> FREE*/
};

typedef union _xt_verify_tailer
{
    unsigned int raw[4];
    struct{
        unsigned long long slba;
        unsigned int buf_index : 28;
        unsigned int sub_buf_index : 4;
        unsigned int tailer_xor;
    };
} xt_verify_tailer;

#define XT_VERIFY_TAILER_SIZE   (sizeof(xt_verify_tailer))

typedef struct _xt_swap{
    void * swap_temp;
    unsigned int swap_size;

}xt_swap;

typedef struct _xt_buffer{
    void * _raw_buf;
    void * buf;
    void * physic_buf;
    void * io_tracker;      /* buffer align is 4096 */
    void * _data_integrity_extension_raw;
    void * data_integrity_extension;
    void ** io_tracker_arrys;
    void ** _io_tracker_raw_buf_arrys;
    unsigned long long seed;
    unsigned long long buf_crc512[XT_BUFFER_IO_TAILER_COUNT];
    unsigned long long buf_crc4096;
    unsigned int buf_length;
    unsigned int buf_align;
    unsigned int buf_type;      /* 1 write buffer; 2 read buffer; 3 trim buffer; 4 admin buffer; 0 and other TBD */
    unsigned int alloc_type;    /* 1 mem alloc; 2 spdk malloc; 3 CMB; 4 cuda; 5 mem share; 0 and other TBD*/
    unsigned int pi_type;       /* 0 no meta data; 1 dif; 2 dix*/
    unsigned int sector_size;   /* 512 or 4096 */
    unsigned int meta_sector_size; 
    unsigned int buf_index : 28;
    unsigned int sub_buf_index : 4;
    unsigned int buf_change;
    unsigned int buf_status;
    unsigned int io_tracker_length;
    xt_verify_tailer io_tailers[XT_BUFFER_IO_TAILER_COUNT];
    pthread_mutex_t buffer_lock;
} xt_buffer;

extern xt_swap g_xt_swap;

extern int xt_buffer_init(xt_buffer *buffer, unsigned int buf_length, unsigned int buf_align, unsigned int alloc_type, unsigned int mem_init);

extern int xt_buffer_free(xt_buffer *buffer);

extern void *xt_buffer_alloc_memory(unsigned int alloc_type, unsigned int buf_length);

extern void xt_buffer_alloc_free(unsigned int alloc_type, void * raw_buf);

extern unsigned char xt_buffer_crc8(xt_buffer *buffer, unsigned int buf_offset, unsigned int buf_length);

extern unsigned short xt_buffer_crc16(xt_buffer *buffer, unsigned int buf_offset, unsigned int buf_length);

extern unsigned int xt_buffer_crc32(xt_buffer *buffer, unsigned int buf_offset, unsigned int buf_length);

extern unsigned long long xt_buffer_crc64(xt_buffer *buffer, unsigned int buf_offset, unsigned int buf_length);

extern void xt_buffer_init_crc(xt_buffer *buffer, unsigned int crc_type);

extern void xt_set_uint8(void *buffer, unsigned int buf_offset, unsigned char value, int type);

extern unsigned char xt_get_uint8(void *buffer, unsigned int buf_offset, int type);

extern void xt_set_uint16(void *buffer, unsigned int buf_offset, unsigned short value, int type);

extern unsigned short xt_get_uint16(void *buffer, unsigned int buf_offset, int type);

extern void xt_set_uint32(void *buffer, unsigned int buf_offset, unsigned int value, int type);

extern unsigned int xt_get_uint32(void *buffer, unsigned int buf_offset, int type);

extern void xt_set_uint64(void *buffer, unsigned int buf_offset, unsigned long long value, int type);

extern unsigned long long xt_get_uint64(void *buffer, unsigned int buf_offset, int type);

extern void xt_buffer_get_init_io_tailer(xt_buffer *buffer);

extern int xt_buffer_reset_init_io_tailer(xt_buffer *buffer);

extern int xt_buffer_set_io_tracker(xt_buffer *buffer, unsigned int io_tracker_length, unsigned int io_tracker_type);

extern int xt_buffer_dif_generate(xt_buffer *buffer);

extern int xt_buffer_dif_init(xt_buffer *buffer, unsigned int meta_sector_size, unsigned int sector_size);

extern int xt_buffer_dix_generate(xt_buffer *buffer);

extern int xt_buffer_dix_init(xt_buffer *buffer, unsigned int meta_sector_size);

extern unsigned char * get_xt_buffer(xt_buffer *buffer);

extern void memory_dump(const void *addr, int length, int step, int dump_file, char * file_name);

extern void* xt_allocate_aligned_memory(unsigned int size, unsigned int alignment);

extern void xt_free_aligned_memory(void* aligned_ptr);

#endif