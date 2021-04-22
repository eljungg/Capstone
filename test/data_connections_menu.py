from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from model.variables import Variable
from conf import *

#This file contains the QDialog popup menu for data connections,
#TODO we will need a ref to variablesList here

class DataConnectionsMenu(QDialog): #general popup window for managing data connections on RESTful node and others
    def __init__(self, parent , dataConnectionsModel): # should probably take in desired size from parent ? TODO
        super().__init__(parent=parent)
        self.model = dataConnectionsModel # get access to our model.
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

        for i in range(0,self.model.valueCount): # make a row and set value for each of our stuffs
            # print("DEBUG FROM data_con_menu self.model.valueCount ==>" + str(self.model.valueCount))
            self.createNewRow(leftVal = self.model.valList[i].value , rightVal = self.model.valList[i].target , index=i)

        self.outtestVbox.addLayout(self.outterHbox)
        self.outtestVbox.addWidget(self.buttonBox)
        self.outterHbox.addWidget(self.leftGroupBox)
        self.outterHbox.addWidget(self.rightGroupBox)

        self.setLayout(self.outtestVbox)

    def createNewRow(self, leftVal="leftTODO" , rightVal="rightTODO" , index=-1): # might need an index or soemthing im not sure
        #Leftval is the val
        #rightVal is the target
        #rightVal is non editable 
        leftLineEdit = QLineEdit(leftVal)
        rightLbl = QLabel(rightVal)
        initialList = ['value' , 'true', 'false'] #taken from calculate node, give user hints for possible options
        #TODO user hints for variables as well?
        comboLeft = QComboBox(self)
        comboLeft.addItem(leftVal)
        comboLeft.addItems(initialList)
        comboLeft.setLineEdit(leftLineEdit)
        self.leftGroupVbox.addWidget(comboLeft)
        self.rightGroupVbox.addWidget(rightLbl)

        self.buttonBox.accepted.connect(lambda : self.model.valList[index]._setValue(leftLineEdit.text()))
     

