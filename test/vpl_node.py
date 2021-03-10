from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_socket import *
from nodeeditor.utils import dumpException
from model.node_data import NodeData

#test
#Over-ride the Graphics of our Node
class VplGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        #self.icons = QImage("icons/status_icons.png")

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0

        # painter.drawImage(
        #     QRectF(-10, -10, 24.0, 24.0),
        #     #self.icons,
        #     QRectF(offset, 0, 24.0, 24.0)
        # )
#Over-Ride the content (gui) stuff of our node
class VplContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)

#Over-ride of node class for our purposes
class VplNode(Node):
    GraphicsNode_class = VplGraphicsNode
    NodeContent_class = VplContent
    #data = NodeData() # hold our data model for this node
    op_code = 0

    content_label = ""
    content_label_objname = "calc_node_bg"
    def __init__(self, scene:'Scene', title:str="Undefined Node", inputs:list=[], outputs:list=[]):
        self.data = NodeData()
        super().__init__(scene , title , inputs, outputs)

        self.newSockets(inputs, outputs)
        
        print("Over-rided node class goes!")

    def onDeserialized(self, data=None):
        self.data.id = self.id

    #eval statment for our execution engine
    def doEval(self, input=None):
        """Evaluation statement for our execution engine. May replace later with normal eval provided by `nodeeditor`."""
        return None

    def findParentFromSocket(self, pid):
        """Allows a node to determine which socket the parent is connected to based on id in NodeData. id of parent node as argument. Used for join"""
        i = 0
        for socket in self.inputs: #loop through inputs of the node
            e = socket.edges[0] #only merge should take multiple inputs on a socket, get the only edge connected to the input
            parent = e.getOtherSocket(socket).node

            if(parent.id == pid):
                return i #returns the socket's postition in the list
            i = i + 1

    def newSockets(self, inputs: list, outputs: list, reset: bool=True):

        if reset:
            # clear old sockets
            if hasattr(self, 'inputs') and hasattr(self, 'outputs'):
                # remove grSockets from scene
                for socket in (self.inputs+self.outputs):
                    self.scene.grScene.removeItem(socket.grSocket)
                    socket.removeAllEdges()
                self.inputs = []
                self.outputs = []

        # create new sockets
        counter = 0
        for item in inputs:
            socket = self.__class__.Socket_class(
                node=self, index=counter, position=LEFT_CENTER,
                socket_type=item, multi_edges=self.input_multi_edged,
                count_on_this_node_side=len(inputs), is_input=True
            )
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = self.__class__.Socket_class(
                node=self, index=counter, position=self.output_socket_position,
                socket_type=item, multi_edges=self.output_multi_edged,
                count_on_this_node_side=len(outputs), is_input=False
            )
            
            counter += 1
            self.outputs.append(socket)

        
        '''
        if(len(inputs) != len(self.inputs)):
            counter = 0
            for item in inputs:
                socket = self.__class__.Socket_class(
                    node=self, index=counter, position=self.input_socket_position,
                    socket_type=item, multi_edges=self.input_multi_edged,
                    count_on_this_node_side=len(inputs), is_input=True
                )
                counter += 1
                self.inputs.append(socket)

        if(len(outputs) != len(self.outputs)):
            if(AddOrSub):
                counter = 0
                for item in outputs:
                    socket = self.__class__.Socket_class(
                        node=self, index=counter, position=self.output_socket_position,
                        socket_type=item, multi_edges=self.output_multi_edged,
                        count_on_this_node_side=len(outputs), is_input=False
                    )
                    if(counter == len(outputs) - 2):
                        self.outputs.insert(counter, socket)
                    elif(counter == len(outputs) - 1):
                        self.outputs[counter].index=counter
                        self.outputs[counter].setSocketPosition=RIGHT_BOTTOM

                        if(self.outputs[counter].hasAnyEdge()):
                            self.outputs[counter].removeAllEdges()
                        
                    counter += 1
            else:
                for socket in self.outputs:
                    if(socket.index == len(self.outputs) - 2):
                        socket.delete()
                        self.outputs.pop(-2)
        '''

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized VplCNode '%s'" % self.__class__.__name__, "res:", res)
        return res
