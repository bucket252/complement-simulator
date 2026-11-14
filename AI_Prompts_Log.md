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
- **用户提示词**："你是一个资深 Python GUI 开发者。请用 Tkinter 帮我写一个窗口程序。要求：窗口大小 800x600，标题叫‘补码加减法模拟器’。窗口里面需要有：
1. 两个输入框（分别用来输入数字A和数字B）。
2. 一个下拉菜单（可以选择 8 位或 16 位）。
3. 两个按钮，一个叫‘计算’，一个叫‘重置’。
4. 一个大大的多行文本框（用来显示计算过程和结果）。
请帮我把这些组件整齐地排列好，加上详细的中文注释。"

- **AI 原始输出**：```python
import tkinter as tk
from tkinter import ttk

# ========== 底层补码运算函数（项目原有逻辑，直接使用） ==========
def add_binary(a_bin, b_bin):
    """8位二进制补码加法，返回结果字符串+溢出标记"""
    width = len(a_bin)
    carry = 0
    result = []
    overflow = False
    # 从最低位逐位相加
    for ai, bi in reversed(list(zip(a_bin, b_bin))):
        a = int(ai)
        b = int(bi)
        total = a + b + carry
        bit = total % 2
        carry = total // 2
        result.insert(0, str(bit))
    # 溢出判断：两个符号位相同，但结果符号位相反
    if a_bin[0] == b_bin[0] and result[0] != a_bin[0]:
        overflow = True
    res_str = "".join(result)
    return res_str, overflow

def int2twos(num, bits):
    """十进制转对应位数补码字符串"""
    limit = 1 << (bits - 1)
    if not (-limit <= num <= limit -1):
        raise ValueError(f"数字超出{bits}位补码范围！范围：{-limit} ~ {limit-1}")
    if num >= 0:
        raw = bin(num)[2:].zfill(bits)
    else:
        raw = bin(2**bits + num)[2:]
    return raw

# ========== Tkinter GUI界面 ==========
root = tk.Tk()
root.title("补码加减法模拟器")
root.geometry("800x600")

# 标签与输入框
tk.Label(root, text="数字A：", font=("SimSun",12)).place(x=40, y=30)
entry_a = tk.Entry(root, font=("SimSun",12), width=15)
entry_a.place(x=110, y=30)

tk.Label(root, text="数字B：", font=("SimSun",12)).place(x=300, y=30)
entry_b = tk.Entry(root, font=("SimSun",12), width=15)
entry_b.place(x=370, y=30)

# 位数下拉选择
tk.Label(root, text="位数：", font=("SimSun",12)).place(x=540, y=30)
bit_var = tk.StringVar(value="8位")
combo_bit = ttk.Combobox(root, textvariable=bit_var, values=["8位","16位"], width=8, state="readonly")
combo_bit.place(x=595, y=30)

# 多行文本框，输出计算过程
tk.Label(root, text="计算过程与结果：", font=("SimSun",12)).place(x=40,y=80)
txt_out = tk.Text(root, font=("SimSun",11), width=90, height=22)
txt_out.place(x=40, y=110)

# 计算按钮回调
def on_calc():
    txt_out.delete(1.0, tk.END)
    try:
        numA = int(entry_a.get())
        numB = int(entry_b.get())
        bits = 8 if bit_var.get()=="8位" else 16
        binA = int2twos(numA, bits)
        binB = int2twos(numB, bits)
        res_bin, overflow = add_binary(binA, binB)
        res_dec = int(res_bin,2)
        if res_dec >= (1 << (bits-1)):
            res_dec -= (1 << bits)
        txt_out.insert(tk.END, f"A={numA}, 补码：{binA}\n")
        txt_out.insert(tk.END, f"B={numB}, 补码：{binB}\n")
        txt_out.insert(tk.END, f"补码相加结果：{res_bin}\n")
        txt_out.insert(tk.END, f"十进制结果：{res_dec}\n")
        txt_out.insert(tk.END, f"溢出判定：{'发生溢出' if overflow else '无溢出'}\n")
    except Exception as e:
        txt_out.insert(tk.END, f"输入错误！{str(e)}")

# 重置按钮回调
def on_reset():
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    txt_out.delete(1.0, tk.END)

btn_calc = tk.Button(root, text="计算", command=on_calc, font=("SimSun",11), width=10)
btn_calc.place(x=180, y=530)
btn_reset = tk.Button(root, text="重置", command=on_reset, font=("SimSun",11), width=10)
btn_reset.place(x=400, y=530)

root.mainloop()
- **发现的问题**：
1. 仅实现加法，没有减法功能（补码减法 = A + (-B)，代码没有处理取负逻辑）

2. 没有分步展示原码、反码、补码转换的过程，只直接输出最终补码，不满足模拟器分步演示的需求

- **人工微调与修复**：
- 修改提示词，增加需求：支持加减法切换，并且输出原码、反码、补码的每一步转换过程，把减法转换为加上B负数的补码，打印每一步演算细节。
- <img width="1156" height="2510" alt="59d20be485be13366dd943896857b76a" src="https://github.com/user-attachments/assets/77ce08f9-df51-4838-a1c2-23840ff1c48a" />

