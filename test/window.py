from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from nodeeditor.node_editor_window import NodeEditorWindow
from Capstone.test.drag_list_box import QDMDragListBox
from Capstone.test.sub_window import SubWindow
import threading
import pathlib
import os
import json

#threadLock = threading.Lock()
start_threads = []
threads = []
windowContent = []


class MainWindow(NodeEditorWindow):

    def initUI(self):
        self.name_company = 'BlenderFreak'
        self.name_product = 'NodeEditor'

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createNodeDock()

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()




        self.readSettings()

        self.setWindowTitle("VPL")    

    def updateMenus(self):
        pass   

    def about(self):
        QMessageBox.about(self, "About VPL gui attemps",
                "The <b>VPL GUI</b> attempts showcase the attempts on utilizing PyQt5 to develop a VPL.")    

    def createMenus(self):
        super().createMenus()

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

        self.menuBar().addSeparator()

        self.runMenu = self.menuBar().addMenu("&Run")
        self.runMenu.addAction(self.runAct)

    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def onFileOpen(self):
        fnames, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file', self.getFileDialogDirectory(), self.getFileDialogFilter())

        try:
            for fname in fnames:
                if fname:
                    existing = self.findMdiChild(fname)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        # we need to create new subWindow and open the file
                        nodeeditor = SubWindow()
                        if nodeeditor.fileLoad(fname):
                            self.statusBar().showMessage("File %s loaded" % fname, 5000)
                            nodeeditor.setTitle()
                            subwnd = self.createMdiChild(nodeeditor)
                            subwnd.show()
                        else:
                            nodeeditor.close()
        except Exception as e: dumpException(e)

    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None

    def runProgram(self):
        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

        edges = []

        for i, window in enumerate(windows):
            child = window.widget()

            nameOfFile = child.getUserFriendlyFilename()

            pathName = pathlib.Path(__file__).parent.absolute()
            print(pathName)
            fullpath = os.path.join(pathName, nameOfFile)
            print(fullpath)
            
            with open(nameOfFile) as f:
                data = json.load(f)

            for j in data['edges']:
                edges.append(j)
            
            for k in edges:
                for m in data['nodes']:
                    if len(m['outputs']) != 0:
                        if k['start'] == m['outputs'][0]['id']:
                            node1Type = m['op_code']
                            contentToTransfer = m['content']['value']
                    if len(m['inputs']) != 0:
                        if k['end'] == m['inputs'][0]['id']:
                            node2Type = m['op_code']

                edgeThread = nodeThread(node1Type, node2Type, contentToTransfer)
                start_threads.append(edgeThread)

            for n in start_threads:
                n.start()

            for p in start_threads:
                threads.append(p)

            for t in threads:
                t.join()

            if(node2Type == 1):
                pass
            elif(node2Type == 2):
                pass
            elif(node2Type == 3):
                pass
            elif(node2Type == 4):
                pass
            elif(node2Type == 5):
                pass
            elif(node2Type == 6):
                pass
            elif(node2Type == 8):
                print("Opening sub window")
                self.window = printWindow()
                self.window.show()

            print("Showing result of printThread")
            
            start_threads.clear()
            threads.clear()
            windowContent.clear()

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else SubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        #subwnd.setWindowIcon(self.empty_icon)
        # nodeeditor.scene.addItemSelectedListener(self.updateEditMenu)
        # nodeeditor.scene.addItemsDeselectedListener(self.updateEditMenu)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd


    def updateWindowMenu(self):

        self.windowMenu.clear()

        toolbar_nodes = self.windowMenu.addAction("Nodes Toolbar")
        toolbar_nodes.setCheckable(True)
        toolbar_nodes.triggered.connect(self.onWindowNodesToolbar)
        toolbar_nodes.setChecked(self.nodesDock.isVisible())
        self.windowMenu.addSeparator()
        
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeMdiChild())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window) 

    def onFileNew(self):
        subwnd = self.createMdiChild()
        subwnd.show()

    def createActions(self):
        super().createActions()

        self.closeAct = QAction("Cl&ose", self, statusTip="Close the active window", triggered=self.mdiArea.closeActiveSubWindow)
        self.closeAllAct = QAction("Close &All", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        self.tileAct = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.cascadeAct = QAction("&Cascade", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        self.nextAct = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild, statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        self.previousAct = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)
        self.separatorAct = QAction(self)
        self.separatorAct.setSeparator(True)
        self.aboutAct = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)
        self.runAct = QAction("&Run Program", self, statusTip="Run the program", triggered=self.runProgram)


    def onWindowNodesToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()

    def createToolBars(self):
        pass

    def createStatusBar(self):
        self.statusBar().showMessage('Ready')

    def createNodeDock(self):
        self.nodesListWidget = QDMDragListBox()

        self.nodesDock = QDockWidget("Nodes")
        self.nodesDock.setWidget(self.nodesListWidget)
        self.nodesDock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.nodesDock)

    def closeEvent(self, event):

        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def createMdiChild(self, child_widget=None):
        #this command executes on ctrl - n, when you make the actually window for adding nodes.
        nodeeditor = child_widget if child_widget is not None else SubWindow() 
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        return subwnd

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

class nodeThread(threading.Thread):
    def __init__(self, node1, node2, node1Content):
        threading.Thread.__init__(self)
        self.node1 = node1
        self.node2 = node2
        self.node1Content = node1Content

    def run(self):
        #threadLock.acquire()

        if(self.node2 == 1):
            pass
        elif(self.node2 == 2):
            pass
        elif(self.node2 == 3):
            pass
        elif(self.node2 == 4):
            pass
        elif(self.node2 == 5):
            pass
        elif(self.node2 == 6):
            pass
        elif(self.node2 == 8):
            printThread(self.node1Content)

        #threadLock.release()

def printThread(node1Content):
    windowContent.append(node1Content)

class printWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        for i in windowContent:
            self.l = QLabel(i)
            layout.addWidget(self.l)

        b = QPushButton("Stop")
        b.pressed.connect(self.on_click)
        b.pressed.connect(self.close)

        layout.addWidget(b)

        self.setLayout(layout)

    def on_click(self):
        print('PyQt5 button click')

