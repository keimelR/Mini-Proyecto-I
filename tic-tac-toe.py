import pygame
from view.HomeScreen import HomeScreen
from view.AboutScreen import AboutScreen
from view.GameScreen import GameScreen
from view.RuleScreen import RuleScreen
from tkinter import Tk

# Ocultamos la ventana de Tkinter para evitar ventanas extra en blanco
root = Tk()
root.withdraw()

# Diccionario centralizado para el manejo de escenas
scenes = {}

# Instanciamos las escenas pasando el diccionario para que puedan comunicarse
scenes["home_screen"] = HomeScreen(scenes)
scenes["about_screen"] = AboutScreen(scenes)
scenes["game_screen"] = GameScreen(scenes)
scenes["rule_screen"] = RuleScreen(scenes)

# Configuración inicial del estado global
scenes["current"] = "home_screen" # Escena de inicio
scenes["running"] = True         # Control del bucle principal

# Bucle Principal del Juego (Manejador de Escenas)
while scenes.get("running", False):
    current_key = scenes.get("current")
    if not current_key:
        break
    
    scene = scenes.get(current_key)
    
    if scene is None:
        print(f"Error: La escena {current_key} no existe.")
        break
        
    # Ejecutar la lógica de la escena actual
    # Al salir de on_execute, el bucle volverá a verificar cual es la 'current' scene
    if hasattr(scene, "on_execute"):
        scene.on_execute()
    else:
        print(f"Error: La escena {current_key} no tiene el método on_execute.")
        break

pygame.quit()