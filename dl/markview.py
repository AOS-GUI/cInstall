from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from sdk.sdk import *

from os import name

#~markview|simple markdown viewer for AOS|v1.0

class markview(QMainWindow):
    def __init__(self):
        super(markview, self).__init__()
        self.resize(500, 400)
        self.setWindowTitle("markview")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        grid = QGridLayout()
        self.centralWidget().setLayout(grid)

        if name == "nt":
            self.menuBar().setStyleSheet(
                """
                QMenuBar
                {
                    background-color: #fff;
                    color: #000;
                }
                QMenuBar::item
                {
                    background-color: #fff;
                    color: #000;
                }
                QMenuBar::item::selected
                {
                    background-color: #3399cc;
                    color: #fff;
                }
                QMenu
                {
                    background-color: #fff;
                    color: #000;
                }
                QMenu::item::selected
                {
                    background-color: #333399;
                    color: #999;
                }
                """
            )

        # self.updateTimer = QTimer()
        # self.updateTimer.timeout.connect(lambda: self.openFile(self.filepath))

        self.viewer = QTextBrowser(self)
        self.viewer.setReadOnly(True)

        self.viewer.setMarkdown("""
# Hello!

### Welcome to markview!

Open a file to, well, view a file.
        """)

        self.fileMenu = self.menuBar().addMenu("&File")
        self.openAction = QAction(self)
        self.openAction.setText("Open...")
        self.openAction.triggered.connect(self.openFile)
        self.refreshAction = QAction(self)
        self.refreshAction.setText("Refresh")
        self.refreshAction.triggered.connect(lambda: self.openFile(True))
        self.quitAction = QAction(self)
        self.quitAction.setText("Exit")
        def leave():
            raise SystemExit
        self.quitAction.triggered.connect(leave)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.refreshAction)
        self.fileMenu.addAction(self.quitAction)

        grid.addWidget(self.viewer,0,0)

        # self.updateTimer.start(1000)

        self.filepath = None

        self.openSC = QShortcut(QKeySequence("Ctrl+O"), self)
        self.openSC.activated.connect(lambda: self.openFile())
        self.refreshSC = QShortcut(QKeySequence("Ctrl+R"), self)
        self.refreshSC.activated.connect(lambda: self.openFile(True))

    def openFile(self, refresh=False):
        if refresh:
            check = True
            file = self.filepath
        else:
            file,check = QFileDialog.getOpenFileName(None, "Open a file", getAOSdir()+"/", "Markdown File (*.md);;All Files (*)")

        if check and file != None:
            fileOpen = open(file,encoding="utf-8")
            text = fileOpen.read()
            fileOpen.close()

            self.filepath = file

            self.viewer.setMarkdown(text)


if __name__ == "__main__":
    app = QApplication([])
    window = markview()

    if getSettings()["inAppTheme"]["use"] == "True":
        app.setPalette(getPalette())

    window.show()
    exit(app.exec_())