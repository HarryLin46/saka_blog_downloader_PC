import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("主界面")
        self.button = QPushButton("打开其他界面", self)
        self.button.clicked.connect(self.open_other_window)
        self.button.resize(200, 50)
        self.setGeometry(300, 300, 400, 300)  # 设置初始位置和大小
        self.other_window = OtherWindow(self)

    def open_other_window(self):
        self.other_window.setGeometry(self.geometry())  # 设置新窗口位置为当前窗口位置
        # self.hide()
        self.other_window.show()
        # self.hide()

class OtherWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("其他界面")
        self.button = QPushButton("返回主界面", self)
        self.button.clicked.connect(self.return_to_main)
        self.button.resize(200, 50)

    def return_to_main(self):
        self.parent().setGeometry(self.geometry())  # 设置主窗口位置为当前窗口位置
        self.parent().show()
        self.close()


# 创建应用程序实例
app = QApplication([])
main_window = MainWindow()
main_window.show()
app.exec()
