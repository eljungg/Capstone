import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class printWindow(QWidget):
    def __init__(self, windowContent):
        super().__init__()
        self.windowContent = windowContent

        layout = QVBoxLayout()
        for i in windowContent:
            self.l = QLabel(i)
            layout.addWidget(self.l)

        b = QPushButton("Stop")
        b.pressed.connect(self.on_click)
        b.pressed.connect(self.close)

        layout.addWidget(b)

        self.setLayout(layout)

    def on_click(self):
        print('PyQt5 button click')