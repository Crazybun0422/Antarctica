#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/2/26 14:47
# @Author：Malcolm
# @File : Output.py
# @Software: PyCharm
import csv
import uuid

import datetime


class CSVWriter:
    def __init__(self, key_list, file_path="result.csv"):
        self.file_path = file_path

        self.file = open(file_path, 'w', newline='', encoding='utf-8')
        # 定义 CSV 写入器
        self.writer = csv.DictWriter(self.file, fieldnames=key_list)

        # 写入表头
        self.writer.writeheader()

    def write(self, row_):
        self.writer.writerow(row_)

    def close(self):
        self.close()
