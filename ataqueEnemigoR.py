import pygame
from pygame.sprite import Group

from configuraciones import Configuraciones
from estadisticas import Estadisticas
from marcador import Marcador
from button import Button
from nave import Nave

import funciones_juego as fj

def run_game():
	# Inicializar el juego, las configuraciones y crear un objeto pantalla
	pygame.init()
	us_configuracion = Configuraciones()
	pantalla = pygame.display.set_mode(
		(us_configuracion.screen_width, us_configuracion.screen_height))
	pygame.display.set_caption("Ataque Enemigo Rounem")

	# Crea el botón Play
	play_button = Button(us_configuracion, pantalla, "Play")


	# Crea una instancia para almacenar estadísticas del juego y crea un marcador
	estadisticas = Estadisticas(us_configuracion)
	marcador = Marcador(us_configuracion, pantalla, estadisticas)

	# Crea una nave, un grupo de balas y un grupo de medusas
	nave = Nave(us_configuracion, pantalla)
	balas = Group()
	medusas = Group()

	# Crea la flota de medusas
	fj.crear_flota(us_configuracion, pantalla, nave, medusas)
 

    # Iniciar el bucle principal del juego
	while True:
		
		# Escuchar eventos de teclado o de ratón
		fj.verificar_eventos(us_configuracion, pantalla, estadisticas, marcador,
			play_button, nave, medusas, balas)

		if estadisticas.game_active:
			nave.update()
			fj.update_balas(us_configuracion, pantalla, estadisticas,
				marcador, nave, medusas, balas)
			fj.update_medusas(us_configuracion, estadisticas, pantalla, marcador, nave, medusas, balas)
		
		fj.actualizar_pantalla(us_configuracion, pantalla, estadisticas, 
			marcador, nave, medusas, balas, play_button)

run_game()