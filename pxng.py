'''

> Practica de creacion de videojuego con pygame y programacion orientada a objetos.

* Juego a desarrollar: Una version de PONG.

'''



#> LIBRERIAS <#
import pygame
import random


#> CLASES <#
class Ventana():
	
	#Constructor
	def __init__(self, an_al):
		self.__AN_AL = an_al
		self.__VENT = None

	def crear_ventana(self):
		self.__VENT = pygame.display.set_mode(self.__AN_AL)

	def poner_nombre_ventana(self, nombre):
		pygame.display.set_caption(nombre)

	def poner_fondo_ventana(self, col):
		self.__VENT.fill(col)

	def control_cerrar_ventana(self, evento):
		#Cierra ventana con boton "cerrar"
		if evento.type == pygame.QUIT:
			return False
			pygame.quit()

		#Cierra ventana con "esc"
		if evento.type == pygame.KEYDOWN:
			if evento.key == pygame.K_ESCAPE:
				return False
				pygame.quit()

	#Getter atributo "VENT"
	def get_vent(self):
		return self.__VENT

	#Getter atributo "AN_AL"
	def get_dimension(self):
		return self.__AN_AL

	#Getters eje x de la dim. de pantalla
	def get_dim_x(self):
		return self.__AN_AL[0]

	#Getters eje y de la dim. de pantalla
	def get_dim_y(self):
		return self.__AN_AL[1]


class Linea():

	#Constructor
	def __init__(self, **kwargs):
		self.__ubicacion = kwargs["ubic"]
		self.__color = kwargs["col"]
		self.__inicio_pos = [kwargs["inicio_pos"] / 2, 30]
		self.__fin_pos = [kwargs["inicio_pos"] / 2, kwargs["fin_pos"] - 30]
		self.__ancho = kwargs["anch"]

	def dibujar(self):
		linea = pygame.draw.line(self.__ubicacion, self.__color, self.__inicio_pos, self.__fin_pos, self.__ancho)


class Cuadrado():

	#Contructor
	def __init__(self, **kwargs):
		self.__ubicacion = kwargs["ubic"]
		self.__color = kwargs["col"]
		self.__form_jug = pygame.Rect(kwargs["x"], kwargs["y"], kwargs["anch"], kwargs["alt"])
		self.__valor_a, self.__valor_b = False, False

	def dibujar(self):
		pygame.draw.rect(self.__ubicacion, self.__color, self.__form_jug)

	def controles(self, evento, tcl_control):
		#Verifica el boton presionado
		if evento.type == pygame.KEYDOWN:
			#Arriba
			if evento.key == tcl_control["ARR"]:
				self.__valor_a = True

			#Abajo
			if evento.key == tcl_control["ABA"]:
				self.__valor_b = True

		if evento.type == pygame.KEYUP:
			#Arriba
			if evento.key == tcl_control["ARR"]:
				self.__valor_a = False

			#Abajo
			if evento.key == tcl_control["ABA"]:
				self.__valor_b = False

	def mover(self, valor_mov, dim_vent):
		#Los movimientos ya tienen las colisiones
		if self.__valor_a and self.__form_jug.y > 0:
			self.__form_jug.y -= valor_mov
		if self.__valor_b and self.__form_jug.y + self.__form_jug.height < dim_vent[1]:
			self.__form_jug.y += valor_mov

	def get_form_jug(self):
		return self.__form_jug


class Redondo():

	#Constructor
	def __init__(self, ubic, col, x, y, rad):
		self.__ubicacion = ubic
		self.__color = col
		self.__form_bol = pygame.Rect(x, y, 11, 11)
		self.__radio = rad
		self.__vel = 6
		self.__vel_mov = [random.choice([self.__vel, -self.__vel]), random.choice([self.__vel, -self.__vel])]

	def dibujar(self):
		pygame.draw.ellipse(self.__ubicacion, self.__color, self.__form_bol)

	#Verifica si no se tocan los bordes de la pantalla y/o los jugadores
	def aplicar_fisica(self, dim_vent, jug_a, jug_b):
		#Colision con las paredes
		#Y
		if self.__form_bol.top <= 0 or self.__form_bol.bottom >= dim_vent[1]:
			self.__vel_mov[1] = -self.__vel_mov[1]

		#Colision con los jugadores
		if self.__form_bol.colliderect(jug_a):
			if self.__form_bol.left <= jug_a.right:
				self.__vel_mov[0] = -self.__vel_mov[0]

		if self.__form_bol.colliderect(jug_b):
			if self.__form_bol.right >= jug_a.left:
				self.__vel_mov[0] = -self.__vel_mov[0]


		if self.__form_bol.x < -10 or self.__form_bol.x > dim_vent[0]:
			self.__form_bol.x = dim_vent[0] / 2
			self.__form_bol.y = dim_vent[1] / 2
			jug_a.y = (dim_vent[1] / 2) - 50
			jug_b.y = (dim_vent[1] / 2) - 50
			pygame.time.delay(1000)

		#Visualiza las coordenadas de las colisiones
		print(str(self.__form_bol.topleft))
		#print("* bol - jug_a: " + str(self.__form_bol.left) + " - " + str(jug_a.right) + " = " + str(self.__form_bol.left - jug_a.right))
		#print("* bol - jug_b: " + str(self.__form_bol.right) + " - " + str(jug_b.left) + " = " + str(self.__form_bol.right - jug_b.left))

		#Mueve el objeto dentro de la pantalla de forma random
		self.__form_bol.move_ip(-self.__vel_mov[0], self.__vel_mov[1])


class Principal():

	#Constructor
	def __init__(self):
		self.__DIMENSIONES = (800, 600)
		self.__dist_mov_jug = 7
		self.__redon_x, self.__redon_y = 400, 300
		self.__radio = 7
		self.__ancho_linea = 2
		self.__fps = 0
		self.__colores =	{
							"NEG": (0, 0, 0),
							"BLA": (255, 255, 255)
							}
		self.__tcl_jug_a = {
							"ARR": pygame.K_w,
							"ABA": pygame.K_s
							}
		self.__tcl_jug_b = {
							"ARR": pygame.K_UP,
							"ABA": pygame.K_DOWN
							}

	def ejecutar(self):
		#Inicia modulos de pygame
		pygame.init()

		#Ayuda a tomar el tiempo en milisegundos
		relog = pygame.time.Clock()

		#Crea la ventana y sus elementos
		vent = Ventana(self.__DIMENSIONES)
		vent.crear_ventana()
		vent.poner_nombre_ventana("PONG!")
		linea = Linea(ubic=vent.get_vent(), col=self.__colores["BLA"], inicio_pos=vent.get_dim_x(), fin_pos=vent.get_dim_y(), anch=self.__ancho_linea)
		jug_a = Cuadrado(x=20, y=250, alt=80, anch=6, ubic=vent.get_vent(), col=self.__colores["BLA"])
		jug_b = Cuadrado(x=774, y=250, alt=80, anch=6, ubic=vent.get_vent(), col=self.__colores["BLA"])
		bolita = Redondo(vent.get_vent(), self.__colores["BLA"], self.__redon_x, self.__redon_y, self.__radio)

		#Bucle principal para ejecutar juego
		corre = True
		while corre:
			#Graficos
			vent.poner_fondo_ventana(self.__colores["NEG"])
			linea.dibujar()
			jug_a.dibujar()
			jug_b.dibujar()
			bolita.dibujar()

			#Controles (Manejador de eventos)
			for e in pygame.event.get():
				if vent.control_cerrar_ventana(e) != None:
					corre = vent.control_cerrar_ventana(e)

				#Se verifican si se presionan las teclas
				jug_a.controles(e, self.__tcl_jug_a)
				jug_b.controles(e, self.__tcl_jug_b)

			#Mueve al jugador
			jug_a.mover(self.__dist_mov_jug, vent.get_dimension())
			jug_b.mover(self.__dist_mov_jug, vent.get_dimension())

			#Ejecuta las fisica de la bolita
			bolita.aplicar_fisica(vent.get_dimension(), jug_a=jug_a.get_form_jug(), jug_b=jug_b.get_form_jug())

			#Actualiza el relog (Limita los fps)
			relog.tick(60)
			self.__fps = relog.get_fps() #Almacena el numero de fps

			#Actualiza contenido en pantalla
			pygame.display.flip()

	def fps(self):
		import subprocess
		subprocess.run(["clear"]) #Ejecuta comando linux
		print(">FPS OBTENIDOS: " + str(self.__fps))



#> EJECUCION PRINCIPAL <#
corre = Principal()
corre.ejecutar()
#corre.fps()