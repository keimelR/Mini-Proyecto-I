import pygame

from model.Text import Text, TypeFont
from model.Colors import Colors
from model.Images import Images

class IconButton:
    def __init__(self, text_button: str, text_color: Colors, left: float, top: float, button_width: int, button_height: int, button_color: Colors, button_shadow_color: Colors, button_shadow_height: float, icon: Images, icon_width: float, icon_height: float, display: pygame.Surface, accion):
        self.text_button = text_button
        self.text_color = text_color
        self.left = left
        self.top = top
        self.button_width = button_width
        self.button_height = button_height
        self.button_color = button_color
        self.button_shadow_height = button_shadow_height
        self.button_shadow_color = button_shadow_color
        self.icon = icon
        self.icon_width = icon_width
        self.icon_height = icon_height
        self.display = display
        self.accion = accion
        self.contador = 0
    
    def handle_event(self, event):        
        # Responder sólo a clic izquierdo para evitar cerrar por otros botones/events
        if event.type == pygame.MOUSEBUTTONDOWN and getattr(event, 'button', None) == 1:
            rect_container_button = self.rect_button_container()
            if rect_container_button.collidepoint(event.pos):
                self.contador = self.contador + 1
                print(f"[INFO] - Model.IconButton - Numero de Presiones en el Boton: {self.contador}")
                # Llama a la función asignada sólo si es callable
                if callable(self.accion):
                    self.accion()
    
    def surface_text(self) -> pygame.Surface:
        text = Text()
        return text.role(TypeFont.TITTLE_LARGE, self.text_button, self.text_color)
    
    def rect_text(self) -> pygame.Rect:
        rect = self.surface_text().get_rect()
        rect.center = (self.left, self.top)
    #    print(f"[INFO] - Model.IconButton - Rectangulo del Texto: {rect}")
        return rect
    
    
    def surface_button_container(self) -> pygame.Surface:
        text = self.surface_text()
        buttonContainerSurface = pygame.Surface(
            (text.get_width() + self.button_width, text.get_height() + self.button_height),
            pygame.SRCALPHA
        )
    #    print(f"[INFO] - Model.IconButton - buttonContainerSurface: {buttonContainerSurface}")

        return buttonContainerSurface
    
    def rect_button_container(self) -> pygame.Rect:
        rect = self.surface_button_container().get_rect(center = self.rect_text().center)
    #    print(f"[INFO] - Model.IconButton - Rectangulo del Container de Boton: {rect}")
        return rect
 
    
    def surface_icon(self) -> pygame.Surface:
        icon = pygame.image.load(self.icon)
        icon = pygame.transform.smoothscale(icon, (self.icon_width, self.icon_height))
    #    print(f"[INFO] - Model.IconButton - Icon: {icon}")
        return icon
    
    def rect_icon(self) -> pygame.Rect:
        icon = self.surface_icon()
        rect_button_container = self.rect_button_container()
        
        rect = icon.get_rect()
        rect.center = (rect_button_container.left + 20, self.top)
    #    print(f"[INFO] - Model.IconButton - Rectangulo del Icon: {rect}")

        return rect
    
    
    def rect_shadow_button_container(self) -> pygame.Rect:
        rect_btn_container = self.rect_button_container()
        shadow_button_container = pygame.Rect(rect_btn_container.left, rect_btn_container.top + rect_btn_container.height, rect_btn_container.width, self.button_shadow_height)
    #    print(f"[INFO] - Model.IconButton - Rectangulo del Shadow Boton: {shadow_button_container}")

        return shadow_button_container

    
    def draw_text(self):
        surface_text = self.surface_text()
        rect_text = self.rect_text()
        self.display.blit(surface_text, rect_text)

    
    def draw_container(self):
        surface_button_container = self.surface_button_container()
        rect_button_container = self.rect_button_container()
        pygame.draw.rect(self.display, self.button_color, rect_button_container, border_top_left_radius=5, border_top_right_radius=5)
        self.display.blit(surface_button_container, rect_button_container)
        
    def draw_icon(self):
        surface_icon = self.surface_icon()
        rect_icon = self.rect_icon()
        self.display.blit(surface_icon, rect_icon)
    
    def draw_shadow_container(self):
        shadow_container = self.rect_shadow_button_container()
        pygame.draw.rect(self.display, self.button_shadow_color, shadow_container, border_bottom_left_radius=5, border_bottom_right_radius=5)
    
    def draw_icon_button(self):
        self.draw_container()
        self.draw_shadow_container()
        self.draw_text()
        self.draw_icon()
    
    
    """
    def __init__(self, x, y, ancho, alto, texto, color_normal, color_hover, color_texto, accion=None):
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
        self.color_texto = color_texto
        self.surface = None

    def draw(self, surface):
        # 1. Dibujar el cuerpo del botón
        pygame.draw.rect(surface, self.color_actual, self.rect, border_radius=5)

        self.surface = surface
        # 2. Renderizar y dibujar el texto
        text_surface = self.font.render(self.texto, True, self.color_texto)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Ejecutar la acción si se hace clic
            if self.rect.collidepoint(event.pos) and self.accion:
                self.accion() # Llama a la función asignada
                
    """