from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication,QFileDialog,QLabel,QScrollArea,QVBoxLayout,QStackedWidget,QWidget,QMainWindow,QPushButton
from PySide6.QtCore import Qt,QCoreApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PIL import Image, ImageQt

class nogi_member_window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(self.parent().geometry())
        self.setWindowTitle("member_select")
        self.entered_btn = QPushButton("確定", self)
        self.entered_btn.setCursor(Qt.PointingHandCursor)
        self.entered_btn.setGeometry(1100, 565,75,24)
        # self.entered_btn.adjustSize()

        self.entered_btn.clicked.connect(self.return_to_main)

        self.member_widget = QWidget(self)
        self.member_widget.setGeometry(80, 10, 1020, 580)
        self.setStyleSheet("QWidget { border: 2px solid black; }")

        #cal member's width and height: 290*350 pixel for picture
        #width: (1020-10-10-9*5)/10 = 96
        #height: (470-10-10-8*3)/3 = 142 (116+26)

        #run for loop, create member buttons
        # self.member_btns = {}
        # self.member_lbls = {}
        posi_x = 10
        posi_y = 10
        with open("member/nogi/concerned_member.txt", "r", encoding="utf-8") as file:
            concerned_members = file.read()
        with open("member/nogi/member_list.txt", 'r', encoding='utf-8') as file:
            for line in file:
                name = line.strip() #ex.遠藤 さくら
                btn_name = name + "btn"
                lbl_name = name + "lbl"
                self.btn_name = QPushButton(self.member_widget)
                self.btn_name.setObjectName(btn_name)
                self.btn_name.setGeometry(posi_x,posi_y,96,116)
                self.btn_name.setCursor(Qt.PointingHandCursor)
                self.lbl_name = QLabel(name,self.member_widget)
                self.lbl_name.setObjectName(lbl_name)
                self.lbl_name.adjustSize()
                self.lbl_name.setGeometry(posi_x,posi_y+116+5,96,21) #space 5 between picture and txt

                # set member picture as the button pattern
                self.btn_name.setStyleSheet(f"QPushButton {{ border-image: url('member/nogi/{name}.jpg') 0; }}")

                # initially, it's red-black relative to concerned member
                if name in concerned_members:
                    self.lbl_name.setStyleSheet("QLabel { color: red; }")
                else:
                    self.lbl_name.setStyleSheet("QLabel { color: black; }")

                # click event
                self.btn_name.clicked.connect(self.change_label_color)

                # self.member_btns[btn_name] = self.btn_name
                # self.member_lbls[lbl_name] = self.lbl_name

                posi_x += 96+5
                if posi_x>1000:
                    posi_x = 10 #next row
                    posi_y += 142

    def change_label_color(self):
        button = self.sender() #is a btn object
        name = button.objectName().rstrip("btn")#ex. 遠藤 さくらbtn
        lbl_name = name+"lbl"
        self.lbl_name = self.member_widget.findChild(QLabel, lbl_name)
        current_style = self.lbl_name.styleSheet()
        # print(current_style)

        #depend on current color, switch to another one
        if "color: red;" in current_style:
            # self.lbl_name.setStyleSheet("QLabel { color: black; }")
            self.lbl_name.setStyleSheet( "color: black;")
        else:
            # self.member_widget.setStyleSheet(f"QLabel#遠藤 さくらlbl {{ color: red; }}")
            self.lbl_name.setStyleSheet( "color: red;")

    def save_concerned_member(self):
        with open('member/nogi/concerned_member.txt', 'w', encoding='utf-8') as file:
            for child in self.member_widget.findChildren(QLabel):
                lbl_name = child.objectName() #ex.遠藤 さくらlbl
                self.lbl_name = self.member_widget.findChild(QLabel, lbl_name)
                current_style = self.lbl_name.styleSheet()
                if "color: red;" in current_style:
                    file.write(child.objectName().rstrip("lbl")+"\n")
    def return_to_main(self):
        self.save_concerned_member()
        self.parent().setGeometry(self.geometry())  
        self.parent().show()
        self.close()


class hina_member_window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(self.parent().geometry())
        self.setWindowTitle("member_select")
        self.entered_btn = QPushButton("確定", self)
        self.entered_btn.setCursor(Qt.PointingHandCursor)
        self.entered_btn.setGeometry(1100, 500,75,24)
        # self.entered_btn.adjustSize()

        self.entered_btn.clicked.connect(self.return_to_main)

        self.member_widget = QWidget(self)
        self.member_widget.setGeometry(80, 20, 1020, 550)
        self.setStyleSheet("QWidget { border: 2px solid black; }")

        #cal member's width and height: 232*320 pixel for picture
        #width: (1020-10-10-9*5)/10 = 96
        #height: (470-10-10-8*3)/3 = 142 (132+10) -> too big!, height isn't enough 

        #v2:
        #width = 88
        #height = 142(120+21)

        #run for loop, create member buttons
        # self.member_btns = {}
        # self.member_lbls = {}
        posi_x = 10
        posi_y = 10
        with open("member/hinata/concerned_member.txt", "r", encoding="utf-8") as file:
            concerned_members = file.read()
        with open("member/hinata/member_list.txt", 'r', encoding='utf-8') as file:
            for line in file:
                name = line.strip() #ex.遠藤 さくら
                btn_name = name + "btn"
                lbl_name = name + "lbl"
                self.btn_name = QPushButton(self.member_widget)
                self.btn_name.setObjectName(btn_name)
                self.btn_name.setGeometry(posi_x,posi_y,88,120)
                self.btn_name.setCursor(Qt.PointingHandCursor)
                self.lbl_name = QLabel(name,self.member_widget)
                self.lbl_name.setObjectName(lbl_name)
                self.lbl_name.adjustSize()
                self.lbl_name.setGeometry(posi_x,posi_y+120+5,88,21) #space 5 between picture and txt

                # set member picture as the button pattern
                self.btn_name.setStyleSheet(f"QPushButton {{ border-image: url('member/hinata/{name}.jpg') 0; }}")

                # initially, it's red-black relative to concerned member
                if name in concerned_members:
                    self.lbl_name.setStyleSheet("QLabel { color: red; }")
                else:
                    self.lbl_name.setStyleSheet("QLabel { color: black; }")

                # click event
                self.btn_name.clicked.connect(self.change_label_color)

                # self.member_btns[btn_name] = self.btn_name
                # self.member_lbls[lbl_name] = self.lbl_name

                posi_x += 88+5
                if posi_x>1000:
                    posi_x = 10 #next row
                    posi_y += 142+10

    def change_label_color(self):
        button = self.sender() #is a btn object
        name = button.objectName().rstrip("btn")#ex. 遠藤 さくらbtn
        lbl_name = name+"lbl"
        self.lbl_name = self.member_widget.findChild(QLabel, lbl_name)
        current_style = self.lbl_name.styleSheet()
        # print(current_style)

        #depend on current color, switch to another one
        if "color: red;" in current_style:
            # self.lbl_name.setStyleSheet("QLabel { color: black; }")
            self.lbl_name.setStyleSheet( "color: black;")
        else:
            # self.member_widget.setStyleSheet(f"QLabel#遠藤 さくらlbl {{ color: red; }}")
            self.lbl_name.setStyleSheet( "color: red;")

    def save_concerned_member(self):
        with open('member/hinata/concerned_member.txt', 'w', encoding='utf-8') as file:
            for child in self.member_widget.findChildren(QLabel):
                lbl_name = child.objectName() #ex.遠藤 さくらlbl
                self.lbl_name = self.member_widget.findChild(QLabel, lbl_name)
                current_style = self.lbl_name.styleSheet()
                if "color: red;" in current_style:
                    file.write(child.objectName().rstrip("lbl")+"\n")
    def return_to_main(self):
        self.save_concerned_member()
        self.parent().setGeometry(self.geometry())  
        self.parent().show()
        self.close()


class saku_member_window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(self.parent().geometry())
        self.setWindowTitle("member_select")
        self.entered_btn = QPushButton("確定", self)
        self.entered_btn.setCursor(Qt.PointingHandCursor)
        self.entered_btn.setGeometry(1100, 500,75,24)
        # self.entered_btn.adjustSize()

        self.entered_btn.clicked.connect(self.return_to_main)

        self.member_widget = QWidget(self)
        self.member_widget.setGeometry(80, 60, 1020, 470)
        self.setStyleSheet("QWidget { border: 2px solid black; }")

        #cal member's width and height: 253*319 pixel for picture
        #width: (1020-10-10-9*5)/10 = 96
        #height: (470-10-10-8*3)/3 = 142 (121+21)

        #run for loop, create member buttons
        # self.member_btns = {}
        # self.member_lbls = {}
        posi_x = 10
        posi_y = 10
        with open("member/sakura/concerned_member.txt", "r", encoding="utf-8") as file:
            concerned_members = file.read()
        with open("member/sakura/member_list.txt", 'r', encoding='utf-8') as file:
            for line in file:
                name = line.strip() #ex.遠藤 さくら
                btn_name = name + "btn"
                lbl_name = name + "lbl"
                self.btn_name = QPushButton(self.member_widget)
                self.btn_name.setObjectName(btn_name)
                self.btn_name.setGeometry(posi_x,posi_y,96,121)
                self.btn_name.setCursor(Qt.PointingHandCursor)
                self.lbl_name = QLabel(name,self.member_widget)
                self.lbl_name.setObjectName(lbl_name)
                self.lbl_name.adjustSize()
                self.lbl_name.setGeometry(posi_x,posi_y+121+5,96,21) #space 5 between picture and txt

                # set member picture as the button pattern
                self.btn_name.setStyleSheet(f"QPushButton {{ border-image: url('member/sakura/{name}.jpg') 0; }}")

                # initially, it's red-black relative to concerned member
                if name in concerned_members:
                    self.lbl_name.setStyleSheet("QLabel { color: red; }")
                else:
                    self.lbl_name.setStyleSheet("QLabel { color: black; }")

                # click event
                self.btn_name.clicked.connect(self.change_label_color)

                # self.member_btns[btn_name] = self.btn_name
                # self.member_lbls[lbl_name] = self.lbl_name

                posi_x += 96+5
                if posi_x>1000:
                    posi_x = 10 #next row
                    posi_y += 142 + 5

    def change_label_color(self):
        button = self.sender() #is a btn object
        name = button.objectName().rstrip("btn")#ex. 遠藤 さくらbtn
        lbl_name = name+"lbl"
        self.lbl_name = self.member_widget.findChild(QLabel, lbl_name)
        current_style = self.lbl_name.styleSheet()
        # print(current_style)

        #depend on current color, switch to another one
        if "color: red;" in current_style:
            # self.lbl_name.setStyleSheet("QLabel { color: black; }")
            self.lbl_name.setStyleSheet( "color: black;")
        else:
            # self.member_widget.setStyleSheet(f"QLabel#遠藤 さくらlbl {{ color: red; }}")
            self.lbl_name.setStyleSheet( "color: red;")

    def save_concerned_member(self):
        with open('member/sakura/concerned_member.txt', 'w', encoding='utf-8') as file:
            for child in self.member_widget.findChildren(QLabel):
                lbl_name = child.objectName() #ex.遠藤 さくらlbl
                self.lbl_name = self.member_widget.findChild(QLabel, lbl_name)
                current_style = self.lbl_name.styleSheet()
                if "color: red;" in current_style:
                    file.write(child.objectName().rstrip("lbl")+"\n")
    def return_to_main(self):
        self.save_concerned_member()
        self.parent().setGeometry(self.geometry())  
        self.parent().show()
        self.close()
