from PyQt5.QtCore import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode
from model.node_data import NodeData

class TerminalPrintContent(VplContent):
    def initUI(self):
        self.label = QLabel("Print Line", self)
    
    #I hope these are correct
    def serialize(self):
        res = super().serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        return res


class TerminalPrintNode(VplNode):
    op_code = OP_CODE_TERMINAL_PRINT
    op_title = "Terminal Print"
    content_label_objname = "VplNodePrint"

    def __init__(self, scene, title:str="Terminal Print"):
        super().__init__(scene, title, inputs = [1], outputs = [1])
        self.eval()

    def initInnerClasses(self):
        self.content = TerminalPrintContent(self)
        self.grNode = VplGraphicsNode(self)
        self.data = NodeData() # THIS FIXES SCOPING ISSUE, 

    def doEval(self, input=None):
        string = ""
        if(input == None):
            string = "ERROR, no value passed to node"
        else:
            string = input
        return string