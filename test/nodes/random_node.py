from PyQt5.QtCore import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode
from model.node_data import NodeData
from random import *

class RandomNodeContent(VplContent):
    def initUI(self):
        self.label = QLabel("Random", self)
    
    #I hope these are correct
    def serialize(self):
        res = super().serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        return res


class RandomNode(VplNode):
    op_code = OP_CODE_RANDOM
    op_title = "Random"
    content_label_objname = "VplNodeRandom"

    def __init__(self, scene, title:str="Random"):
        super().__init__(scene, title, inputs = [0], outputs = [0])
        self.eval()

    def initInnerClasses(self):
        self.content = RandomNodeContent(self)
        self.grNode = VplGraphicsNode(self)
        self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code
        self.data.id = self.id
    
    def doEval(self, input=None):
        self.data.val = randint(0, int(input.val) - 1)
        self.data.valType = TYPE_INT
        return

