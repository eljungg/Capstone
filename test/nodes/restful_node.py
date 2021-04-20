from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.utils import dumpException
from vpl_node import * # get our custom node base
from conf import *
from node_data import NodeData
import requests
import xml.etree.ElementTree as ET
from data_connections_menu import DataConnectionsMenu

class RestfulServiceContent(QDMNodeContentWidget):
    def initUI(self):
        self.dataConnectionsDialog = DataConnectionsMenu(self)
        self.layout = QVBoxLayout()
        self.propertiesBtn = QPushButton("Properties") # VIPLE has on rightclick instead
        self.dataConnectionsBtn = QPushButton("Data Connections") # VIPLE has on right click instead
        self.layout.addWidget(self.propertiesBtn)
        self.layout.addWidget(self.dataConnectionsBtn)
        self.setLayout(self.layout)
        self.initModel()

    def initModel(self):
        self.model = RestModel()
        print("Rest Model Created")
        
    def setContentVariables(self, variablesListRef):
        self.variablesListRef = variablesListRef
    
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
        self.propertiesDialog = RestfulDialog(self, self.variablesListRef)
        self.propertiesDialog.show()
        #self.propertiesDialog.exec_()  
    def showDataConnectionsDialog(self):
        self.dataConnectionsDialog.show()
class RestfulServiceNode(VplNode):
    op_code = OP_CODE_DATA
    TotalOutputs = [0,1]
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[3]) # was 3

    def initInnerClasses(self):
        self.content = RestfulServiceContent(self)
        self.grNode = VplGraphicsNode(self)
        self.grNode.height = 90

        self.data.nodeType = self.op_code
        self.data.id = self.id

        self._connectView()

    def _connectView(self):
        self.content.propertiesBtn.clicked.connect(self.content.showPropertiesDialog)
        self.content.dataConnectionsBtn.clicked.connect(self.content.showDataConnectionsDialog)

    def doEval(self, parentData=None): 
        #self.data.messages.append(self.content.model.endPointURL)
        output = ""
        try: #do webRequest
            r = requests.get(self.content.model.endPointURL)
            output = r.text
        except: # webRequest failed
            output = "RESTful service failed"
        try: #strip xml trags
            
            tree = ET.fromstring(output)
            notags = ET.tostring(tree, encoding='utf8', method='text')
            print(notags)
            output = str(notags , 'UTF-8')
        except:
            pass
        self.data.val = output #set result of service call as our data
        self.__setDataType()
        print("data type of rest call == > " + str(self.data.valType))
        return

    def __setDataType(self):
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

    def setVariableData(self, variables): # wires up stuff, see subWindow.py
        self.variablesRef = variables
        self.content.setContentVariables(self.variablesRef)


class RestfulDialog(QDialog):
    def __init__(self, parent, variablesListRef):
        super().__init__(parent=parent)
        self.parentNode = parent
        self.model = self.parentNode.model

        self.setWindowTitle("RESTful Service Settings")
        self.variablesListRef = variablesListRef
        self.dialogButtons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(self.dialogButtons)
        
        #info
        infoTxt = "For uknown values, make a palcehodler. Expected format for placeholders is an integer (starting with 0) in curly braces, for example: {0}."
        #Widgets
        self.infoLbl = QLabel(infoTxt)
        self.endPointLbl = QLabel("Endpoint URL: ")
        self.endPointInput = QLineEdit(self.model.endPointURL)
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
        variableCount = 0
        while( variableCount < self.model.numVars ):
            self.createNewVariableHbox(newFlag=False , number=variableCount)
            variableCount +=1
            print("Going again because varCount =>" +str(variableCount) +" is < self.model.numVars ==>" +str(self.model.numVars))
        ## add dynamic variable HBOXES into self.dynamicVariablesVBox
        self.outterVbox.addLayout(self.plusMinusHBox)
        self.plusMinusHBox.addWidget(self.minusBtn)
        self.plusMinusHBox.addStretch(1)
        self.plusMinusHBox.addWidget(self.plusBtn)
        self.outterVbox.addWidget(self.buttonBox)
        #self.DEBUGBTN = QPushButton("DEBUG") #DEBUG
        #self.outterVbox.addWidget(self.DEBUGBTN) # DEBUG
        #self.DEBUGBTN.clicked.connect(self.printPOS) # DEBUG
        self._connectView()

    def printPOS(self): #DEBUG of positional error
        print("MY POS")
        print(self.pos())
        print("PARENT POS")
        print(self.parentNode.pos())
        #self.move(self.safePOS.x()+ 300 , self.safePOS.y()+ 250)

    def resizeEvent(self, event): #Over-write resize event
        #Trying to debug a tricky problem where the resize of adding new variables throws off the
        #position of the dialog menu after user drag and drop
        #self.printPOS()
        QDialog.resizeEvent(self, event)
        #self.printPOS()
    def createNewVariableHbox(self, newFlag=True , number=-1):
        print("createNext goes with newFlag ==>" + str(newFlag))
        if(number == -1):
            count = self.model.numVars # get amount of current things
        else:
            count = number
        #when plus btn pressed, create a new hbox.
        self.newHbox = QHBoxLayout()
        self.varInput = QLineEdit("Variable "+str(count)) #TODO NEED TO GET VARIABLE NAME FROM MODEL HERE
        self.typeDropDown = QComboBox()
        self.typeDropDown.addItem("Int")
        self.typeDropDown.addItem("Double")
        self.typeDropDown.addItem("Boolean")
        self.typeDropDown.addItem("Char")
        self.typeDropDown.addItem("String")
        self.newHbox.addWidget(self.varInput)
        self.newHbox.addWidget(self.typeDropDown)
        self.dynamicVariablesVBox.addLayout(self.newHbox)
        if(newFlag == True):
            self.model.numVars += 1

    def removeLastVariableHbox(self):
        self.variableHboxCount = self.dynamicVariablesVBox.count() # get total number of
        print("variableHboxCount ==>" +str(self.variableHboxCount))
        if(self.variableHboxCount == 0):
            return #we done here bois
        self.layoutToDelete = self.dynamicVariablesVBox.itemAt(self.variableHboxCount-1)
        self.layoutToDelete.itemAt(0).widget().deleteLater()
        self.layoutToDelete.itemAt(1).widget().deleteLater()
        self.dynamicVariablesVBox.removeItem(self.layoutToDelete)
        self.model.numVars -= 1

    def _connectView(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.plusBtn.clicked.connect(lambda : self.createNewVariableHbox(newFlag=True , number=-1))
        #self.plusBtn.clicked.connect(self._debugVars)
        self.minusBtn.clicked.connect(self.removeLastVariableHbox)
        self.buttonBox.accepted.connect(self._reportEndPointToParent)
        #self.endPointInput.textChanged.connect(self._reportEndPointToParent)
    def _debugVars(self):
        for var in self.variablesListRef.variables:
            var._printVar()
    def _reportEndPointToParent(self):
        urlTxt = self.endPointInput.text()
        #self.parentNode.restURL = urlTxt #TODO will need to format in variables here later
        self.model.endPointURL = urlTxt
        print("reportEndPointTOParent ==>" + urlTxt)

class RestModel():
    def __init__(self):
        self.endPointURL = ""
        self.numVars = 0
        #TODO more variable stuff i imagine



        