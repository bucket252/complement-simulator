# 第四周：经全组集成测试，确认无 Bug（证明你参与了封版）
def add_binary(a_bin: str, b_bin: str, bits: int) -> dict:
    """
    定长补码加法，返回包含每一步运算细节的字典，供动画演示
    :param a_bin: 二进制字符串
    :param b_bin: 二进制字符串
    :param bits: 总位数，例如8
    :return: dict {result, is_overflow, steps, overflow_reason}
    """
    # 输入校验
    if len(a_bin) != bits or len(b_bin) != bits:
        raise ValueError(f"输入字符串长度必须等于 {bits}")
    if any(c not in "01" for c in a_bin) or any(c not in "01" for c in b_bin):
        raise ValueError("输入只能包含字符0和1")

    # 字符串转数字列表，字符串第0位是最高符号位
    a_bits = [int(c) for c in a_bin]
    b_bits = [int(c) for c in b_bin]

    carry_in = 0
    steps = []
    res_bits = [0] * bits

    # bit_idx：0=最低位，bits-1=最高符号位
    for bit_idx in range(bits):
        pos = bits - 1 - bit_idx
        a_bit = a_bits[pos]
        b_bit = b_bits[pos]

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

        res_bits[pos] = sum_bit
        carry_in = carry_out

    result = "".join(str(x) for x in res_bits)

    # 同号溢出判断（答辩要用的逻辑）
    sign_a = a_bits[0]
    sign_b = b_bits[0]
    sign_res = res_bits[0]
    is_overflow = False
    overflow_reason = ""

    if sign_a == sign_b:
        if sign_a == 0 and sign_res == 1:
            is_overflow = True
            overflow_reason = "两个正数相加得到负数，发生溢出"
        elif sign_a == 1 and sign_res == 0:
            is_overflow = True
            overflow_reason = "两个负数相加得到正数，发生溢出"

    return {
        "result": result,
        "is_overflow": is_overflow,
        "steps": steps,
        "overflow_reason": overflow_reason
    }
