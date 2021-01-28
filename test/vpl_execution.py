#potential execution method
#scene passes list of nodes and edges into this class which handles the actual 
#execution using node functions to find inputs to nodes


from nodeeditor.node_node import Node
from nodeeditor.node_edge import Edge
from nodeeditor.node_socket import *
from conf import *
from execution_window import ExecutionWindow

from collections import deque
import threading

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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
        self.str = "Program XXstarted.\n" # this is nothing??
        self._threads = list() # is this even the list you access calling threads? no _threads? # is this list used???

    def _findStartNodes(self):
        for node in self._nodes:
            if(node.getInput() == None):
                self._startNodes.append(node)
                

    def threadExecute(self, startNode):
        ##Big Picture:
        ##Spin a thread for each start node
        ##Run that nodes activity.
        ## all data we need is accessed via node.data object
        ##TODO## Handle getting info from parent nodes?
        currentNode = startNode
        parentNodes = currentNode.getInputs() #this doesnt work, returns empty list

        nextNodes = []
        moreChildren = True #flag for controlling this thread continueing to more nodes or not
        self._window.appendText("One Thread Spawned!" + '\n')
        while moreChildren:
            self._window.appendText("One Node Processed!" + '\n')
            nextNodes = currentNode.getChildrenNodes() #function returns IMMEDIATE children only
            #Regardless of how we handle the children, current node must be dealt with also
            currentNode.doActivity() #calls base class in VplNode, over-write in your specific node class

            if(len(nextNodes) == 0):
                #CASE 0, no children.
                moreChildren = False
            if(len(nextNodes) > 0): # there are more nodes, dont kill thread
                #CASE # 1a, have some children
                print("CASE 1a")
                print(str(type(currentNode)) + "and the next " +str(type(nextNodes[0])))
                currentNode = nextNodes[0] # move forward like a linked list
                if(len(nextNodes) > 1):
                    #CASE #1b , have more than one children, do we spawn a new thread???
                    print("CASE 1b")
                    for node in nextNodes[1:]: # syntax to skip the first node, which will be run on this thread
                        print("spawn a 1b child node!\n")
                        t = threading.Thread(target=self.threadExecute, args=(node,), daemon=True)
                        threads.append(t)
                        t.start()

     
        print("Thread dies") # end of thread, no more children and this thread executed

    def startExecution(self):
        self._window.show()
        for node in self._startNodes:
            t = threading.Thread(target=self.threadExecute, args=(node,), daemon=True)
            threads.append(t)
            t.start()

        
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

