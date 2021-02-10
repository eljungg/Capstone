from nodeeditor.node_editor_widget import NodeEditorWidget
from PyQt5.QtCore import *
from conf import *
from PyQt5.QtGui import *
from vpl_scene import VplScene
#from ..nodeeditor.node_node import Node # call LOCAL version of Node class
from vpl_node import VplNode # get over-ridedd node
from nodes.variable_node import VariableNode # get our node sub classes
from nodes.if_node import IfNode
from nodes.join_node import JoinNode
from nodes.data_node import DataNode
from nodes.calculate_node import CalculateNode
from nodes.merge_node import MergeNode
from nodes.print_line_node import PrintLineNode
from nodes.simple_dialog_node import SimpleDialogNode
from nodes.terminal_print_node import TerminalPrintNode
from model.variables import VariablesData


class SubWindow(NodeEditorWidget):
    Scene_class = VplScene
    """This is a sub-window, the grey plot for placing nodes on """
    def __init__(self):
        
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitle()

        self.scene.addHasBeenModifiedListener(self.setTitle)
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)
        #passes the function used to determine node type into the deseriazation process
        self.scene.setNodeClassSelector(self.getNodeClass)

        self._close_event_listeners = []
        self.variables = VariablesData() # each "scene" or "subwindow" has a "global" Variables data list

    def getNodeClass(self, data):
        #scan through op codes
        #return a class based on op code
        if 'op_code' not in data: 
            return VplNode
        elif data['op_code'] == 7:
            return VariableNode
        elif data['op_code'] == 8: return CalculateNode
        elif data['op_code'] == 9: return DataNode
        elif data['op_code'] == 10: return MergeNode
        elif data['op_code'] == 11: return IfNode
        elif data['op_code'] == 12: return JoinNode
        elif data['op_code'] == 49: return TerminalPrintNode
        elif data['op_code'] == 50: return PrintLineNode
        elif data['op_code'] == 51: return SimpleDialogNode
        
        return VplNode

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
            #self.scene.addNode(node)

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def doEvalOutputs(self):
        # eval all output nodes
        for node in self.scene.nodes:
            if node.__class__.__name__ == "CalcNode_Output":
                node.eval()

    def onHistoryRestored(self):
        self.doEvalOutputs()

    def fileLoad(self, filename):
        if super().fileLoad(filename):
            self.doEvalOutputs()
            return True

        return False
    
    def setNodeType(self , text , op_code): 

        if(op_code == OP_CODE_VARIABLE):
            node =  VariableNode(self.scene) # Variable node gets reference to global(subWindow) variables object
            node.setVariableData(self.variables)
            node.content.reDrawVariablesDropDown() #dropdown of variables has to be drawn after .setVariableData above, other wise would do this inside of node
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
        elif(op_code == OP_CODE_PRINT_LINE):
            print("adding print line node.")
            node = PrintLineNode(self.scene)
            #node.title = "Join Node"
        elif(op_code == OP_CODE_SIMPLE_DIALOG):
            print("adding simple dialog node node.")
            node = SimpleDialogNode(self.scene)
            #node.title = "Join Node"
        elif(op_code == OP_CODE_TERMINAL_PRINT):
            print("adding terminal print node.")
            node = TerminalPrintNode(self.scene)
        else:
            node =  VplNode(self.scene,  text, inputs=[1,1], outputs=[2])

        return node # give the node back
