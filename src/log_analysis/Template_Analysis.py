#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/2/23 17:23
# @Author：Malcolm
# @File : Template_Analysis.py
# @Software: PyCharm
import abc


class AnalyzerInterface(metaclass=abc.ABCMeta):
    data = {}

    def __init__(self,
                 file_path,
                 use_case):
        self.file_path = file_path
        self.use_case = use_case

    @staticmethod
    @abc.abstractmethod
    def decide_log_type(key_data):
        pass

    @abc.abstractmethod
    def analyzing(self):
        pass

    @abc.abstractmethod
    def statistic(self):
        pass
