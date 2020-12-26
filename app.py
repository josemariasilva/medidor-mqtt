from PyQt5.QtWidgets import QApplication
from src.mainwindow import MainWindow
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
