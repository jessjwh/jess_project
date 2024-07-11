import tkinter as tk
from tkinter import ttk, messagebox, Misc
from ttkthemes import ThemedTk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the custom dataset
data_path = '/Users/jesshuang/Documents/GitHub/jess_window/project/the_happiness_project/World Happiness Report_new.csv'
custom_data = pd.read_csv(data_path)

# List of columns to plot against Life Ladder
columns_to_plot = [
    'Log GDP Per Capita', 'Social Support', 'Healthy Life Expectancy At Birth',
    'Freedom To Make Life Choices', 'Generosity', 'Perceptions Of Corruption',
    'Positive Affect', 'Negative Affect', 'Confidence In National Government'
]

# Set the aesthetics for the plots
sns.set(style="whitegrid")

class Window(ThemedTk):
    def __init__(self, theme:str='arc', **kwargs):
        super().__init__(theme=theme, **kwargs)
        self.title("World Happiness Report")
        try:
            self.__data = custom_data.to_dict(orient='records')
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
        columns = list(custom_data.columns)
        tree = ttk.Treeview(tableFrame, columns=columns, show='headings')

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, anchor=tk.CENTER, width=100)

        tree.bind('<<TreeviewSelect>>', self.item_selected)

        # Add data to the treeview
        for record in self.data:
            tree.insert('', tk.END, values=list(record.values()))

        tree.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        tableFrame.pack(ipadx=20, ipady=20)

        self.scatterPlotFrame = ScatterPlotFrame(mainFrame)
        self.scatterPlotFrame.pack()
        mainFrame.pack(padx=10, pady=10)

    def item_selected(self, event):
        tree = event.widget
        selected_items = tree.selection()
        if selected_items:
            item = tree.item(selected_items[0])
            record = dict(zip(custom_data.columns, item['values']))
            self.scatterPlotFrame.infos = record

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
    def infos(self, data: dict) -> None:
        for w in self.winfo_children():
            w.destroy()

        df = custom_data

        for column in columns_to_plot:
            figure = plt.figure(figsize=(6, 6), dpi=120)
            sns.scatterplot(data=df, x='Life Ladder', y=column, hue='Region', palette='pastel')
            plt.axvline(data['Life Ladder'], color='r', linestyle='--')
            plt.title(f'{column} vs Life Ladder')
            plt.xlabel('Life Ladder')
            plt.ylabel(column)
            plt.legend(loc='upper left', fontsize='8')

            canvas = FigureCanvasTkAgg(figure, self)
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