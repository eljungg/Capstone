from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base
from conf import *
import time

from model.node_data import *


class timerNodeContent(VplContent):
    def initUI(self):
        self.label = QLabel("timer", self)

    def serialize(self):
        res = super().serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        return res

class timerNode(VplNode):
    icon = 'icons\merge.png'
    op_code = OP_CODE_timer
    op_title = 'timer'
    content_label_objname = 'VplMergeNode'

    def initSettings(self):
        super().initSettings()
        self.input_multi_edged = True

    def __init__(self, scene, title: str = "timer"):
        super().__init__(scene, title, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = timerNodeContent(self)
        self.grNode = VplGraphicsNode(self)
        self.data = NodeData()
        self.data.nodeType = self.op_code

    def doEval(self, input=None):
        parentData = input;
        time.sleep(int(parentData.val)/1000)