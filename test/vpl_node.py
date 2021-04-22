from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_socket import *
from nodeeditor.node_edge import *
from vpl_socket import *
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
        self.title_height = 30
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 32

    def initAssets(self):
        super().initAssets()

        # Set the color of the node outline
        self._brush_title = QBrush(QColor("#FF000000"))
        self._brush_background = QBrush(QColor("#FF000000"))

    # Used to change the shape of the node - no changes needed but supplied just in case
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

#Over-Ride the content (gui) stuff of our node
class VplContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)

#Over-ride of node class for our purposes
class VplNode(Node):
    GraphicsNode_class = VplGraphicsNode
    NodeContent_class = VplContent
    Socket_class = VplSocket
    #data = NodeData() # hold our data model for this node
    op_code = 0

    content_label = ""
    content_label_objname = "calc_node_bg"
    def __init__(self, scene:'Scene', title:str="Undefined Node", inputs:list=[], outputs:list=[]):
        self.data = NodeData()
        super().__init__(scene, title, inputs, outputs)

        print("Running: " + title)

        self.newSockets(inputs, outputs)
        
        print("Over-rided node class goes!")

    def initSettings(self):
        super().initSettings()

        self.socket_spacing = 43

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

    # Changes the number of sockets to the supplied amount
    def newSockets(self, inputs: list, outputs: list, reset: bool=True):
        inputEdges = []
        outputEdges = []

        # Reset the sockets if 'true'
        if reset:
            # Clear old sockets
            if hasattr(self, 'inputs') and hasattr(self, 'outputs'):
                # Remove the input sockets from scene
                for socket in (self.inputs):
                    inputSockets = []

                    # Keep track of the connected edges
                    for edge in socket.edges:
                        inputSockets.append(edge.getOtherSocket(socket))

                    # Add the edges based on the socket
                    inputEdges.append(inputSockets)

                    # Remove the input sockets
                    self.scene.grScene.removeItem(socket.grSocket)
                    socket.removeAllEdges()

                # Remove the output sockets from scene
                for socket in (self.outputs):
                    outputSockets = []

                    # Keep track of the connected edges
                    for edge in socket.edges:
                        outputSockets.append(edge.getOtherSocket(socket))

                    # Add the edges based on the socket
                    outputEdges.append(outputSockets)
                    
                    # Remove the output sockets
                    self.scene.grScene.removeItem(socket.grSocket)
                    socket.removeAllEdges()
                self.inputs = []
                self.outputs = []

        # Create new sockets
        counter = 0
        for item in inputs:
            # Create a new socket
            socket = self.__class__.Socket_class(
                node=self, index=counter, position=LEFT_CENTER,
                socket_type=item, multi_edges=self.input_multi_edged,
                count_on_this_node_side=len(inputs), is_input=True
            )

            # Reconnect the edges
            if(counter < len(inputEdges)):       
                for edge in inputEdges[counter]:
                    newEdge = Edge(self.scene, edge, socket, EDGE_TYPE_BEZIER)

            counter += 1

            # Add the socket
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            # Create a new socket
            socket = self.__class__.Socket_class(
                node=self, index=counter, position=self.output_socket_position,
                socket_type=item, multi_edges=self.output_multi_edged,
                count_on_this_node_side=len(outputs), is_input=False
            )

            # Reconnect the edges (used for the if/else if sockets of the If node)
            if(counter < len(outputEdges) - 1):   
                if(len(outputs) < len(outputEdges)):
                    if(counter != len(outputEdges) - 2):
                        for edge in outputEdges[counter]:
                            newEdge = Edge(self.scene, socket, edge, EDGE_TYPE_BEZIER)
                else:
                    for edge in outputEdges[counter]:
                        newEdge = Edge(self.scene, socket, edge, EDGE_TYPE_BEZIER)

            # Reconnect the edges (used for the else socket of the If node)
            if(counter == len(outputs) - 1):
                for edge in outputEdges[-1]:
                    newEdge = Edge(self.scene, socket, edge, EDGE_TYPE_BEZIER)

            counter += 1

            # Add the socket
            self.outputs.append(socket)
        
        self.updateConnectedEdges()

    # Used to calculate where sockets should be placed
    def getSocketPosition(self, index, position, num_out_of=1):
        # Get the position of the sockets
        xy = super().getSocketPosition(index, position, num_out_of)

        # Adjust the positions to fit the nodes better
        x = -17 if (position in (LEFT_TOP, LEFT_CENTER, LEFT_BOTTOM)) else 10
        xy[0] = xy[0] + x

        return xy


    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized VplCNode '%s'" % self.__class__.__name__, "res:", res)
        return res
