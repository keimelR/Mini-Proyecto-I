import pygame

from model.Text import Text, TypeFont
from model.Images import Images
from model.Colors import Colors
from model.Button import Boton
from model.IconButton import IconButton

from model.ScoreCard import ScoreCard
# from util.Scenes import scenes, current_scene

class HomeScreen:
    def __init__(self, scenes):
        self.WIDTH = 1080
        self.HEIGHT = 720
        self.running = False
        self.text = Text()
        self.images = Images()
        self.colors = Colors()
        self.display = None
        self.scenes = scenes
        
    def go_to(self, scene_name):
        print(f"Accediendo a {scene_name}")
        # Indica la escena destino y sale del loop para ceder el control
        self.scenes["current"] = scene_name
        self.running = False
        
    def on_init(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.running = True
        # Compartimos la ventana con otras escenas
        self.scenes["display"] = self.display
        
    def on_execute(self):
        self.on_init()
        
        # Cargar la Imagen de Logo
        self.images.draw(self.images.logo, 30, 30, self.WIDTH // 2, self.HEIGHT // 6, self.display)
        image = pygame.image.load(self.images.logo)
        imageRect = image.get_rect()
        imageRect.center = (self.WIDTH // 2, self.HEIGHT // 6)
        
        # Cargar el Texto de Tic- Tac- Toe
        textHeader = self.text.role(TypeFont.DISPLAY, "Tic- Tac- Toe", (0, 173, 181))
        rectHeader = textHeader.get_rect()
        rectHeader.center = (self.WIDTH // 2, 210)

        # Iconos Buttons
        iniciarJuegoIconButton = IconButton(
            text_button = "Jugar con la AI", text_color = (57, 62, 70), left = self.WIDTH // 2, top = (self.HEIGHT * 0.5),
            button_width = 130, button_height = 30, button_color = (238, 238, 238), button_shadow_color = (8, 217, 214), button_shadow_height = 5,
            icon = self.images.robot, icon_width = 25, icon_height = 25, display = self.display,
            accion=lambda: self.go_to("game_screen")
        )
        
        reglas_juego_icon_button = IconButton(
            text_button = "Reglas del Juego", text_color = (57, 62, 70), left = self.WIDTH // 2, top = (self.HEIGHT * 0.75),
            button_width = 120, button_height = 30, button_color = (238, 238, 238), button_shadow_color = (8, 217, 214), button_shadow_height = 5,
            icon = self.images.libro, icon_width = 25, icon_height = 25, display = self.display,
            accion=lambda: self.go_to("rule_screen")
        )
        
        acercaDeIconButton = IconButton(
            text_button = "Acerca De", text_color = (57, 62, 70), left = self.WIDTH // 2, top = (self.HEIGHT * 0.85),
            button_width = 210, button_height = 30, button_color = (238, 238, 238), button_shadow_color = (8, 217, 214), button_shadow_height = 5,
            icon = self.images.iconAcercaDe, icon_width = 25, icon_height = 25, display = self.display,
            accion=lambda: self.go_to("about_screen")
        )
        while(self.running):
            for event in pygame.event.get():
                self.on_event(event)
                acercaDeIconButton.handle_event(event)
                reglas_juego_icon_button.handle_event(event)
                iniciarJuegoIconButton.handle_event(event)
                
            self.display.fill(self.colors.bkg)
            self.display.blit(image, imageRect)
            self.display.blit(textHeader, rectHeader)
            
            iniciarJuegoIconButton.draw_icon_button()
            reglas_juego_icon_button.draw_icon_button()
            acercaDeIconButton.draw_icon_button()
        
            pygame.display.flip()
            
        
    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            # Señalamos al bucle principal que debe terminar
            self.running = False
            if isinstance(self.scenes, dict):
                self.scenes["running"] = False
            # Opcional: limpiar recursos
            print("Haz presionado en Destroy")
        
    def destroy(self):
        print("Destroy llamado")
        # No devolver nada; el control de cierre lo maneja scenes['running']
        return None

    