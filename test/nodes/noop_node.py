from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base
from conf import *

from model.node_data import *


class NoOPNodeContent(VplContent):
    def initUI(self):
        self.label = QLabel("NOP", self)

    def serialize(self):
        res = super().serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        return res

class NoOPNode(VplNode):
    icon = 'icons\merge.png'
    op_code = OP_CODE_NOOP
    op_title = 'NoOP'
    content_label_objname = 'VplNoOPNode'

    def __init__(self, scene, title: str = "NoOP",inputs=[1], outputs=[1], CAParent:'VplNode'=None):
        super().__init__(scene, title, inputs, outputs)
        self.eval()
        self.CAParent = CAParent

    def initInnerClasses(self):
        self.content = NoOPNodeContent(self)
        self.grNode = VplGraphicsNode(self)
        #self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code
        self.data.id = self.id

    def doEval(self, input=None):
        self.data = input
        return self.data

class CAOutNode(NoOPNode):
    icon = 'icons\merge.png'
    op_code = OP_CODE_CAOUT
    op_title = 'NoOP'
    content_label_objname = 'VplNoOPNode'

    def __init__(self, scene, title: str = "NoOP",inputs=[1], outputs=[], CAParent:'VplNode'=None):
        super().__init__(scene, title, inputs, outputs, CAParent)

    def doEval(self, input=None):
        self.data = input
        return self.data