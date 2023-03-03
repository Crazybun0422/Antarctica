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

        # 实现下面的函数:
        # 1.fields列表里填入对应的日志列名
        # 2.定义一个日志列名和对应的翻译字典如下面title_dict
        # 3.一个类似下面的列名和列号的字典并返回
        # 4.给self.log_ch 赋值一般是当前的日志类型如果是IIS就是IIS
        # 5.定义统计维度，例如 IIS的统计维度就是客户端IP 那么就是self.statistic_vector = "c-ip"

    """
    title_dict = {
        'date': "C0",
        'time': "C1",
        's-ip': "C2",
        'cs-method': "C3",
        'cs-uri-stem': "C4 ",
        'cs-uri-query': "C5",
        's-port': "C6",
        'c-ip': "C7",
        'cs(User-Agent)': "C8",
        'sc-status': "C9"
    }
    """

    def get_field_produce_conditions(self, log_lines, fields):
        self.time_stamp_position = ["C0", "C1"]
        self.default_titles = {
            'date': "日期",
            'time': "时间",
            'action': "动作",
            'message': '消息'
        }
        fields.extend(["date", "time", "action", "message"])
        title_dict = {'date': "C0",
                      'time': "C1",
                      'action': "C2",
                      'message': 'C3'}
        self.log_ch = "sqlserver"
        self.statistic_vector = "action"
        return title_dict

    def get_row_member(self, log_line: str):
        """
        对于每一行日志，拆解每一个对应列的member元素
        :param log_line:
        :return:
        """
        # sqlserver日志的消息分割符号有下面3种
        split_chr_list = [' '*10, ' '*6, ' '*5]
        result = []
        message_arr = []
        if log_line:
            for item in split_chr_list:
                message_arr = log_line.split(item)
                if len(message_arr) >= 2:
                    break
            if len(message_arr) >= 2:
                c_list = message_arr[0].split(" ")
                # 去掉.后面的时间
                c_list[1] = c_list[1][0:-3]
                result.extend(c_list)
                result.append(message_arr[1])
            return result
        return []
