from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.utils import dumpException
from vpl_node import *
from conf import *
from model.variables import VariablesData
from model.node_data import NodeData
from nodeeditor.node_node import *

import re

class SwitchNodeContent(QDMNodeContentWidget):
    TotalIfs = 1

    def __init__(self, parent, variablesRef):
        self.vars = variablesRef
        super().__init__(parent)

    def initUI(self):
        self.layout = QVBoxLayout()       

        self.comboBox = []
        self.comboBox.append(QComboBox(self))
        self.initialList = ['true', 'false']

        for var in self.vars.variables:
            self.initialList.append(var)

        self.initialList.append('value')
        self.comboBox[0].addItems(self.initialList)

        self.edit = []
        self.edit.append(QLineEdit('', self))
        self.comboBox[0].setLineEdit(self.edit[0])

        self.edit[0].setAlignment(Qt.AlignCenter)
        self.subBtn = QPushButton('-', self)
        self.addBtn = QPushButton('+', self)
        self.elseLbl = QLabel('Else', self)
        self.elseLbl.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.comboBox[0])

        self.groupBox = QGroupBox()
        self.layout.addWidget(self.groupBox)

        self.innerHbox = QHBoxLayout() 
        self.groupBox.setLayout(self.innerHbox)

        self.innerHbox.addWidget(self.addBtn)
        self.innerHbox.addWidget(self.subBtn)
        self.innerHbox.addWidget(self.elseLbl)

        self.layout.setStretch(0, 1)
        self.layout.setStretch(1, 1)
        self.layout.setSizeConstraint(0)
        
        self.redrawComboBox()
        self.setLayout(self.layout)

    def redrawComboBox(self): # function displays new variables in dropdown. (GUI REFRESH)
        self.comboBox[self.TotalIfs - 1].clear()
        self.comboBox[self.TotalIfs - 1].addItems(['true', 'false'])
        for var in self.vars.variables:
            self.comboBox[self.TotalIfs - 1].addItem(var.name)
        self.comboBox[self.TotalIfs - 1].addItem('value')

    def setContentVariables(self, variables):
        self.vars = variables

        
    
    #I hope these are correct
    def serialize(self):
        res = super().serialize()
        values = []
        for i in range(len(self.edit)):
            values.append(self.edit[i].text())

        res['value'] = values
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']

            for i in range(len(value)):
                self.edit[i].setText(value[i])

                if i < len(value) - 1:
                    self.increaseWidgetSize()

            return True & res
        except Exception as e:
            dumpException(e)
        return res

    def registerButtons(self):
        self.addBtn.clicked.connect(self.increaseWidgetSize)

    def increaseWidgetSize(self):
        
        self.TotalIfs = self.TotalIfs + 1

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
    
        self.comboBox.append(QComboBox(self))
        self.comboBox[self.TotalIfs - 1].addItems(self.initialList)

        self.edit.append(QLineEdit('' , self))
        self.comboBox[self.TotalIfs - 1].setLineEdit(self.edit[self.TotalIfs - 1])

        self.edit[self.TotalIfs - 1].setAlignment(Qt.AlignCenter)
        
        self.subBtn = QPushButton('-', self)
        self.addBtn = QPushButton('+', self)
        self.elseLbl = QLabel('Else', self)
        
        self.layout.addWidget(self.comboBox[self.TotalIfs - 1])

        self.groupBox = QGroupBox()
        self.layout.addWidget(self.groupBox)

        self.innerHbox = None

        self.innerHbox = QHBoxLayout() 
        self.groupBox.setLayout(self.innerHbox)

        self.innerHbox.addWidget(self.addBtn)
        self.innerHbox.addWidget(self.subBtn)
        self.innerHbox.addWidget(self.elseLbl)

        self.layout.setStretch(self.TotalIfs - 1, 1)
        self.layout.setStretch(self.TotalIfs, 1)

        self.layout.setSizeConstraint(0)
        
        self.redrawComboBox()

        self.registerButtons()


class SwitchNode(VplNode):
    icons = "Capstone/icons/in.png"
    op_code = OP_CODE_SWITCH
    op_title = "Switch"
    content_label_objname = "VplNodeSwitch"
    TotalOutputs = [1,1]

    def __init__(self, scene, title:str="If", outputList=TotalOutputs):
        self.variablesRef = VariablesData()
        super().__init__(scene, title, inputs = [0], outputs = outputList)

    def initInnerClasses(self):
        self.content = SwitchNodeContent(self, self.variablesRef)
        self.TotalIfs = self.content.TotalIfs
        self.grNode = VplGraphicsNode(self)

        self.grNode.height = 225
        self.grNode.width = 298
        self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code

        
        self.registerButtons()

    def setVariableData(self, variables): # wires up stuff, see subWindow.py
        self.variablesRef = variables
        self.content.setContentVariables(self.variablesRef)
    
    def doEval(self, input=None):
        for index in range(len(self.content.edit)):
            statement = self.content.edit[index].text()

            if statement == 'true':
                self.data.val = index
                self.data.valType = TYPE_INT
                return
            elif statement == 'false':
                pass
            else:
                if 'value' in statement:
                    self.inp = input.val
                    statement = self.inp + "==" + statement

                for var in self.content.vars.variables:
                    statement = re.sub(fr'\bstate.{var.name}\b', str(var.val), statement)
                
                # issue with multiple variables sharing parts of the same name

                self.final = eval(statement)

                if(type(self.final) is bool):
                    if(self.final is True):
                        self.data.val = index
                        self.data.valType = TYPE_INT
                        return
                else:
                    print("ERROR: The statement in the text field does not result in a Boolean.")
                    self.data.val = None

        self.data.val = -1
        self.data.valType = TYPE_INT
        return

    def registerButtons(self):
        self.content.subBtn.clicked.connect(self.decreaseWidgetSize)
        self.content.addBtn.clicked.connect(self.increaseWidgetSize)

    def increaseWidgetSize(self):
        
        self.TotalIfs = self.TotalIfs + 1

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
    
        self.content.comboBox.append(QComboBox(self.content))
        self.content.comboBox[self.TotalIfs - 1].addItems(self.content.initialList)

        self.content.edit.append(QLineEdit('' , self.content))
        self.content.comboBox[self.TotalIfs - 1].setLineEdit(self.content.edit[self.TotalIfs - 1])

        self.content.edit[self.TotalIfs - 1].setAlignment(Qt.AlignCenter)
        
        self.content.subBtn = QPushButton('-', self.content)
        self.content.addBtn = QPushButton('+', self.content)
        self.content.elseLbl = QLabel('Else', self.content)
        
        self.content.layout.addWidget(self.content.comboBox[self.TotalIfs - 1])

        self.content.groupBox = QGroupBox()
        self.content.layout.addWidget(self.content.groupBox)

        self.content.innerHbox = None

        self.content.innerHbox = QHBoxLayout() 
        self.content.groupBox.setLayout(self.content.innerHbox)

        self.content.innerHbox.addWidget(self.content.addBtn)
        self.content.innerHbox.addWidget(self.content.subBtn)
        self.content.innerHbox.addWidget(self.content.elseLbl)

        self.content.layout.setStretch(self.TotalIfs - 1, 1)
        self.content.layout.setStretch(self.TotalIfs, 1)
        
        self.TotalOutputs.insert(-2, 1)
        self.newSockets([0], self.TotalOutputs, True)

        self.grNode.height += 43

        self.content.layout.setSizeConstraint(0)
        
        self.registerButtons()

    def decreaseWidgetSize(self):

        if (self.TotalIfs > 1):
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
            
            self.content.layout.removeWidget(self.content.comboBox[self.TotalIfs - 1])
            self.content.comboBox[self.TotalIfs - 1].setParent(None) 
            self.content.comboBox.pop()
            self.content.edit.pop()

            self.TotalIfs = self.TotalIfs - 1
            
            self.content.subBtn = QPushButton('-', self.content)
            self.content.addBtn = QPushButton('+', self.content)
            self.content.elseLbl = QLabel('Else', self.content)
            self.content.elseLbl.setAlignment(Qt.AlignCenter)

            self.content.layout.setSizeConstraint(3)

            self.content.groupBox = QGroupBox()
            self.content.layout.addWidget(self.content.groupBox)

            self.content.innerHbox = QHBoxLayout() 
            self.content.groupBox.setLayout(self.content.innerHbox)
            
            self.content.innerHbox.addWidget(self.content.addBtn)
            self.content.innerHbox.addWidget(self.content.subBtn)
            self.content.innerHbox.addWidget(self.content.elseLbl)
            
            self.TotalOutputs.pop(-2)
            self.newSockets([0], self.TotalOutputs, True)

            self.grNode.height -= 43

            self.content.innerHbox.setSizeConstraint(3)

            self.registerButtons()

        else:
            print('Must have at least one if statement!')

