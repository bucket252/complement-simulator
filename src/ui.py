import tkinter as tk
from tkinter import ttk, messagebox

# ============================================================
# 1 号同学的代码 (convert.py 拼装位置)
# ============================================================
def get_codes(num, bits):
    """
    计算指定位数下一个整数的原码、反码、补码，以字典返回
    特殊：bits=8且num=-128时，yuan='无'，fan='无'，bu='10000000'
    """
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


# ============================================================
# 2 号同学的代码 (calc.py 拼装位置)
# ============================================================
def add_binary(a_bin: str, b_bin: str, bits: int) -> dict:
    """
    对两个指定位数的二进制补码字符串执行补码加法
    """
    if len(a_bin) != bits or len(b_bin) != bits:
        raise ValueError(f"输入字符串长度必须等于 {bits}")
    if any(c not in '01' for c in a_bin) or any(c not in '01' for c in b_bin):
        raise ValueError("输入只能由字符 '0' 和 '1' 组成")

    result_bits = ['0'] * bits
    carry = 0

    for i in range(bits - 1, -1, -1):
        a_bit = int(a_bin[i])
        b_bit = int(b_bin[i])
        total = a_bit + b_bit + carry
        result_bit = total % 2
        carry_out = total // 2
        result_bits[i] = str(result_bit)
        carry = carry_out

    sign_a = int(a_bin[0])
    sign_b = int(b_bin[0])
    sign_res = int(result_bits[0])
    is_overflow = (sign_a == sign_b) and (sign_a != sign_res)

    result = ''.join(result_bits)
    return {"result": result, "is_overflow": is_overflow}


# ============================================================
# 你自己的代码 (ui.py 界面与拼装逻辑)
# ============================================================
class ComplementSimulator:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("补码加减法模拟器")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # ---------- 顶部输入区 ----------
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

        # ---------- 结果输出区 ----------
        output_frame = tk.Frame(root)
        output_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.text_output = tk.Text(
            output_frame,
            font=("Consolas", 12),
            bg="#1e1e1e", fg="#dcdcdc",
            insertbackground="white",
            wrap="word",
            relief="sunken",
            borderwidth=2
        )
        self.text_output.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(output_frame, command=self.text_output.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_output.config(yscrollcommand=scrollbar.set)

        self.show_welcome()

    def show_welcome(self):
        """在结果框显示欢迎/提示信息"""
        self.text_output.delete("1.0", "end")
        hint = (
            "欢迎使用 补码加减法模拟器！\n"
            "─────────────────────────────────────\n"
            "使用说明：\n"
            "  1. 在『数字 A』『数字 B』中输入整数（支持负数，如 -5）\n"
            "  2. 选择字长（8 位 或 16 位）\n"
            "  3. 点击『计算』同时查看加法和减法过程\n"
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
        """核心显示逻辑：使用拼装好的函数进行运算并展示"""
        self.text_output.delete("1.0", "end")

        # 1. 调用 1号同学代码，获取字典
        res_a = get_codes(a, bits)
        res_b = get_codes(b, bits)
        res_neg_b = get_codes(-b, bits) 

        # 2. 调用 2号同学代码，计算 A+B 与 A-B
        sum_result = add_binary(res_a['bu'], res_b['bu'], bits)
        diff_result = add_binary(res_a['bu'], res_neg_b['bu'], bits)

        # 3. 拼接展示
        lines = []
        sep = "═" * 60
        thin = "─" * 40

        lines.append(sep)
        lines.append(f"  补码加减法模拟器 (拼装版) | 字长：{bits} 位 | A = {a}, B = {b}")
        lines.append(sep)

        lines.append("\n【一、原反补码表示】\n")
        lines.append(f"  数字 A = {a}")
        lines.append(f"    原码 = {res_a['yuan']}")
        lines.append(f"    反码 = {res_a['fan']}")
        lines.append(f"    补码 = {res_a['bu']}")
        
        lines.append(f"\n  数字 B = {b}")
        lines.append(f"    原码 = {res_b['yuan']}")
        lines.append(f"    反码 = {res_b['fan']}")
        lines.append(f"    补码 = {res_b['bu']}")
        
        lines.append(f"\n  -B = {-b}")
        lines.append(f"    原码 = {res_neg_b['yuan']}")
        lines.append(f"    补码 = {res_neg_b['bu']}")

        lines.append(f"\n{thin}")
        lines.append(f"【二、加法运算：A + B】\n")
        lines.append(f"     A  补码 = {res_a['bu']}")
        lines.append(f"  +  B  补码 = {res_b['bu']}")
        lines.append(f"    {thin[4:]}")
        lines.append(f"     结果补码 = {sum_result['result']}")
        
        if sum_result['is_overflow']:
            lines.append(f"\n  ⚠ 判断：发生溢出！(结果符号错乱)")
            lines.append(f"  理论正确结果 = {a + b}")
        else:
            lines.append(f"\n  ✔ 无溢出")

        lines.append(f"\n{thin}")
        lines.append(f"【三、减法运算：A - B (即 A + (-B))】\n")
        lines.append(f"     A  补码 = {res_a['bu']}")
        lines.append(f"  + (-B)补码 = {res_neg_b['bu']}")
        lines.append(f"    {thin[4:]}")
        lines.append(f"     结果补码 = {diff_result['result']}")
        
        if diff_result['is_overflow']:
            lines.append(f"\n  ⚠ 判断：发生溢出！(结果符号错乱)")
            lines.append(f"  理论正确结果 = {a - b}")
        else:
            lines.append(f"\n  ✔ 无溢出")

        lines.append(f"\n{sep}")
        lines.append(f"  最终结果：A + B = {a + b} " + ("(溢出)" if sum_result['is_overflow'] else ""))
        lines.append(f"            A - B = {a - b} " + ("(溢出)" if diff_result['is_overflow'] else ""))
        lines.append(sep)

        self.text_output.insert("1.0", "\n".join(lines))


if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 1.2)
    except Exception:
        pass
    app = ComplementSimulator(root)
    root.mainloop()
