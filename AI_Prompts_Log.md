# AI 结对编程过程记录

## 记录一：原码/反码/补码的转换实现（1号同学）

**用户提示词**：你是一个资深Python程序员。请帮我写一个函数。函数名叫get_codes(num. bits)。输入一个十进制整数或位数。请返回它的原码、反码、补码的字符串表示(中间用空格隔开.比如
00000101')。请加上详细的中文注释。

**AI 原始输出**：

```python
#.--边界校验.
if not isinstance(bits, int) or bits < 1:
    raise ValueError("bits 必须是太于等于!的正整数")
#n位有符号整数范围:[-2^(bits-1).2"
# (bits-1)-11
min_val = -(1 << (bits-1))
max_val = (1 << (bits-1)) - 1
if not isinstance(num, int):
    raise TypeError("num 必须是十进制整数")
if not (min_val <= num <= max_val):
    raise OverflowError(f"数字(num)超出(bits)位有符号整数范围[{min_val},{max_val}]")

if num >= 0:
    #==========正数处理=========
    #bin()返回'Obxxxxx'，切片去掉Ob.zfill外商到t信
    origin = bin(num)[2:].zfill(bits)
    reverse = origin  #正数反码=原码 
    complement = origin  #正数补码=原码 
else:
    #==========负数处理=========
    abs_num = -num
    #先写出绝对值的二进制，补齐bits-1住(留给符号位)
    abs_bin = bin(abs_num)[2:].zfill(bits-1)  #原码:符号位固定1+绝对值二进制 
    origin = "1" + abs_bin
    
    #反码:符号位不变，后面数值位逐
    #任取改
    sign_bit = origin[0] 
    value_bits = origin[1:]
    #按位取反:'0''1.'1''0
    reversed_value = "".join('1' if c == '0' else '0' for c in value_bits)
    reverse = sign_bit + reversed_value

    #补码=反码+1
    #把反码字符串转成整数，+1.再转回二进制，去掉Ob.补前导0
    reverse_int = int(reverse, 2) 
    complement_int = reverse_int + 1
    complement = bin(complement_int)[2:].zfill(bits)

#拼接三个码.空格隔开返回
return f"{origin} {reverse} {complement}"

#一    测试示例    
if __name__ == "__main__":
    print(get_codes(5, 8))  #正数5.8位 
    print(get_codes(-5, 8))  #负数-5.8位 
    print(get_codes(0, 8))  #数字0.8位 
    print(get_codes(-1, 4))  #-1.4位
# 运行输出示例
```

**发现的问题**：AI没处理-128，运行时报错

**人工微调与修复**：修改提示词，专门告知AI 8位补码规则：8位补码范围是-128~127，-128只有补码，没有对应的原码和反码。要求代码单独对输入-128做特殊分支判断，直接返回补码10000000，避免程序报错<img width="1206" height="2622" alt="49d8705fdeddbad87108f3737883c1ef" src="https://github.com/user-attachments/assets/5922c262-73a5-4f94-9aad-834f791a6ad6" />

## 记录二：补码加法与溢出的判断（2号同学）

**用户提示词**：你是一个资深Python程序员.请帮我写一个函数，函数名叫 add_binary(a_bin, b_bin)。输入是两个8位的二进制补码字符串(比如'00000101'和
'00000011')。请帮我实现它们按位相加的过程，并且打印出每一位的进位情况,最后返回相加后的8位结果字符串.请加上详细的中文注释.

**AI 原始输出**：

```python
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
```

**发现的问题**：AI计算127+1，没有做溢出检测，不会提示溢出

**人工微调与修复**：重新给AI写提示词，要求增加符号位溢出判断逻辑：两个正数相加结果为负数、或两个负数相加结果为正数时判定溢出。测试用例127 + 1，运算后自动识别溢出并打印溢出提示，不能只输出计算结果。<img width="1080" height="2388" alt="bc1d60171369f9f1480851aa21b1f3c2" src="https://github.com/user-attachments/assets/a85d5aff-0db4-4660-8d78-5372313b8a48" />

## 记录三：Tkinter 界面代码的生成（3号同学）

**用户提示词**："你是一个资深 Python GUI 开发者。请用 Tkinter 帮我写一个窗口程序。要求：窗口大小 800x600，标题叫‘补码加减法模拟器’。窗口里面需要有：
1. 两个输入框（分别用来输入数字A和数字B）。
2. 一个下拉菜单（可以选择 8 位或 16 位）。
3. 两个按钮，一个叫‘计算’，一个叫‘重置’。
4. 一个大大的多行文本框（用来显示计算过程和结果）。
请帮我把这些组件整齐地排列好，加上详细的中文注释。"

**AI 原始输出**：

```python
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
```

**发现的问题**：
1. 仅实现加法，没有减法功能（补码减法 = A + (-B)，代码没有处理取负逻辑）

2. 没有分步展示原码、反码、补码转换的过程，只直接输出最终补码，不满足模拟器分步演示的需求
**人工微调与修复**：
- 修改提示词，增加需求：支持加减法切换，并且输出原码、反码、补码的每一步转换过程，把减法转换为加上B负数的补码，打印每一步演算细节。
- <img width="1156" height="2510" alt="59d20be485be13366dd943896857b76a" src="https://github.com/user-attachments/assets/77ce08f9-df51-4838-a1c2-23840ff1c48a" />

## 记录四：分步高亮与自动播放的实现（3号同学）
用户提示词：
> 我的 Tkinter 界面上有一个大文本框显示结果。现在请帮我新增三个按钮（上一步、下一步、自动播放），并教我怎么在界面上用 Label 组件（或者 Canvas），把我从一个列表里拿到的二进制字符（比如 ['0','0','0','0','0','1','0','1']）每一位画成一个独立的方块格子？

AI原始输出：
```python
import tkinter as tk
from tkinter import ttk, messagebox

# ====================== 【1号同学】convert.py 函数 ======================
def get_codes(num, bits):
    if bits == 8 and num == -128:
        return {
            "yuan": "无",
            "fan": "无",
            "bu": "10000000"
        }
    if num >= 0:
        binary = bin(num)[2:].zfill(bits)
        yuan = binary
        fan = binary
        bu = binary
    else:
        abs_num = -num
        abs_bin = bin(abs_num)[2:].zfill(bits)
        yuan = "1" + abs_bin[1:]
        fan_list = []
        for idx, c in enumerate(yuan):
            if idx == 0:
                fan_list.append(c)
            else:
                fan_list.append("1" if c == "0" else "0")
        fan = "".join(fan_list)
        fan_int = int(fan, 2)
        bu_int = fan_int + 1
        bu = bin(bu_int)[2:].zfill(bits)
    return {"yuan": yuan, "fan": fan, "bu": bu}

# ====================== 【2号同学】calc.py 加法函数 ======================
def add_binary_with_steps(a_bin: str, b_bin: str, bits: int) -> dict:
    if len(a_bin) != bits or len(b_bin) != bits:
        raise ValueError(f"输入字符串长度必须等于 {bits}")

    result_bits = ['0'] * bits
    carry = 0
    steps = []
    # 从右往左（低位到高位）遍历
    for i in range(bits - 1, -1, -1):
        bit_idx = bits - 1 - i
        a_bit = int(a_bin[i])
        b_bit = int(b_bin[i])
        total = a_bit + b_bit + carry
        result_bit = total % 2
        carry_out = total // 2

        steps.append({
            "bit_idx": bit_idx,
            "a_bit": a_bit,
            "b_bit": b_bit,
            "carry_in": carry,
            "sum": result_bit,
            "carry_out": carry_out
        })
        result_bits[i] = str(result_bit)
        carry = carry_out
    sign_a = int(a_bin[0])
    sign_b = int(b_bin[0])
    sign_res = int(result_bits[0])
    is_overflow = (sign_a == sign_b) and (sign_a != sign_res)
    result = ''.join(result_bits)
    return {"result": result, "is_overflow": is_overflow, "steps": steps}

# ====================== 【3号同学】UI主界面+高亮逻辑 ======================
class ComplementSimulator:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("补码加减法模拟器")
        self.root.geometry("950x750")
        self.root.resizable(False, False)
        # 动画状态
        self.steps = []
        self.current_step_idx = 0
        self.is_playing = False
        self.after_id = None
        # 存储方块控件，用来做高亮
        self.ui_blocks = {'yuan': [], 'fan': [], 'bu': []}

        input_frame = tk.Frame(root)
        input_frame.pack(pady=12, padx=20, fill="x")
        tk.Label(input_frame, text="数字 A：", font=("微软雅黑", 12)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_a = tk.Entry(input_frame, font=("Consolas", 12), width=18)
        self.entry_a.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(input_frame, text="数字 B：", font=("微软雅黑", 12)).grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.entry_b = tk.Entry(input_frame, font=("Consolas", 12), width=18)
        self.entry_b.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(input_frame, text="字长：", font=("微软雅黑", 12)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.bits_var = tk.StringVar(value="8 位")
        self.combo_bits = ttk.Combobox(input_frame, textvariable=self.bits_var, values=["8 位", "16 位"], state="readonly", width=10, font=("微软雅黑", 11))
        self.combo_bits.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        self.btn_calc = tk.Button(btn_frame, text="计算", width=10, height=2, font=("微软雅黑", 12, "bold"), bg="#4CAF50", fg="white", command=self.on_calculate)
        self.btn_calc.pack(side="left", padx=5)
        self.btn_reset = tk.Button(btn_frame, text="重置", width=10, height=2, font=("微软雅黑", 12, "bold"), bg="#f44336", fg="white", command=self.on_reset)
        self.btn_reset.pack(side="left", padx=5)
        self.btn_prev = tk.Button(btn_frame, text="上一步", width=10, height=2, font=("微软雅黑", 12), state="disabled", command=self.prev_step)
        self.btn_prev.pack(side="left", padx=5)
        self.btn_next = tk.Button(btn_frame, text="下一步", width=10, height=2, font=("微软雅黑", 12), state="disabled", command=self.next_step)
        self.btn_next.pack(side="left", padx=5)
        self.btn_auto = tk.Button(btn_frame, text="自动播放", width=10, height=2, font=("微软雅黑", 12), state="disabled", command=self.toggle_auto_play)
        self.btn_auto.pack(side="left", padx=5)

        mid_frame = tk.Frame(root)
        mid_frame.pack(padx=20, pady=5, fill="both", expand=True)
        text_frame = tk.Frame(mid_frame)
        text_frame.pack(side="left", fill="both", expand=True)
        self.text_output = tk.Text(text_frame, font=("Consolas", 11), bg="#1e1e1e", fg="#dcdcdc", wrap="word", width=40)
        self.text_output.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(text_frame, command=self.text_output.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_output.config(yscrollcommand=scrollbar.set)

        self.canvas_frame = tk.Frame(mid_frame, bg="#f0f0f0", relief="sunken", borderwidth=2)
        self.canvas_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        self.lbl_animation_info = tk.Label(self.canvas_frame, text="等待计算...", font=("微软雅黑", 12, "bold"), bg="#f0f0f0", fg="red")
        self.lbl_animation_info.pack(pady=10)
        self.blocks_container = tk.Frame(self.canvas_frame, bg="#f0f0f0")
        self.blocks_container.pack(pady=20)
        self.show_welcome()

    def show_welcome(self):
        self.text_output.delete("1.0", "end")
        hint = (
            "欢迎使用 补码加减法模拟器！\n"
            "─────────────────────────────────────\n"
            "使用说明：\n"
            "  1. 输入数字 A 和 B\n"
            "  2. 点击『计算』生成结果\n"
            "  3. 右侧会生成动画格子，可使用下方的\n"
            "     『上一步』『下一步』或『自动播放』\n"
            "     查看加法进位的完整过程！\n"
        )
        self.text_output.insert("1.0", hint)

    def on_reset(self):
        self.entry_a.delete(0, "end")
        self.entry_b.delete(0, "end")
        self.bits_var.set("8 位")
        self.text_output.delete("1.0", "end")
        for widget in self.blocks_container.winfo_children():
            widget.destroy()
        self.lbl_animation_info.config(text="等待计算...")
        self.ui_blocks = {'yuan': [], 'fan': [], 'bu': []}
        self.btn_prev.config(state="disabled")
        self.btn_next.config(state="disabled")
        self.btn_auto.config(state="disabled")
        self.entry_a.focus_set()

    def on_calculate(self):
        a_str = self.entry_a.get().strip()
        b_str = self.entry_b.get().strip()
        try:
            if not a_str or not b_str:
                raise ValueError("输入为空")
            a = int(a_str)
            b = int(b_str)
        except ValueError:
            messagebox.showerror("错误", "请输入合法数字")
            return
        bits = 8 if self.bits_var.get().startswith("8") else 16
        min_val = -(1 << (bits - 1))
        max_val = (1 << (bits - 1)) - 1
        if not (min_val <= a <= max_val) or not (min_val <= b <= max_val):
            messagebox.showerror("范围错误", f"输入超出 {bits} 位范围 [{min_val}, {max_val}]")
            return
        self.perform_and_display(a, b, bits)

    def perform_and_display(self, a: int, b: int, bits: int):
        self.text_output.delete("1.0", "end")
        res_a = get_codes(a, bits)
        res_b = get_codes(b, bits)
        res_neg_b = get_codes(-b, bits)
        sum_result = add_binary_with_steps(res_a['bu'], res_b['bu'], bits)
        diff_result = add_binary_with_steps(res_a['bu'], res_neg_b['bu'], bits)
        lines = []
        lines.append(f"字长：{bits}位 | A = {a}, B = {b}\n")
        lines.append(f"A 补码：{res_a['bu']}")
        lines.append(f"B 补码：{res_b['bu']}\n")
        lines.append(f"A+B 结果：{sum_result['result']}")
        lines.append(f"溢出：{'是' if sum_result['is_overflow'] else '否'}")
        self.text_output.insert("1.0", "\n".join(lines))

        # 把加法运算步骤交给UI动画
        self.steps = sum_result['steps']
        self.current_step_idx = 0
        for widget in self.blocks_container.winfo_children():
            widget.destroy()
        self.ui_blocks = {'yuan': [], 'fan': [], 'bu': []}
        self.draw_row("A 补码:", res_a['bu'], "yuan")
        self.draw_row("B 补码:", res_b['bu'], "fan")
        self.draw_row("结  果:", sum_result['result'], "bu")
        self.btn_prev.config(state="normal")
        self.btn_next.config(state="normal")
        self.btn_auto.config(state="normal")
        self.update_step(0)

    def draw_row(self, title, binary_str, row_key):
        frame = tk.Frame(self.blocks_container, bg="#f0f0f0")
        frame.pack(pady=5)
        tk.Label(frame, text=title, font=("微软雅黑", 12), bg="#f0f0f0", width=8, anchor="e").pack(side="left", padx=5)
        bits = len(binary_str)
        for i in range(bits):
            bit_val = binary_str[i]
            bg_color = "#D3D3D3" if i == 0 else "#87CEFA"
            lbl = tk.Label(frame, text=bit_val, font=("Consolas", 16, "bold"), width=3, height=1, bg=bg_color, relief="raised", borderwidth=2)
            lbl.pack(side="left", padx=3)
            # 保存格子对应的bit索引（高亮关键代码）
            ui_idx = bits - 1 - i
            self.ui_blocks[row_key].append({'ui_idx': ui_idx, 'label': lbl, 'default_bg': bg_color})

    def update_step(self, step_idx):
        if not self.steps or step_idx < 0 or step_idx >= len(self.steps):
            return
        # 全部格子恢复原始颜色
        for row_key in self.ui_blocks:
            for block in self.ui_blocks[row_key]:
                block['label'].config(bg=block['default_bg'])
        step_data = self.steps[step_idx]
        target_bit = step_data['bit_idx']
        # 匹配索引，设置黄色高亮
        for row_key in self.ui_blocks:
            for block in self.ui_blocks[row_key]:
                if block['ui_idx'] == target_bit:
                    block['label'].config(bg="yellow")
        # 更新文字信息
        carry_in = step_data['carry_in']
        carry_out = step_data['carry_out']
        info_text = f"当前计算：第 {target_bit} 位 (bit_idx={target_bit})\n进位输入：{carry_in} -> 进位输出：{carry_out}"
        self.lbl_animation_info.config(text=info_text)

    def next_step(self):
        if self.current_step_idx < len(self.steps) - 1:
            self.current_step_idx += 1
            self.update_step(self.current_step_idx)

    def prev_step(self):
        if self.current_step_idx > 0:
            self.current_step_idx -= 1
            self.update_step(self.current_step_idx)

    def toggle_auto_play(self):
        if self.is_playing:
            self.is_playing = False
            self.btn_auto.config(text="自动播放")
            if self.after_id:
                self.root.after_cancel(self.after_id)
        else:
            self.is_playing = True
            self.btn_auto.config(text="暂停播放")
            self.auto_play_loop()

    def auto_play_loop(self):
        if not self.is_playing:
            return
        if self.current_step_idx < len(self.steps) - 1:
            self.current_step_idx += 1
            self.update_step(self.current_step_idx)
            self.after_id = self.root.after(1000, self.auto_play_loop)
        else:
            self.is_playing = False
            self.btn_auto.config(text="自动播放")

if __name__ == "__main__":
    root = tk.Tk()
    app = ComplementSimulator(root)
    root.mainloop()
```

发现的问题：
AI初次生成自动播放代码误用`time.sleep()`。Tkinter为单线程GUI，sleep阻塞主循环，点击自动播放后整个GUI窗口卡死，按钮完全无法点击，动画不能暂停。

人工微调与修复：
向AI强调tkinter禁止使用time.sleep，改用`root.after()`异步定时器；增加`after_id`保存定时器标识，播放暂停时执行`after_cancel()`取消定时任务；完善`draw_row()`保存每个二进制方块的索引，完善`update_step()`实现按位黄色高亮，实现完整可暂停的分步动画。

<img width="1140" height="1828" alt="b4b910959103af143bbc9c15655837a4" src="https://github.com/user-attachments/assets/3e4998d3-0ba8-4016-be85-21be53d1987a" />
<img width="1118" height="1735" alt="9f2ff1c47543fc687a0425c2b8e5e4ee" src="https://github.com/user-attachments/assets/f27d9555-8af6-4c86-aa28-4e5244ef791c" />


