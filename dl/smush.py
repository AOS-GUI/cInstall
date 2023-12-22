from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import zipfile
import os

from files.apps.sdk.sdk import *

inputs = []
output = ""

#~smush|compression/decompression program|v1.0

class smush(QWidget):
    def __init__(self):
        global inputs, output

        super(smush, self).__init__()
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setFixedSize(400,100)
        
        self.label = QLabel("smush", self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignRight)
        self.label.setStyleSheet("QLabel {font-size:16px;}")
        self.label.setGeometry(0,5,395,100)

        self.button = QPushButton("Select input folder/file...", self)
        self.button2 = QPushButton("Select output folder/file...", self)

        def getinput():
            global inputs, output
            if self.combo.currentText() == "zip":
                files = self.getOpenFilesAndDirs(None, "Select input folders/files", directory=getAOSdir())
            else:
                files = list(QFileDialog.getOpenFileName(None, "Select an input folder / file", directory=getAOSdir()))
            print(files)
            inputs = files

        def getoutput():
            global inputs, output
            file = ""
            check = ""
            if self.combo.currentText() == "decompress":
                file = QFileDialog.getExistingDirectory(None, "Select an output directory", directory=getAOSdir())
                if file != None:
                    check = True
            else:
                file,check = QFileDialog.getSaveFileName(None, "Select an output folder/file", directory=getAOSdir(), filter="zip (*.zip);;AOS compressed file (*.aosc)")
            
            if check:
                output = file

        def zipdir(path, ziph):
            for root, dirs, files in os.walk(path):
                for file in files:
                    ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

        def execute():
            global inputs, output
            out = b""
            if self.combo.currentText() == "zip":
                ZipFile = zipfile.ZipFile(output, "w")

                for a in inputs:
                    if os.path.isdir(a):
                        zipdir(a, ZipFile)
                    else:
                        ZipFile.write(a, "C:\\" + os.path.basename(a), compress_type=zipfile.ZIP_DEFLATED)
                ZipFile.close()
            elif self.combo.currentText() == "aosc":
                msgBox(inputs[0])
            elif self.combo.currentText() == "decompress":
                ZipFile = zipfile.ZipFile(inputs[0], "r")
                ZipFile.extractall(output)
            msgBox("Finished!","smush")

        self.button.clicked.connect(getinput)
        self.button2.clicked.connect(getoutput)

        self.combo = QComboBox(self)
        self.combo.addItems(["zip","decompress"])
        self.button3 = QPushButton("Go!", self)
        self.button3.clicked.connect(execute)

        self.layout = QGridLayout()
        self.layout.addWidget(self.button, 0, 0)
        self.layout.addWidget(self.button2, 0, 1)
        # self.layout.addWidget(self.combo, 0, 2)
        self.layout.addWidget(self.button3, 0, 2)

        self.setLayout(self.layout)
    def getOpenFilesAndDirs(self, parent=None, caption='', directory='', 
                        filter='', initialFilter='', options=None):
        def updateText():
            selected = []
            for index in view.selectionModel().selectedRows():
                selected.append('"{}"'.format(index.data()))
            lineEdit.setText(' '.join(selected))

        dialog = QFileDialog(parent, windowTitle=caption)
        dialog.setFileMode(dialog.ExistingFiles)
        dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
        if options:
            dialog.setOptions(options)
        dialog.setOption(dialog.DontUseNativeDialog, True)
        if directory:
            dialog.setDirectory(directory)
        if filter:
            dialog.setNameFilter(filter)
            if initialFilter:
                dialog.selectNameFilter(initialFilter)
        dialog.accept = lambda: QDialog.accept(dialog)
        stackedWidget = dialog.findChild(QStackedWidget)
        view = stackedWidget.findChild(QListView)
        view.selectionModel().selectionChanged.connect(updateText)

        lineEdit = dialog.findChild(QLineEdit)
        # clear the line edit contents whenever the current directory changes
        dialog.directoryEntered.connect(lambda: lineEdit.setText(''))

        dialog.exec_()
        return dialog.selectedFiles()


window = smush()
window.show()