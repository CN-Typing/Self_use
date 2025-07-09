import tkinter as tk
import random
import time

class ColorReverseGame:
    def __init__(self, root):
        self.root = root
        self.root.title("颜色反话小游戏")
        self.root.geometry("500x300")
        self.root.configure(bg="#f0f0f0")
        
        # 确保中文正常显示
        self.font = ("SimHei", 48)
        
        # 定义颜色列表（名称和对应的实际颜色）
        self.colors = {
            "红色": "#FF0000",
            "绿色": "#00FF00",
            "蓝色": "#0000FF",
            "黄色": "#FFFF00",
            "紫色": "#800080",
            "橙色": "#FFA500",
            "黑色": "#FFFFFF",  # 黑色名称对应白色文字
            "白色": "#000000",  # 白色名称对应黑色文字
            "粉色": "#FFC0CB",
            "灰色": "#808080"
        }
        
        self.current_color_name = ""
        self.current_color_value = ""
        
        self.create_widgets()
        
    def create_widgets(self):
        # 创建标题标签
        title_label = tk.Label(
            self.root, 
            text="颜色反话小游戏", 
            font=("SimHei", 24), 
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=10)
        
        # 创建游戏说明
        instruction = tk.Label(
            self.root, 
            text="判断文字的颜色，而非文字内容！", 
            font=("SimHei", 12), 
            bg="#f0f0f0",
            fg="#666666"
        )
        instruction.pack(pady=5)
        
        # 创建颜色显示标签
        self.color_label = tk.Label(
            self.root, 
            text="点击开始", 
            font=self.font, 
            bg="#f0f0f0",
            fg="#333333"
        )
        self.color_label.pack(pady=30)
        
        # 创建开始/刷新按钮
        self.button = tk.Button(
            self.root, 
            text="开始/刷新", 
            font=("SimHei", 14), 
            bg="#4CAF50",
            fg="white",
            command=self.change_color
        )
        self.button.pack(pady=20)
        
        # 创建状态栏
        self.status = tk.Label(
            self.root, 
            text="准备就绪", 
            font=("SimHei", 10), 
            bg="#f0f0f0",
            fg="#666666"
        )
        self.status.pack(side=tk.BOTTOM, pady=10)
        
    def change_color(self):
        # 随机选择颜色名称和实际显示颜色
        color_names = list(self.colors.keys())
        color_values = list(self.colors.values())
        
        # 确保文字内容和文字颜色不同
        name_index = random.randint(0, len(color_names) - 1)
        value_index = random.randint(0, len(color_values) - 1)
        
        while color_values[value_index] == self.colors[color_names[name_index]]:
            value_index = random.randint(0, len(color_values) - 1)
        
        self.current_color_name = color_names[name_index]
        self.current_color_value = color_values[value_index]
        
        # 更新显示
        self.color_label.config(text=self.current_color_name, fg=self.current_color_value)
        
        # 更新状态
        self.status.config(text=f"现在显示的颜色名称是: {self.current_color_name}")

if __name__ == "__main__":
    root = tk.Tk()
    game = ColorReverseGame(root)
    root.mainloop()    