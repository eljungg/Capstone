from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base
from Capstone.test.conf import * 

class CalculateContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.edit = QLineEdit("Calculate Node Class" , self)
        self.edit.setAlignment(Qt.AlignRight)
        self.layout.addWidget(self.edit)
    
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
        super().__init__(scene, inputs=[2], outputs=[1])

    def initInnerClasses(self):
        self.content = CalculateContent(self)
        self.grNode = VplGraphicsNode(self)
        #below is onTextChanged event for simple self.edit Label
        self.content.edit.textChanged.connect(self.onInputChanged)
        self.content.edit.textChanged.connect(self.doCalculations)
        self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code
    
    def doCalculations(self): ## just gonna run python eval
        ### This doesnt handle any variables or anything like that###
        result =""
        try:
            #Danger Warning #Hackable
            result = str(eval(self.content.edit.text() , {}, {}))
            #this is super unsafe. We already imported OS, can do syscalls or spawn a shell or something
        except Exception:
            result = "error"
        
        self.data.val = result
        self.determineDataType() # set type
        #print("Saved Value from Calcualte : "+ self.data.val) ##DEBUG


    ##Borrowed from data_node for easy type check of eval
    def determineDataType(self):
        ### Determine the type of data given in Text Box by user ###
        val = self.data.val
        if self.__isInt(val) == True:
            self.data.valType = TYPE_INT
        elif self.__isFloat(val) == True:
            self.data.valType = TYPE_DOUBLE
        elif self.__isBool(val) == True:
            self.data.valType = TYPE_BOOL
        elif self.__isChar(val) == True:
            self.data.valType = TYPE_CHAR
        else:
            self.data.valType = TYPE_STRING

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

    def doEval(self, input=None) : #input is the NodeData() object of the parent/input node
        return