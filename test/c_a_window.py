from vpl_scene import VplScene
from nodeeditor.node_graphics_view import QDMGraphicsView
from sub_window import SubWindow
from nodes.noop_node import NoOPNode, CAOutNode
from conf import *

class CustomActivityWindow(SubWindow):
    Scene_class = VplScene
    GraphicsView_class = QDMGraphicsView
    def __init__(self, enclosingWindow, CANode=None, scene=None):
        super().__init__(enclosingWindow)
        self.CANode = CANode
        #if(scene == None):
        self.nodeIn = NoOPNode(self.scene, "Input", [], [1], self.CANode) #The node passing input to the custom activity.
        self.nodeOut = CAOutNode(self.scene, "Output", [1], [], self.CANode) #The node passing output from the custom activity.
        self.nodeOutE = NoOPNode(self.scene, "EventOut", [1], [], self.CANode) #The node passing output event from the custom activity.
        self.nodeIn.setPos(-500, 0)
        self.nodeOut.setPos(500, 0)
        self.nodeOutE.setPos(500, 100)
        if(scene != None): #else:
            self.scene = scene
            for n in self.scene.nodes:
                if(n.op_code == OP_CODE_CAOUT):
                    print("node out found")
                    self.nodeOut = n
                elif(n.op_code == OP_CODE_NOOP):
                    if(n.title == "Input"):
                        print("input found")
                        self.nodeIn == n
            viewTemp = self.view
            self.view = self.__class__.GraphicsView_class(self.scene.grScene, self)
            self.layout.replaceWidget(viewTemp, self.view)
            #self.layout.addWidget(self.view)
            #self.nodeIn.setPos(-500, 0)
            #self.nodeOut.setPos(500, 0)

    def getInputNode(self):
        print('returning input node')
        return self.nodeIn

    def showScene(self):
        for n in self.scene.nodes:
            n.content.show()
        #for e in self.scene.edges:
            #e.show()

    def setScene(self, scene):
        print("setting scene")
        self.scene = scene
        for n in self.scene.nodes:
            if(n.op_code == OP_CODE_CAOUT):
                print("node out found")
                self.nodeOut = n
            elif(n.op_code == OP_CODE_NOOP):
                if(n.title == "Input"):
                    print("input found")
                    self.nodeIn == n
            