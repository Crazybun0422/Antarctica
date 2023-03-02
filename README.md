# Antarctica
日志分析工具集合
- ## 代码说明：
````
E:.
│  changelog.txt
│  README.md
│
│
└─src
    │
    ├
    │  AnalyzerRegister.py          用于注册分析日志的特定类
    │  Antarctica.py                分析日志的流程
    │  Constant.py                  用来保存常用变量
    │  GameStart.py                 启动函数
    │  result.csv                   结果
    │  start.bat                    
    │
    ├─alg
    │      MatchAna.py              字符串匹配
    │      Output.py                输出
    │      __init__.py
    │
    │
    ├─attack_fingerprint            攻击指纹，用正则来识别一些常用的攻击手段
    │
    │
    │
    │
    └─log_analysis
            IIS_Analysis.py         IIS日志分析
            SqlServer_Analysis.py   sqlsever日志分析
            Template_Analysis.py    日志分析模板类
            __init__.py
      
````
## 如何添加不同的web日志分析代码：
```python
# 继承AnalyzerInterface类
from log_analysis.Template_Analysis import AnalyzerInterface
```

```python

KEY_DATA = "#Software: Microsoft Internet Information Services"
class IISAnalyzer(AnalyzerInterface):
    # 实现下面的函数，用于判断对应日志是否匹配本日志分析代码，并输出对应的提示星系
    @staticmethod
    def decide_log_type(key_data):
        
        if key_data.__contains__(KEY_DATA):
            print("Current file is a Microsoft Internet Information Services logfile, "
                  "so we're gonna use corresponding method to process it.")
            return True
        return False
    # 实现下面的函数，并在fields列表里填入对应的日志列名，定义一个日志列名和对应的翻译字典，以及一个类似下面的列名和列号的字典并返回
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
        """
        :param log_lines: 存储日志的具体列表，每行日志，如果没有对它进行删减就直接返回即可
        :param fields: 用来标识每行日志title的英文名，在这个函数里
        :return:
        """
        """3.6以后的dict是有序的"""
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
            log_lines = log_lines[1:]
            if fields:
                fields.remove("#Fields:")
                titles_dict = {fields[i]: "C" + str(i) for i in range(len(fields))}
                break

        return titles_dict, log_lines
```
## 启动命令行
-f filepath（日志文件目录）  

-t 匹配内容逻辑表达式

-s 匹配统计逻辑表达式
```
python.exe GameStart.py -f "E:\FUCK_LOG\iis2023-02-17_w14.log" -t "(C10==200)&&(C3==GET)&&(C4 %%%% "^/Reg/Content/scripts/app/SwfuploadContractFJ3\.js$")"
```
### 一.日志内容筛选逻辑表达式示例：
#### 1.筛选第10列为200（从0列开始）单条不用加括号
```
C10==200
```
==表示等于 

!=表示不等于

!表示非

&&表示与  

||表示或  

@@表示模糊匹配正则  


(C10==200)&&(C3==GET)&&(C4 @@ ^/Reg/Content/scripts/app/SwfuploadContractFJ3\.js$)

#### 2.代表第10列等于200第三列等于GET第四列匹配，多条需要加括号：
```
"^/Reg/Content/scripts/app/SwfuploadContractFJ3\.js$"
```
### 二.日志条目统计表达式示例:
注意，统计表达式不支持==符号，因为另外一个操作数是数字，在做==时，需要再引入别的符号解析
#### 引入操作符号:
例如
x:y 表示x列的某个元素的个数，比如iis的状态列C4(假设位于C4)可能有500，200，302，404
那么表示200的次数大于20次的表达式如下：
````
(C4:200) > 2
````
#### 1.筛选(假设C3列是访问IP) 次数大于等于10次的日志
```
C3 >= 10 
```
#### 2.筛选(假设C3列是访问IP，C4列是访问状态)访问次数大于等于10，状态成功的次数>2的日志
```
(C3>=10)&&((C4:200)>2)
```
