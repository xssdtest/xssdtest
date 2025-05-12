/*
  This is a maximally equidistributed combined Tausworthe generator
  based on code from GNU Scientific Library 1.5 (30 Jun 2004)

   x_n = (s1_n ^ s2_n ^ s3_n)

   s1_{n+1} = (((s1_n & 4294967294) <<12) ^ (((s1_n <<13) ^ s1_n) >>19))
   s2_{n+1} = (((s2_n & 4294967288) << 4) ^ (((s2_n << 2) ^ s2_n) >>25))
   s3_{n+1} = (((s3_n & 4294967280) <<17) ^ (((s3_n << 3) ^ s3_n) >>11))

   The period of this generator is about 2^88.

   From: P. L'Ecuyer, "Maximally Equidistributed Combined Tausworthe
   Generators", Mathematics of Computation, 65, 213 (1996), 203--213.

   This is available on the net from L'Ecuyer's home page,

   http://www.iro.umontreal.ca/~lecuyer/myftp/papers/tausme.ps
   ftp://ftp.iro.umontreal.ca/pub/simulation/lecuyer/papers/tausme.ps

   There is an erratum in the paper "Tables of Maximally
   Equidistributed Combined LFSR Generators", Mathematics of
   Computation, 68, 225 (1999), 261--269:
   http://www.iro.umontreal.ca/~lecuyer/myftp/papers/tausme2.ps

        ... the k_j most significant bits of z_j must be non-
        zero, for each j. (Note: this restriction also applies to the
        computer code given in [4], but was mistakenly not mentioned in
        that paper.)

   This affects the seeding procedure by imposing the requirement
   s1 > 1, s2 > 7, s3 > 15.

*/

#include <string.h>
#include "spdk_internal/log.h"
#include "../spdk/lib/nvme/nvme_internal.h"
#include "xt_rand.h"

int arch_random;
struct frand_state g_frand_state;
struct gauss_state g_gauss_state;
xt_lcg_random g_lcg;

static inline uint64_t __seed(uint64_t x, uint64_t m)
{
	return (x < m) ? x + m : x;
}

static void __init_rand32(struct taus88_state *state, unsigned int seed)
{
	int cranks = 6;

#define LCG(x, seed)  ((x) * 69069 ^ (seed))

	state->s1 = __seed(LCG((2^31) + (2^17) + (2^7), seed), 1);
	state->s2 = __seed(LCG(state->s1, seed), 7);
	state->s3 = __seed(LCG(state->s2, seed), 15);

	while (cranks--)
		__rand32(state);
}

static void __init_rand64(struct taus258_state *state, uint64_t seed)
{
	int cranks = 6;

#define LCG64(x, seed)  ((x) * 6906969069ULL ^ (seed))

	state->s1 = __seed(LCG64((2^31) + (2^17) + (2^7), seed), 1);
	state->s2 = __seed(LCG64(state->s1, seed), 7);
	state->s3 = __seed(LCG64(state->s2, seed), 15);
	state->s4 = __seed(LCG64(state->s3, seed), 33);
	state->s5 = __seed(LCG64(state->s4, seed), 49);

	while (cranks--)
		__rand64(state);
}

void init_rand(struct frand_state *state, bool use64)
{
	if(NULL == state){
		state = &g_frand_state;
	}
	state->use64 = use64;

	if (!use64)
		__init_rand32(&state->state32, 1);
	else
		__init_rand64(&state->state64, 1);
}

void init_rand_seed(struct frand_state *state, unsigned int seed, unsigned int use64)
{
	if(NULL == state){
		state = &g_frand_state;
	}
	state->use64 = use64;
	if (!use64)
		__init_rand32(&state->state32, seed);
	else
		__init_rand64(&state->state64, seed);
}

void reset_rand_seed(unsigned int seed, unsigned int use64){
	init_rand_seed(&g_frand_state, seed, use64);
}

double xt_random(void){
	if (g_frand_state.use64) {
		uint64_t val = __rand64(&g_frand_state.state64);
		return (val + 1.0) / (FRAND64_MAX + 1.0);
	} else {
		uint32_t val = __rand32(&g_frand_state.state32);
		return (val + 1.0) / (FRAND32_MAX + 1.0);
	}
}

static int gauss_dev(void)
{
	unsigned int r;
	int vr;

	if (!g_gauss_state.stddev)
		return 0;

	r = __rand32(&g_frand_state.state32);
	vr = g_gauss_state.stddev * (r / (FRAND32_MAX + 1.0));

	return vr - g_gauss_state.stddev / 2;
}

unsigned long long gauss_next(void)
{
	unsigned long long sum = 0;
	int i;

	for (i = 0; i < GAUSS_ITERS; i++)
		sum += __rand32(&g_frand_state.state32) % (g_gauss_state.nranges + 1);

	sum = (sum + GAUSS_ITERS - 1) / GAUSS_ITERS;

	if (g_gauss_state.stddev) {
		int dev = gauss_dev();

		while (dev + sum >= g_gauss_state.nranges)
			dev /= 2;
		sum += dev;
	}

	// if (!gs->disable_hash)
	// 	sum = __hash_u64(sum);

	return sum % g_gauss_state.nranges;
}

void gauss_init(struct gauss_state *gs, unsigned long nranges, double dev)
{
	if(NULL == gs){
		gs = &g_gauss_state;
	}
	memset(gs, 0, sizeof(*gs));
	// gs->r = &g_frand_state;
	// init_rand_seed(gs->r, seed, 0);
	gs->nranges = nranges;
	if (dev != 0.0) {
		gs->stddev = ceil((double) (nranges * 100.0) / dev);
		if (gs->stddev > nranges / 2)
			gs->stddev = nranges / 2;
	}
}

void gauss_disable_hash(void)
{
	g_gauss_state.disable_hash = true;
}

void init_lcg_random(xt_lcg_random * lcg_random, unsigned int x0, unsigned long long m_modulus, unsigned long long c_increment, 
					 unsigned long long a_multiplier, unsigned long long offset, unsigned long long max_value, unsigned int step,
					 unsigned int *sub_step_arrays, unsigned int sub_step_count){
	unsigned int sub_summary = 0;
	unsigned long long range_count;
	if (NULL == lcg_random){
		lcg_random = &g_lcg;
	}
	if (x0 == 0)
		lcg_random->x0 = __rand32(&g_frand_state.state32) % m_modulus;
	else
		lcg_random->x0 = x0;
	lcg_random->sub_next = 0;
	if (NULL != sub_step_arrays){
		lcg_random->sub_step_arrays = sub_step_arrays;
		lcg_random->sub_step_summary_arrays = (unsigned int *)malloc(sizeof(unsigned int) * sub_step_count);
		lcg_random->sub_m_modulus = sub_step_count;
		lcg_random->sub_m_mark = roundup_pow2(sub_step_count) - 1;
		for(unsigned int i = 0; i < sub_step_count; i++){
			sub_summary += sub_step_arrays[i];
			lcg_random->sub_step_summary_arrays[i] = sub_summary;
		}
		lcg_random->sub_summary = sub_summary;
		lcg_random->sub_count = 0;
		lcg_random->sub_a_multiplier = 5;
		lcg_random->sub_c_increment = 1;
		range_count = (unsigned long long)((max_value - offset + 1) / sub_summary * sub_step_count);
		lcg_random->sub_range_count = range_count;
		lcg_random->sub_stop = (lcg_random->sub_range_count / sub_step_count * sub_summary) + offset;
		for(unsigned int i = 0; i < sub_step_count; i++){
			if(lcg_random->sub_stop + lcg_random->sub_step_summary_arrays[i] - 1 > max_value)
				break;
			range_count ++;
		}
		lcg_random->lcg_count = range_count;
		unsigned long long sub_m_modulus = (unsigned long long)((max_value - offset + 1) / sub_summary);
		lcg_random->lcg_range = sub_m_modulus;
		sub_m_modulus = roundup_pow2(sub_m_modulus);
		if(sub_m_modulus != m_modulus)
			m_modulus = sub_m_modulus;
		lcg_random->m_modulus = m_modulus;
		lcg_random->m_mark = lcg_random->m_modulus - 1;
	}else{
		lcg_random->lcg_count = (unsigned long long)((max_value - offset + 1) / step);
		lcg_random->lcg_range = lcg_random->lcg_count;
		lcg_random->m_modulus = m_modulus;
		lcg_random->m_mark = lcg_random->m_modulus - 1;
		lcg_random->step = step;
		lcg_random->sub_m_modulus = 1;
		if (step & (step - 1))
			lcg_random->step_is_pow = 0;
		else{
			lcg_random->step_is_pow = (unsigned int)log2(step);
			if(pow(2, lcg_random->step_is_pow) != step){
				do
				{
					step = step >> 1;
					lcg_random->step_is_pow ++;
				} while (step == 1);
			}
		}
		lcg_random->next = lcg_random->x0;
		lcg_random->sub_step_arrays = &lcg_random->step;
	}
	lcg_random->c_increment = c_increment;
	lcg_random->a_multiplier = a_multiplier;
	lcg_random->count = 0;
	lcg_random->offset = offset;
	lcg_random->max_value = max_value;
	lcg_random->sub_step_summary = 0;
}

xt_lcg_random *get_lcg_random(void){
	return &g_lcg;
}

void free_sub_lcg(xt_lcg_random * lcg_random){
	if(lcg_random && lcg_random->sub_m_modulus > 1){
		free(lcg_random->sub_step_arrays);
		lcg_random->sub_step_arrays = NULL;
		free(lcg_random->sub_step_summary_arrays);
		lcg_random->sub_step_summary_arrays = NULL;
	}
}