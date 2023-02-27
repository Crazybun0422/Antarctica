#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/2/23 17:22
# @Author：Malcolm
# @File : IIS_Analysis.py
# @Software: PyCharm
import os

from log_analysis.Template_Analysis import AnalyzerInterface
from alg.Output import CSVWriter
import Constant as cons

KEY_DATA = "#Software: Microsoft Internet Information Services"

from tabulate import tabulate
from alg import MatchAna

"""3.6以后的dict是有序的"""
default_titles = {'date': "日期",
                  'time': "时间",
                  's-ip': "服务器 IP 地址",
                  'cs-method': "请求方法",
                  'cs-uri-stem': "URI 资源 ",
                  'cs-uri-query': "URI 查询",
                  's-port': "服务器端口",
                  'c-ip': "客户端 IP 地址",
                  'cs(User-Agent)': "浏览器类型",
                  'sc-status': "状态码"}


def g_dict(node: list):
    table = {}
    for i, item in enumerate(node):
        table.update({"C" + str(i): item})
    return table


"""额外的节点处理函数"""


def extra_pro_node(node: dict):
    n_node = {}
    index = 0
    values = list(node.values())
    for k, v in default_titles.items():
        n_node[(k + "({0})").format(v)] = values[index]
        index += 1
    return n_node


def template_table(table: dict):
    t = tabulate(table, headers="keys", tablefmt="pipe", colalign="left")
    print("当前日志样式：")
    print(t)


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
            fields = None
            keys = []
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
                        keys = ["C" + str(i) for i in range(len(fields))]

                        template_table(g_dict(log_lines[0].split(" ")))
                        if not self.use_case:
                            self.use_case = input("请输入筛选日志的字符串：\r\n例如(C0==2023-02-17)and("
                                                  "C1==08:46:38)代表第一列==2023-02-17，第二列==08:46:38来进行筛选同时你可以用正则匹配，\r\n"
                                                  "如C3 %% ^10\\.115\\.98\\.\\d{1,"
                                                  "3}$来表示匹配10.115.98.网段的IP，具体根据上面提供的日志列号来匹配。\r\n")
                        print("输出的表达式为:", self.use_case)
                        print("分析开始...")
                        list_kv = []
                        for k, v in default_titles.items():
                            list_kv.append((k + "({0})").format(v))
                        csv = CSVWriter(list_kv)
                        conditions = MatchAna.tokenize(self.use_case)
                        print(conditions)
                        break

                for node_list in [line.split(" ") for line in log_lines]:
                    if node_list:
                        """只输出关心得列,在default_tiles里配置"""
                        node = {keys[i]: node_list[i] for i in range(len(node_list)) if default_titles.get(fields[i])}
                        try:
                            if MatchAna.evaluate_expression(conditions, node):
                                csv.write(extra_pro_node(node))
                                print(node)
                        except Exception as e:
                            print("日志不完整:", node, e)
        return

    def statistic(self):
        print("xx")
        return
