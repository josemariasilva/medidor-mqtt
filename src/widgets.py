from PyQt5.QtWidgets import (QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout, 
                            QPushButton, QWidget, QGroupBox, QMessageBox, 
                            QFileDialog, QCheckBox, QSpinBox, QLabel, QLineEdit)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from .plot import Plotting
import paho.mqtt.client as mqtt
from .client_receiver import Receive_from_ad
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import math
from .config import Resources
from scipy import signal
import csv


class Widget(QWidget):

    message = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.backup = None
        self.mark = True
        self.setStyleSheet('background-color:grey')
        #self.ad = Receive_from_ad('mqtt.eclipse.org', 1883, 'request')
        self.channel_1 = Plotting()
        self.channel_2 = Plotting()
 
        self.ganho = 1
        self.ajuste_zero = 0
        self.apply1 = QPushButton("aplicar")
        self.apply1.clicked.connect(self.update_gain)
        self.apply1.setStyleSheet("""background-color:#73706f;
                                        width:50px;
                                        color:white;
                                        border-radius:5px;""")
        self.apply2 = QPushButton("aplicar")
        self.apply2.clicked.connect(self.update_zero)
        self.apply2.setStyleSheet("""background-color:#73706f;
                                        width:50px;
                                        color:white;
                                        border-radius:5px;""")

        self.gain = QLineEdit()
        self.gain.setText("1")
        self.gain.setValidator(QDoubleValidator(1.0000,9999999999.0000,4))
        self.gain.setStyleSheet("""background-color:white;
                                   border-radius:2px;
                                   width:25px;""")
        self.const = QLineEdit()
        self.const.setText("0")
        self.const.setValidator(QDoubleValidator(-999999999.0000,999999999.0000,4))
        self.const.setStyleSheet("""background-color:white;
                                    border-radius:2px;
                                    width:25px;""")


        self.test = QPushButton("ajustes")
        self.test.setStyleSheet("color:white;")
        self.test.clicked.connect(self.newDialog)
        
        self.iniciar = QPushButton("Iniciar")
        self.iniciar.clicked.connect(self.button_play)
        self.iniciar.setStyleSheet("""background-color:#73706f;
                                        height:25px;
                                        color:white;
                                        border-radius:2px;""")

        self.finalizar = QPushButton("Finalizar")
        self.finalizar.clicked.connect(self.button_stop)
        self.finalizar.setStyleSheet("""background-color:#73706f;
                                        height:25px;
                                        color: white;
                                        border-radius:2px;""")

        self.salvar = QPushButton("Salvar")
        self.salvar.clicked.connect(self.button_save)
        self.salvar.setStyleSheet("""background-color:#73706f;
                                        height:25px;
                                        color:white;
                                        border-radius:2px;""")

        self.refresh = QPushButton("Limpar")
        self.refresh.clicked.connect(self.button_refresh_plot)
        self.refresh.setStyleSheet("""background-color:#21201f;
                                        height:50px;
                                        color:white;
                                        border-radius:5px;""")

        self.nav_channel_1 = NavigationToolbar(
            self.channel_1, self.channel_1, coordinates=False)
        self.nav_channel_1.setFixedHeight(25)
        
        self.nav_channel_1.setStyleSheet('background-color: 0;')

        #self.nav_channel_2 = NavigationToolbar(self.channel_2, self.channel_2, coordinates=False)
        # self.nav_channel_2.setFixedHeight(25)
        #self.nav_channel_2.setStyleSheet('background-color: 0;')

        self.vertical_plot = QVBoxLayout()
        self.vertical_button = QVBoxLayout()
        self.horizontal_box = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.vertical_plot.addWidget(self.channel_one())

        self.hbox2.addWidget(self.iniciar)
        self.hbox2.addWidget(self.finalizar)
        self.hbox2.addWidget(self.salvar)
        ##self.hbox2.addWidget(self.test)
        
        self.vertical_plot.addLayout(self.hbox2)
      
        self.horizontal_box.addLayout(self.vertical_plot)

        self.setLayout(self.horizontal_box)
        #self.ad.start()
        #self.ad.data_signal.connect(self.plot_anything)
        self.data = None

    def newDialog(self):
        #4th buttom with configurations
        self.resour = Resources()
        self.resour.start()

    def update_gain(self):
        
        self.ganho = float(self.gain.text())
        if self.ganho in [None, 0]:
            self.ganho=1


    
    def update_zero(self):
        
        self.ajuste_zero = float(self.const.text())
        if self.ajuste_zero is None:
            self.ajuste_zero = 0
        
        
        

    def saveFileDialog(self, o='salvar'):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            None, o, "", "Todos arquivos (*);;CSV arquivos (*.csv)", options=options)
        return fileName

    def channel_one(self):
        gp1 = QGroupBox()
        #gp1.setFixedSize(900,550)
        lb1 = QLabel("ganho")
        lb1.setStyleSheet("color:white;")

        
        lb2 = QLabel("ajuste zero")

        lb2.setStyleSheet("color:white;")
        gp1.setStyleSheet('border:0;')

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(self.channel_1)
        hbox.addWidget(self.nav_channel_1)
        hbox.addStretch()
        hbox.addWidget(lb1)
        hbox.addWidget(self.gain)
        hbox.addWidget(self.apply1)
        hbox.addStretch()
        hbox.addWidget(lb2)
        hbox.addWidget(self.const)
        hbox.addWidget(self.apply2)
        hbox.addStretch()
        vbox.addLayout(hbox)
        gp1.setLayout(vbox)
        return gp1


    def buttons(self):
        gp1 = QGroupBox()
        #gp1.setFixedSize(550, 150)
        gp1.setStyleSheet('border:0;')
        vbox = QVBoxLayout()
        vbox.addWidget(self.iniciar)
        vbox.addWidget(self.finalizar)
        vbox.addWidget(self.salvar)
        vbox.addWidget(self.refresh)
        gp1.setLayout(vbox)
        return gp1

    def button_play(self):
        self.gain.setText("1")
        self.const.setText("0")
        self.button_refresh_plot()
        self.channel_1.refresh()
        if self.mark:
            self.mark = False
            try:
                mqttc = mqtt.Client('999')
                mqttc.connect('mqtt.eclipse.org', 1883)
                mqttc.publish('ad', 'on')
                self.message.emit('Leitura iniciada.')
            except:
                QMessageBox.warning(
                    self, "Error", "Sem conexão com o servidor!")
                self.message.emit('Offline')
        

    def button_stop(self):
        if not(self.mark):
            self.mark=True
            try:
                mqttc = mqtt.Client('999')
                mqttc.connect('mqtt.eclipse.org', 1883)
                mqttc.publish('ad', 'off')
                self.message.emit('Leitura finalizada.')
                
            except:
                self.message.emit('Offline')
        

    def button_save(self):
    
        try:
            file_ = self.saveFileDialog()
            
            with open(file_, "w") as outfile:
                writer = csv.writer(outfile)
                writer.writerow(self.data.keys())
                writer.writerows(zip(*self.data.values()))


        except:
            QMessageBox.warning(self, "Error", "Falha ao salvar o arquivo.")


    def button_refresh_plot(self):
        
        self.channel_1.refresh()
        self.channel_1.plot([0], [0])
    
    # ================NEW=============
    
    def plot_anything(self, data, path=None):
        
        self.channel_1.refresh()
            
        try:
            y1 = data['data']
            x1 = data['time'][:len(y1)]

        except:
            QMessageBox.warning(
                    self, "Error", "Arquivo nao possui colunas 'data' e 'time'")
        else:
            b,a = signal.butter(2,0.00200,output='ba',btype='low')
            filtro = (signal.filtfilt(b,a,y1,axis=0)-self.ajuste_zero)*self.ganho

            self.data = {
                    "data":list(filtro),
                    "time":list(x1)
            }
            if self.backup is None:
                self.backup = self.data
            self.ganho= 1
            self.ajuste_zero=0
            self.gain.setText("1")
            self.const.setText("0")
            self.channel_1.plot(x1, filtro)
            self.message.emit('Pronto!.')
        
    
    # =====================================
    