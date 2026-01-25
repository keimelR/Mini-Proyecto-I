import pygame

from model.Colors import Colors
from model.Images import Images
from model.Symbol import Symbol
from model.Grid import Grid

class Board:
    """Tablero 3x3 para el juego.

    Esta clase encapsula la representación gráfica del tablero,
    la detección de qué casilla fue pulsada y la lista de movimientos
    realizados. Maneja el dibujo del contenedor, las celdas y los
    símbolos (imágenes) colocados en cada casilla.

    Atributos principales:
    - left, top: coordenadas del contenedor del tablero.
    - size_grid: tamaño (px) de cada celda del tablero.
    - widt_line: ancho (px) de los espacios/ bordes entre celdas.
    - display: superficie `pygame.Surface` donde se dibuja el tablero.
    - images, colors: utilidades de dibujo (instancias de `Images` y `Colors`).
    - movements: lista de `Symbol` con los movimientos realizados.
    - grid_map: diccionario que mapea índice de casilla (0-8) a `Grid`.
    """

    def __init__(self, left: int, top: int, size_grid: int, widt_line: int, display: pygame.Surface):
        """Inicializa el `Board` y construye el mapa de celdas.

        Parámetros:
        - left, top: posición superior-izquierda del contenedor del tablero.
        - size_grid: tamaño en píxeles de cada celda.
        - widt_line: ancho en píxeles de las líneas/espacios entre celdas.
        - display: superficie de `pygame` donde se realiza el dibujo.
        """
        self.left = left
        self.top = top
        self.size_grid = size_grid
        self.widt_line = widt_line
        self.display = display
        
        self.images = Images()
        self.colors = Colors()
        
        self.movements: list[Symbol] = []
        self.grid_map = {
            0: Grid(
                left = self.left + self.widt_line,
                top = self.top + self.widt_line,
                right = self.left + self.size_grid + self.widt_line,
                bottom = self.top + self.size_grid + self.widt_line
            ),
            1: Grid(
                left = self.left + self.size_grid + self.widt_line * 2,
                top = self.top + self.widt_line,
                right = self.left + self.size_grid * 2 + self.widt_line * 2,
                bottom = self.top + self.size_grid + self.widt_line
            ),
            2: Grid(
                left = self.left + self.size_grid * 2 + self.widt_line * 3, 
                top = self.top + self.widt_line,
                right = self.left + self.size_grid * 3 + self.widt_line * 3,
                bottom = self.top + self.size_grid + self.widt_line
            ),
            3: Grid(
                left = self.left + self.widt_line,
                top = self.top + self.size_grid + self.widt_line * 2,
                right = self.left + self.size_grid + self.widt_line,
                bottom = self.top + self.size_grid * 2 + self.widt_line * 2
            ),
            4: Grid(
              left = self.left + self.size_grid + self.widt_line * 2,
              top = self.top + self.size_grid + self.widt_line * 2,
              right = self.left + self.size_grid * 2 + self.widt_line * 2,
              bottom = self.top + self.size_grid * 2 + self.widt_line * 2
            ),
            5: Grid(
                left = self.left + self.size_grid * 2 + self.widt_line * 3,
                top = self.top + self.size_grid + self.widt_line * 2,
                right = self.left + self.size_grid * 3 + self.widt_line * 3,
                bottom = self.top + self.size_grid * 2 + self.widt_line * 2
            ),
            6: Grid(
                left = self.left + self.widt_line,
                top = self.top + self.size_grid * 2 + self.widt_line * 3,
                right = self.left + self.size_grid + self.widt_line,
                bottom = self.top + self.size_grid * 3 + self.widt_line * 3
            ),
            7: Grid(
                left = self.left + self.size_grid + self.widt_line * 2,
                top = self.top + self.size_grid * 2 + self.widt_line * 3,
                right = self.left + self.size_grid * 2 + self.widt_line * 2,
                bottom = self.top + self.size_grid * 3 + self.widt_line * 3
            ),
            8: Grid(
                left = self.left + self.size_grid * 2 + self.widt_line * 3,
                top = self.top + self.size_grid * 2 + self.widt_line * 3,
                right = self.left + self.size_grid * 3 + self.widt_line * 3,
                bottom = self.top + self.size_grid * 3 + self.widt_line * 3
            )
        }

    def on_event(self, event: pygame.event.Event):
        """Procesa eventos de `pygame` relacionados con el ratón.

        Si se detecta `MOUSEBUTTONDOWN` devuelve el índice de la casilla
        seleccionada (0-8) si está libre; devuelve `None` si no hay selección
        válida.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid = self.markGrid(x, y)

            if grid != -1 and not self.movement_perfomed(grid):
                return grid
            return None 
           
    def reset(self):
        """Limpia la lista de movimientos, dejando el tablero vacío."""
        self.movements.clear()
        
    def append_movement(self, grid, image):
        """Añade un movimiento a la lista.

        Parámetros:
        - grid: índice de la casilla (0-8).
        - image: identificador/clave de la imagen a dibujar.
        """
        symbol = Symbol(grid, image)
        self.movements.append(symbol)
        
    def draw_movement(self, grid, image):
        """Dibuja una imagen en la casilla indicada sin agregarla a movimientos."""
        casilla = self.grid_map[grid]
        self.images.draw(image, 120, 120, casilla.left, casilla.top, self.display)
         
    def movement_perfomed(self, grid) -> bool:
        """Devuelve True si ya existe un movimiento en la casilla dada."""
        movement_perfomed = False
        for movement in self.movements:
            if movement.grid == grid:
                movement_perfomed = True
                break
        return movement_perfomed

    def draw(self):
        """Punto de entrada para dibujar todo el tablero en pantalla."""
        self.draw_board()  
        
    def draw_board(self):
        """Dibuja el contenedor, las celdas y los movimientos ya realizados."""
        self.draw_container()
        self.draw_grids() 
        self.draw_movements()
           
    def draw_movements(self):
        """Dibuja todos los símbolos/imagenes de `self.movements` sobre el tablero."""
        for movements in self.movements:
            casilla = self.grid_map[movements.grid]
            self.images.draw(movements.image, 120, 120, casilla.left, casilla.top, self.display)     
           
    def surface_container(self) -> pygame.Surface:
        """Crea y devuelve la superficie del contenedor del tablero.

        La superficie se dimensiona para contener las 3x3 celdas más los
        márgenes/espacios definidos por `widt_line`.
        """
        surface = pygame.Surface(
            ((self.size_grid * 3) + (self.widt_line * 4), 
             (self.size_grid * 3) + (self.widt_line * 4)),
            pygame.SRCALPHA
        )
    #    print(f"Surface del Contendor: {surface.get_rect()}")
        return surface
    
    def rect_container(self) -> pygame.Rect:
        """Devuelve el `Rect` del contenedor posicionado en `left, top`."""
        rect = self.surface_container().get_rect()
        rect.left = self.left
        rect.top = self.top
        return rect
    
    def draw_container(self):
        """Dibuja el fondo/contorno del tablero en la superficie principal."""
        surface = self.surface_container()
        rect = self.rect_container()
        pygame.draw.rect(
            surface, (104, 116, 133), surface.get_rect(),  
            border_radius=10
        )
        self.display.blit(surface, rect)      
    
        
    def surface_grid(self) -> pygame.Surface:
        """Crea y devuelve la superficie para una sola celda (grid)."""
        surface = pygame.Surface(
            (self.size_grid, self.size_grid),
            pygame.SRCALPHA
        )
        return surface
    
    def rect_grid(self, left, top) -> pygame.Rect:
        """Devuelve el `Rect` de una celda situado en `left, top`."""
        rect = self.surface_grid().get_rect()
        rect.top = top
        rect.left = left
    #    print(f"[INFO] - RECT_GRID: {rect}")
        return rect

    def draw_grid(self):
        """Dibuja una celda individual en la posición (`left`, `top`)."""
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

    def markGrid(self, areaX: int,areaY: int) -> int:
        """Devuelve el índice de casilla (0-8) que contiene las coordenadas.

        Si ninguna casilla contiene las coordenadas devuelve -1.
        """
        grid = -1
        for n_casilla in self.grid_map:
            casilla = self.grid_map[n_casilla]
            if(areaX >= casilla.left and areaX <= casilla.right and areaY >= casilla.top and areaY <= casilla.bottom):
                grid = n_casilla
                break
        return grid