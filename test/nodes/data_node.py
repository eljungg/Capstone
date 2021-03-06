from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base
from Capstone.test.conf import *
from model.node_data import NodeData
from util import *

class DataContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.edit = QLineEdit("" , self)
        self.edit.setAlignment(Qt.AlignLeft)
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
        super().__init__(scene, inputs=[0], outputs=[0])
        self.title = "Data"

    def initInnerClasses(self):
        self.content = DataContent(self)
        self.grNode = VplGraphicsNode(self)
        self.grNode.height = 90
        #below is onTextChanged event for simple self.edit Label
        self.content.edit.textChanged.connect(self.onInputChanged)
        self.content.edit.textChanged.connect(self.doDataType)
        self.content.edit.textChanged.connect(self.onTextChange)
        #self.data = NodeData() # THIS FIXES SCOPING ISSUE,
        self.data.nodeType = self.op_code
        self.data.id = self.id

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

    def doDataType(self):
        ### Determine the type of data given in Text Box by user ###
        self.data.val = (self.content.edit.text())
        valType = determineDataType(self.data.val) # get the VPL_TYPE
        self.data.valType = valType
        typeStr = valTypeToString(valType)
        self.content.typeLabel.setText(typeStr)
 
        
    def doEval(self, parentData=None): 
        #does literally nothing. 
        #as of now, getting the type and data are handled in determineDataType() # saved to self.data
        self.data.val = (self.content.edit.text())
        return
