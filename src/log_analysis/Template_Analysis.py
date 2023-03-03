#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/2/23 17:23
# @Author：Malcolm
# @File : Template_Analysis.py
# @Software: PyCharm
import abc
import chardet
from prettytable import PrettyTable
import Constant as cons
from alg import MatchAna, StatisticAna
from alg.Output import CSVWriter
from alg.Output import JsonWriter


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
                 sta_case,
                 encoding):
        self.file_path = file_path
        self.use_case = use_case
        self.sta_case = sta_case
        self.encoding = encoding
        self.default_titles = {}
        # 统计向量，以哪一个英文列来做统计的主键，一般是IP
        self.statistic_vector = ""
        # 当前日志的标志字符串，例如IIS可以写IIS
        self.log_ch = ""
        # 定义时间戳所属的列
        self.time_stamp_position = []

    @staticmethod
    @abc.abstractmethod
    def decide_log_type(key_data):
        pass

    @abc.abstractmethod
    def get_field_produce_conditions(self, log_lines, fields):
        pass

    @abc.abstractmethod
    def get_row_member(self, log_line):
        pass

    def produce_conditions(self, log_lines):
        template_table(g_dict(self.get_row_member(log_lines[0])))
        print("用于解析的表达式为:", self.use_case)
        print("用于统计的表达式为:", self.sta_case)
        print("分析开始...")
        list_kv = []
        for k, v in self.default_titles.items():
            list_kv.append((k + "({0})").format(v))
        if not self.log_ch:
            raise Exception("必须设置每个日志解析类的self.log_ch")

        csv = CSVWriter(list_kv, self.log_ch + "_")
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
        with open(self.file_path, encoding=self.encoding) as f:
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
                    title_dict = self.get_field_produce_conditions(log_lines, fields)
                    conditions, conditions_sta, csv = self.produce_conditions(log_lines)

                sta_result = self.__analyzing(log_lines,
                                              title_dict,
                                              conditions,
                                              conditions_sta,
                                              fields,
                                              csv)
                jw = JsonWriter(self.log_ch + "_json")
                jw.write(sta_result)

        print("日志分析完成.")
        return

    def __analyzing(self, log_lines=None,
                    title_dict=None,
                    conditions_t=None,
                    conditions_s=None,
                    fields=None,
                    csv=None):
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
        for line in log_lines:
            node_list = self.get_row_member(line)
            if node_list:
                """只输出关心得列,在default_tiles里配置"""
                node = {list(title_dict.values())[i]: node_list[i] for i in range(len(node_list)) if
                        self.default_titles.get(fields[i])}
                try:
                    # 每一个都要进行统计，这个统计信息是全局得
                    StatisticAna.Statistic(sta_result, node, title_dict[self.statistic_vector])
                    # 如果内容正则匹配
                    if MatchAna.evaluate_expression(conditions_t, node):
                        node_result.append(node)
                except Exception as e:
                    print("日志不完整:", node, e)
        for item in node_result:
            if MatchAna.evaluate_expression(conditions_s,
                                            sta_result[item[title_dict[self.statistic_vector]]],
                                            item):
                csv.write(self.extra_pro_node(item))

        return sta_result
