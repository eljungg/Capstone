from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from nodeeditor.node_editor_window import NodeEditorWindow
from Capstone.test.drag_list_box import QDMDragListBox
from Capstone.test.sub_window import SubWindow

#Luke testing
import inspect


class MainWindow(NodeEditorWindow):

    def initUI(self):
        print("caller name: ", inspect.stack()[1][3])
        print("InitUI is called in MainWindow")
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

    def createMdiChild(self):
        #this command executes on ctrl - n, when you make the actually window for adding nodes.
        print("Called createMdiChild! on ctrl-n")
        nodeeditor = SubWindow() 
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        return subwnd

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None



