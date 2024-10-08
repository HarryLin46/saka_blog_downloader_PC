import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QScrollArea, QLabel, QVBoxLayout, QWidget, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建 QStackedWidget 用于管理不同的页面
        self.stacked_widget = QStackedWidget()

        # 创建第一个页面及其内容
        page1 = QWidget()
        page1_layout = QVBoxLayout(page1)
        scroll_area1 = QScrollArea()
        label1 = QLabel("这是第一页的长文本..." * 100)
        label1.setWordWrap(True)
        scroll_area1.setWidget(label1)
        page1_layout.addWidget(scroll_area1)

        # 创建第二个页面及其内容
        page2 = QWidget()
        page2_layout = QVBoxLayout(page2)
        scroll_area2 = QScrollArea()
        label2 = QLabel("这是第二页的长文本..." * 100)
        label2.setWordWrap(True)
        scroll_area2.setWidget(label2)
        page2_layout.addWidget(scroll_area2)

        # 将页面添加到堆叠小部件
        self.stacked_widget.addWidget(page1)
        self.stacked_widget.addWidget(page2)

        # 设置堆叠小部件为主窗口的中心小部件
        self.setCentralWidget(self.stacked_widget)

        # 创建按钮用于页面切换
        self.btn_toggle = QPushButton("切换页面", self)
        self.btn_toggle.clicked.connect(self.toggle_pages)
        self.btn_toggle.move(10, 10)

    def toggle_pages(self):
        # 切换页面
        current_index = self.stacked_widget.currentIndex()
        new_index = 1 if current_index == 0 else 0
        self.stacked_widget.setCurrentIndex(new_index)

# 创建应用程序实例
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
