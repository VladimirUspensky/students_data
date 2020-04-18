from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
import os
import copy


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

        self.tree = ttk.Treeview(self.tab1, yscrollcommand=self.scroll_filesY.set,
                                 xscrollcommand=self.scroll_filesX.set)

        self.tree.configure(yscrollcommand=self.scroll_filesY.set, xscrollcommand=self.scroll_filesX.set)
        self.tree.place(relwidth=1, relheight=1)

        self.scroll_filesY.config(command=self.tree.yview)
        self.scroll_filesX.config(command=self.tree.xview)

        self.nodes = dict()
        self.buttons_frame = Frame(self.root, relief=RAISED)
        self.buttons_frame.place(relx=0.3, relwidth=0.2, relheight=0.25)

        self.all_files = {}
        self.keys_counter = 0
        self.open_from_list_btn = Button(self.buttons_frame, text='Open file', relief=RAISED,
                                         borderwidth=3, command=self.OpenFromTree)
        self.open_from_list_btn.place(relwidth=1, relheight=0.2)

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
        self.CreateDrawField()

    def OnScale(self, val):
        v = int(float(val))
        self.var.set(v)

    def CreateMenu(self):
        main_menu = Menu(self.root)
        self.root.config(menu=main_menu)
        file_menu = Menu(main_menu, tearoff=0)
        open_files_menu = Menu(file_menu, tearoff=0)
        main_menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_cascade(label='Add...', menu=open_files_menu)
        open_files_menu.add_command(label='Add Project', command=self.Add)


    def Run(self):
        self.root.mainloop()

    def Add(self):
        flag = False
        flag_to_avoid_repeat = False
        idx = 1
        file_list = []
        dir_path = fd.askdirectory()
        parent_name = dir_path.split('/')
        self.tree.insert('', 0, f'{parent_name[-1]}', text=parent_name[-1])
        for file in os.walk(dir_path):
            parent_name = file[0].split('/')[-1]
            for dir in file[1]:
                self.tree.insert(f'{parent_name}', idx, f'{parent_name}' + f'\{dir}', text=dir)
                idx += 1
                flag = True
                if not flag_to_avoid_repeat:
                    for fl in file[2]:
                        self.tree.insert(f'{parent_name}', idx, text=fl)
                        file_list.append(file[0] + '/' + fl)
                        idx += 1
                        flag_to_avoid_repeat = True
                    self.all_files[f'{parent_name}'] = copy.deepcopy(file_list)
                    file_list.clear()

            if not flag:
                for fl in file[2]:
                    self.tree.insert(f'{parent_name}', idx, text=fl)
                    file_list.append(file[0] + '/' + fl)
                    idx += 1
                flag = False
                self.all_files[f'{parent_name}'] = copy.deepcopy(file_list)
                file_list.clear()
            flag_to_avoid_repeat = False


    def OpenFromTree(self):
        self.txt_field.delete(0.0, END)
        selected_file = self.tree.focus()
        try:
            file_list = self.all_files[self.tree.parent(selected_file)]
        except KeyError:
            messagebox.showerror('Error', 'Import Project')
        else:
            file_index = self.tree.index(selected_file)
            print(file_index)
            file_path = file_list[file_index - 1]
            file_path = open(file_path)
            self.txt_field.insert(0.0, file_path.read())
            file_path.close()

    def CreateDrawField(self):
        canvas_first_type = Canvas(self.tab2, bg='grey', cursor='pencil')
        canvas_second_type = Canvas(self.tab2, bg='grey', cursor='pencil')
        canvas_first_type.place(relwidth=1, relheight=0.5)
        canvas_second_type.place(rely=0.5, relwidth=1, relheight=0.5)




if __name__ == '__main__':
    window = MainWindow(600, 400)
    window.Run()
