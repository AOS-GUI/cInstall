# importing required libraries

#~nanoweb|nanoweb for AOS|v1.1

needsInstall = False

from os import mkdir
from sys import argv

try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain

from sdk.sdk import *

try:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtWebEngineWidgets import *
except ModuleNotFoundError:
    needsInstall = True

version = 1.1


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.tabs = QTabWidget()
        self.tabs.setMovable(True)

        self.tabs.setDocumentMode(True)
        self.tabs.tabBarClicked.connect(self.tab_open_click)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        self.fileMenu = self.menuBar().addMenu("&File")
        self.settingsMenu = self.menuBar().addMenu("&Settings")
        self.aboutAction = QAction(self)
        self.aboutAction.setText("About...")
        self.aboutAction.triggered.connect(lambda: msgBox("nanoweb for AOS v"+str(version)+" by nanobot567.","nanoweb"))
        self.quitAction = QAction(self)
        self.quitAction.setText("Quit")
        def leave():
            raise SystemExit
        self.quitAction.triggered.connect(leave)
        def openHTMLActionDef():
            file, check = QFileDialog.getOpenFileName(None, "Open a file", getAOSdir()+"/", "HTML File (*.html)")
            if check:
                self.openHTML(file)
        self.openHTMLAction = QAction(self)
        self.openHTMLAction.setText("Open HTML...")
        self.openHTMLAction.triggered.connect(openHTMLActionDef)
        def clearCache():
            self.tabs.currentWidget().page().profile().clearHttpCache()
            self.tabs.currentWidget().page().profile().clearAllVisitedLinks()
        self.clearCacheAction = QAction(self)
        self.clearCacheAction.setText("Clear cache")
        self.clearCacheAction.triggered.connect(clearCache)
        self.persistentCookiesAction = QAction(self)
        self.persistentCookiesAction.setText("Persistent cookies")
        self.persistentCookiesAction.setCheckable(True)
        self.persistentCookiesAction.setChecked(True)
        self.persistentCookiesAction.triggered.connect(lambda: self.tabs.currentWidget().page().profile().setPersistentCookiesPolicy(self.persistentCookiesAction.isChecked()))

        self.fileMenu.addAction(self.openHTMLAction)
        self.fileMenu.addAction(self.aboutAction)
        self.fileMenu.addAction(self.quitAction)
        self.settingsMenu.addAction(self.clearCacheAction)
        self.settingsMenu.addAction(self.persistentCookiesAction)

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

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        # self.urlbar.setStyleSheet("color: white; background-color:black;")

        navtb.addWidget(self.urlbar)

        if not needsInstall:
            self.add_new_tab(
                QUrl.fromUserInput("http://www.duckduckgo.com/"), "Homepage"
            )

        try:
            mkdir(getAOSdir()+"/apps/assets/nanoweb/")
            mkdir(getAOSdir()+"/apps/assets/nanoweb/cache/")
        except FileExistsError:
            pass

        try:
            self.tabs.currentWidget().page().profile().setPersistentStoragePath(getAOSdir()+"apps/assets/nanoweb/cache")
        except AttributeError:
            pass

        self.show()

        self.setWindowTitle("nanoweb")

    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        self.menu.addAction("My action")
        self.menu.popup(event.globalPos())

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl.fromUserInput("http://www.duckduckgo.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)
        #QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled,False)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(
            lambda qurl, browser=browser: self.update_urlbar(qurl, browser)
        )

        browser.loadFinished.connect(
            lambda _, i=i, browser=browser: self.tabs.setTabText(
                i, browser.page().title()
            )
        )

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
        q = QUrl.fromUserInput(self.urlbar.text())

        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def openHTML(self, f):
        self.add_new_tab()
        q = QUrl.fromUserInput("file:///"+f)

        self.tabs.currentWidget().setUrl(q)


Qt.process_model = "single-process"

app = QApplication(["", "--no-sandbox"])

app.setApplicationName("nanoweb")
app.setWindowIcon(QIcon("nanoweb.png"))
if getSettings()["inAppTheme"]["use"] == "True" and needsInstall == False:
    app.setPalette(getPalette())

# dialog = Ui_Dialog()
window = MainWindow()

if needsInstall:
    respose = msgBox("Hello! You don't currently have PyQtWebEngine installed, which is required for nanoweb. Would you like to install it now? (If you say yes, please wait a couple moments before you try to open nanoweb again.)","nanoweb - requirement not satisfied",QMessageBox.Question,QMessageBox.Yes|QMessageBox.No)
    if respose == QMessageBox.Yes:
        print("nanoweb: a module wasn't installed, installing all modules...")
        pipmain(["install", "PyQtWebEngine"])
        quit()


app.exec_()
