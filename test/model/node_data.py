
from Capstone.test.conf import * ## im really not sure if we can path like this
class NodeData:
    """This is a class which will hold the data for each individual node"""
    #We can then reference this data in the content portion for display, and later for processing nodes
    # SEE test/conf.py for OPERATION and TYPE Constants
    def __init__(self): ##simple params for our object
        print("Node Data Model has been created!")
        self.nodeType = None # will contain opcode that defines type
        self.val = None # Simpler than .vals List, Didnt want to delete vals[] if anyone was using it.mro
        self.valType = None #Simpler than .valsType List, didnt want to delete ValsType[] if anyoe was using it
        self.id = None #The node's id in case look back is needed (join)
    

    def print(self): # Debug utility
        print(f"nodeType = {self.nodeType}")
        print(f"val = {self.val}")
        print(f"valType = {self.valType}" )