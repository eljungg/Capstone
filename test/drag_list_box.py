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
        self.addItem('Variable', 'icons/mul.png', OP_CODE_VARIABLE)
        self.addItem('Calculate', 'icons/mul.png', OP_CODE_CALCULATE)
        self.addItem('Data', 'icons/mul.png', OP_CODE_DATA)
        self.addItem('Merge', 'icons/mul.png', OP_CODE_MERGE)
        self.addItem('If', 'icons/in.png', OP_CODE_IF)
        self.addItem('Join', 'icons/in.png', OP_CODE_JOIN)
        self.addItem('Print Line', 'icons/in.png', OP_CODE_PRINT_LINE)
        self.addItem('Simple Dialog', 'icons/in.png', OP_CODE_SIMPLE_DIALOG)
        self.addItem('Terminal Print', 'icons/in.png', OP_CODE_TERMINAL_PRINT)


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