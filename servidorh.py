import socket
import threading

hilos = []

class MyThread(threading.Thread):
    def __init__(self, socket, num):
        super(MyThread, self).__init__()
        self.socket = socket
        self.sc, self.addr = socket.accept()
        print ("usuario "+str(num)+ " se ha conectado")
        self.sc.settimeout(1) 
        self.num = num

    def revisar(self):
        global hilos
        if len(hilos) == 1:
            return True
        else:
            return False

    def Num(self):
        return self.num

    def mensaje(self,msm):
        msm = msm.encode()
        self.sc.send(msm)

    def run(self):
        global hilos
        if self.num != -1:
            while True:
                mensaje = None
                try:
                    mensaje = self.sc.recv(1024)
                    mensaje = mensaje.decode()
                    if mensaje == "exit":
                        print ("usuario "+str(self.num)+" cerro sesion")
                        break
                    else:
                        print ("usuario "+str(self.num)+" dice: "+ mensaje)
                        for i in hilos:
                            if i.Num() != self.num and i.Num() != -1:
                                i.mensaje(mensaje)
                except socket.timeout:
                    pass

            self.sc.close()
            self.sc, self.addr = self.socket.accept()
            print ("usuario "+ self.num + " se ha conectado")
            self.run()
        else:
            mensaje = "servidor no disponible"
            self.sc.send(mensaje.encode())
            self.sc.close()
            if not self.revisar():
                self.sc, self.addr = self.socket.accept()
                self.run()


s = socket.socket()   
s.bind(("localhost", 9999))  
s.listen(1) 

if __name__ == '__main__':

    for i in range(1):
        print ("esperando conexion")
        hi = MyThread(s,i+1)
        hi.start()
        hilos.append(hi)

    hier = MyThread(s,-1)
    hier.start()
    hilos.append(hier)

    for hilo in hilos:
        hilo.join()  
 
s.close() 