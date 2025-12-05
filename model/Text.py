import pygame
from enum import Enum

class TypeFont(Enum):
    """
    Enumeración de los diferentes estilos de fuente utilizados en la interfaz gráfica.
    """
    DISPLAY = 0
    HEADLINE = 1
    TITTLE_LARGE = 2
    TITTLE_MEDIUM = 3

class Text:
    """
    Clase para gestionar y renderizar diferentes estilos de texto en la interfaz gráfica usando Pygame.
    """
    def __init__(self):
        """
        Inicializa los diferentes estilos de fuente que se usarán para mostrar textos en pantalla.
        """
        self.font = pygame.font.init()
        self.display = pygame.font.SysFont('couriernew', 45, True, False)
        self.headLine = pygame.font.SysFont('couriernew', 28)
        self.tittleLarge = pygame.font.SysFont('couriernew', 22)
        self.tittleMedium = pygame.font.SysFont('couriernew', 16)
    
    def role(
        self,
        typeFont: TypeFont, 
        text: str,
        color: pygame.Color = (0, 0, 0)
    ) -> pygame.Surface:
        """
        Renderiza un texto en la superficie de Pygame usando el estilo de fuente especificado.
        
        Args:
            typeFont (TypeFont): Tipo de fuente a utilizar.
            text (str): Texto a mostrar.
            color (pygame.Color, opcional): Color del texto. Por defecto es negro.
        
        Returns:
            pygame.Surface: Superficie con el texto renderizado lista para ser blitteada.
        """
        textDisplay: pygame.Surface
        match typeFont:
            case TypeFont.DISPLAY:
                textDisplay = self.display.render(text, False, color)
            case TypeFont.HEADLINE:
                textDisplay = self.headLine.render(text, False, color)
            case TypeFont.TITTLE_LARGE:
                textDisplay = self.tittleLarge.render(text, False, color)
            case TypeFont.TITTLE_MEDIUM:
                textDisplay = self.tittleMedium.render(text, False, color)
            case _:
                textDisplay = self.tittleMedium.render(text, False, color)
        return textDisplay
