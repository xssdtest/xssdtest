# cython: language_level=3
cdef extern from "./src/xt_rand.h":
    ctypedef struct frand_state:
        pass

    ctypedef struct gauss_state:
        pass

    ctypedef struct xt_lcg_random:
        unsigned long long a_multiplier
        unsigned long long c_increment
        unsigned long long m_modulus
        unsigned long long m_mark
        unsigned long long count
        unsigned long long next
        unsigned long long offset
        unsigned long long max_value
        unsigned int x0
        unsigned int step
        unsigned int step_is_pow
        unsigned int sub_next
        unsigned int *sub_step_arrays
        unsigned int *sub_step_summary_arrays
        unsigned int sub_m_modulus
        unsigned int sub_m_mark
        unsigned int sub_summary
        unsigned int sub_count
        unsigned int sub_a_multiplier
        unsigned int sub_c_increment
        unsigned int sub_step_summary
        unsigned long long sub_range_count
        unsigned long long sub_stop
        unsigned long long lcg_count
        unsigned long long lcg_range

    unsigned long long rand64()

    unsigned int rand32()

    double xt_random()

    void init_rand(frand_state *, bool)

    void reset_rand_seed(unsigned int seed, unsigned int use64)

    void init_rand_seed(frand_state *, unsigned int seed, unsigned int)

    void gauss_init(gauss_state *gs, unsigned long long nranges, double dev)

    unsigned long long gauss_next()

    void gauss_disable_hash()

    void init_lcg_random(xt_lcg_random * lcg_random, unsigned int x0, unsigned long long m_modulus, unsigned long long c_increment,
                         unsigned long long a_multiplier, unsigned long long offset, unsigned long long max_value, unsigned int step,
                         unsigned int *sub_step_arrays, unsigned int sub_step_count)

    xt_lcg_random *get_lcg_random()

    void free_sub_lcg(xt_lcg_random * lcg_random)

    unsigned long long lcg_next(xt_lcg_random * lcg_random)

    unsigned long long roundup_pow2(unsigned long long value)

    unsigned long long lcg_next_start(xt_lcg_random * lcg_random)

cdef extern from "./src/xt_memory.h":
    ctypedef struct pthread_mutex_t:
        pass

    ctypedef struct xt_verify_tailer:
        unsigned long long slba
        unsigned int buf_index
        unsigned int tailer_xor

    ctypedef struct xt_buffer:
        void * _raw_buf
        void * buf
        void * physic_buf
        void * io_tracker
        void * _data_integrity_extension_raw
        void * data_integrity_extension
        unsigned long long seed
        unsigned long long buf_crc512[8]
        unsigned long long buf_crc4096
        unsigned int buf_length
        unsigned int buf_align
        unsigned int buf_type
        unsigned int alloc_type
        unsigned int pi_type
        unsigned int sector_size
        unsigned int meta_sector_size
        unsigned int buf_index
        unsigned int buf_change
        unsigned int buf_status
        unsigned int io_tracker_length
        xt_verify_tailer io_tailer[8]
        pthread_mutex_t buffer_lock


    int xt_buffer_init(xt_buffer *buffer, unsigned int buf_length, unsigned int buf_align, unsigned int alloc_type, unsigned int mem_init)

    int xt_buffer_free(xt_buffer *buffer)

    void *xt_buffer_alloc_memory(unsigned int alloc_type, unsigned int buf_length)

    void xt_buffer_alloc_free(unsigned int alloc_type, void * raw_buf)

    unsigned char xt_buffer_crc8(xt_buffer *buffer, unsigned int buf_offset, unsigned int buf_length)

    unsigned short xt_buffer_crc16(xt_buffer *buffer, unsigned int buf_offset, unsigned int buf_length)

    unsigned int xt_buffer_crc32(xt_buffer *buffer, unsigned int buf_offset, unsigned int buf_length)

    unsigned long long xt_buffer_crc64(xt_buffer *buffer, unsigned int buf_offset, unsigned int buf_length)

    void xt_buffer_init_crc(xt_buffer *buffer, unsigned int crc_type)

    void xt_set_uint8(void *buffer, unsigned int buf_offset, unsigned char value, int type)

    unsigned char xt_get_uint8(void *buffer, unsigned int buf_offset, int type)

    void xt_set_uint16(void *buffer, unsigned int buf_offset, unsigned short value, int type)

    unsigned short xt_get_uint16(void *buffer, unsigned int buf_offset, int type)

    void xt_set_uint32(void *buffer, unsigned int buf_offset, unsigned int value, int type)

    unsigned int xt_get_uint32(void *buffer, unsigned int buf_offset, int type)

    void xt_set_uint64(void *buffer, unsigned int buf_offset, unsigned long long value, int type)

    unsigned long long xt_get_uint64(void *buffer, unsigned int buf_offset, int type)

    void xt_buffer_get_init_io_tailer(xt_buffer *buffer)

    int xt_buffer_reset_init_io_tailer(xt_buffer *buffer)

    int xt_buffer_set_io_tracker(xt_buffer *buffer, unsigned int io_tracker_length, unsigned int io_tracker_type)

    int xt_buffer_dif_generate(xt_buffer *buffer)

    int xt_buffer_dif_init(xt_buffer *buffer, unsigned int meta_sector_size, unsigned int sector_size)

    int xt_buffer_dix_generate(xt_buffer *buffer)

    int xt_buffer_dix_init(xt_buffer *buffer, unsigned int meta_sector_size)

    unsigned char * get_xt_buffer(xt_buffer *buffer)

    void memory_dump(const void *addr, int length, int step, int dump_file, char * file_name)

    void* xt_allocate_aligned_memory(unsigned int size, unsigned int alignment)

    void xt_free_aligned_memory(void* aligned_ptr)

cdef extern from "./src/xt_cmds_u.h":
    ctypedef enum:
        XT_CMD_UNIT_FREE
        XT_CMD_UNIT_BUSY
        XT_CMD_UNIT_COMPLETED

    ctypedef struct xt_nvme_status:
        unsigned short raw

    ctypedef struct xt_iocb:
        pass

    ctypedef struct cmds_u_ring:
        unsigned int head
        unsigned int tail
        unsigned int max
        unsigned int nr
        unsigned int ring_next
        unsigned int io_u_next
        cmds_u **ring

    ctypedef struct cmds_u:
        unsigned char opc
        unsigned char flags
        unsigned short cid
        unsigned int nsid
        unsigned int cdw2
        unsigned int cdw3
        unsigned long long mptr
        unsigned long long prp1
        unsigned long long prp2
        unsigned int cdw10
        unsigned int cdw11
        unsigned int cdw12
        unsigned int cdw13
        unsigned int cdw14
        unsigned int cdw15
        unsigned int timeout_ms
        unsigned int rsvd4
        unsigned long long result
        unsigned long long cb_func
        unsigned int cpl_cdw0
        unsigned int cpl_rsvd1
        unsigned short cpl_sqhd
        unsigned short cpl_sqid
        unsigned short cpl_cid
        xt_nvme_status cpl_status
        cmds_u_ring *  completed_cmds_u_ring

        unsigned long long start_time
        unsigned long long issue_time
        unsigned long long complete_time
        unsigned long long submit_index
        xt_io_qpair * qpair_info
        unsigned int cmd_status
        unsigned int io_status_code_expected
        unsigned int io_status_code_type_expected
        unsigned int sector_size
        unsigned int meta_sector_size
        unsigned int io_tailer_flag
        unsigned int pi_type

        int rc
        xt_buffer * io_buffer
        unsigned int excepted_write_check
        unsigned int excepted_write_buffer_index
        unsigned int xt_buffer_offset
        xt_iocb *iocb

    ctypedef struct random_io_entry:
        unsigned long long slba
        unsigned int lbacnt
        unsigned int nsid
        unsigned int sector_size
        unsigned int meta_sector_size
        unsigned int buf_index
        unsigned char opcode

    random_io_entry *xt_io_entry_init(unsigned int count)

    void xt_io_entry_fini(random_io_entry *io_entrys)

    void xt_io_entry_shuffle(random_io_entry *io_entrys, unsigned int count, unsigned int reset_seed)

    int cmds_u_rempty(cmds_u_ring *ring)

    cmds_u *cmds_u_rpop(cmds_u_ring *r)

    cmds_u *cmds_u_get_ring_next(cmds_u_ring *r, unsigned int init_next)

    cmds_u *cmds_u_get_io_u_next(cmds_u_ring *r, unsigned int init_next)

    void cmds_u_rpush(cmds_u_ring *r, cmds_u *cmd_u)

    int cmds_u_rinit(cmds_u_ring *ring, unsigned int nr)

    void cmds_u_rexit(cmds_u_ring *ring)

    void cmds_u_rreset(cmds_u_ring *ring)

    int xt_read_data_verify(cmds_u* io_u)

    cmds_u *xt_prepare_io_unit_with_engine(xt_io_qpair *qinfo)

    cmds_u *xt_prepare_admin_unit_with_engine(xt_admin_qpair *aqinfo)


cdef extern from "./src/xssdtest.h":
    ctypedef struct xt_qpair:
        pass

    ctypedef struct xt_ctrlr:
        pass

    ctypedef struct xt_pcie:
        pass

    ctypedef struct xt_histogram_data:
        pass

    ctypedef struct xt_engine_ops:
        pass

    ctypedef struct xt_pci_addr:
        pass

    ctypedef struct xt_timespec:
        pass

    ctypedef struct xt_char_device_info:
        pass

    ctypedef struct xt_engines:
        pass

    ctypedef struct xt_admin_qpair:
        cmds_u * admin_units
        cmds_u_ring * completed_cmds_u_ring
        cmds_u_ring * submit_cmds_u_ring

        # unsigned int    engine_type
        int             pid
        unsigned long long sys_tick_hz
        unsigned long long timeout
        unsigned int qpair_iodepth
        unsigned int qpair_is_pow2

        xt_pci_addr *   pci_whitelist
        unsigned int    spdk_mem_size

        xt_ctrlr *ctrlr
        xt_pcie *pcie_info
        char traddr[64]
        void * nvme_regs
        unsigned int    bir
        void * bar_address
        unsigned long long   bar_size
        unsigned long long   bar_phys_addr
        unsigned int io_unit_clear_size

        unsigned int histogram_flag
        xt_histogram_data	*read_histogram
        xt_histogram_data	*write_histogram
        xt_timespec spec_timeout
        xt_char_device_info device_info
        xt_engines *engine_names

    void xt_admin_init(xt_admin_qpair *aqinfo, char * pcie_list,  int pcie_count)

    unsigned long long xt_admin_get_bar_size(xt_admin_qpair *aqinfo)

    unsigned long long xt_sys_tick_us(xt_admin_qpair *aqinfo)

    int xt_env_init(xt_admin_qpair *aqinfo)

    int xt_env_fini(xt_admin_qpair *aqinfo)

    void xt_device_destory(xt_admin_qpair *aqinfo)

    int xt_device_init(xt_admin_qpair *aqinfo)

    int xt_device_fini(xt_admin_qpair *aqinfo)

    int xt_nvme_device_subsystem_reset(xt_admin_qpair *aqinfo)

    int xt_nvme_device_reset(xt_admin_qpair *aqinfo)

    xt_io_qpair *xt_qpair_create(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, int qprio, int qdepth)

    int xt_qpair_free(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo)

    void xt_qpair_destroy(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo)

    int xt_completed_io_check(xt_admin_qpair *aqinfo, cmds_u* io_unit)

    cmds_u *xt_prepare_io_unit(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo)

    void xt_submit_io_cmd(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, xt_buffer *buf, cmds_u *io_unit, unsigned int length, unsigned int lbacnt)

    int xt_wait_completion_io(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo, unsigned int max_completions)

    int xt_wait_qpair_all_submission_io_completion(xt_admin_qpair *aqinfo, xt_io_qpair *qinfo)

    int xt_completed_admin_check(xt_admin_qpair *aqinfo, cmds_u* admin_unit)

    cmds_u *xt_prepare_admin_unit(xt_admin_qpair *aqinfo)

    void xt_submit_admin_cmd(xt_admin_qpair *aqinfo, xt_buffer *buf, cmds_u *admin_unit, unsigned int length)

    int xt_wait_completion_admin(xt_admin_qpair *aqinfo)

    xt_engine_ops *xt_load_engine(char* engine_ops_name, xt_admin_qpair *aqinfo)

    unsigned int xt_get_engine_io_sync_flag(xt_admin_qpair *aqinfo)

    unsigned int xt_get_engine_admin_sync_flag(xt_admin_qpair *aqinfo)

    unsigned long long get_system_ticks()

    unsigned char xt_pcie_device_config_read8(xt_admin_qpair *aqinfo, unsigned int offset)

    unsigned short xt_pcie_device_config_read16(xt_admin_qpair *aqinfo, unsigned int offset)

    unsigned int xt_pcie_device_config_read32(xt_admin_qpair *aqinfo, unsigned int offset)

    unsigned long long xt_pcie_device_config_read64(xt_admin_qpair *aqinfo, unsigned int offset)

    void xt_pcie_device_config_write8(xt_admin_qpair *aqinfo, unsigned int offset, unsigned char value)

    void xt_pcie_device_config_write16(xt_admin_qpair *aqinfo, unsigned int offset, unsigned short value)

    void xt_pcie_device_config_write32(xt_admin_qpair *aqinfo, unsigned int offset, unsigned int value)

    void xt_pcie_device_config_write64(xt_admin_qpair *aqinfo, unsigned int offset, unsigned long long value)

    unsigned char xt_nvme_register_read8(xt_admin_qpair *aqinfo, unsigned int offset)

    unsigned short xt_nvme_register_read16(xt_admin_qpair *aqinfo, unsigned int offset)

    unsigned int xt_nvme_register_read32(xt_admin_qpair *aqinfo, unsigned int offset)

    unsigned long long xt_nvme_register_read64(xt_admin_qpair *aqinfo, unsigned int offset)

    void xt_nvme_register_write8(xt_admin_qpair *aqinfo, unsigned int offset, unsigned char value)

    void xt_nvme_register_write16(xt_admin_qpair *aqinfo, unsigned int offset, unsigned short value)

    void xt_nvme_register_write32(xt_admin_qpair *aqinfo, unsigned int offset, unsigned int value)

    void xt_nvme_register_write64(xt_admin_qpair *aqinfo, unsigned int offset, unsigned long long value)

    int xt_pcie_bar_map(xt_admin_qpair *aqinfo, unsigned int bir)

    int xt_pcie_bar_unmap(xt_admin_qpair *aqinfo, unsigned int bir)

    int xt_pcie_get_bar_data(xt_admin_qpair *aqinfo, void * bar_addr)

    void print_latency_histogram(xt_admin_qpair *aqinfo, unsigned int latency_summary, unsigned int latency_histogram)

    void xt_io_histogram_reset(xt_admin_qpair *aqinfo)

    void xt_delay_us(unsigned int delay_us)

    void xt_set_io_timespec_timeout(xt_io_qpair *qinfo, unsigned int timeout)

    void xt_set_admin_timespec_timeout(xt_admin_qpair *aqinfo, unsigned int timeout)

    void xt_log_set_print_level(int level)

    unsigned long long get_total_read_size()

    unsigned long long get_total_write_size()

    unsigned long long get_total_iops_count()

    unsigned long long get_total_io_size()

    char * get_engine_names()

    unsigned int reload_engine_check(const char *src_engine, const char *dest_engine)

cdef extern from "./src/xt_io_qpair.h":

    ctypedef struct io_context_t:
        pass

    ctypedef struct io_event:
        pass

    ctypedef struct xt_io_qpair:
        xt_qpair *qpair
        xt_admin_qpair * aqinfo
        unsigned int qpair_id
        int reap_type
        unsigned int io_check_type
        unsigned int current_iodepth_count
        unsigned int qpair_iodepth
        unsigned long long timeout
        unsigned long long last_tick_recover
        unsigned long long completed_check_index
        unsigned long long qpair_completions
        unsigned long long submit_count
        unsigned long long last_submit_count
        unsigned long long limit_iops_count
        unsigned long long last_second_iops_count
        unsigned long long limit_io_count
        unsigned long long last_second_total_io_count
        unsigned long long last_second_total_tick
        unsigned int microseconds_delay
        cmds_u * io_units
        cmds_u_ring * completed_cmds_u_ring
        cmds_u_ring * submit_cmds_u_ring     # recover submit io info
        unsigned long long io_u_submit_map[8]
        unsigned long long io_u_complete_map[8]


        xt_buffer ** write_buf_addr_list
        xt_lcg_random * io_lcg
        xt_lcg_random * write_lcg
        xt_lcg_random * read_lcg

        int fid
        unsigned int nsid
        xt_timespec spec_timeout
        io_context_t aio_ctx
        io_event *aio_events
        xt_iocb **iocbs
        void (* wait_submit_command_function) (void *)
        void * wait_submit_command_args


    void xt_io_qpair_init(xt_io_qpair *qinfo, unsigned int qpair_iodepth, cmds_u * io_units, cmds_u_ring * completed_cmds_u_ring,
                          unsigned long long completed_check_index, unsigned long long submit_count, unsigned long long qpair_completions)

    void xt_set_io_qpair_polling_status(xt_io_qpair *qinfo, xt_admin_qpair * aqinfo, int reap_type, unsigned int io_check_type,
                                        unsigned int current_iodepth_count, unsigned long long timeout, unsigned long long limit_iops_count,
                                        unsigned long long limit_io_count, unsigned int microseconds_delay)

    void xt_io_qpair_lcg_init(xt_io_qpair *qinfo, unsigned int x0, unsigned long long m_modulus, unsigned long long c_increment,
                              unsigned long long a_multiplier, unsigned long long offset, unsigned long long max_value,
                              unsigned int step, unsigned int lcg_type)

    void xt_io_qpair_lcg_fini(xt_io_qpair *qinfo)
    void xt_char_device_info_init(xt_admin_qpair * aqinfo, const char * char_device_name, unsigned int size, unsigned int nsid_count)

    void xt_char_device_update_info(xt_admin_qpair * aqinfo, const char * char_device_name, unsigned int size)

    void xt_update_ctrl_data(xt_admin_qpair * aqinfo, void * ctrl_data)

    unsigned int xt_get_mdts(xt_admin_qpair * aqinfo)

    void xt_update_ns_data(xt_admin_qpair * aqinfo, void * ns_data, unsigned int nsid)

    unsigned int xt_get_ns_sector_size(xt_admin_qpair * aqinfo, unsigned int nsid)

    unsigned int xt_get_ns_meta_data_size(xt_admin_qpair * aqinfo, unsigned int nsid)

    void xt_block_device_update_info(xt_admin_qpair * aqinfo, const char * block_device_name, unsigned int size, unsigned int nsid, unsigned int clear_next_open_index)

    int xt_device_open(xt_admin_qpair * aqinfo, char * path, unsigned int nsid)

    void xt_device_close(xt_admin_qpair * aqinfo)

    void xt_char_device_info_fini(xt_admin_qpair * aqinfo)

    void xt_io_qpair_reset(xt_io_qpair *qinfo, unsigned long long qpair_completions, unsigned long long submit_count,
                           unsigned long long completed_check_index)

    void xt_io_qpair_timeout(xt_io_qpair *qinfo, unsigned long long timeout)

    int xt_check_qpair_completioned(xt_io_qpair *qinfo)

    unsigned long long xt_io_qpair_get_qpair_completions(xt_io_qpair *qinfo)

    void xt_io_qpair_reset_qpair_completions(xt_io_qpair *qinfo)

    void xt_io_qpair_init_write_buffer_addr_list(xt_io_qpair *qinfo, xt_buffer ** write_buf_addr_list)

    unsigned int xt_get_io_qpair_id(xt_io_qpair *qinfo)

    cmds_u_ring * xt_io_qpair_get_completed_cmds_u_ring(xt_io_qpair *qinfo)

    void xt_dump_io_unit(xt_io_qpair *qinfo)