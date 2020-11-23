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
        self.variableVBox = QVBoxLayout() ## we will add line edits for each item in variables array?

        ##TODO##
        #This loop needws to be built into a function, and we need to redraw it on the addBtn call
        #so it will right away show you new variables
        # for variable in self.variablesListRef.variables:
        #     le = QLineEdit(variable) #We need something selectable, Im not sure this is proper widget....
        #     le.setAlignment(Qt.AlignLeft)
        #     le.setReadOnly(True)
        #     self.variableVBox.addWidget(le)
        self.addVarsToVBox() # this will iterate the current variables list, and make QLineEdits for each, and add it to variableVBox

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
        self.innerHBox.addLayout(self.variableVBox)
        self.innerHBox.addLayout(self.innerButtonBox)
        #end inner Hbox
        self.outterVBox.addWidget(self.typeLbl)
        self.outterVBox.addWidget(self.typeDropDown)
        self.outterVBox.addWidget(self.buttonBox)

        self.wireUpMenu() #set click events etc // controller

    def wireUpMenu(self): #wire up events for menu
        self.addBtn.clicked.connect(self.addVariable)
        self.addBtn.clicked.connect(self.addVarsToVBox)

    def addVariable(self): ##function for adding a variable to global list.
        varToAdd = self.varInput.text()
        ### TYPE UNUSED, TODO####
        varType = self.typeDropDown.currentData() # should get opcode type
        self.variablesListRef.variables.append(varToAdd)
        self.parentNodeContent.reDrawVariablesDropDown() # redraw combo box when we get a change

    def addVarsToVBox(self):
        for variable in self.variablesListRef.variables:
            #TODO#### We need to delete EXISTING QLineEdits or it breaks display when you add more than one###
            
            le = QLineEdit(variable) #We need something selectable, Im not sure this is proper widget....
            le.setAlignment(Qt.AlignLeft)
            le.setReadOnly(True)
            self.variableVBox.addWidget(le)


    def deleteVariable(self):
        ### NEEDS TO BE BUILT####
        #TODO#
        return
