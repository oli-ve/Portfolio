import pandas as pd
import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from random import *
from os import listdir

class navigationButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicked.connect(self.goTo)

    def linkToStack(self, stack):
        self.stack = stack
        self.text = self.text()

    def goTo(self):
        if self.text == "Return Home":
            self.stack.setCurrentIndex(0)
        elif self.text == "Search for a book":
            self.stack.setCurrentIndex(1)
        elif self.text == "Add a new book":
            self.stack.setCurrentIndex(2)
        elif self.text == "View a book":
            self.stack.setCurrentIndex(3)

