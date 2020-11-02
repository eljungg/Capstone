from nodeeditor.node_editor_widget import NodeEditorWidget
from PyQt5.QtCore import *
from Capstone.test.conf import *
from PyQt5.QtGui import *
from ..nodeeditor.node_node import Node # call LOCAL version of Node class


class SubWindow(NodeEditorWidget):
    """This is a sub-window, the grey plot for placing nodes on """
    def __init__(self):
        print("Dark Grey Node Plot Created!")
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitle()

        self.scene.addHasBeenModifiedListener(self.setTitle)
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)

        self._close_event_listeners = []


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

            node = Node(self.scene,  text, inputs=[1,1], outputs=[2]) # this actually creates the "nodes"
            self.setNodeType(node=node , op_code=op_code)# Handle specific node types
            
            node.setPos(scene_position.x(), scene_position.y())
            self.scene.addNode(node)

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
    def setNodeType(self , node , op_code): 
        #We need to get a reference to our model object in here somehow
        ###Take a newly created node object, and its opcode, inners###
        node.data.setNodeType = op_code # set type fo any node
        if op_code == OP_CODE_VARIABLE:
            node.title="Variable Node"
            node.content.wdg_label.setText("Variable")
            node.grNode._color = QColor("#6cff51") # so this dont work
            node.data.print()
            #TODO, access the node.content and set color
        if op_code == OP_CODE_CALCULATE:
            node.title="Calculate Node"
            node.content.wdg_label.setText("Calculate")
        if op_code == OP_CODE_DATA:
            node.title = "Data Node"
            node.content.wdg_label.setText("Data")
        if op_code == OP_CODE_MERGE:
            node.title = "Merge Node"
            node.content.wdg_label.setText("Merge")