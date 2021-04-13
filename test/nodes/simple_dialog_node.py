from PyQt5.QtCore import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode

# class SimpleDialogNodeContent(VplContent):
class SimpleDialogContent(QDMNodeContentWidget):
    def initUI(self):
        self.vBox = QVBoxLayout()
        self.label = QLabel("Simple Dialog", self)
        self.label.setAlignment(Qt.AlignCenter) # does nothing
        self.vBox.addWidget(self.label)
        self.setLayout(self.vBox)
    
    #I hope these are correct
    def serialize(self):
        res = super().serialize()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        return res


class SimpleDialogNode(VplNode):
    op_code = OP_CODE_SIMPLE_DIALOG
    op_title = "Simple Dialog"
    content_label_objname = "VplNodeDialog"

    def __init__(self, scene, title:str="Simple Dialog"):
        super().__init__(scene, title, inputs = [1], outputs = [1])
        self.eval()

    def initInnerClasses(self):
        self.content = SimpleDialogContent(self)
        self.grNode = VplGraphicsNode(self)
        #self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code
        self.data.id = self.id

    def doEval(self, input=None):
        usrMsg = input.val
        dialog = AlertDialog(None , usrMsg)
        dialog.exec_() # current implementation locks the thread until user OK's

class AlertDialog(QDialog):
    def __init__(self, parent , userMessage):
        super().__init__(parent=parent )
        self.setWindowTitle("Simple Dialog")
        self.dialogButtons = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(self.dialogButtons)
        self.buttonBox.accepted.connect(self.accept)
        self.userAlert = QLabel(userMessage)
        self.userAlert.setAlignment(Qt.AlignCenter)

        self.box = QVBoxLayout()
        self.box.addWidget(self.userAlert)
        self.box.addWidget(self.buttonBox)
        self.setLayout(self.box)
        
