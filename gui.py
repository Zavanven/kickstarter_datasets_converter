from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter.messagebox import showinfo
from pathlib import Path
import pandas as pd

class Application:
    def __init__(self, root: Tk):
        self.root = root
        root.title('Kickstarter JSON Converter')
        # root.geometry('1000x400')
        style = ttk.Style()
        style.theme_use('default')

        self.frame_main = Frame(root)
        self.frame_main.grid(sticky='news')

        # Menu
        self.menubar = Menu(root)
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_json_file)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.root.config(menu=self.menubar)

        # Labels
        self.select_col_label = Label(self.frame_main, text="Select columns:")
        self.selected_col_label = Label(self.frame_main, text="Columns to export:")
        self.select_categories_label = Label(self.frame_main, text="Select categories:")
        self.selected_categories_label = Label(self.frame_main, text="Categories to export:")
        self.select_categories_label.grid(row=0, column=0, sticky=W, pady=2, padx=5)
        self.selected_categories_label.grid(row=0, column=3, sticky=W, pady=2, padx=5)
        self.select_col_label.grid(row=3, column=0, sticky=W, pady=2, padx=5)
        self.selected_col_label.grid(row=3, column=3, sticky=W, pady=2, padx=5)

        # Frames for columns
        self.categories_frame = Frame(self.frame_main)
        self.available_categories_frame = Frame(self.frame_main, bg="blue")
        self.available_categories_frame.grid(row=1, column=0, columnspan=2, rowspan=2, padx=5, sticky=(N, S, E, W))
        self.selected_categories_frame = Frame(self.frame_main, bg="blue")
        self.selected_categories_frame.grid(row=1, column=3, columnspan=2, rowspan=2, padx=5, sticky=(N, S, E, W))
        self.available_col_frame = Frame(self.frame_main, bg="blue")
        self.available_col_frame.grid(row=4, column=0, columnspan=2, rowspan=2, padx=5, sticky=(N, S, E, W))
        self.selected_col_frame = Frame(self.frame_main, bg="blue")
        self.selected_col_frame.grid(row=4, column=3, columnspan=2, rowspan=2, padx=5, sticky=(N, S, E, W))

        # Frames for buttons
        self.button_frame = Frame(self.frame_main)
        self.button_frame.grid(row=6, column=0, columnspan=5, sticky=(N, S, E, W))

        # Scrollbars
        self.available_list_scrollbar = Scrollbar(self.available_col_frame, orient='vertical')
        self.selected_list_scrollbar = Scrollbar(self.selected_col_frame, orient='vertical')
        self.available_categories_scrollbar = Scrollbar(self.available_categories_frame, orient='vertical')
        self.selected_categories_scrollbar = Scrollbar(self.selected_categories_frame, orient='vertical')


        # Lists
        self.available_list = Listbox(self.available_col_frame, selectmode = "multiple", yscrollcommand=self.available_list_scrollbar.set)
        self.available_list_scrollbar.config(command=self.available_list.yview)
        self.available_list_scrollbar.pack(side='right', fill='y')
        self.available_list.pack(side='left', fill='both', expand=1)
        self.selected_list = Listbox(self.selected_col_frame, selectmode = "multiple", yscrollcommand=self.selected_list_scrollbar.set)
        self.selected_list_scrollbar.config(command=self.selected_list.yview)
        self.selected_list_scrollbar.pack(side="right", fill="y")
        self.selected_list.pack(side="left", fill="both", expand=1)

        self.available_categories_list = Listbox(self.available_categories_frame, selectmode="multiple", yscrollcommand=self.available_categories_scrollbar)
        self.available_categories_scrollbar.config(command=self.available_categories_list.yview)
        self.available_categories_scrollbar.pack(side="right", fill="y")
        self.available_categories_list.pack(side='left', fill="both", expand=1)
        self.selected_categories_list = Listbox(self.selected_categories_frame, selectmode="multiple", yscrollcommand=self.selected_categories_scrollbar)
        self.selected_categories_scrollbar.config(command=self.selected_categories_list.yview)
        self.selected_categories_scrollbar.pack(side="right", fill="y")
        self.selected_categories_list.pack(side='left', fill="both", expand=1)

        # Buttons
        self.add_col_button = Button(self.frame_main, text=">>", command=self.add_columns)
        self.remove_col_button = Button(self.frame_main, text="<<", command=self.remove_columns)
        self.add_category_button = Button(self.frame_main, text=">>", command=self.add_categories)
        self.remove_category_button = Button(self.frame_main, text="<<", command=self.remove_categories)
        self.export_data = Button(self.button_frame, text="Export data", command=self.export_data)
        self.add_col_button.grid(row=4, column=2, padx=5, sticky=(N, S, E, W))
        self.remove_col_button.grid(row=5, column=2, padx=5, sticky=(N, S, E, W))
        self.add_category_button.grid(row=1, column=2, padx=5, sticky=(N, S, E, W))
        self.remove_category_button.grid(row=2, column=2, padx=5, sticky=(N, S, E, W))
        self.export_data.grid(row=0, column=0, padx=5, pady=5, sticky=(N, S, E, W))

        # Column and row configuration
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.frame_main.columnconfigure(0, weight=1)
        self.frame_main.columnconfigure(1, weight=1)
        self.frame_main.columnconfigure(2, weight=1)
        self.frame_main.columnconfigure(3, weight=1)
        self.frame_main.columnconfigure(4, weight=1)
        self.frame_main.rowconfigure(1, weight=2)
        self.frame_main.rowconfigure(2, weight=2)
        self.frame_main.rowconfigure(3, weight=0)
        self.frame_main.rowconfigure(4, weight=2)
        self.frame_main.rowconfigure(5, weight=2)
        self.frame_main.rowconfigure(6, weight=1)
        self.button_frame.columnconfigure(0, weight=2)
        self.button_frame.rowconfigure(0, weight=2)

        # Dataframe
        self.dataframe = None

    def add_categories(self):
        if len(self.available_categories_list.curselection()) == 0:
            return
        available_items = self.available_categories_list.get(0, END)
        selected_items = self.selected_categories_list.get(0, END)
        for each_item in self.available_categories_list.curselection():
            if available_items[each_item] not in selected_items:
                self.selected_categories_list.insert(END, available_items[each_item])
    
    def remove_categories(self):
        if len(self.selected_categories_list.curselection()) == 0:
            return
        tuple_to_remove = self.selected_categories_list.curselection()
        for id in reversed(tuple_to_remove):
            self.selected_categories_list.delete(id)

    def add_columns(self):
        """
        Transfer selected items from 'Select columns' to 'Selected columns' and ommit
        items that are already in 'Selected columns'
        """
        if len(self.available_list.curselection()) == 0:
            return
        available_items = self.available_list.get(0, END)
        selected_items = self.selected_list.get(0, END)
        for each_item in self.available_list.curselection():
            if available_items[each_item] not in selected_items:
                self.selected_list.insert(END, available_items[each_item])

    def remove_columns(self):
        """
        Simply remove selected items from 'Selected columns'
        """
        if len(self.selected_list.curselection()) == 0:
            return
        tuple_to_remove = self.selected_list.curselection()
        for id in reversed(tuple_to_remove):
            self.selected_list.delete(id)

    def open_json_file(self):
        """
        Open json file and pass it to pandas
        """
        file_path = self.select_file()
        try:
            df = pd.read_json(Path(file_path), lines=True)
        except TypeError:
            return
        df = pd.json_normalize(df['data'])
        categories = df['category.name'].drop_duplicates()
        categories = sorted(categories.to_list())
        self.populate_columns_with_data(self.available_list ,list(df.columns))
        self.populate_columns_with_data(self.available_categories_list, categories)
        self.dataframe = df

    def populate_columns_with_data(self, list: Listbox, list_of_columns):
        for each_item in range(len(list_of_columns)):    
            list.insert(END, list_of_columns[each_item])
            list.itemconfig(each_item)

    def select_file(self):
        """
        Show open file dialog and return path to selected file
        """
        filetypes = (
            ('Json files', '*.json'),
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='.',
            filetypes=filetypes
        )

        return filename

    def export_data(self):
        """
        Export dataframe to csv
        """
        if self.dataframe is None:
            messagebox.showerror(title="No json file open", message="You have to open json file first.")
            return
        if len(self.selected_list.get(0, END)) == 0:
            messagebox.showerror(title="No columns to export", message="You have to add columns which you want to export")
            return
        filename = self.save_file()
        df = self.dataframe
        df = df[list(self.selected_list.get(0, END))]
        df.to_csv(filename, index=True)

    def save_file(self):
        """
        Show save file dialog and return path
        """
        filetypes= (
            ('CSV files', '*.csv'),
        )

        filename = fd.asksaveasfile(
            title='Save a file',
            initialdir='.',
            filetypes=filetypes
        )

        return filename


if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()