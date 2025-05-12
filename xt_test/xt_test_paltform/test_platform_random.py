#! /usr/bin/python3
###############################################################################
 #    BSD LICENSE
 #
 #    Copyright (c) Saul Han <2573789168@qq.com>
 #
 #    Redistribution and use in source and binary forms, with or without
 #    modification, are permitted provided that the following conditions
 #    are met:
 #
 #       Redistributions of source code must retain the above copyright
 #        notice, this list of conditions and the following disclaimer.
 #       Redistributions in binary form must reproduce the above copyright
 #        notice, this list of conditions and the following disclaimer in
 #        the documentation and/or other materials provided with the
 #        distribution.
 #
 #    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 #    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 #    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 #    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 #    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 #    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 #    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 #    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 #    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 #    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 #    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################
import sys
import os
import time
import random
pathList = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)
parPath = os.path.sep.join([item for item in pathList[:-2]])
sys.path.append(parPath)
sys.path.append(os.path.sep.join((parPath, 'xt_platform')))
from xt_platform import *

def test_platform_random(xt_fn, rand_fn, *args):
    stime = time.time()
    _count = 536870912
    for _ in range(_count):
        xt_fn(*args)
    endtime = time.time()
    print("%s run %s take time %s"%(xt_fn, _count, endtime-stime))
    stime = time.time()
    for _ in range(_count):
        rand_fn(*args)
    endtime = time.time()
    print("%s run %s take time %s"%(rand_fn, _count, endtime-stime))

if __name__ == '__main__':
    # test xt_randint and randint
    # <cyfunction xt_randint at 0x704ebfb3f920> run 10000000 take time 0.2632930278778076
    # <bound method Random.randint of <random.Random object at 0x24eac60>> run 10000000 take time 2.431035280227661
    test_platform_random(xt_interface.xt_randint, random.randint, 0, 0xFFFFFFFFFF)
    #
    # # test xt_uniform and uniform
    # # <cyfunction xt_uniform at 0x7a049c039970> run 10000000 take time 0.26447319984436035
    # # <bound method Random.uniform of <random.Random object at 0xc6fc60>> run 10000000 take time 0.5839276313781738
    # test_platform_random(xt_interface.xt_uniform, random.uniform, 0, 1)
    #
    # # test xt_triangular and triangular
    # # <cyfunction xt_triangular at 0x74c824bce190> run 10000000 take time 0.6692891120910645
    # # <bound method Random.triangular of <random.Random object at 0x1fd4c60>> run 10000000 take time 1.0041887760162354
    # test_platform_random(xt_interface.xt_triangular, random.triangular, 0, 1)
    #
    # # test xt_choice and choice
    # # <cyfunction xt_choice at 0x743631eca400> run 10000000 take time 0.3002660274505615
    # # <bound method Random.choice of <random.Random object at 0x128b5b0>> run 10000000 take time 1.3623380661010742
    # test_platform_random(xt_interface.xt_choice, random.choice, range(10))
    #
    # # test xt_sample and sample
    # # <cyfunction xt_sample at 0x7146d10ca4d0> run 10000000 take time 4.40740704536438
    # # <bound method Random.sample of <random.Random object at 0x27155e0>> run 10000000 take time 7.778377532958984
    # test_platform_random(xt_interface.xt_sample, random.sample, range(10), 2)
    #
    # # test xt_shuffle and shuffle
    # # <cyfunction xt_shuffle at 0x760b405ce4d0> run 10000000 take time 2.6090478897094727
    # # <bound method Random.shuffle of <random.Random object at 0x20292b0>> run 10000000 take time 11.626448631286621
    # test_platform_random(xt_interface.xt_shuffle, random.shuffle, list(range(10)))
    #
    # # test xt_choices and choices
    # # <cyfunction xt_choices at 0x73d8b8eca5a0> run 10000000 take time 3.3273251056671143
    # # <bound method Random.choices of <random.Random object at 0x126b2b0>> run 10000000 take time 6.337431907653809
    # test_platform_random(xt_interface.xt_choices, random.choices, list(range(10)), [1] * 10)
    #
    # # test xt_normalvariate and normalvariate
    # # <cyfunction xt_normalvariate at 0x7423b8eca5a0> run 10000000 take time 1.110126256942749
    # # <bound method Random.normalvariate of <random.Random object at 0xb60c60>> run 10000000 take time 2.028637409210205
    # test_platform_random(xt_interface.xt_normalvariate, random.normalvariate)
    #
    # # test xt_lognormvariate and lognormvariate
    # # <cyfunction xt_lognormvariate at 0x7b47666ca670> run 10000000 take time 1.3546288013458252
    # # <bound method Random.lognormvariate of <random.Random object at 0x1224c90>> run 10000000 take time 2.6505391597747803
    # test_platform_random(xt_interface.xt_lognormvariate, random.lognormvariate, 0, 1)
    #
    # # test xt_expovariate and expovariate
    # # <cyfunction xt_expovariate at 0x78f4205ce740> run 10000000 take time 0.6402568817138672
    # # <bound method Random.expovariate of <random.Random object at 0x1db3c60>> run 10000000 take time 0.8714292049407959
    # test_platform_random(xt_interface.xt_expovariate, random.expovariate, 1)
    #
    # # test xt_gammavariate and gammavariate
    # # <cyfunction xt_gammavariate at 0x78cddabce8e0> run 10000000 take time 0.705251932144165
    # # <bound method Random.gammavariate of <random.Random object at 0x219fc90>> run 10000000 take time 1.683795690536499
    # test_platform_random(xt_interface.xt_gammavariate, random.gammavariate, 1, 1)
    #
    # # test xt_betavariate and betavariate
    # # <cyfunction xt_betavariate at 0x744fd6fd69b0> run 10000000 take time 2.893285036087036
    # # <bound method Random.betavariate of <random.Random object at 0x1800c90>> run 10000000 take time 5.113191843032837
    # test_platform_random(xt_interface.xt_betavariate, random.betavariate, 0.5, 0.5)
    #
    # # test xt_paretovariate and paretovariate
    # # <cyfunction xt_paretovariate at 0x70f91c6caa80> run 10000000 take time 0.41266441345214844
    # # <bound method Random.paretovariate of <random.Random object at 0x1a3bc60>> run 10000000 take time 0.7296497821807861
    # test_platform_random(xt_interface.xt_paretovariate, random.paretovariate, 0.5)
    #
    # # test xt_weibullvariate and weibullvariate
    # # <cyfunction xt_weibullvariate at 0x7f586b7d2b50> run 10000000 take time 0.790226936340332
    # # <bound method Random.weibullvariate of <random.Random object at 0x2485c90>> run 10000000 take time 1.1348469257354736
    # test_platform_random(xt_interface.xt_weibullvariate, random.weibullvariate, 0.5, 0.5)
    #
    # # test xt_gauss and gauss
    # # <cyfunction xt_gauss at 0x7a4cd2ecee90> run 10000000 take time 0.642559289932251
    # # <bound method Random.gauss of <random.Random object at 0xec7680>> run 10000000 take time 1.9460618495941162
    # xt_interface.xt_gauss_init(10000, 1)
    # stime = time.time()
    # _count = 10000000
    # for _ in range(_count):
    #     xt_interface.xt_gauss(10000, 1)
    # endtime = time.time()
    # print("%s run %s take time %s"%(xt_interface.xt_gauss, _count, endtime-stime))
    # stime = time.time()
    # for _ in range(_count):
    #     random.gauss(0, 1)
    # endtime = time.time()
    # print("%s run %s take time %s"%(random.gauss, _count, endtime-stime))

    # lcg random run 244190646 take time 10.814697265625
    # slba, elba, lba_cnt = 0, 0x74706db0 - 1, 8
    # xt_interface.xt_lcg_init(slba, elba, lba_cnt)
    # next = xt_interface.xt_lcg_first(slba, elba, lba_cnt)
    # loop_cnt = (elba - slba + 1) // lba_cnt
    # stime = time.time()
    # for _ in range(loop_cnt - 1):
    #     next = xt_interface.xt_lcg_next()
    # else:
    #     if loop_cnt * lba_cnt == (elba - slba + 1):
    #         next = slba + loop_cnt * lba_cnt
    #         lba_cnt = (elba - next + 1)
    # stime = time.time() - stime
    # print("lcg random run %s take time %s"%(loop_cnt, stime))



