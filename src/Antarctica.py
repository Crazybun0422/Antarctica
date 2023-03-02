#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/2/23 17:11
# @Author：Malcolm
# @File : Antarctica.py
# @Software: PyCharm
import chardet

import AnalyzerRegister as ar
import Constant as cons


class Antarctica:
    def __init__(self, path, use_case=None, s_case=None):
        self.file_path = path
        self.use_case = use_case
        self.s_case = s_case

    def run_all(self):
        try:
            with open(self.file_path, 'rb') as f:
                content = f.read(cons.MAX_VERIFY_FILE_DATA_LENGTH)
                encoding = chardet.detect(content)['encoding']
            with open(self.file_path, 'r', encoding=encoding) as f:
                data = f.read(cons.MAX_VERIFY_FILE_DATA_LENGTH)
        except Exception as e:
            print(e)
            return

        for analyzer in ar.CurrentRegister:
            if analyzer.decide_log_type(data):
                ana = analyzer(self.file_path,
                               self.use_case,
                               self.s_case,
                               encoding)
                break
        if ana:
            ana.analyzing()
        else:
            print("ERROR: No log analyzer support current file...")
