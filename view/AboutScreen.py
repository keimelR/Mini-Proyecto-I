import pygame

from model.Text import Text, TypeFont
from model.Images import Images
from model.Colors import Colors
from model.Button import Boton
from model.IconButton import IconButton

from view.HomeScreen import HomeScreen
# from util.Scenes import scenes

class AboutScreen:
    def __init__(self, scenes):
        self.scenes = scenes
        self.text = Text()
        self.images = Images()
        self.colors = Colors()
        self.display = None
        self.running = False


    def handle_events(self, events):
        pass
    
    def draw(self, screen, regresar_button=None):
        # Icon Button para Regresar al Inicio
        if regresar_button is None:
            regresarHomeIconButton = IconButton(
                text_button = "", text_color = (57, 62, 70), left = 25, 
                top = 28, button_width = 50, button_height = 30, 
                button_color = (255, 46, 99), button_shadow_color = self.colors.bkg, button_shadow_height = 5,
                icon = self.images.iconRegresar, icon_width = 25, icon_height = 25, display = screen,
                accion=lambda: self.go_to("home_screen")
            )
        else:
            regresarHomeIconButton = regresar_button
        # Titulo de "Acerca del Juego"
        textAcercaDelJuego = self.text.role(TypeFont.HEADLINE, "Acerca del Juego", (238, 238, 238))
        rectAcercaDelJuego = textAcercaDelJuego.get_rect()
        rectAcercaDelJuego.top = 80
        rectAcercaDelJuego.left = 10

        # Texto Correspondiente al Titulo de "Acerca del Juego"
        texto_completo_juego = "El Tic-Tac-Toe es un juego clásico de estrategia por turnos,\n" + "diseñado para dos jugadores, que se desarrolla en un tablero de 3 x 3.\n" + "Cada participante posee una marca única (tradicionalmente X u O),\n" + "y el objetivo principal es ser el primero en colocar tres de sus marcas,\n" + "de forma consecutiva de manera horizontal, vertical o diagonal."
        
        # Inagen oara el "Acerca del Juego"
        surfaceImageTicTacToe = pygame.image.load(self.images.imageTicTacToe)
        surfaceImageTicTacToe = pygame.transform.smoothscale(surfaceImageTicTacToe, (100, 100))
        rectImageTicTacToe = surfaceImageTicTacToe.get_rect()
        rectImageTicTacToe.left = 850
        rectImageTicTacToe.top = 120
        texto_completo_desarrolladores = ""
        
        # Titulo de "Acerca de los Desarrolladores"
        textAcercaDesarrollador = self.text.role(TypeFont.HEADLINE, "Acerca de los Desarrolladores", (238, 238, 238))
        rectAcercaDesarrollador = textAcercaDesarrollador.get_rect()
        rectAcercaDesarrollador.top = 240
        rectAcercaDesarrollador.left = 10
        
        textoCompletoAcercaDesarrollador = "Bello, muy amable, es aceptable, inalcanzable, razonable, incuestionable, Re impactante, agradable,\nimpresionante, alucinante, inquebrantable, desafiante al cobrarte y embargarte por que soy emprendedor,\nes lo que soy. Guapo, poderoso, asombroso, muy hermoso, soy precioso, armonioso, Un buen socio, misterioso,\nbuena gente, detergente, muy majete, inteligente, nada ojete, irreverente, un exponente muy perfecto\nes lo que...Bello, muy amable, es aceptable, inalcanzable, razonable, incuestionable, inquebrantable,\nagradable, impresionante, alucinante, inquebrantable, desafiante al cobrarte y embargarte\npor que soy emprendedor, es lo que soy"
        
        
        screen.fill(self.colors.bkg)

        # Dibujamos el Icon Button
        regresarHomeIconButton.draw_icon_button()

        # Dibujamos la Primera Seccion Correspondiente al Juego
        screen.blit(textAcercaDelJuego, rectAcercaDelJuego)   # Dibujamos el Titulo
        self.dibujar_parrafos(screen, texto_completo_juego, 120)                 # Dibujamos el contenido
        screen.blit(surfaceImageTicTacToe, rectImageTicTacToe)

        # Dibujamos la Segunda Seccion
        screen.blit(textAcercaDesarrollador, rectAcercaDesarrollador)
        self.dibujar_parrafos(screen, textoCompletoAcercaDesarrollador, 280)
            
        pygame.display.flip()

    def go_to(self, scene_name):
        self.scenes["current"] = scene_name
        self.running = False

    def on_execute(self):
        # Obtener la ventana compartida
        self.display = self.scenes.get("display")
        if self.display is None:
            # Si no existe, inicializamos una propia
            pygame.init()
            self.display = pygame.display.set_mode((1080, 720))

        self.running = True

        # Creamos el boton de regresar para poder reutilizarlo en manejo de eventos y dibujado
        regresarHomeIconButton = IconButton(
            text_button = "", text_color = (57, 62, 70), left = 25, 
            top = 28, button_width = 50, button_height = 30, 
            button_color = (255, 46, 99), button_shadow_color = self.colors.bkg, button_shadow_height = 5,
            icon = self.images.iconRegresar, icon_width = 25, icon_height = 25, display = self.display,
            accion=lambda: self.go_to("home_screen")
        )

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    if isinstance(self.scenes, dict):
                        self.scenes["running"] = False
                # Delegamos el manejo del evento al botón de regresar
                regresarHomeIconButton.handle_event(event)

            # Dibujar la escena usando el mismo método draw
            self.draw(self.display, regresar_button=regresarHomeIconButton)

    def dibujar_parrafos(self, screen, texto_completo: str, top):
        lineas = texto_completo.splitlines()
        for linea in lineas:
            surfaceLinea = self.text.role(TypeFont.TITTLE_MEDIUM, linea, (238, 238, 238))
            
            rectLinea = surfaceLinea.get_rect()
            rectLinea.top = top
            rectLinea.left = 10
            screen.blit(surfaceLinea, rectLinea)
            
            top = top + 20 

    """
    def on_init(self):
        pygame.init()
    #    self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.running = True
        
    def on_execute(self):
        self.on_init()
        
        # Icon Button para Regresar al Inicio
        regresarHomeIconButton = IconButton(
            text_button = "", text_color = (57, 62, 70), left = 25, 
            top = 28, button_width = 50, button_height = 30, 
            button_color = (255, 46, 99), button_shadow_color = self.colors.bkg, button_shadow_height = 5,
            icon = self.images.iconRegresar, icon_width = 25, icon_height = 25, display = self.display,
            accion=HomeScreen().on_execute
        )
        
        # Titulo de "Acerca del Juego"
        textAcercaDelJuego = self.text.role(TypeFont.HEADLINE, "Acerca del Juego", (238, 238, 238))
        rectAcercaDelJuego = textAcercaDelJuego.get_rect()
        rectAcercaDelJuego.top = 80
        rectAcercaDelJuego.left = 10

        # Texto Correspondiente al Titulo de "Acerca del Juego"
        texto_completo_juego = "El Tic-Tac-Toe es un juego clásico de estrategia por turnos,\n" + "diseñado para dos jugadores, que se desarrolla en un tablero de 3 x 3.\n" + "Cada participante posee una marca única (tradicionalmente X u O),\n" + "y el objetivo principal es ser el primero en colocar tres de sus marcas,\n" + "de forma consecutiva de manera horizontal, vertical o diagonal."
        
        # Inagen oara el "Acerca del Juego"
        surfaceImageTicTacToe = pygame.image.load(self.images.imageTicTacToe)
        surfaceImageTicTacToe = pygame.transform.smoothscale(surfaceImageTicTacToe, (100, 100))
        rectImageTicTacToe = surfaceImageTicTacToe.get_rect()
        rectImageTicTacToe.left = 850
        rectImageTicTacToe.top = 120
        texto_completo_desarrolladores = ""
        
        # Titulo de "Acerca de los Desarrolladores"
        textAcercaDesarrollador = self.text.role(TypeFont.HEADLINE, "Acerca de los Desarrolladores", (238, 238, 238))
        rectAcercaDesarrollador = textAcercaDesarrollador.get_rect()
        rectAcercaDesarrollador.top = 240
        rectAcercaDesarrollador.left = 10
        
        textoCompletoAcercaDesarrollador = "Bello, muy amable, es aceptable, inalcanzable, razonable, incuestionable, Re impactante, agradable,\nimpresionante, alucinante, inquebrantable, desafiante al cobrarte y embargarte por que soy emprendedor,\nes lo que soy. Guapo, poderoso, asombroso, muy hermoso, soy precioso, armonioso, Un buen socio, misterioso,\nbuena gente, detergente, muy majete, inteligente, nada ojete, irreverente, un exponente muy perfecto\nes lo que...Bello, muy amable, es aceptable, inalcanzable, razonable, incuestionable, inquebrantable,\nagradable, impresionante, alucinante, inquebrantable, desafiante al cobrarte y embargarte\npor que soy emprendedor, es lo que soy"
        
        
        while(self.running):
            for event in pygame.event.get():
                self.on_event(event)
            
            self.display.fill(self.colors.bkg)
            
            # Dibujamos el Icon Button
            regresarHomeIconButton.draw_icon_button()

            # Dibujamos la Primera Seccion Correspondiente al Juego
            self.display.blit(textAcercaDelJuego, rectAcercaDelJuego)   # Dibujamos el Titulo
            self.dibujar_parrafos(texto_completo_juego, 120)                 # Dibujamos el contenido
            self.display.blit(surfaceImageTicTacToe, rectImageTicTacToe)

            # Dibujamos la Segunda Seccion
            self.display.blit(textAcercaDesarrollador, rectAcercaDesarrollador)
            self.dibujar_parrafos(textoCompletoAcercaDesarrollador, 280)
            
            pygame.display.flip()

    def dibujar_parrafos(self, texto_completo: str, top):
        lineas = texto_completo.splitlines()
        for linea in lineas:
            surfaceLinea = self.text.role(TypeFont.TITTLE_MEDIUM, linea, (238, 238, 238))
            
            rectLinea = surfaceLinea.get_rect()
            rectLinea.top = top
            rectLinea.left = 10
            self.display.blit(surfaceLinea, rectLinea)
            
            top = top + 20

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.running = False
   """     