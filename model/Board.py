import pygame

from model.Colors import Colors
class Board:
    def __init__(self, left: int, top: int, size_grid: int, widt_line: int, display: pygame.Surface):
        self.left = left
        self.top = top
        self.size_grid = size_grid
        self.widt_line = widt_line
        self.display = display
        
        self.colors = Colors()
        
    def draw(self):
        self.draw_container()
        self.draw_grids()   
        
    def surface_container(self) -> pygame.Surface:
        surface = pygame.Surface(
            ((self.size_grid * 3) + (self.widt_line * 4), 
             (self.size_grid * 3) + (self.widt_line * 4)),
            pygame.SRCALPHA
        )
    #    print(f"Surface del Contendor: {surface.get_rect()}")
        return surface
    
    def rect_container(self) -> pygame.Rect:
        rect = self.surface_container().get_rect()
        rect.left = self.left
        rect.top = self.top
        return rect
    
    def draw_container(self):
        surface = self.surface_container()
        rect = self.rect_container()
        pygame.draw.rect(
            surface, (104, 116, 133), surface.get_rect(),  
            border_radius=10
        )
        self.display.blit(surface, rect)      
    
        
    def surface_grid(self) -> pygame.Surface:
        surface = pygame.Surface(
            (self.size_grid, self.size_grid),
            pygame.SRCALPHA
        )
        return surface
    
    def rect_grid(self, left, top) -> pygame.Rect:
        rect = self.surface_grid().get_rect()
        rect.top = top
        rect.left = left
        print(f"[INFO] - RECT_GRID: {rect}")
        return rect

    def draw_grid(self):
        surface = self.surface_grid()
        rect = self.rect_grid(self.left, self.top)
        
        # Dibujamos en la superficie pequeña (en su origen local)
        pygame.draw.rect(surface, (238, 238, 238), surface.get_rect(), border_radius=10)
        self.display.blit(surface, rect)

    def draw_grids(self):
        start_x = self.left + self.widt_line
        start_y = self.top + self.widt_line
        for row in range(3):
            for column in range(3):
                # 2. Creamos la superficie de la celda
                surface = self.surface_grid()
                
                # 3. Calculamos la posición exacta de este cuadro
                pos_x = start_x + (column * (self.size_grid + self.widt_line))
                pos_y = start_y + (row * (self.size_grid + self.widt_line))
                
                # 4. Dibujamos internamente en la superficie (coordenadas 0,0)
                pygame.draw.rect(
                    surface, self.colors.bkg, surface.get_rect(),
                    border_radius=10
                )
                
                # 5. Lo pegamos en la posición calculada
                self.display.blit(surface, (pos_x, pos_y))
        # Dibujamos en la superficie pequeña (en su origen local)
    #    pygame.draw.rect(surface, (238, 238, 238), surface.get_rect(), border_radius=10)
    #    self.display.blit(surface, rect)