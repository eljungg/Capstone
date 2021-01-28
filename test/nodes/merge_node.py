from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base
from conf import *
from model.node_data import NodeData

class MergeContent(QDMNodeContentWidget):
    def initUI(self):
        pass

class MergeNode(VplNode):
    icon = 'icons\merge.png'
    op_code = OP_CODE_MERGE
    op_title = 'Merge'
    content_label_objname = 'VplMergeNode'

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = VPLMergeContent(self)
        self.grNode = VPLGraphicsNode(self)
        self.data = NodeData() # THIS FIXES SCOPING ISSUE, 
        self.grNode.edge_roundness = 22
        self.grNode.width = 60
        self.grNode.height = 60
        self.grNode.title_vertical_padding = 5