# Odio python con toda mi alma

import pygame

class Mark:
    def __init__(self, color: pygame.Color, screen: pygame.Surface):
        """
        Inicializa el objeto Mark con un color y una superficie de pantalla.
        
        Args:
            color (pygame.Color): Color del símbolo.
            screen (pygame.Surface): Superficie de Pygame donde se dibuja el símbolo.
        """
        self.color = color
        self.screen = screen
    
    def drawSymbolO(
        self,
        startX: int,
        startY: int,
        sizeGrid: int,
        radius: int,
        width: int
    ):
        """
        Dibuja el símbolo O en la celda correspondiente del tablero.
        
        Args:
            startX (int): offset X de la casilla
            startY (int): offset Y de la casilla
            left (int): Posición X inicial del tablero.
            top (int): Posición Y inicial del tablero.
            sizeGrid (int): Tamaño de cada celda.
            widhtLineBoard (int): Grosor de las líneas del tablero.
            radius (int): Radio del círculo O.
            width (int): Grosor de la línea del círculo.
        """
        
        pygame.draw.circle(
            self.screen,
            self.color,
            (startX + sizeGrid // 2, startY + sizeGrid // 2),
            radius,
            width
        )
        
        
    def drawSymbolX(
        self,
        startX: int,
        startY: int,
        sizeGrid: int,
        widthLineSymbol: int,
        margin = 10
    ):
        """
        Dibuja el símbolo X en la celda correspondiente del tablero.
        
        Args:
            startX (int): offset X de la casilla
            startY (int): offset Y de la casilla
            left (int): Posición X inicial del tablero.
            top (int): Posición Y inicial del tablero.
            sizeGrid (int): Tamaño de cada celda.
            widhtLineBoard (int): Grosor de las líneas del tablero.
            widthLineSymbol (int): Grosor de la línea del símbolo X.
        """
        
        pygame.draw.line(
            self.screen,
            self.color,
            (startX + margin, startY + margin),
            (startX + sizeGrid - margin, startY + sizeGrid - margin),
            widthLineSymbol
        )
            
        pygame.draw.line(
            self.screen,
            self.color,
            (startX + sizeGrid - margin, startY + margin),
            (startX + margin, startY + sizeGrid - margin),
            widthLineSymbol
        )  
    
    def getGridStartPosX(
        self, 
        areaX: int, 
        left: int,
        sizeGrid: int,
        widhtLine: int
    ) -> int:
        """
        Calcula la posición X inicial de la celda en el tablero.
        
        Args:
            areaX (int): Posición X del clic o referencia.
            left (int): Posición X inicial del tablero.
            sizeGrid (int): Tamaño de cada celda.
            widhtLine (int): Grosor de las líneas del tablero.
        
        Returns:
            int: Posición X inicial de la celda.
        """
        areaXPos = (areaX - (left + widhtLine // 2)) // sizeGrid
        areaXStart = left + (areaXPos * sizeGrid) + (sizeGrid // 4)
        if(areaXPos > 1):
            areaXStart += (widhtLine // 2)
        return areaXStart + 5
            
    def getGridStartPosY(
        self, 
        areaY: int, 
        top: int,
        sizeGrid: int,
        widhtLine: int
    ) -> int:
        """
        Calcula la posición Y inicial de la celda en el tablero.
        
        Args:
            areaY (int): Posición Y del clic o referencia.
            top (int): Posición Y inicial del tablero.
            sizeGrid (int): Tamaño de cada celda.
            widhtLine (int): Grosor de las líneas del tablero.
        
        Returns:
            int: Posición Y inicial de la celda.
        """
        areaYPos = (areaY - (top - sizeGrid + widhtLine)) // sizeGrid
        areaYStart = (top - sizeGrid + widhtLine) + (areaYPos * sizeGrid) + (sizeGrid // 4)
        if(areaYPos > 1):
            areaYStart += (widhtLine // 2)
        return areaYStart
    
    def setScreen(self, screen: pygame.Surface):
        """
        Asigna una nueva superficie de pantalla para dibujar los símbolos.
        
        Args:
            screen (pygame.Surface): Nueva superficie de Pygame.
        """
        self.screen = screen