#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/2/23 17:11
# @Author：Malcolm
# @File : Antarctica.py
# @Software: PyCharm

import AnalyzerRegister as ar
import Constant as cons


class Antarctica:
    def __init__(self, path, use_case=None):
        self.file_path = path
        self.use_case = use_case

    def run_all(self):
        try:
            with open(self.file_path) as f:
                data = f.read(cons.MAX_VERIFY_FILE_DATA_LENGTH)
        except Exception as e:
            print(e)
            return

        for analyzer in ar.CurrentRegister:
            if analyzer.decide_log_type(data):
                ana = analyzer(self.file_path,
                               self.use_case)
                break
        if ana:
            ana.analyzing()
        else:
            print("ERROR: No log analyzer support current file...")
