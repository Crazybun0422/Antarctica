#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/3/3 17:11
# @Author：Malcolm
# @File : TimeAna.py
# @Software: PyCharm

import datetime
import re


def converse_seconds(time_stamp, con_para: str):
    return datetime.datetime.strptime(time_stamp, con_para).timestamp()


class TimeAna:
    dic_of_con = {
        # """'2023-03-02 15:30:00'"""
        r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}$': '%Y-%m-%d %H:%M:%S',
        # """'[10/Mar/2021:11:36:22 +0000]'"""
        r'^\[(\d{2})/([A-Za-z]{3})/(\d{4}):(\d{2}):(\d{2}):(\d{2})\s([\+\-]\d{4})\]$': '%d/%b/%Y:%H:%M:%S %z'
    }
    cur_seconds_recorded = []

    def __init__(self, org_string: str):
        if not org_string:
            return

        seconds_str_list = org_string.split(";")

        for seconds_str in seconds_str_list:
            if not seconds_str.__contains__("--"):
                raise Exception(
                    "Error:时间戳的范围设置应该是'2023-03-02 15:30:00--2023-03-02 15:30:00',当前没有找到符号'--'")
            time_arr = seconds_str.split("--")

            time_sec_pair = []
            for item in time_arr:
                if not re.match(r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}$', item):
                    raise Exception("格式不正确，请参考readme")
                else:
                    time_sec_pair.append(converse_seconds(item, '%Y-%m-%d %H:%M:%S'))

            self.cur_seconds_recorded.append(time_sec_pair)

    def confirm(self, time_stamp_position, node):
        """
        :param time_stamp_position: 时间戳所处的列号
        :param node: 日志节点
        :return:
        """
        time_exact = []
        for col in time_stamp_position:
            time_exact.append(node.get(col).strip(" "))
        """组合时间"""
        time_stamp = " ".join(time_exact)

        if not self.cur_seconds_recorded:
            return True

        log_time = -1
        """转换成秒数"""
        for k, v in self.dic_of_con.items():
            if re.match(k, time_stamp):
                log_time = converse_seconds(time_stamp, v)
                break

        for item in self.cur_seconds_recorded:
            if item[0] <= log_time <= item[1]:
                return True
        return False
