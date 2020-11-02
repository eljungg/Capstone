
from Capstone.test.conf import * ## im really not sure if we can path like this
class NodeData:
    """This is a class which will hold the data for each individual node"""
    #We can then reference this data in the content portion for display, and later for processing nodes
    # SEE test/conf.py for OPERATION and TYPE Constants
    def __init__(self): ##simple params for our object
        print("Node Data Model has been created!")
        self.nodeType = None # will contain opcode that defines type
        self.vals = [] # list, can handle multiple data vals
        self.valsTypes = [] # matching list to vals, holds type infor for each val. e.g TYPE_STRING, TYPE_INT
        self.name = "Name me"
        self.operations = [] # list for storing operations E.G OPERATION_IF OPERATION_ELSE
        # as of right now, none of this is private and there are no setters etc.
    

    def print(self): # Debug utility
        print(f"nodeType = {self.nodeType}")
        print("vals = ")
        for x in self.vals:
            print(x)
        print("valsTypes = ")
        for y in self.valsTypes:
            print(y)
        print("name = " , self.name)
        print("operations =")
        for z in self.operations:
            print(z)