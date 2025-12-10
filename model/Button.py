import pygame

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_normal, color_hover, accion=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_actual = color_normal
        self.accion = accion  # La función que se ejecuta al hacer clic
        self.font = pygame.font.Font(None, 30)
        self.left = x
        self.top = y
        self.width = ancho
        self.height = alto
        self.right = x + ancho
        self.bottom = y + alto
        self.surface = None

    def draw(self, surface):
        # 1. Dibujar el cuerpo del botón
        pygame.draw.rect(surface, self.color_actual, self.rect, border_radius=5)

        self.surface = surface
        # 2. Renderizar y dibujar el texto
        text_surface = self.font.render(self.texto, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Ejecutar la acción si se hace clic
            if self.rect.collidepoint(event.pos) and self.accion:
                self.accion() # Llama a la función asignada