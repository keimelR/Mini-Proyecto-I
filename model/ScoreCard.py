import pygame
from model.Text import Text, TypeFont
from model.Images import Images
from model.Colors import Colors
from model.Button import Boton


class ScoreCard:
    def __init__(self, text_card: str, text_score: str, text_color: Colors, left: float, top: float, card_width: int, card_height: int, card_color: Colors, image: Images, image_width: float, image_height: float, display: pygame.Surface):
        self.text_card = text_card
        self.text_score = text_score
        self.text_color = text_color
        self.left = left
        self.top = top
        self.card_width = card_width
        self.card_height = card_height
        self.card_color = card_color
        self.image = image
        self.image_width = image_width
        self.image_height = image_height
        self.display = display
        
    def surface_card_container(self) -> pygame.Surface:
        surface_card_container = pygame.Surface(
            (self.card_width, self.card_height),
            pygame.SRCALPHA
        )
    #    print(f"[INFO] - Model.IconButton - buttonContainerSurface: {surface_card_container}")
        return surface_card_container
    
    def rect_card_container(self) -> pygame.Rect:
        rect = self.surface_card_container().get_rect()
        rect.left = self.left
        rect.top = self.top
    #    print(f"[INFO] - Model.IconButton - Rectangulo del Container de Boton: {rect}")
        return rect
    
    def surface_text(self) -> pygame.Surface:
        text = Text()
        return text.role(TypeFont.TITTLE_LARGE, self.text_card, self.text_color)
    
    def surface_score(self) -> pygame.Surface:
        text = Text()
        return text.role(TypeFont.TITTLE_LARGE, self.text_score, self.text_color)   
    
    def rect_text(self) -> pygame.Rect:
        rect = self.surface_text().get_rect()
        # self.left + (self.card_width // 5) ,
        rect.center = (self.left + (self.card_width // 5), self.top + (3 * self.card_height  // 4))
    #    print(f"[INFO] - Model.IconButton - Rectangulo del Texto: {rect}")
        return rect
    
    def rect_score(self) -> pygame.Rect:
        rect = self.surface_score().get_rect()
        rect.center = (self.left + self.card_width - (self.card_width // 8)), self.top + (3 * self.card_height  // 4)
    #    print(f"[INFO] - Model.IconButton - Rectangulo del Texto: {rect}")
        return rect
    
    def surface_image(self) -> pygame.Surface:
        image = pygame.image.load(self.image)
        image = pygame.transform.smoothscale(image, (self.image_width, self.image_height))
    #    print(f"[INFO] - Model.IconButton - Icon: {icon}")
        return image
    
    def rect_image(self) -> pygame.Rect:
        image = self.surface_image()
        rect_card_container = self.rect_card_container()
        
        rect = image.get_rect()
        rect.center = (
            self.left + (self.card_width // 6) ,
            self.top + (self.card_height // 3)
        )
    #    print(f"[INFO] - Model.IconButton - Rectangulo del Icon: {rect}")
        return rect
    
    def draw_text(self):
        surface = self.surface_text()
        rect = self.rect_text()
        self.display.blit(surface, rect)
        
    def draw_score(self):
        surface = self.surface_score()
        rect = self.rect_score()
        self.display.blit(surface, rect)
        
    def draw_container(self):
        surface = self.surface_card_container()
        rect = self.rect_card_container()
        pygame.draw.rect(self.display, self.card_color, rect, border_radius=5)
        self.display.blit(surface, rect)
        
    def draw_image(self):
        surface = self.surface_image()
        rect = self.rect_image()
        self.display.blit(surface, rect)
        
    def draw_score_card(self):
        self.draw_container()
        self.draw_text()
        self.draw_score()
        self.draw_image()
        