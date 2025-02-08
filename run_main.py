from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout

from commen import commen, downloader
from commen.libarytab import LibaryTab
from commen.downloadtab import DownloadTab

import sys, os

class Ui_MainWindow(object):
    def init(self, mainwindow: QMainWindow):
        
        downloader.init()
        
        self.mainwindow = mainwindow
        
        self.search_generated_objects = []
        self.listed_games_objects = []
        
        self.mainwindow.setWindowTitle(commen.WINDOW_TITLE)
        self.mainwindow.resize(*commen.WINDOW_SIZE.get())
        
        self.tab_widget = TabWidget()
        
        self.tab_widget.setStyleSheet(commen.TAB_QWIDGET_STYLESHEET)
        
        self.mainwindow.setCentralWidget(self.tab_widget)
        
        self.mainwindow.setStyleSheet(commen.MAIN_STYLESHEET)

#class 
        
class TabWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.tab_info = {}
        self.last_tab = "Libary"

        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(commen.TAB_BUTTON_STYLESHEET)

        self.libary_tab = LibaryTab()
        self.download_tab = DownloadTab()
        
        self.tab21 = QWidget()
        self.tab14 = QWidget()

        # Inhalte für Tab 1
        #self.tab1_layout = QVBoxLayout()
        #self.tab1_layout.addWidget(QLabel("Das ist Tab 1"))
        #self.tab1.setLayout(self.tab1_layout)

        # Inhalte für Tab 2
        #self.tab2_layout = QVBoxLayout()
        #self.tab2_layout.addWidget(QLabel("Das ist Tab 2"))
        #self.tab2.setLayout(self.tab2_layout)

        # Tabs zum QTabWidget hinzufügen
        self.add_tab(self.libary_tab, "Libary")
        self.add_tab(self.download_tab, "Download")
        self.add_tab(self.tab14, "Settings")
        self.add_tab(self.tab21, "Support")
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        
        self.tabs.currentChanged.connect(self._on_tab_switch)
    
    def add_tab(self, tab, name):
        amount = self.tabs.count()
        self.tabs.addTab(tab, name)
        self.tab_info[amount] = name
    
    def _on_tab_switch(self, index):
        if self.tab_info[index] == "Libary":
            self.libary_tab.update_list()
        
        if self.tab_info[index] == "Support":
            os._exit(0)
        
        #if self.last_tab == "Libary":
        #    self.libary_tab.cleanup()
        
        self.last_tab = self.tab_info[index]
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    
    ui = Ui_MainWindow()
    ui.init(MainWindow)
    
    MainWindow.show()
    sys.exit(app.exec_())