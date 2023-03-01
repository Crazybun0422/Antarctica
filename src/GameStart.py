#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/2/23 17:45
# @Author：Malcolm
# @File : GameStart.py
# @Software: PyCharm


import os
import getopt
import sys
import Constant as cons
from Antarctica import Antarctica

if __name__ == "__main__":
    use_case = None
    filename = None
    statistic_info = None
    opts, args = getopt.getopt(sys.argv[1:], '-f:-t:-s:-v', ['--filepath=',
                                                             'target_use_case=',
                                                             'statistic_info=',
                                                             'version'])
    for opt_name, opt_value in opts:
        if opt_name in ('-f', '--filepath'):
            filename = opt_value
        if opt_name in ('-t', '--target_use_case'):
            use_case = opt_value
        if opt_name in ('-s', '--statistic_info'):
            statistic_info = opt_value
        if opt_name in ('-v', '--version'):
            print("[*] Version is ", cons.CURRENT_VERSION)
    if not filename:
        print("ERROR:你必须通过 -f [filepath]来提供路径")
    else:
        ant = Antarctica(filename,
                         use_case,
                         statistic_info)
        ant.run_all()
    exit(0)
