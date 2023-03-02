#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/2/27 16:05
# @Author：Malcolm
# @File : StatisticAna.py
# @Software: PyCharm
"""统计各项日志的出现次数并生成json"""


def Statistic(current_node, node: dict, vec: str):
    """
    :param current_node: 用于保存统计信息的节点
    :param node: 单一日志节点
    :param vec: key，一般是访问IP，这个是用来保存的维度
    :return:
    """
    ip = node.get(vec, None)
    if not ip:
        print(f"日志不完整:{node}")
        return
    if ip not in current_node:
        current_node[ip] = {}
    for key, value in node.items():
        if key not in current_node[ip]:
            current_node[ip][key] = {}
        if value not in current_node[ip][key]:
            current_node[ip][key][value] = 0
        current_node[ip][key][value] += 1
