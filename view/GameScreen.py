import pygame

from model.Text import Text, TypeFont
from model.Images import Images
from model.Colors import Colors
from model.Button import Boton
from model.IconButton import IconButton
from model.ScoreCard import ScoreCard

from model.Board import Board

class GameScreen:
    def __init__(self, scenes):
        self.scenes = scenes
        self.text = Text()
        self.images = Images()
        self.colors = Colors()
        self.display = pygame.display.set_mode((1080, 720))
        self.running = False
        self.board = Board(140, 240, 120, 10, self.display)
        
    def draw(self, display: pygame.Surface):
        score_card_user = ScoreCard(
            text_card="YOU: ", text_score="0", text_color=(255, 255, 255), left=140, top=90, 
            card_width= 260, card_height=100, card_color=(104, 116, 133), 
            image=self.images.symbol_x, image_width=30, image_height=30, 
            display=display
        )
        
        score_card_bot = ScoreCard(
            text_card="BOT: ", text_score="0", text_color=(255, 255, 255), left=680, top=90, 
            card_width= 260, card_height=100, card_color=(104, 116, 133), 
            image=self.images.symbol_o, image_width=30, image_height=30, 
            display=display
        )

        score_card_user.draw_score_card()
        score_card_bot.draw_score_card()
        self.board.draw()
    
    def on_execute(self):
        print("Accediendo al GameScreen")
        """
        self.display = self.scenes.get("display")
        if self.display is None:
            
            print("Sin Display Iniciado")
            pygame.init()
            self.display = pygame.display.set_mode((1080, 720))
        """
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    if isinstance(self.scenes, dict):
                        self.scenes["running"] = False
                # Delegamos el manejo del evento al botón de regresar
             #   regresarHomeIconButton.handle_event(event)
            self.display.fill(self.colors.bkg)

            # Dibujar la escena usando el mismo método draw
            self.draw(self.display)
            pygame.display.flip()