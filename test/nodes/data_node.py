from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base
from Capstone.test.conf import *

class DataContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.edit = QLineEdit("Data Node Class" , self)
        self.edit.setAlignment(Qt.AlignRight)
        self.typeLabel = QLabel("none" , self)
        self.typeLabel.setAlignment(Qt.AlignRight)
        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.typeLabel)
    
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
        

class DataNode(VplNode):
    op_code = OP_CODE_DATA
    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])

    def initInnerClasses(self):
        self.content = DataContent(self)
        self.grNode = VplGraphicsNode(self)
        #below is onTextChanged event for simple self.edit Label
        self.content.edit.textChanged.connect(self.onInputChanged)
        self.content.edit.textChanged.connect(self.determineDataType)

    def determineDataType(self):
        ### Determine the type of data given in Text Box by user ###
        self.data.val = (self.content.edit.text())
        val = self.data.val
        if self.__isInt(val) == True:
            self.data.valType = TYPE_INT
            self.content.typeLabel.setText("Int")
        elif self.__isFloat(val) == True:
            self.data.valType = TYPE_DOUBLE
            self.content.typeLabel.setText("Double")
        elif self.__isBool(val) == True:
            self.data.valType = TYPE_BOOL
            self.content.typeLabel.setText("Boolean")
        elif self.__isChar(val) == True:
            self.data.valType = TYPE_CHAR
            self.content.typeLabel.setText("Char")
        else:
            self.data.valType = TYPE_STRING
            self.content.typeLabel.setText("String")

    def __isInt(self , val): #helper function for determineType
        try:
            int(val)
            return True
        except ValueError:
            return False
    def __isFloat(self, val):
        try:
            float(val)
            return True
        except ValueError:
            return False
    def __isBool(self, val):
        lcVal = val.lower()
        if lcVal == "false" or lcVal == "true":
            return True
        else:
            return False
    def __isChar(self, val): #Python doesnt do Char, but VIPLE does so we just emulate?
        if len(val) == 1:
            return True
        else:
            return False