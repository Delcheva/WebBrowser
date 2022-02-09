import os, sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QLineEdit, QDesktopWidget, QTabWidget, QHBoxLayout,
                             QVBoxLayout, QAction, QToolBar, QProgressBar, QStatusBar)
from PyQt5.QtCore import QSize, QUrl, QRect
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

stylesheet = """
    QTabWidget: pane{
    border: none
    }
    """


class MyWebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create lists that will keep track of the new windows,
        # tabs and urls
        self.window_list = []
        self.list_of_pages = []
        self.list_of_urls = []

        self.initialize_ui()

    def initialize_ui(self):
        self.setMinimumSize(400, 300)
        self.setWindowTitle("My Web Browser")
        self.setWindowIcon(QIcon(os.path.join("images", "My_Logo.png")))

        self.position_main_window()

        self.create_menu()
        self.create_toolbar()
        self.create_tabs()

        self.show()

    def position_main_window(self):
        """
        Use QDesktopWidget class to access information about your screen
        and use it to position the application window when starting a new application.
        """
        desktop = QDesktopWidget().screenGeometry()
        screen_width = desktop.width()
        screen_height = desktop.height()
        self.setGeometry(0, 0, screen_width, screen_height)

    def create_menu(self):
        # Setup menu bar
        new_window = QAction("New Window", self)
        new_window.setShortcut("Ctrl + N")
        new_window.triggered.connect(self.open_new_window)

        new_tab = QAction("New Tab", self)
        new_tab.setShortcut("Ctrl + T")
        new_tab.triggered.connect(self.open_new_tab)

        reload_page = QAction("Reload Page", self)
        reload_page.setShortcut("Ctrl + R")
        reload_page.triggered.connect(self.reload_pages)

        print_page = QAction("Print Page", self)
        print_page.setShortcut("Ctrl + P")
        print_page.triggered.connect(self.print_pages)

        quit_file = QAction("Quit From Browser", self)
        quit_file.setShortcut("Ctrl + Q")
        quit_file.triggered.connect(self.close)

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Menu and Actions
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(new_window)
        file_menu.addSeparator()
        file_menu.addAction(new_tab)
        file_menu.addSeparator()
        file_menu.addAction(reload_page)
        file_menu.addSeparator()
        file_menu.addAction(print_page)
        file_menu.addSeparator()
        file_menu.addAction(quit_file)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def create_toolbar(self):
        # Setup navigation toolbar

        toolbar = QToolBar("Address Bar")
        toolbar.setIconSize(QSize(40, 40))
        self.addToolBar(toolbar)

        # Toolbar actions
        back_page_btn = QAction(QIcon(os.path.join("images", "back.png")), "Back", self)
        back_page_btn.triggered.connect(self.back_page_button)

        forward_page_btn = QAction(QIcon(os.path.join("images", "forward.png")), "Forward", self)
        forward_page_btn.triggered.connect(self.forward_page_button)

        refresh_button = QAction(QIcon(os.path.join("images", "refresh.png")), "Refresh", self)
        refresh_button.triggered.connect(self.refresh_page_button)

        home_button = QAction(QIcon(os.path.join("images", "home.png")), "Home", self)
        home_button.triggered.connect(self.home_page_button)

        stop_button = QAction(QIcon(os.path.join("images", "stop.png")), "Stop", self)
        stop_button.triggered.connect(self.stop_page_button)

        print_page = QAction(QIcon(os.path.join("images", "print.png")), "Print Page", self)
        print_page.triggered.connect(self.print_pages)

        # Address Bar
        self.adress_line = QLineEdit()
        self.adress_line.addAction(QIcon("images/find.png"), QLineEdit.LeadingPosition)
        self.adress_line.setPlaceholderText("Enter Website Address")
        self.adress_line.returnPressed.connect(self.search_for_url)

        toolbar.addAction(home_button)
        toolbar.addAction(back_page_btn)
        toolbar.addAction(forward_page_btn)
        toolbar.addAction(refresh_button)
        toolbar.addAction(print_page)
        toolbar.addWidget(self.adress_line)
        toolbar.addAction(stop_button)

    def create_tabs(self):
        #Create QTabWidget

        self.tab_bar = QTabWidget()
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setTabBarAutoHide(True)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)

        self.main_tab = QWidget()
        self.tab_bar.addTab(self.main_tab, "New Tab")

        self.setup_tab(self.main_tab)

        self.setCentralWidget(self.tab_bar)

    def open_new_window(self):
        new_window = MyWebBrowser()
        new_window.show()
        self.window_list.append(new_window)

    def open_new_tab(self):
        new_tab = QWidget()
        self.tab_bar.addTab(new_tab, "New Tab")
        self.setup_tab(new_tab)

        tab_index = self.tab_bar.currentIndex()
        self.tab_bar.setCurrentIndex(tab_index + 1)
        self.list_of_pages[self.tab_bar.currentIndex()].load(QUrl("https://www.python.org"))

    def back_page_button(self):
        tab_index = self.tab_bar.currentIndex()
        self.list_of_pages[tab_index].back()

    def forward_page_button(self):
        tab_index = self.tab_bar.currentIndex()
        self.list_of_pages[tab_index].forward()

    def refresh_page_button(self):
        tab_index = self.tab_bar.currentIndex()
        self.list_of_pages[tab_index].reload()

    def reload_pages(self):
        tab_index = self.tab_bar.currentIndex()
        self.list_of_pages[tab_index].reload()

    def home_page_button(self):
        tab_index = self.tab_bar.currentIndex()
        self.list_of_pages[tab_index].setUrl(QUrl("https://www.python.org"))

    def stop_page_button(self):
        tab_index = self.tab_bar.currentIndex()
        self.list_of_pages[tab_index].stop()

    def search_for_url(self):
        current_index = self.tab_bar.currentIndex()
        url_page = self.list_of_urls[current_index].text()

        url = QUrl(url_page)
        if url.scheme() == "":
            url.setScheme("http")

        if url.isValid():
            self.list_of_pages[current_index].page().load(url)
        else:
            url.clear()

    def close_tab(self, tab_index):
        self.list_of_pages.pop(tab_index)
        self.list_of_urls.pop(tab_index)

        self.tab_bar.removeTab(tab_index)

    def setup_tab(self, tab):
        self.web_page = self.setup_page()

        v_box = QVBoxLayout()
        v_box.setContentsMargins(0, 0, 0, 0)
        v_box.addWidget(self.web_page)

        self.list_of_pages.append(self.web_page)
        self.list_of_urls.append(self.adress_line)
        self.tab_bar.setCurrentWidget(self.web_page)

        self.tab_bar.currentChanged.connect(self.update_url)
        tab.setLayout(v_box)

    def print_pages(self):
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.NativeFormat)

        print_dialog = QPrintDialog(printer)

        if print_dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter()
            painter.begin(printer)
            rect = QRect(painter.viewport())
            size = QSize(self.web_page.pixmap().size())
            size.scale(rect.size().QtKeepAspectRatio)
            printer.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.web_page.pixmap().rect())
            painter.drawPixmap(0, 0, self.web_page.pixmap())
            painter.end()

    def setup_page(self):
        web_view = QWebEngineView()
        web_view.setUrl(QUrl("https://www.python.org"))

        self.page_progress = QProgressBar()
        self.page_progress_label = QLabel()
        web_view.loadProgress.connect(self.update_progressbar)

        web_view.urlChanged.connect(self.update_url)

        yes = web_view.loadFinished.connect(self.update_tab_name)

        if yes:
            return web_view
        else:
            print("Requested time out!")

    def update_progressbar(self, progress):
        if progress < 100:
            self.page_progress.setVisible(progress)
            self.page_progress.setValue(progress)
            self.page_progress_label.setVisible(progress)
            self.page_progress_label.setText("Loading Page ... ({}/100). Please Wait...".format(str(progress)))
            self.status_bar.addWidget(self.page_progress)
            self.status_bar.addWidget(self.page_progress_label)
        else:
            self.status_bar.removeWidget(self.page_progress)
            self.status_bar.removeWidget(self.page_progress_label)

    def update_url(self):
        tab_index = self.tab_bar.currentIndex()
        url = self.list_of_pages[tab_index].page().url()
        formatted_url = QUrl(url).toString()
        self.list_of_urls[tab_index].setText(formatted_url)

    def update_tab_name(self):
        tab_index = self.tab_bar.currentIndex()
        name = self.list_of_pages[tab_index].page().title()
        self.tab_bar.setTabText(tab_index, name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = MyWebBrowser()
    app.exec_()







