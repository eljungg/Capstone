from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base

class MergeContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("Merge Node Class" , self)
        self.edit.setAlignment(Qt.AlignLeft)

class MergeNode(VplNode):
    def __init__(self, scene):
        super().__init__(scene, inputs=[4], outputs=[1])

    def initInnerClasses(self):
        self.content = MergeContent(self)
        self.grNode = VplGraphicsNode(self)
        #below is onTextChanged event for simple self.edit Label
        self.content.edit.textChanged.connect(self.onInputChanged)