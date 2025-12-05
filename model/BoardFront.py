import pygame
from model.Mark import Mark 

class BoardFront:
    def __init__(
        self, 
        colorBoard: pygame.Color, 
        colorSymbolX: pygame.Color, 
        colorSymbolO: pygame.Color,
        screen: pygame.Surface,
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
        width = sizeGrid * 3
        for column in range(2):
            columnLine = pygame.Rect((
                left + widhtLine,
                top + (sizeGrid * column),
                width,
                widhtLine
            ))
            pygame.draw.rect(
                self.screen, 
                self.colorBoard, 
                columnLine, 
                border_top_left_radius=10, 
                border_bottom_right_radius=10
            )
        for row in range(2):
            rowLine = pygame.Rect((
                left + (width // 3) + (row * sizeGrid),
                top - sizeGrid + widhtLine,
                widhtLine,
                width
            ))
            pygame.draw.rect(
                self.screen, 
                self.colorBoard, 
                rowLine, 
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