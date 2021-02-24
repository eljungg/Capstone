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
        self.reDrawVariablesDropDown() # on node creation, show current variables in dropdown
        
    def reDrawVariablesDropDown(self): # function displays new variables in dropdown. (GUI REFRESH)
        self.variablesDropDown.clear()
        for var in self.vars.variables:
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
        self.variablesRef = VariablesData() # set on construction in sub_window.py # reference to out subWindow level variables
        super().__init__(scene, inputs=[1], outputs=[3]) #added single input
        

    def initInnerClasses(self):
        self.content = VariableContent(self , self.variablesRef)
        self.grNode = VplGraphicsNode(self)
        self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code
        self.data.id = self.id

        self.grNode.height = 120
        self.grNode.width = 160
        self.content.variableMenuBtn.clicked.connect(self.content.showVariableMenu) # do modal popup
    def doEval(self, parentData=None):
        selectedVariable = self._getSelectedVariable()#we need a handle on selected variable
        if(selectedVariable == None): # case we have no variables yet, but data comes into variable node
            print("This is an error message! You can have data coming in with no defined variables!") # TODO build some type of popup alert like in VIPLE for this
            self.__clearNodeData()
            return
        if(parentData == None): #case its the first node in thread 
            #selected variable != None here, so we are a first node, but our variable is set
            self.data.val = selectedVariable.val
            self.data.valType = selectedVariable.valType
            return

        self.__setVariableVal(selectedVariable , parentData.val) # set that variable with the new data
        self.__setVariableType(selectedVariable , parentData.valType)
        #now we need to set this nodes NodeData() to have its val, and type. So that we pass these one to children
        self.data.val = parentData.val
        self.data.valType = parentData.valType
    
    def _getSelectedVariable(self): # get variable object which is selected on node-face
        varName = self.content.variablesDropDown.currentText() # get varname as string
        variable = self.variablesRef._findVarByName(varName)
        return variable;
    
    def __setVariableVal(self , variable , inpVal):
        variable.val = inpVal;

    def __setVariableType(self , variable, inpType): #im not sure if we need this #should type be determined by incoming datanode or by what user selected in variable menu???
        variable.valType = inpType 

    def __printVariables(self): ## DEBUG TESTING ONLY
        for variable in self.variablesRef.variables:
            print("Variable found! : " + variable.name)

    def setVariableData(self, variables): # wires up stuff, see subWindow.py
        self.variablesRef = variables
        self.content.setContentVariables(self.variablesRef)
    
    def __clearNodeData(self): # for a weird case where the variable inside a node has been deleted and not replaced / empty
        #could wire this to onDropDown changed event might be smart honestly
        self.data.val = None
        self.valType = None