# AI 结对编程过程记录
 
## 记录一：原码/反码/补码的转换实现（1号同学）
- **用户提示词**：
> "你是一个资深Python程序员。请帮我写一个函数。函数名叫`get_codes(num, bits)`。输入一个十进制整数和位数。请返回它的原码、反码、补码的字符串表示（中间用空格隔开，比如 '00000101'）。请加上详细的中文注释。"

- **AI原始输出**：
```python
def get_codes(num, bits):
    if not isinstance(bits, int) or bits < 1:
        raise TypeError("bits 必须是大于等于1的正整数")
    # n位有符号整数范围: [-2^(bits-1), 2^(bits-1)-1]
    min_val = -(1 << (bits - 1))
    max_val = (1 << (bits - 1)) - 1
    if not isinstance(num, int):
        raise TypeError("num 必须是十进制整数")
    if not (min_val <= num <= max_val):
        raise OverflowError(f"数字{num}超出{bits}位有符号整数范围[{min_val},{max_val}]")

    # ==========正数处理==========
    if num >= 0:
        # bin()返回'0bxxxxxx'，切片去掉0b，zfill补高位到bits位
        origin_bin = bin(num)[2:].zfill(bits)
        reverse_bin = origin_bin
        complement_bin = origin_bin
    # ==========负数处理==========
    else:
        abs_num = -num
        # 先写出绝对值的二进制，补齐bits-1位(留给符号位)
        abs_bin = bin(abs_num)[2:].zfill(bits - 1)
        # 符号位固定为1，绝对值做二进制
        origin_bin = "1" + abs_bin
        # 反码：符号位不变，后面数值位取反
        sign_bit = origin_bin[0]
        value_bits = origin_bin[1:]
        reversed_value = "".join('1' if c == '0' else '0' for c in value_bits)
        reverse_bin = sign_bit + reversed_value
        # 补码 = 反码 +1
        temp = int(reverse_bin, 2) + 1
        complement_bin = bin(temp)[2:].zfill(bits)
    return f"{origin_bin} {reverse_bin} {complement_bin}"


if __name__ == "__main__":
    print(get_codes(5,8))
运行输出示例
- **发现的问题**： AI 没处理 8 位补码的特殊值 -128。在 8 位下，-128 只有补码 10000000，没有原码和反码，导致程序运行报错。
- **人工微调与修复**：修改提示词，专门告知AI 8位补码规则：8位补码范围是-128~127，-128只有补码，没有对应的原码和反码。要求代码单独对输入-128做特殊分支判断，直接返回补码10000000，避免程序报错
<img width="1206" height="2622" alt="49d8705fdeddbad87108f3737883c1ef" src="https://github.com/user-attachments/assets/5922c262-73a5-4f94-9aad-834f791a6ad6" />



 
## 记录二：补码加法器的实现（2号同学）
- **用户提示词**：
> "你是一个资深Python程序员。请帮我写一个补码加法器。函数名叫`add_twos_complement(a, b, bits)`。输入两个十进制整数和位数，请返回它们用补码相加后的结果字符串，格式要求为'补码和 = 结果'。请加上详细的中文注释，并处理溢出情况。"

- **AI原始输出**：
```python
def add_twos_complement(a, b, bits):
    if not isinstance(bits, int) or bits < 1:
        raise TypeError("bits 必须是大于等于1的正整数")

    min_val = -(1 << (bits - 1))
    max_val = (1 << (bits - 1)) - 1

    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("a 和 b 必须是十进制整数")

    if not (min_val <= a <= max_val) or not (min_val <= b <= max_val):
        raise OverflowError(f"输入数字超出{bits}位补码范围[{min_val},{max_val}]")

    # 把负数转为对应补码无符号整数
    a_unsigned = a & ((1 << bits) - 1)
    b_unsigned = b & ((1 << bits) - 1)

    # 补码加法：直接按无符号整数相加，再截断到 bits 位
    sum_unsigned = (a_unsigned + b_unsigned) & ((1 << bits) - 1)

    # 判断溢出：两个正数相加结果为负，或两个负数相加结果为正
    a_sign = (a >> (bits - 1)) & 1
    b_sign = (b >> (bits - 1)) & 1
    sum_sign = (sum_unsigned >> (bits - 1)) & 1

    overflow = (a_sign == b_sign) and (a_sign != sum_sign)

    # 转成补码字符串
    complement_str = bin(sum_unsigned)[2:].zfill(bits)

    # 输出结果
    result = f"补码和 = {complement_str}"
    if overflow:
        result += "（溢出）"

    return result


if __name__ == "__main__":
    print(add_twos_complement(5, 3, 8))
    print(add_twos_complement(-1, -2, 8))
- **发现的问题**：AI计算127+1，没有做溢出检测，不会提示溢出
- **人工微调与修复**：重新给AI写提示词，要求增加符号位溢出判断逻辑：两个正数相加结果为负数、或两个负数相加结果为正数时判定溢出。测试用例127 + 1，运算后自动识别溢出并打印溢出提示，不能只输出计算结果。
<img width="1080" height="2388" alt="bc1d60171369f9f1480851aa21b1f3c2" src="https://github.com/user-attachments/assets/a85d5aff-0db4-4660-8d78-5372313b8a48" />

 
## 记录三：Tkinter 界面代码的生成（3号同学）
- **用户提示词**：（待填）。
- **AI 原始输出**：（待填）
- **发现的问题**：（待填）
- **人工微调与修复**：（待填）
