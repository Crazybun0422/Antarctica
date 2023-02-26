# Antarctica
日志分析工具集合
## 代码说明：
````
E:.
│  changelog.txt
│  README.md
│
│
└─src
    │  AnalyzerRegister.py          用于注册分析日志的特定类
    │  Antarctica.py                分析日志的流程
    │  Constant.py                  用来保存常用变量
    │  GameStart.py                 启动函数
    │  result.csv                   结果
    │  start_windows.bat            windows启动的脚本这个结合下面的讲解，linux就是在%%时使用不用
    │
    ├─alg
    │      MatchAna.py              字符串匹配
    │      Output.py                输出
    │      __init__.py
    │
    └─log_analysis
            IIS_Analysis.py         IIS日志分析
            SqlServer_Analysis.py   sqlsever日志分析
            Template_Analysis.py    日志分析模板类
            __init__.py
````
## 启动命令行
-f filepath（日志文件目录）  

-t 匹配正则
```
python.exe GameStart.py -f "E:\FUCK_LOG\iis2023-02-17_w14.log" -t "(C10==200)&&(C3==GET)&&(C4 %%%% ^/Reg/Content/scripts/app/SwfuploadContractFJ3\.js$)"
```
### 日志筛选逻辑表达式示例：
#### 1.第10列为200（从0列开始）
```
C10==200
```
==表示等于 

!=表示不等于

!表示非

&&表示与  

||表示或  

%%表示模糊匹配正则  

*特别注意windows需要使用%%来代表一个%所以在windows命令行配置时需要写%%%%*
````
(C10==200)&&(C3==GET)&&(C4 %% ^/Reg/Content/scripts/app/SwfuploadContractFJ3\.js$)
````
#### 2.代表第10列等于200第三列等于GET第四列匹配：
```
^/Reg/Content/scripts/app/SwfuploadContractFJ3\.js$
```
