
#######################################################################
# Every Modul that does not have to be installed

import os
import threading
import logging
import shutil
import json
import re
import time
import random
import string
import subprocess

#######################################################################
# installed packages imports

import requests
import rarfile
import psutil
import ctypes

from tqdm import tqdm

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QStackedWidget, QHBoxLayout, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt

from playwright.sync_api import sync_playwright #playwright install

#######################################################################
# relativ imports

from . import search
from . import downloader
from . import commen
from . import libarytab
from . import rungame
from . import search
from . import downloadtab