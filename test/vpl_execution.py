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

# Library for Python tts library. 
# Luke, on Linux you need to make sure that 'espeak' and 'ffmpeg' are installed
# For everyone else, just pip install pyttsx3. 
# If you recieve errors such as No module named win32com.client, No module named win32, or No module named win32api, you will need to additionally install pypiwin32.

import pyttsx3

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
            #if(node.op_code == OP_CODE_JOIN):
                #self._registerJoinNode(node)

    def threadExecute(self, startNode, pData=None):
        parentData = pData
        currentNode = startNode
        moreChildren = True
        nextNodes = []
        ifValue = False
        switchValue = False
        speak = False

        engine = pyttsx3.init()

        if (startNode.op_code == OP_CODE_MERGE or startNode.op_code == OP_CODE_JOIN):
            self._window.appendText("Error, you cannot have a Merge or Join activity as Start-Node!" + '\n')
        else:
            while moreChildren:

                if(currentNode.op_code == OP_CODE_SIMPLE_DIALOG):
                    self._simpleDialogEx(parentData) #broken? -luke     Very broken -Ceres

                elif(currentNode.op_code == OP_CODE_IF):
                    ifValue = True

                elif(currentNode.op_code == OP_CODE_SWITCH):
                    switchValue = True
                
                elif(currentNode.op_code == OP_CODE_TTS):
                    speak = True

                currentNode.doEval(parentData) #evaluate the current node, parentData is the data object from parent node if applicable
                parentData = currentNode.data # save data object for passing to child node
                self.printNodeMessages(parentData, speak, engine) # print any messages resulting from our doEval() function.

                nextNodes = currentNode.getChildrenNodes()

                if nextNodes != []:
                    if(ifValue):
                        outputNodes = currentNode.getOutputs(parentData.val)
                        if(len(outputNodes) > 0):
                            currentNode = outputNodes[0]
                            if len(outputNodes) > 1:
                                for node in outputNodes[1:]:
                                    #print("new thread from child\n")
                                    t = threading.Thread(target=self.threadExecute, args=(node, parentData), daemon=True)
                                    threads.append(t)
                                    t.start()
                        ifValue = False
                    elif(switchValue):
                        currentNode = nextNodes[parentData.val]
                        switchValue = False
                    elif(currentNode.op_code == OP_CODE_JOIN and not parentData.val):
                        moreChildren = False
                        #join node returned empty list, not ready, let thread die. Non-empty list will pass through and execute normally.
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

            engine.stop()

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

    def printNodeMessages(self, dataObject, speak, engine): # prints all a nodes messages, and then clears them
        for msg in dataObject.messages: # iterate any messages
            if(type(msg) == str): #verify type
                self._window.appendText(msg + '\n') # any given msg string to the print_line execution window
                if speak:
                    engine.say(msg)
                    engine.runAndWait()
            else:
                print("printNodeMessages passed non-string type error") #Debug
        dataObject.clearMessages() # clear all messages after printing
