from PyQt5.QtCore import *

from vpl_conf import *
from vpl_node_base import *

from nodeeditor.utils import dumpException

class VPLMergeContent(QDMNodeContentWidget):
    def initUI(self):
        pass

@register_node(OP_NODE_MERGE)
class VPLNode_Merge(VPLNode):
    icon = 'icons/merge.png'
    op_code = OP_NODE_MERGE
    op_title = 'Merge'
    content_label_objname = 'vpl_node_merge'

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = VPLMergeContent(self)
        self.grNode = VPLGraphicsNode(self)
        self.grNode.edge_roundness = 22
        self.grNode.width = 60
        self.grNode.height = 60
        self.grNode.title_vertical_padding = 5