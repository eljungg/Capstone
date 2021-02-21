
# note -- Should this be in the model???? -luke

LISTBOX_MIMETYPE = "application/x-item"
### Side menu options for node types ###
OP_CODE_INPUT = 1
OP_CODE_OUTPUT = 2
OP_CODE_ADD = 3
OP_CODE_SUB = 4
OP_CODE_MUL = 5
OP_CODE_DIV = 6
OP_CODE_VARIABLE = 7
OP_CODE_CALCULATE = 8
OP_CODE_DATA = 9
OP_CODE_MERGE = 10
OP_CODE_IF = 11
OP_CODE_JOIN = 12
OP_CODE_SWITCH = 13
OP_CODE_COMMENT = 14

OP_CODE_TERMINAL_PRINT = 49
OP_CODE_PRINT_LINE = 50
OP_CODE_SIMPLE_DIALOG = 51

###In Node Operations###
OPERATION_IF = 0
OPERATION_ELSE = 1
OPERATION_ADD = 2
OPERATION_SUB = 3
OPERATION_MULT = 4
OPERATION_DIV = 5
OPERATION_OR = 6
OPERATION_AND = 7

###Type Flags###
TYPE_STRING = 0
TYPE_INT = 1
TYPE_DOUBLE = 2
TYPE_BOOL = 3
TYPE_CHAR = 4

#Need to add all the nodes we use into this list
#NODETYPES = {OP_CODE_VARIABLE, OP_CODE_CALCULATE, OP_CODE_DATA, OP_CODE_MERGE, 
#OP_CODE_IF, OP_CODE_JOIN}
