import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns

# 確認當前工作目錄
current_dir = os.getcwd()
# 列出目錄中的文件
files = os.listdir(current_dir)

# 指定正確的文件路徑
file_path = '/Users/jesshuang/Documents/GitHub/jess_project/the_happiness_project/World Happiness Report_new.csv'

# 檢查文件是否存在
if os.path.exists(file_path):
    # 讀取 CSV 文件
    data = pd.read_csv(file_path)
    # 顯示數據框的前幾行
    print(data.head())
else:
    print(f"File not found: {file_path}")

# 創建 Tkinter 主窗口
root = tk.Tk()
root.title("What makes you happy?")

# 創建下半部分的圖形顯示區域
plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True)

# 創建下拉式選單
selected_column = tk.StringVar()
column_menu = ttk.Combobox(plot_frame, textvariable=selected_column)

column_menu['values'] = ['Life Ladder', 'Log GDP Per Capita', 'Social Support', 'Healthy Life Expectancy At Birth',	'Freedom To Make Life Choices',	'Generosity','Perceptions Of Corruption',	'Positive Affect', 'Negative Affect', 'Confidence In National Government']

column_menu.set('Select a factor')
column_menu.pack()

# 創建一個畫布以顯示圖形
fig = Figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

sns.set(style="whitegrid")

# 更新圖形
def update_plot(event):
    selected_col = selected_column.get()
    if selected_col in data.columns:
        ax.clear()  # 清除以前的圖形
        sns.scatterplot(data=data, x=selected_col, y='Life Ladder', hue='Region', palette='pastel', ax=ax)
        ax.set_title(f'Life Ladder vs {selected_col}')
        ax.set_xlabel(selected_col)
        ax.set_ylabel('Life Ladder')
        ax.legend(loc='upper left', fontsize='8')
        canvas.draw()  # 更新畫布

# 綁定選擇事件
column_menu.bind("<<ComboboxSelected>>", update_plot)

# 運行 Tkinter 主循環
root.mainloop()