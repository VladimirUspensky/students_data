from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
import os


class MainWindow:
    def __init__(self, width, height, title='title', resizable=(True, True)):
        self.root = Tk()
        self.root.geometry(f'{width}x{height}')
        self.root.title(title)
        self.root.resizable(resizable[0], resizable[1])

        self.file_dialog_frame = Frame(self.root, relief=RAISED, bg='grey')
        self.file_dialog_frame.place(relx=0, rely=0, relwidth=0.3, relheight=1)

        self.txt_frame = Frame(self.root, relief=RAISED)
        self.txt_frame.place(relx=0.3, rely=0.25, relwidth=0.7, relheight=0.5)

        self.scroll_txtY = Scrollbar(self.txt_frame)
        self.scroll_txtY.pack(side=RIGHT, fill=Y)

        self.txt_field = Text(self.txt_frame, yscrollcommand=self.scroll_txtY.set, wrap=WORD)
        self.txt_field.pack(expand=True, fill=BOTH)
        self.scroll_txtY.config(command=self.txt_field.yview)

        self.notebook = ttk.Notebook(self.file_dialog_frame)
        self.tab1 = Frame(self.notebook)
        self.tab2 = Frame(self.notebook)
        self.tab3 = Frame(self.notebook)

        self.notebook.add(self.tab1, text='First')
        self.notebook.add(self.tab2, text='Second')
        self.notebook.add(self.tab3, text='Third')

        self.notebook.place(relwidth=1, relheight=1)

        self.scroll_filesY = Scrollbar(self.notebook)
        self.scroll_filesY.pack(side=RIGHT, fill=Y)
        self.scroll_filesX = Scrollbar(self.notebook, orient=HORIZONTAL)
        self.scroll_filesX.pack(side=BOTTOM, fill=X)
        self.CreateMenu()

        self.tree = ttk.Treeview(self.tab1, column=('first', 'second'), yscrollcommand=self.scroll_filesY.set,
                                 xscrollcommand=self.scroll_filesX.set)


        self.tree.configure(yscrollcommand=self.scroll_filesY.set, xscrollcommand=self.scroll_filesX.set)
        self.tree.place(relwidth=1, relheight=1)


        self.scroll_filesY.config(command=self.tree.yview)
        self.scroll_filesX.config(command=self.tree.xview)

        self.nodes = dict()
        self.buttons_frame = Frame(self.root, relief=RAISED)
        self.buttons_frame.place(relx=0.3, relwidth=0.2, relheight=0.25)

        self.all_files = {}
        self.delete_from_tree_btn = Button(self.buttons_frame, text='Delete file', relief=RAISED,
                                        borderwidth=3, command=self.DeleteFileFromTree)
        self.delete_from_tree_btn.place(relwidth=0.5, relheight=0.2)
        self.open_from_list_btn = Button(self.buttons_frame, text='Open file', relief=RAISED,
                                        borderwidth=3, command=self.OpenFileFromTree)
        self.open_from_list_btn.place(relx=0.5, relwidth=0.5, relheight=0.2)

        self.combobox_frame = Frame(self.root, relief=RAISED)
        self.combobox_frame.place(relx=0.5, relwidth=0.2, relheight=0.25)

        self.combobox = ttk.Combobox(self.combobox_frame)
        self.combobox['values'] = ('first', 'second', 'third')
        self.combobox.pack(fill=X)
        self.combo_btn = Button(self.combobox_frame, text='btn')
        self.combo_btn.pack(fill=X)

        self.var = IntVar()
        self.lbl = Label(self.combobox_frame, textvariable=self.var)
        self.lbl.pack()
        self.scale = ttk.Scale(self.combobox_frame, from_=0, to=100, command=self.OnScale)
        self.scale.pack(fill=X)

    def OnScale(self, val):
        v = int(float(val))
        self.var.set(v)

    def DeleteFileFromTree(self):
        try:
            selected_file = self.tree.focus()
            parent = self.tree.parent(selected_file)
            parent_idx = self.tree.index(parent)
            file_index = self.tree.index(selected_file)
            file_list = self.all_files.get(parent_idx)
            file_list.pop(file_index)
            self.all_files[parent_idx] = file_list

            self.tree.delete(selected_file)
            print(self.all_files)
        except:
            messagebox.showerror('Error', 'Choose the file')

    def OpenFileFromTree(self):
        try:
            selected_file = self.tree.focus()
            file_index = self.tree.index(selected_file)
            parent = self.tree.parent(selected_file)
            parent_idx = self.tree.index(parent)
            file_list = self.all_files.get(parent_idx)
            print(file_list[file_index])
            opened_file = open(file_list[file_index], 'r')
            self.txt_field.delete(0.0, END)
            self.txt_field.insert(0.0, opened_file.read())
            opened_file.close()
        except AttributeError and TypeError:
            messagebox.showerror('Error', 'choose the file')

    def CreateMenu(self):
        main_menu = Menu(self.root)
        self.root.config(menu=main_menu)
        file_menu = Menu(main_menu, tearoff=0)
        open_files_menu = Menu(file_menu, tearoff=0)
        main_menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_cascade(label='Add...', menu=open_files_menu)

        open_files_menu.add_command(label='Add Folder', command=self.AddFolder)
      #  open_files_menu.add_command(label='Add file', command=self.AddFile)

    def AddFolder(self):
        dir_path = fd.askdirectory()
        file_tree = []
        for file in os.walk(dir_path):
            file_tree.append(file)
        name = dir_path.split('/')
        name.reverse()
        dir_id = self.tree.insert('', END, name[0], text=name[0])

        array = []
        for address, dirs, files in file_tree:
            for file in files:
                self.tree.insert(dir_id, END, text=file)
                array.append(address+'/'+file)
        index = self.tree.index(dir_id)
        self.all_files[index] = array


    def Run(self):
        self.root.mainloop()

    """
        def AddFile(self):
            file = []
            file_path = fd.askopenfilename()
            file_name = file_path.split('/')
            self.tree.insert('', END, text=file_name[len(file_name) - 1])
            file.append(file_path)
            self.all_files[len(self.all_files.keys())] = file
            print(self.all_files)
    """

if __name__ == '__main__':
    window = MainWindow(600, 400)
    window.Run()
