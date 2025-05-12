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
pathList = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)
parPath = os.path.sep.join([item for item in pathList[:-2]])
sys.path.append(parPath)
sys.path.append(os.path.sep.join((parPath, 'xt_platform')))
from xt_platform import *

if __name__ == '__main__':
    logger = xt_interface.Logger()
    logger.info("test platform logger info: get name: %s"%(logger.get_name()))
    logger.debug("test platform logger debug: get name: %s"%(logger.get_name()))
    logger.warning("test platform logger warning: get name: %s"%(logger.get_name()))
    logger.error("test platform logger error: get name: %s"%(logger.get_name()))
    logger.critical("test platform logger critical: get name: %s"%(logger.get_name()))
    logger.fatal("test platform logger fatal: get name: %s"%(logger.get_name()))

    level_dic = {'CRITICAL': 50, 'FATAL': 50, 'ERROR': 40, 'WARNING': 30, 'WARN': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}
    for item in level_dic.keys():
        print("Set Logger Level: %s : %s"%(item, level_dic[item]))
        logger.info("test platform logger info: get name: %s"%(logger.get_name()))
        logger.debug("test platform logger debug: get name: %s"%(logger.get_name()))
        logger.warning("test platform logger warning: get name: %s"%(logger.get_name()))
        logger.error("test platform logger error: get name: %s"%(logger.get_name()))
        logger.critical("test platform logger critical: get name: %s"%(logger.get_name()))
        logger.fatal("test platform logger fatal: get name: %s"%(logger.get_name()))