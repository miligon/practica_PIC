#!/usr/bin/python3
from gui import *
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QWidget
import matplotlib.pyplot as plt
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import serial
import time

# -----------------------------------------------------
#                 CLASE PARA LA GUI
# -----------------------------------------------------
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    # Cuando se inicializa el Form
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.datos_rpm = [[0,10,20,30,50,70,80],
                     [0,0,0,0,0,0,0]]
        
        # Crea la gráfica y agrega el widget correspondiente
        self.figure, self.axes = plt.subplots()
        self.layout = QtWidgets.QVBoxLayout(self.widget)
        self.grafica = FigureCanvas(self.figure)
        self.layout.addWidget(self.grafica)
        self.axes = plt.scatter(self.datos_rpm[0], self.datos_rpm[1], zorder=500, s=20, color='red')
        self.axes = plt.plot(self.datos_rpm[0], self.datos_rpm[1], 'r', lw=1, color='grey')
        self.axes = plt.xlabel('Tiempo (ms)')
        self.axes = plt.ylabel('RPM')
        #xlim=(xmin, xmax), ylim=(ymin, ymax)
        self.axes = plt.title('Medicion de RPM')
        
        # Se conectan los eventos
        self.btnConectar.clicked.connect(self.conectar)
        self.btnMotor.clicked.connect(self.toggle_motor)
        self.btnAdquirir.clicked.connect(self.adquirir)
    
    def graficar(self):
        #Limpia la figura
        self.figure.clf()
        # Grafica los datos
        self.axes = plt.scatter(self.datos_rpm[0], self.datos_rpm[1], zorder=500, s=20, color='red')
        self.axes = plt.plot(self.datos_rpm[0], self.datos_rpm[1], 'r', lw=1, color='grey')
        self.axes = plt.xlabel('Tiempo (ms)')
        self.axes = plt.ylabel('RPM')
        self.axes = plt.title('Medicion de RPM')
        # Refresca la información del Widget
        self.layout.removeWidget(self.grafica)
        self.grafica = FigureCanvas(self.figure)
        self.layout.addWidget(self.grafica)
    
    def cleanInputBuffer(self):
        # Limpia la información en el buffer de entrada
        self.ser.write("\n".encode("ASCII"))
        self.ser.flush()
        self.ser.reset_input_buffer()
        
    def conectar(self):
        print("conectar")
        puerto = self.txtPuerto.text()
        self.ser = serial.Serial(puerto, 9600, timeout=3, parity=serial.PARITY_NONE, rtscts=0)
        # Limpia la información en el buffer de entrada
        cleanInputBuffer()
        # Pide el estado del motor
        self.ser.write("#3\n".encode("ASCII"))
        estado=self.ser.readline().decode("ASCII")
        if ("ON" in estado):
            self.btnMotor.setText("Motor: ON")
            print("motor on")
        if ("OFF" in estado):
            self.btnMotor.setText("Motor: OFF")
            print("motor off")
        
    def adquirir(self):
        print("adquirir")
        # Limpia la información en el buffer de entrada
        cleanInputBuffer()
        #Envia comando de inicio
        self.ser.write("#1\n".encode("ASCII"))
        self.ser.flush()
        print(self.ser.readline())
        c = "BUSY"
        t = 0
        print("esperando",end='')
        while ("BUSY" in c and t < 20):  # Timeout de 2000ms 
            # Envia comando para preguntar estado
            self.ser.write("#4\n".encode("ASCII"))
            self.ser.flush()
            c = self.ser.readline().decode("ASCII")
            print(".",end='')
            time.sleep(0.5)
            t = t + 1
        
        print("\nmedicion finalizada, pidiendo datos . . .")
        # Envia comando para pedir datos
        self.ser.write("#5\n".encode("ASCII"))
        self.ser.flush()
        c = self.ser.readline()
        print(c)
        # Decodifica y gráfica la informacion
        self.decode_data(c)
        
    def toggle_motor(self):
        self.ser.write("\n".encode("ASCII"))
        self.ser.flush()
        self.ser.reset_input_buffer()
        self.ser.write("#2\n".encode("ASCII"))
        self.ser.flush()
        estado=self.ser.readline().decode("ASCII")
        if ("ON" in estado):
            self.btnMotor.setText("Motor: ON")
            print("motor on")
        if ("OFF" in estado):
            self.btnMotor.setText("Motor: OFF")
            print("motor off")
            
    def decode_data(self, c):
            # 35 -> '#'            10 -> '\n'
        if (c[0] == 35 and c[len(c)-1] == 10): 
            datos = c[1:len(c)-1]
            # Separa los datos usando como referencia el simbolo #
            splited = datos.split(b'$')
            
            self.datos_rpm = [[],[]]
            for pair in splited:
                if (len(pair) == 5):
                    # Separa cada par de datos (tiempo,rpms) usando ',' como referencia
                    data = pair.split(b',')
                    t = int.from_bytes(data[0], byteorder="big")
                    rpm = int.from_bytes(data[1], byteorder="big")
                    self.datos_rpm[0].append(t)
                    self.datos_rpm[1].append(rpm)
            #Imprime la informacion recibida y la gráfica
            print(self.datos_rpm)
            self.graficar()
        else:
            print("data_error")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
