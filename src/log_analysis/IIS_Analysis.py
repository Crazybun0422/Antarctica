#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/2/23 17:22
# @Author：Malcolm
# @File : IIS_Analysis.py
# @Software: PyCharm
import os

from log_analysis.Template_Analysis import AnalyzerInterface

KEY_DATA = r"#Software: Microsoft Internet Information Services"


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

    def get_field_produce_conditions(self, log_lines: list, fields):
        """
        :param log_lines: 存储日志的具体列表，每行日志，如果没有对它进行删减就直接返回即可
        :param fields: 用来标识每行日志title的英文名，在这个函数里
        :return:
        """
        """3.6以后的dict是有序的"""
        self.log_ch = "IIS"
        self.statistic_vector = "c-ip"
        self.default_titles = {'date': "日期",
                               'time': "时间",
                               's-ip': "服务器 IP 地址",
                               'cs-method': "请求方法",
                               'cs-uri-stem': "URI 资源 ",
                               'cs-uri-query': "URI 查询",
                               's-port': "服务器端口",
                               'c-ip': "客户端 IP 地址",
                               'cs(User-Agent)': "浏览器类型",
                               'sc-status': "状态码"}
        while log_lines[0].startswith("#") and not fields:
            """把具体的日志分区读出来"""
            fields.extend(self.__get_field(log_lines[0]))
            log_lines.pop(0)
            if fields:
                fields.remove("#Fields:")
                titles_dict = {fields[i]: "C" + str(i) for i in range(len(fields))}
                break

        return titles_dict

    def get_row_member(self, log_line: str):
        """
        对于每一行日志，拆解每一个对应列的member元素
        :param log_line:
        :return:
        """
        return log_line.split(" ")
