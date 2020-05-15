from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import sys
import subprocess


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.InitUI()
        self.MakeFrames()
        self.CreateMenu()

    def InitUI(self):
        self.setStyleSheet(open('style.css', 'r').read())
        self.setWindowTitle('title')
        self.setGeometry(500, 500, 500, 500)
        self.txt_field = QTextEdit()
        self.txt_field.setStyleSheet(open('style.css', 'r').read())
        self.file_tree = QTreeView()
        self.manage_tabs = QTabWidget()
        self.show_info_tabs = QTabWidget()
        self.img_label = QLabel()
        self.toolbar = QToolBar()
        self.scroll_info = QScrollArea()
        self.scroll_info.setWidget(self.show_info_tabs)
        self.scroll_info.setWidgetResizable(True)
        self.group_box = QGroupBox('MainWindow')
        self.setCentralWidget(self.group_box)
        self.show_info_tabs.addTab(self.txt_field, 'Text Tab')
        self.show_info_tabs.addTab(self.img_label, 'Image')
        self.manage_tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.manage_tabs.setAutoFillBackground(True)
        self.show_info_tabs.setStyleSheet(open('style.css', 'r').read())
#        self.txt_field.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
#        self.txt_field.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)


    def MakeFrames(self):
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.StyledPanel)
        form_lay = QVBoxLayout()

        form_lay.addWidget(self.manage_tabs)
        form_frame.setLayout(form_lay)
        ver_frame = QFrame()
        ver_frame.setFrameShape(QFrame.StyledPanel)

        ver_box = QVBoxLayout()
        ver_box.setContentsMargins(25, 20, 25, 25)
        ver_box.addWidget(self.scroll_info)
        ver_frame.setLayout(ver_box)

        bottom_frame = QFrame()
        bottom_frame.setFrameShape(QFrame.StyledPanel)
        bottom_frame.setMinimumWidth(150)
        bottom_lay = QFormLayout()
        bottom_frame.setLayout(bottom_lay)

        horizontal_splitter = QSplitter(QtCore.Qt.Horizontal)
        horizontal_splitter.addWidget(form_frame)
        horizontal_splitter.addWidget(ver_frame)

        vertical_splitter = QSplitter(QtCore.Qt.Vertical)
        vertical_splitter.addWidget(horizontal_splitter)
        vertical_splitter.addWidget(bottom_frame)

        vbox = QVBoxLayout()
        vbox.addWidget(vertical_splitter)
        bottom_frame.setStyleSheet(open('style.css', 'r').read())
        ver_frame.setStyleSheet(open('style.css', 'r').read())
        form_frame.setStyleSheet(open('style.css', 'r').read())
        self.group_box.setLayout(vbox)

    def CreateMenu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet(open('style.css', 'r').read())
        file_menu = menubar.addMenu('File')
        import_project = QAction('New', self)
        import_project.setShortcut('Ctrl+Q')

        menubar.setStyleSheet(open('style.css', 'r').read())
        import_project.triggered.connect(self.CreateFileTree)
        file_menu.addAction(import_project)

        show_bar_btn = QAction('Some command', self)
        show_bar_btn.setShortcut('Ctrl+W')
        file_menu.addAction(show_bar_btn)

        edit = menubar.addMenu('Edit')
        view = menubar.addMenu('View')
        navigate = menubar.addMenu('Navigate')

    def CreateFileTree(self):
        options = QFileDialog.DontResolveSymlinks
        dir_cur = QtCore.QDir.currentPath()
        selected_directory = QFileDialog.getExistingDirectory(None, 'Find Files', dir_cur, options)
        self.file_tree = QTreeView()
        self.file_model = QFileSystemModel()
        self.file_model.setReadOnly(False)
        self.file_model.setRootPath(selected_directory)
        self.file_tree.setModel(self.file_model)
        self.file_tree.setAnimated(True)
        self.file_tree.setRootIndex(self.file_model.index(selected_directory))
        self.manage_tabs.addTab(self.file_tree, 'Project')
        self.file_tree.clicked.connect(self.OpenFile)

    def OpenFile(self, index):
        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        image_path = file_path.split('/')[-1]

        if image_path.split('/')[-1] == 'exe':
            subprocess.call(file_path)
            return
        if image_path.split('.')[-1] != 'txt':
            self.img_label.setPixmap(QtGui.QPixmap(file_path))
            self.img_slider = QSlider(QtCore.Qt.Horizontal, self.img_label)
            self.setGeometry(60, 50, 100, 500)
            return
        file = open(file_path, 'r')
        info_from_file = file.read()
        self.txt_field.setText(info_from_file)
        file.close()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec_()





