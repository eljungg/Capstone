import os
import sys
from PyQt5.QtWidgets import *

sys.path.insert(0, os.path.join( os.path.dirname(__file__), "..", ".." ))


from window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # print(QStyleFactory.keys())
    app.setStyle('Fusion')

    wnd = MainWindow() #somehow this calls initUI() in the MainWindow class
    wnd.show()

    sys.exit(app.exec_())
 