#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023/2/23 18:36
# @Author：Malcolm
# @File : AnalyzerRegister.py
# @Software: PyCharm
from log_analysis.IIS_Analysis import IISAnalyzer
from log_analysis.SqlServer_Analysis import SqlServerAnalyzer
"""
日志解析器在此处注册即可
"""
CurrentRegister = [
    IISAnalyzer,
    SqlServerAnalyzer,
]
