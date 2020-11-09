from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base

class DataContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("Data Node Class" , self)
        self.edit.setAlignment(Qt.AlignLeft)

class DataNode(VplNode):
    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])

    def initInnerClasses(self):
        self.content = DataContent(self)
        self.grNode = VplGraphicsNode(self)
        #below is onTextChanged event for simple self.edit Label
        self.content.edit.textChanged.connect(self.onInputChanged)