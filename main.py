import sys
from PyQt5.QtWidgets import *

from vpl_window import VPLWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyle('Fusion')

    wnd = VPLWindow()
    wnd.show()
    
    sys.exit(app.exec_())
