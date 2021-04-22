from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base
from Capstone.test.conf import *
from model.node_data import NodeData

class CodeActivityPythonContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
    
    def serialize(self):
        res = super().serialize()
        #res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            #self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res
        

class CodeActivityPythonNode(VplNode):
    op_code = OP_CODE_DATA
    TotalOutputs = [0,1]
    def __init__(self, scene):
        super().__init__(scene, inputs=[0], outputs=[0])

    def initInnerClasses(self):
        self.content = CodeActivityPythonContent(self)
        self.grNode = VplGraphicsNode(self)
        self.grNode.height = 90

        self.data.nodeType = self.op_code
        self.data.id = self.id

    def doEval(self, parentData=None): 
        #does literally nothing. 
        #as of now, getting the type and data are handled in determineDataType() # saved to self.data
        return


