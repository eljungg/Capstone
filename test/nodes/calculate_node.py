from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base
from Capstone.test.conf import * 
from model.variables import VariablesData
from model.node_data import NodeData
from nodeeditor.node_node import *

class CalculateContent(QDMNodeContentWidget):

    def __init__(self, parent, variablesRef):
        self.vars = variablesRef
        super().__init__(parent)

    def initUI(self):
        self.layout = QVBoxLayout()

        self.comboBox = QComboBox(self)
        self.initialList = ['true', 'false']

        for var in self.vars.variables:
            self.initialList.append(var)
        self.initialList.append('value')
        self.comboBox.addItems(self.initialList)

        self.edit = QLineEdit('', self)
        self.comboBox.setLineEdit(self.edit)

        self.layout.addWidget(self.comboBox)
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


class CalculateNode(VplNode):
    op_code = OP_CODE_CALCULATE

    def __init__(self, scene):
        self.variablesRef = VariablesData()
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = CalculateContent(self, self.variablesRef)
        self.grNode = VplGraphicsNode(self)
        self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code


    def setVariableData(self, variables): # wires up stuff, see subWindow.py
        self.variablesRef = variables
        self.content.setContentVariables(self.variablesRef)

    def doEval(self, input=None):
        
        statement = self.content.edit.text()
        print(statement)

        if statement == 'true':
            self.data.val = True
            self.data.valType = bool
            return

        if statement == 'false':
            self.data.val = False
            self.data.valType = bool
            return

        if 'value' in statement:
            self.inp = input.val
            statement = statement.replace('value', str(self.inp))

        for var in self.content.vars.variables:
            if var.name in statement:
                print('variable detected')
                statement = statement.replace(var.name, str(var.val))
        
        self.final = eval(statement)
        self.data.val = self.final
        self.data.valType = type(self.final)
        

        
        


        
        