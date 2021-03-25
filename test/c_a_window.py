from vpl_scene import VplScene
from nodeeditor.node_graphics_view import QDMGraphicsView
from sub_window import SubWindow
from nodes.noop_node import NoOPNode, CAOutNode
from conf import *

class CustomActivityWindow(SubWindow):
    Scene_class = VplScene
    GraphicsView_class = QDMGraphicsView
    def __init__(self, enclosingWindow, CANode=None):
        super().__init__(enclosingWindow)
        self.CANode = CANode
        self.nodeIn = NoOPNode(self.scene, "Input", [], [1], self.CANode) #The node passing input to the custom activity.
        self.nodeOut = CAOutNode(self.scene, "Output", [1], [], self.CANode) #The node passing output from the custom activity.
        self.nodeOutE = NoOPNode(self.scene, "EventOut", [1], [], self.CANode) #The node passing output event from the custom activity.
        self.nodeIn.setPos(-500, 0)
        self.nodeOut.setPos(500, 0)
        self.nodeOutE.setPos(500, 100)

    def getInputNode(self):
        return self.nodeIn

    def setScene(self, scene):
        self.scene = scene
        for n in self.scene.nodes:
            if(n.op_code == OP_CODE_CAOUT):
                self.nodeOut = n
            elif(n.op_code == OP_CODE_NOOP):
                if(n.title == "Input"):
                    self.nodeIn == n
            