from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from nodeeditor.utils import dumpException
from nodeeditor.node_content_widget import QDMNodeContentWidget

from conf import *
from vpl_node import *

# In order to utilize TTS, you must ( for now ) place a TTS node before a Print node

class TtsContent(QDMNodeContentWidget):

    def __init__(self, parent):
        super().__init__(parent)

    
    def initUI(self):
        self.edit = QLabel('')
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.edit)
        self.setLayout(self.layout)

    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res 

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


class TtsNode(VplNode):
    op_code = OP_CODE_TTS

    def __init__(self, scene):
        super().__init__(scene, inputs=[0], outputs=[0])

    def initInnerClasses(self):
        self.content = TtsContent(self)
        self.grNode = VplGraphicsNode(self)
        #self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code
        self.data.id = self.id

    def doEval(self, input=None):
        self.data = input
        return self.data