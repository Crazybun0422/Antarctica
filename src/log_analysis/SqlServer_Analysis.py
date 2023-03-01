#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/2/23 17:23
# @Author：Malcolm
# @File : SqlServer_Analysis.py
# @Software: PyCharm
from log_analysis.Template_Analysis import AnalyzerInterface

KEY_DATA = "Server      Microsoft SQL Server"


class SqlServerAnalyzer(AnalyzerInterface):

    @staticmethod
    def decide_log_type(key_data):
        if key_data.__contains__(KEY_DATA):
            print("Current file is a Microsoft SQL Server logfile, "
                  "so we're gonna use corresponding method to process it.")
            return True
        return False

    def analyzing(self):
        print("xx")
        return

    def get_field_produce_conditions(self, log_lines, fields):
        return
