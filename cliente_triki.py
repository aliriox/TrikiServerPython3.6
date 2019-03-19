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
import select
import threading
from tkinter import *

contin = True

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
        


if __name__ == '__main__':

    hilos = []

    #s = socket.socket()
    #s.settimeout(1)
    #s.connect(("localhost", 9999))
    print ("estas conctado al servidor")

    ventana = Tk()
    ventana.title("Bienvenido a alirixTriki!!")
    ventana.geometry("600x600")
    ventana.mainloop()

    #for i in range(2):
    #    hi = MyThread(s,i+1)
    #    hi.start()
    #    hilos.append(hi)

    #for hilo in hilos:
    #    hilo.join()  

    print ("connect close")
    #s.close()