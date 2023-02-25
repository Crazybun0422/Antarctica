#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/2/23 17:22
# @Author：Malcolm
# @File : IIS_Analysis.py
# @Software: PyCharm
from log_analysis.Template_Analysis import AnalyzerInterface
import Constant as cons

KEY_DATA = "#Software: Microsoft Internet Information Services"


class IISAnalyzer(AnalyzerInterface):
    @staticmethod
    def decide_log_type(key_data):
        if key_data.__contains__(KEY_DATA):
            print("Current file is a Microsoft Internet Information Services logfile, "
                  "so we're gonna use corresponding method to process it.")
            return True
        return False

    @staticmethod
    def __get_field(data: str):
        if data.startswith("#Fields:"):
            return data.split(" ")
        return []

    def analyzing(self):
        with open(self.file_path, encoding="utf-8") as f:
            index = 0
            log_tree = []
            fields = None
            while True:
                data = f.read(cons.MAX_ANALYZE_DATA_LENGTH)
                if not data:
                    break
                """读到这一行结束"""
                while data[-1] != '\n':
                    data_ = f.read(1)
                    if data_:
                        data += data_
                    else:
                        break

                log_lines = data.split("\n")
                while log_lines[0].startswith("#") and not fields:
                    """把具体的日志分区读出来"""
                    fields = self.__get_field(log_lines[0])
                    log_lines = log_lines[1:]
                    if fields:
                        fields.remove("#Fields:")
                        break

                log_tree.extend([{fields[i]: node_list[i] for i in range(len(node_list))}
                                 for node_list in [line.split(" ") for line in log_lines]])
            print(log_tree)
        return

    def statistic(self):
        print("xx")
        return
