import io
import sys
from io import StringIO

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.utils import dumpException
from vpl_node import *  # get our custom node base
from Capstone.test.conf import *
from model.node_data import NodeData
from conf import OP_CODE_CODEPY

OutputValue = 0
NodeName = ""


class CODE_ACT_PY_Graphics(QDMGraphicsNode):

    def initSizes(self):
        super().initSizes()
        self.width = 210
        self.height = 150
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10


class CodeActivityPythonContent(QDMNodeContentWidget):

    def initUI(self):
        key_list1 = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "f", "e", "f", "g", "h", "i", "j",
                     "k", "l", "m", "n", "o", "p", "q", "r", "s",
                     "t", "u", "v", "w", "x", "y", "z"]

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.combo = QComboBox(self)

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
        self.combo.addItems(key_list1)
        self.button = QPushButton("Edit Code")
        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.button)

    def serialize(self):
        pass

    def deserialize(self, data, hashmap={}):
        pass


class CodeActivityPythonNode(VplNode):
    op_code = OP_CODE_CODEPY

    def __init__(self, scene):
        super().__init__(scene, inputs=[0], outputs=[0])

    def initInnerClasses(self):
        self.content = CodeActivityPythonContent(self)
        self.grNode = CODE_ACT_PY_Graphics(self)
        self.content.button.clicked.connect(self.buttonClicked)
        self.data.nodeType = self.op_code
        self.data.id = self.id
        self.w = AnotherWindow()

    def getOutValue(self, input=None):
        global NodeName
        NodeName = self.getKey()
        mytext = self.w.codeEdit.toPlainText()
        old_stdout = sys.stdout
        # keep a named handle on io.StringIO() buffer
        new_stdout = io.StringIO()
        # Redirect python stdout into the builtin io.StringIO() buffer
        sys.stdout = new_stdout
        # variable contains python code referencing external memory
        if input != None:

            InputValue = input.val
        else:
            InputValue = "No input data from parent nodes"
        exec(mytext)

        # stdout from mytext is read into a variable
        result = sys.stdout.getvalue().strip()
        # put stdout back to normal
        sys.stdout = old_stdout
        self.data.val = result
        return self.data

    def doEval(self, input=None):
        NodeName = self.getKey()
        g = dict()
        l = dict()

        mytext = self.w.codeEdit.toPlainText()
        if input != None:
            InputValue = input.val
        exec(mytext)
        self.data.val = OutputValue
        return self.data

    def onChanged(self, text):
        self.previousText = text

    def buttonClicked(self):
        # self.codeEdit = QPlainTextEdit()
        # self.content.layout.addWidget(self.codeEdit)
        # self.w.codeEdit.setPlainText(self.previousText)
        self.w.show()

    def stdoutIO(stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

    def getKey(self):
        return self.content.combo.currentText()


class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("code edit")
        layout.addWidget(self.label)
        self.codeEdit = QPlainTextEdit()
        self.codeEdit.setMinimumSize(1000, 400)
        self.codeEdit.setPlainText("#Edit your code here: "
                                   "Input from outside Node is stored in variable 'InputValue'. \n"
                                   "#Node Output is stored in variable 'OutputValue', which is set to be 1 as default value."
                                   "\nglobal OutputValue\nglobal NodeName\nprint('Code Activity '+ NodeName + ':') \n#------------------------------------------------------------------------------\n\n"

                                   "print(InputValue)\n\n\n\n\n\n\n\n\n\nOutputValue = 1"
                                   ""
                                   "")
        self.setLayout(layout)
        self.layout().addWidget(self.codeEdit)