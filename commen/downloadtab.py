from . import QWidget, QHBoxLayout
from . import threading, logging

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QListWidget, 
    QListWidgetItem, QProgressBar, QLabel, QCheckBox, QScrollArea, QFrame
)

from PyQt5.QtCore import QThread, pyqtSignal
import time

from . import search, downloader

class SearchThread(QThread):
    search_finished = pyqtSignal()
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def run(self):
        self.parent.search_button.setText("Searching...")
        self.parent.search_button.setEnabled(False)
        time.sleep(2)  # Simulate search delay
        self.parent.deploy_search()
        self.search_finished.emit()

class DownloadTab(QWidget):
    def __init__(self):
        super().__init__()
        logging.info("Generating Download tab")
        self.delete_list = []
        self.searcher = search.Searcher()
        #self.downloader = downloader.Downloader()
        
        main_layout = QHBoxLayout(self)
        
        # Left Section (Search & Results)
        left_layout = QVBoxLayout()
        
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.deploy_search)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        left_layout.addLayout(search_layout)
        
        self.results_list = QListWidget()
        left_layout.addWidget(self.results_list)
        
        # Download Progress Section
        self.progress_bar = QProgressBar()
        left_layout.addWidget(self.progress_bar)
        
        self.download_info = QLabel("Speed: 0 KB/s | ETA: --:--")
        left_layout.addWidget(self.download_info)
        
        main_layout.addLayout(left_layout)
        
        # Right Section (Search Settings)
        right_layout = QVBoxLayout()
        
        self.checkboxes = []
        for i in range(4):
            checkbox = QCheckBox(f"Option {i+1}")
            self.checkboxes.append(checkbox)
            right_layout.addWidget(checkbox)
        
        main_layout.addLayout(right_layout)
        
        self.setLayout(main_layout)

    def start_search(self):
        logging.info("Search thread started")
        self.search_thread = SearchThread(self)
        self.search_thread.search_finished.connect(self.search_complete)
        self.search_thread.start()
    
    def search_complete(self):
        logging.info("Seach completed")
        self.search_button.setText("Search")
        self.search_button.setEnabled(True)
    
    def deploy_search(self):
        results = self.searcher.search(self.search_input.text())
        
        for i in reversed(range(self.results_list.count())):
            item = self.results_list.takeItem(i)  # Removes item
            del item  # Ensure deletion

        self.delete_list.clear()  # ✅ Remove old references

        
        for result in results:
            self.add_result(result["name"], result["link"])

    def add_result(self, name, url):
        logging.debug(f"added {name}")
        item = QListWidgetItem(name)
        button = QPushButton("Download")
        button.clicked.connect(lambda _, link=url: threading.Thread(target=downloader.start, args=[link]).start())
        
        list_item_widget = QWidget()
        item_layout = QHBoxLayout()
        item_layout.addWidget(QLabel(name))
        item_layout.addWidget(button)
        list_item_widget.setLayout(item_layout)
        
        list_item_widget.setLayout(item_layout)
        item.setSizeHint(list_item_widget.sizeHint())
        self.results_list.addItem(item)
        self.results_list.setItemWidget(item, list_item_widget)
        
        self.delete_list.append(item)
        self.delete_list.append(list_item_widget)
        self.delete_list.append(button)  # Keep track of buttons if needed

