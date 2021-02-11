from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from model.variables import Variable
from conf import *

class VariableMenu(QDialog):
    def __init__(self, parent, variablesListRef):
        super().__init__(parent=parent) ## might need kwargs nonsense
        self.setWindowTitle("Variable Selection")

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
        self.variableListBox = QListWidget() # list for storing our vars
        self.variableVBox.addWidget(self.variableListBox)
        for variable in self.variablesListRef.variables:
            self._drawListBoxEntry(variable.name)

        self.addBtn = QPushButton("Add")
        self.deleteBtn = QPushButton("Delete")
        self.typeLbl = QLabel("Type:")
        #Combo box dropdown for selecting type for a variable.
        self.typeDropDown = QComboBox(self)
        self.typeDropDown.addItem("Integer")
        self.typeDropDown.addItem("Double")
        self.typeDropDown.addItem("Boolean")
        self.typeDropDown.addItem("Char")
        self.typeDropDown.addItem("String")

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

        #wire up buttons
        self.addBtn.clicked.connect(self._addVar) # add variable to varList
        self.addBtn.clicked.connect(parent.reDrawVariablesDropDown) # refresh current nodes dropdown when item added
        
        self.deleteBtn.clicked.connect(self._deleteVar) # Delete selected variables
        self.deleteBtn.clicked.connect(parent.reDrawVariablesDropDown) # refresh current nodes dropdown when item deleted
 

    def _addVar(self):
        varName = self.varInput.text()
        varTypeStr = self.typeDropDown.currentText() #get type as text from comboBox
        varType = self._typeStringToOpCode(varTypeStr) # get type as int/enum
        varVal = None # value of variable is not assigned at creation
        newVar = Variable(varName , varVal , varType) # create Variable Object
        self.variablesListRef._addVariable(newVar) # add Variable object to "global" variables list
        self._drawListBoxEntry(varName) # add item to listbox

    def _deleteVar(self):
        selectedVarList = self.variableListBox.selectedItems() # returns list of selected items
        for selected in selectedVarList: # plan on only deleting one at a time, but its set to handle multiple selected it needed
            varName = selected.text()
            variable = self.variablesListRef._findVarByName(varName);
            if(variable == None): #basic error handling, no variable found from name
                print("Variable not found to delete")
            else: # variable found, delete
                self.variablesListRef._deleteVariable(variable)
        self._reDrawListBoxEntries()

    def _typeStringToOpCode(self , typeStr): # just sort out the text from comboBox to actual type enum style
        if(typeStr == "String"):
            return TYPE_STRING
        if(typeStr == "Integer"):
            return TYPE_INT
        if(typeStr == "Double"):
            return TYPE_DOUBLE
        if(typeStr == "Boolean"):
            return TYPE_BOOL;
        if(typeStr == "Char"):
            return TYPE_CHAR

    def _drawVarLineEdit(self , variable): #where variable == string of varName
        le = QLineEdit(variable) #We need something selectable, Im not sure this is proper widget....
        le.setAlignment(Qt.AlignLeft)
        le.setReadOnly(True)
        self.variableVBox.addWidget(le)

    def _drawListBoxEntry(self , variableName):
        listBoxItem = QListWidgetItem(variableName)
        self.variableListBox.addItem(listBoxItem)
        
    def _reDrawListBoxEntries(self):
        self.variableListBox.clear() # clear old
        for variable in self.variablesListRef.variables: # re-draw based on current variables
            self._drawListBoxEntry(variable.name)
    
