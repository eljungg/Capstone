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
    TotalIfs = 1

    def __init__(self, parent, variablesRef):
        self.vars = variablesRef
        super().__init__(parent)

    def initUI(self):
        self.layout = QGridLayout()
        self.backup = QGridLayout()

        self.layout.setRowStretch(1, 3)
        self.layout.setRowStretch(2, 3)
        

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

        self.layout.addWidget(self.comboBox[0], 1, 1, 1, 3)
        self.layout.addWidget(self.subBtn, 2, 2)
        self.layout.addWidget(self.elseLbl, 2, 3)
        self.layout.addWidget(self.addBtn, 2, 1)
        self.setLayout(self.layout)
        self.redrawComboBox()

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
        res['value'] = self.edit[0].text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit[0].setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


class IfNode(VplNode):
    icons = "Capstone/icons/in.png"
    op_code = OP_CODE_IF
    op_title = "If"
    content_label_objname = "VplNodeIf"
    TotalOutputs = [1,2]

    def __init__(self, scene, title:str="If", outputList=[1,2]):
        self.variablesRef = VariablesData()
        super().__init__(scene, title, inputs = [1], outputs = outputList)

    def initInnerClasses(self):
        self.content = IfNodeContent(self, self.variablesRef)
        self.TotalIfs = self.content.TotalIfs
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
                    statement = statement.replace('value', str(self.inp))

                for var in self.content.vars.variables:
                    statement = re.sub(fr'\b{var.name}\b', str(var.val), statement)
                
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

        self.content.layout.removeWidget(self.content.subBtn)
        self.content.subBtn.deleteLater()
        self.content.subBtn = None
        self.content.layout.removeWidget(self.content.elseLbl)
        self.content.elseLbl.deleteLater()
        self.content.elseLbl = None
        self.content.layout.removeWidget(self.content.addBtn)
        self.content.addBtn.deleteLater()
        self.content.addBtn = None      

        self.content.comboBox.append(QComboBox(self.content))
        self.content.comboBox[self.TotalIfs - 1].addItems(self.content.initialList)

        self.content.edit.append(QLineEdit('' , self.content))
        self.content.comboBox[self.TotalIfs - 1].setLineEdit(self.content.edit[self.TotalIfs - 1])

        self.content.edit[self.TotalIfs - 1].setAlignment(Qt.AlignCenter)
        
        self.content.subBtn = QPushButton('-', self.content)
        self.content.addBtn = QPushButton('+', self.content)
        self.content.elseLbl = QLabel('Else', self.content)
        self.content.elseLbl.setAlignment(Qt.AlignCenter)

        self.content.layout.setRowStretch(self.TotalIfs, 3)
        self.content.layout.setRowStretch(self.TotalIfs + 1, 3)
        
        self.content.layout.addWidget(self.content.comboBox[self.TotalIfs - 1], self.TotalIfs, 1, 1, 3)        
        
        self.content.layout.addWidget(self.content.subBtn, self.TotalIfs + 1, 2)
        self.content.layout.addWidget(self.content.elseLbl, self.TotalIfs + 1, 3)
        self.content.layout.addWidget(self.content.addBtn, self.TotalIfs + 1, 1)
        
        self.TotalOutputs.insert(-2, 1)
        self.newSockets([1], self.TotalOutputs, True)

        self.grNode.height += 43
        
        self.content.redrawComboBox()
        self.registerButtons()

    def decreaseWidgetSize(self):

        if (self.TotalIfs > 1):
            self.content.layout.removeWidget(self.content.subBtn)
            self.content.subBtn.deleteLater()
            self.content.subBtn = None
            self.content.layout.removeWidget(self.content.elseLbl)
            self.content.elseLbl.deleteLater()
            self.content.elseLbl = None
            self.content.layout.removeWidget(self.content.addBtn)
            self.content.addBtn.deleteLater()
            self.content.addBtn = None   
            
            self.content.layout.removeWidget(self.content.comboBox[self.TotalIfs - 1])
            self.content.comboBox[self.TotalIfs - 1].setParent(None) 
            self.content.comboBox.pop()
            self.content.edit.pop()

            self.TotalIfs = self.TotalIfs - 1
            
            self.content.subBtn = QPushButton('-', self.content)
            self.content.addBtn = QPushButton('+', self.content)
            self.content.elseLbl = QLabel('Else', self.content)
            self.content.elseLbl.setAlignment(Qt.AlignCenter)
            
            self.content.layout.addWidget(self.content.subBtn, self.TotalIfs + 1, 2)
            self.content.layout.addWidget(self.content.elseLbl, self.TotalIfs + 1, 3)
            self.content.layout.addWidget(self.content.addBtn, self.TotalIfs + 1, 1)
            
            self.TotalOutputs.pop(-2)
            self.newSockets([1], self.TotalOutputs, False)

            self.grNode.height -= 43

            self.registerButtons()

        else:
            print('Must have at least one if statement!')

