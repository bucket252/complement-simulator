def get_codes(num, bits):
    """
    计算给定数字的原码、反码、补码，同时返回按位拆分的字符列表，方便前端逐位高亮
    :param num: 十进制整数
    :param bits: 二进制位数，只支持 8 / 16
    :return: 字典，包含6个key
        yuan: 原码字符串 | 超出范围/特殊最小值时为"无"
        fan: 反码字符串 | 超出范围/特殊最小值时为"无"
        bu: 补码字符串
        yuan_list: 原码每一位组成的字符列表
        fan_list: 反码每一位组成的字符列表
        bu_list: 补码每一位组成的字符列表
    特殊规则：
        8位：-128，无原反码，补码 10000000
        16位：-32768，无原反码，补码 1000000000000000
    """
    # 定义对应位数的有符号最小值
    min_val = {8: -128, 16: -32768}[bits]
    max_val = {8: 127, 16: 32767}[bits]

    # 边界判断：数字超出当前bits能表示的范围
    if not (min_val <= num <= max_val):
        yuan_str = "无"
        fan_str = "无"
        bu_str = "无"
        yuan_list = ["无"]
        fan_list = ["无"]
        bu_list = ["无"]
        return {
            "yuan": yuan_str,
            "fan": fan_str,
            "bu": bu_str,
            "yuan_list": yuan_list,
            "fan_list": fan_list,
            "bu_list": bu_list
        }

    # 判断是不是该位数的特殊最小值（-128 / -32768）
    if num == min_val:
        yuan_str = "无"
        fan_str = "无"
        bu_str = "1" + "0" * (bits - 1)
        yuan_list = ["无"]
        fan_list = ["无"]
        bu_list = list(bu_str)
        return {
            "yuan": yuan_str,
            "fan": fan_str,
            "bu": bu_str,
            "yuan_list": yuan_list,
            "fan_list": fan_list,
            "bu_list": bu_list
        }

    # 正数处理：原码、反码、补码相同
    if num >= 0:
        code_str = format(num, f'0{bits}b')
        yuan_str = code_str
        fan_str = code_str
        bu_str = code_str
    else:
        # 负数（不是特殊最小值）
        abs_num = -num
        yuan_str = format(abs_num, f'0{bits}b')
        # 原码符号位是1
        yuan_str = '1' + yuan_str[1:]
        # 反码：符号位不变，其余取反
        fan_list_temp = []
        for idx, c in enumerate(yuan_str):
            if idx == 0:
                fan_list_temp.append('1')
            else:
                fan_list_temp.append('1' if c == '0' else '0')
        fan_str = ''.join(fan_list_temp)
        # 补码 = 反码 + 1
        fan_int = int(fan_str, 2)
        bu_int = fan_int + 1
        bu_str = format(bu_int, f'0{bits}b')

    yuan_list = list(yuan_str)
    fan_list = list(fan_str)
    bu_list = list(bu_str)

    return {
        "yuan": yuan_str,
        "fan": fan_str,
        "bu": bu_str,
        "yuan_list": yuan_list,
        "fan_list": fan_list,
        "bu_list": bu_list
    }
