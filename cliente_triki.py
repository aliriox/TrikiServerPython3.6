"""
                /////////////////////////////////////////
                /                                       /
                /   PYTHON VERSION 3.6.4                /
                /   MYSQLCONNECTOR VERSION 8.0.15       /
                /   AUTHOR: ALIRIOX                     /
                /   SERVIDOR VERSION: MARIADB 10.1.36   /
                /   TKINTER VERSION 8.6.6               /
                /                                       /
                /////////////////////////////////////////
"""
import socket
import threading
from tkinter import *
import time

contin = True
suTurno = False
s = socket.socket()
Recambio = [0,0]

def mouseClick(event):

    global suTurno
    mensaje = "0"
    Recambio[0] = 0
    Recambio[1] = 0    
    if suTurno:
        if event.x > 32 and event.x < 115 and event.y < 88 and event.y > 10:
            #fondo1.place(x=42,y=15)
            mensaje = "1"
            Recambio[0] = 42
            Recambio[1] = 15
        elif event.x > 130 and event.x < 205 and event.y < 88 and event.y > 10:
            #fondo1.place(x=132.5,y=15)
            mensaje = "2"
            Recambio[0] = 132.5
            Recambio[1] = 15
        elif event.x > 220 and event.x < 295 and event.y < 88 and event.y > 10:
            #fondo1.place(x=223,y=15)
            mensaje = "3"
            Recambio[0] = 223
            Recambio[1] = 15
        elif event.x > 32 and event.x < 115 and event.y < 175 and event.y > 105:
            #fondo1.place(x=42,y=107)
            mensaje = "4"
            Recambio[0] = 42
            Recambio[1] = 107
        elif event.x > 130 and event.x < 205 and event.y < 175 and event.y > 105:
            #fondo1.place(x=132.5,y=107)
            mensaje = "5"
            Recambio[0] = 132.5
            Recambio[1] = 107
        elif event.x > 220 and event.x < 295 and event.y < 175 and event.y > 105:
            #fondo1.place(x=223,y=107)
            mensaje = "6"
            Recambio[0] = 223
            Recambio[1] = 107
        elif event.x > 32 and event.x < 115 and event.y < 267 and event.y > 195:
            #fondo1.place(x=42,y=198)
            mensaje = "7"
            Recambio[0] = 42
            Recambio[1] = 198
        elif event.x > 130 and event.x < 205 and event.y < 267 and event.y > 195:
            #fondo1.place(x=132.5,y=198)
            mensaje = "8"
            Recambio[0] = 132.5
            Recambio[1] = 198
        elif event.x > 220 and event.x < 295 and event.y < 267 and event.y > 195:
            #fondo1.place(x=223,y=198)
            mensaje = "9"
            Recambio[0] = 223
            Recambio[1] = 198

        if mensaje != "0":

            print("enviando posicion")
            mensaje = mensaje.encode()
            s.send(mensaje)
            suTurno = False

        else:
            pass
    else:
        print("espere su turno")


def recv_mensaje(msm):
    boolmsm = False
    x = 0
    y = 0
    if msm == "1":
        x = 42
        y = 15
        boolmsm = True
    elif msm == "2":
        x = 132.5
        y = 15
        boolmsm = True
    elif msm == "3":
        x = 223
        y = 15
        boolmsm = True
    elif msm == "4":
        x = 42
        y = 107
        boolmsm = True
    elif msm == "5":
        x = 132.5
        y = 107
        boolmsm = True
    elif msm == "6":
        x = 223
        y = 107
        boolmsm = True
    elif msm == "7":
        x = 42
        y = 198
        boolmsm = True
    elif msm == "8":
        x = 132.5
        y = 198
        boolmsm = True
    elif msm == "9":
        x = 223
        y = 198
        boolmsm = True
    else:
        pass
    return boolmsm, x, y
'''
class GUI(threading.Thread):
    def __init__(self):
        super(GUI, self).__init__()
        self.ventana = Tk()
        self.ventana.title("Bienvenido a alirioxTriki!!")
        self.ventana.geometry("354x281")

    def run(self):
        self.ventana.mainloop()

class MyThread(threading.Thread):
    def __init__(self, socket, num):
        super(MyThread, self).__init__()
        self.sc = socket
        self.sc.settimeout(1) 
        self.num = num

    def escuchar(self):
        global contin
        while contin:
            try:
                mensaje = self.sc.recv(1024)
                mensaje = mensaje.decode()
                print ("< "+mensaje)
                if mensaje == "servidor no disponible":
                    print("presione enter para terminar.....")
                    contin = False
                elif mensaje == "fin":
                    print("*******fin de la partida********")
                    print("presione enter para terminar.....")
                    contin = False
            except socket.timeout:
                pass

    def escribir(self):
        global contin
        while contin:
            mensaje = input()
            mensaje = mensaje.encode()
            self.sc.send(mensaje)
            if mensaje.decode() == "exit":
                contin = False      

    def run(self):
        
        if self.num == 1:
            self.escuchar()
        elif self.num == 2:
            self.escribir()
'''

if __name__ == '__main__':

    hilos = []
    #cambio = True
    s.settimeout(1)
    s.connect(("localhost", 9999))
    print ("estas conctado al servidor")

    ventana = Tk()
    ventana.title("Bienvenido a alirioxTriki!!")
    ventana.geometry("337x300")
    imagen_fondo = PhotoImage(file = "imagen/loadtriki.gif")
    imagen_o = PhotoImage(file = "imagen/O.gif")
    imagen_x = PhotoImage(file = "imagen/x.gif")
    imagen_J1 = None
    imagen_J2 = None
    imagen_R = PhotoImage(file = "imagen/turnoR.gif")
    imagen_V = PhotoImage(file = "imagen/turnoV.gif")
    fondo = Label(ventana, image = imagen_fondo).place(x=0,y=0)
    ventana.bind("<Button>", mouseClick)
    
    while contin:
        try:
            ventana.update()
            #cambio = False
        except TclError:
            print("--saliendo--")
            break

        try:
            mensaje = s.recv(1024)
            mensaje = mensaje.decode()
            print ("< "+mensaje)
            msm,x,y = recv_mensaje(mensaje)
            if mensaje == "servidor no disponible":
                print("presione enter para terminar.....")
                contin = False
            elif mensaje == "fin":
                print("*******fin de la partida********")
                contin = False
            elif mensaje == "link start":
                print("iniciando tablero")
                imagen = PhotoImage(file="imagen/triki.png")
                fondo = Label(ventana, image = imagen).place(x=0,y=0)
                textlabel = Label(ventana, text="Su turno: ").place(x=100,y=282)
                turnoC = Label(ventana, image=imagen_R).place(x=170,y=285)
                #cambio = True
            elif mensaje == "su turno":
                turnoC = Label(ventana, image=imagen_V).place(x=170,y=285)
                suTurno = True
                #cambio = True
            elif mensaje == "valido":
                fondo1 = Label(ventana, image = imagen_J1)
                fondo1.place(x=Recambio[0],y=Recambio[1])
                turnoC = Label(ventana, image=imagen_R).place(x=170,y=285)
                #cambio = True
                suTurno = False
            elif mensaje == "O":
                imagen_J1 = imagen_o
                imagen_J2 = imagen_x
            elif mensaje == "X":
                imagen_J1 = imagen_x
                imagen_J2 = imagen_o
            elif mensaje == "invalido":
                suTurno = True
            elif msm:
                fondo2 = Label(ventana, image = imagen_J2).place(x=x,y=y)

        except socket.timeout:
            pass


    ventana.mainloop()
    s.send("exit".encode())

    '''
    gui = GUI()
    gui.start()
    hilos.append(gui)

    for i in range(2):
        hi = MyThread(s,i+1)
        hi.start()
        hilos.append(hi)

    for hilo in hilos:
        hilo.join() 
    '''

    print ("connect close")
    s.close()