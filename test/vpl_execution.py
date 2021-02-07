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
threads = []


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

    def _findStartNodes(self):
        for node in self._nodes:
            if(node.getInput() == None):
                self._startNodes.append(node)

    def threadExecute(self, startNode, nextVal=None):
        nextValue = nextVal
        currentNode = startNode
        moreChildren = True
        nextNodes = []
        while moreChildren:
            #print("start while\n")
            if(currentNode.op_code == OP_CODE_SIMPLE_DIALOG):
                self._simpleDialogEx(nextValue)
                
            elif(currentNode.op_code == OP_CODE_PRINT_LINE):
                self._window.appendText(nextValue + '\n')
            
            nextValue = currentNode.doEval(nextValue)

            nextNodes = currentNode.getChildrenNodes()
            if nextNodes != []:
                currentNode = nextNodes[0]
                #print("continuing thread\n")
                if len(nextNodes) > 1:
                    for node in nextNodes:
                        #print("new thread from child\n")
                        t = threading.Thread(target=self.threadExecute, args=(node, nextValue), daemon=True)
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

    #Old non-threaded function. Not currently in use.         
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

            """
                self._simpleDialogEx(nextValue)
                
            elif(nodeEx.op_code == OP_CODE_TERMINAL_PRINT):
                if(nextValue == None):
                    print("ERROR, no value passed to simple dialog\n")
                else:
                    print(nextValue)
            elif(nodeEx.op_code == OP_CODE_PRINT_LINE):
                self._window.appendText(nextValue + '\n')

            elif(nodeEx.op_code == OP_CODE_DATA):
                nextValue = nodeEx.doEval()

            elif(nodeEx.op_code == OP_CODE_CALCULATE):
                nextValue = nodeEx.content.edit.text()
            """

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

class printWindow(QWidget):
    def __init__(self, windowContent):
        super().__init__()
        self.windowContent = windowContent

        layout = QVBoxLayout()
        for i in windowContent:
            self.l = QLabel(i)
            layout.addWidget(self.l)

        b = QPushButton("Stop")
        b.pressed.connect(self.on_click)
        b.pressed.connect(self.close)

        layout.addWidget(b)

        self.setLayout(layout)

    def on_click(self):
        for n in start_threads:
            if n.is_alive():
                n.join()
            nextValue = nodeEx.doEval(nextValue)

            for node in nodeEx.getChildrenNodes():
                self._nodeQueue.append(node)
        
    def _simpleDialogEx(self, nextValue):
        print("entered simple dialog")
        self._dialogOpen = True
        if(nextValue == None):
            line = "ERROR, no value passed to simple dialog\n"
        else:
            line = nextValue + '\n'
        newWindow = ExecutionWindow(True)
        newWindow.appendText(line) 
        newWindow.show()
