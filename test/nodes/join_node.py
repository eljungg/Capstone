from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from vpl_node import *
from conf import *
from nodeeditor.utils import dumpException
from nodeeditor.node_graphics_node import QDMGraphicsNode
from collections import deque

# TODO: Add resizability to join node, like if and switch.

class JoinNodeContent(VplContent):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.conditional1 = QLineEdit("", self)
        self.conditional1.setAlignment(Qt.AlignLeft)
        self.conditional1.setObjectName(self.node.content_label_objname)
        self.conditional2 = QLineEdit("", self)
        self.conditional2.setAlignment(Qt.AlignLeft)
        self.conditional2.setObjectName(self.node.content_label_objname2)

        self.layout.addWidget(self.conditional1)
        self.layout.addWidget(self.conditional2)
        #To imitate VIPLE we'll want to implement a way to add extra
        #fields. probably another function and graphics
    
    def serialize(self):
        res = super().serialize()
        res['value1'] = self.conditional1.text()
        res['value2'] = self.conditional2.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value1 = data['value1']
            value2 = data['value2']
            self.conditional1.setText(value1)
            self.conditional2.setText(value2)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


class JoinNode(VplNode):
    icons = "icons/in.png"
    op_code = OP_CODE_JOIN
    op_title = "Join"
    content_label_objname = "VplNodeJoin"
    content_label_objname2 = "VplNodeJoin"

    def __init__(self, scene, title:str="Join"):
        super().__init__(scene, title, inputs = [0, 0], outputs = [0])
        self.eval()

    def initInnerClasses(self):
        self.content = JoinNodeContent(self)
        self.grNode = VplGraphicsNode(self)
        self.content.conditional1.textChanged.connect(self.onInputChanged)
        self.content.conditional2.textChanged.connect(self.onInputChanged)
        self.data.nodeType = self.op_code
        self.data.id = self.id
        self.size = 2 #default value
        self.queueList = [] #queues for each input of the join node
        #will need to be change on size update
        for i in range(self.size):
            self.queueList.append(deque())

    def addEntry(self, position, entry):
        returnList = []
        if(position == None):
            pass
        elif(position < 0 or position >= self.size):
            print("Error: position is out of range")
        else:
            self.queueList[position].append(entry) # append entry to the proper queue
            full = True
            for i in self.queueList: # i is one of the queues in the list
                if not (i): #if i is empty... returnList will remain empty and be returned
                    full = False
            if full: # if no queues are empty...
                for i in self.queueList:
                    returnList.append(i.popleft())
                returnList.reverse() #nodeeditor has the bottom socket as 0 so the entries are backwards from what one would expect.

        return returnList

    def doEval(self, input=None):
        if (input != None):
            inputpos = self.findParentFromSocket(input.id)
            temp = []
            temp = self.addEntry(inputpos, input.val) #add entry returns a list
            returndict = {} #dictionary formed by text fields and list returned by addEntry
            if(temp): #if addEntry didn't return an empty list.
                #will need to be altered for resizable nodes
                returndict[str(self.content.conditional1.text())] = temp[0]
                returndict[str(self.content.conditional2.text())] = temp[1]
            self.data.val = returndict
            return returndict

        else:
            print("ERROR, join recieved a null input")
            