from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from files.apps.sdk.sdk import *
from os import makedirs

#~noted|quick notes app|v1.1

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

        try:
            with open(getAOSdir()+"apps/assets/noted/pos","r") as f:
                pos = f.read().split(",")
                self.move(int(pos[0]),int(pos[1]))
        except Exception as e:
            pass

        makedirs(getAOSdir()+"apps/assets/noted/",exist_ok=True)

        try:
            with open(getAOSdir()+"apps/assets/noted/notes.txt","r") as f:
                totaldata = f.read()
                self.editBox.setText(totaldata)
        except FileNotFoundError:
            f = open(getAOSdir()+"apps/assets/noted/notes.txt","w+")
            f.close()

        self.installEventFilter(self)

    def location(self):
        #geo = self.geometry()
        return [self.x(),self.y()]

    def updateStatus(self):
        global totaldata
        totaldata = self.editBox.toPlainText()

        with open(getAOSdir()+"apps/assets/noted/notes.txt","w+") as f:
            f.write(totaldata)
            f.close()
        with open(getAOSdir()+"apps/assets/noted/pos","w+") as f:
            pos = self.location()

            f.write(str(pos[0])+","+str(pos[1]))

    def eventFilter(self, obj, event):
        global firstResize
        if (event.type() == QEvent.Resize):
            if firstResize == True:
                self.editBox.setGeometry(0,0,self.frameGeometry().width(),self.frameGeometry().height())
                firstResize = False
            else:
                self.editBox.setGeometry(0,0,self.frameGeometry().width(),self.frameGeometry().height()-30)
        elif event.type() == QEvent.Move:
            with open(getAOSdir()+"apps/assets/noted/pos","w+") as f:
                pos = self.location()

                f.write(str(pos[0])+","+str(pos[1]))
        return super().eventFilter(obj, event)
            

window = noted()
window.show()
