from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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
        for variable in self.variablesListRef.variables:
            le = QLineEdit(variable) #We need something selectable, Im not sure this is proper widget....
            le.setAlignment(Qt.AlignLeft)
            le.setReadOnly(True)
            self.variableVBox.addWidget(le)
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


