from PyQt5.QtCore import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode

class BreakNodeContent(VplContent):
    def initUI(self):
        self.label = QLabel("Break", self)
    
    def serialize(self):
        res = super().serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        return res


class BreakNode(VplNode):
    # Set the opcode, title, and content label
    op_code = OP_CODE_BREAK
    op_title = "Break"
    content_label_objname = "VplNodeBreak"

    def __init__(self, scene, title:str="Break"):
        super().__init__(scene, title, inputs = [0], outputs = [0])

    def initInnerClasses(self):
        self.content = BreakNodeContent(self)
        self.grNode = VplGraphicsNode(self)
        self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code
        self.data.id = self.id
    
    # Used in vpl_execution.py and is the common function name among the nodes
    def doEval(self, parentData=None):
        self.data.val = parentData.val
        return
