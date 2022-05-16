import sys
from time import sleep

import pygame
from bala import Bala

from medusa import Medusa

def verificar_eventos_keydown(event, us_configuracion, pantalla, nave, balas):
	#Responde a las pulsaciones de teclas
	if event.key == pygame.K_RIGHT:
		nave.moving_right = True
	elif event.key == pygame.K_LEFT:
		nave.moving_left = True	
	elif event.key == pygame.K_SPACE:
		fuego_bala(us_configuracion, pantalla, nave, balas)
	elif event.key == pygame.K_q:
		sys.exit()



def verificar_eventos_keyup(event, nave):
	#Responde a las pulsaciones de teclas
	if event.key == pygame.K_RIGHT:
		nave.moving_right = False
	elif event.key == pygame.K_LEFT:
		nave.moving_left = False	

def verificar_eventos(us_configuracion, pantalla, estadisticas, marcador,
	play_button, nave, medusas, balas):
	#Responde a las pulsaciones de teclas y los eventos del ratón
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			verificar_eventos_keydown(event, us_configuracion, pantalla, nave, balas)

		elif event.type == pygame.KEYUP:
			verificar_eventos_keyup(event, nave)

		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(us_configuracion, pantalla, estadisticas, marcador,
				play_button, nave, medusas, balas, mouse_x, mouse_y)

def check_play_button(us_configuracion, pantalla, estadisticas, marcador,
	play_button, nave, medusas, balas, mouse_x, mouse_y):
	#Comienza un nuevo juego cuando el jugador hace clic en Play
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not estadisticas.game_active:
		# Restablece la configuración del juego
		us_configuracion.inicializa_configuraciones_dinamicas()
		
		# Ocultar el cursor del ratón
		pygame.mouse.set_visible(False)

		# Restablece las estadísticas del juego
		estadisticas.reset_stats()
		estadisticas.game_active = True

		# Restablece las imágenes de marcador
		marcador.prep_puntaje()
		marcador.prep_alto_puntaje()
		marcador.prep_nivel()
		marcador.prep_naves()

		# Vacía la lista de medusas y balas
		medusas.empty()
		balas.empty()

		# Crea una nueva flota y centra la nave
		crear_flota(us_configuracion, pantalla, nave, medusas)
		nave.centrar_nave()



def actualizar_pantalla(us_configuracion, pantalla, estadisticas, 
	marcador, nave, medusas, balas, play_button):
	#Actualiza las imágenes en la pantalla y pasa a la nueva pantalla

	# Volver a dibujar la pantalla durante cada pasada por el bucle
	pantalla.fill(us_configuracion.bg_color)
	# Vuelve a dibujar todas las balas detrás de la nave y de los extraterrestres
	for bala in balas.sprites():
		bala.draw_bala()
	nave.blitme()
	medusas.draw(pantalla)

	# Dibuja la información de la puntuación
	marcador.muestra_puntaje()

	# Dibuja el botón de Play si el juego está inactivo
	if not estadisticas.game_active:
		play_button.draw_button()

		
	# Hacer visile la pantalla dibujada más reciente
	pygame.display.flip()

def update_balas(us_configuracion, pantalla, estadisticas, 
	marcador, nave, medusas, balas):
	#Actualiza la posición de las balas y elimina las antiguas
	# Actualiza las posiciones de las balas
	balas.update()

	#Deshace las balas que han desaparecido
	for bala in balas.copy():
		if bala.rect.bottom <= 0:
			balas.remove(bala)

	check_bala_medusa_collisions(us_configuracion, pantalla, estadisticas,
	marcador, nave, medusas, balas)


def check_bala_medusa_collisions(us_configuracion, pantalla, estadisticas,
	marcador, nave, medusas, balas):
	#Responde a las colisiones entre balas y medusas
	# Elimina las balas y los medusas que hayan chocado
	collisions = pygame.sprite.groupcollide(balas, medusas, True, True)

	if collisions:
		for medusas in collisions.values():
			estadisticas.puntaje += us_configuracion.puntos_medusa * len(medusas)
			marcador.prep_puntaje()
		verifica_alto_puntaje(estadisticas, marcador)

	if len(medusas) == 0:
		# Si se destruye toda la flota, comienza un nuevo nivel
		balas.empty()
		us_configuracion.aumentar_velocidad()

		# Incrementa el nivel
		estadisticas.nivel += 1
		marcador.prep_nivel()

		crear_flota(us_configuracion, pantalla, nave, medusas)


def verifica_alto_puntaje(estadisticas, marcador):
	#Verifica si existe un puntaje más alto
	if estadisticas.puntaje > estadisticas.alto_puntaje:
		estadisticas.alto_puntaje = estadisticas.puntaje
		marcador.prep_alto_puntaje()

def fuego_bala(us_configuracion, pantalla, nave, balas):
	#Dispara una bala si aún no ha alcanzado el límite
	# Crea una nueva bala y la agrega al grupo de balas
	if len(balas) < us_configuracion.balas_allowed:
		nueva_bala = Bala(us_configuracion, pantalla, nave)
		balas.add(nueva_bala)

def get_number_medusas_x(us_configuracion, medusa_width):
	#Determina el número de medusas que caben en una fila
	available_space_x = us_configuracion.screen_width - 2 * medusa_width
	number_medusas_x = int(available_space_x / (2 * medusa_width))
	return number_medusas_x

def get_number_rows(us_configuracion, nave_height, medusa_height):
	#Determina el número de filas de medusas que se ajustan en la pantalla
	available_space_y = (us_configuracion.screen_height - 
		                  (3 * medusa_height) - nave_height)
	number_rows = int(available_space_y / (2 * medusa_height))
	return number_rows

def crear_medusa(us_configuracion, pantalla, medusas, medusa_number, row_number):
	#Crea un medusa y lo coloca en la fila
	medusa = Medusa(us_configuracion, pantalla)
	medusa_width = medusa.rect.width
	medusa.x = medusa_width + 2 * medusa_width * medusa_number
	medusa.rect.x = medusa.x
	medusa.rect.y = medusa.rect.height + 2 * medusa.rect.height * row_number
	medusas.add(medusa)

def crear_flota(us_configuracion, pantalla, nave, medusas):
	#Crea una flota completa de medusas
	# Crea un medusa y encuentra el número de medusas seguidos
	# El espacio entre cada medusa es igual a un ancho del medusa
	medusa = Medusa(us_configuracion, pantalla)
	number_medusas_x = get_number_medusas_x(us_configuracion, medusa.rect.width)
	number_rows = get_number_rows(us_configuracion, nave.rect.height, medusa.rect.height)


	# Crea la flota de medusas
	for row_number in range(number_rows):
		for medusa_number in range(number_medusas_x):
			crear_medusa(us_configuracion, pantalla, medusas, medusa_number, row_number) 

def check_fleet_edges(us_configuracion, medusas):
	#Responde de forma apropiada si algún medusa ha llegado a un borde
	for medusa in medusas.sprites():
		if medusa.check_edges():
			change_fleet_direction(us_configuracion, medusas)
			break

def change_fleet_direction(us_configuracion, medusas):
	#Desciende toda la flota y cambia la dirección de la flota
	for medusa in medusas.sprites():
		medusa.rect.y += us_configuracion.fleet_drop_speed
	us_configuracion.fleet_direction *= -1

def nave_golpeada(us_configuracion, estadisticas, pantalla, marcador, nave, medusas, balas):
	#Responde a una nave siendo golpeada por un medusa

	if estadisticas.naves_restantes > 0:
		# Disminuye naves_restantes
		estadisticas.naves_restantes -= 1

		# Actualiza el marcador
		marcador.prep_naves()

		# Vacía la lista de medusas y balas
		medusas.empty()
		balas.empty()

		# Crea una nueva flota y centra la nave
		crear_flota(us_configuracion, pantalla, nave, medusas)
		nave.centrar_nave()

		# Pausa
		sleep(0.5)

	else:
		estadisticas.game_active = False
		pygame.mouse.set_visible(True)



def check_medusas_bottom(us_configuracion, estadisticas, pantalla, marcador, nave, medusas, balas):
	#Comprueba si algún medusa ha llegado al final de la pantalla
	pantalla_rect = pantalla.get_rect()

	for medusa in medusas.sprites():
		if medusa.rect.bottom >= pantalla_rect.bottom:
			# Trata esto de la misma forma que si la nave fuera golpeada
			nave_golpeada(us_configuracion, estadisticas, pantalla, marcador, nave, medusas, balas)
			break

def update_medusas(us_configuracion, estadisticas, pantalla, marcador, nave, medusas, balas):
	#Comprueba si la flota está al borde y luego actualiza las posiciones de todos los medusas de la flota#
	check_fleet_edges(us_configuracion, medusas)
	medusas.update()

	# Busca colisiones de medusa-nave
	if pygame.sprite.spritecollideany(nave, medusas):
		nave_golpeada(us_configuracion, estadisticas, pantalla, marcador, nave, medusas, balas)

	# Busca medusas que golpean la parte inferior de la pantalla
	check_medusas_bottom(us_configuracion, estadisticas, pantalla, marcador, nave, medusas, balas)

