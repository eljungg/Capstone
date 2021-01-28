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

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

start_threads = []
threads = []
windowContent = []

array = []
queue = []

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

    #def close(self):



    

class VplExecution():

    def __init__(self, nodes: list=[], edges: list=[]):
        self._nodes = nodes
        self._edges = edges
        self._startNodes = []
        self._nodeQueue = deque()
        self._findStartNodes()
        self._window = _ExecutionWindow(False)
        self.dialogOpen = False
        self.str = "Program started.\n"

    def _findStartNodes(self):
        for node in self._nodes:
            if(node.getInput() == None):
                queue.append(node)
                array.append(queue)
                #self._startNodes.append(node)

    def startExecution(self):
        #for node in self._startNodes:
        for start in queue:
            array.append(start)

            #self._nodeQueue.append(node)
            self._executeNodes()
            print("end of thread.")

        windowContent.append("Test")
        #print("Opening sub window")
        window = ExecutionWindow(True)
        window.show()
             
    def _executeNodes(self):
        #this should be changed to multithreaded implementation
        nextValue = None
        while self._nodeQueue: #continues until nodeQueue is empty
            nodeEx = self._nodeQueue.popleft()
            if(nodeEx.op_code == OP_CODE_SIMPLE_DIALOG):
                self._dialogOpen = True
                if(nextValue == None):
                    line = "ERROR, no value passed to simple dialog\n"
                else:
                    line = nextValue + '\n'
                newWindow = _DialogWindow()
                newWindow.appendLabel(line)
                #while self._dialogOpen

            edgeThread = nodeThread(target=nodeEx.doEval, args=(nextValue,))
            start_threads.append(edgeThread)

            edgeThread.start()
            nextValue = edgeThread.join()
            
            #execute the node node.implementation()
            #nodevalue = nodeEx.evalImplemantation(nodeValue)
            #save its value
            #execute
            for node in nodeEx.getChildrenNodes():
                self._nodeQueue.append(node)
        
class nodeThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return
        