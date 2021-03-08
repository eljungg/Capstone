from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode
DEBUG = True
ADDITIONAL_SWITCHES = 2
INITIAL_OUTPUTS = 5
outputList = [1,1]

class SwitchNodeContent(QDMNodeContentWidget):
    def initUI(self):
        # Setup of all the widgets needed
        self.edit = QLineEdit('' , self)
        self.edit.setAlignment(Qt.AlignCenter)
        self.subBtn = QPushButton('-', self)
        self.addBtn = QPushButton('+', self)
        self.elseLbl = QLabel('Default', self)
        self.elseLbl.setAlignment(Qt.AlignCenter)

        # Set up layout
        self.layout = QGridLayout()

        self.layout.addWidget(self.edit, 1, 1, 1, 3)
        self.layout.addWidget(self.subBtn, 2, 1)
        self.layout.addWidget(self.elseLbl, 2, 2)
        self.layout.addWidget(self.addBtn, 2, 3)
        self.setLayout(self.layout)

        
    
    #I hope these are correct
    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res

        except Exception as e:
            dumpException(e)

        return res


class SwitchNode(VplNode):
    icons = "Capstone/icons/in.png"
    op_code = OP_CODE_SWITCH
    op_title = "Switch"
    content_label_objname = "VplNodeSwitch"

    def __init__(self, scene, title:str="Switch"):
        super().__init__(scene, title, inputs = [1], outputs = [1,2])

    def initInnerClasses(self):
        self.content = SwitchNodeContent(self)
        self.grNode = VplGraphicsNode(self)

        self.grNode.height = 100
        self.grNode.width = 230
        #self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code
         
        self.registerButtons()

    
    def doEval(self, input=None):
        statement = self.content.edit.text()

        givenValue = ""

        if(statement[0] == "\"" and statement[-1] == "\""):
            givenValue = statement[1:-1]
        else:
            givenValue = statement


        if(input.val == givenValue):
            self.data.val = True
        else:
            self.data.val = False
            
        return
    

    def registerButtons(self):
        self.content.subBtn.clicked.connect(self.decreaseWidgetSize)
        self.content.addBtn.clicked.connect(self.increaseWidgetSize)

    def increaseWidgetSize(self):
        # will have to change this to account for multiple if nodes
        # maybe make a local copy
        global ADDITIONAL_SWITCHES
        self.grNode.height = self.grNode.height + 24
        if DEBUG:
            print('Add button clicked!')

        # increment global variable ADDITIONAL_SWITCHES
        ADDITIONAL_SWITCHES = ADDITIONAL_SWITCHES + 1
        outputList.append(1)

        # remove current bottom row (buttons + else label)
        if DEBUG:
            print('REMOVING BOTTOM ROW')
        self.content.layout.removeWidget(self.content.subBtn)
        self.content.subBtn.setParent(None)
        self.content.layout.removeWidget(self.content.elseLbl)
        self.content.elseLbl.setParent(None)
        self.content.layout.removeWidget(self.content.addBtn)
        self.content.addBtn.setParent(None)

        # for some reason, must redefine widgets
        if DEBUG:
            print('REDEFINING WIDGETS')        
        self.content.edit = QLineEdit('' , self.content)
        self.content.edit.setAlignment(Qt.AlignCenter)
        self.content.subBtn = QPushButton('-', self.content)
        self.content.addBtn = QPushButton('+', self.content)
        self.content.elseLbl = QLabel('Else', self.content)
        self.content.elseLbl.setAlignment(Qt.AlignCenter)

        # add redefined widgets back into the layout
        if DEBUG:
            print('ADDING WIDGETS BACK INTO LAYOUT')
        numIfs = ADDITIONAL_SWITCHES - 1
        self.content.layout.addWidget(self.content.edit, numIfs, 1, 1, 3)
        self.content.layout.addWidget(self.content.subBtn, ADDITIONAL_SWITCHES, 1)
        self.content.layout.addWidget(self.content.elseLbl, ADDITIONAL_SWITCHES, 2)
        self.content.layout.addWidget(self.content.addBtn, ADDITIONAL_SWITCHES, 3)

        # must reregister buttons because they are new
        if DEBUG:
            print('REGISTERING BUTTONS')  
        self.registerButtons()

    def decreaseWidgetSize(self):
        print('Sub button clicked!')
        if (self.grNode.height > 100):
            
            global ADDITIONAL_SWITCHES
            self.grNode.height = self.grNode.height - 24
            if DEBUG:
                print('Add button clicked!')

            # increment global variable ADDITIONAL_SWITCHES
            ADDITIONAL_SWITCHES = ADDITIONAL_SWITCHES - 1

            # remove current bottom row
            if DEBUG:
                print('REMOVING BOTTOM ROW')
            self.content.layout.removeWidget(self.content.subBtn)
            self.content.subBtn.setParent(None)
            self.content.layout.removeWidget(self.content.elseLbl)
            self.content.elseLbl.setParent(None)
            self.content.layout.removeWidget(self.content.addBtn)
            self.content.addBtn.setParent(None)

            if DEBUG:
                print('REMOVING BOTTOM IF STATEMENT')
            
            
            # Remove row at ADDITIONAL_IFS
            toRemove = self.content.layout.itemAtPosition(ADDITIONAL_SWITCHES, 1)
            remove = toRemove.widget()
            self.content.layout.removeWidget(remove)
            remove.setParent(None)
            
            
            # for some reason, must redefine widgets
            if DEBUG:
                print('REDEFINING WIDGETS')        
            self.content.subBtn = QPushButton('-', self.content)
            self.content.addBtn = QPushButton('+', self.content)
            self.content.elseLbl = QLabel('Default', self.content)
            self.content.elseLbl.setAlignment(Qt.AlignCenter)

            if DEBUG:
                print('ADDING WIDGETS BACK INTO LAYOUT')
            self.content.layout.addWidget(self.content.subBtn, ADDITIONAL_SWITCHES, 1)
            self.content.layout.addWidget(self.content.elseLbl, ADDITIONAL_SWITCHES, 2)
            self.content.layout.addWidget(self.content.addBtn, ADDITIONAL_SWITCHES, 3)      
            
            if DEBUG:
                print('REGISTERING BUTTONS')  

            self.registerButtons()

        else:
            print('Must have at least one switch statement!')