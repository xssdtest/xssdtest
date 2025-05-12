#ifndef XT_SHA256_H
#define XT_SHA256_H

#include <inttypes.h>

#define SHA256_DIGEST_SIZE	32
#define SHA256_BLOCK_SIZE	64

struct xt_sha256_ctx {
	uint32_t count;
	uint32_t state[SHA256_DIGEST_SIZE / 4];
	uint8_t *buf;
};

void xt_sha256_init(struct xt_sha256_ctx *);
void xt_sha256_update(struct xt_sha256_ctx *, const uint8_t *, unsigned int);
void xt_sha256_final(struct xt_sha256_ctx *);

#endif
