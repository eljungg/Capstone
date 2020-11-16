from nodeeditor.node_editor_widget import NodeEditorWidget
from PyQt5.QtCore import *
from conf import *
from PyQt5.QtGui import *
#from ..nodeeditor.node_node import Node # call LOCAL version of Node class
from vpl_node import VplNode # get over-ridedd node
from nodes.variable_node import VariableNode # get our node sub classes
from nodes.if_node import IfNode
from nodes.join_node import JoinNode
from nodes.data_node import DataNode
from nodes.calculate_node import CalculateNode
from nodes.merge_node import MergeNode
from model.variables import VariablesData


class SubWindow(NodeEditorWidget):
    """This is a sub-window, the grey plot for placing nodes on """
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitle()

        self.scene.addHasBeenModifiedListener(self.setTitle)
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)

        self._close_event_listeners = []
        self.variables = VariablesData() # each "scene" or "subwindow" has a "global" Variables data list

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())
        
    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)

    def onDragEnter(self, event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            event.setAccepted(False)
        

    
    def onDrop(self, event): #Finish startDrag started in dra_list_box.py
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readInt()
            text = dataStream.readQString()

            mouse_position = event.pos()
            scene_position = self.scene.grScene.views()[0].mapToScene(mouse_position)

            print("GOT DROP: [%d] '%s' " % (op_code, text), 'mouse: ', mouse_position, 'scene: ', scene_position)

            node = self.setNodeType(text, op_code)
            
            node.setPos(scene_position.x(), scene_position.y())
            self.scene.addNode(node)

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
    def setNodeType(self , text , op_code): 

        if(op_code == OP_CODE_VARIABLE):
            node =  VariableNode(self.scene , self.variables) # Variable node gets reference to global(subWindow) variables object
            node.title = "Variable Node"
            
        elif op_code == OP_CODE_CALCULATE:
            node = CalculateNode(self.scene)
            node.title="Calculate Node"

        elif op_code == OP_CODE_DATA:
            node = DataNode(self.scene)
            node.title = "Data Node"

        elif op_code == OP_CODE_MERGE:
            node = DataNode(self.scene)
            node.title = "Merge Node"
        elif(op_code == OP_CODE_IF):
            print("adding if node.")
            node = IfNode(self.scene)
            node.title = "If Node"
        elif(op_code == OP_CODE_JOIN):
            print("adding join node.")
            node = JoinNode(self.scene)
            node.title = "Join Node"
            
        else:
            node =  VplNode(self.scene,  text, inputs=[1,1], outputs=[2])

        return node # give the node back
