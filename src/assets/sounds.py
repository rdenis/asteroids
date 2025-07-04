def load_sound(file_path):
    """Load a sound file from the specified path."""
    import pygame
    sound = pygame.mixer.Sound(file_path)
    return sound

def play_sound(sound):
    """Play the specified sound."""
    sound.play()