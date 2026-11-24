import tkinter as tk
from convert import get_codes
from calc import add_binary


class ComplementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("补码加减法可视化模拟器")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # 默认空白
        self.var_a = tk.StringVar(value="")
        self.var_b = tk.StringVar(value="")
        self.var_bits = tk.StringVar(value="8")

        self.bit_idx = 0
        self.max_bit = 8
        self.auto_timer_id = None
        self.carry_in = 0
        self.carry_out = 0
        self.a_bin = ""
        self.b_bin = ""
        self.res_bin = ""
        self.sum_result = None
        self.diff_result = None
        self.res_a = None
        self.res_b = None
        self.res_neg_b = None
        self.calc_mode = "add"

        # 顶部输入区域
        frame_top = tk.Frame(root, bg="#f0f0f0")
        frame_top.pack(pady=16, padx=16, fill="x")

        # 第一行：数字A、数字B（放大字体+输入框）
        tk.Label(frame_top, text="数字A：", bg="#f0f0f0", font=("SimHei", 18)).grid(row=0, column=0, padx=8, pady=8)
        tk.Entry(frame_top, textvariable=self.var_a, width=20, font=("SimHei", 18)).grid(row=0, column=1, padx=8, pady=8)

        tk.Label(frame_top, text="数字B：", bg="#f0f0f0", font=("SimHei", 18)).grid(row=0, column=2, padx=20, pady=8)
        tk.Entry(frame_top, textvariable=self.var_b, width=20, font=("SimHei", 18)).grid(row=0, column=3, padx=8, pady=8)

        # 第二行：字长
        tk.Label(frame_top, text="字长：", bg="#f0f0f0", font=("SimHei", 18)).grid(row=1, column=0, padx=8, pady=8)
        cb_bits = tk.OptionMenu(frame_top, self.var_bits, "8", "16")
        cb_bits.config(font=("SimHei", 18), width=6)
        cb_bits.grid(row=1, column=1, padx=8, pady=8)

        # 按钮区域，大幅放大
        frame_btn = tk.Frame(root, bg="#f0f0f0")
        frame_btn.pack(pady=12)
        btn_w = 16
        btn_h = 3
        btn_font = ("SimHei", 16)
        self.btn_calc = tk.Button(frame_btn, text="计算", bg="#39b54a", fg="white", command=self.calc, font=btn_font, width=btn_w, height=btn_h)
        self.btn_calc.grid(row=0, column=0, padx=10)
        self.btn_reset = tk.Button(frame_btn, text="重置", bg="#ed4337", fg="white", command=self.reset_all, font=btn_font, width=btn_w, height=btn_h)
        self.btn_reset.grid(row=0, column=1, padx=10)
        self.btn_prev = tk.Button(frame_btn, text="上一步", command=self.prev_bit, font=btn_font, width=btn_w, height=btn_h)
        self.btn_prev.grid(row=0, column=2, padx=10)
        self.btn_next = tk.Button(frame_btn, text="下一步", command=self.next_bit, font=btn_font, width=btn_w, height=btn_h)
        self.btn_next.grid(row=0, column=3, padx=10)
        self.btn_auto = tk.Button(frame_btn, text="自动播放", command=self.auto_play, font=btn_font, width=btn_w, height=btn_h)
        self.btn_auto.grid(row=0, column=4, padx=10)

        # 左右主容器
        frame_main = tk.Frame(root, bg="#f0f0f0")
        frame_main.pack(pady=12, padx=16, fill="both", expand=True)

        # 左侧运算日志
        frame_left = tk.Frame(frame_main)
        frame_left.pack(side="left", fill="both", expand=True)
        tk.Label(frame_left, text="运算日志：", bg="#f0f0f0", font=("SimHei", 14)).pack(anchor="w")
        self.text_output = tk.Text(frame_left, font=("SimHei", 12), bg="#000000", fg="#ffffff")
        self.text_output.pack(fill="both", expand=True)

        # 右侧位可视化画布
        frame_right = tk.Frame(frame_main)
        frame_right.pack(side="right", fill="both", expand=True, padx=(16,0))
        tk.Label(frame_right, text="位可视化", bg="#f0f0f0", font=("SimHei", 14)).pack(anchor="w")
        self.canvas = tk.Canvas(frame_right, bg="white")
        self.canvas.pack(fill="both", expand=True)

    def calc(self):
        self.stop_auto()
        self.text_output.delete("1.0", tk.END)
        try:
            a = int(self.var_a.get())
            b = int(self.var_b.get())
            bits = int(self.var_bits.get())
            self.max_bit = bits

            self.res_a = get_codes(a, bits)
            self.res_b = get_codes(b, bits)
            self.res_neg_b = get_codes(-b, bits)

            self.sum_result = add_binary(self.res_a["bu"], self.res_b["bu"], bits)
            self.diff_result = add_binary(self.res_a["bu"], self.res_neg_b["bu"], bits)

            lines = []
            lines.append(f"字长：{bits}位 | A = {a}, B = {b}")
            lines.append("")
            lines.append(f"A 补码：{self.res_a['bu']}")
            lines.append(f"B 补码：{self.res_b['bu']}")
            lines.append(f"A+B 结果：{self.sum_result['result']}")
            lines.append(f"溢出：{'是' if self.sum_result['is_overflow'] else '否'}")
            lines.append("")
            lines.append("-" * 50)
            lines.append(f"【一、A = {a}】")
            lines.append(f"原码：{self.res_a['yuan']}")
            lines.append(f"反码：{self.res_a['fan']}")
            lines.append(f"补码：{self.res_a['bu']}")
            lines.append("")
            lines.append(f"【二、B = {b}】")
            lines.append(f"原码：{self.res_b['yuan']}")
            lines.append(f"反码：{self.res_b['fan']}")
            lines.append(f"补码：{self.res_b['bu']}")
            lines.append("")
            lines.append(f"【三、加法运算：A + B】")
            lines.append(f"A 补码 = {self.res_a['bu']}")
            lines.append(f"B 补码 = {self.res_b['bu']}")
            lines.append("-" * 50)
            lines.append(f"结果补码 = {self.sum_result['result']}")
            if self.sum_result['is_overflow']:
                lines.append(f"⚠ 溢出：{self.sum_result['overflow_reason']}")
            else:
                lines.append("✅ 无溢出")
            lines.append("")
            lines.append(f"【减法运算：A - B (A + (-B))】")
            lines.append(f"A 补码 = {self.res_a['bu']}")
            lines.append(f"+(-B)补码 = {self.res_neg_b['bu']}")
            lines.append("-" * 50)
            lines.append(f"结果补码 = {self.diff_result['result']}")
            if self.diff_result['is_overflow']:
                lines.append(f"⚠ 溢出：{self.diff_result['overflow_reason']}")
            else:
                lines.append("✅ 无溢出")
            lines.append("")
            lines.append(f"最终：A+B = {a + b}")
            lines.append(f"A-B = {a - b}")

            self.text_output.insert("1.0", "\n".join(lines))

            self.calc_mode = "add"
            self.a_bin = self.res_a["bu"]
            self.b_bin = self.res_b["bu"]
            self.res_bin = self.sum_result["result"]
            self.bit_idx = 0

            # 初始化第一步进位，从steps读取
            if self.sum_result and "steps" in self.sum_result and len(self.sum_result["steps"]) > 0:
                first_step = self.sum_result["steps"][0]
                self.carry_in = first_step["carry_in"]
                self.carry_out = first_step["carry_out"]

            self.draw_bit_canvas()
        except Exception as e:
            self.text_output.insert("1.0", f"错误：{str(e)}")

    def draw_bit_canvas(self):
        self.canvas.delete(tk.ALL)
        if not self.a_bin:
            return
        cell_w = 52
        cell_h = 52
        start_x = 140
        start_y = 100
        # 行标签
        self.canvas.create_text(40, start_y + 26, text="A补码:", font=("SimHei",14), anchor="w")
        self.canvas.create_text(40, start_y + 78, text="B补码:", font=("SimHei",14), anchor="w")
        self.canvas.create_text(40, start_y + 130, text="结果:", font=("SimHei",14), anchor="w")

        # 换成更亮的蓝、亮黄
        bright_blue = "#00ccff"
        bright_yellow = "#ffdd00"

        for i in range(self.max_bit):
            pos = self.max_bit - 1 - i
            bit_a = self.a_bin[pos]
            bit_b = self.b_bin[pos]
            bit_r = self.res_bin[pos]
            x1 = start_x + i * cell_w
            y1 = start_y
            x2 = x1 + cell_w - 3
            y2 = y1 + cell_h
            is_active = (pos == self.bit_idx)
            fill_color = bright_yellow if is_active else bright_blue
            self.canvas.create_rectangle(x1,y1,x2,y2, fill=fill_color, outline="#222222")
            self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=bit_a, font=("SimHei",16))

            y1_b = start_y + 52
            y2_b = y1_b + cell_h
            self.canvas.create_rectangle(x1,y1_b,x2,y2_b, fill=fill_color, outline="#222222")
            self.canvas.create_text((x1+x2)/2, (y1_b+y2_b)/2, text=bit_b, font=("SimHei",16))

            y1_r = start_y + 104
            y2_r = y1_r + cell_h
            self.canvas.create_rectangle(x1,y1_r,x2,y2_r, fill=fill_color, outline="#222222")
            self.canvas.create_text((x1+x2)/2, (y1_r+y2_r)/2, text=bit_r, font=("SimHei",16))

        self.canvas.create_text(340, 32, text=f"当前计算: 第 {self.bit_idx} 位 (bit_idx={self.bit_idx})", font=("SimHei",14), fill="#dd2222")
        self.canvas.create_text(340, 56, text=f"进位输入: {self.carry_in} -> 进位输出: {self.carry_out}", font=("SimHei",14), fill="#dd2222")

    def next_bit(self):
        self.stop_auto()
        if self.sum_result is None or "steps" not in self.sum_result:
            return
        steps = self.sum_result["steps"]
        if self.bit_idx < len(steps) - 1:
            self.bit_idx += 1
            current_step = steps[self.bit_idx]
            self.carry_in = current_step["carry_in"]
            self.carry_out = current_step["carry_out"]
            self.draw_bit_canvas()

    def prev_bit(self):
        self.stop_auto()
        if self.sum_result is None or "steps" not in self.sum_result:
            return
        steps = self.sum_result["steps"]
        if self.bit_idx > 0:
            self.bit_idx -= 1
            current_step = steps[self.bit_idx]
            self.carry_in = current_step["carry_in"]
            self.carry_out = current_step["carry_out"]
            self.draw_bit_canvas()

    def auto_play(self):
        self.stop_auto()
        def run():
            if self.sum_result is None or "steps" not in self.sum_result:
                return
            steps = self.sum_result["steps"]
            if self.bit_idx < len(steps) -1:
                self.bit_idx +=1
                current_step = steps[self.bit_idx]
                self.carry_in = current_step["carry_in"]
                self.carry_out = current_step["carry_out"]
                self.draw_bit_canvas()
                self.auto_timer_id = self.root.after(600, run)
        run()

    def stop_auto(self):
        if self.auto_timer_id is not None:
            self.root.after_cancel(self.auto_timer_id)
            self.auto_timer_id = None

    def reset_all(self):
        self.stop_auto()
        self.bit_idx = 0
        self.carry_in = 0
        self.carry_out = 0
        self.a_bin = ""
        self.b_bin = ""
        self.res_bin = ""
        self.text_output.delete("1.0", tk.END)
        self.canvas.delete(tk.ALL)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 1.2)
    except Exception:
        pass
    app = ComplementSimulator(root)
    root.mainloop()