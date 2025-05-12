#ifndef XT_SHA1
#define XT_SHA1

#include <inttypes.h>

/*
 * Based on the Mozilla SHA1 (see mozilla-sha1/sha1.h),
 * optimized to do word accesses rather than byte accesses,
 * and to avoid unnecessary copies into the context array.
 */

struct xt_sha1_ctx {
	uint32_t *H;
	unsigned int W[16];
	unsigned long long size;
};

void xt_sha1_init(struct xt_sha1_ctx *);
void xt_sha1_update(struct xt_sha1_ctx *, const void *dataIn, unsigned long len);
void xt_sha1_final(struct xt_sha1_ctx *);

#endif
