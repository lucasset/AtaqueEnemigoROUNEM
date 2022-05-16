import pygame
from pygame.sprite import Sprite

class Medusa(Sprite):
	#Sirve para representar a un solo alienígena en la flota
	def __init__(self, us_configuracion, pantalla):
		#Inicializa el medusa y establece su posición inicial
		super(Medusa, self).__init__()

		self.pantalla = pantalla
		self.us_configuracion = us_configuracion

		# Carga la imagen del medusa y establece su atributo rect
		self.image = pygame.image.load("imagenes/monster.bmp")
		self.rect = self.image.get_rect()

		# Inicia cada nuevo medusa cerca de la parte superior izquierda de la pantalla
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# Almacena la posición exacta del medusa
		self.x = float(self.rect.x)

	def blitme(self):
		#Dibuja el medusa en su ubicación actual
		self.pantalla.blit(self.image, self.rect)

	def check_edges(self):
		#Devuelve Verdadero si el medusa está en el borde de la pantalla
		screen_rect = self.pantalla.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True	

	def update(self):
		#Mueve el medusa a la derecha
		#self.x += (self.us_configuracion.medusa_speed_factor *
		#	           self.us_configuracion.fleet_direction)
		self.x += (self.us_configuracion.medusa_speed_factor *	self.us_configuracion.fleet_direction)
		self.rect.x = self.x