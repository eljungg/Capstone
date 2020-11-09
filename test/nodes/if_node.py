from PyQt5.QtCore import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode

class IfNodeContent(VplContent):
    def initUI(self):
        self.conditional1 = QLineEdit("", self)
        self.conditional1.setAlignment(Qt.AlignLeft)
        self.conditional1.setObjectName(self.node.content_label_objname)
        #To imitate VIPLE we'll want to implement a way to add extra
        #conditionals to simulate else if statements. probably another
        #function and graphics
    
    #I hope these are correct
    def serialize(self):
        res = super().serialize()
        res['value'] = self.conditional1.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.conditional1.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


class IfNode(VplNode):
    icons = "icons/in.png"
    op_code = OP_CODE_IF
    op_title = "If"
    content_label_objname = "VplNodeIf"

    def __init__(self, scene):
        super().__init__(scene, inputs = [1], outputs = [3])
        self.eval()

    def initInnerClasses(self):
        self.content = IfNodeContent(self)
        self.grNode = VplGraphicsNode(self)
        self.content.conditional1.textChanged.connect(self.onInputChanged)
    
    #def evalImplementation
    #May use in the future for syntax checking. Not needed for compilation



