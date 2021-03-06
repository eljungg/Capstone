from nodeeditor.node_editor_widget import NodeEditorWidget
from nodeeditor.node_graphics_scene import QDMGraphicsScene
from nodeeditor.node_graphics_view import QDMGraphicsView
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
from nodes.switch_node import SwitchNode
from model.variables import VariablesData
from nodes.comment_node import CommentNode
from nodes.timer_node import timerNode
from nodes.custom_activity_node import CustomActivityNode
from nodes.noop_node import NoOPNode
from nodes.tts_node import TtsNode
from nodes.restful_node import RestfulServiceNode
from nodes.code_activity_python_node import CodeActivityPythonNode
from nodes.while_node import WhileNode
from nodes.end_while_node import EndWhileNode
from nodes.break_node import BreakNode
from nodes.key_press_node import KeypressNode
from nodes.key_release_node import KeyReleaseNode
from nodes.random_node import RandomNode

class SubWindow(NodeEditorWidget):
    Scene_class = VplScene
    GraphicsView_class = QDMGraphicsView
    """This is a sub-window, the grey plot for placing nodes on """
    def __init__(self, enclosingWindow):
        
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
        self.enclosingWindow = enclosingWindow
        self.scene.setWindowRef(self.enclosingWindow)

    def getScene(self):
        return self.scene

    def setScene(self, scene):
        self.scene = scene

    def getNodeClass(self, data):
        #scan through op codes
        #return a class based on op code
        if 'op_code' not in data: 
            return VplNode
        elif data['op_code'] == OP_CODE_VARIABLE:
            return VariableNode
        elif data['op_code'] == OP_CODE_CALCULATE: return CalculateNode
        elif data['op_code'] == OP_CODE_DATA: return DataNode
        elif data['op_code'] == OP_CODE_MERGE: return MergeNode
        elif data['op_code'] == OP_CODE_IF: return IfNode
        elif data['op_code'] == OP_CODE_JOIN: return JoinNode
        elif data['op_code'] == OP_CODE_WHILE: return WhileNode
        elif data['op_code'] == OP_CODE_END_WHILE: return EndWhileNode
        elif data['op_code'] == OP_CODE_BREAK: return BreakNode
        elif data['op_code'] == OP_CODE_TERMINAL_PRINT: return TerminalPrintNode
        elif data['op_code'] == OP_CODE_PRINT_LINE: return PrintLineNode
        elif data['op_code'] == OP_CODE_SIMPLE_DIALOG: return SimpleDialogNode
        elif data['op_code'] == OP_CODE_COMMENT: return CommentNode
        elif data['op_code'] == OP_CODE_TIMER: return timerNode
        elif data['op_code'] == OP_CODE_CUSTOM_ACTIVITY: return CustomActivityNode
        elif data['op_code'] == OP_CODE_NOOP: return NoOPNode
        elif data['op_code'] == OP_CODE_REST: return RestfulServiceNode
        elif data['op_code'] == OP_CODE_CODEPY: return CodeActivityPythonNode
        elif data['op_code'] == OP_CODE_KEYPRESS: return KeypressNode
        elif data['op_code'] == OP_CODE_KEYRELEASE: return KeyReleaseNode
        elif data['op_code'] == OP_CODE_RANDOM: return RandomNode
        
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
            node.setVariableData(self.variables)
            node.content.redrawComboBox()
            node.title="Calculate Node"

        elif op_code == OP_CODE_DATA:
            node = DataNode(self.scene)
            node.title = "Data Node"

        elif op_code == OP_CODE_MERGE:
            node = MergeNode(self.scene)
            node.title = "Merge Node"

        elif(op_code == OP_CODE_IF):
            node = IfNode(self.scene)
            node.setVariableData(self.variables)
            node.content.redrawComboBox()
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
            
        elif(op_code == OP_CODE_SWITCH):
            node = SwitchNode(self.scene)
            node.setVariableData(self.variables)
            node.content.redrawComboBox()

        elif (op_code == OP_CODE_COMMENT):
            print("adding comment node.")
            node = CommentNode(self.scene)
        elif (op_code == OP_CODE_TIMER):
            print("adding timer node.")
            node = timerNode(self.scene)
        elif (op_code == OP_CODE_CUSTOM_ACTIVITY):
            print("adding custom activity node.")
            node = CustomActivityNode(self.scene)
        elif(op_code == OP_CODE_TTS):
            print('TTS added!')
            node = TtsNode(self.scene)
            node.title = 'TTS Node'
        elif(op_code == OP_CODE_REST):
            print("RESTful node added")
            node = RestfulServiceNode(self.scene)
            node.setVariableData(self.variables)
            node.title = "RESTful Service"
        elif(op_code == OP_CODE_CODEPY):
            print("Code Activity Python node added")
            node = CodeActivityPythonNode(self.scene)
            node.title = "Code Activity (python)"
        elif(op_code == OP_CODE_WHILE):
            print("While node added")
            node = WhileNode(self.scene)
            node.setVariableData(self.variables)
            node.content.redrawComboBox()
            node.title = "While"
        elif(op_code == OP_CODE_END_WHILE):
            print("End While node added")
            node = EndWhileNode(self.scene)
            node.title = "End While"
        elif(op_code == OP_CODE_BREAK):
            print("Break node added")
            node = BreakNode(self.scene)
            node.title = "Break"
        elif (op_code == OP_CODE_KEYRELEASE):
            print("Key Release Python node added")
            node = KeyReleaseNode(self.scene)
            node.title = "Key Release"
        elif (op_code == OP_CODE_KEYPRESS):
            print("Key Press Python node added")
            node = KeypressNode(self.scene)
            node.title = "Key Press"
        elif(op_code == OP_CODE_RANDOM):
            print("Random node added")
            node = RandomNode(self.scene)
            node.title = "Random"
        else:
            node =  VplNode(self.scene,  text, inputs=[1,1], outputs=[2])

        return node # give the node back
