from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base
from Capstone.test.conf import *
from model.node_data import NodeData

class RestfulServiceContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.propertiesBtn = QPushButton("Properties") # temporary / DEBUG
        self.layout.addWidget(self.propertiesBtn)
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

    def showPropertiesDialog(self):
        self.propertiesDialog = RestfulDialog(self, "BADREF_TODO")
        self.propertiesDialog.exec_()
        print("showPropertiesDialog goes")    

class RestfulServiceNode(VplNode):
    op_code = OP_CODE_DATA
    TotalOutputs = [0,1]
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[3])

    def initInnerClasses(self):
        self.content = RestfulServiceContent(self)
        self.grNode = VplGraphicsNode(self)
        self.grNode.height = 90

        self.data.nodeType = self.op_code
        self.data.id = self.id

        self._connectView()

    def _connectView(self):
        self.content.propertiesBtn.clicked.connect(self.content.showPropertiesDialog)

    def doEval(self, parentData=None): 
        #does literally nothing. 
        #as of now, getting the type and data are handled in determineDataType() # saved to self.data
        return


class RestfulDialog(QDialog):
    def __init__(self, parent, variablesListRef):
        super().__init__(parent=parent)
        self.setWindowTitle("RESTful Service Settings")
        self.variablesListRef = variablesListRef
        self.dialogButtons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(self.dialogButtons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        #info
        infoTxt = "For uknown values, make a palcehodler. Expected format for placeholders is an integer (starting with 0) in curly braces, for example: {0}."
        #Widgets
        self.infoLbl = QLabel(infoTxt)
        self.endPointLbl = QLabel("Endpoint URL: ")
        self.endPointInput = QLineEdit()
        self.varLbl = QLabel("Variables: ")
        self.minusBtn = QPushButton("-")
        self.plusBtn = QPushButton("+")
        #layouts
        self.outterVbox = QVBoxLayout()
        self.endPointHbox = QHBoxLayout()
        self.dynamicVariablesVBox = QVBoxLayout()
        self.plusMinusHBox = QHBoxLayout()
        #DYNAMICALLY NEED TO CREATE HBOX WITH Variable LineEdit and QComboBox TODO

        #add widgets to boxes
        self.setLayout(self.outterVbox)
        self.outterVbox.addWidget(self.infoLbl)
        self.outterVbox.addLayout(self.endPointHbox)
        self.endPointHbox.addWidget(self.endPointLbl)
        self.endPointHbox.addWidget(self.endPointInput)
        self.outterVbox.addWidget(self.varLbl)
        self.outterVbox.addLayout(self.dynamicVariablesVBox)
        ## add dynamic variable HBOXES into self.dynamicVariablesVBox
        self.outterVbox.addLayout(self.plusMinusHBox)
        self.plusMinusHBox.addWidget(self.minusBtn)
        self.plusMinusHBox.addStretch(1)
        self.plusMinusHBox.addWidget(self.plusBtn)
        self.outterVbox.addWidget(self.buttonBox)

        self._connectView()

    def createNextVariableHbox(self):
        print("createNext goes")
        #when plus btn pressed, create a new hbox.
        self.newHbox = QHBoxLayout()
        self.varInput = QLineEdit("Variable #")
        self.typeDropDown = QComboBox()
        self.typeDropDown.addItem("Int")
        self.typeDropDown.addItem("Double")
        self.typeDropDown.addItem("Boolean")
        self.typeDropDown.addItem("Char")
        self.typeDropDown.addItem("String")
        self.newHbox.addWidget(self.varInput)
        self.newHbox.addWidget(self.typeDropDown)
        self.dynamicVariablesVBox.addLayout(self.newHbox)

    def removeLastVariableHbox(self):
        self.variableHboxCount = self.dynamicVariablesVBox.count() # get total number of
        print("variableHboxCount ==>" +str(self.variableHboxCount))
        if(self.variableHboxCount == 0):
            return #we done here bois
        self.layoutToDelete = self.dynamicVariablesVBox.itemAt(self.variableHboxCount-1)
        self.layoutToDelete.itemAt(0).widget().deleteLater()
        self.layoutToDelete.itemAt(1).widget().deleteLater()
        self.dynamicVariablesVBox.removeItem(self.layoutToDelete)
        # if(self.variableHboxCount == 0):
        #     print("No variable HBOX?")
        #     return
        # else:
        #     layToDelete = self.dynamicVariablesVBox.itemAt(self.variableHboxCount -1)
        #     # we know its only two variables in each layout
        #     layToDelete.itemAt(0).widget().deleteLater()
        #     layToDelete.itemAt(1).widget().deleteLater()

    def _connectView(self):
        self.plusBtn.clicked.connect(self.createNextVariableHbox)
        self.minusBtn.clicked.connect(self.removeLastVariableHbox)
        


        

        