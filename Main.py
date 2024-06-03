import sys
import pygame
import pygame_menu
import time
from music import MusicPlayer

import pygame_menu.widgets

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Car Park Puzzle")

# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0) 
GRAY = (128, 128, 128)

red_car = None
green_cars = []

# Inicializar el reproductor de música
music_player = MusicPlayer()

# Clase para los carros
class Car(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, direction):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction  # 'horizontal' o 'vertical'

    def move(self, x_change, y_change):
        self.rect.x += x_change
        self.rect.y += y_change

def set_dificultad(value, dificultad):
    global red_car, green_cars, dificultad_actual, play_button

    dificultad_actual = dificultad

    if dificultad == 1:
        # Crear carros para dificultad fácil
        red_car = Car(RED, 120, 60, 200, 300, 'horizontal')
        green_cars = [
            Car(YELLOW, 60, 120, 100, 100, 'vertical'),
            Car(YELLOW, 120, 60, 300, 100, 'horizontal'),
            Car(YELLOW, 120, 60, 300, 500, 'horizontal'),
            Car(YELLOW, 60, 120, 350, 300, 'vertical'),
            Car(YELLOW, 60, 120, 500, 250, 'vertical'),
        ]

    elif dificultad == 2:
        # Crear carros para dificultad normal
        red_car = Car(RED, 120, 60, 200, 300, 'horizontal')
        green_cars = [
            Car(YELLOW, 60, 120, 200, 40, 'vertical'),
            Car(YELLOW, 60, 120, 200, 170, 'vertical'),
            Car(YELLOW, 120, 60, 300, 220, 'horizontal'),
            Car(YELLOW, 120, 60, 300, 450, 'horizontal'),
            Car(YELLOW, 60, 120, 350, 300, 'vertical'),
            Car(YELLOW, 60, 120, 500, 250, 'vertical'),
        ]

    elif dificultad == 3:
        # Crear carros para dificultad difícil
        red_car = Car(RED, 120, 60, 200, 300, 'horizontal')
        green_cars = [
            Car(YELLOW, 120, 60, 100, 100, 'horizontal'),
            Car(YELLOW, 60, 120, 300, 50, 'vertical'),
            Car(YELLOW, 120, 60, 300, 400, 'horizontal'),
            Car(YELLOW, 120, 60, 500, 150, 'horizontal'),
            Car(YELLOW, 60, 120, 320, 270, 'vertical'),
            Car(YELLOW, 60, 120, 500, 250, 'vertical'),
        ]

    # Mostrar el botón de jugar después de seleccionar la dificultad
    play_button.show()

def start_the_game():
    global red_car, green_cars

    set_dificultad(None, dificultad_actual)

    # Crear la salida y definir las paredes
    exit_rect = pygame.Rect(740, 300, 65, 60)
    walls = [
        pygame.Rect(0, 0, 800, 10),  # Pared superior
        pygame.Rect(0, 10, 10, 600),  # Pared izquierda
        pygame.Rect(0, 590, 800, 10), # Pared inferior
        pygame.Rect(790, 0, 10, 600), # Pared derecha superior
    ]

    # Grupo de sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(red_car)
    all_sprites.add(*green_cars)

    # Mensaje de victoria
    font = pygame.font.Font(None, 53)
    win_text = font.render("¡Has llegado a la salida!", True, WHITE)
    size = win_text.get_rect(center=(400, 300))

    # Carro seleccionado
    selected_car = red_car

    # Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Seleccionar un carro
                pos = pygame.mouse.get_pos()
                for car in all_sprites:
                    if car.rect.collidepoint(pos):
                        selected_car = car
                        break

        # Movimiento del carro seleccionado y control del volumen
        keys = pygame.key.get_pressed()
        if keys[pygame.K_KP2]:  # Bajar volumen
            music_player.vol_Down()
        if keys[pygame.K_KP8]:  # Subir volumen
            music_player.vol_Up()
        if keys[pygame.K_KP5]:  # Mute y unmute
            music_player.muteORdemue()

        if selected_car:
            x_change = 0
            y_change = 0
            if selected_car.direction == 'horizontal':
                if keys[pygame.K_LEFT]:
                    x_change = -1
                if keys[pygame.K_RIGHT]:
                    x_change = 1
            elif selected_car.direction == 'vertical':
                if keys[pygame.K_UP]:
                    y_change = -1
                if keys[pygame.K_DOWN]:
                    y_change = 1

            # Mover el carro y verificar colisiones
            if x_change != 0 or y_change != 0:
                selected_car.move(x_change, y_change)
                collision = pygame.sprite.spritecollideany(selected_car, all_sprites, collided=lambda x, y: x != y and pygame.sprite.collide_rect(x, y))
                if collision:
                    selected_car.move(-x_change, -y_change)

        # Comprobar si el carro rojo está en la salida
        if red_car.rect.colliderect(exit_rect):
            screen.blit(win_text, size)
            pygame.display.flip()
            time.sleep(2)
            running = False

        # Asegurar que los carros no salgan de la pantalla
        for car in all_sprites:
            if car.rect.left < 10:
                car.rect.left = 10
            if car.rect.right > 790:
                car.rect.right = 790
            if car.rect.top < 10:
                car.rect.top = 10
            if car.rect.bottom > 590:
                car.rect.bottom = 590

        # Dibujar todo
        screen.fill(GRAY)
        for wall in walls:
            pygame.draw.rect(screen, BLACK, wall)  # Dibujar las paredes
        pygame.draw.rect(screen, RED, exit_rect)  # Dibujar la salida
        all_sprites.draw(screen)

        # Dibujar un borde alrededor del carro seleccionado
        if selected_car:
            pygame.draw.rect(screen, GREEN, selected_car.rect, 3)

        pygame.display.flip()

# Apariencia del menu:
apariencia = pygame_menu.Theme(
    background_color=(50, 50, 50),
    title_background_color=(0, 0, 0),
    title_font_shadow=True,
    title_font=pygame_menu.font.FONT_8BIT,
    widget_font=pygame_menu.font.FONT_NEVIS, 
    widget_font_color=(255, 255, 255),
    widget_margin=(0, 30),
    selection_color=(255, 255, 0),
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE,  # Estilo para la barra del título
    title_font_color=(255, 255, 255),
    title_font_size=50,  # Tamaño de fuente del título
    widget_font_size=30  # Tamaño de fuente de los widgets
)

# Crear el menú y agregar las opciones de dificultad
menu = pygame_menu.Menu('Car Puzzle', 800, 600, theme=apariencia)
menu.add.dropselect('Dificultad:', [('Principiante', 1), ('Normal', 2), ('Experto', 3)], onchange=set_dificultad)

play_button = menu.add.button('Jugar', start_the_game)
play_button.hide()  # Ocultar el botón de jugar inicialmente

menu.add.button('Salir', pygame_menu.events.EXIT)

# Bucle principal del menú
while True:
    screen.fill(BLACK)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)
    pygame.display.flip()
