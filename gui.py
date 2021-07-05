from tkinter import *
from tkinter import ttk

class Application:
    def __init__(self, root: Tk):
        self.root = root
        root.title('Kickstarter JSON Converter')
        style = ttk.Style()
        style.theme_use('default')

        self.frame_main = Frame(root)
        self.frame_main.grid(sticky='news')

        # Labels
        self.select_col_label = Label(self.frame_main, text="Select columns:")
        self.selected_col_label = Label(self.frame_main, text="Selected columns:")
        self.select_col_label.grid(row=0, column=0, sticky=W, pady=2, padx=5)
        self.selected_col_label.grid(row=0, column=2, sticky=W, pady=2, padx=5)

        # Frames for columns
        self.available_col_frame = Frame(self.frame_main, bg="blue")
        self.available_col_frame.grid(row=1, column=0, rowspan=2)
        self.selected_col_frame = Frame(self.frame_main, bg="blue")
        self.selected_col_frame.grid(row=1, column=2, rowspan=2)

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

        # Fake data
        self.populate_with_fake_data()

        # Buttons
        self.add_col_button = Button(self.frame_main, text=">>", command=self.add_columns)
        self.remove_col_button = Button(self.frame_main, text="<<", command=self.remove_columns)
        self.add_col_button.grid(row=1, column=1, padx=5)
        self.remove_col_button.grid(row=2, column=1, padx=5)

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


if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()