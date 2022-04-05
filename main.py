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
import math
import statistics
import img

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
        self.calcular()
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
        self.radioSub.clicked.connect(self.calcularSub)
        self.radioSobre.clicked.connect(self.calcularSobre)
    
    def calcularSobre(self):
        longitud = len(self.datos_rpm[0])
        val_estables = self.datos_rpm[1][(longitud-int(longitud*0.2)):longitud]
        val_estable = statistics.mean(val_estables)
        print(longitud, statistics.mean(val_estables), statistics.stdev(val_estables))
        alpha = 0.632*val_estable
        t_alpha = 1
        print(alpha)
        for i in range(longitud):
            dato = self.datos_rpm[1][i]
            diferencia = (dato - alpha)/alpha
            if (abs(diferencia) < 0.01):
                print(i, dato)
                t_alpha = i
                
        aproximacion = [[],[]]
        k = round(val_estable,4)
        alpha = round(t_alpha,4)
        print(1/alpha)
        for x in range(0, 1000,10):
            x = x
            aproximacion[0].append(x)
            aproximacion[1].append(k*(1-math.exp(-1*(x/alpha))))
        
        self.graficar()
        self.axes = plt.scatter(aproximacion[0], aproximacion[1], zorder=500, s=20, color='blue')
        self.axes = plt.plot(aproximacion[0], aproximacion[1], 'r', lw=1, color='lightgray')
        # Refresca la información del Widget
        self.layout.removeWidget(self.grafica)
        self.grafica = FigureCanvas(self.figure)
        self.layout.addWidget(self.grafica)
        self.frame.setStyleSheet("image: url(:/img/s1.PNG);")
        self.txtAlpha.setText(str(alpha))
        self.txtK.setText(str(k))
        self.txtWn.setText("")
        self.txtZ.setText("")
             
        
    
    def calcularSub(self):
        longitud = len(self.datos_rpm[0])
        val_estables = self.datos_rpm[1][(longitud-int(longitud*0.2)):longitud]
        val_estable = statistics.mean(val_estables)
        print(longitud, statistics.mean(val_estables), statistics.stdev(val_estables))
        Mp = max(self.datos_rpm[1])
        t_Mp = self.datos_rpm[1].index(Mp)
        print(t_Mp, Mp)
        z = (-1*math.log(Mp/100))/math.sqrt((math.pi*math.pi)+(math.pow(math.log(Mp/100),2)))
        print(z)
        z = round(z,4)
        wn = round(math.pi/(t_Mp*math.sqrt(1-(z*z))),4)
        aproximacion = [[],[]]
        k = round(val_estable,4)
        
        for x in range(0, 1000,5):
            x = x
            aproximacion[0].append(x)
            # Grafica a partir de los valores calculados
            aproximacion[1].append(k*(1-(((math.exp(-1*z*wn*x))/(math.sqrt(1-(z*z))))*math.sin((wn*x)+(math.pi/2)))))
        
        self.graficar()
        self.axes = plt.scatter(aproximacion[0], aproximacion[1], zorder=500, s=20, color='blue')
        self.axes = plt.plot(aproximacion[0], aproximacion[1], 'r', lw=1, color='lightgray')
        # Refresca la información del Widget
        self.layout.removeWidget(self.grafica)
        self.grafica = FigureCanvas(self.figure)
        self.layout.addWidget(self.grafica)
        self.frame.setStyleSheet("image: url(:/img/s2.PNG);")
        self.txtAlpha.setText("")
        self.txtK.setText(str(k))
        self.txtWn.setText(str(wn))
        self.txtZ.setText(str(z))       
        
        
    # Calcula una grafica de prueba 
    def calcular(self):
        self.datos_rpm = [[],[]]
        wn=0.045 #0.0003    #0.0045
        z=0.5   #0.00008
        k = 5
        
        alpha = 30
        for x in range(0, 1000,10):
            x= x
            self.datos_rpm[0].append(x)
            #sobre amortiguado
            self.datos_rpm[1].append(int((k*(1-math.exp(-1*(x/alpha))))*1000) )
            # Sub amortiguado
            #self.datos_rpm[1].append(k*(1-(((math.exp(-1*z*wn*x))/(math.sqrt(1-(z*z))))*math.sin((wn*x)+(math.pi/2))))) 
        print(self.datos_rpm[1])
            
    # Grafica los datos contenidos en datos_rpm
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
    
    #Limpia el buffer de entrada
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
        self.cleanInputBuffer()
        # Pide el e9stado del motor
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
        self.cleanInputBuffer()
        #Envia comando de inicio
        # self.ser.write("#1\n".encode("ASCII"))
        # self.ser.flush()
        # print(self.ser.readline())
        # c = "BUSY"
        # t = 0
        # print("esperando",end='')
        # while ("BUSY" in c and t < 20):  # Timeout de 2000ms 
        #     # Envia comando para preguntar estado
        #     self.ser.write("#4\n".encode("ASCII"))
        #     self.ser.flush()
        #     c = self.ser.readline().decode("ASCII")
        #     print(".",end='')
        #     time.sleep(0.5)
        #     t = t + 1
        
        # print("\nmedicion finalizada, pidiendo datos . . .")
        # Envia comando para pedir datos
        self.ser.write("#5\n".encode("ASCII"))
        self.ser.flush()
        c = self.ser.read_until(expected='\r\n')
        print(c)
        # Decodifica y gráfica la informacion
        self.decode_data(c)
        
    def toggle_motor(self):
        self.cleanInputBuffer()
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
