# importing required libraries

#~nanoweb|nanoweb for AOS|v1.0

from sys import argv


try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain


try:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtWebEngineWidgets import *
    from PyQt5.QtPrintSupport import *
    import sys
    import os
except:
    print("nanoweb: a module wasn't installed, installing all modules...")
    pipmain(["install","PyQt5"])
    pipmain(["install","PyQtWebEngine"])


try:
    argvAddr = sys.argv[1]
    if (argvAddr.find("https://") or argvAddr.find("http://")):
        argvAddr = "https://"+sys.argv[1]
except IndexError:
    argvAddr = ""


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.tabs = QTabWidget()
        self.tabs.setMovable(False)

        # self.setStyleSheet('''
        #     QTabWidget {
        #         color: white;
        #         background-color: black;
        #     }
        # ''')

        # self.tabs.setStyleSheet("color: black; background-color:black")

        self.tabs.setDocumentMode(True)
        self.tabs.tabBarClicked.connect(self.tab_open_click)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        back_btn = QAction("<", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(">", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction("↻", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)
        
        navtb.addSeparator()

        # dlBtn = QAction("DL", self)
        # dlBtn.setStatusTip("Download URL")
        # dlBtn.triggered.connect(lambda: self.dl())
        # navtb.addAction(dlBtn)

        # bookmark = QAction("🔖", self)
        # bookmark.setStatusTip("Create Bookmark")
        # bookmark.triggered.connect(lambda: self.bookmark())
        # navtb.addAction(bookmark)

        # showBMs = QAction("📓", self)
        # showBMs.setStatusTip("List Bookmarks")
        # showBMs.triggered.connect(lambda: self.dl())
        # navtb.addAction(showBMs)

        # delBK = QAction("📓X", self)
        # delBK.setStatusTip("Delete a Bookmark (go to the webpage that was bookmarked, then press me)")
        # delBK.triggered.connect(lambda: self.delBK())
        # navtb.addAction(delBK)

        # delABK = QAction("X📓X", self)
        # delABK.setStatusTip("Delete All Bookmarks")
        # delABK.triggered.connect(lambda: self.delABK())
        # navtb.addAction(delABK)

        navtb.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        # self.urlbar.setStyleSheet("color: white; background-color:black;")

        navtb.addWidget(self.urlbar)

        # stop_btn = QAction("X", self)
        # stop_btn.setStatusTip("Stop loading current page")
        # stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        # navtb.addAction(stop_btn)
        if argvAddr == "":
            self.add_new_tab(QUrl("http://www.duckduckgo.com/"), "Homepage")
        else:
            self.add_new_tab(QUrl(argvAddr), "Webpage")

        self.show()

        self.setWindowTitle("nanoweb")
    
    def bookmark(self):
        f = open("data\\bkmk.nweb","r")
        q = QUrl(self.urlbar.text()).toString()
        if q in f.read():
            print("bookmark already added")
            f.close()
        else:
            f.close()
            f = open("data\\bkmk.nweb","a")
            f.write(f"\n{q}")
            f.close()

    def dl(self):
        os.system('python browser/nanoscrape.py"')
    
    def showBookmarks(self):
        f = open("data\\bkmk.nweb","r")
        nf = f.read().split("\n")
        for i in nf:
            if i == "\n":
                pass
            else:
                print(i)
        f.close()
    
    def delBK(self):
        with open("data\\bkmk.nweb", "r+") as f:
            read = f.readlines()
            q = QUrl(self.urlbar.text()).toString()
        with open("data\\bkmk.nweb", "w") as f:
            for line in read:
                if line.strip("\n") != q:
                    f.write(line)
            
    def delABK(self):
        with open("data\\bkmk.nweb","w") as f:
            f.truncate()
            f.write("# nanoweb bookmarks\n")

    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        self.menu.addAction('My action')
        self.menu.popup(event.globalPos())

    def add_new_tab(self, qurl = None, label ="Blank"):
        if qurl is None:
            qurl = QUrl("http://www.duckduckgo.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser = browser:
            self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i = i, browser = browser:
            self.tabs.setTabText(i, browser.page().title()))

    def tab_open_click(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

        

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            quit()

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()

        if title == "":
            self.setWindowTitle(f"blank - nanoweb")
        else:
            self.setWindowTitle(f"{title} - nanoweb")

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.duckduckgo.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())

        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser = None):
        if browser != self.tabs.currentWidget():
            return

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


# class Ui_Dialog(object):
#     # def setupUi(self,Dialog):
#     def setupUi(self, Dialog):
#         Dialog.setObjectName("Dialog")
#         Dialog.resize(401, 165)
#         self.buttonBox = QDialogButtonBox(Dialog)
#         self.buttonBox.setGeometry(QRect(30, 120, 341, 32))
#         self.buttonBox.setOrientation(Qt.Horizontal)
#         self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
#         self.buttonBox.setCenterButtons(True)
#         self.buttonBox.setObjectName("buttonBox")
#         self.checkBox = QCheckBox(Dialog)
#         self.checkBox.setGeometry(QRect(120, 100, 171, 17))
#         self.checkBox.setObjectName("checkBox")
#         self.textBrowser = QTextBrowser(Dialog)
#         self.textBrowser.setGeometry(QRect(0, 40, 401, 41))
#         self.textBrowser.setObjectName("textBrowser")

#         self.retranslateUi(Dialog)
#         self.buttonBox.accepted.connect(Dialog.accept)
#         self.buttonBox.rejected.connect(Dialog.reject)
#         QMetaObject.connectSlotsByName(Dialog)

#     def retranslateUi(self, Dialog):
#         _translate = QCoreApplication.translate
#         Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
#         self.checkBox.setText(_translate("Dialog", "Don\'t show this message again"))
#         self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
# "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Welcome to NANOWEB, the portable, cross-platform browser.</span></p>\n"
# "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">for more information, visit <a href=\" https://nanobot567.github.io/nanoweb\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">https://nanobot567.github.io/nanoweb</span></a></p></body></html>"))



app = QApplication(sys.argv)

app.setApplicationName("nanoweb")
app.setWindowIcon(QIcon("nanoweb.png"))

# dialog = Ui_Dialog()
window = MainWindow()


app.exec_()
