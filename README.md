# Antarctica
## 代码说明：

## 日志筛选逻辑表达式示例：
第10列为200（从0列开始）
```
C10==200
```
&&表示与
||表示或
%%表示模糊匹配正则
````
(C10==200)&&(C3==GET)&&(C4 %% ^/Reg/Content/scripts/app/SwfuploadContractFJ3\.js$)
````
代表第10列等于200第三列等于GET第四列匹配：
```
^/Reg/Content/scripts/app/SwfuploadContractFJ3\.js$
```
