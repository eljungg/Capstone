#for utility functions we might need in more than one place.
from conf import *
def valTypeToString(valType):
    if valType == TYPE_STRING:
        return "String"
    if valType == TYPE_INT:
        return "Int"
    if valType == TYPE_DOUBLE:
        return "Double"
    if valType == TYPE_BOOL:
        return "Boolean"
    if valType == TYPE_CHAR:
        return "Char"
def stringToValType(valStr):
    valStr = valStr.lower()
    if valStr == "string":
        return TYPE_STRING
    if valStr == "int":
        return TYPE_INT
    if valStr == "double":
        return TYPE_DOUBLE
    if valStr == "boolean":
        return TYPE_BOOL
    if valStr == "char":
        return TYPE_CHAR

def determineDataType(val):
        #take any value, return VPL_TYPE
        if __isInt(val) == True:
            valType = TYPE_INT
        elif __isFloat(val) == True:
            valType = TYPE_DOUBLE
        elif __isBool(val) == True:
            valType = TYPE_BOOL
        elif __isChar(val) == True:
            valType = TYPE_CHAR
        else:
            valType = TYPE_STRING
        return valType

def __isInt(val): #helper function for determineType
    try:
        int(val)
        return True
    except ValueError:
        return False
def __isFloat(val):
    try:
        float(val)
        return True
    except ValueError:
        return False
def __isBool(val):
    lcVal = val.lower()
    if lcVal == "false" or lcVal == "true":
        return True
    else:
        return False
def __isChar(val): #Python doesnt do Char, but VIPLE does so we just emulate?
    if len(val) == 1:
        return True
    else:
        return False