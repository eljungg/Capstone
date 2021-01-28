from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QPushButton
from conf import *
from variables import VariablesData
from variable_menu import VariableMenu
from nodeeditor.node_graphics_node import QDMGraphicsNode

class VariableContent(QDMNodeContentWidget):
    
    def __init__(self, parent, variablesRef):
        self.vars = variablesRef
        super().__init__(parent)
    

    def initUI(self):
        self.layout = QVBoxLayout()
        
        self.edit = QLineEdit("Variable Node Class" , self)
        self.edit.setAlignment(Qt.AlignRight)
        ###We are going to need some globla (subWindow) level variable holder
        self.variablesDropDown = QComboBox(self)
        for var in self.vars.variables:
            self.variablesDropDown.addItem(var)
        
        self.variableMenuBtn = QPushButton("more")

        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.variablesDropDown)
        self.layout.addWidget(self.variableMenuBtn)

        self.setLayout(self.layout)
        
    def reDrawVariablesDropDown(self): # function displays new variables in dropdown. (GUI REFRESH)
        self.variablesDropDown.clear()
        for var in self.vars.variables:
            self.variablesDropDown.addItem(var)

    def setContentVariables(self, variables):
        self.vars = variables

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

        self.grNode.height = 120
        self.grNode.width = 160
        #self.content.edit.textChanged.connect(self.onInputChanged)
        self.content.edit.textChanged.connect(self.__printVariables) # DEBUG TESTING
        self.content.edit.textChanged.connect(self.content.reDrawVariablesDropDown) # redraw content of dropdown
        self.content.variableMenuBtn.clicked.connect(self.content.showVariableMenu) # do modal popup
    
    def __printVariables(self): ## DEBUG TESTING ONLY
        self.variablesRef.variables.append("another")
        for variable in self.variablesRef.variables:
            print("Variable found! : " + variable)

    def setVariableData(self, variables):
        self.variablesRef = variables
        self.content.setContentVariables(self.variablesRef)
