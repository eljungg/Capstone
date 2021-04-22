from PyQt5.QtCore import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode

class EndWhileNodeContent(VplContent):
    def initUI(self):
        self.label = QLabel("End While", self)
    
    #I hope these are correct
    def serialize(self):
        res = super().serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        return res


class EndWhileNode(VplNode):
    op_code = OP_CODE_END_WHILE
    op_title = "End While"
    content_label_objname = "VplNodeEndWhile"

    def __init__(self, scene, title:str="End While"):
        super().__init__(scene, title, inputs = [1], outputs = [1])
        self.eval()

    def initInnerClasses(self):
        self.content = EndWhileNodeContent(self)
        self.grNode = VplGraphicsNode(self)
        #self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code
        self.data.id = self.id

    def nodeDataValtoString(self, input=None):
        rString = ""
        if(input == None):
            rString = "ERROR: Null value passed to End While node."
        else:
            if(isinstance(input, list)):
                for s in input:
                    rString = rString + str(s) + '\n'
            else:
                rString = str(input)
        return rString
    
    def doEval(self, parentData=None):
        msg = self.nodeDataValtoString(parentData.val)
        self.data.messages.append(msg)

