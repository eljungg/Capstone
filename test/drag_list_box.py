from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from conf import *
from nodeeditor.utils import dumpException


class QDMDragListBox(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)

        self.addItems()



    def addItems(self):
        self.addItem('Variable', None, OP_CODE_VARIABLE)
        self.addItem('Calculate', None, OP_CODE_CALCULATE)
        self.addItem('Data', None, OP_CODE_DATA)
        self.addItem('Join', None, OP_CODE_JOIN)
        self.addItem('3Join', None, OP_CODE_JOIN3)
        self.addItem('Merge', None, OP_CODE_MERGE)
        self.addItem('If', None, OP_CODE_IF)
        self.addItem('Switch', None, OP_CODE_SWITCH)
        self.addItem('While', None, OP_CODE_WHILE)
        self.addItem('End While', None, OP_CODE_END_WHILE)
        self.addItem('Break', None, OP_CODE_BREAK)
        self.addItem('Comment', None, OP_CODE_COMMENT)

        self.addItem('Code Activity - Python', None, OP_CODE_CODEPY)
        self.addItem('Key Press Event', None, OP_CODE_KEYPRESS)
        self.addItem('Key Release Event', None, OP_CODE_KEYRELEASE)
        self.addItem('Print Line', None, OP_CODE_PRINT_LINE)
        self.addItem('Random', None, OP_CODE_RANDOM)
        self.addItem('RESTful Service', None, OP_CODE_REST)
        self.addItem('Simple Dialog', None, OP_CODE_SIMPLE_DIALOG)
        self.addItem('Text-To-Speech', None, OP_CODE_TTS)
        self.addItem('Timer', None, OP_CODE_TIMER)

        self.addItem('Terminal Print', None, OP_CODE_TERMINAL_PRINT)



    def addItem(self, name, icon=None, op_code=0):
        item = QListWidgetItem(name, self)
        pixmap = QPixmap(icon if icon is not None else '.')
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(32, 32))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, op_code)

    def startDrag(self, *args, **kvargs):

        try:
            item = self.currentItem()
            op_code = item.data(Qt.UserRole + 1)

            pixmap = QPixmap(item.data(Qt.UserRole))
            
            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap
            dataStream.writeInt(op_code)
            dataStream.writeQString(item.text())

            mimeData = QMimeData()
            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            #drag.setPixmap(pixmap)
            drag.setHotSpot(QPoint(pixmap.width()/2, pixmap.height()/2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e: 
            dumpException(e)