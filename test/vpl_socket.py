from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_socket import QDMGraphicsSocket
from nodeeditor.node_socket import *
from nodeeditor.utils import dumpException
from model.node_data import NodeData

class VplGraphicsSocket(QDMGraphicsSocket):
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self._brush)
        painter.setPen(self._pen if not self.isHighlighted else self._pen_highlight)
        painter.drawPie(-self.radius, -self.radius - 15, 40, 40, 150 * 16, 60 * 16)

        '''
        rectangle = QRectF(-self.radius, -self.radius + 7, 40, 40)
        startAngle = 150 * 16
        spanAngle = 60 * 16
        painter.drawPie(rectangle, startAngle, spanAngle)
        '''

class VplSocket(Socket):
    Socket_GR_Class = VplGraphicsSocket

    def __init__(self, node:'Node', index:int=0, position:int=LEFT_TOP, socket_type:int=1, multi_edges:bool=True, count_on_this_node_side:int=1, is_input:bool=False):
        super().__init__(node, index, position, socket_type, multi_edges, count_on_this_node_side, is_input)