import pygame

from model.Text import Text, TypeFont
from model.Images import Images
from model.Colors import Colors
from model.IconButton import IconButton

class RuleScreen:
    def __init__(self, scenes):
        self.scenes = scenes
        self.text = Text()
        self.images = Images()
        self.colors = Colors()
        self.display = pygame.display.set_mode((1080, 720))
        self.running = False
        
    def go_to(self, scene_name):
        """
        Permite Dirigirse a la Screen Solicitado como Parametro
        
        :param scene_name: Nombre de la Screen
        """
        self.scenes["current"] = scene_name
        self.running = False

    def draw(self):
        """
        Dibuja en Pantalla los Elementos Estaticos
        """
        self.text.draw(TypeFont.DISPLAY, "Reglas del Juego", (238, 238, 238), 20, 50, self.display)
        
        self.text.draw(TypeFont.HEADLINE, "Victoria", (238,238,238), 90, 20, self.display)
        text_win = "La condición de victoria se\n cumple en el momento exacto,\n en que logras conectar tres\n fichas consecutivas en cualquier\n dirección: horizontal, vertical\n o diagonal. El éxito depende\n de ocupar los espacios clave,\n antes que el rival, obligándolo\n a elegir entre defenderse o\n intentar su propia línea,\n hasta que consigues cerrar tu\n formación de tres."
        self.dibujar_parrafos(self.display, text_win, 130, 20)
        pygame.draw.rect(self.display, (255, 46, 99), pygame.Rect(370, 130, 2, 300))
        self.images.draw(self.images.victoria, 150, 150, 100, 450, self.display)
        
        self.text.draw(TypeFont.HEADLINE, "Derrota", (238,238,238), 90, 390, self.display)
        text_loss = "La derrota ocurre cuando el\n oponente completa su hilera,\n de tres fichas antes que tú.\n Esto sucede generalmente,\n porque el otro jugador logró\n anticiparse a tus movimientos,\n o porque dejaste un espacio\n crítico sin bloquear,\n permitiéndole conectar sus\n marcas de forma ininterrumpida\n y finalizar la partida a su\n favor."
        self.dibujar_parrafos(self.display, text_loss, 130, 390)
        pygame.draw.rect(self.display, (255, 46, 99), pygame.Rect(730, 130, 2, 300))
        self.images.draw(self.images.derrota, 150, 150, 460, 450, self.display)

        self.text.draw(TypeFont.HEADLINE, "Empate", (238,238,238), 90, 750, self.display)
        text_draw = "El empate, conocido como\n 'tablas', se produce cuando\n se han ocupado las nueve\n casillas del tablero, y ninguno\n de los jugadores ha conseguido\n alinear tres fichas. Es el\n resultado de un juego\n defensivo recíproco, donde\n cada intento de ataque fue\n neutralizado, dejando el\n tablero bloqueado y sin un\n ganador definido."
        self.dibujar_parrafos(self.display, text_draw, 130, 750)
        self.images.draw(self.images.empate, 150, 150, 840, 450, self.display)
        
        pygame.display.flip()


    def on_execute(self):
        pygame.init()
        self.running = True
 
        # Creamos el boton de regresar para poder reutilizarlo en manejo de eventos y dibujado
        regresarHomeIconButton = IconButton(
            text_button = "", text_color = (57, 62, 70), left = 25, 
            top = 28, button_width = 50, button_height = 30, 
            button_color = (255, 46, 99), button_shadow_color = self.colors.bkg, button_shadow_height = 5,
            icon = self.images.home_icon, icon_width = 25, icon_height = 25, display = self.display,
            accion=lambda: self.go_to("home_screen")
        )
        
        self.display.fill(self.colors.bkg)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    if isinstance(self.scenes, dict):
                        self.scenes["running"] = False

                regresarHomeIconButton.handle_event(event)
            
            self.draw()
            regresarHomeIconButton.draw_icon_button()
            
                
    def dibujar_parrafos(self, screen, texto_completo: str, top, left):
        """
        Divide e Imprime en Pantalla Grandes Extensiones de Texto para evitar que Salgan de la Pantalla
        
        :param screen: Superficie donde se dibujara el texto
        :param texto_completo: Texto
        :param top: Punto Superior desde donde Comenzara a Dibujar el Parrafo
        :param left: Punto Izquierdo desde donde Comenzara a Dibujar el Parrafo 
        """
        lineas = texto_completo.splitlines()
        for linea in lineas:
            surfaceLinea = self.text.role(TypeFont.TITTLE_MEDIUM, linea, (238, 238, 238))
            
            rectLinea = surfaceLinea.get_rect()
            rectLinea.top = top
            rectLinea.left = left
            screen.blit(surfaceLinea, rectLinea)
            
            top = top + 20 