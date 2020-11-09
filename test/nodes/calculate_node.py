from PyQt5.QtCore import *
from PyQt5.QtWidgets import QComboBox
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base

class CalculateContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("Calculate Node Class" , self)
        self.edit.setAlignment(Qt.AlignLeft)
        self.cBox = QComboBox(self)
        self.cBox.addItem('+')
        self.cBox.addItem('-')
        self.cBox.addItem('/')
        self.cBox.addItem('*')

class CalculateNode(VplNode):
    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[1])

    def initInnerClasses(self):
        self.content = CalculateContent(self)
        self.grNode = VplGraphicsNode(self)
        #below is onTextChanged event for simple self.edit Label
        self.content.edit.textChanged.connect(self.onInputChanged)