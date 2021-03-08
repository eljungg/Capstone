from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from model.variables import Variable
from conf import *
from util import valTypeToString
from util import stringToValType


class customSignals(QObject): #custom signals
    focusInVarInp = pyqtSignal()
    focusOutVarInp = pyqtSignal()

s = customSignals() # we need this signal object as shared instance, not in any class

class varLineEdit(QLineEdit): # we have to sub-class this to get event handlers for the on-focus event.
    #onfucous event of varInput to lock the type dropdown
    def __init__(self, *args , **kwargs):
        super(varLineEdit , self).__init__(*args , **kwargs)
    
    def focusInEvent(self, event):
        s.focusInVarInp.emit() # emit custom signals
        super(varLineEdit , self).focusInEvent(event) #make sure and include parent functionality
    def focusOutEvent(self, event):
        s.focusOutVarInp.emit() # emit custom signal
        super(varLineEdit , self).focusOutEvent(event) #make sure and include parent functionality
        #we will catch these emits inside our variableMenu

class VariableMenu(QDialog):
    def __init__(self, parent, variablesListRef , s1):
        super().__init__(parent=parent) ## might need kwargs nonsense
        self.setWindowTitle("Variable Selection")
        self.s1 =s1
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
        self.varInput = varLineEdit("variableName" , self) #for adding new variables input
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
        self.typeDropDown.addItem("Int")
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
        self.currentlySelectedVariable = None

        self._determineTypeDropDownLockStatus() # lock the typeDropDown if no vars yet
        self._connectView(parent) # wire up all the events
        
 
    def _determineTypeDropDownLockStatus(self):
        if (self.variableListBox.count() == 0 or self.currentlySelectedVariable == None): #no entries
            self._lockTypeBox()
        else:
            self._unlockTypeBox()

    def _connectView(self , parent):
        #wire up buttons
        self.addBtn.clicked.connect(self._addVar) # add variable to varList
        self.deleteBtn.clicked.connect(self._deleteVar) # Delete selected variables
        self.variableListBox.itemClicked.connect(self._updateVariableTypeDropdown) # potential weakness, only responds to mouse clicks not tabs or arrows?
        s.focusInVarInp.connect(self._lockTypeBox) # lock typeDropDownwhen adding new vars
        s.focusOutVarInp.connect(self._unlockTypeBox) # unclock typeDropDown
        self.typeDropDown.currentTextChanged.connect(self._setVarTypeFromDropDown) #set varType on variable with typeDropdown

    def _isDuplicateVariable(self , varName): # check for existing var by same name
        if(self.variablesListRef._findVarByName(varName) == None):
            return False # not duplicate
        else:
            return True #is duplicate

    def _lockTypeBox(self): # this is breaking variables stored type info
        self.typeDropDown.setCurrentIndex(-1)
        self.typeDropDown.setEnabled(False) # disable

    def _unlockTypeBox(self):
        self.typeDropDown.setEnabled(True)
        self._updateVariableTypeDropdown(self.currentlySelectedVariable)

    def _updateVariableTypeDropdown(self , item):
        self.currentlySelectedVariable = item;
        if(item == None):
            return
        varName = self.currentlySelectedVariable.text() # get name of variable
        variable = self.variablesListRef._findVarByName(varName)
        varType = variable.valType
        varTypeStr = valTypeToString(varType) # convert to string
        self.typeDropDown.setCurrentText(varTypeStr)
        self.typeDropDown.setEnabled(True)

    def _setVarTypeFromDropDown(self): #on indexChanged of typeDropDown
        if(self.currentlySelectedVariable == None or self.typeDropDown.currentIndex() == -1): # ignore case when dropdown is cleared on inputFocus event or no vars yet
            return #somethings wrong
        varName = self.currentlySelectedVariable.text()
        variable = self.variablesListRef._findVarByName(varName)
        chosenTypeStr = self.typeDropDown.currentText()
        chosenType = stringToValType(chosenTypeStr)
        variable.valType = chosenType
        self.s1.typeChange.emit() # emit cusom event to change the typeLabel on variable node itself real-time

    def _addVar(self):
        varName = self.varInput.text()
        if(self._isDuplicateVariable(varName) == True): #check for duplicate
            self.showDuplicateErrorDialog() # run error popup dialog
            return # dont add variables just end
        varTypeStr = self.typeDropDown.currentText() #get type as text from comboBox
        varType = TYPE_INT # Default value, copied VIPLE.
        varVal = None
        newVar = Variable(varName , varVal , varType) # create Variable Object
        self.variablesListRef._addVariable(newVar) # add Variable object to "global" variables list
        self._drawListBoxEntry(varName) # add item to listbox
        self._determineTypeDropDownLockStatus()
        self.s1.varAdded.emit(varName)

    def showDuplicateErrorDialog(self): #simple popup for warning user attempting to add duplicate variable
        self.errorString = "ERROR: Variable already exists.\n Cannot add duplicate."
        self.dialog = QDialog()
        self.dVBox = QVBoxLayout()
        self.errorLbl = QLabel(self.errorString)
        self.okBtn = QPushButton("OK" , self.dialog) # this button could be smaller
        self.dVBox.addWidget(self.errorLbl)
        self.dVBox.addWidget(self.okBtn)
        self.dialog.setLayout(self.dVBox) # add layout
        self.okBtn.clicked.connect(self.dialog.close)
        self.dialog.show()

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
        self.currentlySelectedVariable = None # reset this because if selected was deleted it breaks
        self._determineTypeDropDownLockStatus()
        self.s1.varDeleted.emit(varName)

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
    
