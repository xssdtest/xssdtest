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
#include "xt_load_engines.h"

xt_engines g_engines_list;
static FLIST_HEAD(engines_list);

void xt_register_engine(xt_engine_ops *engine_ops){
    flist_add_tail(&engine_ops->list, &engines_list);
}

xt_engine_ops *xt_find_engine(const char *name){
	xt_engine_ops *ops;
	struct flist_head *entry;
	if (NULL == name){
		g_engines_list.engines_count = 0;
	}
	flist_for_each(entry, &engines_list) {
		ops = flist_entry(entry, xt_engine_ops, list);
		if (NULL == name){
			if(sizeof(ops->name) > XT_ENGINE_NAME_SIZE){
				printf("The size of the engine name is greater than the defined maximum:%d\n", XT_ENGINE_NAME_SIZE);
			}
			if(g_engines_list.engines_count >= XT_ENGINE_NAME_COUNT){
				printf("The size of the engine count is greater than the defined maximum: %d\n", XT_ENGINE_NAME_COUNT);
			}
			strcpy(g_engines_list.engine_names[g_engines_list.engines_count], ops->name);
			g_engines_list.engines_count ++;
		}else{
			if (!strcmp(name, ops->name))
				return ops;
		}
	}
	return NULL;
}

char* get_engine_names(void){
	unsigned int index = g_engines_list.index;
	if(g_engines_list.engines_count == 0){
		xt_find_engine(NULL);
	}
	if (g_engines_list.index >= g_engines_list.engines_count){
		g_engines_list.index = 0;
		return NULL;
	}else{
		g_engines_list.index ++;
		return g_engines_list.engine_names[index];
	}
}

unsigned int reload_engine_check(const char *src_engine, const char *dest_engine){
	if(NULL == src_engine || NULL == dest_engine){
		printf("src or dest engine is NULL src engine %p dest engine %p\n", src_engine, dest_engine);
	}else{
		if(!strcmp(src_engine, dest_engine)){
			return 1;
		}
		if(strstr(dest_engine, "null") != NULL){
			return 1;
		}
		unsigned int src_engine_nvme_type = 0;
		unsigned int src_engine_simulator_type = 0;
		unsigned int src_engine_sata_type = 0;
		unsigned int dest_engine_nvme_type = 0;
		unsigned int dest_engine_simulator_type = 0;
		unsigned int dest_engine_sata_type = 0;	
		if (strstr(src_engine, "simulator") != NULL){
			src_engine_simulator_type = 1;
		}else if (strstr(src_engine, "nvme") != NULL && strstr(src_engine, "simulator") == NULL){
			src_engine_nvme_type = 1;
		}else if (strstr(src_engine, "sata") != NULL){
			src_engine_sata_type = 1;
		}
		if (strstr(dest_engine, "simulator") != NULL){
			dest_engine_simulator_type = 1;
		}else if (strstr(dest_engine, "nvme") != NULL && strstr(dest_engine, "simulator") == NULL){
			dest_engine_nvme_type = 1;
		}else if (strstr(dest_engine, "sata") != NULL){
			dest_engine_sata_type = 1;
		}
		if(src_engine_nvme_type && src_engine_nvme_type == dest_engine_nvme_type){
			return 1;
		}
		if(src_engine_sata_type && src_engine_sata_type == dest_engine_sata_type){
			return 1;
		}
		if(src_engine_simulator_type && src_engine_simulator_type == dest_engine_simulator_type){
			printf("src engine %s dest engine %s \n", src_engine, dest_engine);
		}
	}
	return 0;
}
