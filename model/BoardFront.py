from typing import Callable
import pygame
from model.Mark import Mark 
from bigtree import Node

class BoardFront:
    def __init__(
        self, 
        colorBoard: pygame.Color, 
        colorSymbolX: pygame.Color, 
        colorSymbolO: pygame.Color,
        screen: pygame.Surface,
        accion: Callable = None,
        nodo: Node = None
    ):
        """
        Inicializa el tablero gráfico y los agentes X y O.
        
        Args:
            colorBoard (pygame.Color): Color del tablero.
            colorSymbolX (pygame.Color): Color del símbolo X.
            colorSymbolO (pygame.Color): Color del símbolo O.
            screen (pygame.Surface): Superficie de Pygame donde se dibuja el tablero.
        """
        self.colorBoard = colorBoard
        self.screen = screen
        self.agentX = Mark(colorSymbolX, self.screen)
        self.agentO = Mark(colorSymbolO, self.screen)
        self.width = 0
        self.height = 0
        self.left = 0
        self.top = 0
        self.accion = accion
        self.rect = None
        
        self.nodo = nodo
        
        self.grid_map = {}

    def handle_event(self, event):        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Ejecutar la acción si se hace clic
            if self.rect.collidepoint(event.pos) and self.accion:
                self.accion(self.nodo) # Llama a la función asignada

    def draw(
        self,
        left: int,
        top: int,
        sizeGrid: int,
        widhtLine: int
    ):
        """
        Dibuja el tablero de tres en raya en la pantalla.
        
        Args:
            left (int): Posición X inicial del tablero.
            top (int): Posición Y inicial del tablero.
            sizeGrid (int): Tamaño de cada celda del tablero.
            widhtLine (int): Grosor de las líneas del tablero.
        """
        self.width = sizeGrid * 3 + (widhtLine * 2)
        self.height = self.width
        self.left = left
        self.top = top
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        
        self.grid_map = {
            0: (left, top, left + sizeGrid, top + sizeGrid),
            1: (left + sizeGrid + widhtLine, top, left + sizeGrid * 2 + widhtLine, top + sizeGrid),
            2: (left + sizeGrid * 2 + widhtLine * 2, top, left + sizeGrid * 3 + widhtLine * 2, top + sizeGrid),
            
            3: (left, top + sizeGrid + widhtLine, left + sizeGrid, top + sizeGrid * 2 + widhtLine),
            4: (left + sizeGrid + widhtLine, top + sizeGrid + widhtLine, left + sizeGrid * 2 + widhtLine, top + sizeGrid * 2 + widhtLine),
            5: (left + sizeGrid * 2 + widhtLine * 2, top + sizeGrid + widhtLine, left + sizeGrid * 3 + widhtLine * 2, top + sizeGrid * 2 + widhtLine),
            
            6: (left, top + sizeGrid * 2 + widhtLine * 2, left + sizeGrid, top + sizeGrid * 3 + widhtLine * 2),
            7: (left + sizeGrid + widhtLine, top + sizeGrid * 2 + widhtLine * 2, left + sizeGrid * 2 + widhtLine, top + sizeGrid * 3 + widhtLine * 2),
            8: (left + sizeGrid * 2 + widhtLine * 2, top + sizeGrid * 2 + widhtLine * 2, left + sizeGrid * 3 + widhtLine * 2, top + sizeGrid * 3 + widhtLine * 2),
        }
        
        for row in range(2):
            
            rowLine = pygame.Rect((
                left,
                top + (sizeGrid * (row + 1)) + (widhtLine * (row)),
                self.width,
                widhtLine
            ))
            pygame.draw.rect(
                self.screen, 
                self.colorBoard, 
                rowLine, 
                border_top_left_radius=3,
                border_bottom_right_radius=3
            )
            
        for column in range(2):
            columnLine = pygame.Rect((
                left + (sizeGrid * (column + 1)) + (widhtLine * (column)),
                top ,
                widhtLine,
                self.width
            ))
            pygame.draw.rect(
                self.screen, 
                self.colorBoard, 
                columnLine, 
                border_top_left_radius=10, 
                border_bottom_right_radius=10
            )

    def resetAgent(self):
        """
        Restablece la pantalla de los agentes X y O al valor actual de la pantalla.
        """
        self.agentO.setScreen(self.screen)
        self.agentX.setScreen(self.screen)

    def setScreen(self, screen: pygame.Surface):
        """
        Asigna una nueva superficie de pantalla y actualiza los agentes.
        
        Args:
            screen (pygame.Surface): Nueva superficie de Pygame.
        """
        self.screen = screen
        self.agentO.setScreen(screen)
        self.agentX.setScreen(screen)
        
    def setColorBoard(self, colorBoard: pygame.Color):
        """
        Cambia el color del tablero.
        
        Args:
            colorBoard (pygame.Color): Nuevo color para el tablero.
        """
        self.colorBoard = colorBoard
        
    def getScreen(self) -> pygame.Surface:
        """
        Devuelve la superficie de pantalla actual.
        
        Returns:
            pygame.Surface: Superficie de Pygame usada para dibujar.
        """
        return self.screen
        
    def getColorBoard(self) -> pygame.Color:
        """
        Devuelve el color actual del tablero.
        
        Returns:
            pygame.Color: Color del tablero.
        """
        return self.colorBoard