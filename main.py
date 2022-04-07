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
        #self.calcular()
        
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
        
        dat = b'#\x00\x00,\x00\x00$\x00\x14,\x00\x00$\x00(,\x00\x00$\x00<,\x00\x01$\x00P,\x00\x01$\x00d,\x00\x01$\x00x,\x00\x02$\x00\x8c,\x00\x02$\x00\xa0,\x00\x02$\x00\xb4,\x00\x03$\x00\xc8,\x00\x03$\x00\xdc,\x00\x03$\x00\xf0,\x00\x04$\x01\x04,\x00\x04$\x01\x18,\x00\x04$\x01,,\x00\x05$\x01@,\x00\x05$\x01T,\x00\x05$\x01h,\x00\x06$\x01|,\x00\x06$\x01\x90,\x00\x06$\x01\xa4,\x00\x07$\x01\xb8,\x00\x07$\x01\xcc,\x00\x07$\x01\xe0,\x00\x08$\x01\xf4,\x00\x07$\x02\x08,\x00\t$\x02\x1c,\x00\x08$\x020,\x00\t$\x02D,\x00\t$\x02X,\x00\t$\x02l,\x00\t$\x02\x80,\x00\n$\x02\x94,\x00\n$\x02\xa8,\x00\n$\x02\xbc,\x00\n$\x02\xd0,\x00\x0b$\x02\xe4,\x00\n$\x02\xf8,\x00\x0b$\x03\x0c,\x00\x0b$\x03 ,\x00\x0c$\x034,\x00\x0c$\x03H,\x00\x0b$\x03\\,\x00\x0c$\x03p,\x00\x0c$\x03\x84,\x00\x0c$\x03\x98,\x00\x0c$\x03\xac,\x00\x0c$\x03\xc0,\x00\x0c$\x03\xd4,\x00\x0c$\x03\xe8,\x00\r$\x03\xfc,\x00\r$\x04\x10,\x00\r$\x04$,\x00\x0e$\x048,\x00\r$\x04L,\x00\r$\x04`,\x00\r$\x04t,\x00\r$\x04\x88,\x00\r$\x04\x9c,\x00\r$\x04\xb0,\x00\r$\x04\xc4,\x00\r$\x04\xd8,\x00\x0e$\x04\xec,\x00\x0e$\x05\x00,\x00\r$\x05\x14,\x00\r$\x05(,\x00\r$\x05<,\x00\x0e$\x05P,\x00\r$\x05d,\x00\r$\x05x,\x00\x0e$\x05\x8c,\x00\r$\x05\xa0,\x00\x0e$\x05\xb4,\x00\r$\x05\xc8,\x00\x0e$\x05\xdc,\x00\r$\x05\xf0,\x00\x0e$\x06\x04,\x00\r$\x06\x18,\x00\x0e$\x06,,\x00\x0e$\x06@,\x00\r$\x06T,\x00\x0e$\x06h,\x00\r$\x06|,\x00\x0e$\x06\x90,\x00\x0e$\x06\xa4,\x00\r$\x06\xb8,\x00\x0e$\x06\xcc,\x00\x0e$\x06\xe0,\x00\x0e$\x06\xf4,\x00\x0e$\x07\x08,\x00\r$\x07\x1c,\x00\x0e$\x070,\x00\x0e$\x07D,\x00\x0e$\x07X,\x00\x0e$\x07l,\x00\x0e$\x07\x80,\x00\r$\x07\x94,\x00\x10$\x07\xa8,\x00\x0e$\x07\xbc,\x00\x0e$\x07\xd0,\x00\x0f$\x07\xe4,\x00\x0e$\x07\xf8,\x00\x0f$\x08\x0c,\x00\x0f$\x08 ,\x00\x0e$\x084,\x00\x0e$\x08H,\x00\x0e$\x08\\,\x00\x0e$\x08p,\x00\x0e$\x08\x84,\x00\r$\x08\x98,\x00\x0e$\x08\xac,\x00\x0e$\x08\xc0,\x00\x0e$\x08\xd4,\x00\x0e$\x08\xe8,\x00\x0e$\x08\xfc,\x00\x0e$\t\x10,\x00\x0e$\t$,\x00\x0e$\t8,\x00\x0e$\tL,\x00\x0e$\t`,\x00\x0e$\tt,\x00\x0e$\t\x88,\x00\x0e$\t\x9c,\x00\x0e$\t\xb0,\x00\x0e$\t\xc4,\x00\x0e$\t\xd8,\x00\x0e$\t\xec,\x00\x0e$\n\x00,\x00\x0e$\n\x14,\x00\x0e$\n(,\x00\r$\n<,\x00\x0e$\nP,\x00\x0e$\nd,\x00\x0e$\nx,\x00\x0e$\n\x8c,\x00\x0e$\n\xa0,\x00\x0e$\n\xb4,\x00\x0e$\n\xc8,\x00\x0e$\n\xdc,\x00\x0e$\n\xf0,\x00\x0e$\x0b\x04,\x00\x0e$\x0b\x18,\x00\x0e$\x0b,,\x00\x0e$\x0b@,\x00\x0e$\x0bT,\x00\x0e$\x0bh,\x00\x0e$\x0b|,\x00\x0e$\x0b\x90,\x00\x0e$\x0b\xa4,\x00\x0e$\x0b\xb8,\x00\x0e$\x0b\xcc,\x00\x0e$\x0b\xe0,\x00\x0e$\x0b\xf4,\x00\x0e$\x0c\x08,\x00\x0e$\x0c\x1c,\x00\x0e$\x0c0,\x00\x0e$\x0cD,\x00\x0e$\x0cX,\x00\x0e$\x0cl,\x00\x0e$\x0c\x80,\x00\x0e$\x0c\x94,\x00\x0e$\x0c\xa8,\x00\x0e$\x0c\xbc,\x00\x0e$\x0c\xd0,\x00\x0e$\x0c\xe4,\x00\x0e$\x0c\xf8,\x00\x0e$\r\x0c,\x00\x0e$\r ,\x00\x0e$\r4,\x00\x0e$\rH,\x00\x0e$\r\\,\x00\x0e$\rp,\x00\x0e$\r\x84,\x00\x0e$\r\x98,\x00\x0e$\r\xac,\x00\r$\r\xc0,\x00\x0f$\r\xd4,\x00\r$\r\xe8,\x00\x0e$\r\xfc,\x00\x0e$\x0e\x10,\x00\x0e$\x0e$,\x00\x0e$\x0e8,\x00\x0e$\x0eL,\x00\x0e$\x0e`,\x00\x0e$\x0et,\x00\x0e$\x0e\x88,\x00\x0e$\x0e\x9c,\x00\x0e$\x0e\xb0,\x00\x0e$\x0e\xc4,\x00\x0e$\x0e\xd8,\x00\x0e$\x0e\xec,\x00\x0e$\x0f\x00,\x00\x0e$\x0f\x14,\x00\x0e$\x0f(,\x00\x0e$\x0f<,\x00\x0e$\x0fP,\x00\x0e$\x0fd,\x00\x0e$\x0fx,\x00\x0e$\x0f\x8c,\x00\x0e$\x0f\xa0,\x00\x0e$\x0f\xb4,\x00\x0e$\x0f\xc8,\x00\x0e$\x0f\xdc,\x00\x0e$\x0f\xf0,\x00\x0e$\x10\x04,\x00\x0e$\x10\x18,\x00\x0e$\x10,,\x00\x0e$\x10@,\x00\x0e$\x10T,\x00\x0e$\x10h,\x00\x0e$\x10|,\x00\x0e$\x10\x90,\x00\x0e$\x10\xa4,\x00\x0e$\x10\xb8,\x00\x0e$\x10\xcc,\x00\x0e$\x10\xe0,\x00\r$\x10\xf4,\x00\x0e$\x11\x08,\x00\x0e$\x11\x1c,\x00\x0f$\x110,\x00\x0e$\x11D,\x00\x0e$\x11X,\x00\x0e$\x11l,\x00\x0e$\x11\x80,\x00\x0e$\x11\x94,\x00\x0e$\x11\xa8,\x00\x0e$\x11\xbc,\x00\x0e$\x11\xd0,\x00\x0e$\x11\xe4,\x00\x0e$\x11\xf8,\x00\x0e$\x12\x0c,\x00\r$\x12 ,\x00\x0e$\x124,\x00\x0e$\x12H,\x00\x0e$\x12\\,\x00\x0e$\x12p,\x00\x0e$\x12\x84,\x00\x0f$\x12\x98,\x00\x0f$\x12\xac,\x00\x0f$\x12\xc0,\x00\x0e$\x12\xd4,\x00\x0e$\x12\xe8,\x00\x0e$\x12\xfc,\x00\x0e$\x13\x10,\x00\x0e$\x13$,\x00\r$\x138,\x00\x0e$\x13L,\x00\x0e$\x13`,\x00\x0e$\x13t,\x00\x0f$\r\n'
        self.decode_data(dat)
        
        # Se conectan los eventos
        self.btnConectar.clicked.connect(self.conectar)
        self.btnMotor.clicked.connect(self.toggle_motor)
        self.btnAdquirir.clicked.connect(self.adquirir)
        self.radioSub.clicked.connect(self.calcularSub)
        self.radioSobre.clicked.connect(self.calcularSobre)
    
    def calcularSobre(self):
        try:
            longitud = len(self.datos_rpm[0])
            val_estables = self.datos_rpm[1][(longitud-int(longitud*0.2)):longitud]
            val_estable = statistics.mean(val_estables)
            print(longitud, statistics.mean(val_estables), statistics.stdev(val_estables))
            alpha = 0.632*val_estable
            t_alpha = 1
            print(alpha)
            diferencias = [[],[]]
            for i in range(longitud):
                dato = self.datos_rpm[1][i]
                t = self.datos_rpm[0][i]
                diff = abs((dato - alpha)/alpha)
                diferencias[0].append(diff)
                diferencias[1].append(t)
            
            val = min(diferencias[0])
            indice = diferencias[0].index(val)
            t_alpha = diferencias[1][indice]
            print(val, t_alpha)
            
                    
            aproximacion = [[],[]]
            k = round(val_estable,4)
            alpha = round(t_alpha,4)
            print(1/alpha)
            for x in range(0, 5000,30):
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
        except(x):
            print(x)
    
    def calcularSub(self):
        try:
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
        except(x):
            print(x)
        
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
                    rpm = ((int.from_bytes(data[1], byteorder="big")/5.0)/0.02)*60.0 ;
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
