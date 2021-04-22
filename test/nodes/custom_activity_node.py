from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode
from vpl_scene import VplScene

# TODO: Change node to look and function similar to variable node.
# TODO: Fix deserialize to give the scene the getNodeClass() function from Subwindow/CustomActivityWindow
# Currently the loaded scene in this node has no way to figure out the class of the node from opcode and tries to
# create the default node and crashes. 
# TODO: Addition of data connections.

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
            print("scene to save not found")
            res['scene'] = None
        else:
            print("saving scene")
            res['scene'] = self.innerScene.serialize()
        #save internal scene
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            name = data['name']
            scene = data['scene']
            self.name.setText(name)
            tempScene = VplScene()
            tempScene.deserialize(scene)
            #self.innerScene.deserialize(scene)
            self.innerScene = tempScene
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
        # try catch blocks. The nodeeditor cannot tell if the custom activity window was closed.
        # Trying to open it again will crash the program without these blocks. Feel free to 
        # clean this section up if you can.
        if(self.scene.windowRef != None):
            print("window ref found")
            if self.innerSubwindow == None:
                print("subwindow not found")
                if(self.content.innerScene == None):
                    print("innerScene not found. creating new scene")
                    self.innerSubwindow = self.scene.windowRef.createCAWindow(self).widget()
                    self.content.innerScene = self.innerSubwindow.getScene()
                    self.innerInput = self.innerSubwindow.getInputNode()
                else:
                    print("innerscene found. attempting to show subwindow")
                    try:
                        self.innerSubwindow.show()
                    except:
                        print("subwindow failed to open. creating new window")
                        self.innerSubwindow = self.scene.windowRef.createCAWindow(self, self.content.innerScene).widget()
                        print("number of nodes in scene: " + str(len(self.content.innerScene.nodes)))
                        self.innerInput = self.innerSubwindow.getInputNode()
                        self.innerSubwindow.show()
            else:
                print("subwindow found. attempting to show")
                try:
                    self.innerSubwindow.show()
                except:
                    print("subwindow could not be shown. creating new subwindow")
                    self.innerSubwindow = self.scene.windowRef.createCAWindow(self, self.content.innerScene).widget()
                    print("number of nodes in scene: " + str(len(self.content.innerScene.nodes)))
                    self.innerInput = self.innerSubwindow.getInputNode()
                    self.innerSubwindow.show()

        else:
            print("failure")
        print("button pressed")

    def doEval(self, input=None):
        pass
            
