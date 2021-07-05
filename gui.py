from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from pathlib import Path
import pandas as pd

class Application:
    def __init__(self, root: Tk):
        self.root = root
        root.title('Kickstarter JSON Converter')
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
        self.selected_col_label = Label(self.frame_main, text="Selected columns:")
        self.select_col_label.grid(row=0, column=0, sticky=W, pady=2, padx=5)
        self.selected_col_label.grid(row=0, column=3, sticky=W, pady=2, padx=5)

        # Frames for columns
        self.available_col_frame = Frame(self.frame_main, bg="blue")
        self.available_col_frame.grid(row=1, column=0, columnspan=2, rowspan=2, sticky=(N, S, E, W))
        self.selected_col_frame = Frame(self.frame_main, bg="blue")
        self.selected_col_frame.grid(row=1, column=3, columnspan=2, rowspan=2, sticky=(N, S, E, W))

        # Scrollbars
        self.available_list_scrollbar = Scrollbar(self.available_col_frame, orient='vertical')
        self.selected_list_scrollbar = Scrollbar(self.selected_col_frame, orient='vertical')

        # Columns
        self.available_list = Listbox(self.available_col_frame, selectmode = "multiple", yscrollcommand=self.available_list_scrollbar.set)
        self.available_list_scrollbar.config(command=self.available_list.yview)
        self.available_list_scrollbar.pack(side='right', fill='y')
        self.available_list.pack(side='left', fill='both', expand=1)
        self.selected_list = Listbox(self.selected_col_frame, selectmode = "multiple", yscrollcommand=self.selected_list_scrollbar.set)
        self.selected_list_scrollbar.config(command=self.selected_list.yview)
        self.selected_list_scrollbar.pack(side="right", fill="y")
        self.selected_list.pack(side="left", fill="both", expand=1)

        # Buttons
        self.add_col_button = Button(self.frame_main, text=">>", command=self.add_columns)
        self.remove_col_button = Button(self.frame_main, text="<<", command=self.remove_columns)
        self.add_col_button.grid(row=1, column=2, padx=5)
        self.remove_col_button.grid(row=2, column=2, padx=5)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.frame_main.columnconfigure(0, weight=1)
        self.frame_main.columnconfigure(1, weight=1)
        self.frame_main.columnconfigure(2, weight=1)
        self.frame_main.columnconfigure(3, weight=1)
        self.frame_main.columnconfigure(4, weight=1)
        self.frame_main.rowconfigure(1, weight=1)
        self.frame_main.rowconfigure(2, weight=1)
        # self.frame_main.rowconfigure(3, weight=1)
        # self.frame_main.rowconfigure(4, weight=1)


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

    def populate_with_fake_data(self):
        # Fake data
        x =["C", "C++", "C#", "Java", "Python",
            "R", "Go", "Ruby", "JavaScript", "Swift",
            "SQL", "Perl", "XML"]
        
        for each_item in range(len(x)):    
            self.available_list.insert(END, x[each_item])
            self.available_list.itemconfig(each_item)

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
        self.populate_columns_with_data(list(df.columns))

    def populate_columns_with_data(self, list_of_columns):
        for each_item in range(len(list_of_columns)):    
            self.available_list.insert(END, list_of_columns[each_item])
            self.available_list.itemconfig(each_item)


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
            filetypes=filetypes)

        return filename


if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()