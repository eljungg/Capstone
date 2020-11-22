from PyQt5.QtCore import *

from vpl_conf import *
from vpl_node_base import *

from nodeeditor.utils import dumpException

# ADDITIONAL_IFS used to keep track of the # of how many rows
# in the QGridLayout there are (n - 1 if statement with 1 extra row)
ADDITIONAL_IFS = 2
DEBUG = True

class VPLIfContent(QDMNodeContentWidget):
    def initUI(self):

        # Setup of all the widgets needed
        self.edit = QLineEdit('' , self)
        self.edit.setAlignment(Qt.AlignCenter)
        self.subBtn = QPushButton('-', self)
        self.addBtn = QPushButton('+', self)
        self.elseLbl = QLabel('Else', self)
        self.elseLbl.setAlignment(Qt.AlignCenter)

        # Set up layout
        self.layout = QGridLayout()

        self.layout.addWidget(self.edit, 1, 1, 1, 3)
        self.layout.addWidget(self.subBtn, 2, 1)
        self.layout.addWidget(self.elseLbl, 2, 2)
        self.layout.addWidget(self.addBtn, 2, 3)
        self.setLayout(self.layout)

    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res

        except Exception as e:
            dumpException(e)

        return res

@register_node(OP_NODE_IF)
class VPLNode_If(VPLNode):
    icon = 'icons/if.png'
    op_code = OP_NODE_IF
    op_title = 'If'
    content_label_objname = 'vpl_node_if'

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content = VPLIfContent(self)
        self.grNode = VPLGraphicsNode(self)
        self.grNode.height = 100
        self.grNode.width = 210
         
        self.registerButtons()
        

    def registerButtons(self):
        self.content.subBtn.clicked.connect(self.decreaseWidgetSize)
        self.content.addBtn.clicked.connect(self.increaseWidgetSize)

    def increaseWidgetSize(self):
        try:
            # will have to change this to account for multiple if nodes
            # maybe make a local copy
            global ADDITIONAL_IFS
            self.grNode.height = self.grNode.height + 20
            if DEBUG:
                print('Add button clicked!')

            # increment global variable ADDITIONAL IFS
            ADDITIONAL_IFS = ADDITIONAL_IFS + 1

            # remove current bottom row (buttons + else label)
            if DEBUG:
                print('REMOVING BOTTOM ROW')
            self.content.layout.removeWidget(self.content.subBtn)
            self.content.subBtn.setParent(None)
            self.content.layout.removeWidget(self.content.elseLbl)
            self.content.elseLbl.setParent(None)
            self.content.layout.removeWidget(self.content.addBtn)
            self.content.addBtn.setParent(None)

            # for some reason, must redefine widgets
            if DEBUG:
                print('REDEFINING WIDGETS')        
            self.content.edit = QLineEdit('' , self.content)
            self.content.edit.setAlignment(Qt.AlignCenter)
            self.content.subBtn = QPushButton('-', self.content)
            self.content.addBtn = QPushButton('+', self.content)
            self.content.elseLbl = QLabel('Else', self.content)
            self.content.elseLbl.setAlignment(Qt.AlignCenter)

            # add redefined widgets back into the layout
            if DEBUG:
                print('ADDING WIDGETS BACK INTO LAYOUT')
            numIfs = ADDITIONAL_IFS - 1
            self.content.layout.addWidget(self.content.edit, numIfs, 1, 1, 3)
            self.content.layout.addWidget(self.content.subBtn, ADDITIONAL_IFS, 1)
            self.content.layout.addWidget(self.content.elseLbl, ADDITIONAL_IFS, 2)
            self.content.layout.addWidget(self.content.addBtn, ADDITIONAL_IFS, 3)

            # must reregister buttons because they are new
            if DEBUG:
                print('REGISTERING BUTTONS')  
            self.registerButtons()

        except Exception as e:
            dumpException(e)

    # i commented this section out to focus on the strange program crashes from the add button
    def decreaseWidgetSize(self):
        print('Sub button clicked!')
        if (self.grNode.height > 100):
            '''
            global ADDITIONAL_IFS
            self.grNode.height = self.grNode.height - 20
            if DEBUG:
                print('Add button clicked!')

            # increment global variable ADDITIONAL IFS
            ADDITIONAL_IFS = ADDITIONAL_IFS - 1

            # remove current bottom row
            if DEBUG:
                print('REMOVING BOTTOM ROW')
            self.content.layout.removeWidget(self.content.subBtn)
            self.content.subBtn.setParent(None)
            self.content.layout.removeWidget(self.content.elseLbl)
            self.content.elseLbl.setParent(None)
            self.content.layout.removeWidget(self.content.addBtn)
            self.content.addBtn.setParent(None)

            if DEBUG:
                print('REMOVING BOTTOM IF STATEMENT')
            
            # Remove row at ADDITIONAL_IFS
            
            
            
            
            # for some reason, must redefine widgets
            if DEBUG:
                print('REDEFINING WIDGETS')        
            self.content.edit = QLineEdit('' , self.content)
            self.content.edit.setAlignment(Qt.AlignCenter)
            self.content.subBtn = QPushButton('-', self.content)
            self.content.addBtn = QPushButton('+', self.content)
            self.content.elseLbl = QLabel('Else', self.content)
            self.content.elseLbl.setAlignment(Qt.AlignCenter)

            if DEBUG:
                print('ADDING WIDGETS BACK INTO LAYOUT')
            numIfs = ADDITIONAL_IFS - 1
            self.content.layout.addWidget(self.content.edit, numIfs, 1, 1, 3)
            self.content.layout.addWidget(self.content.subBtn, ADDITIONAL_IFS, 1)
            self.content.layout.addWidget(self.content.elseLbl, ADDITIONAL_IFS, 2)
            self.content.layout.addWidget(self.content.addBtn, ADDITIONAL_IFS, 3)      
            '''
            if DEBUG:
                print('REGISTERING BUTTONS')  

            #self.registerButtons()
        else:
            print('Must have at least one if statement!')
        
        self.registerButtons()
        '''
    def subClicked(self):
        pass
  
    def addClicked(self):
        global ADDITIONAL_IFS
        if DEBUG:
            print('Add button clicked!')
        
        # increment global variable ADDITIONAL IFS
        ADDITIONAL_IFS = ADDITIONAL_IFS + 1

        # remove current bottom row
        if DEBUG:
            print('REMOVING BOTTOM ROW')
        self.layout.removeWidget(self.subBtn)
        self.subBtn.setParent(None)
        self.layout.removeWidget(self.elseLbl)
        self.elseLbl.setParent(None)
        self.layout.removeWidget(self.addBtn)
        self.addBtn.setParent(None)

        # for some reason, must redefine widgets
        self.edit = QLineEdit('' , self)
        self.edit.setAlignment(Qt.AlignCenter)
        self.subBtn = QPushButton('-', self)
        self.addBtn = QPushButton('+', self)
        self.elseLbl = QLabel('Else', self)
        self.elseLbl.setAlignment(Qt.AlignCenter)

        numIfs = ADDITIONAL_IFS - 1
        self.layout.addWidget(self.edit, numIfs, 1, 1, 3)
        self.layout.addWidget(self.subBtn, ADDITIONAL_IFS, 1)
        self.layout.addWidget(self.elseLbl, ADDITIONAL_IFS, 2)
        self.layout.addWidget(self.addBtn, ADDITIONAL_IFS, 3)        
        '''
