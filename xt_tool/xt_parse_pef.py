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
import os
import sys
import argparse
path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(path)))
from xt_liabary.parse_perf import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="xSSD Test pyecharts")
    parser.add_argument("-p", "--parse_files", type=str, dest="parse_files", nargs='+', required=True, default=None, help="parse file path, default is None")
    parser.add_argument("-ct", "--chart_title", type=str, dest="chart_title", default=None, help="chart title, default is None")
    parser.add_argument("-xu", "--xaxis_unit", type=int, dest="xaxis_unit", default=1000, help="xaxis unit is microseconds, default is 1000ms for fio")
    parser.add_argument("-b", "--base_date", type=str, dest="base_date", default=None, help="xaxis base date for record date info, default is None")
    parser.add_argument("-df", "--date_format", type=str, dest="date_format", default="%Y-%m-%d %H:%M:%S", help="xaxis base date format, default is %%Y-%%m-%%d %%H:%%M:%%S")
    parser.add_argument("-e", "--expect_value", type=int, dest="expect_value", default=None, help="expect value, default is None")
    parser.add_argument("-smv", "--set_min_value", type=int, dest="set_min_value", default=None, help="set min value, default is None")
    parser.add_argument("-min", "--min_line", type=int, dest="min_line", default=None, help="set min line, default is None")
    parser.add_argument("-max", "--max_line", type=int, dest="max_line", default=None, help="set max line, default is None")
    parser.add_argument("-aver", "--average_line", type=int, dest="average_line", default=None, help="set average line, default is None")
    parser.add_argument("-sa", "--show_all_lines", type=int, dest="show_all_lines", default=None, help="show all charts , default is None")
    parser.add_argument("-y", "--yaxis_name", type=str, dest="yaxis_name", default=None, help="yaxis nmae default is None")
    parser.add_argument("-d", "--delimiter", type=str, dest="delimiter", default=",", help="file delimiter, default is ','")
    parser.add_argument("-o", "--output_path", type=str, dest="output_path", default=None, help="out put path,  default is None")
    parser.add_argument("-l", "--local_js", type=int, dest="local_js", default=0, help="local java scripts, default is 0")
    args = parser.parse_args()
    if len(args.parse_files) == 1:
        export_fio_line_chart(args.parse_files[0], args.delimiter, args.base_date, args.date_format, args.xaxis_unit, args.chart_title, args.yaxis_name, args.show_all_lines, args.output_path, args.expect_value,
                           args.set_min_value, args.min_line, args.max_line, args.average_line, args.local_js)
    else:
        export_multfio_lines_chart(args.parse_files, args.delimiter, args.xaxis_unit, args.chart_title, args.yaxis_name, args.output_path, args.local_js)