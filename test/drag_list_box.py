from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Capstone.test.conf import *
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
        # self.addItem('Input', 'icons/in.png', OP_CODE_INPUT)
        # self.addItem('Output', 'icons/out.png', OP_CODE_OUTPUT)
        # self.addItem('Add', 'icons/add.png', OP_CODE_ADD)
        # self.addItem('Subtract', 'icons/sub.png', OP_CODE_SUB)
        # self.addItem('Multiply', 'icons/mul.png', OP_CODE_MUL)
        # self.addItem('Divide', 'icons/divide.png', OP_CODE_DIV)
        self.addItem('Variable', 'icons/mul.png', OP_CODE_VARIABLE)
        self.addItem('Calculate', 'icons/mul.png', OP_CODE_CALCULATE)
        self.addItem('Data', 'icons/mul.png', OP_CODE_DATA)
        self.addItem('Merge', 'icons/mul.png', OP_CODE_MERGE)

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
            drag.setPixmap(pixmap)
            drag.setHotSpot(QPoint(pixmap.width()/2, pixmap.height()/2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e: 
            dumpException(e)