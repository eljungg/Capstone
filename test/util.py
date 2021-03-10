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
