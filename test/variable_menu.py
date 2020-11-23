from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Capstone.test.conf import *

class VariableMenu(QDialog):
    def __init__(self, parent, variablesListRef):
        super().__init__(parent=parent) ## might need kwargs nonsense
        self.setWindowTitle("Variable Selection")
        
        self.parentNodeContent = parent
        self.variablesListRef = variablesListRef
        dialogButtons = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(dialogButtons)
        self.buttonBox.accepted.connect(self.accept)

        #Layouts
        self.outterVBox = QVBoxLayout()
        self.innerHBox = QHBoxLayout()
        self.innerButtonBox = QVBoxLayout()
        self.setLayout(self.outterVBox)

        ##Widgets
        self.varLbl = QLabel("Variables:")
        self.varLbl.setAlignment(Qt.AlignLeft)
        self.varInput = QLineEdit("variableName" , self)
        self.varQList = QListWidget()
        self.addVarsToQList() # this will iterate the current variables list, and make QLineEdits for each, and add it to variableVBox

        self.addBtn = QPushButton("Add")
        self.deleteBtn = QPushButton("Delete")
        self.typeLbl = QLabel("Type:")
        #Combo box dropdown for selecting type for a variable.
        self.typeDropDown = QComboBox(self)
        self.typeDropDown.addItem("Integer" , TYPE_INT)
        self.typeDropDown.addItem("Double" , TYPE_DOUBLE)
        self.typeDropDown.addItem("Boolean" , TYPE_BOOL)
        self.typeDropDown.addItem("Char" , TYPE_CHAR)
        self.typeDropDown.addItem("String" , TYPE_STRING)

        ##Build button box###
        self.innerButtonBox.addWidget(self.addBtn);
        self.innerButtonBox.addWidget(self.deleteBtn)
        ###Build the thing####
        self.outterVBox.addWidget(self.varLbl)
        self.outterVBox.addWidget(self.varInput)
        self.outterVBox.addLayout(self.innerHBox)
        self.innerHBox.addWidget(self.varQList)
        self.innerHBox.addLayout(self.innerButtonBox)
        #end inner Hbox
        self.outterVBox.addWidget(self.typeLbl)
        self.outterVBox.addWidget(self.typeDropDown)
        self.outterVBox.addWidget(self.buttonBox)

        self.wireUpMenu() #set click events etc // controller

    def wireUpMenu(self): #wire up events for menu
        self.addBtn.clicked.connect(self.addVariable)
        self.addBtn.clicked.connect(self.addVarsToQList)

    def addVariable(self): ##function for adding a variable to global list.
        varToAdd = self.varInput.text()
        ### TYPE UNUSED, TODO####
        varType = self.typeDropDown.currentData() # should get opcode type
        self.variablesListRef.variables.append(varToAdd)
        self.parentNodeContent.reDrawVariablesDropDown() # redraw combo box when we get a change

    def addVarsToQList(self):
        self.varQList.clear() # clear old contents of listbox
        for variable in self.variablesListRef.variables: #populate listbox from variables 'global' list
            QListWidgetItem(variable , self.varQList)

    def deleteVariable(self):
        ### NEEDS TO BE BUILT####
        #TODO#
        return
