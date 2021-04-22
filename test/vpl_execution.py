#potential execution method
#scene passes list of nodes and edges into this class which handles the actual 
#execution using node functions to find inputs to nodes

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from nodeeditor.node_node import Node
from nodeeditor.node_edge import Edge
from nodeeditor.node_socket import *

from execution_window import ExecutionWindow
from conf import *

import threading
import time
import pyttsx3
import keyboard
from collections import deque
from pynput import keyboard
from pynput.keyboard import Key, Controller, Listener

# Library for Python tts library. 
# Luke, on Linux you need to make sure that 'espeak' and 'ffmpeg' are installed
# For everyone else, just pip install pyttsx3. 
# If you recieve errors such as No module named win32com.client, No module named win32, or No module named win32api, you will need to additionally install pypiwin32.

start_threads = []
threads = []
windowContent = []
myDict = []
key_press_Merge = False
whileNodes = []
endWhileNodes = []

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
        whileValue = False

        engine = pyttsx3.init()

        if (startNode.op_code == OP_CODE_MERGE or startNode.op_code == OP_CODE_JOIN):
            self._window.appendText("Error, you cannot have a Merge or Join activity as Start-Node!" + '\n')

        elif (startNode.op_code == OP_CODE_KEYPRESS):
            keyEle = currentNode.getKey()
            def on_press(key):
                global myDict
                if isinstance(keyEle, str):
                    if key == keyboard.Key.esc:
                        print("Listener Closed!")
                        return False
                    elif key.char == keyEle:
                        if not key.char in myDict:
                            print("New key Pressed: " + key.char)
                            if(startNode.getChildrenNodes()[0].op_code== OP_CODE_MERGE):
                                self.key_press_Merge = True
                            for node in startNode.getChildrenNodes():
                                self.startnode(node)
                            myDict.append(key.char)
                            print("List: ", myDict)
                else:
                    COMBINATION = {keyEle[0], keyEle[1]}
                    if key == keyboard.Key.esc:
                        print("Listener Closed!")
                        return False
                    elif key.char in COMBINATION:
                        if not key.char in myDict:
                             print("New key Pressed: " + key.char)
                             if (startNode.getChildrenNodes()[0].op_code == OP_CODE_MERGE):
                                 self.key_press_Merge = True
                             for node in startNode.getChildrenNodes():
                                 self.startnode(node)
                             myDict.append(key.char)
                             print("List: ", myDict)

            def on_release(key):
                print('{0} released'.format(key))
                if key.char in myDict:
                    myDict.remove(key.char)
                print("List: ", myDict)

            time.sleep(0.2)
            with Listener(on_press=on_press, on_release=on_release) as listener:  # Create an instance of Listener
                listener.join()
            breakpoint()

        elif (startNode.op_code == OP_CODE_KEYRELEASE):
            def on_release(key):
                print('{0} release'.format(key))
                if (startNode.getChildrenNodes()[0].op_code == OP_CODE_MERGE):
                    self.key_press_Merge = True
                for node in startNode.getChildrenNodes():
                    self.startnode(node)
            time.sleep(1)
            listener = keyboard.Listener(
                on_release=on_release)
            listener.start()
            breakpoint()

        else:
            while moreChildren:

                if(currentNode.op_code == OP_CODE_SIMPLE_DIALOG):
                    self._simpleDialogEx(parentData) #broken? -luke     Very broken -Ceres

                elif(currentNode.op_code == OP_CODE_IF):
                    ifValue = True

                elif(currentNode.op_code == OP_CODE_SWITCH):
                    switchValue = True

                elif(currentNode.op_code == OP_CODE_WHILE):
                    whileNodes.append([currentNode, parentData])
                    print(currentNode)
                    whileValue = True

                elif(currentNode.op_code == OP_CODE_TTS):
                    speak = True

                # Checks to see if the node is an End While node and the corresponding While node has a 'true' condition
                if(currentNode.op_code == OP_CODE_END_WHILE and whileValue):
                    currentNode = whileNodes[-1][0]
                    parentData = whileNodes[-1][1]

                currentNode.doEval(parentData) #evaluate the current node, parentData is the data object from parent node if applicable
                parentData = currentNode.data # save data object for passing to child node
                self.printNodeMessages(parentData, speak, engine) # print any messages resulting from our doEval() function.
                nextNodes = currentNode.getChildrenNodes()

                if nextNodes != []:
                    if(ifValue):
                        # If the node is an If node, choose the corresponding socket based on the correct statement
                        outputNodes = currentNode.getOutputs(parentData.val)

                        # If the socket has connected edges
                        if(len(outputNodes) > 0):
                            currentNode = outputNodes[0]

                            # Spawn a new thread if there are more than one edges connected to the socket
                            if len(outputNodes) > 1:
                                for node in outputNodes[1:]:
                                    t = threading.Thread(target=self.threadExecute, args=(node, parentData), daemon=True)
                                    threads.append(t)
                                    t.start()
                        else:
                            moreChildren = False
                        ifValue = False                        
                    elif(switchValue):
                        # If the node is an If node, choose the corresponding socket based on the correct statement
                        outputNodes = currentNode.getOutputs(parentData.val)
                        
                        # If the socket has connected edges
                        if(len(outputNodes) > 0):
                            currentNode = outputNodes[0]

                            # Spawn a new thread if there are more than one edges connected to the socket
                            if len(outputNodes) > 1:
                                for node in outputNodes[1:]:
                                    t = threading.Thread(target=self.threadExecute, args=(node, parentData), daemon=True)
                                    threads.append(t)
                                    t.start()
                        else:
                            moreChildren = False
                        switchValue = False
                    # If the node was a While node and it was a 'false' condition  
                    elif(whileValue and parentData.val == False):
                        noEndWhile = True
                        
                        # Search for the End While node
                        for nodeThread in nextNodes:
                            if(nodeThread.op_code == OP_CODE_END_WHILE):
                                currentNode = nodeThread
                                noEndWhile = False
                                whileValue = False
                                whileNodes.pop(-1)
                                break
                            else:
                                nodeAfter = nodeThread.getChildrenNodes()
                                while(nodeAfter != []):
                                    if(nodeAfter[0].op_code == OP_CODE_END_WHILE):
                                        currentNode = nodeAfter[0]
                                        noEndWhile = False
                                        whileValue = False
                                        whileNodes.pop(-1)
                                        break
                                    else:
                                        nodeAfter = nodeAfter[0].getChildrenNodes()
                        
                        # Check to see if there is an End While node connected the the sequence of nodes
                        if(noEndWhile):
                            self._window.appendText("Error, you cannot have a While node without an End While node!" + '\n')

                        whileValue = False
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

    def startnode(self, node):
        t = threading.Thread(target=self.threadExecute, args=(node,), daemon=True)
        threads.append(t)
        t.start()