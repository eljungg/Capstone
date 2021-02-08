from PyQt5.QtCore import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode

class SimpleDialogNodeContent(VplContent):
    def initUI(self):
        self.label = QLabel("Simple Dialog", self)
    
    #I hope these are correct
    def serialize(self):
        res = super().serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        return res


class SimpleDialogNode(VplNode):
    op_code = OP_CODE_SIMPLE_DIALOG
    op_title = "Simple Dialog"
    content_label_objname = "VplNodeDialog"

    def __init__(self, scene, title:str="Simple Dialog"):
        super().__init__(scene, title, inputs = [1], outputs = [1])
        self.eval()

    def initInnerClasses(self):
        self.content = SimpleDialogNodeContent(self)
        self.grNode = VplGraphicsNode(self)
        self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code

    def doEval(self, input=None):
        if(input == None):
            print("ERROR, no value given to simple dialog")
        return None