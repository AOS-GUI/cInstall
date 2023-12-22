# required imports

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from files.apps.sdk.sdk import *

#~autorunedit|autorun.aos editor|v1.1

class ARedit(QWidget):
    def __init__(self):
        super(ARedit, self).__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle("autorun.aos editor")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        self.appList = QListWidget(self)
        self.appList.setObjectName(u"appList")
        self.appList.setGeometry(QRect(0, 0, 260, 300))
        self.addAppButton = QPushButton(self)
        self.addAppButton.setObjectName(u"addAppButton")
        self.addAppButton.setGeometry(QRect(280, 70, 100, 28))
        self.addAppButton.setText(u"Add app")
        self.addAppButton.clicked.connect(self.addApp)
        self.removeAppButton = QPushButton(self)
        self.removeAppButton.setObjectName(u"removeAppButton")
        self.removeAppButton.setGeometry(QRect(280, 170, 100, 28))
        self.removeAppButton.setText(u"Remove app")
        self.removeAppButton.clicked.connect(self.removeApp)
        self.editAppButton = QPushButton(self)
        self.editAppButton.setObjectName(u"editAppButton")
        self.editAppButton.setGeometry(QRect(280, 120, 100, 28))
        self.editAppButton.setText(u"Edit app")
        self.editAppButton.clicked.connect(self.editApp)
        self.saveChangesButton = QPushButton(self)
        self.saveChangesButton.setObjectName(u"saveChangesButton")
        self.saveChangesButton.setGeometry(QRect(280, 260, 100, 28))
        self.saveChangesButton.setText(u"Save changes")
        self.saveChangesButton.clicked.connect(self.saveChanges)

        f = open("files/system/data/user/autorun.aos","r")

        for i in f.read().split("|"):
            if i:
                self.appList.addItem(i)

        f.close()

    def addApp(self):
        appInput, z = QInputDialog.getText(window, "Add app","Enter the name of the app you'd like to add:", QLineEdit.Normal, "")
        self.appList.addItem(appInput)
    
    def removeApp(self):
        self.appList.takeItem(self.appList.currentRow())
    
    def editApp(self):
        appInput, z = QInputDialog.getText(window, "Edit app","Enter the new name of the app:", QLineEdit.Normal, self.appList.currentItem().text())
        if appInput.strip() != "":
            self.appList.currentItem().setText(appInput)

    def saveChanges(self):
        f = open("files/system/data/user/autorun.aos","w")

        for i in range(self.appList.count()):
            f.write(self.appList.item(i).text())
            if i != self.appList.count()-1:
                f.write("|")

        f.close()
        msgBox("Saved changes to autorun.aos!","Saved!")


# these last two lines must be included for the app to launch.

window = ARedit()
window.show()
