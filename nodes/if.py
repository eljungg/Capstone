from PyQt5.QtCore import *

from vpl_conf import *
from vpl_node_base import *

from nodeeditor.utils import dumpException

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
        self.content.subBtn.clicked.connect(self.content.subClicked)
        self.content.subBtn.clicked.connect(self.decreaseWidgetSize)
        self.content.addBtn.clicked.connect(self.content.addClicked)
        self.content.addBtn.clicked.connect(self.increaseWidgetSize)

    def increaseWidgetSize(self):
        self.grNode.height = self.grNode.height + 20
        self.registerButtons()

    def decreaseWidgetSize(self):
        print('Sub button clicked!')
        if (self.grNode.height > 100):
            self.grNode.height = self.grNode.height - 10
        else:
            print('Must have at least one if statement!')
        
        self.registerButtons()
        