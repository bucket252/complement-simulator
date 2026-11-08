def add_binary(a_bin: str, b_bin: str) -> str:
    """
    对两个 8 位二进制补码字符串进行按位相加，并打印每一位的进位情况。

    参数:
        a_bin: 8 位二进制补码字符串，例如 '00000101'
        b_bin: 8 位二进制补码字符串，例如 '00000011'

    返回:
        相加后的 8 位二进制结果字符串（截断最高位的溢出）

    说明:
        - 采用从最低位(索引7)到最高位(索引0)的顺序依次相加，模拟硬件全加器。
        - 补码溢出判断规则：两个输入符号相同，但结果符号不同 → 溢出
        - 最高位向外的进位直接丢弃（8 位定长）
    """
    # ---------- 1. 输入校验 ----------
    if len(a_bin) != 8 or len(b_bin) != 8:
        raise ValueError("输入必须是 8 位二进制字符串")
    if any(c not in '01' for c in a_bin) or any(c not in '01' for c in b_bin):
        raise ValueError("输入只能是 '0' 或 '1' 组成的字符串")

    # ---------- 2. 逐位相加 ----------
    result_bits = ['0'] * 8   # 用于存放最终结果位，索引 0 为最高位
    carry = 0                 # 初始进位为 0

    print(f"被加数 A = {a_bin}")
    print(f"加  数 B = {b_bin}")
    print("-" * 60)
    print(f"{'位序':<6}{'a位':<6}{'b位':<6}{'进位输入':<10}"
          f"{'和':<6}{'进位输出':<10}{'结果位':<6}")
    print("-" * 60)

    # 从最低位（索引 7）向最高位（索引 0）遍历
    for i in range(7, -1, -1):
        a_bit = int(a_bin[i])
        b_bit = int(b_bin[i])

        # 全加器逻辑：三个输入相加
        total = a_bit + b_bit + carry
        result_bit = total % 2     # 本位和
        carry_out = total // 2     # 向高位的进位

        result_bits[i] = str(result_bit)

        # 打印当前位的详细信息
        bit_pos = 7 - i
        print(f"{bit_pos:<6}{a_bit:<6}{b_bit:<6}{carry:<10}"
              f"{result_bit:<6}{carry_out:<10}{result_bit:<6}")

        # 更新进位，供下一位使用
        carry = carry_out

    # ---------- 3. 补码溢出判断（新增逻辑） ----------
    sign_a = int(a_bin[0])
    sign_b = int(b_bin[0])
    sign_res = int(result_bits[0])
    # 同号相加、结果符号相反 → 溢出
    overflow = (sign_a == sign_b) and (sign_a != sign_res)

    print("-" * 60)
    if carry:
        print(f"最高位产生的最终进位 = {carry}（丢弃）")
    else:
        print("最高位无最终进位")

    if overflow:
        print("发生溢出")
    else:
        print("无溢出")

    result = ''.join(result_bits)

    # ---------- 4. 打印最终结果 ----------
    print(f"相加结果 = {result}")
    # 顺便解释一下结果的补码含义
    print(f"（按补码解释：A={int(a_bin, 2) if a_bin[0]=='0' else int(a_bin,2)-256}, "
          f"B={int(b_bin, 2) if b_bin[0]=='0' else int(b_bin,2)-256}, "
          f"结果={int(result,2) if result[0]=='0' else int(result,2)-256}）")

    return result


# ---------- 测试示例 ----------
if __name__ == '__main__':
    print("示例 1：5 + 3")
    r1 = add_binary('00000101', '00000011')
    print(f"返回结果: {r1}\n")

    print("示例 2：-1 + 1（补码 11111111 + 00000001）")
    r2 = add_binary('11111111', '00000001')
    print(f"返回结果: {r2}\n")

    print("示例 3：-5 + 3（补码 11111011 + 00000011）")
    r3 = add_binary('11111011', '00000011')
    print(f"返回结果: {r3}\n")

    print("示例 4：127 + 1（溢出测试）")
    r4 = add_binary('01111111', '00000001')
    print(f"返回结果: {r4}")
