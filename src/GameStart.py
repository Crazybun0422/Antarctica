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
    opts, args = getopt.getopt(sys.argv[1:], '-f:-t:-v', ['--filepath=', 'target_use_case=', 'version'])
    for opt_name, opt_value in opts:
        if opt_name in ('-f', '--filepath'):
            filename = opt_value
        if opt_name in ('-t', '--target_use_case'):
            use_case = opt_value
        if opt_name in ('-v', '--version'):
            print("[*] Version is ", cons.CURRENT_VERSION)
    if not filename:
        print("ERROR:You have to provide full filepath by -f [filepath]")
    else:
        ant = Antarctica(filename, use_case)
        ant.run_all()
    exit(0)
