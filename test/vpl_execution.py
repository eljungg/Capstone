#potential execution method
#scene passes list of nodes and edges into this class which handles the actual 
#execution using node functions to find inputs to nodes

import threading
from nodeeditor.node_node import Node
from nodeeditor.node_edge import Edge
from nodeeditor.node_socket import *
from conf import *
from execution_window import ExecutionWindow

from collections import deque
import threading
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

start_threads = []
threads = []
windowContent = []

class _DialogWindow(QWidget):
    def __init__(self, simpleDialog=True):
        super().__init__()
        self.windowString = ""
        self.setFixedWidth(600)
        self.setFixedHeight(600)
        self.layout = QVBoxLayout()

        self.textArea = QLabel()
        self.textArea.setText(self.windowString)
        self.textArea.setFixedWidth(580)
        self.textArea.setFixedHeight(500)
        self.layout.addWidget(self.textArea)

        self.button = QPushButton()
        self.button.setFixedWidth(120)
        self.button.setFixedHeight(50)
        if simpleDialog:
            self.button.setText("Ok")
        else:
            self.button.setText("Stop")
        self.layout.addWidget(self.button)
        #self.button.clicked.connect(self.buttonClicked())

        self.setLayout(self.layout)

        self.show()

    def buttonClicked(self):
        self.close()

    
    def appendLabel(self, string):
        self.windowString += string
        self.textArea.setText(self.windowString)

class _joinData():
    def __init__(self, nodeId, size):
        self.nodeId = nodeId
        self.size = size
        self.queueList = []

        for i in range(size):
            self.queueList.append(deque())

    def addEntry(self, position, entry):
        returnList = []
        if(position < 0 or position >= self.size):
            print("Error: position is out of range")
        else:
            self.queueList[position].append(entry)
            full = True
            for i in self.queueList:
                if not self.queueList[i]:
                    full = False
            if full:
                for i in self.queueList:
                    returnList.append(self.queueList[i].popleft())
        return returnList


class VplExecution():

    def __init__(self, nodes: list=[], edges: list=[]):
        self._nodes = nodes
        self._edges = edges
        self._startNodes = []
        self._nodeQueue = deque()
        self._findStartNodes()
        self._window = ExecutionWindow(False)
        self.dialogOpen = False
        self.str = "Program started.\n"
        self._threads = list()
        self._joinNodeList = []

    def _registerJoinNode(self, node):
        self._joinNodeList.append(_joinData(node.size, node.id))

    def _addEntrytoJoinNode(self, nodeId, position, entry):
        returnList = []
        for n in self._joinNodeList:
            if(self._joinNodeList[n].nodeId == nodeId):
                #semaphore blocking here
                returnList = self._joinNodeList[n].addEntry(position, entry)
                #semaphore release here
    
    def _findStartNodes(self):
        for node in self._nodes:
            if(node.getInput() == None):
                self._startNodes.append(node)
            if(node.op_code == OP_CODE_JOIN):
                self._registerJoinNode(node)

    def threadExecute(self, startNode, pData=None):
        parentData = pData
        currentNode = startNode
        moreChildren = True
        nextNodes = []
        ifValue = False
        switchValue = False

        if (startNode.op_code == OP_CODE_MERGE or startNode.op_code == OP_CODE_JOIN):
            self._window.appendText("Error, you cannot have a Merge or Join activity as Start-Node!" + '\n')
        else:
            while moreChildren:

                if(currentNode.op_code == OP_CODE_SIMPLE_DIALOG):
                    self._simpleDialogEx(parentData) #broken? -luke     Very broken -Ceres

                elif(currentNode.op_code == OP_CODE_PRINT_LINE):
                    self._window.appendText(str(parentData.val) + '\n') #prints val from parents NodeData object

                elif(currentNode.op_code == OP_CODE_IF):
                    ifValue = True

                elif(currentNode.op_code == OP_CODE_SWITCH):
                    switchValue = True

                currentNode.doEval(parentData) #evaluate the current node, parentData is the data object from parent node if applicable
                parentData = currentNode.data # save data object for passing to child node

                nextNodes = currentNode.getChildrenNodes()
                if nextNodes != []:
                    if(ifValue and parentData.val):
                        currentNode = nextNodes[0]
                        ifValue = False
                    elif(ifValue and not parentData.val):
                        currentNode = nextNodes[1]
                        ifValue = False
                    elif(switchValue and parentData.val):
                        currentNode = nextNodes[0]
                        switchValue = False
                    elif(switchValue and not parentData.val):
                        currentNode = nextNodes[1]
                        switchValue = False
                    else:
                        currentNode = nextNodes[0]
                        #print("continuing thread\n")
                        if len(nextNodes) > 1:
                            for node in nextNodes[1:]:
                                #print("new thread from child\n")
                                t = threading.Thread(target=self.threadExecute, args=(node, parentData), daemon=True)
                                threads.append(t)
                                t.start()

                else:
                    moreChildren = False
                    #print("Ending a thread\n")

    def startExecution(self):
        self._window.show()
        for node in self._startNodes:
            t = threading.Thread(target=self.threadExecute, args=(node,), daemon=True)
            threads.append(t)
            #print("Starting a thread\n")
            t.start()
            #self._nodeQueue.append(node)
            #self._executeNodes()
            #print("end of thread.")
