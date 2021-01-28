from PyQt5.QtCore import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode
from model.node_data import NodeData

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
        self.data = NodeData() # THIS FIXES SCOPING ISSUE, 
    def doActivity(self): #Print Line Node Do Activity!
        print("\n*****Im a Print Line Node, doing my Activity!")
        print("You can access all my attributes through thisnode.data!")
        print("I Dont have any data! Oops! We need to get that data from my PARENT node. How do we do that?")
        print("This function returns nothing! but it could do whatever you wanted!*****\n")
    
