from PyQt5.QtCore import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode

class PrintLineNodeContent(VplContent):
    def initUI(self):
        self.label = QLabel("Print Line", self)
    
    #I hope these are correct
    def serialize(self):
        res = super().serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        return res


class PrintLineNode(VplNode):
    op_code = OP_CODE_PRINT_LINE
    op_title = "Print Line"
    content_label_objname = "VplNodePrint"

    def __init__(self, scene, title:str="Print Line"):
        super().__init__(scene, title, inputs = [1], outputs = [1])
        self.eval()

    def initInnerClasses(self):
        self.content = PrintLineNodeContent(self)
        self.grNode = VplGraphicsNode(self)
        #self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code
        self.data.id = self.id

    def nodeDataValtoString(self, input):
        rString = ""
        if(input == None):
            rString = "ERROR: Null value passed to PrintLine node."
        else:
            if(isinstance(input, dict)):
                for j, k in input.items():
                    rString = rString + j + ': ' + k + '\n'
            else:
                rString = str(input)
        return rString
    
    def doEval(self, parentData=None):
        msg = self.nodeDataValtoString(parentData.val)
        self.data.messages.append(msg)

