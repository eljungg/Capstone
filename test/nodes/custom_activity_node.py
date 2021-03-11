from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode
from vpl_scene import VplScene

class CustomActivityContent(VplContent):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.button = QPushButton("Edit", self)

        self.layout.addWidget(self.button)
        #To imitate VIPLE we'll want to implement a way to add extra
        #fields. probably another function and graphics
    
    #I hope these are correct
    def serialize(self):
        res = super().serialize()
        #save internal scene
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            #restore internal scene
            return True & res
        except Exception as e:
            dumpException(e)
        return res


class CustomActivityNode(VplNode):
    icons = "icons/in.png"
    op_code = OP_CODE_CUSTOM_ACTIVITY
    op_title = "Custom Activity"
    content_label_objname = "VplNodeCustomActivity"
    content_label_objname2 = "VplNodeCustomActivity"

    def __init__(self, scene, title:str="Custom Activity"):
        super().__init__(scene, title, inputs = [1], outputs = [1])
        self.eval()

    def initInnerClasses(self):
        self.content = CustomActivityContent(self)
        self.grNode = VplGraphicsNode(self)
        self.content.button.clicked.connect(self.buttonClicked)
        self.data.nodeType = self.op_code
        self.data.id = self.id
        self.innerScene = None
        self.innerSubwindow = None

    def buttonClicked(self):
        if(self.scene.windowRef != None):
            self.innerSubwindow = self.scene.windowRef.createMdiChild().widget()
            self.innerScene = self.innerSubwindow.getScene()
        else:
            print("failure")
        print("button pressed")

    def doEval(self, input=None):
        pass
            
