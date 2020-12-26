from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog
import pandas as pd
from .widgets import Widget
import numpy as np

class MainWindow(QMainWindow):

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.setMinimumSize(900, 600)
        #self.setFixedSize(1200,800)
        self.setWindowTitle("MEDIDOR TORQUE")
        self.wid = Widget(self)
        self.wid.message.connect(self.refresh_status_bar)
        self.setCentralWidget(self.wid)
        bar = self.menuBar()
        bar.setStyleSheet("color:grey")
        self.setStyleSheet('background-color:grey')
        
    
        
        
        file_menu = bar.addMenu('File')
        
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.plotting_recent_file)
        close_action = QAction('Close', self)
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)
        

    def refresh_status_bar(self, message):
        self.statusBar().showMessage(message)
        self.statusBar().setStyleSheet("color:white")
        
    
    
    def openFileDialog(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileNames(None,"Abrir","","Todos arquivos (*);;CSV arquivos (*.csv)", options=options)
            return fileName
        except:
            pass
    
    #==========NEW=========================
    
    def plotting_recent_file(self):
        try:
            path = self.openFileDialog()
            
            f = pd.read_csv(path[0])
            self.wid.plot_anything(f)
        except:
            pass
        
            

    
    #=======================================
    