from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.utils import dumpException
from vpl_node import *
from conf import *
from model.variables import VariablesData
from model.node_data import NodeData
from nodeeditor.node_node import *

import re

TotalIfs = 1

class IfNodeContent(QDMNodeContentWidget):
    def __init__(self, parent, variablesRef):
        self.vars = variablesRef
        super().__init__(parent)

    def initUI(self):
        self.layout = QGridLayout()

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
        self.registerButtons()

    def redrawComboBox(self): # function displays new variables in dropdown. (GUI REFRESH)
        global TotalIfs
        self.comboBox[TotalIfs - 1].clear()
        self.comboBox[TotalIfs - 1].addItems(['true', 'false'])
        for var in self.vars.variables:
            self.comboBox[TotalIfs - 1].addItem(var.name)
        self.comboBox[TotalIfs - 1].addItem('value')

    def setContentVariables(self, variables):
        self.vars = variables

    def registerButtons(self):
        self.subBtn.clicked.connect(self.decreaseWidgetSize)
        self.addBtn.clicked.connect(self.increaseWidgetSize)

    def increaseWidgetSize(self):
        global TotalIfs
        TotalIfs = TotalIfs + 1

        self.layout.removeWidget(self.subBtn)
        self.subBtn.deleteLater()
        self.subBtn = None
        self.layout.removeWidget(self.elseLbl)
        self.elseLbl.deleteLater()
        self.elseLbl = None
        self.layout.removeWidget(self.addBtn)
        self.addBtn.deleteLater()
        self.addBtn = None      

        self.comboBox.append(QComboBox(self))
        self.comboBox[TotalIfs - 1].addItems(self.initialList)

        self.edit.append(QLineEdit('' , self))
        self.comboBox[TotalIfs - 1].setLineEdit(self.edit[TotalIfs - 1])

        self.edit[TotalIfs - 1].setAlignment(Qt.AlignCenter)
        
        self.subBtn = QPushButton('-', self)
        self.addBtn = QPushButton('+', self)
        self.elseLbl = QLabel('Else', self)
        self.elseLbl.setAlignment(Qt.AlignCenter)
        
        self.layout.addWidget(self.comboBox[TotalIfs - 1], TotalIfs, 1, 1, 3)        
        
        self.layout.addWidget(self.subBtn, TotalIfs + 1, 2)
        self.layout.addWidget(self.elseLbl, TotalIfs + 1, 3)
        self.layout.addWidget(self.addBtn, TotalIfs + 1, 1)
        
        self.setLayout(self.layout)
        self.redrawComboBox()
        self.registerButtons()

    def decreaseWidgetSize(self):
        global TotalIfs

        if (TotalIfs > 1):
            self.layout.removeWidget(self.subBtn)
            self.subBtn.deleteLater()
            self.subBtn = None
            self.layout.removeWidget(self.elseLbl)
            self.elseLbl.deleteLater()
            self.elseLbl = None
            self.layout.removeWidget(self.addBtn)
            self.addBtn.deleteLater()
            self.addBtn = None   
            
            self.layout.removeWidget(self.comboBox[TotalIfs - 1])
            self.comboBox[TotalIfs - 1].setParent(None) 
            self.comboBox.pop()
            self.edit.pop()

            TotalIfs = TotalIfs - 1
            
            self.subBtn = QPushButton('-', self)
            self.addBtn = QPushButton('+', self)
            self.elseLbl = QLabel('Else', self)
            self.elseLbl.setAlignment(Qt.AlignCenter)
            
            self.layout.addWidget(self.subBtn, TotalIfs + 1, 2)
            self.layout.addWidget(self.elseLbl, TotalIfs + 1, 3)
            self.layout.addWidget(self.addBtn, TotalIfs + 1, 1)
            
            self.setLayout(self.layout)

            self.registerButtons()

        else:
            print('Must have at least one if statement!')
    
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