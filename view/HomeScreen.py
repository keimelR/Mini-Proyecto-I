import os
import pygame
from model.Text import Text, TypeFont
from model.Images import Images
from model.Colors import Colors
from model.Button import Boton
from model.IconButton import IconButton
from model.ScoreCard import ScoreCard

# --- IMPORTACIONES PARA EL MODELO ---
from qlearning import TicTacToeBot, Entrenamiento
from view.TrainingForm import TrainingForm

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

        self.entrenamiento = Entrenamiento()
        
        # --- ATRIBUTOS DEL BOT Y FORMULARIO ---
        self.bot_q = TicTacToeBot()
        self.training_form = None

    def go_to(self, scene_name):
        print(f"Accediendo a {scene_name}")
        # Si vamos a jugar, inyectamos el bot configurado en la GameScreen
        if scene_name == "game_screen":
            self.scenes["game_screen"].bot = self.bot_q
            
        self.scenes["current"] = scene_name
        self.running = False
        
    def on_init(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.running = True
        self.scenes["display"] = self.display
        
        if os.path.exists("q_table.json"):
            self.entrenamiento.cargar_archivo(self.bot_q)
            self.bot_q.epsilon = 0
            print("Archivo q_table.json cargado")

        # Inicializamos el formulario de entrenamiento
        # Usamos una fuente estándar de Pygame para el formulario
        fuente_form = pygame.font.SysFont("Arial", 22)
        self.training_form = TrainingForm(self.display, self.bot_q, fuente_form)
        
    def abrir_configuracion(self):
        if self.training_form:
            self.training_form.is_open = True


    def on_execute(self):
        self.on_init()
        clock = pygame.time.Clock()

        # Cargar la Imagen de Logo
        image = pygame.image.load(self.images.logo)
        imageRect = image.get_rect()
        imageRect.center = (self.WIDTH // 2, self.HEIGHT // 6)
        
        # Cargar el Texto de Tic- Tac- Toe
        textHeader = self.text.role(TypeFont.DISPLAY, "Tic- Tac- Toe", (0, 173, 181))
        rectHeader = textHeader.get_rect()
        rectHeader.center = (self.WIDTH // 2, 210)

        # Iconos Buttons
        iniciarJuegoIconButton = IconButton(
            text_button = "Jugar con la AI", text_color = (57, 62, 70), left = self.WIDTH // 2, top = (self.HEIGHT * 0.45),
            button_width = 130, button_height = 30, button_color = (238, 238, 238), button_shadow_color = (8, 217, 214), button_shadow_height = 5,
            icon = self.images.robot, icon_width = 25, icon_height = 25, display = self.display,
            accion=lambda: self.go_to("game_screen")
        )

        # --- BOTÓN NUEVO: AJUSTAR MODELO ---
        ajustarModeloIconButton = IconButton(
            text_button = "Ajustar Parámetros IA", text_color = (57, 62, 70), left = self.WIDTH // 2, top = (self.HEIGHT * 0.58),
            button_width = 180, button_height = 30, button_color = (238, 238, 238), button_shadow_color = (131, 150, 126), button_shadow_height = 5,
            icon = self.images.robot, icon_width = 25, icon_height = 25, display = self.display,
            accion=self.abrir_configuracion
        )
        
        reglas_juego_icon_button = IconButton(
            text_button = "Reglas del Juego", text_color = (57, 62, 70), left = self.WIDTH // 2, top = (self.HEIGHT * 0.72),
            button_width = 120, button_height = 30, button_color = (238, 238, 238), button_shadow_color = (8, 217, 214), button_shadow_height = 5,
            icon = self.images.libro, icon_width = 25, icon_height = 25, display = self.display,
            accion=lambda: self.go_to("rule_screen")
        )
        
        acercaDeIconButton = IconButton(
            text_button = "Acerca De", text_color = (57, 62, 70), left = self.WIDTH // 2, top = (self.HEIGHT * 0.84),
            button_width = 210, button_height = 30, button_color = (238, 238, 238), button_shadow_color = (8, 217, 214), button_shadow_height = 5,
            icon = self.images.iconAcercaDe, icon_width = 25, icon_height = 25, display = self.display,
            accion=lambda: self.go_to("about_screen")
        )

        while(self.running):
            clock.tick(60)
            for event in pygame.event.get():
                # Si el formulario está abierto, captura los eventos exclusivamente
                if self.training_form and self.training_form.is_open:
                    self.training_form.handle_event(event)
                else:
                    self.on_event(event)
                    # Solo manejamos botones si el modal está cerrado
                    acercaDeIconButton.handle_event(event)
                    reglas_juego_icon_button.handle_event(event)
                    iniciarJuegoIconButton.handle_event(event)
                    ajustarModeloIconButton.handle_event(event)
                
            # --- DIBUJADO ---
            self.display.fill(self.colors.bkg)
            self.display.blit(image, imageRect)
            self.display.blit(textHeader, rectHeader)
            
            iniciarJuegoIconButton.draw_icon_button()
            ajustarModeloIconButton.draw_icon_button() # Nuevo botón
            reglas_juego_icon_button.draw_icon_button()
            acercaDeIconButton.draw_icon_button()

            # Dibujar el formulario (siempre al final para que quede encima)
            if self.training_form:
                self.training_form.draw()
        
            pygame.display.flip()
            
    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.running = False
            if isinstance(self.scenes, dict):
                self.scenes["running"] = False
        
    def destroy(self):
        print("Destroy llamado")
        return None