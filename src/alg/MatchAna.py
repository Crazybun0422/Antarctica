import re


def opr_int_check(x, y, func):
    int_x = 0
    int_y = 0
    if type(x) == str and x.isalnum():
        int_x = int(x)
    elif type(x) == int:
        int_x = x
    if type(y) == str and y.isalnum():
        int_y = int(y)
    elif type(y) == int:
        int_y = y

    if type(x) == dict:
        for _, v in x.items():
            if func(v, int_y):
                return True
        return False
    if type(y) == dict:
        for _, v in y.items():
            if func(int_x, v):
                return True
        return False

    return func(int_x, int_y)


# 定义操作符映射表

def opr_dict_check(x, y):
    if type(x) == str:
        return re.match(y, x) is not None
    elif type(x) == dict:
        for k, v in x.items():
            if re.match(y, k) is not None:
                return v
        """没找到"""
        return -1


op_map = {
    "@@": lambda x, y: opr_dict_check(x, y),
    "==": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    "||": lambda x, y: x or y,
    "&&": lambda x, y: x and y,
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y,
    "<": lambda x, y: x < y,
    "<=": lambda x, y: x <= y,
    "!": lambda x: not x,
    ":": lambda x, y: x.get(y),
    ")": None,
    "(": None,
}
# 二元操作符号
opr_2_list = ["&&", "||", "@@", "==", "!=", ]
# 二元操作符号，但是接个数组做查询
opr_arr_list = ["<", ">", "<=", ">="]


def db_p(ch, mch_, opr, temp, tokens, input_str, index):
    tokens.append(temp)
    if input_str[index + 1] == mch_:
        tokens.append(opr)
        index += 1
    else:
        if ch == mch_:
            raise Exception(opr + " 应该成对出现")
        else:
            tokens.append(ch)
    return index, ''


def tokenize(input_str):
    tokens = []
    temp = ""
    index = 0
    bucket = False
    if not input_str:
        return None
    while index < len(input_str):
        ch = input_str[index]
        "引号括起来的都当整体"
        if bucket and ch != '\'' and ch != '\"':
            temp += ch
        elif ch == '(':
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
            index, temp = db_p(ch, '&', '&&', temp, tokens, input_str, index)
        elif ch == '|':
            index, temp = db_p(ch, '|', '||', temp, tokens, input_str, index)
        elif ch == '=':
            index, temp = db_p(ch, '=', '==', temp, tokens, input_str, index)
        elif ch == '@':
            index, temp = db_p(ch, '@', '@@', temp, tokens, input_str, index)
        elif ch == '!':
            index, temp = db_p(ch, '=', '!=', temp, tokens, input_str, index)
        elif ch == '>':
            index, temp = db_p(ch, '=', '>=', temp, tokens, input_str, index)
        elif ch == '<':
            index, temp = db_p(ch, '=', '<=', temp, tokens, input_str, index)
        elif ch == ':':
            tokens.append(temp)
            temp = ""
            tokens.append(ch)
        elif ch == '\'' or ch == '\"':
            bucket = not bool(bucket)
        else:
            temp += ch
        index += 1
    if temp:
        tokens.append(temp)
    while "" in tokens:
        tokens.remove('')
    return tokens


# def test_tokenize():
#     # 测试用例
#     test_cases = [
#         {
#             "input": "(a>b)&&(c<d)",
#             "output": ["(", "a", ">", "b", ")", "&&", "(", "c", "<", "d", ")"],
#         },
#         {
#             "input": "name=='john' && age>20",
#             "output": ["name", "==", "'john'", "&&", "age", ">", "20"],
#         },
#         {
#             "input": "is_vip==True",
#             "output": ["is_vip", "==", "True"],
#         },
#         {
#             "input": "name!='jane' || age<=30",
#             "output": ["name", "!=", "'jane'", "||", "age", "<=", "30"],
#         },
#         {
#             "input": "regex@@'\\d{4}-\\d{2}-\\d{2}'",
#             "output": ["regex", "@@", "'\\d{4}-\\d{2}-\\d{2}'"],
#         },
#         {
#             "input": "(a+b)*(c-d)/e",
#             "output": ["(", "a", "+", "b", ")", "*", "(", "c", "-", "d", ")", "/", "e"],
#         },
#         {
#             "input": "a == b",
#             "output": ["a", "==", "b"],
#         },
#         {
#             "input": "!a",
#             "output": ["!", "a"],
#         },
#         {
#             "input": "a<b && b<c || d==e",
#             "output": ["a", "<", "b", "&&", "b", "<", "c", "||", "d", "==", "e"],
#         },
#         {
#             "input": "a>=b",
#             "output": ["a", ">=", "b"],
#         },
#     ]
#
#     # 对每个测试用例进行测试
#     for i, test_case in enumerate(test_cases):
#         print(f"Running test case {i + 1}: {test_case['input']}")
#         tokens = tokenize(test_case["input"])
#         assert tokens == test_case["output"]
#         print("Pass")

# print(tokenize('(C0!=200)&&(C3!=GET)&&!(C4 @@ "\\([^\\]+\\)*([^\\]+)\.php")'))


def opr_calc_value(op_stack, value_stack, pop_left=True, b_get_content=False):
    """
    :param op_stack: 符号操作栈
    :param value_stack: 值栈
    :param pop_left: 是否弹出左括号
    :param b_get_content: 是否将对应列的内容取出来作比较，默认是不操作的
    :return:
    """
    while op_stack and op_stack[-1] != "(":

        op = op_stack.pop()
        if op in opr_2_list:
            right = value_stack.pop()["value"]
            left = value_stack.pop()["value"]
            value_stack.append({"take": True, "value": op_map[op](left, right)})
        if op in opr_arr_list:
            right = value_stack.pop()["value"]
            left = value_stack.pop()["value"]
            value_stack.append({"take": True, "value": opr_int_check(left,
                                                                     right,
                                                                     op_map[op])})
        if op == ":":
            right = value_stack.pop()["value"]
            left = value_stack.pop()["value"]
            """每一个统计字典的第一层值都是一个字典"""
            v = op_map[op](left, right)
            if not v:
                print("当前查询的元素节点{0}:{1}不存在.".format(left, right))
                return False
            value_stack.append({"take": True, "value": v})
    if pop_left:
        op_stack.pop()  # 弹出左括号
    if op_stack and op_stack[-1] == "!":
        value_stack.append({"take": True, "value": not value_stack.pop()["value"]})
        op_stack.pop()  # 弹出 not
    return True


def evaluate_expression(conditions, value_dict, accessories=None):
    """
    :param conditions: 查询条件
    :param value_dict: 用于查询的节点
    :param accessories: 附属查询节点
    :return:
    """
    # 初始化运算符栈和操作数栈
    op_stack, value_stack = [], []

    if not value_dict:
        return False

    if not conditions:
        return True

    # 逐个处理条件和运算符
    for token in conditions:
        if token in op_map:
            if token == "(":
                op_stack.append(token)
            elif token == ")":
                if not opr_calc_value(op_stack, value_stack, True):
                    return False
            else:
                op_stack.append(token)

        else:
            # 获取操作数对应的值
            take = True
            value = value_dict.get(token, None)
            if not value:
                if value_stack and value_stack[-1]["take"]:
                    take = False
                    value = token
                else:
                    print(f"日志中的'{token}'列没有找到，对于单列出现偶尔是正常的...")
                    return False
            """对于统计来说在如下每个日志节点中需要查询到有对应的节点，不然此次查询是没有意义的"""
            if type(value) == dict and accessories:
                q_value = accessories.get(token)
                b_value = value.get(q_value)
                if not b_value:
                    print(f"当前日志节点中没有{q_value}")
                    return False
                else:
                    value = b_value

            value_stack.append({"take": take, "value": value})
    # 计算剩余的操作符
    while op_stack:
        opr_calc_value(op_stack, value_stack, False, value_dict)

    # 返回最终结果
    return value_stack[0]["value"]


# expression_dict = '(C0==200)&&(C3==GET)&&(C4 %% ^/Reg/Content/scripts/app/SwfuploadContractFJ3\\.js$)'
# value_dict = {'C0': '2023-02-17', 'C1': '08:47:34', 'C2': '10.115.98.108',
#               'C3': 'GET', 'C4': '/YSZJJG/Archive',
#               'C5': 'caseID=2302150001_ywfj&sAction=edit&showMode=file&imagebar=true',
#               'C6': '881', 'C7': '-', 'C8': '218.87.91.42',
#               'C9': 'Mozilla/5.0+(Windows+NT+10.0;+WOW64;+Trident/7.0;+rv:11.0)+like+Gecko',
#               'C10': '200', 'C11': '0', 'C12': '0', 'C13': '28'}
#
# result = evaluate_expression(tokenize(expression_dict), value_dict)
# print(result)  # True

# expression_dict = '(C0==200)&&(C3==GET)&&(C4 %% ^/Reg/Content/scripts/app/SwfuploadContractFJ3\\.js$)'
# value_dict = {'C0': '2023-02-17', 'C1': '08:47:34', 'C2': '10.115.98.108',
#               'C3': 'GET', 'C4': '/YSZJJG/Archive',
#               'C5': 'caseID=2302150001_ywfj&sAction=edit&showMode=file&imagebar=true',
#               'C6': '881', 'C7': '-', 'C8': '218.87.91.42',
#               'C9': 'Mozilla/5.0+(Windows+NT+10.0;+WOW64;+Trident/7.0;+rv:11.0)+like+Gecko',
#               'C10': '200', 'C11': '0', 'C12': '0', 'C13': '28'}
#
# result = evaluate_expression(tokenize(expression_dict), value_dict)
# print(result)  # True


# exp = "((C0:404)>499)" \
#       "&&(C1>=100)" \
#       "&&(C1<=100)" \
#       "&&(C2>=10)" \
#       "&&(C2<=10)" \
#       "&&((C4 @@ {0}) <100)".format(r'^\/\w+\/\d+\/\w+\.js$')
# value_dict = {"C0": {"200": 10,
#                      "404": 500, },
#               "C1": {
#                   "xx": 10,
#                   "yy": 400,
#               },
#               "C2": {
#                   "lol": 10,
#                   "lmao": 200
#               },
#               "C4": {
#                   "/PATH/32321/index.js": 99
#               }
#               }
#
# tokens = tokenize(exp)
# print(evaluate_expression(tokens, value_dict))
