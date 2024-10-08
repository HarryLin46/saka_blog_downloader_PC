from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication,QFileDialog,QLabel,QScrollArea,QVBoxLayout,QStackedWidget,QWidget,QMainWindow,QPushButton
from PySide6.QtCore import Qt,QCoreApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QThread, Signal, Slot

from PIL import Image, ImageQt
from txt_to_html_nogi import resize_pictures_nogi #,txt_to_html_nogi,prepare_html
from txt_to_html_hina import resize_pictures_hina
from txt_to_html_saku import resize_pictures_saku

from member_window import nogi_member_window,hina_member_window,saku_member_window

import requests,bs4,os,json,time

from update_member import update_nogi,update_hinata,update_sakura

from nogi_crawler import nogi_crawling
from hina_crawler import hina_crawling
from saku_crawler import saku_crawling

class Worker(QThread):
    finished = Signal()

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)
        self.finished.emit()

class MainWindow:
    def __init__(self):
        loader = QUiLoader()
        self.ui = loader.load("main.ui")

        #create stack widget, which has 3 pages, for showing a blog 
        self.show_blog_stack = QStackedWidget(self.ui.centralwidget)
        self.show_blog_stack.setGeometry(320,10, 920, 550)
        self.page0 = QWidget()
        self.page1 = QWidget()
        self.page2 = QWidget()


        self.show_blog_stack.addWidget(self.page0)
        self.show_blog_stack.addWidget(self.page1)
        self.show_blog_stack.addWidget(self.page2)

        self.nogi_scroll = QScrollArea(self.page0)
        self.nogi_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.nogi_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.nogi_scroll.setGeometry(0,0, 920, 550)

        self.nogi_blog = QLabel()
        self.nogi_blog.setWordWrap(True)
        self.nogi_scroll.setWidget(self.nogi_blog)
        self.nogi_blog.setGeometry(0, 0, 896, 1000)
        self.nogi_scroll.setWidgetResizable(True)

        self.hina_scroll = QScrollArea(self.page1)
        self.hina_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.hina_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.hina_scroll.setGeometry(0,0, 920, 550)

        self.hina_blog = QLabel()
        self.hina_blog.setWordWrap(True)
        self.hina_scroll.setWidget(self.hina_blog)
        self.hina_blog.setGeometry(0, 0, 896, 1000)
        self.hina_scroll.setWidgetResizable(True)

        self.saku_scroll = QScrollArea(self.page2)
        self.saku_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.saku_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.saku_scroll.setGeometry(0,0, 920, 550)

        self.saku_blog = QLabel()
        self.saku_blog.setWordWrap(True)
        self.saku_scroll.setWidget(self.saku_blog)
        self.saku_blog.setGeometry(0, 0, 896, 1000)
        self.saku_scroll.setWidgetResizable(True)

        self.ui.nogi_btn.clicked.connect(self.set_nogi_blog)
        self.ui.hina_btn.clicked.connect(self.set_hina_blog)
        self.ui.saku_btn.clicked.connect(self.set_saku_blog)

        self.nogi_mem_window = nogi_member_window(self.ui)
        self.hina_mem_window = hina_member_window(self.ui)
        self.saku_mem_window = saku_member_window(self.ui)
        self.ui.mem_btn.clicked.connect(self.switch_mem_window)

        self.ui.update_mem_btn.clicked.connect(self.update_members)

        self.ui.crawling_btn.clicked.connect(self.run_crawling)

        self.ui.next_blog_btn.clicked.connect(self.next_blog)
        self.ui.back_blog_btn.clicked.connect(self.back_blog)

        nogi_mem_lists = []
        with open("member/nogi/member_list.txt",'r',encoding='utf-8') as file:
            for member in file:
                nogi_mem_lists.append(member.rstrip("\n")) #nogi_mem_lists = ['五百城 茉央', '池田 瑛紗', ...]
        self.ui.member_cbbox.addItems(nogi_mem_lists)
        # self.ui.member_cbbox.setCurrentIndex(1)

        self.ui.member_cbbox.currentIndexChanged.connect(self.show_blog)

        self.worker = None

        #hide loading/updating labels
        self.ui.loading_label_update_members.setVisible(False)
        self.ui.updating_label_crawling.setVisible(False)

    def update_cbbox(self):
        mem_lists = []
        current_idx = self.show_blog_stack.currentIndex()
        if current_idx==0: #it's nogi
            mem_list_path = "member/nogi/member_list.txt"
        elif current_idx==1: #it's hinata
            mem_list_path = "member/hinata/member_list.txt"
        elif current_idx==2: #it's sakura
            mem_list_path = "member/sakura/member_list.txt"

        with open(mem_list_path,'r',encoding='utf-8') as file:
            for member in file:
                mem_lists.append(member.rstrip("\n")) #nogi_mem_lists = ['五百城 茉央', '池田 瑛紗', ...]
        # print(mem_lists)
        self.ui.member_cbbox.clear()  # 清空現有項目
        self.ui.member_cbbox.addItems(mem_lists)

    def set_nogi_blog(self):
        self.show_blog_stack.setCurrentIndex(0)
        self.update_cbbox()
        self.show_blog()
    def set_hina_blog(self):
        self.show_blog_stack.setCurrentIndex(1)
        self.update_cbbox()
        self.show_blog()
    def set_saku_blog(self):
        self.show_blog_stack.setCurrentIndex(2)
        self.update_cbbox()
        self.show_blog()

    def switch_mem_window(self):
        # self.nogi_mem_window.setGeometry(self.ui.geometry()) #move 1st line of nogi_member_window class
        current_idx = self.show_blog_stack.currentIndex()
        if current_idx==0: #it's nogi
            self.nogi_mem_window.show()
        elif current_idx==1: #it's hinata
            self.hina_mem_window.show()
        elif current_idx==2: #it's sakura
            self.saku_mem_window.show()
        
    @Slot()
    def update_members(self):
        current_idx = self.show_blog_stack.currentIndex()
        self.ui.loading_label_update_members.setVisible(True)  # 顯示 "loading..." 字樣
        if current_idx==0: #it's nogi
            # update_nogi()
            self.start_worker(update_nogi,self.update_msg_update_members)

        elif current_idx==1: #it's hinata
            # update_hinata()
            self.start_worker(update_hinata,self.update_msg_update_members)

        elif current_idx==2: #it's sakura
            # update_sakura()
            self.start_worker(update_sakura,self.update_msg_update_members)

    def run_crawling(self):
        current_idx = self.show_blog_stack.currentIndex()
        self.ui.updating_label_crawling.setVisible(True)
        if current_idx==0: #it's nogi
            # nogi_crawling()
            self.start_worker(nogi_crawling,self.update_msg_crawling)
        elif current_idx==1: #it's hinata
            # hina_crawling()
            self.start_worker(hina_crawling,self.update_msg_crawling)
        elif current_idx==2: #it's sakura
            # saku_crawling()
            self.start_worker(saku_crawling,self.update_msg_crawling)

    def start_worker(self, func,update_msg):
        if self.worker and self.worker.isRunning():
            return  # 避免重複啟動線程

        self.worker = Worker(func)
        self.worker.finished.connect(update_msg)
        self.worker.start()

    @Slot()
    def update_msg_update_members(self):
        self.ui.loading_label_update_members.setVisible(False)  # 隱藏 "loading..." 字樣
        # print("更新完成")  # 可以在這裡更新UI，例如顯示提示信息

    @Slot()
    def update_msg_crawling(self):
        self.ui.updating_label_crawling.setVisible(False)  # 隱藏 "loading..." 字樣
        # print("更新完成")  # 可以在這裡更新UI，例如顯示提示信息

    def show_blog(self):
        global current_showing
        select_mem = self.ui.member_cbbox.currentText() #ex. 遠藤さくら

        current_idx = self.show_blog_stack.currentIndex() #0: nogi, 1: hinata, 2: sakura

        if current_idx==0: #it's nogi
            blogs_root = os.path.join("blog_source/Nogizaka46/",select_mem) #ex.blog_source/Nogizaka46/遠藤さくら
            try: #member may have no blog to show, or even haven't setup a file
                blogs = os.listdir(blogs_root)
                blog_html = os.path.join(blogs_root,blogs[0]+"/","blog_article.html") #choose the first/newest blog
                with open(blog_html, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                os.chdir(os.path.join(blogs_root,blogs[0]))
                current_showing = os.getcwd()
                html_content = resize_pictures_nogi(html_content)
                self.nogi_blog.setTextFormat(Qt.TextFormat.RichText)
                self.nogi_blog.setText(html_content)
                self.nogi_scroll.verticalScrollBar().setValue(0)
                os.chdir("../../../../")
            except:#indeed the member has no blog to show
                self.nogi_blog.setText("No Data!!")
        elif current_idx==1: #it's hinata
            blogs_root = os.path.join("blog_source/Hinatazaka46/",select_mem) #ex.blog_source/Nogizaka46/遠藤さくら
            try: #member may have no blog to show, or even haven't setup a file
                blogs = os.listdir(blogs_root)
                blog_html = os.path.join(blogs_root,blogs[0]+"/","blog_article.html") #choose the first/newest blog
                with open(blog_html, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                os.chdir(os.path.join(blogs_root,blogs[0]))
                current_showing = os.getcwd()
                html_content = resize_pictures_hina(html_content)
                self.hina_blog.setTextFormat(Qt.TextFormat.RichText)
                self.hina_blog.setText(html_content)
                self.hina_scroll.verticalScrollBar().setValue(0)
                os.chdir("../../../../")
            except:#indeed the member has no blog to show
                self.hina_blog.setText("No Data!!")
        elif current_idx==2: #it's sakura
            blogs_root = os.path.join("blog_source/Sakurazaka46/",select_mem) #ex.blog_source/Nogizaka46/遠藤さくら
            try: #member may have no blog to show, or even haven't setup a file
                blogs = os.listdir(blogs_root)
                blog_html = os.path.join(blogs_root,blogs[0]+"/","blog_article.html") #choose the first/newest blog
                with open(blog_html, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                os.chdir(os.path.join(blogs_root,blogs[0]))
                current_showing = os.getcwd()
                html_content = resize_pictures_saku(html_content)
                self.saku_blog.setTextFormat(Qt.TextFormat.RichText)
                self.saku_blog.setText(html_content)
                self.saku_scroll.verticalScrollBar().setValue(0)
                os.chdir("../../../../")
            except:#indeed the member has no blog to show
                self.saku_blog.setText("No Data!!")
        # print(blogs)

    def next_blog(self):
        global current_showing
        select_mem = self.ui.member_cbbox.currentText() #ex. 遠藤さくら

        current_idx = self.show_blog_stack.currentIndex() #0: nogi, 1: hinata, 2: sakura

        if current_idx==0: #it's nogi
            blogs_root = os.path.join("blog_source/Nogizaka46/",select_mem) #ex.blog_source/Nogizaka46/遠藤さくら
        elif current_idx==1: #it's hinata
            blogs_root = os.path.join("blog_source/Hinatazaka46/",select_mem) #ex.blog_source/Nogizaka46/遠藤さくら
        elif current_idx==2: #it's sakura
            blogs_root = os.path.join("blog_source/Sakurazaka46/",select_mem) #ex.blog_source/Nogizaka46/遠藤さくら

        blogs = os.listdir(blogs_root)
        blog_title = os.path.basename(current_showing)
        blog_index = blogs.index(blog_title)
        blog_html = os.path.join(blogs_root,blogs[blog_index+1]+"/","blog_article.html") #choose the first/newest blog
        with open(blog_html, 'r', encoding='utf-8') as file:
            html_content = file.read()
        os.chdir(os.path.join(blogs_root,blogs[blog_index+1]))
        current_showing = os.getcwd()
        html_content = resize_pictures(html_content)

        if current_idx==0: #it's nogi
            self.nogi_blog.setTextFormat(Qt.TextFormat.RichText)
            self.nogi_blog.setText(html_content)
            self.nogi_scroll.verticalScrollBar().setValue(0)
        elif current_idx==1: #it's hinata
            self.hina_blog.setTextFormat(Qt.TextFormat.RichText)
            self.hina_blog.setText(html_content)
            self.hina_scroll.verticalScrollBar().setValue(0)
        elif current_idx==2: #it's sakura
            self.saku_blog.setTextFormat(Qt.TextFormat.RichText)
            self.saku_blog.setText(html_content)
            self.saku_scroll.verticalScrollBar().setValue(0)
        os.chdir("../../../../")

        if blog_index+1 == len(blogs)-1: #next is the last one
            self.ui.next_blog_btn.setEnabled(False)
        if blog_index+1 > 0: #next is the last one
            self.ui.back_blog_btn.setEnabled(True)

    def back_blog(self):
        global current_showing
        select_mem = self.ui.member_cbbox.currentText() #ex. 遠藤さくら

        current_idx = self.show_blog_stack.currentIndex() #0: nogi, 1: hinata, 2: sakura

        if current_idx==0: #it's nogi
            blogs_root = os.path.join("blog_source/Nogizaka46/",select_mem) #ex.blog_source/Nogizaka46/遠藤さくら
        elif current_idx==1: #it's hinata
            blogs_root = os.path.join("blog_source/Hinatazaka46/",select_mem) #ex.blog_source/Nogizaka46/遠藤さくら
        elif current_idx==2: #it's sakura
            blogs_root = os.path.join("blog_source/Sakurazaka46/",select_mem) #ex.blog_source/Nogizaka46/遠藤さくら

        blogs = os.listdir(blogs_root)
        blog_title = os.path.basename(current_showing)
        blog_index = blogs.index(blog_title)
        blog_html = os.path.join(blogs_root,blogs[blog_index-1]+"/","blog_article.html") #choose the first/newest blog
        with open(blog_html, 'r', encoding='utf-8') as file:
            html_content = file.read()
        os.chdir(os.path.join(blogs_root,blogs[blog_index-1]))
        current_showing = os.getcwd()
        html_content = resize_pictures(html_content)

        if current_idx==0: #it's nogi
            self.nogi_blog.setTextFormat(Qt.TextFormat.RichText)
            self.nogi_blog.setText(html_content)
            self.nogi_scroll.verticalScrollBar().setValue(0)
        elif current_idx==1: #it's hinata
            self.hina_blog.setTextFormat(Qt.TextFormat.RichText)
            self.hina_blog.setText(html_content)
            self.hina_scroll.verticalScrollBar().setValue(0)
        elif current_idx==2: #it's sakura
            self.saku_blog.setTextFormat(Qt.TextFormat.RichText)
            self.saku_blog.setText(html_content)
            self.saku_scroll.verticalScrollBar().setValue(0)
        os.chdir("../../../../")

        if blog_index-1 == 0: #back is the newest one
            self.ui.back_blog_btn.setEnabled(False)
        if blog_index-1 < len(blogs)-1: #next is the last one
            self.ui.next_blog_btn.setEnabled(True)


        



if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    window = MainWindow()
    window.ui.show()
    app.exec()
