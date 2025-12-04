import pygame
from enum import Enum

class TypeFont(Enum):
    DISPLAY = 0
    HEADLINE = 1
    TITTLE_LARGE = 2
    TITTLE_MEDIUM = 3

class Text:
    def __init__(self):
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
