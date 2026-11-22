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
# 2 号同学的代码 (calc.py 拼装位置) - 由 3号 同学修改以适配动画
# ============================================================
def add_binary_with_steps(a_bin: str, b_bin: str, bits: int) -> dict:
    """
    执行补码加法，并返回每一步的明细（steps），用于 3号 同学的动画展示。
    """
    if len(a_bin) != bits or len(b_bin) != bits:
        raise ValueError(f"输入字符串长度必须等于 {bits}")
    
    result_bits = ['0'] * bits
    carry = 0
    steps = []

    # 从右往左（低位到高位）遍历
    for i in range(bits - 1, -1, -1):
        # 计算 bit_idx，0 表示最低位（最右边）
        bit_idx = bits - 1 - i
        
        a_bit = int(a_bin[i])
        b_bit = int(b_bin[i])
        total = a_bit + b_bit + carry
        result_bit = total % 2
        carry_out = total // 2
        
        # 记录当前步，完全符合 2号 林飞飞同学的数据格式
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


# ============================================================
# 3 号同学的代码 (ui.py 界面与拼装逻辑)
# ============================================================
class ComplementSimulator:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("补码加减法模拟器 - 3号同学可视化界面")
        self.root.geometry("950x750") # 稍微加大窗口以容纳左侧文本框和右侧动画画板
        self.root.resizable(False, False)

        # --- 3号同学增加的动画状态变量 ---
        self.steps = []
        self.current_step_idx = 0
        self.is_playing = False
        self.after_id = None
        self.ui_blocks = {'yuan': [], 'fan': [], 'bu': []}

        # ---------- 顶部输入区 ----------
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

        # ---------- 按钮区 (3号同学增加动画控制按钮) ----------
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        self.btn_calc = tk.Button(btn_frame, text="计算", width=10, height=2, font=("微软雅黑", 12, "bold"), bg="#4CAF50", fg="white", command=self.on_calculate)
        self.btn_calc.pack(side="left", padx=5)

        self.btn_reset = tk.Button(btn_frame, text="重置", width=10, height=2, font=("微软雅黑", 12, "bold"), bg="#f44336", fg="white", command=self.on_reset)
        self.btn_reset.pack(side="left", padx=5)

        # 3号新增的动画按钮，默认禁用，等计算后再启用
        self.btn_prev = tk.Button(btn_frame, text="上一步", width=10, height=2, font=("微软雅黑", 12), state="disabled", command=self.prev_step)
        self.btn_prev.pack(side="left", padx=5)

        self.btn_next = tk.Button(btn_frame, text="下一步", width=10, height=2, font=("微软雅黑", 12), state="disabled", command=self.next_step)
        self.btn_next.pack(side="left", padx=5)

        self.btn_auto = tk.Button(btn_frame, text="自动播放", width=10, height=2, font=("微软雅黑", 12), state="disabled", command=self.toggle_auto_play)
        self.btn_auto.pack(side="left", padx=5)

        # ---------- 结果输出区 (左右分栏设计) ----------
        mid_frame = tk.Frame(root)
        mid_frame.pack(padx=20, pady=5, fill="both", expand=True)

        # 左侧：文本输出区
        text_frame = tk.Frame(mid_frame)
        text_frame.pack(side="left", fill="both", expand=True)
        self.text_output = tk.Text(text_frame, font=("Consolas", 11), bg="#1e1e1e", fg="#dcdcdc", wrap="word", width=40)
        self.text_output.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(text_frame, command=self.text_output.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_output.config(yscrollcommand=scrollbar.set)

        # 右侧：3号同学增加的动画画板区
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

        # 3号调用 2号修改后的带步骤函数
        sum_result = add_binary_with_steps(res_a['bu'], res_b['bu'], bits)
        diff_result = add_binary_with_steps(res_a['bu'], res_neg_b['bu'], bits)

        lines = []
        lines.append(f"字长：{bits}位 | A = {a}, B = {b}\n")
        lines.append(f"A 补码：{res_a['bu']}")
        lines.append(f"B 补码：{res_b['bu']}\n")
        lines.append(f"A+B 结果：{sum_result['result']}")
        lines.append(f"溢出：{'是' if sum_result['is_overflow'] else '否'}")
        self.text_output.insert("1.0", "\n".join(lines))

        # ======== 3号核心：绘制动画格子 ========
        self.steps = sum_result['steps']
        self.current_step_idx = 0
        
        for widget in self.blocks_container.winfo_children():
            widget.destroy()
        self.ui_blocks = {'yuan': [], 'fan': [], 'bu': []}

        # 画出三行
        self.draw_row("A 补码:", res_a['bu'], "yuan")
        self.draw_row("B 补码:", res_b['bu'], "fan")
        self.draw_row("结  果:", sum_result['result'], "bu")

        self.btn_prev.config(state="normal")
        self.btn_next.config(state="normal")
        self.btn_auto.config(state="normal")
        
        self.update_step(0)

    def draw_row(self, title, binary_str, row_key):
        """3号同学的画格子函数"""
        frame = tk.Frame(self.blocks_container, bg="#f0f0f0")
        frame.pack(pady=5)
        tk.Label(frame, text=title, font=("微软雅黑", 12), bg="#f0f0f0", width=8, anchor="e").pack(side="left", padx=5)

        bits = len(binary_str)
        for i in range(bits):
            bit_val = binary_str[i]
            # 符号位（最高位，索引0）用灰色，数值位用蓝色（符合组长防坑提示）
            bg_color = "#D3D3D3" if i == 0 else "#87CEFA"
            
            lbl = tk.Label(frame, text=bit_val, font=("Consolas", 16, "bold"), width=3, height=1, bg=bg_color, relief="raised", borderwidth=2)
            lbl.pack(side="left", padx=3)
            
            # ui_idx: 0是最低位，所以用 bits-1-i
            ui_idx = bits - 1 - i
            self.ui_blocks[row_key].append({'ui_idx': ui_idx, 'label': lbl, 'default_bg': bg_color})

    def update_step(self, step_idx):
        """3号同学的高亮动画逻辑"""
        if not self.steps or step_idx < 0 or step_idx >= len(self.steps):
            return

        # 1. 恢复默认颜色
        for row_key in self.ui_blocks:
            for block in self.ui_blocks[row_key]:
                block['label'].config(bg=block['default_bg'])

        # 2. 获取当前步数据
        step_data = self.steps[step_idx]
        target_bit = step_data['bit_idx']

        # 3. 将匹配的位高亮为黄色
        for row_key in self.ui_blocks:
            for block in self.ui_blocks[row_key]:
                if block['ui_idx'] == target_bit:
                    block['label'].config(bg="yellow")

        # 4. 更新文字信息展示进位
        carry_in = step_data['carry_in']
        carry_out = step_data['carry_out']
        info_text = f"当前计算：第 {target_bit} 位 (bit_idx={target_bit})\n"
        info_text += f"进位输入：{carry_in} -> 进位输出：{carry_out}"
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
        """3号同学防卡死的自动播放逻辑"""
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
            # 使用 root.after 延迟 1000 毫秒，绝不使用 time.sleep
            self.after_id = self.root.after(1000, self.auto_play_loop) 
        else:
            self.is_playing = False
            self.btn_auto.config(text="自动播放")


if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 1.2)
    except Exception:
        pass
    app = ComplementSimulator(root)
    root.mainloop()