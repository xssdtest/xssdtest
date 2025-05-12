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
#ifndef XT_RAND_H
#define XT_RAND_H

#include <inttypes.h>
#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include "config-host.h"
#include "xt_compiler/xt_compiler.h"
#include "xt_include/hash.h"

#define FRAND32_MAX	(-1U)
#define FRAND64_MAX	(-1ULL)
#define GAUSS_ITERS	12

/*
*	m a power of 2, c ≠ 0
*	When c ≠ 0, correctly chosen parameters allow a period equal to m, for all seed values. This will occur if and only if:
*		condition:
*		1. m and c are coprime,
*		2. a-1 is divisible by all prime factors of 
*		3. a-1 is divisible by 4 if m is divisible by 4.
*	These three requirements are referred to as the Hull–Dobell Theorem.
*/ 
typedef struct _xt_lcg_random{
	unsigned long long a_multiplier;	/* a-1 is divisible by 4 if m is divisible by 4. */
	unsigned long long c_increment; 	/* Xn+1 = (a * Xn + c) mod m */
	unsigned long long m_modulus; 		/* m a power of 2 */
	unsigned long long m_mark;          /* m_mark = m_modulus - 1*/
	unsigned long long count;
	unsigned long long next;
	unsigned long long offset;
	unsigned long long max_value;
	unsigned int x0;
	unsigned int step;
	unsigned int step_is_pow;
	unsigned int sub_next;   				// sub lcg next value
	unsigned int *sub_step_arrays;  		// step list 
	unsigned int *sub_step_summary_arrays;	// step index summary list 
	unsigned int sub_m_modulus; 			// sub lcg m_modulus(total sub step count), sub_step_arrays and sub_step_summary_arrays array count;
	unsigned int sub_m_mark;				// a power of 2 - 1
	unsigned int sub_summary;				// step list summary
	unsigned int sub_count;					// record sub lcg next value count
	unsigned int sub_a_multiplier;			// sub lcg a_multiplier
	unsigned int sub_c_increment;			// sub lcg c_increment
	unsigned int sub_step_summary;
	unsigned long long sub_range_count;		// twice lcg range count for Non-aligned step lcg  
	unsigned long long sub_stop;			// twice lcg range end value + 1 for Non-aligned step lcg  
	unsigned long long lcg_count;			// total range count
	unsigned long long lcg_range;			// record lcg range for Non-aligned step lcg  
}xt_lcg_random;


struct taus88_state {
	unsigned int s1, s2, s3;
};

struct taus258_state {
	uint64_t s1, s2, s3, s4, s5;
};

struct frand_state {
	unsigned int use64;
	union {
		struct taus88_state state32;
		struct taus258_state state64;
	};
};

struct gauss_state {
	// struct frand_state *r;
	uint64_t nranges;
	unsigned int stddev;
	bool disable_hash;
};

static inline uint64_t rand_max(struct frand_state *state)
{
	if (state->use64)
		return FRAND64_MAX;
	else
		return FRAND32_MAX;
}

static inline void __frand32_copy(struct taus88_state *dst,
				  struct taus88_state *src)
{
	dst->s1 = src->s1;
	dst->s2 = src->s2;
	dst->s3 = src->s3;
}

static inline void __frand64_copy(struct taus258_state *dst,
				  struct taus258_state *src)
{
	dst->s1 = src->s1;
	dst->s2 = src->s2;
	dst->s3 = src->s3;
	dst->s4 = src->s4;
	dst->s5 = src->s5;
}

static inline void frand_copy(struct frand_state *dst, struct frand_state *src)
{
	if (src->use64)
		__frand64_copy(&dst->state64, &src->state64);
	else
		__frand32_copy(&dst->state32, &src->state32);

	dst->use64 = src->use64;
}

static inline unsigned int __rand32(struct taus88_state *state)
{
#define TAUSWORTHE(s,a,b,c,d) ((s&c)<<d) ^ (((s <<a) ^ s)>>b)

	state->s1 = TAUSWORTHE(state->s1, 13, 19, 4294967294UL, 12);
	state->s2 = TAUSWORTHE(state->s2, 2, 25, 4294967288UL, 4);
	state->s3 = TAUSWORTHE(state->s3, 3, 11, 4294967280UL, 17);

	return (state->s1 ^ state->s2 ^ state->s3);
}

static inline uint64_t __rand64(struct taus258_state *state)
{
	uint64_t xval;

	xval = ((state->s1 <<  1) ^ state->s1) >> 53;
	state->s1 = ((state->s1 & 18446744073709551614ULL) << 10) ^ xval;

	xval = ((state->s2 << 24) ^ state->s2) >> 50;
	state->s2 = ((state->s2 & 18446744073709551104ULL) <<  5) ^ xval;

	xval = ((state->s3 <<  3) ^ state->s3) >> 23;
	state->s3 = ((state->s3 & 18446744073709547520ULL) << 29) ^ xval;

	xval = ((state->s4 <<  5) ^ state->s4) >> 24;
	state->s4 = ((state->s4 & 18446744073709420544ULL) << 23) ^ xval;

	xval = ((state->s5 <<  3) ^ state->s5) >> 33;
	state->s5 = ((state->s5 & 18446744073701163008ULL) <<  8) ^ xval;

	return (state->s1 ^ state->s2 ^ state->s3 ^ state->s4 ^ state->s5);
}

static inline uint64_t __rand(struct frand_state *state)
{
	if (state->use64)
		return __rand64(&state->state64);
	else
		return __rand32(&state->state32);
}

static inline double __rand_0_1(struct frand_state *state)
{
	if (state->use64) {
		uint64_t val = __rand64(&state->state64);

		return (val + 1.0) / (FRAND64_MAX + 1.0);
	} else {
		uint32_t val = __rand32(&state->state32);

		return (val + 1.0) / (FRAND32_MAX + 1.0);
	}
}

static inline uint32_t rand32_upto(struct frand_state *state, uint32_t end)
{
	uint32_t r;

	assert(!state->use64);

	r = __rand32(&state->state32);
	end++;
	return (int) ((double)end * (r / (FRAND32_MAX + 1.0)));
}

static inline uint64_t rand64_upto(struct frand_state *state, uint64_t end)
{
	uint64_t r;

	assert(state->use64);

	r = __rand64(&state->state64);
	end++;
	return (uint64_t) ((double)end * (r / (FRAND64_MAX + 1.0)));
}

/*
 * Generate a random value between 'start' and 'end', both inclusive
 */
static inline uint64_t rand_between(struct frand_state *state, uint64_t start,
				    uint64_t end)
{
	if (state->use64)
		return start + rand64_upto(state, end - start);
	else
		return start + rand32_upto(state, end - start);
}

extern struct frand_state g_frand_state;
extern struct gauss_state g_gauss_state;
extern xt_lcg_random g_lcg;

static inline unsigned long long rand64(void){
	return __rand64(&g_frand_state.state64); 
}

static inline unsigned int rand32(void){
	return __rand32(&g_frand_state.state32);
}

extern double xt_random(void);

extern void init_rand(struct frand_state *, bool);

extern void init_rand_seed(struct frand_state *, unsigned int seed, unsigned int);

extern void reset_rand_seed(unsigned int seed, unsigned int use64);

extern void gauss_init(struct gauss_state *gs, unsigned long nranges, double dev);

extern unsigned long long gauss_next(void);

extern void gauss_disable_hash(void);

extern void init_lcg_random(xt_lcg_random * lcg_random, unsigned int x0, unsigned long long m_modulus, unsigned long long c_increment, 
						   unsigned long long a_multiplier, unsigned long long offset, unsigned long long max_value, unsigned int step,
						   unsigned int *sub_step_arrays, unsigned int sub_step_count);

extern xt_lcg_random *get_lcg_random(void);

extern void free_sub_lcg(xt_lcg_random * lcg_random);

static inline unsigned long long lcg_next(xt_lcg_random * lcg_random){
	if (NULL == lcg_random){
		lcg_random = &g_lcg;
	}
	lcg_random->count ++;
	lcg_random->next = (lcg_random->a_multiplier * lcg_random->next + lcg_random->c_increment )& lcg_random->m_mark;
	return lcg_random->next + lcg_random->offset;
}

static inline unsigned long long roundup_pow2(unsigned long long value){
	if (value & (value - 1)){
		value |= value >> 1;
		value |= value >> 2;
		value |= value >> 4;
		value |= value >> 8;
		value |= value >> 16;
		value |= value >> 32;
		return value + 1;
	}else{
		return value == 0 ? 1 : value;
	}
}

static inline unsigned long long lcg_next_start(xt_lcg_random * lcg_random){
	unsigned long long next;
	if (NULL == lcg_random){
		lcg_random = &g_lcg;
	}
	if (lcg_random->sub_m_modulus == 1){
		do{
			lcg_random->next = (lcg_random->a_multiplier * lcg_random->next + lcg_random->c_increment) & lcg_random->m_mark;
			if (lcg_random->step_is_pow)
				next = (lcg_random->next << lcg_random->step) + lcg_random->offset;
			else
				next = (lcg_random->next * lcg_random->step) + lcg_random->offset;
		} while (next > lcg_random->max_value);
		lcg_random->count ++;
	}else{
		if (lcg_random->count < lcg_random->sub_range_count){
			if(lcg_random->sub_count == 0){
				if(lcg_random->sub_a_multiplier + 4 > lcg_random->sub_m_modulus){
					lcg_random->sub_a_multiplier = 5;
					lcg_random->sub_c_increment = 1;
				}else{
					lcg_random->sub_a_multiplier += 4;
					lcg_random->sub_c_increment += 2;				
				}
				lcg_random->sub_next = lcg_random->sub_c_increment % lcg_random->sub_m_modulus;
				do{
					lcg_random->next = (lcg_random->a_multiplier * lcg_random->next + lcg_random->c_increment) & lcg_random->m_mark;
				} while (lcg_random->next > lcg_random->lcg_range);
			}else{
				do{
					lcg_random->sub_next = ((lcg_random->sub_c_increment * lcg_random->sub_next) + lcg_random->sub_c_increment) & lcg_random->sub_m_mark;
				}while (lcg_random->sub_next >= lcg_random->sub_m_modulus);
				lcg_random->sub_step_summary += lcg_random->sub_step_arrays[lcg_random->sub_next];
			}

			next = (lcg_random->next * lcg_random->sub_summary) + lcg_random->sub_step_summary + lcg_random->offset;
		}else{
			lcg_random->sub_step_summary += lcg_random->sub_step_arrays[lcg_random->sub_count];
			next = lcg_random->sub_stop + lcg_random->sub_step_summary;
			lcg_random->sub_next = lcg_random->count - lcg_random->sub_range_count;
		}
		lcg_random->count ++;
		lcg_random->sub_count ++;
		if(lcg_random->sub_count == lcg_random->sub_m_modulus){
			lcg_random->sub_count = 0;
			lcg_random->sub_step_summary = 0;
		}
		if(lcg_random->count == lcg_random->lcg_count){
			lcg_random->count = 0;
		}
	}
	return next;
}

#endif
