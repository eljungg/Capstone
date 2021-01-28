from PyQt5.QtWidgets import *
import PyQt5.QtCore

class ExecutionWindow(QWidget):
    def __init__(self, sDialog=False):
        super().__init__()
        self.sDialog = sDialog
        self.text = ""
        if sDialog == False:
            self.text += "Program Started.\n"
        self._InitUI()
        
    def _InitUI(self):
        self.setFixedSize(600, 600)
        self.layout = QVBoxLayout()

        self.textBox = QLabel()
        self.title = QLabel("This is the Execution Window") #just to show us what we are looking at
        self.textBox.setFixedSize(580, 500)
        self.textBox.setText(self.text)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.textBox)

        self.button = QPushButton()
        if self.sDialog:
            self.button.setText("Ok")
        else:
            self.button.setText("Stop")
        self.button.clicked.connect(lambda: self._buttonClicked())
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def _buttonClicked(self):
        self.close()

    def appendText(self, text):
        self.text += text
        self.textBox.setText(self.text)
