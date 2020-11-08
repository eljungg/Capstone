from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base

class VariableContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("Variable Node Class" , self)
        self.edit.setAlignment(Qt.AlignLeft)

class VariableNode(VplNode):
    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])

    def initInnerClasses(self):
        self.content = VariableContent(self)
        self.grNode = VplGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)