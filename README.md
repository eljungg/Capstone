# ASU VIPLE

## Project Goal & Directives:
To make a Cross Platform (Works on macOS , windows, and ubuntu linux) Visual Programming Language. Built as a X-platform replacement (or substitute) for ASU VIPLE. An existing .NET Visual programming language. Goal of the language is for educational use. ASU VIPLE is already used for educational purposes in a variety of ways.

## FrameWorks
This Project is built in Python3 using PyQt5 GUI Library. We took an existing open source node editor library for the foundation of our drag and drop GUI.
[PyQt5](https://pypi.org/project/PyQt5/)
[nodeeditor library](https://pypi.org/project/nodeeditor/) 
For a close look into the nodeeditor library, check the [GitLab repository]([nodeeditor library](https://pypi.org/project/nodeeditor/).

## Project Big Picture
User selects from a variety of nodes, dragging them from the left menu bar, onto the graph.
Each node represents a basic functionality, such as storing data, summing data, or printing data.
Nodes are connected in sequential order by clicking on their input/output points and dragging to the following node
You can have as many threads/groups of nodes as you like, but execution goes from left to right inside a chain of nodes.
At run time, one thread spins up for each chain, and executes the function of each node, passing resultant data to its descendants.

## GUI Overview
The application’s main window is a QMdiArea which acts as a sort of container for the other sections of the application. The sub-window is the actual graph where the user can place nodes on; the canvas if you will. The application opens with one sub-window by default, but the user can add more/less as they wish. The drag list box is a draggable list of all of the available nodes. The user can place this box on the top, bottom, left, or right of the main window as they wish. To add nodes to the sub-window, the user simply needs to drag their node of choice onto the sub-window. To make a connection between nodes, click and drag from the sockets present on the nodes.

## Nodes (Big picture)
A node is an activity block that can be connected to other nodes in order to execute specific functions created by the user. There are many types of nodes to represent the various abilities that a programming language contains.

To add a new type of node to the program perform the following:
- Add a new opcode to the conf.py file in the following format: 
```python
OP_CODE_\*NODE NAME\* = \*UNUSED NUMBER\*
```
- Add a new line to the addItems function in the drag_list_box.py file in the following format:
```python
self.addItem(‘\*Node Name\*’, None, OP_CODE_\*NODE NAME\*)
```
- Create a new node file inside the nodes folder and make it look similar to how all the other node files look (with a Node class and a NodeContent class named as \*NodeName\*Node and \*NodeName\*NodeContent)
- Add the following lines of code to if statement in the setNodeType function in the sub_window.py file:
```python
elif(op_code == OP_CODE_\*NODE NAME\*):
	print(“\*Node Name\* node added”)
	Node = \*NodeName\*Node(self.scene)
	Node.title = “\*Node Name\*”
```
if the node requires the use of variables in a text box, include the following line in the elif statement:
```python
	node.setVariableData(self.variables)
	node.content.redrawComboBox()
```

##Sockets
A socket can be an input or an output socket. An output socket can be either a service socket (pie slice-shaped socket) or an event socket (circular-shaped socket). In the init function of each node class, the number of input and output sockets is assigned by the number of elements in a corresponding list. If the element is a ‘0’ or ‘1’, the socket is a service socket. If the element is a ‘2’, the socket is an event socket.

## Execution Engine
Vpl_execution.py contains the logic that connects the nodes. The execution object is created by passing it the list of nodes and edges in the graph. This will set up the list of starting nodes, the nodes that do not have input from any other node. Actual execution is started by calling the startExecution() function. 
The general execution loop is as follows. A node’s doEval function is executed with parentData as input. The resulting output of doEval is stored into parentData. Next, the children nodes are found and placed into a list. The child in the list continues the thread, new threads are spawned for the other children. If the node has no children, the thread dies ending execution. 
Many nodes will require special handling which can be added to the threadExecute function.

## Conf File
The conf.py file contains the values associated with specific variable names so that it is simpler to assign specific functionality to nodes and variable types. When a new type of node is added to the program, a new opcode with a unique value needs to be added to this file.

## Data model
There is a folder called model/ which holds several classes which are used for data management.
Due to the nature of the program, most data is created dynamically at run-time, as nodes are executed.
Each node is assigned an instance of NodeData(). This class has fields for nodeType, Value, ValueType, and messages.
This is done to ensure that every node has a predictable format for accessing pertinent members.
 Although each node is a combination of unique classes, they have a common data structure using this NodeData object.
A similar pattern is given for Variables, and DataConnections.
You can extend this data structure, and then ALL nodes will contain the new members.

## Individual Nodes
### Variable node
The variable node takes input from any node that gives output, and stores the value into the selected variable.

The node has a popup QDialog which allows for dynamic creation/editing of variables. There is one “master” list of variables which is shared between all the nodes in a graph.

Variables use the model/variables.py vile for a dataStructure. Each variable has self.name, self.val, and self.valType. valType should be set by the TYPES found in the conf.py file. Not as native python types. This is because we are following VIPLE implementation which uses more C style types.

### Calculate node
The calculate node has a drop down menu which contains boolean values, any variables created in the program, and a "value" variable, which takes the immediate value of whatever is connected to the input of the calculate node (e.g. Data node with the value of 100 can be represented in the calculate node with "value") If the previous node is a join node, there will be temporary variables available in the calculate node as well, based off of join's dictionary output. The node performs calculations by taking whatever the user input is and performing Python eval() function on it. The result of this eval() is passed along to the node's output, along with the value type of the result

### Data
Data node is the basis for a program. Takes input from a user and determines the type dynamically

At runtime this node passes its value and type to any child nodes.

### Merge node
The functionality of Merge node is to connect and pass the incoming nodes’ data directly to the next node. It can take multiple input nodes. The doEval function of this node class is to return the “data'' object of the parent nodes.

### If
If node works the same as the code implementation of an If statement. When a node is connected to the input socket of an If node, the data from that node can be used for writing statements if the word “value” is used in an If node textbox. Variables can also be used in the text boxes by typing out “state.\*variable_name\*”.

By clicking the “+” or “-” buttons on the node, new textboxes can be created or removed. Extra textboxes are connected to a corresponding socket and represent additional “else if” statements.

There are currently three known bugs or issues associated with the If node. 
1. When loading a saved graph that contains an If node, the “+” and “-” buttons are not registered properly and do not create or remove additional textboxes. The functions used to do these actions are written in the IfNode class rather than the IfNodeContent class so that height can be adjusted based on the number of output sockets. Specifically, when a saved graph is loaded, the deserialize function is called from the IfNodeContent class (like all content classes) and creates the node based on the data that is in the JSON file. Since both the serialize and deserialize functions have to be in the content class, there are some issues with passing data between the node class and the content class. Some rearranging might be able to fix it but requires further testing.
2. Unlike VIPLE, the return value of the node is not the input value. It is the index of the correct socket to read from. This presents problems when certain nodes that utilize the input socket for data transfer, such as Variable or Print Line, are connected directly to the If node output socket.
3. There are problems with the text change adjusting the size of the textbox and node. THe problem differs from how other nodes have handled it due to the possibility of multiple textboxes being part of the node. The function to adjust the size has been commented out until further fixes are applied.

### Switch
Switch node works much the same way as If node but must take an input to be compared with the values that are written in the textboxes. Other than this, Switch node has the same functionality and bugs as If node.

### Join node
The join node contains multiple inputs with a text field for each input. During execution, the join node will stop all threads that enter it until a thread has entered each of its inputs once. When each input has received data from a thread, the join node will bundle the inputs into a dictionary object, with the contents of the text fields as keys and populated with data from the inputs.
If an input receives data from multiple threads it will store the data into a queue. When all inputs have received something, data is popped from all the input’s queues.

### Print Line node
The Print Line node will display inputs on a window that displays upon execution start. Non-string inputs will be cast as strings and printed on a new line.

### Simple Dialog node
Simple dialog prints user messages to screen in a separate dialog window
WARNING: This node is BROKEN on macOS. Crashes whole application.
Problem with spawning GUI object from doEval() function called in execution threads.
Needs to be reworked.

### Terminal Print node
Terminal Print is a debugging node that prints a line to the terminal. Currently disabled in the drag list box.

### While node
While node is able to loop through a sequence of nodes multiple times until the condition that is in the textbox is “false”. The end of the loop is where an End While node is placed.

In its current implementation, when a While node is read by the execution engine, it is appended to a local list of While nodes called whileNodes. If the condition in the textbox is “true”, it will continue with the nodes that are connected to the While node’s output socket. When an End While node is reached, it will jump back to the last While node in the list. If the condition in the textbox of the While node is “false”, it will look for the next End While node without executing any other nodes between the While node and the End While node. Once it reaches the End While node, the End While node will execute and continue with any nodes that are connected to its output socket.

Unlike VIPLE, the return value of the node is not the input value. It is the condition evaluated to a boolean value. This presents problems when certain nodes that utilize the input socket for data transfer, such as Variable or Print Line, are connected directly to the While node output socket.

### End While node
End While will jump back to the last used While node or will continue to the next node if the While node contains a “false” condition.

End While node relies on the use of While node. Without it, End While does nothing. See While node for more details on how End While works.

### Break node
Break node will end the last loop that was executed and continue executing nodes that are connected to the next End While node’s output socket. A Break node must have an End While in the sequence of nodes connected to the Break node’s output socket.

Currently, Break node does not function properly. It does not break the last loop that was executed. Further development is needed.

### Comment node
This node will provide a text box with a scroll bar for the user to write down some comments about the VPL diagram.

### Timer
Timer node will accept a Data node as the input and will suspend the thread engine for the next node according to the integer received. Notice that the actual pause time is (Input_Integer / 1000) second.

### Text-To-Speech node
The text-to-speech library that this application utilizes is [pyttsx3](https://pypi.org/project/pyttsx3/). The node expects some input to be able to speak. The "speak" logic is located in vpl_execution.py file, and the node just passes along its input through its output.  

### RESTful Service node
Takes the URL of a RESTful web service and returns the result. 
Input to the node are passed into URL as parameters using the DataConnections class and the DataConnectionsMenu.
These DataConnections classes are not unique to restful services, and can be implemented in other places as done in VIPLE.


### Code Activity (Python) node
Code Activity node allows users to edit their own python command in the textbox by clicking the “Edit Code” button. It also requires the user to select a code name for the Activity node from the Combo Box. Notice that inside the actual edit area, the input data outside the Activity Node is stored inside variable 'InputValue' and the generated output is stored in variable “OutputValue”, which is set to be 1 as default. Remember the code activity node at this time only takes one node for input data. Remember to import the required library when editing your python scripts.

### Key Press node
Key Press nodes provide a combo box to choose the target key element, which as pressed, will spawn the thread for all connected children nodes. Each time the target key is pressed, the node will only spawn thread for once, meaning that holding the key won’t keep generating new thread and will instead prevent new thread from being started. The terminal will record every key that is being held. You can have at most two target keys in one KeyPress node by clicking on the add button. To reduce the number of target keys, just press the minus button. Importantly, the Key Press node responds to the event by initiating a Key Listener as the project starts, and it  has to be the starting node of the whole VPL diagram.

### Key Release node
Key Release node has no input, its functionality is to start a thread for its children nodes when any keyboard key is released. It detect the keyboard event by starting a Key Listener. It has to be the starting node of the whole VPL diagram like key press node. Noticed that when running the project using hot key (Ctrl + R), the project will first pause for around 1 second and then start the key listener of the Key Release node.

### Custom Activity node
The custom activity node acts as a function. A drop down menu will display the list of custom activities defined. The ‘more’ button allows the user to name new custom activities. The ‘edit’ button opens a window that the user can drop nodes into. 
Execution in the custom activity will start with the interior input node and continue with its children. If the chain of nodes connects to the interior output execution will continue along the exterior output of the custom activity node.

Currently the custom activity node needs to be rebuilt.

## Package Requirements
The packages that are currently implemented into the VPL that require additional installation are as follows:
- PyQt5
- nodeeditor
- requests
- keyboard
- pyttsx3
- pynput

To install all packages, run the following command in the project terminal:
```bash
pip install -r requirements.txt
```

## Executable creation
The creation of executables was accomplished through [pyinstaller](https://www.pyinstaller.org/). For creating the application in the Linux environment, the following command was used
```bash
pyinstaller main.py --name CapstoneVPL --onefile --hidden-import=pynput.keyboard._xorg --hidden-import=pynput.mouse._xorg --windowed 
```
pynput had some dependency issues with Linux's X server, so we had to manually import the mouse and keyboard. This creates an executable that can be run by double clicking. Further customization can be done with, for example, an icon.
In order to build the executable on Linux, some reordering of the file hierarchy is necessary. 

The general structure for the project looks like

```
Capstone/
└── test/
    ├── model/
    │   └── model files.py    (multiple)
    │
    ├── nodes/
    │   └── all node files.py (multiple)
    │
    └── main program files.py (multiple)
 
```
The reasoning behind this hierarchy was to try and organize our program into a MVC style format, but for some reason, the packaging utility the team used, PyInstaller, can't follow through different branches, so the project was restructured to follow the following format
```
Capstone/
└── test/
    │    
    ├── nodes/
    │   └── all node files.py (multiple)
    │
    ├── model files.py    (multiple)
    │
    │
    └── main program files.py (multiple)
```
There is an unidentified bug where the original file hierarchy can't be parsed by PyInstaller, but the issue is resolved if the hierarchy is restructured into the bottom example.

For creating the application in the Windows environment, get to the test directory and use “pyinstaller main.py --name CapstoneVPL --onefile --windowed, notice that the file hierarchy is the same as for Linux executable:




Capstone/
└── test/
    │    
    ├── nodes/
    │   └── all node files.py (multiple)
    │
    ├── model files.py    (multiple)
    │
    │
    └── main program files.py (multiple)


The file in the model folder in the general project must be pulled out and placed inside the test folder. Use --hidden-import=pynput.keyboard._xorg --hidden-import=pynput.mouse._xorg in the script like how we did in Linux in case your python can not import the pynput library by itself on Windows.


