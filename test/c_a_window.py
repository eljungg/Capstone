from vpl_scene import VplScene
from nodeeditor.node_graphics_view import QDMGraphicsView
from sub_window import SubWindow
from nodes.noop_node import NoOPNode

class CustomActivityWindow(SubWindow):
    Scene_class = VplScene
    GraphicsView_class = QDMGraphicsView
    def __init__(self, enclosingWindow):
        super().__init__(enclosingWindow)
        self.addInOutNodes()

    def addInOutNodes(self):
        #The node passing input to the custom activity.
        nodeIn = NoOPNode(self.scene, "Input", inputs=[], outputs=[1]) 
        #The node passing output from the custom activity.
        nodeOut = NoOPNode(self.scene, "Output", inputs=[1], outputs=[])
        #The node passing output event from the custom activity.
        nodeOutE = NoOPNode(self.scene, "EventOut", inputs=[1], outputs=[])

        nodeIn.setPos(-500, 0)
        nodeOut.setPos(500, 0)
        nodeOutE.setPos(500, 100)