from PyQt5.QtCore import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode

class EndWhileNodeContent(VplContent):
    def initUI(self):
        self.label = QLabel("End While", self)
    
    def serialize(self):
        res = super().serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        return res


class EndWhileNode(VplNode):
    # Set the opcode, title, and content label
    op_code = OP_CODE_END_WHILE
    op_title = "End While"
    content_label_objname = "VplNodeEndWhile"

    def __init__(self, scene, title:str="End While"):
        super().__init__(scene, title, inputs = [0], outputs = [0])

    def initInnerClasses(self):
        self.content = EndWhileNodeContent(self)
        self.grNode = VplGraphicsNode(self)
        self.data = NodeData()
        self.data.nodeType = self.op_code
        self.data.id = self.id

    # Used in vpl_execution.py and is the common function name among the nodes
    def doEval(self, parentData=None):
        self.data.val = parentData.val
        return

