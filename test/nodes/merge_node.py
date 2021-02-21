from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base
from conf import *

from model.node_data import *


class MergeNodeContent(VplContent):
    def initUI(self):
        self.label = QLabel("Merging", self)

    def serialize(self):
        res = super().serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        return res

class MergeNode(VplNode):
    icon = 'icons\merge.png'
    op_code = OP_CODE_MERGE
    op_title = 'Merge'
    content_label_objname = 'VplMergeNode'

    def initSettings(self):
        super().initSettings()
        self.input_multi_edged = True

    def __init__(self, scene, title: str = "Merge"):
        super().__init__(scene, title, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = MergeNodeContent(self)
        self.grNode = VplGraphicsNode(self)

    def doEval(self, input=None):
        self.data = input
        return self.data