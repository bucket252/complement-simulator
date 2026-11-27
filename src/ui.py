import tkinter as tk
from tkinter import ttk

class ComplementAdderSim:
    def __init__(self, root):
        self.root = root
        self.root.title("补码加法运算模拟器")
        self.root.geometry("860x640")
        self.root.resizable(True, True)

        # ========== 暗黑终端配色 ==========
        self.bg_deep = "#050807"
        self.bg_sub = "#0A0F0D"
        self.card_bg = "#101A15"
        self.neon_green = "#00FF9C"
        self.term_green = "#39FF88"
        self.border_dark_green = "#123B2A"
        self.holo_cyan = "#00E5FF"
        self.text_main = "#E6FFF5"
        self.text_sub = "#C0D8CF"
        self.text_weak = "#5C6B63"
        self.warn = "#FFB000"
        self.err = "#FF3B3B"
        self.highlight_text = "#000000"

        self.root.configure(bg=self.bg_deep)

        self.step_idx = 0
        self.step_list = []
        self.A_comp = []
        self.B_comp = []
        self.S_comp = []
        self.carry_arr = []
        self.bit_length = 8
        self.highlight_bit = -1
        self.auto_timer_id = None

        font_title = ("Consolas", 14)
        font_body = ("Consolas", 11)
        font_btn = ("Consolas", 11)
        font_log = ("Consolas", 10)
        font_canvas = ("Consolas", 14)
        font_label = ("Consolas", 13)
        font_desc = ("微软雅黑", 10)

        # ========== 主容器 ==========
        outer_frame = tk.Frame(root, bg=self.bg_sub)
        outer_frame.pack(pady=18, padx=18, fill=tk.BOTH, expand=True)

        # ========== 顶部标题 ==========
        title_frame = tk.Frame(outer_frame, bg=self.bg_sub)
        title_frame.pack(pady=(0, 12))

        tk.Label(
            title_frame,
            text="COMPLEMENT ADDER SIMULATOR",
            font=("Consolas", 16, "bold"),
            bg=self.bg_sub,
            fg=self.neon_green
        ).pack()

        tk.Label(
            title_frame,
            text="补码加减法可视化终端",
            font=("微软雅黑", 10),
            bg=self.bg_sub,
            fg=self.text_weak
        ).pack()

        # ========== 输入控制区 ==========
        control_wrap = tk.Frame(
            outer_frame,
            bg=self.card_bg,
            highlightbackground=self.border_dark_green,
            highlightthickness=1
        )
        control_wrap.pack(pady=12, padx=10, fill=tk.X)

        row1_frame = tk.Frame(control_wrap, bg=self.card_bg)
        row1_frame.pack(pady=12, padx=12)

        tk.Label(row1_frame, text="数字A", font=font_body, bg=self.card_bg, fg=self.text_sub).grid(row=0, column=0, padx=8)
        self.var_a = tk.StringVar()
        tk.Entry(
            row1_frame,
            textvariable=self.var_a,
            width=10,
            font=font_body,
            relief=tk.FLAT,
            bg=self.bg_sub,
            fg=self.text_main,
            insertbackground=self.neon_green,
            highlightthickness=1,
            highlightbackground=self.border_dark_green
        ).grid(row=0, column=1, padx=8)

        tk.Label(row1_frame, text="数字B", font=font_body, bg=self.card_bg, fg=self.text_sub).grid(row=0, column=2, padx=8)
        self.var_b = tk.StringVar()
        tk.Entry(
            row1_frame,
            textvariable=self.var_b,
            width=10,
            font=font_body,
            relief=tk.FLAT,
            bg=self.bg_sub,
            fg=self.text_main,
            insertbackground=self.neon_green,
            highlightthickness=1,
            highlightbackground=self.border_dark_green
        ).grid(row=0, column=3, padx=8)

        tk.Label(row1_frame, text="字长", font=font_body, bg=self.card_bg, fg=self.text_sub).grid(row=0, column=4, padx=8)
        self.len_var = tk.StringVar(value="8")
        cb_len = ttk.Combobox(row1_frame, textvariable=self.len_var, values=["8", "16"], width=4, font=font_body)
        cb_len.grid(row=0, column=5, padx=8)

        # ========== 按钮区 ==========
        btn_frame = tk.Frame(control_wrap, bg=self.card_bg)
        btn_frame.pack(pady=(0, 12))

        btn_texts = ["计算", "重置", "上一步", "下一步", "自动播放"]
        btn_cmds = [self.calculate, self.reset, self.prev_step, self.next_step, self.auto_play]

        for i, (txt, cmd) in enumerate(zip(btn_texts, btn_cmds)):
            btn = tk.Button(
                btn_frame,
                text=txt,
                command=cmd,
                font=font_btn,
                bg=self.bg_sub,
                fg=self.neon_green,
                relief=tk.FLAT,
                padx=12,
                pady=6,
                highlightthickness=1,
                highlightbackground=self.border_dark_green
            )
            btn.grid(row=0, column=i, padx=6)

        # ========== 双面板区域 ==========
        bottom_frame = tk.Frame(outer_frame, bg=self.bg_sub)
        bottom_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        bottom_frame.columnconfigure(0, weight=0)
        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.rowconfigure(0, weight=1)

        # 日志面板
        log_wrap = tk.Frame(
            bottom_frame,
            bg=self.card_bg,
            highlightbackground=self.border_dark_green,
            highlightthickness=1
        )
        log_wrap.grid(row=0, column=0, padx=8, sticky="n")

        tk.Label(
            log_wrap,
            text="运算日志",
            font=font_title,
            bg=self.card_bg,
            fg=self.text_sub
        ).pack(pady=(10, 4))

        self.log_text = tk.Text(
            log_wrap,
            width=23,
            height=15,
            font=font_log,
            bg=self.bg_sub,
            fg=self.text_main,
            relief=tk.FLAT,
            padx=8,
            pady=8,
            highlightthickness=0
        )
        self.log_text.pack()

        # 位可视化面板
        vis_wrap = tk.Frame(
            bottom_frame,
            bg=self.card_bg,
            highlightbackground=self.border_dark_green,
            highlightthickness=1
        )
        vis_wrap.grid(row=0, column=1, padx=8, sticky="nsew")
        vis_wrap.rowconfigure(1, weight=1)
        vis_wrap.columnconfigure(0, weight=1)

        tk.Label(
            vis_wrap,
            text="位可视化",
            font=font_title,
            bg=self.card_bg,
            fg=self.text_sub
        ).pack(pady=(10, 4))

        self.canvas = tk.Canvas(
            vis_wrap,
            bg=self.bg_sub,
            relief=tk.FLAT,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 画布大小变化自动重绘
        self.canvas.bind("<Configure>", lambda e: self.draw_visual())

    def int2complement(self, num, n):
        if num >= 0:
            raw = bin(num)[2:].zfill(n)
        else:
            raw = bin((1 << n) + num)[2:]
        return [int(c) for c in raw]

    def calc_complement_add(self, a, b, n):
        A = self.int2complement(a, n)
        B = self.int2complement(b, n)
        carry = 0
        S = [0] * n
        carry_list = [0] * n
        step_info = []

        step_info.append(f"A = {a}，B = {b}，字长 {n} 位")
        step_info.append(f"A 补码：{''.join(map(str, A))}")
        step_info.append(f"B 补码：{''.join(map(str, B))}")
        step_info.append("")

        for i in range(n - 1, -1, -1):
            bitA = A[i]
            bitB = B[i]
            s = bitA + bitB + carry
            S[i] = s % 2
            new_carry = s // 2
            carry_list[i] = carry

            step_info.append(
                f"第{i}位：A={bitA} + B={bitB} + C={carry} = {s}，S={S[i]}，C_out={new_carry}"
            )

            carry = new_carry

        overflow = carry != carry_list[0]

        step_info.append("")
        step_info.append(f"结果补码：{''.join(map(str, S))}")

        if overflow:
            step_info.append("溢出：结果超出当前字长表示范围")
        else:
            res_val = int(''.join(map(str, S)), 2)
            if S[0] == 1:
                res_val = res_val - (1 << n)
            step_info.append(f"结果：{res_val}")

        return A, B, S, carry_list, step_info

    def draw_visual(self):
        self.canvas.delete("all")
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        if cw < 10 or ch < 10:
            return

        bit_count = self.bit_length
        label_width = 70
        padding = 10
        usable_w = cw - label_width - padding * 2
        box_w = usable_w / bit_count

        box_h = 36
        line_gap = 12
        start_y = 20

        y_A = start_y
        y_B = y_A + box_h + line_gap
        y_S = y_B + box_h + line_gap
        y_C = y_S + box_h + line_gap

        font_canvas = ("Consolas", 14)
        font_label = ("Consolas", 13)
        font_desc = ("微软雅黑", 10)

        # ========== CRT 扫描线 ==========
        for line_y in range(0, ch, 2):
            self.canvas.create_line(
                0, line_y, cw, line_y,
                fill="#181818", width=1, stipple="gray25"
            )

        # ========== 暗角边框 ==========
        for v in range(0, 10, 2):
            alpha = 255 - v * 12
            if alpha < 100:
                alpha = 100
            color = f"#{alpha:02X}{alpha:02X}{alpha:02X}"
            self.canvas.create_rectangle(v, v, cw - v, ch - v, outline=color, width=1)

        # 绘制一行比特
        def draw_row(y_base, label_text, sub_text, data):
            self.canvas.create_text(12, y_base + box_h / 2, text=label_text, font=font_label, fill=self.text_sub, anchor="w")
            self.canvas.create_text(32, y_base + box_h / 2, text=sub_text, font=font_desc, fill=self.text_sub, anchor="w")
            for idx, bit in enumerate(data):
                x1 = label_width + padding + idx * box_w
                y1 = y_base
                x2 = x1 + box_w
                y2 = y1 + box_h
                if idx == self.highlight_bit:
                    fill = self.neon_green
                    outline = self.term_green
                    text_color = self.highlight_text
                else:
                    fill = self.bg_sub
                    outline = self.border_dark_green
                    text_color = self.text_main
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline, width=1)
                self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=str(bit), font=font_canvas, fill=text_color)

        draw_row(y_A, "A", "加数", self.A_comp)
        draw_row(y_B, "B", "被加数", self.B_comp)
        draw_row(y_S, "S", "和", self.S_comp)
        draw_row(y_C, "C", "进位", self.carry_arr)

    def show_current_step(self):
        self.log_text.delete(1.0, tk.END)
        for i in range(self.step_idx + 1):
            if i < len(self.step_list):
                line = self.step_list[i]
                self.log_text.insert(tk.END, line + "\n")
        self.log_text.see(tk.END)

        txt = self.step_list[self.step_idx] if self.step_idx < len(self.step_list) else ""
        if "第" in txt and "位" in txt:
            try:
                pos = txt.find("第")
                num_str = txt[pos + 1:].split("位")[0]
                self.highlight_bit = int(num_str)
            except:
                self.highlight_bit = -1
        else:
            self.highlight_bit = -1
        self.draw_visual()

    def calculate(self):
        self.stop_auto()
        self.log_text.delete(1.0, tk.END)
        try:
            a = int(self.var_a.get())
            b = int(self.var_b.get())
        except:
            self.log_text.insert(tk.END, "请输入合法整数！\n")
            return
        self.bit_length = int(self.len_var.get())
        self.A_comp, self.B_comp, self.S_comp, self.carry_arr, self.step_list = self.calc_complement_add(a, b, self.bit_length)
        self.step_idx = 0
        self.highlight_bit = -1
        self.show_current_step()

    def prev_step(self):
        self.stop_auto()
        if self.step_idx > 0:
            self.step_idx -= 1
            self.show_current_step()

    def next_step(self):
        self.stop_auto()
        if self.step_idx < len(self.step_list) - 1:
            self.step_idx += 1
            self.show_current_step()

    def auto_play(self):
        self.stop_auto()
        def run():
            if self.step_idx < len(self.step_list) - 1:
                self.step_idx += 1
                self.show_current_step()
                self.auto_timer_id = self.root.after(900, run)
        run()

    def stop_auto(self):
        if self.auto_timer_id is not None:
            self.root.after_cancel(self.auto_timer_id)
            self.auto_timer_id = None

    def reset(self):
        self.stop_auto()
        self.log_text.delete(1.0, tk.END)
        self.step_idx = 0
        self.step_list = []
        self.A_comp = []
        self.B_comp = []
        self.S_comp = []
        self.carry_arr = []
        self.highlight_bit = -1
        self.var_a.set("")
        self.var_b.set("")
        self.draw_visual()

if __name__ == "__main__":
    root = tk.Tk()
    app = ComplementAdderSim(root)
    root.mainloop()