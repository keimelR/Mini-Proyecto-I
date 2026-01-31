import time
import pygame

from model.Text import Text, TypeFont
from model.Images import Images
from model.Colors import Colors
from model.Button import Boton
from model.IconButton import IconButton
from model.ScoreCard import ScoreCard

from model.Board import Board
from model.Player import Player
from constantes import *
from qlearning import TicTacToeBot, Entrenamiento

class GameScreen:
    def __init__(self, scenes):
        self.scenes = scenes
        self.text = Text()
        self.images = Images()
        self.colors = Colors()
        self.display = pygame.display.set_mode((1080, 720))
        self.running = False

        self.bot = TicTacToeBot()
        self.entrenamiento = Entrenamiento()
        
        self.board = Board(345, 260, 120, 10, self.display)
        self.player_user = Player(self.images.symbol_x)
        self.player_bot = Player(self.images.symbol_o)
        self.turn = PLAYER
        self.turno_n = 0
        self.boardState = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.number_win_user = 0
        self.number_win_bot = 0
        self.existWinner = 0

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
        
        text_turn = self.text_turn()
        text_result = self.text_result()
  
        score_card_user = ScoreCard(
            text_card="YOU: ", text_score=str(self.number_win_user), text_color=(255, 255, 255), left=140, top=90, 
            card_width= 260, card_height=100, card_color=(104, 116, 133), 
            image=self.images.symbol_x, image_width=30, image_height=30, 
            display=self.display
        )
        
        score_card_bot = ScoreCard(
            text_card="BOT: ", text_score=str(self.number_win_bot), text_color=(255, 255, 255), left=680, top=90, 
            card_width= 260, card_height=100, card_color=(104, 116, 133), 
            image=self.images.symbol_o, image_width=30, image_height=30, 
            display=self.display
        )
        
        # Dibuja en Pantalla el Turno y el Resultado del Juego
        self.text.draw(TypeFont.HEADLINE, text_turn, (238, 238, 238), 115, 440, self.display)
        self.text.draw(TypeFont.HEADLINE, text_result, (238, 238, 238), 170, 440, self.display)

        # Dibuja en Pantalla los ScoreCard
        score_card_user.draw_score_card()
        score_card_bot.draw_score_card()

    
    def on_execute(self):  
        # IconButton para Regresar a HomeScreen
        icon_button_home = IconButton(
            text_button = "", text_color = (57, 62, 70), left = 25, 
            top = 28, button_width = 50, button_height = 30, 
            button_color = (255, 46, 99), button_shadow_color = self.colors.bkg, button_shadow_height = 5,
            icon = self.images.home_icon, icon_width = 25, icon_height = 25, display = self.display,
            accion=lambda: self.go_to("home_screen")
        )
        
        # IconButton para Reiniciar la Partida
        icon_button_reset_game = IconButton(
            text_button = "Reiniciar Juego", text_color = (57, 62, 70), left = 900, 
            top = 500, button_width = 100, button_height = 30, 
            button_color = (255, 46, 99), button_shadow_color = self.colors.bkg, button_shadow_height = 5,
            icon = self.images.iconRegresar, icon_width = 25, icon_height = 25, display = self.display,
            accion=lambda: self.reset()
        )
        
        self.running = True
        
        self.display.fill(self.colors.bkg)
        
        # Dibujamos los IconButtons
        icon_button_home.draw_icon_button()
        icon_button_reset_game.draw_icon_button()

        # Dibujamos el Tablero
        self.board.draw()

        self.entrenamiento.entrenar_bot(self.bot, 20000)

        while self.running:
            # Manejamos los eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    if isinstance(self.scenes, dict):
                        self.scenes["running"] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Obtenemos la casilla
                    grid = self.board.on_event(event)
                    if grid != None and not self.has_winner():
                        # Hacemos la Jugada
                        self.player_turn(grid)
                        
                        # Actualizamos el Puntaje
                        status_partida = self.update_score()
                        
                        # Cubrimos los Textos Generados del Turno y Ganador de la Partida
                        self.cover_text(pygame.Rect(430, 95, 220, 50))
                        self.cover_text(pygame.Rect(430, 170, 220, 50))

                        if status_partida == EN_PARTIDA:
                            self.bot_turn()
                                
                            # Actualizamos el Puntaje
                            self.update_score()
                            
                            # Cubrimos los Textos Generados del Turno y Ganador de la Partida
                            self.cover_text(pygame.Rect(430, 95, 220, 50))
                            self.cover_text(pygame.Rect(430, 170, 220, 50))

                # Manejamos los eventos en los IconButtons
                icon_button_home.handle_event(event)
                icon_button_reset_game.handle_event(event)
                
            self.draw()
            pygame.display.flip()
    
    def cover_text(self, rect: pygame.Rect):
        """
        Ocultar/Cubrir el Texto con el Color de Fondo
        
        :param rect: Area Rectangular donde se Cubrira Texto
        :type rect: pygame.Rect
        """
        pygame.draw.rect(self.display, self.colors.bkg, rect)
            
    def text_turn(self) -> str:
        """
        Genera un Mensaje Descriptivo Indicando qué Entidad tiene el Control del Turno Actual en el Juego.
        
        :return: Un Mensaje segun el Turno 
        :rtype: str
        """
        text_turn = ""
        if self.turn == PLAYER:
            text_turn = "Es tu Turno!"
        else:
            text_turn = "Bot Jugando!"
        return text_turn
    
    def text_result(self) -> str:
        """
        Genera un Mensaje Descriptivo Indicando el Ganador/Perdedor o Empate en el Juego.
        
        :return: Un Mensaje segun el Ganador 
        :rtype: str
        """
        text_result = ""
        winner = self.has_winner()
        if winner:
            if self.turn == PLAYER:
                text_result = "HAZ GANADO!"
            if self.turn == IA:
                text_result = "HAZ PERDIDO!"
        elif self.turno_n == 9:
            text_result = "EMPATE!"
        return text_result
            
    def update_score(self):
        winner = self.has_winner()
        if winner:
            if self.turn == PLAYER:
                self.number_win_user = self.number_win_user + 1
                self.existWinner = PLAYER
                return VICTORIA
            if self.turn == IA:
                self.number_win_bot = self.number_win_bot + 1
                self.existWinner = IA
                return DERROTA

        if 0 not in self.boardState:
            return EMPATE
        
        return EN_PARTIDA
            
    def reset(self):
        self.turn = PLAYER
        self.boardState = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.turno_n = 0   
        self.existWinner = 0
        
        self.cover_text(pygame.Rect(430, 95, 220, 50))  
        self.cover_text(pygame.Rect(430, 170, 220, 50))

        self.board.reset()
        self.board.draw()      
    
    def player_turn(self, grid):
        symbol_current = self.player_user.image_symbol
                        
        self.board.append_movement(grid, symbol_current)
        self.board.draw_movement(grid, symbol_current)  
        self.boardState[grid] = self.turn
        
        if not self.has_winner():      
            self.turn = IA
            self.turno_n = self.turno_n + 1

            
    def bot_turn(self):
        time.sleep(2) # Simulacion de pensamiento

        jugada = self.bot.jugada_bot(self.boardState)

        self.board.append_movement(jugada, self.player_bot.image_symbol)
        self.board.draw_movement(jugada, self.player_bot.image_symbol)  
        self.boardState[jugada] = self.turn
        
        if not self.has_winner():      
            self.turn = PLAYER
            self.turno_n = self.turno_n + 1

    
    def has_winner(self) -> bool:
        return self.winDiagonalLeft() or self.winDiagonalRight() or self.winHorizontal() or self.winVertical()
    
    def winHorizontal(self) -> bool:
        return (self.boardState[0] == self.turn and self.boardState[1] == self.turn and self.boardState[2] == self.turn) or (self.boardState[3] == self.turn and self.boardState[4] == self.turn and self.boardState[5] == self.turn) or (self.boardState[6] == self.turn and self.boardState[7] == self.turn and self.boardState[8] == self.turn)
    
    def winVertical(self) -> bool:
        return (self.boardState[0] == self.turn and self.boardState[3] == self.turn and self.boardState[6] == self.turn) or (self.boardState[1] == self.turn and self.boardState[4] == self.turn and self.boardState[7] == self.turn) or (self.boardState[2] == self.turn and self.boardState[5] == self.turn and self.boardState[8] == self.turn)

    def winDiagonalLeft(self) -> bool:
        return (self.boardState[0] == self.turn and self.boardState[4] == self.turn and self.boardState[8] == self.turn)
    
    def winDiagonalRight(self) -> bool:
        return (self.boardState[2] == self.turn and self.boardState[4] == self.turn and self.boardState[6] == self.turn)