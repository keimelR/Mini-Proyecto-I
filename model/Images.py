import pygame.image
from pathlib import Path

class Images:
    def __init__(self):
        # Imagenes del HomeScreen
        self.logo = Path("res/images/homeScreen/Logo-Home-Screen.png")
        self.iconPerson = Path("res/images/homeScreen/user.png")
        self.iconAcercaDe = Path("res/images/homeScreen/ayuda.png")
        self.libro = Path("res/images/homeScreen/libro.png")
        self.robot = Path("res/images/homeScreen/robot.png")
     
        # Imagenes del AboutScreen
        self.iconRegresar = Path("res/images/aboutScreen/volver.png")
        self.imageTicTacToe = Path("res/images/aboutScreen/tres-en-raya.png")
        
        # Imagenes del GameScreen
        self.symbol_x = Path("res/images/gameScreen/borrar.png")
        self.symbol_o = Path("res/images/gameScreen/circle.png")
        self.home_icon = Path("res/images/gameScreen/home.png")
        
        # Imagenes del RuleScreen
        self.derrota = Path("res/images/ruleScreen/derrota.png")
        self.empate = Path("res/images/ruleScreen/empate.png")
        self.victoria = Path("res/images/ruleScreen/victoria.png")

        self.backgroundImage = Path("res/images/background_main_screen.jpg")
        self.ticTacToeLogo = Path("res/images/tic-tac-toe-logo-v2.png")
        self.userHumanLogo = Path("res/images/user-human.png")
        self.userAgentAi = Path("res/images/user-artificial-inteligence.png")
        
    def surface_image(self, image, image_width, image_height) -> pygame.Surface:
        surface_image = pygame.image.load(image)
        surface_image = pygame.transform.smoothscale(surface_image, (image_width, image_height))
        return surface_image

    def rect_image(self, image, image_width, image_height, left, top) -> pygame.Rect:
        surface_image = self.surface_image(image, image_width, image_height)        
        rect = surface_image.get_rect()
        rect.left = left
        rect.top = top
        return rect
    
    def draw(self, image, image_width, image_height, left, top, surface: pygame.Surface):
        surface_image = self.surface_image(
            image = image, image_width = image_width, image_height = image_height 
        )
        rect_image = self.rect_image(
            image = image, image_width = image_width, image_height = image_height , 
            left = left, top = top
        )
    #    print(f"[INFO] - Surface: {surface_image} - Rect: {rect_image}") 
        surface.blit(surface_image, rect_image)
        pygame.display.flip()