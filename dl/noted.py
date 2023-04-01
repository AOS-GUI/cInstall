from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from files.apps.sdk.sdk import *
from os import makedirs

#~noted|quick notes app|v1.0

totaldata = ""
firstResize = True

class noted(QWidget):
    def __init__(self):
        global totaldata
        super(noted, self).__init__()
        self.resize(250, 200)
        self.setWindowTitle("noted")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        self.editBox = QTextEdit(self)
        self.editBox.setGeometry(0,0,self.frameGeometry().width(),self.frameGeometry().height())
        self.editBox.textChanged.connect(self.updateStatus)

        makedirs(getAOSdir()+"apps/assets/noted/",exist_ok=True)

        try:
            with open(getAOSdir()+"apps/assets/noted/notes.txt","r") as f:
                totaldata = f.read()
                self.editBox.setText(totaldata)
        except FileNotFoundError:
            f = open(getAOSdir()+"apps/assets/noted/notes.txt","w+")
            f.close()

        self.installEventFilter(self)

    def updateStatus(self):
        global totaldata
        totaldata = self.editBox.toPlainText()

    def eventFilter(self, obj, event):
        global firstResize
        if (event.type() == QEvent.Resize):
            if firstResize == True:
                self.editBox.setGeometry(0,0,self.frameGeometry().width(),self.frameGeometry().height())
                firstResize = False
            else:
                self.editBox.setGeometry(0,0,self.frameGeometry().width(),self.frameGeometry().height()-30)
        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        global totaldata
        f = open(getAOSdir()+"apps/assets/noted/notes.txt","w+")
        f.write(totaldata)
        f.close()

window = noted()
window.show()