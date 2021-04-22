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
import keyboard
from pynput import keyboard
from pynput.keyboard import Key, Controller, Listener

start_threads = []
threads = []
windowContent = []
myDict = []
key_press_Merge = False

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

                # if(currentNode.op_code == OP_CODE_SIMPLE_DIALOG): // just gonna handle in doEval()
                #     self._simpleDialogEx(parentData) #broken? -luke     Very broken -Ceres

                if(currentNode.op_code == OP_CODE_IF):
                    ifValue = True

                elif(currentNode.op_code == OP_CODE_SWITCH):
                    switchValue = True
                
                elif(currentNode.op_code == OP_CODE_TTS):
                    speak = True

                currentNode.doEval(parentData) #evaluate the current node, parentData is the data object from parent node if applicable
                parentData = currentNode.data # save data object for passing to child node
                self.printNodeMessages(parentData, speak) # print any messages resulting from our doEval() function.

                if(currentNode.op_code == OP_CODE_CUSTOM_ACTIVITY):
                    nextNodes = [currentNode.innerInput]
                elif(currentNode.op_code == OP_CODE_CAOUT):
                    nextNodes = currentNode.CAParent.getChildrenNodes()
                else:
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
                        else:
                            moreChildren = False
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
                    return parentData
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

    def printNodeMessages(self, dataObject, speak): # prints all a nodes messages, and then clears them
        for msg in dataObject.messages: # iterate any messages
            if(type(msg) == str): #verify type
                self._window.appendText(msg + '\n') # any given msg string to the print_line execution window
                if speak:
                    engine = pyttsx3.init()
                    engine.say(msg)
                    engine.runAndWait()
                    engine.stop()
            else:
                print("printNodeMessages passed non-string type error") #Debug
        dataObject.clearMessages() # clear all messages after printing

    def startnode(self, node):
        t = threading.Thread(target=self.threadExecute, args=(node,), daemon=True)
        threads.append(t)
        t.start()