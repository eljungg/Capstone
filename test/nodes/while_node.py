from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.utils import dumpException
from vpl_node import *
from conf import * 
from model.variables import VariablesData
from model.node_data import NodeData
from nodeeditor.node_node import *

import re

class WhileContent(QDMNodeContentWidget):
    def __init__(self, parent, variablesRef):
        self.vars = variablesRef
        super().__init__(parent)

    def initUI(self):
        # Set the layout to a box layout
        self.layout = QVBoxLayout()

        # Create a combo box
        self.comboBox = QComboBox(self)
        self.initialList = ['true', 'false']

        # Add variables to the list
        for var in self.vars.variables:
            self.initialList.append("state." + var)

        self.initialList.append('value')
        self.comboBox.addItems(self.initialList)

        # Add a line edit to the combo box
        self.edit = QLineEdit('', self)
        self.comboBox.setLineEdit(self.edit)

        # Add the combo box to the layout
        self.layout.addWidget(self.comboBox)

        # Set the layout
        self.setLayout(self.layout)

        # Redraw the combo box to set the list of values
        self.redrawComboBox()

    # Function displays new variables in dropdown. (GUI REFRESH)
    def redrawComboBox(self):
        self.comboBox.clear()
        self.comboBox.addItems(['true', 'false'])
        for var in self.vars.variables:
            self.comboBox.addItem("state." + var.name)
        self.comboBox.addItem('value')

    # Set the variables
    def setContentVariables(self, variables):
        self.vars = variables
    
    # Used for saving the graph
    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res 

    # Used for loading a saved graph
    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


class WhileNode(VplNode):
    # Set the opcode, title, and content label
    op_code = OP_CODE_WHILE
    op_title = "While"
    content_label_objname = "VplNodeWhile"

    def __init__(self, scene):
        self.variablesRef = VariablesData()
        super().__init__(scene, inputs=[0], outputs=[0])

    def initInnerClasses(self):
        self.content = WhileContent(self, self.variablesRef)
        self.grNode = VplGraphicsNode(self)
        self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code
        self.data.id = self.id
        self.content.edit.textChanged.connect(self.onTextChange)

    # Changes the size of the text box based when the text is larger than the box - NEEDS SMALL ADJUSTMENTS
    def onTextChange(self):
        self.text = self.content.edit.text()
        self.textLen = len(self.text)
        self.metrics = self.content.edit.fontMetrics()
        self.w = self.metrics.boundingRect(self.text).width()
        if (self.w > 138) : 
            self.content.edit.resize(self.w, self.content.edit.height())
            self.grNode.width = self.w + 22
            self.content.setGeometry(self.content.geometry().x(), self.content.geometry().y(), self.w + 22, self.content.geometry().height())

            self.newSockets([0], [0], True)
            
    # Set the variable references
    def setVariableData(self, variables): # wires up stuff, see subWindow.py
        self.variablesRef = variables
        self.content.setContentVariables(self.variablesRef)

    # Used in vpl_execution.py and is the common function name among the nodes
    def doEval(self, input=None):
        # Set the text in the line edit to a variable
        statement = self.content.edit.text()

        # Checks to see if the statement is was written as 'true'
        if statement == 'true':
            self.data.val = True
            self.data.valType = TYPE_BOOL
            return
        # Checks to see if the statement is was written as 'false'
        elif statement == 'false':
            self.data.val = False
            self.data.valType = TYPE_BOOL
            return
        # Checks to see if the statement is was anything else
        else:
            # If the word 'value' is contained inside the statement
            if 'value' in statement:
                # Set the input value to a variable and replace the word value with the variable
                self.inp = input.val
                statement = statement.replace('value', str(self.inp))

            # Search for a saved variable and apply the value saved to that variable to the statement
            for var in self.content.vars.variables:
                statement = re.sub(fr'\bstate.{var.name}\b', str(var.val), statement)
            
                # issue with multiple variables sharing parts of the same name

            # Evaluate the statement and save the result
            self.final = eval(statement)

            # Check to see if the final result is a boolean
            if(type(self.final) is bool):
                if(self.final is True):
                    # Set the data value (which is the parentData for the next node) to the index of the correct if/else statement
                    self.data.val = True
                    self.data.valType = TYPE_BOOL
                    return
                if(self.final is False):
                    self.data.val = False
                    self.data.valType = TYPE_BOOL
                    return
            else:
                print("ERROR: The statement in the text field does not result in a Boolean.")
                self.data.val = None