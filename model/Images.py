from pathlib import Path

class Images:
    def __init__(self):
        # Imagenes del HomeScreen
        self.logo = Path("res/images/homeScreen/Logo-Home-Screen.png")
        self.iconPerson = Path("res/images/homeScreen/user.png")
        self.iconAcercaDe = Path("res/images/homeScreen/ayuda.png")
        
        # Imagenes del AboutScreen
        self.iconRegresar = Path("res/images/aboutScreen/volver.png")
        self.imageTicTacToe = Path("res/images/aboutScreen/tic-tac-toe.png")
        
        # Imagenes del GameScreen
        self.symbol_x = Path("res/images/gameScreen/borrar.png")
        self.symbol_o = Path("res/images/gameScreen/circle.png")

        
        self.backgroundImage = Path("res/images/background_main_screen.jpg")
        self.ticTacToeLogo = Path("res/images/tic-tac-toe-logo-v2.png")
        self.userHumanLogo = Path("res/images/user-human.png")
        self.userAgentAi = Path("res/images/user-artificial-inteligence.png")