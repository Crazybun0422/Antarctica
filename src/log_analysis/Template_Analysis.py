#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/2/23 17:23
# @Author：Malcolm
# @File : Template_Analysis.py
# @Software: PyCharm
import abc

from prettytable import PrettyTable
import Constant as cons
from alg import MatchAna, StatisticAna
from alg.Output import CSVWriter


def g_dict(node: list):
    table = {}
    for i, item in enumerate(node):
        table.update({"C" + str(i): item})
    return table


def template_table(table: dict):
    t = PrettyTable()
    t.field_names = table.keys()
    t.add_row(table.values())
    print("当前日志样式：")
    print(t)


class AnalyzerInterface:
    data = {}

    def __init__(self,
                 file_path,
                 use_case,
                 sta_case):
        self.file_path = file_path
        self.use_case = use_case
        self.sta_case = sta_case
        self.default_titles = {}

    @staticmethod
    @abc.abstractmethod
    def decide_log_type(key_data):
        pass

    @abc.abstractmethod
    def get_field_produce_conditions(self, log_lines, fields):
        raise AttributeError("Error")

    def produce_conditions(self, log_lines):
        template_table(g_dict(log_lines[0].split(" ")))
        print("用于解析的表达式为:", self.use_case)
        print("用于统计的表达式为:", self.sta_case)
        print("分析开始...")
        list_kv = []
        for k, v in self.default_titles.items():
            list_kv.append((k + "({0})").format(v))
        csv = CSVWriter(list_kv, "IIS_")
        conditions = MatchAna.tokenize(self.use_case)
        conditions_sta = MatchAna.tokenize(self.sta_case)
        return conditions, conditions_sta, csv

    """额外的节点处理函数"""

    def extra_pro_node(self, node: dict):
        n_node = {}
        index = 0
        values = list(node.values())
        for k, v in self.default_titles.items():
            n_node[(k + "({0})").format(v)] = values[index]
            index += 1
        return n_node

    def analyzing(self):
        with open(self.file_path, encoding="utf-8") as f:
            fields = []
            title_dict = {}
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

                if not fields:
                    title_dict, log_lines = self.get_field_produce_conditions(log_lines, fields)
                    conditions, conditions_sta, csv = self.produce_conditions(log_lines)

                sta_result = self.__analyzing(log_lines,
                                              title_dict,
                                              conditions,
                                              conditions_sta,
                                              fields,
                                              csv)

        return

    def __analyzing(self, log_lines=None,
                    title_dict=None,
                    conditions_t=None,
                    conditions_s=None,
                    fields=None,
                    csv=None,
                    cares_col="c-ip"):
        """
        :param log_lines:
        :param title_dict:
        :param conditions_t:
        :param conditions_s:
        :param fields:
        :param csv:
        :return:
        """
        sta_result = {}
        node_result = []
        for node_list in [line.split(" ") for line in log_lines]:
            if node_list:
                """只输出关心得列,在default_tiles里配置"""
                node = {list(title_dict.values())[i]: node_list[i] for i in range(len(node_list)) if
                        self.default_titles.get(fields[i])}
                try:
                    # 每一个都要进行统计，这个统计信息是全局得
                    StatisticAna.Statistic(sta_result, node, title_dict[cares_col])
                    # 如果内容正则匹配
                    if MatchAna.evaluate_expression(conditions_t, node):
                        node_result.append(node)
                except Exception as e:
                    print("日志不完整:", node, e)
        for item in node_result:
            if MatchAna.evaluate_expression(conditions_s,
                                            item[title_dict[cares_col]],
                                            item):
                csv.write(self.extra_pro_node(item))

        return sta_result
