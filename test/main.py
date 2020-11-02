import os
import sys
from PyQt5.QtWidgets import *

sys.path.insert(0, os.path.join( os.path.dirname(__file__), "..", ".." ))


from Capstone.test.window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # print(QStyleFactory.keys())
    app.setStyle('Fusion')

    wnd = MainWindow() #somehow this calls initUI() in the MainWindow class
    print("BEFORE SHOW CALL")
    wnd.show()

    sys.exit(app.exec_())
