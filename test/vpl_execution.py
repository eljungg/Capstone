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

threads = []
myDict = [] #Used for Key Press nodes
key_press_Merge = False

class VplExecution():
    """ Class handles execution of the program formed by the nodes """
    def __init__(self, nodes: list=[], edges: list=[]):
        """
        :Instance Attributes:

            - **_nodes** - list of `Nodes` given to execution
            - **_edges** - list of `Edges` given to execution

        """
        self._nodes = nodes
        self._edges = edges
        self._startNodes = []
        self._findStartNodes()
        self._window = ExecutionWindow(False)
        self.dialogOpen = False
        self.str = "Program started.\n"
    
    def _findStartNodes(self):
        """Checks all nodes to see if they have a parent node. If not, add the node to the start list."""
        for node in self._nodes:
            if(node.getInput() == None):
                self._startNodes.append(node)

    def threadExecute(self, startNode, pData=None):
        """Executes program defined by nodes"""
        parentData = pData #data from parent node to be passed to child/current node
        currentNode = startNode #Node currently being processed
        moreChildren = True
        nextNodes = [] #list of node(s) to be executed next
        ifValue = False
        switchValue = False
        speak = False


        if (startNode.op_code == OP_CODE_MERGE or startNode.op_code == OP_CODE_JOIN):
            #These nodes should not be at the start of a program
            self._window.appendText("Error, you cannot have a Merge or Join activity as Start-Node!" + '\n')

        elif (startNode.op_code == OP_CODE_KEYPRESS): #special handling for keypress node
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

        elif (startNode.op_code == OP_CODE_KEYRELEASE): #special handling for keyrelase node
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

        else: #normal handling for nodes
            while moreChildren:

                #set flags as needed for certain nodes.
                if(currentNode.op_code == OP_CODE_IF):
                    ifValue = True

                elif(currentNode.op_code == OP_CODE_SWITCH):
                    switchValue = True
                
                elif(currentNode.op_code == OP_CODE_TTS):
                    speak = True

                elif (currentNode.op_code == OP_CODE_CODEPY):
                    result = currentNode.getOutValue(parentData)
                    self._window.appendText(result.val + '\n')

                #general execution for nodes
                currentNode.doEval(parentData) #evaluate the current node, parentData is the data object from parent node if applicable
                parentData = currentNode.data # save data object for passing to child node
                self.printNodeMessages(parentData, speak) # print any messages resulting from our doEval() function.

                #determine which nodes will be executed next
                if(currentNode.op_code == OP_CODE_CUSTOM_ACTIVITY):
                    nextNodes = [currentNode.innerInput]
                elif(currentNode.op_code == OP_CODE_CAOUT):
                    nextNodes = currentNode.CAParent.getChildrenNodes()
                else:
                    nextNodes = currentNode.getChildrenNodes()

                if nextNodes != []: #If there are more nodes after current...
                    if(ifValue): #Special handling for if nodes
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
                    elif(switchValue): #special handling for switch nodes
                        currentNode = nextNodes[parentData.val]
                        switchValue = False
                    elif(currentNode.op_code == OP_CODE_JOIN and not parentData.val): #special handling for join nodes
                        moreChildren = False
                        #join node returned empty list, not ready, let thread die. Non-empty list will pass through and execute normally.
                    else: # normal handling for nodes
                        currentNode = nextNodes[0] #continue thread with first available node in next
                        if len(nextNodes) > 1:
                            for node in nextNodes[1:]: #if there are more nodes, create threads for remaining children
                                t = threading.Thread(target=self.threadExecute, args=(node, parentData), daemon=True)
                                threads.append(t)
                                t.start()

                else: 
                    moreChildren = False #no more children, while loop will ends, thread will die.
                    return parentData
                    #print("Ending a thread\n")

            

    def startExecution(self):
        """Spawns a thread for each node in the `_startNodes` list."""
        self._window.show()
        for node in self._startNodes:
            t = threading.Thread(target=self.threadExecute, args=(node,), daemon=True)
            threads.append(t)
            t.start()

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