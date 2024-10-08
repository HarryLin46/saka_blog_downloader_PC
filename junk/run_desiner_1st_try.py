from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication,QFileDialog,QLabel,QScrollArea,QVBoxLayout,QStackedWidget,QWidget
from PySide6.QtCore import Qt,QCoreApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PIL import Image, ImageQt
from txt_to_html import txt_to_html

class MainWindow:
    def __init__(self):
        loader = QUiLoader()
        self.ui = loader.load("designer_1st_try.ui")

        self.ui.pushButton.clicked.connect(self.say_hello)

        self._image: "Image" = None
        self.ui.pushButton_2.clicked.connect(self.load)

        self.ui.show_blog_btn.clicked.connect(self.show_blog)

        self.show_blog_stack = QStackedWidget(self.ui.centralwidget)
        self.show_blog_stack.setGeometry(320,10, 920, 550)
        # self.ui.centralwidget.addWidget(self.show_blog_stack)
        self.page0 = QWidget()
        # self.page0_layout = QVBoxLayout(self.page0)
        self.page1 = QWidget()
        # self.page1_layout = QVBoxLayout(self.page1)

        self.show_blog_stack.addWidget(self.page0)
        self.show_blog_stack.addWidget(self.page1)

        self.nogi_scroll = QScrollArea(self.page0)
        self.nogi_scroll.setGeometry(0,0, 920, 550)

        self.nogi_blog = QLabel()
        self.nogi_scroll.setWidget(self.nogi_blog)
        self.nogi_blog.setGeometry(0, 0, 896, 1000)
        self.nogi_scroll.setWidgetResizable(True)

        self.hina_scroll = QScrollArea(self.page1)
        self.hina_scroll.setGeometry(0,0, 920, 550)

        self.hina_blog = QLabel()
        self.hina_scroll.setWidget(self.hina_blog)
        self.hina_blog.setGeometry(0, 0, 896, 1000)
        self.hina_scroll.setWidgetResizable(True)

        self.ui.stack_btn.clicked.connect(self.switch_satck_page)

        self.ui.nogi_btn.clicked.connect(self.set_nogi_blog)
        self.ui.hina_btn.clicked.connect(self.set_hina_blog)




    def say_hello(self):
        self.ui.label.setText("putton pressed!!")

    def load(self):
        file_name, file_type = QFileDialog.getOpenFileName(
            self.ui,
            "Select Image",
            "./",
            "Image (*.png *.bmp *.jpg *.jpeg);;All Files(*)"
        )

        if file_name:
            self._image = Image.open(file_name)

        self.show_image()
    def show_image(self):
        if self._image:
            # #specify the ideal size of the picture
            max_size = (896, 896*10) #height don't care

            # # 调整图像大小，保持宽高比
            self._image.thumbnail(max_size, Image.Resampling.LANCZOS)
            qt_img = ImageQt.ImageQt(self._image)
            q_pixmap = QPixmap.fromImage(qt_img)
            # self.ui.show_pic.setPixmap(q_pixmap.scaled(896, 896*10, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.ui.label_2.setPixmap(q_pixmap)
            self.ui.label_2.adjustSize()

    def show_blog(self):
        current_idx = self.show_blog_stack.currentIndex() #0: nogi, 1: hinata
        if current_idx==0: #it's nogi
            html_content = txt_to_html("blog_source/raw_blog.txt")
            self.nogi_blog.setTextFormat(Qt.TextFormat.RichText)
            self.nogi_blog.setText(html_content)
        elif current_idx==1:
            html_content = txt_to_html("blog_source/raw_blog_h.txt")
            self.hina_blog.setTextFormat(Qt.TextFormat.RichText)
            self.hina_blog.setText(html_content)
        # print(html_content)
        
        # self.ui.show_pic.setTextFormat(Qt.TextFormat.RichText)
        # self.ui.show_pic.setText(html_content)

        # scroll = QScrollArea(self.ui.centralwidget)
        # scroll.setGeometry(300, 10, 920, 550)
        # scroll.setGeometry(300, 10, 896, 1000)

        # self.blog.setText("hhh")
        # scroll.setWidget(blog)
        # scroll.setWidgetResizable(True)


    def scroll(self):
        imageLabel = QLabel()
        image = Image.open("saku_nagi.jpg")
        qt_img = ImageQt.ImageQt(image)
        imageLabel.setPixmap(QPixmap.fromImage(qt_img))

        scrollArea = QScrollArea()
        scrollArea.setWidget(imageLabel)
        scrollArea.show()

    def switch_satck_page(self):
        p = self.show_blog_stack.currentIndex()
        # print(type(p),p)
        if p==0:
            # self.ui.page1_lb.setText("This is Page1")
            # self.ui.page1_lb.adjustSize()
            self.show_blog_stack.setCurrentIndex(1)
        elif p==1:
            # self.ui.page2_lb.setText("This is Page2")
            # self.ui.page2_lb.adjustSize()
            self.show_blog_stack.setCurrentIndex(0)

    def set_nogi_blog(self):
        self.show_blog_stack.setCurrentIndex(0)
        self.show_blog()
    def set_hina_blog(self):
        self.show_blog_stack.setCurrentIndex(1)
        self.show_blog()


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    window = MainWindow()
    window.ui.show()
    app.exec()
