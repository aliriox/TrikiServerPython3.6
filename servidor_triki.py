"""
				/////////////////////////////////////////
				/										/
				/	PYTHON VERSION 3.6.4				/
				/	MYSQLCONNECTOR VERSION 8.0.15		/
				/	AUTHOR: ALIRIOX						/
				/	SERVIDOR VERSION: MARIADB 10.1.36	/
				/	TKINTER VERSION 8.6.6				/
				/										/
				/////////////////////////////////////////
"""
import mysql.connector
from mysql.connector import errorcode
import socket
import threading
import time

# se define una lista de hilos que conectan con los clientes del servidor
# tantos hilos como clientes necesiten
hilos = []
# definimos el tablero como una matriz 3 x 3
tablero = [[[],[],[]],[[],[],[]],[[],[],[]]]
# estimamos la cantidad de usuarios ya conectados como una variable global para restricciones
jugadores_conectados = 0
# se determina de manera global el turno para poder jugar por turnos como lo especifica el juego
# de primera mano se le asigna el primer turno al primer cliente que se conecte con el servidor
turno = 1


# funcion que llena el tablero de ceros
def llenarTableroDefault():
	global tablero
	for i in range(3):
		for j in range(3):
			tablero[i][j] = 0

# funcion que imprime lo que hay en el tablero
def printTablero():
	global tablero
	for i in range(3):
		cadena = ""
		for j in range(3):
			cadena = cadena + "["+str(tablero[i][j])+"]"
		print(cadena)

# funcion que me permite saber si hay alguna jugada disponible en el juego
def esposiblejugar():
	global tablero
	tmp = False
	for i in tablero:
		for j in i:
			if j == 0:
				tmp = True
	return tmp		

# funcion que evalua el tablero y determina si hay un ganador
def bucarGanador():
	global tablero
	hayganador = False
	mensaje = ""

	# se define jugador uno y se representa en el tablero con 1
	# se define jugador dos y se representa en el tablero con -1
	# para el tablero los espacios que no han sido ocupados se definen con 0

	# buscamos un ganador por las filas y las columnas del tablero
	# hay ganador si una fila suma 3 o -3

	for i in range(3):
		contador1 = 0
		contador2 = 0
		for j in range(3):
			contador1 += tablero[i][j]
			contador2 += tablero[j][i]
		if contador1 == 3 or contador2 == 3:
			print ("ganador jugador1")
			hayganador = True
			mensaje = "ganador jugador1"
		elif contador1 == -3 or contador2 == -3:
			print ("ganador jugador2")
			hayganador = True
			mensaje = "ganador jugador2"
		else:
			pass

	# ahora buscamos un ganador por las diagonales del juego
	if tablero[0][0] + tablero[1][1] + tablero[2][2] == 3:
		print ("ganador jugador1")
		hayganador = True
		mensaje = "ganador jugador1"
	elif tablero[0][2] + tablero[1][1] + tablero[2][0] == -3:
		print ("ganador jugador2")
		hayganador = True
		mensaje = "ganador jugador2"
	else:
		pass

	if not esposiblejugar():
		hayganador = True
		mensaje = "se declara empate"	

	return hayganador, mensaje	

def ingresarTablero(x , y, valor):
	global tablero
	global turno

	tablero[x][y] = valor
	if valor == 1:
		turno += 1
	elif valor == -1:
		turno -= 1

# funcion que me permite cambiar los valores del tablero si esta disponible
def boolingresarTablero(x , y):
	global tablero
	global turno

	if tablero[x][y] == 0:
		return True
	else:
		return False



def validarjugada(msm, turno):

	valor = 0

	if turno == 1:
		valor = 1
	else:
		valor = -1

	posicion = 0

	try:
		posicion = int(msm)
	except ValueError:
		pass

	x = -1
	y = -1
	if posicion == 1:
		x = 0
		y = 0
	elif posicion == 2:
		x = 0;
		y = 1;
	elif posicion == 3:
		x = 0;
		y = 2;
	elif posicion == 4:
		x = 1;
		y = 0;
	elif posicion == 5:
		x = 1;
		y = 1;
	elif posicion == 6:
		x = 1;
		y = 2;
	elif posicion == 7:
		x = 2;
		y = 0;
	elif posicion == 8:
		x = 2;
		y = 1;
	elif posicion == 9:
		x = 2;
		y = 2;
	else:
		print("ingreso de posicion invalida")

	return x,y,valor

# funcion de ingresar datos en una base de datos
def ingresarusuario(crs):

	nombres = input("ingrese nombres: ")
	apellidos = input("ingrese apellidos: ")
	usuario = input("ingrese el user: ")
	contrasenia = input("ingrese el password: ")
	sql = ("insert into usuarios (nombres, apellidos, usuario, contraseña) "
		"values ('"+nombres+"','"+apellidos+"','"+usuario+"','"+contrasenia+"')")

	crs.execute(sql)

# funcion de actualizar datos en una base de datos
def updateusuario(crs):

	nm = input("ingrese llave del usuario a actualizar")
	nombres = input("ingrese nombres: ")
	apellidos = input("ingrese apellidos: ")
	usuario = input("ingrese el user: ")
	contrasenia = input("ingrese el password: ")
	sql = ("update usuarios set "
		"nombres = '"+nombres+"', "
		"apellidos = '"+apellidos+"', "
		"usuario = '"+usuario+"', "
		"contraseña = '"+contrasenia+"' "
		"where id_usuario = "+nm+";")

	crs.execute(sql)

# funcion de consulta de datos en la base de datos
def obtenerdatos(crs):

	sql = "select * from usuarios"
	crs.execute(sql)
	for i in crs:
		print(i)

# funcion de eliminar registro de la base de datos
def deleteuser(crs):
	id_u = input("ingrese la id del usuario a eliminar")
	sql = "delete from usuarios where id_usuario = "+id_u+";"
	crs.execute(sql)

# funcion que me permite establecer conexion en la base de datos
def connectorDB():
	try:
		cnx = mysql.connector.connect(user='root',
		                            database='trikidb')
		cursor = cnx.cursor()
		#ingresarusuario(cursor)
		obtenerdatos(cursor)
		#updateusuario(cursor)
		#deleteuser(cursor)
		cnx.commit()
		cursor.close()
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cnx.close()
	cnx.close()

# Esta clase es la que me permite manejar los hilos ... en este caso conecta a los clientes en el servidor
# para interactuar entre ellos
class MyThread(threading.Thread):
	def __init__(self, socket, num):
		super(MyThread, self).__init__()
		global jugadores_conectados
		self.socket = socket
		self.sc, self.addr = socket.accept()
		self.conectado = True
		print ("usuario "+str(num)+ " se ha conectado")
		self.sc.settimeout(1) 
		self.num = num
		jugadores_conectados += 1

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

	def estaConectado(self):
		return self.conectado

	def enviarTablero(self):
		global tablero

		for i in range(3):
			cadena = ""
			for j in range(3):
				cadena = cadena + "["+str(tablero[i][j])+"]"
			self.mensaje(cadena)
			time.sleep(0.1)

	def run(self):

		global hilos
		global jugadores_conectados
		global turno
		
		enviartablero = True
		bienvenidos = False
		advertespera = False

		if self.num != -1:
			while True:
				ganador, msm = bucarGanador()
				if ganador:
					self.mensaje(msm)
					print("Fin de la partida")
					time.sleep(0.1)
					self.mensaje("fin")
					break
				elif jugadores_conectados >= 2:
					advertespera = False
					if not bienvenidos:
						self.mensaje("   Bienvenidos a aliriox Triki!!!  ")
						time.sleep(0.5)
						self.mensaje("todos los jugadores estan conectados")
						time.sleep(0.5)
						self.mensaje("link start")
						time.sleep(1)
						if self.num == 1:
							self.mensaje("X")
						elif self.num == 2:
							self.mensaje("O")
						else:
							pass
						bienvenidos = True
					#print(turno)
					if self.num == turno:
						if enviartablero:
						#	self.enviarTablero()
							self.mensaje("su turno")
							time.sleep(0.5)
							enviartablero = False

						mensaje = None
						try:
							mensaje = self.sc.recv(1024)
							mensaje = mensaje.decode()
							if mensaje == "exit":
								print ("usuario "+str(self.num)+" cerro sesion")
								self.conectado = False
								jugadores_conectados -= 1
								for i in hilos:
									if i.Num() != -1 and i.Num() != self.num and i.estaConectado():
										i.mensaje("usuario "+str(self.num)+" cerro sesion")
								if self.num == 1:
									turno = 2
								elif self.num == 2:
									turno = 1
								enviartablero = True
								break
							else:
								if esposiblejugar():
									x,y,valor = validarjugada(mensaje,self.num)
									if x != -1 and boolingresarTablero(x,y):
										ingresarTablero(x,y,valor)
										self.mensaje("valido")
										printTablero()
										if self.num == 1:
											turno = 2
										elif self.num == 2:
											turno = 1
										for i in hilos:
											if i.Num() != -1 and i.Num() != self.num and i.estaConectado():
												i.mensaje(mensaje)
										enviartablero = True
									else:
										self.mensaje("invalido")
								else:
									self.mensaje("empate")
						except socket.timeout:
							pass
					else:
						mensaje = None
						try:
							mensaje = self.sc.recv(1024)
							mensaje = mensaje.decode()
							self.mensaje("espere su turno")
						except socket.timeout:
							pass
				else:
					if not advertespera:
						self.mensaje("...esperando jugadores...")
						advertespera = True
					try:
						mensaje = self.sc.recv(1024)
						mensaje = mensaje.decode()
						if mensaje == "exit":
							print ("usuario "+str(self.num)+" cerro sesion")
							self.conectado = False
							jugadores_conectados -= 1
							if self.num == 1:
								turno = 2
							elif self.num == 2:
								turno = 1
						else:
							advertespera = True
					except socket.timeout:
						pass
			self.sc.close()
			self.sc, self.addr = self.socket.accept()
			print ("usuario "+ str(self.num) + " se ha conectado")
			jugadores_conectados += 1
			self.conectado = True
			bienvenidos = False
			enviartablero = True
			self.run()
		else:
			mensaje = "servidor no disponible"
			self.sc.send(mensaje.encode())
			print ("usuario "+ str(self.num) + " a sido rechazado:: servidor lleno")
			self.sc.close()
			if not self.revisar():
				self.sc, self.addr = self.socket.accept()
				self.run()

if __name__ == '__main__':
	s = socket.socket()   
	s.bind(("localhost", 9999))  
	s.listen(1)

	llenarTableroDefault()
	printTablero()

	for i in range(2):
		print ("esperando conexion")
		hi = MyThread(s,i+1)
		hi.start()
		hilos.append(hi)

	hier = MyThread(s,-1)
	hier.start()
	hilos.append(hier)

	for hilo in hilos:
		hilo.join()
	#connectorDB()