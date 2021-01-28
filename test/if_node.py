from PyQt5.QtCore import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode

DEBUG = False
ADDITIONAL_IFS = 1
INITIAL_OUTPUTS = 2


class IfNodeContent(QDMNodeContentWidget):
    def initUI(self):

        # Setup of all the widgets needed
        
        self.edit = QLineEdit('' , self)
        self.edit.setAlignment(Qt.AlignCenter)
        self.subBtn = QPushButton('-', self)
        self.addBtn = QPushButton('+', self)
        self.elseLbl = QLabel('Else', self)
        self.elseLbl.setAlignment(Qt.AlignCenter)

        # Set up initial layout
        '''
        self.layout = QGridLayout()

        self.layout.addWidget(self.edit, 1, 1, 1, 3)
        self.layout.addWidget(self.subBtn, 2, 1)
        self.layout.addWidget(self.elseLbl, 2, 2)
        self.layout.addWidget(self.addBtn, 2, 3)
        self.setLayout(self.layout)
        '''
        # Attempt at a nested layout once again
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.edit)
        
        self.bottomRow = QHBoxLayout()
        self.bottomRow.addWidget(self.subBtn)
        self.bottomRow.addWidget(self.elseLbl)
        self.bottomRow.addWidget(self.addBtn)

        self.layout.addLayout(self.bottomRow)
        self.setLayout(self.layout)
    
    #I hope these are correct
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


class IfNode(VplNode):
    icons = "Capstone/icons/in.png"
    op_code = OP_CODE_IF
    op_title = "If"
    content_label_objname = "VplNodeIf"

    def __init__(self, scene, title:str="If"):
        super().__init__(scene, title, inputs = [1], outputs = [1,INITIAL_OUTPUTS])

    def initInnerClasses(self):
        self.content = IfNodeContent(self)
        self.grNode = VplGraphicsNode(self)

        self.grNode.height = 100
        self.grNode.width = 210
         
        self.content.subBtn.clicked.connect(self.decreaseWidgetSize)
        self.content.addBtn.clicked.connect(self.increaseWidgetSize)


    def increaseWidgetSize(self):

        global ADDITIONAL_IFS
        ADDITIONAL_IFS = ADDITIONAL_IFS + 1
        # increase size of graphical node
        self.grNode.height = self.grNode.height + 24
        self.clearWidgets(self.content.layout)

        
        # Reset the widget layout
        for i in range(0, ADDITIONAL_IFS):
            self.newEditLine = QLineEdit('')
            self.content.layout.addWidget(self.newEditLine)
        bottomRow = QHBoxLayout()
        bottomRow.addWidget(self.content.subBtn)
        bottomRow.addWidget(self.content.elseLbl)
        bottomRow.addWidget(self.content.addBtn)

        self.content.layout.addLayout(bottomRow)
        self.content.setLayout(self.content.layout)

    def decreaseWidgetSize(self):
        if (self.grNode.height > 100):
            
            # Decrement global IF count
            global ADDITIONAL_IFS
            ADDITIONAL_IFS = ADDITIONAL_IFS - 1

            self.clearWidgets(self.content.layout)
            self.grNode.height = self.grNode.height - 24
            
            
            for i in range(0, ADDITIONAL_IFS):
                self.newEditLine = QLineEdit('')
                self.content.layout.addWidget(self.newEditLine)
            '''
            self.content.layout = QVBoxLayout()
            self.newEditLine = QLineEdit('')
            self.content.layout.addWidget(self.newEditLine)
            self.content.setLayout(self.content.layout)
            '''

            bottomRow = QHBoxLayout()
            bottomRow.addWidget(self.content.subBtn)
            bottomRow.addWidget(self.content.elseLbl)
            bottomRow.addWidget(self.content.addBtn)

            self.content.layout.addLayout(bottomRow)
            self.content.setLayout(self.content.layout)

        else:
            print('Must have at least one if statement!')
        
    def clearWidgets(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clearWidgets(item.layout())