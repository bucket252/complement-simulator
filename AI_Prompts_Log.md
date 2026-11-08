# AI 结对编程过程记录
 
## 记录一：原码/反码/补码的转换实现（1号同学）
- **用户提示词**：你是一个资深Python程序员。请帮我写一个函数。函数名叫get_codes(num. bits)。输入一个十进制整数或位数。请返回它的原码、反码、补码的字符串表示(中间用空格隔开.比如
00000101')。请加上详细的中文注释。
- **AI 原始输出**：#.--边界校验.
if not isinstance (bits. int) or bits <1:
raise ValueError("bits 必须是太于等于!的正整数")
#n位有符号整数范围:[-2^(bits-1).2"
(bits-1)-11
min_val=-(1<<(bits-1)) max_val=(1<<(bits-1))-1 if not isinstance (num. int):
raise TypeError("num 必须是十进制整数")
if not (min_val <= num <= max_val)
raise OverflowError(f"数字(num)超出(bits)位有符号整数范围[(min.val),(max va[\]")

if num>=0
#==========正数处理=========

#bin()返回'Obxxxxx'，切片去掉Ob.zfill外商到t信
origin=bin(num)[2:].zfill(bits)
reverse=origin#正数反码=原码 complement=origin#正数补码=原码 else:
#==========负数处理=========

abs_num=-num
#先写出绝对值的二进制，补齐bits-1住(留给符号位)
abs_bin=bin(abs_num)[2:].zfill(bits-1)#原码:符号位固定1+绝对值二进制 origin="1"+abs_bin
#反码:符号位不变，后面数值位逐

任取改
sign_bit=origin[0] value_bits=origin[1:]
#按位取反:'0''1.'1''0
reversed_value ="join('1 if c== '0' else(' for c in value_bits)
reverse = sign_bit + reversed_value

#补码=反码+1
#把反码字符串转成整数，+1.再转回二进制，去掉Ob.补前导0
reverse_int= int(reverse.2) complement_int = reverse_int +1
complement = bin(complement_int)[2:]. zfill(bits)

#拼接三个码.空格隔开返回
return f"(origin) (reverse) (complement)"
#一	测试示例	
if__name__==	"_.main_."	
print(get_codes(5.8))#正数5.8位 print(get_codes(-5.8))#负数-5.8位 print(get_codes(0.8))#数字0.8位 print(get_codes(-1.4)) #-1.4位
运行输出示例
- **发现的问题**：AI没处理-128，运行时报错
- **人工微调与修复**：修改提示词，专门告知AI 8位补码规则：8位补码范围是-128~127，-128只有补码，没有对应的原码和反码。要求代码单独对输入-128做特殊分支判断，直接返回补码10000000，避免程序报错<img width="1206" height="2622" alt="49d8705fdeddbad87108f3737883c1ef" src="https://github.com/user-attachments/assets/5922c262-73a5-4f94-9aad-834f791a6ad6" />



 
## 记录二：补码加法与溢出的判断（2号同学）
- **用户提示词**：你是一个资深Python程序员.请帮我写一个函数，函数名叫 add_binary(a_bin, b_bin)。输入是两个8位的二进制补码字符串(比如'00000101'和
'00000011')。请帮我实现它们按位相加的过程，并且打印出每一位的进位情况,最后返回相加后的8位结果字符串.请加上详细的中文注释.
- **AI 原始输出**：def add_binary(a_bin: str, b_bin: str) -> str:
    """
    对两个 8 位二进制补码字符串进行按位相加，并打印每一位的进位情况。

    参数:
        a_bin: 8 位二进制补码字符串，例如 '00000101'
        b_bin: 8 位二进制补码字符串，例如 '00000011'

    返回:
        相加后的 8 位二进制结果字符串（截断最高位的溢出）

    说明:
        - 采用从最低位(索引7)到最高位(索引0)的顺序依次相加，模拟硬件全加器。
        - 由于补码的加法规则与无符号二进制加法一致（只是最终结果按补码解释），
          因此直接按位加即可，最高位的进位丢弃（8 位定长）。
        - 每一位的计算：sum = a_bit + b_bit + carry_in
                       result_bit = sum % 2
                       carry_out = sum // 2
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
        # 位序从 0（最低位）到 7（最高位）显示更符合习惯
        bit_pos = 7 - i
        print(f"{bit_pos:<6}{a_bit:<6}{b_bit:<6}{carry:<10}"
              f"{result_bit:<6}{carry_out:<10}{result_bit:<6}")

        # 更新进位，供下一位使用
        carry = carry_out

    # ---------- 3. 处理最高位之后的最终进位 ----------
    # 对于 8 位定长补码，最终进位（carry）表示溢出，被丢弃
    print("-" * 60)
    if carry:
        print(f"最高位产生的最终进位 = {carry}（溢出，8 位定长补码中丢弃）")
    else:
        print("最高位无最终进位（无溢出）")

    result = ''.join(result_bits)

    # ---------- 4. 打印最终结果 ----------
    print(f"相加结果 = {result}")
    # 顺便解释一下结果的补码含义（方便验证）
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
    print(f"返回结果: {r3}")
- **发现的问题**：AI计算127+1，没有做溢出检测，不会提示溢出
- **人工微调与修复**：重新给AI写提示词，要求增加符号位溢出判断逻辑：两个正数相加结果为负数、或两个负数相加结果为正数时判定溢出。测试用例127 + 1，运算后自动识别溢出并打印溢出提示，不能只输出计算结果。<img width="1080" height="2388" alt="bc1d60171369f9f1480851aa21b1f3c2" src="https://github.com/user-attachments/assets/a85d5aff-0db4-4660-8d78-5372313b8a48" />

 
## 记录三：Tkinter 界面代码的生成（3号同学）
- **用户提示词**：（待填）。
- **AI 原始输出**：（待填）
- **发现的问题**：（待填）
- **人工微调与修复**：（待填）
