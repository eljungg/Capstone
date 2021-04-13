from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from model.variables import Variable
from conf import *
# from util import valTypeToString
# from util import stringToValType

class DataConnectionsMenu(QDialog): #general popup window for managing data connections on RESTful node and others
    def __init__(self, parent): # should probably take in desired size from parent ? TODO
        super().__init__(parent=parent)
        self.setWindowTitle("Data Connections")

        self.dialogButtons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(self.dialogButtons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        #layout seems to just be HBox with Two Vboxes
        self.outtestVbox = QVBoxLayout()
        self.outterHbox = QHBoxLayout() #outter

        self.leftGroupBox = QGroupBox("Value")
        self.rightGroupBox = QGroupBox("Target")
        self.leftGroupVbox = QVBoxLayout()
        self.leftGroupBox.setLayout(self.leftGroupVbox)
        self.rightGroupVbox = QVBoxLayout()
        self.rightGroupBox.setLayout(self.rightGroupVbox)

        self.createNewRow() # PROOF OF CONCEPT
        self.createNewRow()

        self.outtestVbox.addLayout(self.outterHbox)
        self.outtestVbox.addWidget(self.buttonBox)
        self.outterHbox.addWidget(self.leftGroupBox)
        self.outterHbox.addWidget(self.rightGroupBox)

        self.setLayout(self.outtestVbox)

        #TODO determine amount of lineEdits from the node itself.
        #TODO data structure to share with nodes

    def createNewRow(self, leftVal="leftTODO" , rightVal="rightTODO"): # might need an index or soemthing im not sure
        #create two line edits, add them to appropriate boxes
        leftLineEdit = QLineEdit(leftVal)
        rightLineEdit = QLineEdit(rightVal)

        initialList = ['value' , 'true', 'false']
        
        comboLeft = QComboBox(self)
        comboRight = QComboBox(self)
        comboLeft.addItems(initialList)
        comboRight.addItems(initialList)
        comboLeft.setLineEdit(leftLineEdit)
        comboRight.setLineEdit(rightLineEdit)
        self.leftGroupVbox.addWidget(comboLeft)
        self.rightGroupVbox.addWidget(comboRight)

