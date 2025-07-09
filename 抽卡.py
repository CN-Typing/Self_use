import tkinter as tk
from tkinter import messagebox
import random

class PrizeDrawApp:
    def __init__(self, root):
        self.root = root
        self.root.title("幸运抽奖")
        self.root.geometry("400x320")  # 增加窗口高度
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # 设置中文字体
        self.font = ("SimHei", 12)
        
        # 奖项设置
        self.prizes = [5, 10, 20]
        self.weights = [50, 30, 20]  # 基础权重：5元50%，10元30%，20元20%
        
        # 保底机制设置
        self.small_pity_threshold = 5  # 小保底阈值（连续未中10/20元时触发）
        self.big_pity_threshold = 10   # 大保底阈值（累计抽奖次数触发）
        self.current_pity = 0          # 当前小保底计数
        self.total_draws = 0           # 总抽奖次数
        
        self.create_widgets()
    
    def create_widgets(self):
        # 标题
        title_label = tk.Label(
            self.root, 
            text="幸运抽奖", 
            font=("SimHei", 24, "bold"), 
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=15)
        
        # 抽奖结果显示
        self.result_var = tk.StringVar()
        self.result_var.set("点击抽奖按钮开始抽奖！")
        result_label = tk.Label(
            self.root, 
            textvariable=self.result_var, 
            font=self.font, 
            bg="#f0f0f0",
            fg="#333333"
        )
        result_label.pack(pady=10)
        
        # 保底机制说明
        pity_frame = tk.Frame(self.root, bg="#f0f0f0")
        pity_frame.pack(pady=5)
        
        tk.Label(
            pity_frame, 
            text="保底机制：", 
            font=self.font, 
            bg="#f0f0f0",
            fg="#333333"
        ).grid(row=0, column=0, padx=5, pady=5)
        
        tk.Label(
            pity_frame, 
            text=f"小保底：连续{self.small_pity_threshold}次未中大奖", 
            font=self.font, 
            bg="#f0f0f0",
            fg="#333333"
        ).grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        
        tk.Label(
            pity_frame, 
            text=f"大保底：累计{self.big_pity_threshold}次未中特等奖", 
            font=self.font, 
            bg="#f0f0f0",
            fg="#333333"
        ).grid(row=1, column=1, padx=5, pady=5, columnspan=2)
        
        # 保底进度条
        self.pity_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.pity_frame.pack(pady=10)
        
        # 小保底进度
        small_frame = tk.Frame(self.pity_frame, bg="#f0f0f0")
        small_frame.grid(row=0, column=0, sticky="ew", pady=2)
        
        tk.Label(
            small_frame, 
            text="小保底进度：", 
            font=self.font, 
            bg="#f0f0f0",
            fg="#333333"
        ).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        
        self.small_pity_text_var = tk.StringVar()
        self.small_pity_text_var.set(f"{self.current_pity}/{self.small_pity_threshold}")
        
        tk.Label(
            small_frame, 
            textvariable=self.small_pity_text_var, 
            font=self.font, 
            bg="#f0f0f0",
            fg="#333333"
        ).grid(row=0, column=2, padx=5, pady=2, sticky="e")
        
        self.small_pity_bar = tk.Canvas(
            small_frame, 
            width=200, 
            height=20, 
            bg="#e0e0e0", 
            highlightthickness=0
        )
        self.small_pity_bar.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        # 大保底进度
        big_frame = tk.Frame(self.pity_frame, bg="#f0f0f0")
        big_frame.grid(row=1, column=0, sticky="ew", pady=2)
        
        tk.Label(
            big_frame, 
            text="大保底进度：", 
            font=self.font, 
            bg="#f0f0f0",
            fg="#333333"
        ).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        
        self.big_pity_text_var = tk.StringVar()
        self.big_pity_text_var.set(f"{self.total_draws}/{self.big_pity_threshold}")
        
        tk.Label(
            big_frame, 
            textvariable=self.big_pity_text_var, 
            font=self.font, 
            bg="#f0f0f0",
            fg="#333333"
        ).grid(row=0, column=2, padx=5, pady=2, sticky="e")
        
        self.big_pity_bar = tk.Canvas(
            big_frame, 
            width=200, 
            height=20, 
            bg="#e0e0e0", 
            highlightthickness=0
        )
        self.big_pity_bar.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        # 设置列权重，使进度条可扩展
        small_frame.columnconfigure(1, weight=1)
        big_frame.columnconfigure(1, weight=1)
        
        # 抽奖按钮
        self.draw_button = tk.Button(
            self.root,
            text="开始抽奖",
            font=("SimHei", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            width=15,
            height=2,
            command=self.draw_prize
        )
        self.draw_button.pack(pady=15)
        
        # 统计信息
        self.count_5 = 0
        self.count_10 = 0
        self.count_20 = 0
        
        stats_frame = tk.Frame(self.root, bg="#f0f0f0")
        stats_frame.pack(pady=5)
        
        self.stats_var = tk.StringVar()
        self.stats_var.set("统计：5元(0) 10元(0) 20元(0)")
        stats_label = tk.Label(
            stats_frame, 
            textvariable=self.stats_var, 
            font=self.font, 
            bg="#f0f0f0",
            fg="#666666"
        )
        stats_label.pack()
    
    def draw_prize(self):
        # 禁用抽奖按钮，防止重复点击
        self.draw_button.config(state=tk.DISABLED)
        self.draw_button.config(text="抽奖中...")
        self.root.update()
        
        # 模拟抽奖过程
        self.animate_prize()
    
    def animate_prize(self):
        # 模拟抽奖动画
        for i in range(15):
            temp_prize = random.choice(self.prizes)
            self.result_var.set(f"抽奖中... {temp_prize}元")
            self.root.update()
            self.root.after(50)
        
        # 应用保底机制
        pity_triggered = False
        
        # 大保底判断（优先触发）
        if self.total_draws >= self.big_pity_threshold:
            prize = 20  # 必中20元
            pity_triggered = True
            self.total_draws = 0  # 重置大保底计数
            self.current_pity = 0  # 同时重置小保底计数
        # 小保底判断
        elif self.current_pity >= self.small_pity_threshold:
            # 提高10/20元概率
            pity_weights = [10, 45, 45]  # 5元10%，10元45%，20元45%
            prize = random.choices(self.prizes, weights=pity_weights, k=1)[0]
            pity_triggered = True
            # 只有当抽中10/20元时才重置小保底计数
            if prize != 5:
                self.current_pity = 0
        # 正常抽奖
        else:
            prize = random.choices(self.prizes, weights=self.weights, k=1)[0]
            # 更新保底计数
            if prize == 5:
                self.current_pity += 1
                self.total_draws += 1
            elif prize == 10:
                self.current_pity = 0
                self.total_draws += 1
            else:  # prize == 20
                self.current_pity = 0
                self.total_draws = 0
        
        # 显示抽奖结果
        result_text = f"恭喜您获得：{prize}元！"
        if pity_triggered:
            result_text += " (保底触发)"
        self.result_var.set(result_text)
        
        # 更新统计信息
        if prize == 5:
            self.count_5 += 1
        elif prize == 10:
            self.count_10 += 1
        else:
            self.count_20 += 1
        
        self.stats_var.set(f"统计：5元({self.count_5}) 10元({self.count_10}) 20元({self.count_20})")
        
        # 更新保底进度
        self.update_pity_bars()
        
        # 恢复抽奖按钮
        self.draw_button.config(state=tk.NORMAL)
        self.draw_button.config(text="再来一次")
    
    def update_pity_bars(self):
        # 更新小保底文本和进度条
        self.small_pity_text_var.set(f"{self.current_pity}/{self.small_pity_threshold}")
        
        small_percentage = self.current_pity / self.small_pity_threshold
        small_width = 200 * small_percentage
        
        self.small_pity_bar.delete("progress")
        if small_percentage > 0:
            self.small_pity_bar.create_rectangle(
                0, 0, small_width, 20, fill="#ff9800", tags="progress"
            )
        
        # 更新大保底文本和进度条
        self.big_pity_text_var.set(f"{self.total_draws}/{self.big_pity_threshold}")
        
        big_percentage = self.total_draws / self.big_pity_threshold
        big_width = 200 * big_percentage
        
        self.big_pity_bar.delete("progress")
        if big_percentage > 0:
            self.big_pity_bar.create_rectangle(
                0, 0, big_width, 20, fill="#f44336", tags="progress"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = PrizeDrawApp(root)
    root.mainloop()    