
from conf import * 

class Variable:
    """This will be object for handling Variables"""
    def __init__(self, nameInp, valInp , valTypeInp):
        self.name = nameInp
        self.val = valInp
        self.valType = valTypeInp
    def _printVar(self): #helpful for #debug
        print("variableObj.name ==" + str(self.name))
        print("variableObj.val ==" + str(self.val))
        print("variableObj.valType ==" +str(self.valType))

class VariablesData:
    """This is a class which will hold the variables for an entire subWindow (instance of VPL)"""
    ###

    def __init__(self): ##simple params for our object
        self.variables = [] # simple list to hold our variables (for now)
    def _addVariable(self, variableObj):
        self.variables.append(variableObj)
    
    def _findVarByName(self, varName): # returns Variable object
        for var in self.variables: # iterate variables objects
            if var.name == varName: #check by name
                return var # return object
        return None # not found case / error handling

    def _deleteVariable(self , variableObj): # delete variable object
        self.variables.remove(variableObj)
