
from Capstone.test.conf import * ## im really not sure if we can path like this
class DataConnections:
    """Class holds the data for a DataConnectionsMenu and its parent Node (e.g restful service node)"""
    #We can then reference this data in the content portion for display, and later for processing nodes
    # SEE test/conf.py for OPERATION and TYPE Constants
    def __init__(self): ##simple params for our object
        self.valueCount = 0; # default as zero
        self.valList = []

    def _valListContains(self, valTargetPair): # bool check if list has element (for add and remove)
        if(valTargetPair in self.valList):
            return True
        return False

    def _addValueTargetPair(self, valTargetPair=""):
        if(valTargetPair == ""):
            valTargetPair = ValueTargetPair()
        if(self._valListContains(valTargetPair)): # if element already in list
            print("Duplicates not allowed") # warning message?
            return
        self.valList.append(valTargetPair)
    
    def _removeValueTargetPair(self):
        if(len(self.valList) > 0): # if list not empty
            self.valList.pop() # remove last element
        print("DataConncetion: cant remove element, empty list") # warning message?

    def print(self): # Debug utility # print the list
        print("Debug Printing dataConnections model , size of list is "+str(len(self.valList)))
        print("valCount ==> " +str(self.valueCount))
        for x in self.valList:
            print("Value ==> "+ str(x.value))
            print("target ==> "+str(x.target))

class ValueTargetPair: # simple data struct for our objects for use with dataConnectionsMenu
    #NOTE that the value here may be for instance a variable, state.x
    # the actual VALUE of state.x is unknown until runtime.
    #your node must process these valueTargetPairs inside of its doEval function
    def __init__(self , val="" , tar=""):
        self.value = val
        self.target = tar
    def _setValue(self , val):
        self.value = val
    def _setTarget(self , tar):
        self.target = tar
    def _setValueTarget(self , val , tar):
        self.value = val
        self.target = tar
        
      