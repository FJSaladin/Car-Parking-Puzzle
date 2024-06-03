import os
import pygame

class MusicPlayer(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # Obtener la ruta del directorio actual del script
        base_path = os.path.dirname(__file__)
        
        # Construir la ruta completa del archivo de sonido usando una ruta relativa
        sound_path = os.path.join(base_path, "assets", "Sonidos", "music.mp3")
        
        # Verificación de la existencia del archivo
        if not os.path.exists(sound_path):
            print(f"El archivo de sonido no existe en la ruta especificada: {sound_path}")
            return
        
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)
        self.current_volume = 0.5  # Volumen inicial entre 0.0 y 1.0
        self.set_volume(self.current_volume)

    def set_volume(self, volume):
        # Asegurarse de que el volumen esté en el rango de 0.0 a 1.0
        self.current_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.current_volume)

    def vol_Up(self):
        self.set_volume(1.0)

    def vol_Down(self):
        self.set_volume(0.1)

    def muteORdemue(self):
        if self.current_volume == 0.0:
            self.set_volume(0.5)  # Restaurar el volumen a la mitad
        else:
            self.set_volume(0.0)  # Silenciar el volumen

# Crear una instancia del reproductor de música para probar
music_player = MusicPlayer()
