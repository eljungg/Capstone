from PyQt5.QtCore import *
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException
from vpl_node import *  # get our custom node base
from Capstone.test.conf import *
from model.node_data import NodeData
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QWidget
from PyQt5.QtCore import Qt


class KeypressContent(QDMNodeContentWidget):
    key_list1 = []
    key_list2 = []

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.combo = QComboBox(self)
        global key_list1
        global key_list2
        key_list1=["a","b","c","d","f","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9"]
        key_list2=["`","-","=","/",",",".","[","]",'\\']
        self.combo.addItems(key_list1)
        self.combo.addItems(key_list2)
        self.combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.combo.setStyleSheet("QComboBox {"
                                    "combobox-popup: 0;\n"  
                                    "border-style:none; "
                                    "padding-left:80px;  " 
                                    "width:48px; "
                                    "height:24px; "
                                    "font-size:24px; "
                                    "font-family:PingFangSC-Regular,PingFang SC; "
                                    "font-weight:400; "
                                    "color:rgba(93,169,255,1);\n"
                                    "line-height:24px; }\n"

                                    "QComboBox:drop-down {"  
                                    "width:40px;  "
                                    "height:50px; "
                                    "border: none;  "
                                    "subcontrol-position: right center; "  
                                    "subcontrol-origin: padding;}\n"  

                                    "")
        self.combo.setMaxVisibleItems(10)
        self.layout.addWidget(self.combo)

        self.addBtn = QPushButton('+', self)
        self.subBtn = QPushButton('-', self)
        self.layout.addWidget(self.addBtn)
        self.layout.addWidget(self.subBtn)


    def serialize(self):
        pass

    def deserialize(self, data, hashmap={}):
        pass


class KeypressNode(VplNode):
    op_code = OP_CODE_KEYPRESS
    op_title = "Key Press Event"
    additionalBox = False

    def __init__(self, scene, title: str = "Key Press Event"):
        super().__init__(scene, title, inputs=[], outputs=[2])

    def initInnerClasses(self):
        self.content = KeypressContent(self)
        self.grNode = VplGraphicsNode(self)
        self.grNode.height = 155
        self.grNode.width = 200
        self.data = NodeData()
        self.data.nodeType = self.op_code
        self.registerButtons()

    def getKey(self):
        if self.additionalBox == True:
            return [self.content.combo.currentText(), self.extaComb.currentText()]
        return self.content.combo.currentText()


    def doEval(self, input=None):
        self.data = input
        return self.data

    def registerButtons(self):
        self.content.addBtn.clicked.connect(self.addonClicked)
        self.content.subBtn.clicked.connect(self.subonClicked)

    def addonClicked(self):
        self.additionalBox = True
        self.content.layout.removeWidget(self.content.subBtn)
        QWidget.hide(self.content.addBtn)
        self.extaComb = QComboBox()
        self.extaComb.setStyleSheet("QComboBox {"
                                    "combobox-popup: 0;\n"  
                                    "border-style:none; "
                                    "padding-left:80px;  " 
                                    "width:48px; "
                                    "height:24px; "
                                    "font-size:24px; "
                                    "font-family:PingFangSC-Regular,PingFang SC; "
                                    "font-weight:400; "
                                    "color:rgba(93,169,255,1);\n"
                                    "line-height:24px; }\n"

                                    "QComboBox:drop-down {"  
                                    "width:40px;  "
                                    "height:50px; "
                                    "border: none;  "
                                    "subcontrol-position: right center; "  
                                    "subcontrol-origin: padding;}\n"  

                                    "")
        global key_list1
        global key_list2
        self.extaComb.addItems(key_list1)
        self.extaComb.addItems(key_list2)
        self.content.layout.addWidget(self.extaComb)
        self.content.layout.addWidget(self.content.subBtn)

    def subonClicked(self):
        self.content.layout.removeWidget(self.content.subBtn)
        QWidget.show(self.content.addBtn)
        QWidget.hide(self.extaComb)
        self.content.layout.addWidget(self.content.addBtn)
        self.content.layout.addWidget(self.content.subBtn)