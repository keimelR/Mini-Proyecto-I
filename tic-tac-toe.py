from view.MainScreen import MainScreen
from view.HomeScreen import HomeScreen
from view.AboutScreen import AboutScreen
from view.GameScreen import GameScreen
from tkinter import Tk

# Ocultamos la ventana de Tkinter (si es necesaria)
root = Tk()
root.withdraw()

mainScreen: MainScreen = MainScreen()
mainScreen.on_execute()
"""
# Diccionario con las escenas
scenes = {}

# Instanciamos las escenas
scenes["home_screen"] = HomeScreen(scenes)
scenes["about_screen"] = AboutScreen(scenes)
scenes["game_screen"] = GameScreen(scenes)

# Escena inicial
scenes["current"] = "home_screen"

# Flag global de ejecución (las escenas deben establecerla a False en QUIT)
scenes["running"] = True

# Bucle de escenas
while scenes.get("running", False):
    current_key = scenes.get("current")
    if not current_key:
        break
    scene = scenes.get(current_key)
    if scene is None:
        break
    # Cada escena debe implementar on_execute y salir cuando quiera ceder el control
    if hasattr(scene, "on_execute"):
        scene.on_execute()
"""