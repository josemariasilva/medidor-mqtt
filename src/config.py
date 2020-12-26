from PyQt5.QtWidgets import QWidget, QInputDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGroupBox, QSpinBox, QCheckBox, QGridLayout, QLabel, QMessageBox, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt
import paho.mqtt.client as mqtt



class Resources(QWidget):
    
    def __init__(self, parent=None):
        super(Resources, self).__init__(parent)
        self.setFixedSize(250,150)
        self.setWindowTitle("configuração")
        self.bt1 = QPushButton("aplicar")
        self.bt1.clicked.connect(self.send_config)

        self.bt2 = QPushButton("cancelar")
        self.bt2.clicked.connect(self.close_dialog)
        self.temp_ = QLineEdit
        self.temp_.setFixedWidth(60)
        self.check = QCheckBox()
        self.vb = QVBoxLayout()
        self.vb.addWidget(self.config())
        self.setLayout(self.vb)
        self.modal = self
        self.modal.setWindowModality(Qt.ApplicationModal)
    
    def send_config(self):
        config = {"enable":self.check.isChecked(),
                  "time":self.temp_.value(),
                  }
        self.bt1.setEnabled(False)
        print(config)

    def close_dialog(self):
        if not self.bt1.isEnabled():
            self.close()
        
    def config(self):

        gp1 = QGroupBox("configurações")
        hb1 = QHBoxLayout()
        hb2 = QHBoxLayout()
        vb1 = QVBoxLayout()
        hb1.addWidget(self.check)
        hb1.addWidget(QLabel("ganho:"))
        hb1.addWidget(self.temp_)
        hb1.addStretch(1)
        vb1.addLayout(hb1)
        hb2.addWidget(self.bt1)
        hb2.addWidget(self.bt2)
        vb1.addLayout(hb2)    
        gp1.setLayout(vb1)
        return gp1
    
    def start(self):
        self.modal.show()
        self.modal.raise_()

    

