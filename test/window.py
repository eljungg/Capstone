import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from nodeeditor.utils import loadStylesheets, dumpException
from nodeeditor.node_editor_window import NodeEditorWindow
from drag_list_box import QDMDragListBox
from sub_window import SubWindow
from vpl_execution import VplExecution

from c_a_window import CustomActivityWindow

import qss.nodeeditor_dark_resources



class MainWindow(NodeEditorWindow):

    def initUI(self):
        self.name_company = 'ASU'
        self.name_product = 'ASU VPL'
        '''
        self.stylesheet_filename = os.path.join(os.path.dirname(__file__), "qss")
        loadStylesheets(
            os.path.join(os.path.dirname(__file__), "nodeeditor-dark.qss"),
            self.stylesheet_filename
        )
        '''

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
        self.createMdiChild()    

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
                        nodeeditor = SubWindow(self)
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
    '''
    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else SubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        #subwnd.setWindowIcon(self.empty_icon)
        # nodeeditor.scene.addItemSelectedListener(self.updateEditMenu)
        # nodeeditor.scene.addItemsDeselectedListener(self.updateEditMenu)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd
    '''

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
        self.windowMenu.addAction(self.actRun)
        self.windowMenu.addAction(self.actShowCAWindow)

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
        self.actRun = QAction('&Run', self, shortcut='Ctrl+R', statusTip="Run the program.", triggered=self.executeProgram)

        self.actShowCAWindow = QAction('&CAWindow', self, statusTip="Show a custom activity window", triggered=self.createCAWindow)

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

        self.addDockWidget(Qt.LeftDockWidgetArea, self.nodesDock)

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
        nodeeditor = child_widget if child_widget is not None else SubWindow(self) 
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        return subwnd

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def executeProgram(self):
        currentScene = self.getCurrentNodeEditorWidget().scene
        execution = VplExecution(currentScene.nodes, currentScene.edges)
        execution.startExecution()
        #execution.setDialogWindow(window)
        #execution.executeProgram()

    def createCAWindow(self, CANode:'CANode'=None, scene:'VplScene'=None):
        subwnd = self.createMdiChild(CustomActivityWindow(self, CANode, scene))
        subwnd.show()
        return subwnd



