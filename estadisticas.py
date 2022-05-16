class Estadisticas():
	#Seguimiento de las estadísticas de Invasión Alienígena
	def __init__(self, us_configuracion):
		#Inicializa las estadísticas
		self.us_configuracion = us_configuracion
		self.reset_stats()

		# Inicia Invasión Alienígena en un estado activo
		self.game_active = False

		# La puntuación alta nunca debe restablecerse
		self.alto_puntaje = 0


	def reset_stats(self):
		#Inicializa estadísticas que pueden cambiar durante el juego
		self.naves_restantes = self.us_configuracion.cantidad_naves
		self.puntaje = 0
		self.nivel = 1
		