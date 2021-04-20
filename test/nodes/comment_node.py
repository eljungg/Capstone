from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from vpl_node import *  # get our custom node base
from conf import *

class CommentGraphics(QDMGraphicsNode):

    def initSizes(self):
        super().initSizes()
        self.width = 450
        self.height = 205
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10


class CommentNodeContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.edit = QPlainTextEdit()
        self.layout.addWidget(self.edit)

    def serialize(self):
        pass

    def deserialize(self, data, hashmap={}):
        pass


class CommentNode(VplNode):
    op_code = OP_CODE_COMMENT
    op_title = "Comment"
    content_label_objname = "VplNodeComment"

    def __init__(self, scene, title:str="Comment"):
        super().__init__(scene, title, inputs=[], outputs=[])

    def initInnerClasses(self):
        self.content = CommentNodeContent(self)
        self.grNode = CommentGraphics(self)
        # below is onTextChanged event for simple self.edit Label


