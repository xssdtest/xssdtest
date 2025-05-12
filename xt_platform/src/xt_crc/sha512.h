#ifndef XT_SHA512_H
#define XT_SHA512_H

#include <inttypes.h>

struct xt_sha512_ctx {
	uint64_t state[8];
	uint32_t count[4];
	uint8_t *buf;
	uint64_t W[80];
};

void xt_sha512_init(struct xt_sha512_ctx *);
void xt_sha512_update(struct xt_sha512_ctx *, const uint8_t *, unsigned int);

#endif
