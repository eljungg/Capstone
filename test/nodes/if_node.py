from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.utils import dumpException
from vpl_node import *
from conf import *
from model.variables import VariablesData
from model.node_data import NodeData
from nodeeditor.node_node import *

import re

class IfNodeContent(QDMNodeContentWidget):
    #Initialize the total number of if/elses to 1 when a new node is spawned
    TotalIfs = 1

    def __init__(self, parent, variablesRef):
        self.vars = variablesRef
        super().__init__(parent)

    def initUI(self):
        # Set the layout to a box layout
        self.layout = QVBoxLayout()       

        # Create a list of combo boxes that will be added to when additional if/elses are added
        self.comboBox = []
        self.comboBox.append(QComboBox(self))

        # Populate the list that will drop down from a combo box
        self.initialList = ['true', 'false']

        for var in self.vars.variables:
            self.initialList.append("state." + var)

        self.initialList.append('value')

        # Add the list to the combo box
        self.comboBox[0].addItems(self.initialList)

        # Create a list of line edits that will be used in the combo box
        self.edit = []
        self.edit.append(QLineEdit('', self))
        self.comboBox[0].setLineEdit(self.edit[0])

        # Create the buttons and label associated with additional if/elses
        self.subBtn = QPushButton('-', self)
        self.addBtn = QPushButton('+', self)
        self.elseLbl = QLabel('Else', self)
        self.elseLbl.setAlignment(Qt.AlignCenter)

        # Add the combo box to the layout
        self.layout.addWidget(self.comboBox[0])

        # Make a group box for the +, -, Else items
        self.groupBox = QGroupBox()
        self.layout.addWidget(self.groupBox)

        # Set the layout of the group box
        self.innerHbox = QHBoxLayout() 
        self.groupBox.setLayout(self.innerHbox)

        # Add the +, -, Else items to the groupbox layout
        self.innerHbox.addWidget(self.addBtn)
        self.innerHbox.addWidget(self.subBtn)
        self.innerHbox.addWidget(self.elseLbl)

        # Set the stretch and size constraint of the layout
        self.layout.setSizeConstraint(0)
        
        # Redraw the combo box to set the list of values
        self.redrawComboBox()

        # Set the layout of the content
        self.setLayout(self.layout)

    # Function displays new variables in dropdown. (GUI REFRESH)
    def redrawComboBox(self):
        self.comboBox[self.TotalIfs - 1].clear()
        self.comboBox[self.TotalIfs - 1].addItems(['true', 'false'])
        for var in self.vars.variables:
            self.comboBox[self.TotalIfs - 1].addItem("state." + var.name)
        self.comboBox[self.TotalIfs - 1].addItem('value')

    # Set the variables for the content
    def setContentVariables(self, variables):
        self.vars = variables        
    
    # Used for saving the graph
    def serialize(self):
        res = super().serialize()

        values = []

        # Save the content of the text boxes 
        for i in range(len(self.edit)):
            values.append(self.edit[i].text())

        res['value'] = values

        return res

    # Used for loading from a saved graph
    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)

        try:
            value = data['value']

            # Set the text to the values that were saved
            for i in range(len(value)):
                self.edit[i].setText(value[i])

                # Increase the number of combo boxes based on the number of if/elses
                if i < len(value) - 1:
                    self.increaseWidgetSize()

            return True & res
        except Exception as e:
            dumpException(e)

        return res

    # Increase the number of combo boxes
    def increaseWidgetSize(self):        
        self.TotalIfs = self.TotalIfs + 1

        # Remove the +, -, Else items from the layout temporarily to add a new combo box
        self.innerHbox.removeWidget(self.subBtn)
        self.subBtn.deleteLater()
        self.subBtn = None
        self.innerHbox.removeWidget(self.elseLbl)
        self.elseLbl.deleteLater()
        self.elseLbl = None
        self.innerHbox.removeWidget(self.addBtn)
        self.addBtn.deleteLater()
        self.addBtn = None
        self.layout.removeWidget(self.groupBox)
        self.groupBox.deleteLater()
        self.groupBox = None

        # Create a new combo box
        self.comboBox.append(QComboBox(self))
        self.comboBox[self.TotalIfs - 1].addItems(self.initialList)

        # Add a new line edit
        self.edit.append(QLineEdit('' , self))
        self.comboBox[self.TotalIfs - 1].setLineEdit(self.edit[self.TotalIfs - 1])

        self.edit[self.TotalIfs - 1].setAlignment(Qt.AlignLeft)
        
        # Create new +, -, Else items
        self.subBtn = QPushButton('-', self)
        self.addBtn = QPushButton('+', self)
        self.elseLbl = QLabel('Else', self)
        
        # Add the new combo box
        self.layout.addWidget(self.comboBox[self.TotalIfs - 1])

        # Make a new group box
        self.groupBox = QGroupBox()
        self.layout.addWidget(self.groupBox)

        self.innerHbox = None

        # Make a new layout for the group box
        self.innerHbox = QHBoxLayout() 
        self.groupBox.setLayout(self.innerHbox)

        # Add the +, -, Else items to the layout
        self.innerHbox.addWidget(self.addBtn)
        self.innerHbox.addWidget(self.subBtn)
        self.innerHbox.addWidget(self.elseLbl)

        # Set the stretch and size constraint
        self.layout.setSizeConstraint(3)


class IfNode(VplNode):
    # Set the opcode, title, and content label
    op_code = OP_CODE_IF
    op_title = "If"
    content_label_objname = "VplNodeIf"

    def __init__(self, scene, title:str="If", outputList=[0,1]):
        # Set the variables
        self.variablesRef = VariablesData()

        # Call super to initialize the node
        super().__init__(scene, title, inputs = [0], outputs = outputList)

    def initInnerClasses(self):
        # Set the content and other data
        self.content = IfNodeContent(self, self.variablesRef)
        self.TotalIfs = self.content.TotalIfs
        self.TotalOutputs = [0,1]
        self.grNode = VplGraphicsNode(self)

        self.grNode.height = 225
        self.grNode.width = 298
        self.data = NodeData()
        self.data.nodeType = self.op_code

        # Adjust the size of the text boxes - NEEDS ADJUSTMENTS
        #for i in range(len(self.content.edit)):
        #    self.content.edit[i].textChanged.connect(self.onTextChange)
        
        self.registerButtons()

    # Changes the size of the text box based when the text is larger than the box - NEEDS ADJUSTMENTS
    '''
    def onTextChange(self):
        for i in range(len(self.content.edit)):
            self.text = self.content.edit[i].text()
            self.textLen = len(self.text)
            self.metrics = self.content.edit[i].fontMetrics()
            self.w = self.metrics.boundingRect(self.text).width()
            if (self.w > 225) : 
                self.content.edit[i].resize(self.w, self.content.edit[i].height())
                self.grNode.width = self.w + 22
                self.content.setGeometry(self.content.geometry().x(), self.content.geometry().y(), self.w + 22, self.content.geometry().height())

                self.newSockets([0], self.TotalOutputs, True)
    '''

    def setVariableData(self, variables): # wires up stuff, see subWindow.py
        # Set the variables reference
        self.variablesRef = variables
        self.content.setContentVariables(self.variablesRef)
    
    # Used in vpl_execution.py and is the common function name among the nodes
    def doEval(self, input=None):
        # Reads through each line edit
        for index in range(len(self.content.edit)):
            # Set the text in the line edit to a variable
            statement = self.content.edit[index].text()

            # Checks to see if the statement is was written as 'true'
            if statement == 'true':
                self.data.val = index
                self.data.valType = TYPE_INT
                return
            # Checks to see if the statement is was written as 'false'
            elif statement == 'false':
                pass
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
                        self.data.val = index
                        self.data.valType = TYPE_INT
                        return
                else:
                    print("ERROR: The statement in the text field does not result in a Boolean.")
                    self.data.val = None

        # If no other if/else statement returned a true result, set the index to -1 (which will read as the last/else socket of the node)
        self.data.val = -1
        self.data.valType = TYPE_INT
        return

    # Register the buttons with the corresponding functions
    def registerButtons(self):
        self.content.subBtn.clicked.connect(self.decreaseWidgetSize)
        self.content.addBtn.clicked.connect(self.increaseWidgetSize)

    # Increase the number of combo boxes
    def increaseWidgetSize(self):
        self.TotalIfs = self.TotalIfs + 1

        # Remove the +, -, Else items from the layout temporarily to add a new combo box
        self.content.innerHbox.removeWidget(self.content.subBtn)
        self.content.subBtn.deleteLater()
        self.content.subBtn = None
        self.content.innerHbox.removeWidget(self.content.elseLbl)
        self.content.elseLbl.deleteLater()
        self.content.elseLbl = None
        self.content.innerHbox.removeWidget(self.content.addBtn)
        self.content.addBtn.deleteLater()
        self.content.addBtn = None
        self.content.layout.removeWidget(self.content.groupBox)
        self.content.groupBox.deleteLater()
        self.content.groupBox = None
    
        # Create a new combo box
        self.content.comboBox.append(QComboBox(self.content))
        self.content.comboBox[self.TotalIfs - 1].addItems(self.content.initialList)

        # Add a new line edit
        self.content.edit.append(QLineEdit('' , self.content))
        self.content.comboBox[self.TotalIfs - 1].setLineEdit(self.content.edit[self.TotalIfs - 1])

        self.content.edit[self.TotalIfs - 1].setAlignment(Qt.AlignLeft)
        
        # Create new +, -, Else items
        self.content.subBtn = QPushButton('-', self.content)
        self.content.addBtn = QPushButton('+', self.content)
        self.content.elseLbl = QLabel('Else', self.content)
        
        # Add the new combo box
        self.content.layout.addWidget(self.content.comboBox[self.TotalIfs - 1])

        # Make a new group box
        self.content.groupBox = QGroupBox()
        self.content.layout.addWidget(self.content.groupBox)

        self.content.innerHbox = None

        # Make a new layout for the group box
        self.content.innerHbox = QHBoxLayout() 
        self.content.groupBox.setLayout(self.content.innerHbox)

        # Add the +, -, Else items to the layout
        self.content.innerHbox.addWidget(self.content.addBtn)
        self.content.innerHbox.addWidget(self.content.subBtn)
        self.content.innerHbox.addWidget(self.content.elseLbl)

        # Set the size constraint
        self.content.layout.setSizeConstraint(3)
        
        # Change the number of sockets
        self.TotalOutputs.insert(-2, 0)
        self.newSockets([0], self.TotalOutputs, True)

        # Increase the size of the node
        self.grNode.height += 43

        # Adjust the size of text boxes - NEEDS ADJUSTMENTS
        #for i in range(len(self.content.edit)):
        #    self.content.edit[i].textChanged.connect(self.onTextChange)

        # Register the buttons
        self.registerButtons()
        

    # Decrease the number of combo boxes and 
    def decreaseWidgetSize(self):
        # Make sure the node always has at least 1 combo box
        if (self.TotalIfs > 1):
            # Remove the +, -, Else items from the layout temporarily to add a new combo box
            self.content.innerHbox.removeWidget(self.content.subBtn)
            self.content.subBtn.deleteLater()
            self.content.subBtn = None
            self.content.innerHbox.removeWidget(self.content.elseLbl)
            self.content.elseLbl.deleteLater()
            self.content.elseLbl = None
            self.content.innerHbox.removeWidget(self.content.addBtn)
            self.content.addBtn.deleteLater()
            self.content.addBtn = None
            self.content.layout.removeWidget(self.content.groupBox)
            self.content.groupBox.deleteLater()
            self.content.groupBox = None
            
            # Remove the last combo box
            self.content.layout.removeWidget(self.content.comboBox[self.TotalIfs - 1])
            self.content.comboBox[self.TotalIfs - 1].setParent(None) 
            self.content.comboBox.pop()
            self.content.edit.pop()

            # Decrease the total number of if/elses
            self.TotalIfs = self.TotalIfs - 1
            
            # Create the +, -, Else items
            self.content.subBtn = QPushButton('-', self.content)
            self.content.addBtn = QPushButton('+', self.content)
            self.content.elseLbl = QLabel('Else', self.content)
            self.content.elseLbl.setAlignment(Qt.AlignCenter)

            # Create a group box
            self.content.groupBox = QGroupBox()
            self.content.layout.addWidget(self.content.groupBox)

            # Set the layout of the group box
            self.content.innerHbox = QHBoxLayout() 
            self.content.groupBox.setLayout(self.content.innerHbox)
            
            # Add the +, -, Else items
            self.content.innerHbox.addWidget(self.content.addBtn)
            self.content.innerHbox.addWidget(self.content.subBtn)
            self.content.innerHbox.addWidget(self.content.elseLbl)
            
            # Decrease the number of sockets
            self.TotalOutputs.pop(-2)
            self.newSockets([0], self.TotalOutputs, True)

            # Decrease the size of the node
            self.grNode.height -= 43
            
            # Set the size constraint
            self.content.layout.setSizeConstraint(3)

            # Adjust the size of text boxes - NEEDS ADJUSTMENTS
            #for i in range(len(self.content.edit)):
            #    self.content.edit[i].textChanged.connect(self.onTextChange)

            # Register the buttons
            self.registerButtons()

        else:
            print('Must have at least one if statement!')

