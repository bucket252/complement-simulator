# -*- coding: utf-8 -*-
"""
补码加减法模拟器
----------------
使用 Tkinter 编写的 GUI 程序，支持：
  1. 输入两个整数 A、B（支持负数）
  2. 选择 8 位或 16 位字长
  3. 计算 A+B 与 A-B 的补码运算过程
  4. 展示原码、反码、补码、运算过程、溢出判断等详细信息
"""

import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# 一、补码运算的核心函数（与 GUI 分离，便于测试与复用）
# ============================================================

def int_to_twos_complement(value: int, bits: int) -> str:
    """
    将整数转换成指定字长的补码二进制字符串。
    原理：Python 的整数是无限精度的，负数直接用 (1<<bits)+value 转换为无符号数即可。
    """
    # 先做范围检查：n 位补码能表示的范围是 [-2^(n-1), 2^(n-1)-1]
    min_val = -(1 << (bits - 1))
    max_val = (1 << (bits - 1)) - 1
    if value < min_val or value > max_val:
        raise ValueError(f"{value} 超出 {bits} 位补码可表示范围 [{min_val}, {max_val}]")

    # 负数转成无符号表示，正数直接使用
    if value < 0:
        value = (1 << bits) + value
    # 格式化为定长二进制字符串，前面补 0
    return format(value, f"0{bits}b")


def twos_complement_to_int(binary_str: str) -> int:
    """
    将补码二进制字符串转换回整数。
    原理：最高位为 1 表示负数，值为 二进制值 - 2^bits。
    """
    bits = len(binary_str)
    value = int(binary_str, 2)
    # 最高位是 1 则为负数
    if binary_str[0] == '1':
        value -= (1 << bits)
    return value


def add_binary(a: str, b: str, bits: int) -> tuple:
    """
    按位做二进制加法（模拟硬件加法器）。
    返回 (结果位串, 最高位进位, 次高位进位)。
    这两个进位用于判断溢出。
    """
    result = []          # 存放结果的每一位
    carry = 0            # 当前进位
    carry_out_msb = 0    # 最高位产生的进位（第 bits 位）
    carry_out_prev = 0   # 次高位产生的进位（第 bits-1 位）

    # 从最低位往最高位逐位相加
    for i in range(bits - 1, -1, -1):
        ai = int(a[i])
        bi = int(b[i])
        s = ai + bi + carry
        result.append(str(s & 1))   # 本位结果
        carry = s >> 1              # 新的进位
        # 记录关键位置的两个进位
        if i == 0:        # 处理完最高位后 carry 就是最高位进位
            carry_out_msb = carry
        if i == 1:        # 处理完次高位后的进位
            carry_out_prev = carry

    # 注意：循环结束后 carry 是"最高位相加后的进位"，
    # 但为了更直观，我们上面已经记录了 i==0 时的进位。
    # 修正：i==0 时 carry 还未被使用，此时计算完得到的就是最高位进位。
    carry_out_msb = carry

    # result 是逆序的，需要翻转回来
    result_str = "".join(reversed(result))
    return result_str, carry_out_msb, carry_out_prev


def detect_overflow(a_bits: str, b_bits: str, result_bits: str) -> bool:
    """
    判断溢出（针对加法）：
    同号相加结果变号，则溢出。
    也等价于：最高位进位 XOR 次高位进位 = 1
    """
    sign_a = a_bits[0]
    sign_b = b_bits[0]
    sign_r = result_bits[0]
    # 同号且结果异号 → 溢出
    return sign_a == sign_b and sign_r != sign_a


def binary_group(bits_str: str) -> str:
    """把二进制串每 4 位用空格分组，方便阅读。"""
    groups = []
    for i in range(0, len(bits_str), 4):
        groups.append(bits_str[i:i + 4])
    return " ".join(groups)


# ============================================================
# 二、GUI 界面部分
# ============================================================

class ComplementSimulator:
    """补码加减法模拟器主类，封装所有控件与事件。"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("补码加减法模拟器")
        self.root.geometry("800x600")
        self.root.resizable(False, False)  # 固定窗口大小，布局更稳定

        # ---------- 顶部输入区 ----------
        # 用一个 Frame 把所有输入控件打包，方便整体布局
        input_frame = tk.Frame(root)
        input_frame.pack(pady=12, padx=20, fill="x")

        # 数字 A 的标签 + 输入框
        tk.Label(input_frame, text="数字 A：", font=("微软雅黑", 12)).grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        self.entry_a = tk.Entry(input_frame, font=("Consolas", 12), width=18)
        self.entry_a.grid(row=0, column=1, padx=5, pady=5)

        # 数字 B 的标签 + 输入框
        tk.Label(input_frame, text="数字 B：", font=("微软雅黑", 12)).grid(
            row=0, column=2, sticky="e", padx=5, pady=5
        )
        self.entry_b = tk.Entry(input_frame, font=("Consolas", 12), width=18)
        self.entry_b.grid(row=0, column=3, padx=5, pady=5)

        # 字长选择下拉框
        tk.Label(input_frame, text="字长：", font=("微软雅黑", 12)).grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        self.bits_var = tk.StringVar(value="8 位")
        self.combo_bits = ttk.Combobox(
            input_frame,
            textvariable=self.bits_var,
            values=["8 位", "16 位"],
            state="readonly",
            width=10,
            font=("微软雅黑", 11)
        )
        self.combo_bits.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # ---------- 按钮区 ----------
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        self.btn_calc = tk.Button(
            btn_frame, text="计算", width=12, height=2,
            font=("微软雅黑", 12, "bold"),
            bg="#4CAF50", fg="white", activebackground="#45a049",
            command=self.on_calculate
        )
        self.btn_calc.pack(side="left", padx=15)

        self.btn_reset = tk.Button(
            btn_frame, text="重置", width=12, height=2,
            font=("微软雅黑", 12, "bold"),
            bg="#f44336", fg="white", activebackground="#d32f2f",
            command=self.on_reset
        )
        self.btn_reset.pack(side="left", padx=15)

        # ---------- 结果输出区（多行文本框） ----------
        # 用 Frame 包裹 Text 和 Scrollbar，实现带滚动条的文本框
        output_frame = tk.Frame(root)
        output_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.text_output = tk.Text(
            output_frame,
            font=("Consolas", 12),
            bg="#1e1e1e", fg="#dcdcdc",   # 深色背景，像终端
            insertbackground="white",
            wrap="word",
            relief="sunken",
            borderwidth=2
        )
        self.text_output.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(output_frame, command=self.text_output.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_output.config(yscrollcommand=scrollbar.set)

        # 首次运行时给一段提示文字
        self.show_welcome()

    # ---------------- 事件处理函数 ----------------

    def show_welcome(self):
        """在结果框显示欢迎/提示信息。"""
        self.text_output.delete("1.0", "end")
        hint = (
            "欢迎使用 补码加减法模拟器！\n"
            "─────────────────────────────────────\n"
            "使用说明：\n"
            "  1. 在『数字 A』『数字 B』中输入整数（支持负数，如 -5）\n"
            "  2. 选择字长（8 位 或 16 位）\n"
            "  3. 点击『计算』查看补码运算过程\n"
            "  4. 点击『重置』清空所有内容\n"
        )
        self.text_output.insert("1.0", hint)

    def on_reset(self):
        """重置：清空输入框、恢复默认字长、清空输出区。"""
        self.entry_a.delete(0, "end")
        self.entry_b.delete(0, "end")
        self.bits_var.set("8 位")
        self.text_output.delete("1.0", "end")
        self.entry_a.focus_set()

    def on_calculate(self):
        """计算按钮的回调：读取输入 → 校验 → 计算 → 显示。"""
        # 1) 读取并校验输入
        try:
            a = int(self.entry_a.get().strip())
            b = int(self.entry_b.get().strip())
        except ValueError:
            messagebox.showerror("输入错误", "请输入合法的整数（支持负数）！")
            return

        # 2) 读取字长
        bits = 8 if self.bits_var.get().startswith("8") else 16

        # 3) 检查取值范围
        min_val = -(1 << (bits - 1))
        max_val = (1 << (bits - 1)) - 1
        if not (min_val <= a <= max_val):
            messagebox.showerror(
                "范围错误", f"数字 A = {a} 超出 {bits} 位补码范围 [{min_val}, {max_val}]"
            )
            return
        if not (min_val <= b <= max_val):
            messagebox.showerror(
                "范围错误", f"数字 B = {b} 超出 {bits} 位补码范围 [{min_val}, {max_val}]"
            )
            return

        # 4) 计算并展示
        self.perform_and_display(a, b, bits)

    # ---------------- 核心显示逻辑 ----------------

    def perform_and_display(self, a: int, b: int, bits: int):
        """执行补码加法/减法并把过程写入文本框。"""
        self.text_output.delete("1.0", "end")

        # ---- 先计算 A、B 的补码 ----
        comp_a = int_to_twos_complement(a, bits)
        comp_b = int_to_twos_complement(b, bits)

        # ---- 计算 -B 的补码（用于减法 A - B = A + (-B)） ----
        # 方法：把 B 的补码按位取反再加 1（这就是求相反数补码的标准做法）
        # 也可以直接调用 int_to_twos_complement(-b, bits)，这里演示按位运算
        comp_neg_b = int_to_twos_complement(-b, bits)

        # 记录输出内容的列表，最后一次性写入
        lines = []
        sep = "═" * 60
        thin = "─" * 60

        lines.append(sep)
        lines.append(f"  补码加减法模拟器  |  字长：{bits} 位  |  A = {a}, B = {b}")
        lines.append(sep)

        # ============ 第一部分：原数与补码表示 ============
        lines.append("\n【一、补码表示】\n")
        lines.append(f"  可表示范围：{-(1 << (bits - 1))} ~ {(1 << (bits - 1)) - 1}\n")

        lines.append(f"  数字 A = {a}")
        lines.append(f"    补码 = {binary_group(comp_a)}  (二进制 {comp_a})")
        lines.append(f"    数值 = {twos_complement_to_int(comp_a)}")

        lines.append(f"\n  数字 B = {b}")
        lines.append(f"    补码 = {binary_group(comp_b)}  (二进制 {comp_b})")
        lines.append(f"    数值 = {twos_complement_to_int(comp_b)}")

        lines.append(f"\n  -B = {-b}")
        lines.append(f"    补码 = {binary_group(comp_neg_b)}  (二进制 {comp_neg_b})")

        # ============ 第二部分：加法 A + B ============
        lines.append(f"\n{thin}")
        lines.append(f"【二、加法运算：A + B = {a} + ({b})】\n")

        sum_bits, carry_msb, carry_prev = add_binary(comp_a, comp_b, bits)
        overflow_add = detect_overflow(comp_a, comp_b, sum_bits)
        sum_value = twos_complement_to_int(sum_bits)

        # 用"竖式"形式展示
        lines.append(f"     A  补码 = {binary_group(comp_a)}")
        lines.append(f"  +  B  补码 = {binary_group(comp_b)}")
        lines.append(f"    {thin[4:]}")
        lines.append(f"     结果补码 = {binary_group(sum_bits)}")

        lines.append(f"\n  最高位进位 = {carry_msb}")
        lines.append(f"  次高位进位 = {carry_prev}   （两者异或 = {carry_msb ^ carry_prev}）")

        if overflow_add:
            lines.append("  ⚠ 判断：发生溢出！结果不可信。")
            lines.append(f"  理论正确结果 = {a + b}，超出 {bits} 位补码范围。")
        else:
            lines.append(f"  ✔ 无溢出，结果补码对应的数值 = {sum_value}")
            # 若是负数，额外展示原码让用户直观感受
            if sum_value < 0:
                # 原码 = 符号位保持，数值位取反加一（从补码反推）
                mag = (1 << (bits - 1)) - (-sum_value) if False else None
                lines.append(f"    （负数补码，最高位为 1 表示负号）")

        # ============ 第三部分：减法 A - B ============
        lines.append(f"\n{thin}")
        lines.append(f"【三、减法运算：A - B = A + (-B) = {a} + ({-b})】\n")

        diff_bits, carry_msb2, carry_prev2 = add_binary(comp_a, comp_neg_b, bits)
        overflow_sub = detect_overflow(comp_a, comp_neg_b, diff_bits)
        diff_value = twos_complement_to_int(diff_bits)

        lines.append(f"     A  补码 = {binary_group(comp_a)}")
        lines.append(f"  + (-B)补码 = {binary_group(comp_neg_b)}")
        lines.append(f"    {thin[4:]}")
        lines.append(f"     结果补码 = {binary_group(diff_bits)}")

        lines.append(f"\n  最高位进位 = {carry_msb2}")
        lines.append(f"  次高位进位 = {carry_prev2}   （两者异或 = {carry_msb2 ^ carry_prev2}）")

        if overflow_sub:
            lines.append("  ⚠ 判断：发生溢出！结果不可信。")
            lines.append(f"  理论正确结果 = {a - b}，超出 {bits} 位补码范围。")
        else:
            lines.append(f"  ✔ 无溢出，结果补码对应的数值 = {diff_value}")

        # ============ 结尾小结 ============
        lines.append(f"\n{sep}")
        if not overflow_add:
            lines.append(f"  最终：A + B = {a + b}")
        else:
            lines.append(f"  最终：A + B = {a + b} （溢出，{bits} 位下无法表示）")
        if not overflow_sub:
            lines.append(f"        A - B = {a - b}")
        else:
            lines.append(f"        A - B = {a - b} （溢出，{bits} 位下无法表示）")
        lines.append(sep)

        # 写入文本框
        self.text_output.insert("1.0", "\n".join(lines))


# ============================================================
# 三、程序入口
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    # 让字体在 Windows 上更清晰（可选）
    try:
        root.tk.call("tk", "scaling", 1.2)
    except Exception:
        pass
    app = ComplementSimulator(root)
    root.mainloop()
