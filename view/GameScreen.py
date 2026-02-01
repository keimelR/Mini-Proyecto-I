import math
import time
import pygame
import matplotlib.pyplot as plt
import numpy as np

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
from minimax import mejor_movimiento_IA

class GameScreen:
    def __init__(self, scenes):
        self.scenes = scenes
        self.text = Text()
        self.images = Images()
        self.colors = Colors()
        self.display = pygame.display.set_mode((1080, 720))
        self.running = False

        self.initial_turn = IA

        if not hasattr(self, 'bot') or self.bot is None:
            self.bot = TicTacToeBot()

        self.board = Board(345, 260, 120, 10, self.display)
        self.player_user = Player(self.images.symbol_x)
        self.player_bot = Player(self.images.symbol_o)
        self.turn = IA
        self.turno_n = 0
        self.boardState = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.number_win_user = 0
        self.number_win_bot = 0
        self.existWinner = 0

        # --- Variables para la animación de carga ---
        self.bot_thinking = False
        self.think_start_time = 0
        self.think_duration = 2000  # 2 segundos en milisegundos

        self.btn_heatmap = pygame.Rect(1080 - 210, 20, 200, 50)

        # En __init__
        self.history_states = []

    def draw_loading_animation(self):
        """Dibuja un arco giratorio que indica que el bot está procesando"""
        center_x, center_y = 200, 540 # Posición arriba del tablero
        rect = pygame.Rect(center_x - 25, center_y - 25, 55, 55)
        pygame.draw.rect(self.display, self.colors.bkg, rect)

        
        # El ángulo depende del tiempo actual para crear rotación constante
        angle = (pygame.time.get_ticks() / 3) % 360
        
        start_angle = math.radians(angle)
        end_angle = math.radians(angle + 280) # Un arco de 280 grados
        rect2 = pygame.Rect(center_x - 25, center_y - 25, 50, 50)
        
        # Dibujamos el arco de carga
        pygame.draw.arc(self.display, (255, 46, 99), rect2, start_angle, end_angle, 5)
        
        # Texto de estado debajo del arco
        self.text.draw(TypeFont.HEADLINE, "PENSANDO...", (238, 238, 238), center_y - 60, center_x - 65, self.display)

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

        pygame.draw.rect(self.display, (0, 173, 181), self.btn_heatmap, border_radius=8)
    # Usamos tu objeto self.text para mantener la consistencia
        self.text.draw(TypeFont.HEADLINE, "VER HEATMAP", (255, 255, 255), 32, 1080 - 200, self.display)

    
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


        if self.turn == IA:
            self.bot_thinking = True
            self.think_start_time = pygame.time.get_ticks()

        while self.running:
            current_time = pygame.time.get_ticks()

            if self.bot_thinking and (current_time - self.think_start_time >= self.think_duration):
                self.execute_bot_move()

            # Manejamos los eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    if isinstance(self.scenes, dict):
                        self.scenes["running"] = False
                # Bloqueamos la interacción del usuario mientras el bot piensa
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_heatmap.collidepoint(event.pos) and not self.bot_thinking:
                        self.mostrar_heatmap()
                        continue

                    if not self.bot_thinking:
                        grid = self.board.on_event(event)
                        if grid != None and not self.has_winner():
                            self.player_turn(grid)
                            status_partida = self.update_score()
                            
                            # Limpiar áreas de texto
                            self.cover_text(pygame.Rect(430, 95, 220, 50))
                            self.cover_text(pygame.Rect(430, 170, 220, 50))

                            if status_partida == EN_PARTIDA:
                                # Iniciamos el "tiempo de pensamiento"
                                self.bot_thinking = True
                                self.think_start_time = pygame.time.get_ticks()
                            

                # Manejamos los eventos en los IconButtons
                icon_button_home.handle_event(event)
                icon_button_reset_game.handle_event(event)
                
            
            if self.bot_thinking:
                self.draw_loading_animation()
            self.draw()
            pygame.display.flip()
    
    def cover_text(self, rect: pygame.Rect):
        """
        Ocultar/Cubrir el Texto con el Color de Fondo
        
        :param rect: Area Rectangular donde se Cubrira Texto
        :type rect: pygame.Rect
        """
        pygame.draw.rect(self.display, self.colors.bkg, rect)
            
    def mostrar_heatmap(self):
        if not self.history_states:
            print("No hay jugadas registradas.")
            return

        num_jugadas = len(self.history_states)
        cols = 3
        rows = math.ceil(num_jugadas / cols)
        
        # Creamos la figura
        fig, axes = plt.subplots(rows, cols, figsize=(15, rows * 4), squeeze=False)
        fig.suptitle("Análisis de Q-Table por Movimiento", fontsize=16, fontweight='bold')
        
        # .flatten() convierte cualquier matriz (1x1, 2x2, 3x3) en una lista simple
        axes_flat = axes.flatten()

        for i, data in enumerate(self.history_states):
            estado_tuple = tuple(data["board"])
            jugador = data["player"]
            
            # Consultar la Q-Table
            q_values = self.bot.q_table.get(estado_tuple, np.zeros(9))
            grid_q = q_values.reshape((3, 3))

            # Ahora axes_flat[i] siempre será un objeto de ejes válido
            im = axes_flat[i].imshow(grid_q, cmap='RdYlGn', interpolation='nearest')
            
            axes_flat[i].set_title(f"Turno {i+1}: Movió {jugador}", fontsize=10)
            
            # Dibujar valores Q
            for r in range(3):
                for c in range(3):
                    val = grid_q[r, c]
                    axes_flat[i].text(c, r, f'{val:.2f}', ha="center", va="center", 
                                    color="black", fontsize=9, fontweight='bold')

        # Eliminar los cuadros blancos sobrantes
        for j in range(num_jugadas, len(axes_flat)):
            fig.delaxes(axes_flat[j])

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

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
        self.turn = self.initial_turn

        if self.turn == IA:
            self.bot_thinking = True
            self.think_start_time = pygame.time.get_ticks()

        self.boardState = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.history_states = []
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
        self.history_states.append({
        "board": list(self.boardState),
        "player": "TÚ (Humano)"
    })
        
        if not self.has_winner():      
            self.turn = IA
            self.turno_n = self.turno_n + 1

    def execute_bot_move(self):
        """Realiza el movimiento lógico del bot tras la espera"""
        jugada = self.bot.jugada_bot(self.boardState, False)
        # jugada = mejor_movimiento_IA(0, self.boardState)

        self.board.append_movement(jugada, self.player_bot.image_symbol)
        self.board.draw_movement(jugada, self.player_bot.image_symbol)  
        self.boardState[jugada] = IA
        self.history_states.append({
        "board": list(self.boardState),
        "player": "IA (Bot)"
    })
        self.bot_thinking = False # Apagar animación
        self.update_score()
        
        if not self.has_winner():      
            self.turn = PLAYER
            self.turno_n += 1

        # Limpiar textos de estado
        self.cover_text(pygame.Rect(430, 95, 220, 50))
        self.cover_text(pygame.Rect(430, 170, 220, 50))

        # Eliminamos la animacion de carga
        center_x, center_y = 200, 500 # Posición central de la animacion de carga
        rect = pygame.Rect(center_x - 100, center_y - 100, 220, 200)

        pygame.draw.rect(self.display, self.colors.bkg, rect)

    
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