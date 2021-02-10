from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QPushButton
from conf import *
from model.variables import VariablesData
from variable_menu import *
from nodeeditor.node_graphics_node import QDMGraphicsNode

class VariableContent(QDMNodeContentWidget):
    
    def __init__(self, parent, variablesRef):
        self.vars = variablesRef
        super().__init__(parent)
    

    def initUI(self):
        self.layout = QVBoxLayout()
        
        ###We are going to need some globla (subWindow) level variable holder
        self.variablesDropDown = QComboBox(self)
        for var in self.vars.variables:
            self.variablesDropDown.addItem(var)
        
        self.variableMenuBtn = QPushButton("more")

        #self.layout.addWidget(self.edit) #hiding the O.G. edit line, not needed
        self.layout.addWidget(self.variablesDropDown)
        self.layout.addWidget(self.variableMenuBtn)

        self.setLayout(self.layout)
        print("debug size of self.vars ==>" + str(len(self.vars.variables)))
        self.reDrawVariablesDropDown() # on node creation, show current variables in dropdown
        
    def reDrawVariablesDropDown(self): # function displays new variables in dropdown. (GUI REFRESH)
        self.variablesDropDown.clear()
        print("size of self.vars.variables ==>" + str(len(self.vars.variables)))
        for var in self.vars.variables:
            # var._printVar() #debug
            self.variablesDropDown.addItem(var.name)

    def setContentVariables(self, variables):
        self.vars = variables

    def serialize(self):
        res = super().serialize()
        #res['value'] = self.edit.text() #TODO this QT widget has been deleted, saving needs work 
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            #self.edit.setText(value) #TODO this QT widget has been deleted, saving needs work 
            return True & res
        except Exception as e:
            dumpException(e)
        return res
    def showVariableMenu(self): #maybe better in content class?
        menuDialog = VariableMenu(self, self.vars)
        menuDialog.exec_()

class VariableNode(VplNode):
    op_code = OP_CODE_VARIABLE
    def __init__(self, scene):
        #VariablesData() called to create a dummy value for compatibility with library loading function
        self.variablesRef = VariablesData() # set on construction in sub_window.py # reference to out subWindow level variables
        super().__init__(scene, inputs=[], outputs=[3])
        

    def initInnerClasses(self):
        self.content = VariableContent(self , self.variablesRef)
        self.grNode = VplGraphicsNode(self)
        self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code

        self.grNode.height = 120
        self.grNode.width = 160
        self.content.variableMenuBtn.clicked.connect(self.content.showVariableMenu) # do modal popup
    
    def __printVariables(self): ## DEBUG TESTING ONLY
        for variable in self.variablesRef.variables:
            print("Variable found! : " + variable.name)

    def setVariableData(self, variables): # wires up stuff, see subWindow.py
        self.variablesRef = variables
        self.content.setContentVariables(self.variablesRef)
