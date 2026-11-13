def get_codes(num, bits):
    """
    计算指定位数下一个整数的原码、反码、补码，以字典返回
    :param num: 十进制整数
    :param bits: 二进制位数（正整数，常用8）
    :return: 字典，键固定为 'yuan','fan','bu'；值为字符串
             特殊：bits=8且num=-128时，yuan='无'，fan='无'，bu='10000000'
    """
    # 处理特殊情况：8位的-128，只有补码，没有原码反码
    if bits == 8 and num == -128:
        return {
            "yuan": "无",
            "fan": "无",
            "bu": "10000000"
        }

    # 正数：原码、反码、补码完全相同，高位补0凑够bits位
    if num >= 0:
        # bin()返回'0bxxxx'，切片去掉0b，zfill向左补0到指定位数
        binary = bin(num)[2:].zfill(bits)
        yuan = binary
        fan = binary
        bu = binary
    # 负数处理
    else:
        abs_num = -num
        # 先写出绝对值的二进制，补0凑bits位（这就是负数原码的数值位，最高位符号位是1）
        abs_bin = bin(abs_num)[2:].zfill(bits)
        # 原码：最高位符号1，后面接上绝对值的二进制
        yuan = "1" + abs_bin[1:]

        # 反码：符号位不变，数值位全部取反
        fan_list = []
        for idx, c in enumerate(yuan):
            if idx == 0:
                # 符号位保持不变
                fan_list.append(c)
            else:
                # 数值位 0变1，1变0
                fan_list.append("1" if c == "0" else "0")
        fan = "".join(fan_list)

        # 补码 = 反码 + 1
        # 把反码字符串转为整数，加1，再转二进制，去掉0b，保证长度为bits位
        fan_int = int(fan, 2)
        bu_int = fan_int + 1
        bu = bin(bu_int)[2:].zfill(bits)

    # 返回固定三键的字典
    return {
        "yuan": yuan,
        "fan": fan,
        "bu": bu
    }
