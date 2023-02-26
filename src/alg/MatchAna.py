import re

# 定义操作符映射表
op_map = {
    "%%": lambda x, y: re.match(y, x) is not None,
    "==": lambda x, y: x == y,
    "||": lambda x, y: x or y,
    "&&": lambda x, y: x and y,
    "!": lambda x: not x,
    ")": None,
    "(": None,
}
# 二元操作符号
opr_2_list = ["&&", "||", "%%", "=="]


def db_p(ch, mch_, opr, temp, tokens, input_str, index):
    if ch == mch_:
        tokens.append(temp)
        if input_str[index + 1] == ch:
            tokens.append(opr)
        else:
            raise Exception(opr + " 应该成对出现")


def tokenize(input_str):
    tokens = []
    temp = ""
    index = 0
    while index < len(input_str):
        ch = input_str[index]
        if ch == '(':
            tokens.append(temp)
            temp = ""
            tokens.append(ch)
        elif ch == ')':
            tokens.append(temp)
            temp = ""
            tokens.append(ch)

        elif ch == ' ':
            tokens.append(temp)
            temp = ""
        elif ch == '&':
            db_p(ch, '&', '&&', temp, tokens, input_str, index)
            temp = ""
            index += 1
        elif ch == '|':
            db_p(ch, '|', '||', temp, tokens, input_str, index)
            temp = ""
            index += 1
        elif ch == '=':
            db_p(ch, '=', '==', temp, tokens, input_str, index)
            temp = ""
            index += 1
        elif ch == '!':
            tokens.append(temp)
            temp = ""
            tokens.append(ch)
        elif ch != '\'' and ch != '\"':
            temp += ch
        index += 1
    if temp:
        tokens.append(temp)
    while "" in tokens:
        tokens.remove('')

    return tokens


# print(tokenize('(C0==200)&&(C3==GET)&&(C4 like ^/Reg/Content/scripts/app/SwfuploadContractFJ3\.js$)'))


def opr_calc_value(op_stack, value_stack, pop_left=True):
    while op_stack and op_stack[-1] != "(":
        op = op_stack.pop()
        if op in opr_2_list:
            right = value_stack.pop()["value"]
            left = value_stack.pop()["value"]
            value_stack.append({"take": False, "value": op_map[op](left, right)})
    if pop_left:
        op_stack.pop()  # 弹出左括号
    if op_stack and op_stack[-1] == "not":
        value_stack.append({"take": False, "value": not value_stack.pop()})
        op_stack.pop()  # 弹出 not


def evaluate_expression(conditions, value_dict):
    # 初始化运算符栈和操作数栈
    op_stack, value_stack = [], []

    # 逐个处理条件和运算符
    for token in conditions:
        if token in op_map:
            if token == "(":
                op_stack.append(token)
            elif token == ")":
                opr_calc_value(op_stack, value_stack)
            else:
                op_stack.append(token)
        else:
            # 获取操作数对应的值
            take = True
            value = value_dict.get(token, None)
            if value is None:
                if value_stack[-1]["take"]:
                    take = False
                    value = token
                else:
                    raise ValueError(f"Value not found for variable '{token}'")
            value_stack.append({"take": take, "value": value})

    # 计算剩余的操作符
    while op_stack:
        opr_calc_value(op_stack, value_stack, False)

    # 返回最终结果
    return value_stack[0]["value"]


# expression_dict = '(C0==200)&&(C3==GET)&&(C4 %% ^/Reg/Content/scripts/app/SwfuploadContractFJ3\\.js$)'
# # expression_dict = '((type == "human") or not (type == "animal"))'
# value_dict = {'C0': '2023-02-17', 'C1': '08:47:34', 'C2': '10.115.98.108',
#               'C3': 'GET', 'C4': '/YSZJJG/Archive',
#               'C5': 'caseID=2302150001_ywfj&sAction=edit&showMode=file&imagebar=true',
#               'C6': '881', 'C7': '-', 'C8': '218.87.91.42',
#               'C9': 'Mozilla/5.0+(Windows+NT+10.0;+WOW64;+Trident/7.0;+rv:11.0)+like+Gecko',
#               'C10': '200', 'C11': '0', 'C12': '0', 'C13': '28'}
#
# result = evaluate_expression(tokenize(expression_dict), value_dict)
# print(result)  # True
