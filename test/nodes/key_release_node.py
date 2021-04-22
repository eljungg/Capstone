import threading
from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base
from conf import *
from pynput.keyboard import Key, Listener
from model.node_data import *
from vpl_execution import *
from conf import *

class keyReleaseNodeContent(VplContent):
    def initUI(self):
        self.label = QLabel("Key Release Event", self)

    def serialize(self):
        res = super().serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        return res

class KeyReleaseNode(VplNode):
    icon = 'icons\merge.png'
    op_code = OP_CODE_KEYRELEASE
    op_title = 'Merge'
    content_label_objname = 'VplMergeNode'

    def initSettings(self):
        super().initSettings()
        self.input_multi_edged = True

    def __init__(self, scene, title: str = "Key Release"):
        super().__init__(scene, title, inputs=[], outputs=[2])
        self.eval()

    def initInnerClasses(self):
        self.content = keyReleaseNodeContent(self)
        self.grNode = VplGraphicsNode(self)