def get_codes(num, bits):
    """
    计算一个整数的 原码、反码、补码，返回三者字符串，空格分隔
    :param num: int，十进制整数（可以是正数、负数、0）
    :param bits: int，二进制总位数，必须 >=1，例如 8 代表8位二进制
    :return: str
        正常情况："原码 反码 补码"，每一段都是固定长度bits的01字符串
        特殊情况：当是8位有符号数 -128 时，返回字符串 '该值没有原码和反码'
    规则说明：
        1. 最高位是符号位：0代表正数，1代表负数
        2. 正数：原码 = 反码 = 补码
        3. 负数：
            原码：符号位为1，数值位是该数绝对值的二进制
            反码：原码符号位不变，数值位按位取反
            补码：反码 + 1
        4. 重点特例：8位有符号数 -128，只有补码10000000，不存在原码、反码
        5. 如果数字超出 bits 位有符号整数表示范围，抛出异常
    """
    # ---------- 边界校验 ----------
    if not isinstance(bits, int) or bits < 1:
        raise ValueError("bits 必须是大于等于1的正整数")
    min_val = - (1 << (bits - 1))
    max_val = (1 << (bits - 1)) - 1
    if not isinstance(num, int):
        raise TypeError("num 必须是十进制整数")
    if not (min_val <= num <= max_val):
        raise OverflowError(f"数字 {num} 超出 {bits} 位有符号整数范围 [{min_val}, {max_val}]")

    # ======================
    # 【优先判断特例！！】命中直接返回，不会进入后面的计算
    # ======================
    if bits == 8 and num == -128:
        return '该值没有原码和反码'

    if num >= 0:
        # 正数
        origin = bin(num)[2:].zfill(bits)
        reverse = origin
        complement = origin
    else:
        # 普通负数（排除了-128）
        abs_num = -num
        abs_bin = bin(abs_num)[2:].zfill(bits - 1)
        origin = "1" + abs_bin

        sign_bit = origin[0]
        value_bits = origin[1:]
        reversed_value = ''.join('1' if c == '0' else '0' for c in value_bits)
        reverse = sign_bit + reversed_value

        reverse_int = int(reverse, 2)
        complement_int = reverse_int + 1
        complement = bin(complement_int)[2:].zfill(bits)

    return f"{origin} {reverse} {complement}"


# ------------------- 循环交互主程序 -------------------
if __name__ == "__main__":
    print("===== 原码、反码、补码查询工具 =====")
    print("输入 q 可以退出程序")
    while True:
        try:
            num_input = input("\n请输入十进制整数：")
            if num_input.lower() == 'q':
                print("程序退出！")
                break
            num = int(num_input)

            bits_input = input("请输入二进制位数：")
            if bits_input.lower() == 'q':
                print("程序退出！")
                break
            bits = int(bits_input)

            res = get_codes(num, bits)
            print(f"结果：{res}")

        except ValueError:
            print("输入错误！请输入合法整数。")
        except OverflowError as e:
            print(f"超出范围错误：{e}")
        except Exception as e:
            print(f"发生错误：{e}")
