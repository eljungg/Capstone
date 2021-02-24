from PyQt5.QtCore import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode
from model.variables import VariablesData
from model.node_data import NodeData

from PyQt5.QtWidgets import *
from Capstone.test.conf import * 
from nodeeditor.node_node import *

import re

DEBUG = True
ADDITIONAL_IFS = 2
INITIAL_OUTPUTS = 5

class IfNodeContent(QDMNodeContentWidget):

    def __init__(self, parent, variablesRef):
        self.vars = variablesRef
        super().__init__(parent)

    def initUI(self):
        self.layout = QGridLayout()

        # Setup of all the widgets needed
        self.comboBox = QComboBox(self)
        self.initialList = ['true', 'false']

        for var in self.vars.variables:
            self.initialList.append(var)
        self.initialList.append('value')
        self.comboBox.addItems(self.initialList)

        self.edit = QLineEdit('', self)
        self.comboBox.setLineEdit(self.edit)

        self.edit.setAlignment(Qt.AlignCenter)
        self.subBtn = QPushButton('-', self)
        self.addBtn = QPushButton('+', self)
        self.elseLbl = QLabel('Else', self)
        self.elseLbl.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.comboBox, 1, 1, 1, 3)
        self.layout.addWidget(self.subBtn, 2, 1)
        self.layout.addWidget(self.elseLbl, 2, 2)
        self.layout.addWidget(self.addBtn, 2, 3)
        self.setLayout(self.layout)
        
        self.redrawComboBox()

    def redrawComboBox(self): # function displays new variables in dropdown. (GUI REFRESH)
        self.comboBox.clear()
        self.comboBox.addItems(['true', 'false'])
        for var in self.vars.variables:
            self.comboBox.addItem(var.name)
        self.comboBox.addItem('value')

    def setContentVariables(self, variables):
        self.vars = variables
    
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


class IfNode(VplNode):
    icons = "Capstone/icons/in.png"
    op_code = OP_CODE_IF
    op_title = "If"
    content_label_objname = "VplNodeIf"

    def __init__(self, scene, title:str="If"):
        self.variablesRef = VariablesData()
        super().__init__(scene, title, inputs = [1], outputs = [1,2])

    def initInnerClasses(self):
        self.content = IfNodeContent(self, self.variablesRef)
        self.grNode = VplGraphicsNode(self)

        self.grNode.height = 160
        self.grNode.width = 260
        self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code
         
        self.registerButtons()

    def setVariableData(self, variables): # wires up stuff, see subWindow.py
        self.variablesRef = variables
        self.content.setContentVariables(self.variablesRef)
    
    def doEval(self, input=None):
        statement = self.content.edit.text()
        broken = statement.split(" ")

        if statement == 'true':
            self.data.val = 0
            return

        if statement == 'false':
            self.data.val = -1
            return

        if 'value' in statement:
            self.inp = input.val
            statement = statement.replace('value', str(self.inp))

        for var in self.content.vars.variables:
            statement = re.sub(fr'\b{var.name}\b', str(var.val), statement)
        
        # issue with multiple variables sharing parts of the same name

        self.final = eval(statement)

        if(type(self.final) is bool):
            if(self.final is True):
                self.data.val = 0
                self.data.valType = TYPE_INT
            else:
                self.data.val = -1
                self.data.valType = TYPE_INT
        else:
            print("ERROR: The statement in the text field does not result in a Boolean.")
            self.data.val = None

        """
        givenValue = ""

        if(len(broken) == 3):
            if(broken[2][0] == "\"" and broken[2][-1] == "\""):
                givenValue = broken[2][1:-1]
            else:
                givenValue = broken[2]

            if(broken[0] == "value"):
                if(broken[1] == "=="):
                    if(input.val == givenValue):
                        self.data.val = 0
                    else:
                        self.data.val = -1
                elif(broken[1] == ">="):
                    if(input.val >= givenValue):
                        self.data.val = 0
                    else:
                        self.data.val = -1
                elif(broken[1] == "<="):
                    if(input.val <= givenValue):
                        self.data.val = 0
                    else:
                        self.data.val = -1
                elif(broken[1] == ">"):
                    if(input.val > givenValue):
                        self.data.val = 0
                    else:
                        self.data.val = -1
                elif(broken[1] == "<"):
                    if(input.val < givenValue):
                        self.data.val = 0
                    else:
                        self.data.val = -1
                elif(broken[1] == "!="):
                    if(input.val != givenValue):
                        self.data.val = 0
                    else:
                        self.data.val = -1
                else:
                    print("There is an error in the logic.")
        """
        return
    

    def registerButtons(self):
        self.content.subBtn.clicked.connect(self.decreaseWidgetSize)
        self.content.addBtn.clicked.connect(self.increaseWidgetSize)

    def increaseWidgetSize(self):
        # will have to change this to account for multiple if nodes
        # maybe make a local copy

        global ADDITIONAL_IFS
        self.grNode.height = self.grNode.height + 24
        if DEBUG:
            print('Add button clicked!')

        # increment global variable ADDITIONAL IFS
        ADDITIONAL_IFS = ADDITIONAL_IFS + 1

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
        numIfs = ADDITIONAL_IFS - 1
        self.content.layout.addWidget(self.content.edit, numIfs, 1, 1, 3)
        self.content.layout.addWidget(self.content.subBtn, ADDITIONAL_IFS, 1)
        self.content.layout.addWidget(self.content.elseLbl, ADDITIONAL_IFS, 2)
        self.content.layout.addWidget(self.content.addBtn, ADDITIONAL_IFS, 3)

        # must reregister buttons because they are new
        if DEBUG:
            print('REGISTERING BUTTONS')  
        self.registerButtons()

    def decreaseWidgetSize(self):
        print('Sub button clicked!')
        if (self.grNode.height > 100):
            
            global ADDITIONAL_IFS
            self.grNode.height = self.grNode.height - 24
            if DEBUG:
                print('Add button clicked!')

            # increment global variable ADDITIONAL IFS
            ADDITIONAL_IFS = ADDITIONAL_IFS - 1

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
            toRemove = self.content.layout.itemAtPosition(ADDITIONAL_IFS, 1)
            remove = toRemove.widget()
            self.content.layout.removeWidget(remove)
            remove.setParent(None)
            
            
            # for some reason, must redefine widgets
            if DEBUG:
                print('REDEFINING WIDGETS')        
            self.content.subBtn = QPushButton('-', self.content)
            self.content.addBtn = QPushButton('+', self.content)
            self.content.elseLbl = QLabel('Else', self.content)
            self.content.elseLbl.setAlignment(Qt.AlignCenter)

            if DEBUG:
                print('ADDING WIDGETS BACK INTO LAYOUT')
            self.content.layout.addWidget(self.content.subBtn, ADDITIONAL_IFS, 1)
            self.content.layout.addWidget(self.content.elseLbl, ADDITIONAL_IFS, 2)
            self.content.layout.addWidget(self.content.addBtn, ADDITIONAL_IFS, 3)      
            
            if DEBUG:
                print('REGISTERING BUTTONS')  

            self.registerButtons()

        else:
            print('Must have at least one if statement!')