import sys
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,QGridLayout,QWidget
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QScreen

# create a function that do things after button is pressed
def nogi_clicked():
    label.setText("Button pressed!!")
    label.adjustSize()

#create an app example
app = QApplication(sys.argv)

# create a window
window = QWidget()
window.setWindowTitle("Sakamichi_blog_downloader")

# set window size
window.resize(1200, 600) 

# get screen size and move to its center
screen = app.primaryScreen().geometry()
window.move(
    int((screen.width() - window.width()) / 2),
    int((screen.height() - window.height()) / 2 - 30)
)


# create a label and a button
label = QLabel(window)
label.setText('pressed the button below')
label.setStyleSheet("QLabel { border: 1px solid black; }")
label.setGeometry(200,200,100,100)
label.adjustSize()
button = QPushButton(window)
button.setText('pressed me')
# button.setStyleSheet("QPushButton { border: 1px solid blue; }")
button.setGeometry(10,10,100,100)
button.adjustSize()

# link the button to the function
button.clicked.connect(nogi_clicked)

# show window
window.show()

#run the process and loop the event
sys.exit(app.exec())
