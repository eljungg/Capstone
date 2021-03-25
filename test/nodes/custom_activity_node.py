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

        self.name = QLineEdit("", self)
        self.button = QPushButton("Edit", self)

        self.layout.addWidget(self.name)
        self.layout.addWidget(self.button)

        self.innerScene:VplScene = None
        #To imitate VIPLE we'll want to implement a way to add extra
        #fields. probably another function and graphics
    
    #I hope these are correct
    def serialize(self):
        res = super().serialize()
        res['name'] = self.name.text()
        if(self.innerScene == None):
            res['scene'] = None
        else:
            res['scene'] = self.innerScene.serialize()
        #save internal scene
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            name = data['name']
            scene = data['scene']
            self.name.setText(name)
            self.innerScene.deserialize(scene)
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
        self.innerSubwindow = None
        self.innerInput = None

    def buttonClicked(self):
        if(self.scene.windowRef != None):
            print("window ref found")
            if self.content.innerScene == None:
                self.innerSubwindow = self.scene.windowRef.createCAWindow(self).widget()
                self.content.innerScene = self.innerSubwindow.getScene()
                self.innerInput = self.innerSubwindow.getInputNode()
            else:
                if(self.innerSubwindow == None):
                    self.innerSubwindow = self.scene.windowRef.createCAWindow(self).widget()
                    self.innerSubwindow.setScene(self.content.innerScene)

            self.innerSubwindow.show()
        else:
            print("failure")
        print("button pressed")

    def doEval(self, input=None):
        pass
            
