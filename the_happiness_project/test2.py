import tkinter as tk
from tkinter import ttk, messagebox, Misc
from ttkthemes import ThemedTk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the custom dataset
data_path = '/Users/jesshuang/Documents/GitHub/jess_window/project/the_happiness_project/World Happiness Report_new.csv'
custom_data = pd.read_csv(data_path).to_dict(orient='records')

class Window(ThemedTk):
    def __init__(self, theme:str='arc', **kwargs):
        super().__init__(theme=theme, **kwargs)
        self.title("World Happiness Report")
        try:
            self.__data = custom_data
        except Exception as error:
            messagebox.showwarning(title="Error", message=str(error))

        self._display_interface()

    @property
    def data(self) -> list[dict]:
        return self.__data

    def _display_interface(self):
        mainFrame = ttk.Frame(borderwidth=1, relief="groove")
        ttk.Label(mainFrame, text="World Happiness Report Data", font=('arial',16)).pack(pady=(20,10))

        tableFrame = ttk.Frame(mainFrame)
        columns = list(custom_data[0].keys())  # Extract columns from dataset
        tree = ttk.Treeview(tableFrame, columns=columns, show='headings')

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, anchor=tk.CENTER, width=100)

        tree.bind('<<TreeviewSelect>>', self.item_selected)

        # Add data to the treeview
        for record in self.data:
            tree.insert('', tk.END, values=list(record.values()))

        tree.grid(row=0, column=0, sticky='nsew')

        tableFrame.pack(ipadx=20, ipady=20)

        # Replace scrollbar with a dropdown menu
        self.selected_columns = tk.StringVar(value=columns)
        dropdown = ttk.Combobox(tableFrame, textvariable=self.selected_columns, values=columns, state="readonly")
        dropdown.grid(row=1, column=0, sticky='ew')
        dropdown.bind('<<ComboboxSelected>>', self.item_selected_dropdown)

        self.scatterPlotFrame = ScatterPlotFrame(mainFrame)
        self.scatterPlotFrame.pack()
        mainFrame.pack(padx=10, pady=10)

    def item_selected(self, event):
        tree = event.widget
        records = []
        for selected_item in tree.selection()[:3]:
            item = tree.item(selected_item)
            record = item['values']
            records.append(record)
        self.scatterPlotFrame.infos = records

    def item_selected_dropdown(self, event):
        selected_column = self.selected_columns.get()
        self.scatterPlotFrame.selected_column = selected_column

class ScatterPlotFrame(ttk.Frame):
    def __init__(self, master: Misc, **kwargs):
        super().__init__(master=master, **kwargs)
        self.configure({'borderwidth': 2, 'relief': 'groove'})
        style = ttk.Style()
        style.configure('abc.TFrame', background='#ffffff')
        self.configure(style='abc.TFrame')

    @property
    def infos(self) -> None:
        return None

    @infos.setter
    def infos(self, datas: list[list]) -> None:
        for w in self.winfo_children():
            w.destroy()

        if not hasattr(self, 'selected_column'):
            self.selected_column = 'Log GDP Per Capita'

        for data in datas:
            fig, ax = plt.subplots(figsize=(5, 4))
            x = range(len(data))
            y = data
            ax.scatter(x, y)

            ax.set_xticks(x)
            ax.set_xticklabels(custom_data[0].keys(), rotation=90)
            ax.set_title('Selected Data Points')
            ax.set_xlabel('Attributes')
            ax.set_ylabel('Values')

            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.draw()
            canvas.get_tk_widget().pack(side='left', expand=True, fill='both')

        self.plot_scatter()

    def plot_scatter(self):
        fig, ax = plt.subplots(figsize=(6, 6), dpi=120)
        data = pd.read_csv(data_path)
        sns.scatterplot(data=data, x=self.selected_column, y='Life Ladder', hue='Region', palette='pastel', ax=ax)
        ax.set_title(f'Life Ladder vs {self.selected_column}')
        ax.set_xlabel(self.selected_column)
        ax.set_ylabel('Life Ladder')
        ax.legend(loc='upper left', fontsize='8')
        
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side='left', expand=True, fill='both')

def main():
    def on_closing():
        window.destroy()

    window = Window(theme='breeze')
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

if __name__ == '__main__':
    main()