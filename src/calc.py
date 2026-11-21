def add_binary(a_bin: str, b_bin: str, bits: int) -> dict:
    """
    对两个指定位数的二进制补码字符串执行补码加法
    :param a_bin: 第一个二进制补码字符串
    :param b_bin: 第二个二进制补码字符串
    :param bits: 二进制总位数，例如 8
    :return: 字典，包含 result, is_overflow, steps, overflow_reason
        'result': 相加之后定长二进制字符串
        'is_overflow': 布尔值，True代表发生补码溢出
        'steps': 列表，从bit_idx=0最低位开始，依次到最高位，每一项是字典
                 字段：bit_idx, a_bit, b_bit, carry_in, sum, carry_out
        'overflow_reason': 字符串，溢出原因，无溢出为空串
    """
    # 输入校验：长度必须和bits一致
    if len(a_bin) != bits or len(b_bin) != bits:
        raise ValueError(f"输入字符串长度必须等于 {bits}")
    # 校验字符只能是0、1
    if any(c not in '01' for c in a_bin) or any(c not in '01' for c in b_bin):
        raise ValueError("输入只能由字符 '0' 和 '1' 组成")

    result_bits = ['0'] * bits
    carry_in = 0
    steps = []

    # i 是字符串下标（从末尾最低位向前遍历）
    # bit_idx 是文档要求的序号：0=最低位
    for bit_idx in range(bits):
        str_pos = bits - 1 - bit_idx
        a_bit = int(a_bin[str_pos])
        b_bit = int(b_bin[str_pos])

        total = a_bit + b_bit + carry_in
        sum_bit = total % 2
        carry_out = total // 2

        steps.append({
            "bit_idx": bit_idx,
            "a_bit": a_bit,
            "b_bit": b_bit,
            "carry_in": carry_in,
            "sum": sum_bit,
            "carry_out": carry_out
        })

        result_bits[str_pos] = str(sum_bit)
        carry_in = carry_out

    # 补码溢出判断：两个数符号相同，结果符号相反 → 溢出
    sign_a = int(a_bin[0])
    sign_b = int(b_bin[0])
    sign_res = int(result_bits[0])
    is_overflow = (sign_a == sign_b) and (sign_a != sign_res)

    overflow_reason = ""
    if is_overflow:
        if sign_a == 0:
            overflow_reason = "两个正数相加，结果变成负数，发生溢出"
        else:
            overflow_reason = "两个负数相加，结果变成正数，发生溢出"

    result = ''.join(result_bits)
    return {
        "result": result,
        "is_overflow": is_overflow,
        "steps": steps,
        "overflow_reason": overflow_reason
    }


# 测试代码（只放在这里，函数内部没有打印）
if __name__ == '__main__':
    print(add_binary('00000101', '00000011', 8))
    print(add_binary('01111111', '00000001', 8))
    print(add_binary('0000000000000101', '0000000000000011', 16))
