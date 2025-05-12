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
#include "xssdtest.h"
#include "../spdk/lib/nvme/nvme_internal.h"
SPDK_LOG_REGISTER_COMPONENT("xssdtest", XT_SSD_TEST_LOG)
xt_commands_logger* g_xt_cmd_log;
uint64_t g_tsc_rate;
int g_pid;
int g_shmid;

static bool driver_init_flag = true;
static char g_share_memory_filename[256];
static const double g_latency_cutoffs[] = {
	0.01,
	0.10,
	0.25,
	0.50,
	0.75,
	0.90,
	0.95,
	0.98,
	0.99,
	0.995,
	0.999,
	0.9999,
	0.99999,
	0.999999,
	0.9999999,
	-1,
};

void xt_admin_qpair_check(xt_admin_qpair *aqinfo){
    if(NULL == aqinfo){
        SPDK_ERRLOG("Get a null admin qpair\n");
        assert(0);
    }
}

void xt_admin_init(xt_admin_qpair *aqinfo, char * pcie_list,  int pcie_count){
    xt_admin_qpair_check(aqinfo);
    aqinfo->pid = getpid();
    if(0 != pcie_count){
        aqinfo->pci_whitelist = (struct spdk_pci_addr *) malloc(sizeof(struct spdk_pci_addr) * pcie_count * XT_PCIE_FUNC_COUNT);
        if(NULL == aqinfo->pci_whitelist){
            SPDK_ERRLOG("alloc memory failed, pcie_list: %p pcie_count: %d\n", pcie_list, pcie_count ++);
            assert(0);
        }
        struct spdk_pci_addr pcie_addr;
        int rc = 0;
        for(int pcie_index = 0; pcie_index < pcie_count; pcie_index ++){
            rc = spdk_pci_addr_parse(&pcie_addr, (pcie_list + XT_PCIE_NAME_SIZE * pcie_index));
            if ( rc != 0){
                SPDK_ERRLOG("parse pcie address failed: %s \n", (char *)(pcie_list + XT_PCIE_NAME_SIZE * pcie_index));
                assert(0);
            }
            for(int func_index = 0; func_index < XT_PCIE_FUNC_COUNT; func_index ++){
                aqinfo->pci_whitelist[pcie_index * XT_PCIE_FUNC_COUNT + func_index].domain = pcie_addr.domain;
                aqinfo->pci_whitelist[pcie_index * XT_PCIE_FUNC_COUNT + func_index].bus    = pcie_addr.bus;
                aqinfo->pci_whitelist[pcie_index * XT_PCIE_FUNC_COUNT + func_index].dev    = pcie_addr.dev;
                aqinfo->pci_whitelist[pcie_index * XT_PCIE_FUNC_COUNT + func_index].func   = func_index;
            }
        }
    }
    aqinfo->io_unit_clear_size = offsetof(cmds_u, iocb);
    if(NULL == aqinfo->engine_names && g_engines_list.engines_count == 0){
        xt_find_engine(NULL);
        aqinfo->engine_names = &g_engines_list;
    }else{
        aqinfo->engine_names = &g_engines_list;
    }
    g_engines_list.index = 0;
}

unsigned long long xt_admin_get_bar_size(xt_admin_qpair *aqinfo){
    xt_admin_qpair_check(aqinfo);
    return aqinfo->bar_size;
}

unsigned long long xt_sys_tick_us(xt_admin_qpair *aqinfo){
    xt_admin_qpair_check(aqinfo);
    if(0 == aqinfo->sys_tick_hz){
        aqinfo->sys_tick_hz = (unsigned long long)(spdk_get_ticks_hz() / 1000000);
    }
    return aqinfo->sys_tick_hz;
}

static int pci_enum_cb(void *ctx, struct spdk_pci_device *dev){
	return 0;
}

int xt_pcie_init(xt_admin_qpair *aqinfo){
    char buf[128];
    struct spdk_env_opts opts;
    struct spdk_pci_addr pcie_addr;
    struct spdk_pci_device *dev;
    struct stat sb;
    int shm_id = getpid();
    int rc = 0;
    // get the shared memory group id among primary and secondary processes
    if (driver_init_flag){
        sprintf(buf, "/var/run/dpdk/spdk%d", aqinfo->pid);
        if (stat(buf, &sb) == 0 && S_ISDIR(sb.st_mode)){
            //it is a secondary process
            shm_id = aqinfo->pid;
        }
        spdk_env_opts_init(&opts);
        opts.name = "xsssdtest";
        opts.shm_id = shm_id;
        opts.mem_size = aqinfo->spdk_mem_size;
        opts.pci_whitelist = aqinfo->pci_whitelist;
        if (spdk_env_init(&opts) < 0) {
            SPDK_ERRLOG("initialize SPDK env failed\n");
            return -1;
        }
        if (spdk_vmd_init()) {
            SPDK_NOTICELOG("Failed to initialize VMD. Some NVMe devices can be unavailable.\n");
        }
        if (NULL != aqinfo->pci_whitelist){
            free(aqinfo->pci_whitelist);
        }
        driver_init_flag = false;
    }
    rc = spdk_pci_addr_parse(&pcie_addr, aqinfo->traddr);
    if ( rc != 0){
        SPDK_ERRLOG("parse pcie address failed: %s \n", aqinfo->traddr);
        return -1;
    }
	if (spdk_pci_enumerate(spdk_pci_nvme_get_driver(), pci_enum_cb, NULL)) {
		SPDK_ERRLOG("Unable to enumerate PCI nvme driver\n");
	}
    dev = spdk_pci_get_first_device();
	while (dev) {
        SPDK_NOTICELOG("PCIe info -- domain: %04x, bus: %02x, dev: %02x, dev: %1x dev->internal.attached: %d\n", dev->addr.domain,
                dev->addr.bus, dev->addr.dev, dev->addr.func, dev->internal.attached);
        if (dev->addr.domain == pcie_addr.domain && dev->addr.bus == pcie_addr.bus && \
            dev->addr.dev == pcie_addr.dev && dev->addr.func == pcie_addr.dev){
                aqinfo->pcie_info = dev;
                int rc = 0;
                void *addr;
                uint32_t bir = 0;
                uint64_t bar_size, bar_phys_addr;
                rc = dev->map_bar(dev, bir, &addr, &bar_phys_addr, &bar_size);
                if(rc){
                    SPDK_ERRLOG("pcie device map bar 0 failed");
                }
                SPDK_NOTICELOG("pcie address %p  bir: %d, addr: %p bar_phys_addr: 0x%lx, bar_size: 0x%lx\n", aqinfo->pcie_info,
                                bir, addr, bar_phys_addr, bar_size);
                aqinfo->nvme_regs = addr;
                dev->internal.attached = 0;
            }
        dev = spdk_pci_get_next_device(dev);
    }
    SPDK_INFOLOG(XT_SSD_TEST_LOG, "PCIE Address: %p \n", aqinfo->pcie_info);
    return 0;
}

void xt_init_share_memory(void){
    key_t key;
    g_pid = getpid();
    sprintf(g_share_memory_filename, "/var/log/xssdtest_%d.config", g_pid);
    FILE *file = fopen(g_share_memory_filename, "w");
    if (file == NULL) {
        SPDK_ERRLOG("opening %s fail \n", g_share_memory_filename); 
        assert(0);
    }
    fclose(file);

    key = ftok(g_share_memory_filename, g_pid);
    g_shmid = shmget(key, XT_SHARE_MEMORY_SIZE, IPC_CREAT | 0666);
    if (g_shmid == -1){
        SPDK_ERRLOG("get share memory failed\n");
        assert(0);
    }
    g_xt_cmd_log = (xt_commands_logger *)shmat(g_shmid, NULL, 0);
    if (g_xt_cmd_log == NULL){
        SPDK_ERRLOG("connect share memory failed\n");
        assert(0);
    }
    memset(g_xt_cmd_log, 0, XT_SHARE_MEMORY_SIZE);
    g_xt_cmd_log->cmds_log_header.pid = g_pid;
    g_xt_cmd_log->cmds_log_header.shm_id = g_shmid;
    g_xt_cmd_log->cmds_log_header.ioprint_thread_flag = 1;
    g_xt_cmd_log->cmds_log_header.cmds_log_count = (XT_SHARE_MEMORY_SIZE - sizeof(g_xt_cmd_log->cmds_log_header.raw)) / XT_CMD_LOG_ENTRY_SIZE;
}

void xt_init_commands_logger(void){
    int pid = fork();
    if (pid == 0){
        g_xt_cmd_log = (xt_commands_logger *)shmat(g_shmid, NULL, 0);
        if (g_xt_cmd_log == NULL){
            SPDK_ERRLOG("connect share memory failed in subprocess\n");
            assert(0);
        }
        start_io_print_thread();
        while (kill(g_pid, 0) != -1)
        {
            /* To be supplemented */ 
        }
        SPDK_NOTICELOG("main preocess exit; subprocess exit\n");
        exit(0);
    }
}

void handle_sigint(int sig) {
    SPDK_NOTICELOG("Get a interrupt sign, main process exit\n");
    exit(0); 
}

int xt_env_init(xt_admin_qpair *aqinfo){
    unsigned long long init_tick = 0;
    init_rand(&g_frand_state, 1);
    SPDK_NOTICELOG("init share memory for commnads logger\n");
    xt_init_share_memory();
    xt_init_commands_logger();
    if (signal(SIGINT, handle_sigint) == SIG_ERR) {
        SPDK_NOTICELOG("Can't handle sigint\n");
    }
    SPDK_NOTICELOG("init pcie for pcie deivce\n");
    if (xt_pcie_init(aqinfo) != 0){
        return -1;
    }
    if(strstr(aqinfo->engine_ops->name, "spdk") != NULL){
        aqinfo->sys_tick_hz = spdk_get_ticks_hz();
        g_tsc_rate = spdk_get_ticks_hz();
    }else{
        init_tick = spdk_get_ticks();
        spdk_delay_us(1000000);
        aqinfo->sys_tick_hz = spdk_get_ticks() - init_tick;
        g_tsc_rate = aqinfo->sys_tick_hz;
    }
    aqinfo->read_histogram = xt_histogram_data_alloc(); 
    aqinfo->write_histogram = xt_histogram_data_alloc();
    SPDK_NOTICELOG("Get the tick rate of %ld per second.\n", g_tsc_rate);
    bind_cpu_main_thread();
    return aqinfo->engine_ops->xt_engine_env_init(aqinfo);
}

void bind_cpu_main_thread(void){
    unsigned long long init_tick = spdk_get_ticks();
    int cpu = -1;
    int cpu_num = sysconf(_SC_NPROCESSORS_ONLN);
    cpu_set_t mask;
    do{
        cpu = sched_getcpu();
        if (cpu >= 0){
            break;
        }
    } while (spdk_get_ticks() - init_tick < g_tsc_rate);
    if(cpu >= 0){
        CPU_ZERO(&mask);
        CPU_SET(cpu, &mask);
        if (sched_setaffinity(0, sizeof(mask), &mask) == -1) {
            SPDK_NOTICELOG("set sched_setaffinity failed in first\n");
        }
        if (sched_setaffinity(0, sizeof(mask), &mask) == -1) {
            SPDK_NOTICELOG("set sched_setaffinity failed in second\n");
        }else{
            for(int i = 0; i < cpu_num; i ++){
                if (CPU_ISSET(i, &mask)){
                    SPDK_NOTICELOG("run cpu core %d, bind cpu core %d\n", i, cpu);
                }
            }
        }
    }else{
        SPDK_NOTICELOG("get cpu core from main thread failed\n");
    }
}

int xt_env_fini(xt_admin_qpair *aqinfo){
    spdk_vmd_fini();
    return aqinfo->engine_ops->xt_engine_env_fini(aqinfo);
}

void xt_device_destory(xt_admin_qpair *aqinfo){
    return aqinfo->engine_ops->xt_engine_device_destory(aqinfo);
}

int xt_device_init(xt_admin_qpair *aqinfo){
    return aqinfo->engine_ops->xt_engine_device_init(aqinfo);
}

int xt_device_fini(xt_admin_qpair *aqinfo){
    return aqinfo->engine_ops->xt_engine_device_fini(aqinfo);
}

int xt_nvme_device_subsystem_reset(xt_admin_qpair *aqinfo){
    if(aqinfo->device_info.admin_handle_id <= 0){
        SPDK_NOTICELOG("char device fid %d \n", aqinfo->device_info.admin_handle_id);
    }else{
        return ioctl(aqinfo->device_info.admin_handle_id, NVME_IOCTL_SUBSYS_RESET);
    }
    return -1;
}

int xt_nvme_device_reset(xt_admin_qpair *aqinfo){
    if(aqinfo->device_info.admin_handle_id <= 0){
        SPDK_NOTICELOG("char device fid %d \n", aqinfo->device_info.admin_handle_id);
    }else{
        return ioctl(aqinfo->device_info.admin_handle_id, NVME_IOCTL_RESET);
    }
    return -1;
}

xt_io_qpair *xt_qpair_create(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, int qprio, int qdepth){
    qinfo->aqinfo = aqinfo;
    if (qdepth > 65535){
        SPDK_ERRLOG("create qpair qdepth(%d) need less 65535\n", qdepth);
        return NULL;
    }
    /*int (*xt_engine_qpair_create)(xt_admin_qpair *, xt_io_qpair *, int , int )*/
    if(aqinfo->engine_ops->xt_engine_qpair_create(aqinfo, qinfo, qprio, qdepth) == 0){
        return qinfo;
    }
    else{
        return NULL;
    }    
}

int xt_qpair_free(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo){
    return aqinfo->engine_ops->xt_engine_qpair_free(qinfo);
}

void xt_qpair_destroy(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo){
    return aqinfo->engine_ops->xt_engine_qpair_destroy(qinfo);
}

int xt_completed_io_check(xt_admin_qpair *aqinfo, cmds_u* io_unit){
    bool check_status = true;
    // xt_buffer * _buf;
    if(io_unit->cmd_status != XT_CMD_UNIT_FREE){
        check_status = aqinfo->engine_ops->xt_engine_completed_io_check(io_unit);
        // _buf = io_unit->io_buffer;
        // if (NULL != _buf){
        //     _buf->buf_status = XT_BUFFER_FREE;
        // }
    }
    return check_status;
}

cmds_u *xt_prepare_io_unit(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo){
    return aqinfo->engine_ops->xt_engine_prepare_io_unit(qinfo);
}

void xt_submit_io_cmd(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, xt_buffer *buf, cmds_u *io_unit, unsigned int length, unsigned int lbacnt){
    io_unit->cmd_status = XT_CMD_UNIT_BUSY;
    aqinfo->engine_ops->xt_engine_submit_io_cmd(qinfo, buf, io_unit, length, lbacnt);
    io_unit->submit_index = qinfo->submit_count;
}

int xt_wait_completion_io(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, unsigned int max_completions){
    return aqinfo->engine_ops->xt_engine_wait_completion_io(qinfo, max_completions);
}

int xt_wait_qpair_all_submission_io_completion(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo){
    return aqinfo->engine_ops->xt_engine_wait_qpair_all_submission_io_completion(qinfo);
}

int xt_completed_admin_check(xt_admin_qpair *aqinfo, cmds_u* admin_unit){
    return aqinfo->engine_ops->xt_engines_completed_admin_check(admin_unit);
}

cmds_u *xt_prepare_admin_unit(xt_admin_qpair *aqinfo){
    return aqinfo->engine_ops->xt_engine_prepare_admin_unit(aqinfo);
}

void xt_submit_admin_cmd(xt_admin_qpair *aqinfo, xt_buffer *buf, cmds_u *admin_unit, unsigned int length){
    admin_unit->cmd_status = XT_CMD_UNIT_BUSY;
    return aqinfo->engine_ops->xt_engine_submit_admin_cmd(aqinfo, buf, admin_unit, length);
}

int xt_wait_completion_admin(xt_admin_qpair *aqinfo){
    return aqinfo->engine_ops->xt_engine_wait_completion_admin(aqinfo);
}

xt_engine_ops *xt_load_engine(char* engine_ops_name, xt_admin_qpair *aqinfo){
    xt_admin_qpair_check(aqinfo);
    if (engine_ops_name){
        /*change str to lower str */
        for (int i = 0; engine_ops_name[i] != '\0' && i < 64; i++) {
            if (isupper(engine_ops_name[i])) {
                engine_ops_name[i] = tolower(engine_ops_name[i]);
            }
        }
        aqinfo->engine_ops = xt_find_engine(engine_ops_name);
        return aqinfo->engine_ops;
    }
    if(NULL != aqinfo->engine_ops){
        SPDK_ERRLOG("Get a invalid engine name: %p, return null \n", engine_ops_name);
    }
    return aqinfo->engine_ops;
}

unsigned int xt_get_engine_io_sync_flag(xt_admin_qpair *aqinfo){
    xt_admin_qpair_check(aqinfo);
    if(NULL == aqinfo->engine_ops){
        SPDK_ERRLOG("%p not load engine\n", aqinfo);
    }else{
        return aqinfo->engine_ops->io_sync_flag;
    }
    return 0;
}

unsigned int xt_get_engine_admin_sync_flag(xt_admin_qpair *aqinfo){
    xt_admin_qpair_check(aqinfo);
    if(NULL == aqinfo->engine_ops){
        SPDK_ERRLOG("%p not load engine\n", aqinfo);
    }else{
        return aqinfo->engine_ops->admin_sync_flag;
    }
    return 0;    
}


unsigned long long get_system_ticks(void){
    return spdk_get_ticks();
}

void xt_delay_us(unsigned int delay_us){
    spdk_delay_us(delay_us);
}

void xt_set_io_timespec_timeout(xt_io_qpair *qinfo, unsigned int timeout){
    if(timeout > 1000000){
        qinfo->spec_timeout.tv_sec =  (unsigned int) timeout / 1000000;
        qinfo->spec_timeout.tv_nsec = (timeout - (unsigned int)timeout / 100000) * 1000;

    }else{
        qinfo->spec_timeout.tv_nsec = timeout  * 1000;
    }
}

void xt_set_admin_timespec_timeout(xt_admin_qpair *aqinfo, unsigned int timeout){
    if(timeout > 1000000){
        aqinfo->spec_timeout.tv_sec =  (unsigned int) timeout / 1000000;
        aqinfo->spec_timeout.tv_nsec = (timeout - (unsigned int)timeout / 100000) * 1000;

    }else{
        aqinfo->spec_timeout.tv_nsec = timeout  * 1000;
    }    
}

void xt_log_set_print_level(int level){
    spdk_log_set_print_level(level);
    spdk_log_set_level(level);
}

unsigned char xt_pcie_device_config_read8(xt_admin_qpair *aqinfo, unsigned int offset){
    assert (offset > 4096);
    unsigned char value;
    if(spdk_pci_device_cfg_read8(aqinfo->pcie_info, &value, offset)){
        SPDK_ERRLOG("Get pcie header with int: 0x%x \n", offset);
    }
    return value;
}

unsigned short xt_pcie_device_config_read16(xt_admin_qpair *aqinfo, unsigned int offset){
    assert (offset > 4096);
    unsigned short value;
    if(spdk_pci_device_cfg_read16(aqinfo->pcie_info, &value, offset)){
        SPDK_ERRLOG("Get pcie header with int: 0x%x \n", offset);
    }
    return value;
}

unsigned int xt_pcie_device_config_read32(xt_admin_qpair *aqinfo, unsigned int offset){

    assert (offset > 4096);
    unsigned int value;
    if(spdk_pci_device_cfg_read32(aqinfo->pcie_info, &value, offset)){
        SPDK_ERRLOG("Get pcie header with int: 0x%x \n", offset);
    }
    return value;
}
unsigned long long xt_pcie_device_config_read64(xt_admin_qpair *aqinfo, unsigned int offset){
    assert (offset > 4096);
    unsigned long long value;
    if(spdk_pci_device_cfg_read(aqinfo->pcie_info, &value, 8, offset)){
        SPDK_ERRLOG("Get pcie header with int: 0x%x \n", offset);
    }
    return value;
}

void xt_pcie_device_config_write8(xt_admin_qpair *aqinfo, unsigned int offset, unsigned char value){
    assert (offset > 4096);
    if(spdk_pci_device_cfg_write8(aqinfo->pcie_info, value, offset)){
        SPDK_ERRLOG("Set pcie header with int: 0x%x  value 0x%x\n", offset, value);
    }
}

void xt_pcie_device_config_write16(xt_admin_qpair *aqinfo, unsigned int offset, unsigned short value){
    assert (offset > 4096);
    if(spdk_pci_device_cfg_write16(aqinfo->pcie_info, value, offset)){
        SPDK_ERRLOG("Set pcie header with int: 0x%x  value 0x%x\n", offset, value);
    }
}

void xt_pcie_device_config_write32(xt_admin_qpair *aqinfo, unsigned int offset, unsigned int value){
    assert (offset > 4096);
    if(spdk_pci_device_cfg_write32(aqinfo->pcie_info, value, offset)){
        SPDK_ERRLOG("Set pcie header with int: 0x%x  value 0x%x\n", offset, value);
    }
}

void xt_pcie_device_config_write64(xt_admin_qpair *aqinfo, unsigned int offset, unsigned long long value){
    assert (offset > 4096);
    if(spdk_pci_device_cfg_write(aqinfo->pcie_info, (void *)&value, 8, offset)){
        SPDK_ERRLOG("Set pcie header with int: 0x%x  value 0x%llx\n", offset, value);
    }
}

unsigned char xt_nvme_register_read8(xt_admin_qpair *aqinfo, unsigned int offset){
    if(aqinfo->nvme_regs != NULL){
        assert (offset > 4096);
        read_barrier();
        return *(unsigned char *)(aqinfo->nvme_regs + offset);
    }else{
        SPDK_ERRLOG("Get pcie header with char: 0x%x \n", offset);
        assert(0);       
    }
    return -1;
}

unsigned short xt_nvme_register_read16(xt_admin_qpair *aqinfo, unsigned int offset){
    if(aqinfo->nvme_regs != NULL){
        assert (offset > 4096);
        read_barrier();
        return *(unsigned short *)(aqinfo->nvme_regs + offset);
    }else{
        SPDK_ERRLOG("Get pcie header with short: 0x%x \n", offset);
        assert(0);       
    }
    return -1;
}

unsigned int xt_nvme_register_read32(xt_admin_qpair *aqinfo, unsigned int offset){
    if(aqinfo->nvme_regs != NULL){
        assert (offset > 4096);
        read_barrier();
        return *(unsigned int *)(aqinfo->nvme_regs + offset);
    }else{
        SPDK_ERRLOG("Get pcie header with int: 0x%x \n", offset);
        assert(0);   
    }
    return -1;
}

unsigned long long xt_nvme_register_read64(xt_admin_qpair *aqinfo, unsigned int offset){
    if(aqinfo->nvme_regs != NULL){
        assert (offset > 4096);
        read_barrier();
        return *(unsigned long long *)(aqinfo->nvme_regs + offset);
    }else{
        SPDK_ERRLOG("Get pcie header with long: 0x%x \n", offset);
        assert(0);       
    }
    return -1;
}

void xt_nvme_register_write8(xt_admin_qpair *aqinfo, unsigned int offset, unsigned char value){
    if(aqinfo->nvme_regs != NULL){
        assert (offset > 4096);
        write_barrier();
        *(unsigned char *)(aqinfo->nvme_regs + offset) = value;
    }else{
        SPDK_ERRLOG("Get pcie header with char: 0x%x \n", offset);
        assert(0);       
    } 
}

void xt_nvme_register_write16(xt_admin_qpair *aqinfo, unsigned int offset, unsigned short value){
    if(aqinfo->nvme_regs != NULL){
        assert (offset > 4096);
        write_barrier();
        *(unsigned short *)(aqinfo->nvme_regs + offset) = value;
    }else{
        SPDK_ERRLOG("Get pcie header with short: 0x%x \n", offset);
        assert(0);       
    }
}

void xt_nvme_register_write32(xt_admin_qpair *aqinfo, unsigned int offset, unsigned int value){
    if(aqinfo->nvme_regs != NULL){
        assert (offset > 4096);
        write_barrier();
        *(unsigned int *)(aqinfo->nvme_regs + offset) = value;
    }else{
        SPDK_ERRLOG("Get pcie header with int: 0x%x \n", offset);
        assert(0);       
    }
}

void xt_nvme_register_write64(xt_admin_qpair *aqinfo, unsigned int offset, unsigned long long value){
    if(aqinfo->nvme_regs != NULL){
        assert (offset > 4096);
        write_barrier();
        *(unsigned long long *)(aqinfo->nvme_regs + offset) = value;
    }else{
        SPDK_ERRLOG("Get pcie header with long: 0x%x \n", offset);
        assert(0);       
    }
}

int xt_pcie_bar_map(xt_admin_qpair *aqinfo, unsigned int bir){
    void *addr;
    int rc;
    /*	int (*map_bar)(struct spdk_pci_device *dev, uint32_t bar, void **mapped_addr, uint64_t *phys_addr, uint64_t *size);*/
    rc = aqinfo->pcie_info->map_bar(aqinfo->pcie_info, bir, &addr, (uint64_t *)&aqinfo->bar_phys_addr, (uint64_t *)&aqinfo->bar_size);
    SPDK_NOTICELOG("map pcie bar: bar:0x%x addr:%p bar_phys_addr:0x%llx bar_size: 0x%llx map command return %d \n", bir, addr, \
                    aqinfo->bar_phys_addr, aqinfo->bar_size, rc);
    return rc;
}

int xt_pcie_bar_unmap(xt_admin_qpair *aqinfo, unsigned int bir){
    int rc;
    void * bar_address = (void *)aqinfo->bar_address;
    rc = aqinfo->pcie_info->unmap_bar(aqinfo->pcie_info, bir, bar_address); 
    if (rc == 0){
        aqinfo->bir = 0;
        aqinfo->bar_address = 0;
        aqinfo->bar_phys_addr = 0;
        aqinfo->bar_size = 0;
    }
    return rc;
}

void xt_pcie_get_bar_data(xt_admin_qpair *aqinfo, void * bar_addr){
    write_barrier();
    memcpy(bar_addr, (const void *)aqinfo->bar_address, aqinfo->bar_size);
}

void check_cutoff(void *ctx, uint64_t start, uint64_t end, uint64_t count, uint64_t total, uint64_t so_far)
{
	double so_far_pct;
	double **cutoff = ctx;

	if (count == 0) {
		return;
	}

	so_far_pct = (double)so_far / total;
	while (so_far_pct >= **cutoff && **cutoff > 0) {
        if(**cutoff * 100 >= 10){
            printf("%9.7f%% : %9.3fus\n", **cutoff * 100, (double)end * 1000 * 1000 / g_tsc_rate);
        }else{
            printf("%9.8f%% : %9.3fus\n", **cutoff * 100, (double)end * 1000 * 1000 / g_tsc_rate);
        }
		(*cutoff)++;
	}
}

void print_bucket(void *ctx, uint64_t start, uint64_t end, uint64_t count, uint64_t total, uint64_t so_far)
{
    int print_with = 18;
    int init_end_width = 0;
	double so_far_pct;
    double init_start_us = (double)start * 1000 * 1000 / g_tsc_rate;
    double init_end_us = (double)end * 1000 * 1000 / g_tsc_rate;
    double _init_end_us = init_end_us;
    while (_init_end_us / 10 >= 1)
    {
        _init_end_us = _init_end_us / 10;
        init_end_width ++;
    }
    init_end_width += 1;
    print_with = init_end_width >= print_with ? init_end_width + 1: print_with;
    int space_count = print_with - init_end_width;
    space_count = space_count > 1 ? space_count: 1;
	if (count == 0) {
		return;
	}
	so_far_pct = (double)so_far * 100 / total;
    if (so_far_pct >= 99.999999){
        printf("%*.6f - %*.6f %*.s %4.5f%%      (%12ju)\n", print_with, init_start_us, init_end_width, init_end_us, 
                space_count , " ", so_far_pct, count);
    }else{
        if (so_far_pct >= 10){
            printf("%*.6f - %*.6f %*.s %4.6f%%      (%12ju)\n", print_with, init_start_us, init_end_width, init_end_us, 
                    space_count, " ", so_far_pct, count);
        }else{
            printf("%*.6f - %*.6f %*.s %4.7f%%      (%12ju)\n", print_with, init_start_us, init_end_width, init_end_us, 
                    space_count, " ", so_far_pct, count);
        }
    }
}

void print_latency_histogram(xt_admin_qpair *aqinfo, unsigned int latency_summary, unsigned int latency_histogram){
    const double *cutoff = g_latency_cutoffs;
    bool read_histogram_empty, write_histogram_empty;
    if(aqinfo->histogram_flag){
        read_histogram_empty = xt_histogram_empty_check(aqinfo->read_histogram);
        if (!read_histogram_empty){
            if(latency_summary){
                printf("=================================================================================================\n");
                printf("                           summary read command latency histogram                     \n");
                xt_histogram_data_iterate(aqinfo->read_histogram, check_cutoff, &cutoff);
            }
            if(latency_histogram){
                printf("=================================================================================================\n");
                printf("                               read command latency histogram                        \n");
                printf("              Range in us                       Cumulative       IO count\n");
                xt_histogram_data_iterate(aqinfo->read_histogram, print_bucket, NULL);
            }
        }
        write_histogram_empty = xt_histogram_empty_check(aqinfo->write_histogram);
        if (!write_histogram_empty){
            if(latency_summary){
                printf("=================================================================================================\n");
                printf("                           summary write command latency histogram                     \n");
                xt_histogram_data_iterate(aqinfo->write_histogram, check_cutoff, &cutoff);
            }
            if(latency_histogram){
                printf("=================================================================================================\n");
                printf("                               write command latency histogram                        \n");
                printf("              Range in us                       Cumulative       IO count\n");
                xt_histogram_data_iterate(aqinfo->write_histogram, print_bucket, NULL);
            }
        }
        if(write_histogram_empty && read_histogram_empty){
            SPDK_NOTICELOG("no data for histogram \n");
        }
    }else{
        SPDK_NOTICELOG("no data for histogram \n");
    }
}

void xt_io_histogram_reset(xt_admin_qpair *aqinfo){
    if(aqinfo->histogram_flag){
        xt_histogram_data_reset(aqinfo->read_histogram);
        xt_histogram_data_reset(aqinfo->write_histogram);
    }else{
        SPDK_NOTICELOG("no data for histogram \n");
    }
}

unsigned long long get_total_read_size(void){
	return g_xt_cmd_log->cmds_log_header.total_read_size;
}

unsigned long long get_total_write_size(void){
	return g_xt_cmd_log->cmds_log_header.total_write_size;
}

unsigned long long get_total_iops_count(void){
	return g_xt_cmd_log->cmds_log_header.total_iops_count;
}

unsigned long long get_total_io_size(void){
	return g_xt_cmd_log->cmds_log_header.total_io_size;
}