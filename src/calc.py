def add_binary(a_bin: str, b_bin: str, bits: int) -> dict:
    """
    对两个指定位数的二进制补码字符串执行补码加法
    :param a_bin: 第一个二进制补码字符串
    :param b_bin: 第二个二进制补码字符串
    :param bits: 二进制总位数，例如 8
    :return: 字典，包含两个key
        'result': 相加之后定长二进制字符串
        'is_overflow': 布尔值，True代表发生补码溢出
    """
    # 输入校验：长度必须和bits一致
    if len(a_bin) != bits or len(b_bin) != bits:
        raise ValueError(f"输入字符串长度必须等于 {bits}")
    # 校验字符只能是0、1
    if any(c not in '01' for c in a_bin) or any(c not in '01' for c in b_bin):
        raise ValueError("输入只能由字符 '0' 和 '1' 组成")

    result_bits = ['0'] * bits
    carry = 0

    # 从最低位（末尾）循环加到最高位（下标0）
    for i in range(bits - 1, -1, -1):
        a_bit = int(a_bin[i])
        b_bit = int(b_bin[i])
        total = a_bit + b_bit + carry
        result_bit = total % 2
        carry_out = total // 2
        result_bits[i] = str(result_bit)
        carry = carry_out

    # 补码溢出判断：两个数符号相同，结果符号相反 → 溢出
    sign_a = int(a_bin[0])
    sign_b = int(b_bin[0])
    sign_res = int(result_bits[0])
    is_overflow = (sign_a == sign_b) and (sign_a != sign_res)

    result = ''.join(result_bits)
    return {
        "result": result,
        "is_overflow": is_overflow
    }


# 测试代码（只放在这里，函数内部没有打印）
if __name__ == '__main__':
    print(add_binary('00000101', '00000011', 8))
    print(add_binary('01111111', '00000001', 8))
