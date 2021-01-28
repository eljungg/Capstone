from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode
from model.node_data import NodeData

class JoinNodeContent(VplContent):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.conditional1 = QLineEdit("", self)
        self.conditional1.setAlignment(Qt.AlignLeft)
        self.conditional1.setObjectName(self.node.content_label_objname)
        self.conditional2 = QLineEdit("", self)
        self.conditional2.setAlignment(Qt.AlignLeft)
        self.conditional2.setObjectName(self.node.content_label_objname2)

        self.layout.addWidget(self.conditional1)
        self.layout.addWidget(self.conditional2)
        #To imitate VIPLE we'll want to implement a way to add extra
        #fields. probably another function and graphics
    
    #I hope these are correct
    def serialize(self):
        res = super().serialize()
        res['value1'] = self.conditional1.text()
        res['value2'] = self.conditional2.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value1 = data['value1']
            value2 = data['value2']
            self.conditional1.setText(value1)
            self.conditional2.setText(value2)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


class JoinNode(VplNode):
    icons = "icons/in.png"
    op_code = OP_CODE_JOIN
    op_title = "Join"
    content_label_objname = "VplNodeJoin"
    content_label_objname2 = "VplNodeJoin"

    def __init__(self, scene, title:str="Join"):
        super().__init__(scene, title, inputs = [1, 1], outputs = [1])
        self.eval()

    def initInnerClasses(self):
        self.content = JoinNodeContent(self)
        self.grNode = VplGraphicsNode(self)
        self.content.conditional1.textChanged.connect(self.onInputChanged)
        self.content.conditional2.textChanged.connect(self.onInputChanged)
        self.data = NodeData() # THIS FIXES SCOPING ISSUE
    
    #def evalImplementation():
    #May use in the future for syntax checking. Not needed for compilation



