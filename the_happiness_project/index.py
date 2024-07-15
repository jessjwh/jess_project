import os
import pandas as pd
import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns



# 確認當前工作目錄
current_dir = os.getcwd()
# print(f"Current directory: {current_dir}")

# 列出目錄中的文件
files = os.listdir(current_dir)
# print(f"Files in current directory: {files}")

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
root.title("World Happiness Report")

# 創建上半部分的樹狀視圖小部件
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True)

tree = ttk.Treeview(tree_frame)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 添加垂直滾動條
v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=v_scrollbar.set)
v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 添加水平滾動條
h_scrollbar = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=tree.xview)
tree.configure(xscroll=h_scrollbar.set)
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# 定義列
tree["columns"] = list(data.columns)
tree["show"] = "headings"

# 設置列標題
for col in tree["columns"]:
    tree.heading(col, text=col)

# 添加數據到樹狀視圖
for index, row in data.iterrows():
    tree.insert("", "end", values=list(row))

# 創建下半部分的圖形顯示區域
plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True)

# 創建下拉式選單
selected_column = tk.StringVar()
column_menu = ttk.Combobox(plot_frame, textvariable=selected_column)

column_menu['values'] = ['Life Ladder', 'Log GDP Per Capita', 'Social Support', 'Healthy Life Expectancy At Birth',	'Freedom To Make Life Choices',	'Generosity','Perceptions Of Corruption',	'Positive Affect'	'Negative Affect'	'Confidence In National Government'
]

column_menu.set('Select a column')
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
        plt.figure(figsize=(6,6), dpi=120)
        sns.scatterplot(data=data, x=selected_col, y='Life Ladder', hue='Region', palette='pastel')
        plt.title(f'Life Ladder vs {selected_col}')
        plt.xlabel(selected_col)
        plt.ylabel('Life Ladder')
        plt.legend(loc='upper left', fontsize='8')
        plt.show()


# 綁定選擇事件
column_menu.bind("<<ComboboxSelected>>", update_plot)

# 運行 Tkinter 主循環
root.mainloop()