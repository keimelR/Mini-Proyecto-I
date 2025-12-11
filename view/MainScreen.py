import pygame
import time
import pygame.math
from constantes import *
from tkinter import messagebox
from model.Button import Boton

from bigtree import Node

from typing import Tuple

from model.BoardFront import BoardFront
from model.Text import Text, TypeFont
from model.Images import Images
from model.Colors import Colors
from minimax import mejor_movimiento_IA, cargar_arbol_de_nodos


PESTAÑA_PARTIDA = 0
PESTAÑA_ARBOL_DE_DESICIONES = 1

SIZE_GRID = 60
WIDTH_LINE_CASILLA = 10


class MainScreen:
    def __init__(self):
        self.widht = 1080
        self.height = 720
        self.running = True
        self.display = None
        self.text = Text()
        self.colors = Colors()
        self.images = Images()
        self.boardFront = BoardFront(self.colors.neutral, self.colors.secondary, self.colors.terciary, self.display)
        self.usedHeight = 0

        self.leftBoard = self.widht // 2 - ((WIDTH_LINE_CASILLA * 3) // 2) - (SIZE_GRID * 3 // 2)
        self.topBoard = self.height // 3 - 50

        self.existWinner = 0
        self.turn = -1
        self.turno_n = 0
        self.boardState = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.numberWinUser = 0
        self.numberWinAgentAi = 0

        self.pestaña = PESTAÑA_PARTIDA

        self.boton_partida = None
        self.boton_arbol_de_desiciones = None

        self.nodo_raiz_arbol_de_desiciones = Node("raiz", tablero=[0,0,0,0,0,0,0,0,0]) # Este es el nodo raíz del arbol de desiciones

        self.nodo_actual_partida_arbol_de_desiciones = self.nodo_raiz_arbol_de_desiciones # Este es el nodo que se muestra en la vista de la partida
        self.nodo_actual_arbol_de_desiciones = self.nodo_raiz_arbol_de_desiciones # Este es el nodo padre que se muestra en el arbol de desiciones

        self.boton_ver_nodo_padre = None
        self.boton_ver_estado_actual = None

        self.subTablerosArbolDeDesiciones = []


        self.grid_map = {
        # Fila 1 (Y: 190 - 250)
        0: (self.leftBoard, self.topBoard, self.widht // 3, self.height // 1.5),
        1: (375, 190, 435, 250),
        2: (435, 190, 495, 250),

        # Fila 2 (Y: 250 - 310)
        3: (315, 250, 375, 310),
        4: (375, 250, 435, 310),
        5: (435, 250, 495, 310),

        # Fila 3 (Y: 310 - 370)
        6: (315, 310, 375, 370),
        7: (375, 310, 435, 370),
        8: (435, 310, 495, 370),
        }


    def on_init(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.widht, self.height))
        self.running = True
        cargar_arbol_de_nodos(self.nodo_raiz_arbol_de_desiciones, profundidad=0)

    def on_execute(self):
        self.on_init()

        self.boton_partida = Boton(10, 5, 130, 40, "Partida", self.colors.secondary, self.colors.terciary, self.cambiarPestañaPartida)
        self.boton_arbol_de_desiciones = Boton(self.boton_partida.right + 10, self.boton_partida.top, 230, 40, "Arbol de Desiciones", self.colors.secondary, self.colors.terciary, self.cambiarPestañaArbolDeDesiciones)
        navBar = pygame.Rect((0, 0, self.widht, 50))

        while(self.running):
            for event in pygame.event.get():
                self.on_event(event)

            self.display.fill(self.colors.background)

            if self.pestaña == PESTAÑA_PARTIDA:
                self.cargar_pestaña_partida()

            if self.pestaña == PESTAÑA_ARBOL_DE_DESICIONES:
                self.cargar_pestaña_arbol_de_desiciones()


            pygame.draw.rect(self.display, self.colors.backgroundCard, navBar, border_radius=10)
            self.boton_partida.draw(self.display)
            self.boton_arbol_de_desiciones.draw(self.display)

            pygame.display.flip()

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.running = False

        if self.boton_partida:
            self.boton_partida.handle_event(event)

        if self.boton_arbol_de_desiciones:
            self.boton_arbol_de_desiciones.handle_event(event)

        if self.boton_ver_nodo_padre:
            self.boton_ver_nodo_padre.handle_event(event)

        if self.boton_ver_estado_actual:
            self.boton_ver_estado_actual.handle_event(event)

        if len(self.subTablerosArbolDeDesiciones) > 0:
            for tablero in self.subTablerosArbolDeDesiciones:
                tablero.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                print(f"X = {mouse_x} - Y = {mouse_y}")

                if self.turn == PLAYER:
                    # Boton de Reiniciar Juego
                    if((mouse_x > 432 and mouse_x < 648) and (mouse_y > 605 and mouse_y < 645)):
                        cleanBoard = pygame.Rect(
                            self.leftBoard,
                            self.topBoard,
                            SIZE_GRID * 3,
                            SIZE_GRID * 3
                        )      
                        pygame.draw.rect(self.display, self.colors.backgroundCard, cleanBoard)
                        self.resetGame()
                        
                    # Tablero
                    if((mouse_x > self.boardFront.left and mouse_x < self.boardFront.left + self.boardFront.width) and (mouse_y > self.boardFront.top and mouse_y < self.boardFront.top + self.boardFront.height)) and self.pestaña == PESTAÑA_PARTIDA:
                        # Obtenemos la cuadricula del tablero que fue marcada
                        grid = self.markGrid(areaX=mouse_x, areaY=mouse_y)

                        if grid == -1:
                            return
                        
                        pygame.draw.rect(
                            self.display,
                            self.colors.terciary,
                            (self.boardFront.grid_map[grid][0], self.boardFront.grid_map[grid][1], SIZE_GRID, SIZE_GRID),
                            5,
                        )
                        pygame.display.flip()
                        pygame.time.delay(100)
                        
                        if self.boardState[grid] == IA or self.boardState[grid] == PLAYER:
                            # TODO. Pop-Up Anunciando que cuadricula ocupada
                            messagebox.showwarning("Cuadricula Ocupada", "La cuadricula seleccionada ya esta ocupada")
                            return


                        # Mientras no exista un ganador se puede jugar
                        if self.existWinner == 0:
                            self.turnoPlayer(grid=grid)

                            self.turno_n += 1

                            if(self.winVertical() or self.winHorizontal() or self.winDiagonalLeft() or self.winDiagonalRight()):
                                # Realizamos un efecto de desplazamiento por medio de una linea en la jugada ganadora
                                self.effectWin(grid)
                                # Almacenamos el ganador
                                self.existWinner = PLAYER

                                self.numberWinUser += 1
                            else:
                                self.turn = IA

                                # Aqui se debe de colocar una pantalla de carga hasta que se acabe el tiempo
                                # time.sleep(5)

                                mejor_movimiento = self.turnoIA()

                                self.turno_n += 1

                                if(self.winVertical() or self.winHorizontal() or self.winDiagonalLeft() or self.winDiagonalRight()):
                                    # Realizamos un efecto de desplazamiento por medio de una linea en la jugada ganadora
                                    self.effectWin(n_casilla=mejor_movimiento)
                                    # Almacenamos el ganador
                                    self.existWinner = IA

                                    self.numberWinAgentAi += 1
                                    
                                    self.turn = PLAYER
                                                            
                            if self.existWinner == 0:
                                self.turn *= -1
                    
    def turnoPlayer(self, grid: int):
        self.boardState[grid] = PLAYER
        casilla = self.boardFront.grid_map[grid]

        for nodo in self.nodo_actual_partida_arbol_de_desiciones.children:
            print(nodo.get_attr("tablero"))
            if nodo.get_attr("tablero") == self.boardState:
                self.nodo_actual_partida_arbol_de_desiciones = nodo
                break

        self.nodo_actual_arbol_de_desiciones = self.nodo_actual_partida_arbol_de_desiciones
        # Modificamos el estado del tablero en memoria con la jugada en la cuadricula realizada
        
    def turnoIA(self):
        mejor_movimiento = mejor_movimiento_IA(self.turno_n, self.boardState)

        if mejor_movimiento == -1:
            print("No se puede realizar la jugada")
            print(self.boardState)
            return
        self.boardState[mejor_movimiento] = IA
        casilla = self.boardFront.grid_map[mejor_movimiento]

        # 2. Buscamos y actualizamos el nodo después del movimiento de la IA
        for nodo in self.nodo_actual_partida_arbol_de_desiciones.children:
            # Comparamos el tablero del nodo hijo con el estado actual del juego
            if nodo.get_attr("tablero") == self.boardState:
                self.nodo_actual_partida_arbol_de_desiciones = nodo
                self.nodo_actual_arbol_de_desiciones = self.nodo_actual_partida_arbol_de_desiciones # También actualiza el nodo de la vista del árbol
                break
        else:
            # Esto NO debería pasar si el árbol se cargó correctamente y mejor_movimiento_IA funciona bien
            print("IA: ¡Advertencia! No se encontró el nodo hijo de la IA.")

        return mejor_movimiento
        #    self.printSymbolX(areaX=mouse_x, areaY=mouse_y)

        # Modificamos el estado del tablero en memoria con la jugada en la cuadricula realizada
      
     
    def cambiarPestañaPartida(self):
        self.pestaña = PESTAÑA_PARTIDA
        print("Partida")

    def cambiarPestañaArbolDeDesiciones(self):
        self.pestaña = PESTAÑA_ARBOL_DE_DESICIONES
        print("Arbol de desiciones")

    def resetGame(self):
        self.existWinner = 0
        self.turn = PLAYER
        self.boardState = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.turno_n = 0 
        
        # Resetear los nodos del árbol
        self.nodo_actual_partida_arbol_de_desiciones = self.nodo_raiz_arbol_de_desiciones
        self.nodo_actual_arbol_de_desiciones = self.nodo_raiz_arbol_de_desiciones
        
        self.boardFront.draw(self.leftBoard, self.topBoard, 60, 10)

    def print(
        self,
        typeFont:
        TypeFont,
        text: str,
        areaX: float,
        areaY: float,
        align: str = "none",
        color: pygame.Color = (0, 0, 0)
    ):
        textDisplay = self.text.role(typeFont, text, color)
        if(align == "center"):
            self.display.blit(textDisplay, (areaX - textDisplay.get_width() / 2, areaY))
        else:
            self.display.blit(textDisplay, (areaX, areaY))

    def printImage(
        self,
        image: str,
        areaX: float,
        areaY: float
    ):
        loadImage = pygame.image.load(image)
        transparencyImage = loadImage.convert_alpha()
        self.display.blit(transparencyImage, (areaX , areaY))

    def markGrid(
        self,
        areaX: int,
        areaY: int
    ) -> int:
        grid = -1
        for n_casilla in self.boardFront.grid_map:
            casilla = self.boardFront.grid_map[n_casilla]
            if(areaX >= casilla[0] and areaX <= casilla[2] and areaY >= casilla[1] and areaY <= casilla[3]):
                grid = n_casilla
                break
        return grid

    def effectWin(self, n_casilla: int):
        row = 0 if n_casilla >= 0 and n_casilla <= 2 else 1 if n_casilla >= 3 and n_casilla <= 5 else 2
        column = n_casilla % 3

        self.effectWinHorizontal(row)
        self.effectWinVertical(column)
        self.effectWinDiagonalLeft()
        self.effectWinDiagonalRight()

    def winHorizontal(self) -> bool:
        return (self.boardState[0] == self.turn and self.boardState[1] == self.turn and self.boardState[2] == self.turn) or (self.boardState[3] == self.turn and self.boardState[4] == self.turn and self.boardState[5] == self.turn) or (self.boardState[6] == self.turn and self.boardState[7] == self.turn and self.boardState[8] == self.turn)

    def effectWinHorizontal(self, row: int):
        if self.winHorizontal():
            cantidad_de_pasos = 180
            for pasos in range(1, cantidad_de_pasos + 1):
                progreso = pasos / cantidad_de_pasos
                x_final = self.boardFront.left + (self.boardFront.width * progreso)
                
                pygame.draw.line(
                    self.display,
                    (255,0,0),
                    (self.boardFront.left, self.boardFront.top + (row * (SIZE_GRID + WIDTH_LINE_CASILLA)) + SIZE_GRID // 2),
                    (x_final, self.boardFront.top + (row * (SIZE_GRID + WIDTH_LINE_CASILLA)) + SIZE_GRID // 2),
                    5
                )
                pygame.display.flip()
                pygame.time.delay(5)


    def winVertical(self) -> bool:
        return (self.boardState[0] == self.turn and self.boardState[3] == self.turn and self.boardState[6] == self.turn) or (self.boardState[1] == self.turn and self.boardState[4] == self.turn and self.boardState[7] == self.turn) or (self.boardState[2] == self.turn and self.boardState[5] == self.turn and self.boardState[8] == self.turn)

    def effectWinVertical(self, column: int):
        print(column)
        if (self.winVertical()):
            cantidad_de_pasos = 180
            for pasos in range(1, cantidad_de_pasos + 1):
                progreso = pasos / cantidad_de_pasos
                y_final = self.boardFront.top + (self.boardFront.height * progreso)
                
                pygame.draw.line(
                    self.display,
                    (255,0,0),
                    (self.boardFront.left + (column * (SIZE_GRID + WIDTH_LINE_CASILLA)) + SIZE_GRID // 2, self.boardFront.top),
                    (self.boardFront.left + (column * (SIZE_GRID + WIDTH_LINE_CASILLA)) + SIZE_GRID // 2, y_final),
                    5
                )
                pygame.display.flip()
                pygame.time.delay(5)

    def winDiagonalLeft(self) -> bool:
        return (self.boardState[0] == self.turn and self.boardState[4] == self.turn and self.boardState[8] == self.turn)

    def effectWinDiagonalLeft(self):
        if (self.winDiagonalLeft()):
            grid_map = self.boardFront.grid_map

            cantidad_de_pasos = 180
            for pasos in range(cantidad_de_pasos):
                progreso = pasos / cantidad_de_pasos

                # Calcular punto final basado en progreso
                start_x = self.boardFront.grid_map[0][0] + 10
                start_y = self.boardFront.grid_map[0][1] + 10
                end_x = self.boardFront.grid_map[8][2] - 10
                end_y = self.boardFront.grid_map[8][3] - 10
                
                current_x = start_x + (end_x - start_x) * progreso
                current_y = start_y + (end_y - start_y) * progreso

                pygame.draw.line(
                    self.display,
                    (255,0,0),
                    (start_x, start_y),
                    (current_x, current_y),
                    5
                )
                pygame.display.flip()
                pygame.time.delay(5)

    def winDiagonalRight(self) -> bool:
        return (self.boardState[2] == self.turn and self.boardState[4] == self.turn and self.boardState[6] == self.turn)

    def effectWinDiagonalRight(self):
        if (self.winDiagonalRight()):
            print("Este es el bug")
            grid_map = self.boardFront.grid_map

            cantidad_de_pasos = 180
            for pasos in range(cantidad_de_pasos):
                
                progreso = pasos / cantidad_de_pasos
                
                # Coordenadas para diagonal derecha
                start_x = self.boardFront.grid_map[2][2] - 10  # Superior derecha
                start_y = self.boardFront.grid_map[2][1] + 10
                end_x = self.boardFront.grid_map[6][0] + 10    # Inferior izquierda
                end_y = self.boardFront.grid_map[6][3] - 10
                
                current_x = start_x + (end_x - start_x) * progreso
                current_y = start_y + (end_y - start_y) * progreso
                
                pygame.draw.line(
                    self.display,
                    (255, 0, 0),
                    (start_x, start_y),
                    (current_x, current_y),
                    5
                )
                pygame.display.flip()
                pygame.time.delay(5)

    def drawCard(self):
        containerRect = pygame.Rect((
            self.widht // 4,
            83 + 20,
            self.widht // 2,
            self.height // 1.5
        ))
        pygame.draw.rect(self.display, self.colors.backgroundCard, containerRect, 0, 20)

    def drawCardIcon(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        color: pygame.Color,
        imgPath: str,
        coordinates: Tuple[int, int]
    ):
        # Container de la Card
        containerUser = pygame.Rect((
            left,
            top,
            width,
            height
        ))

        # Dibujar el Container en la Pantalla
        pygame.draw.rect(self.display, color, containerUser, 0,
            border_top_left_radius=60,
            border_bottom_left_radius=60
        )

        areaX, areaY = coordinates
        # Dibujar el Icono del Card
        self.printImage(
            image=imgPath,
            areaX=areaX,
            areaY=areaY
        )

    def drawTitleCard(
        self,
        typeFont: TypeFont,
        text: str,
        coordinates: Tuple[float, float],
        align: str = "none",
        color: pygame.Color = (0, 0, 0)
    ):
        # Dibujamos el titulo de la "Card" del juego
        containerRectTitle = pygame.Rect((
            self.widht // 4,
            83 + 20,
            self.widht // 2,
            32
        ))
        pygame.draw.rect(
            self.display, self.colors.terciary, containerRectTitle,
            border_top_left_radius=10,
            border_top_right_radius=10
        )

        areaX, areaY = coordinates
        self.print(
            typeFont=typeFont,
            text=text,
            areaX=areaX,
            areaY=areaY,
            align=align
        )

    def cargar_pestaña_arbol_de_desiciones(self):
        # if self.turno_n == 0:
        #     self.print(
        #         typeFont=TypeFont.HEADLINE,
        #         text="Realiza tu jugada para cargar el arbol de desiciones",
        #         areaX=(self.widht // 2),
        #         areaY=120,
        #         align="center"
        #     )

        #     size_grid_tablero = 60
        #     widthline_tablero = 10
        #     width_tablero = size_grid_tablero * 3 + (widthline_tablero * 2)

        #     tablero_draw = BoardFront(self.colors.neutral, self.colors.secondary, self.colors.terciary, self.display)
        #     tablero_draw.draw(self.widht // 2 - (width_tablero // 2), 190, sizeGrid=size_grid_tablero, widhtLine=widthline_tablero)
        #     return

        def accion_boton_ver_nodo_padre():
            if self.nodo_actual_arbol_de_desiciones.parent != None:
                self.nodo_actual_arbol_de_desiciones = self.nodo_actual_arbol_de_desiciones.parent
                print(self.nodo_actual_arbol_de_desiciones)
            else:
                messagebox.showwarning("Error", "No se puede acceder al nodo padre")

        def accion_boton_ver_estado_actual():
            self.nodo_actual_arbol_de_desiciones = self.nodo_actual_partida_arbol_de_desiciones

        self.cargar_tableros_arbol_de_desiciones()
        width_boton_ver_nodo_padre = 200
        width_boton_ver_estado_actual = 200

        self.boton_ver_nodo_padre = Boton(self.widht - width_boton_ver_nodo_padre - 20, 60, width_boton_ver_nodo_padre, 40, "Ver nodo padre", self.colors.secondary, self.colors.terciary, accion=accion_boton_ver_nodo_padre)
        self.boton_ver_estado_actual = Boton(self.widht - width_boton_ver_estado_actual - 20, self.boton_ver_nodo_padre.bottom + 20, width_boton_ver_estado_actual, 40, "Ver estado actual", self.colors.secondary, self.colors.terciary, accion=accion_boton_ver_estado_actual)


        self.boton_ver_nodo_padre.draw(self.display)
        self.boton_ver_estado_actual.draw(self.display)

    def cargar_tableros_arbol_de_desiciones(self):
        size_grid_tablero_padre = 50
        widthline_tablero_padre = 8
        width_tablero_padre = size_grid_tablero_padre * 3 + (widthline_tablero_padre * 2)

        self.subTablerosArbolDeDesiciones = []

        def accion_click_tablero(nodo: Node):
            self.nodo_actual_arbol_de_desiciones = nodo

        turno = self.nodo_actual_arbol_de_desiciones.get_attr("jugador")
        is_win = self.nodo_actual_arbol_de_desiciones.get_attr("victoria")
        
        # ----------------------------------------------------
        # Parámetros de conexión y coordenadas del padre
        # ----------------------------------------------------
        color_linea_conexion = self.colors.terciary

        # Coordenadas X del centro del tablero padre
        x_centro_padre = self.widht // 2 
        # Coordenadas Y del borde inferior del tablero padre (100 es la Y de inicio del tablero)
        y_borde_inferior_padre = 100 + (size_grid_tablero_padre * 3 + widthline_tablero_padre * 2)
        # ----------------------------------------------------

        # Indicamos el tipo de jugador del nodo actual
        self.print(
            typeFont=TypeFont.HEADLINE,
            text="Player" if turno == PLAYER else "IA" if turno == IA else "Tablero Vacio",
            areaX=100,
            areaY=70,
            align="left"
        )

        tablero_padre = self.nodo_actual_arbol_de_desiciones.get_attr("tablero")
        tablero_padre_draw = BoardFront(self.colors.morado if turno == PLAYER else self.colors.azul, self.colors.secondary, self.colors.terciary, self.display, nodo=self.nodo_actual_arbol_de_desiciones)
        tablero_padre_draw.draw(self.widht // 2 - (width_tablero_padre // 2), 100, sizeGrid=size_grid_tablero_padre, widhtLine=widthline_tablero_padre)
        radio_circulo_tablero_padre = 20
        widthline_circulo_tablero_padre = 7

        for i in range(9):
            if tablero_padre[i] == PLAYER:
                tablero_padre_draw.agentO.drawSymbolO(
                    startX=tablero_padre_draw.grid_map[i][0],
                    startY=tablero_padre_draw.grid_map[i][1],
                    sizeGrid=size_grid_tablero_padre,
                    radius=radio_circulo_tablero_padre,
                    width=widthline_circulo_tablero_padre
                )
            elif tablero_padre[i] == IA:
                tablero_padre_draw.agentX.drawSymbolX(
                    startX=tablero_padre_draw.grid_map[i][0],
                    startY=tablero_padre_draw.grid_map[i][1],
                    sizeGrid=size_grid_tablero_padre,
                    widthLineSymbol=7
                )

        if is_win == PLAYER:
            self.print(
                typeFont=TypeFont.TITTLE_LARGE,
                text="¡Vcitoria del Usuario!",
                areaX=self.widht // 2,
                areaY=self.height // 2,
                align="center"
            )
        
        if is_win == IA:
            self.print(
                typeFont=TypeFont.TITTLE_LARGE,
                text="¡Vcitoria de la IA!",
                areaX=self.widht // 2,
                areaY=self.height // 2,
                align="center"
            )
            
        if is_win == VACIO and len(self.nodo_actual_arbol_de_desiciones.children) == 0:
            self.print(
                typeFont=TypeFont.TITTLE_LARGE,
                text="¡Empate!",
                areaX=self.widht // 2,
                areaY=self.height // 2,
                align="center"
            )

        # --- CÁLCULO PARA CENTRAR LOS TABLEROS HIJOS ---
        size_grid_tablero = 30
        widthline_tablero = 4
        width_tablero_hijo = size_grid_tablero * 3 + (widthline_tablero * 2)
        espacio_entre_tableros = 20
        
        num_hijos = len(self.nodo_actual_arbol_de_desiciones.children)
        
        # Coordenada Y de inicio de la segunda fila
        y_inicio_hijos = 500
        
        if num_hijos > 0:
            # Calcular el ancho total que ocuparán los tableros y los espacios
            ancho_total_tableros = (num_hijos * width_tablero_hijo)
            ancho_total_espacios = (num_hijos - 1) * espacio_entre_tableros
            ancho_total_ocupado = ancho_total_tableros + ancho_total_espacios
            
            # Calcular la coordenada X de inicio para centrar el grupo
            lastX = (self.widht // 2) - (ancho_total_ocupado // 2)
        else:
            lastX = 20 # Valor predeterminado si no hay hijos
        # --- FIN DEL CÁLCULO ---

        # Posición Y del borde superior de la fila de hijos
        y_borde_superior_hijo = y_inicio_hijos 

        for nodo in self.nodo_actual_arbol_de_desiciones.children:
            tablero = nodo.get_attr("tablero")
            turno = nodo.get_attr("jugador")

            # 1. Dibujar el tablero hijo
            tablero_draw = BoardFront(self.colors.morado if turno == PLAYER else self.colors.azul, self.colors.secondary, self.colors.terciary, self.display, accion=accion_click_tablero, nodo=nodo)
            tablero_draw.draw(lastX, y_inicio_hijos, sizeGrid=size_grid_tablero, widhtLine=widthline_tablero)

            self.subTablerosArbolDeDesiciones.append(tablero_draw)
            
            # 2. Dibujar la línea de conexión al tablero padre (CORRECCIÓN APLICADA AQUÍ)
            x_centro_hijo = lastX + (width_tablero_hijo // 2)
            
            # Conexión del centro inferior del padre al centro superior del hijo
            pygame.draw.line( # <--- CORREGIDO: Usar pygame.draw.line()
                self.display, # Pasar la superficie de dibujo
                color_linea_conexion,
                (x_centro_padre, y_borde_inferior_padre),
                (x_centro_hijo, y_borde_superior_hijo),
                3
            )

            radio_circulo_tablero_hijo = 10
            widthline_circulo_tablero_hijo = 4

            # Actualizar la posición X para el siguiente tablero
            lastX += tablero_draw.width + espacio_entre_tableros

            # 3. Dibujar los símbolos del tablero hijo
            for j in range(9):
                if tablero[j] == PLAYER:
                    tablero_draw.agentO.drawSymbolO(
                        startX=tablero_draw.grid_map[j][0],
                        startY=tablero_draw.grid_map[j][1],
                        sizeGrid=size_grid_tablero,
                        radius=radio_circulo_tablero_hijo,
                        width=widthline_circulo_tablero_hijo
                    )
                elif tablero[j] == IA:
                    tablero_draw.agentX.drawSymbolX(
                        startX=tablero_draw.grid_map[j][0],
                        startY=tablero_draw.grid_map[j][1],
                        sizeGrid=size_grid_tablero,
                        widthLineSymbol=3,
                        margin=5
                    )

    def cargar_pestaña_partida(self):
        # Dibujamos el texto "Bienvenido a:"
        self.print(
            typeFont=TypeFont.HEADLINE,
            text="Bienvenido a:",
            areaX=(self.widht // 2),
            areaY=0 + (self.height // 60),
            align="center"
        )

        # Dibujamos el texto "Tic Tac Toe"
        self.print(
            typeFont=TypeFont.DISPLAY,
            text="Tic Tac Toe",
            areaX=self.widht // 2,
            areaY=32 + (self.height // 40),
            align="center"
        )

        self.drawCard()

        # Dibujamos el Tablero
        self.boardFront.setScreen(self.display)
        self.boardFront.draw(self.leftBoard, self.topBoard, 60, 10)

        # Dibujamos el CardIcon del Usuario
        self.drawCardIcon(
            left=20 + (self.widht // 4),
            top=440,
            width=225,
            height=70,
            color=self.colors.secondary,
            imgPath=self.images.userHumanLogo,
            coordinates=(20 + (self.widht // 4), 440)
        )

        # Dibujamos el CardIcon del Agente AI
        self.drawCardIcon(
            left=565,
            top=440,
            width=225,
            height=70,
            color=self.colors.terciary,
            imgPath=self.images.userAgentAi,
            coordinates=(565, 440)
        )

        # Dibujamos el texto "Usuario"
        self.print(
            typeFont=TypeFont.TITTLE_LARGE,
            text="Usuario",
            areaX=435,
            areaY=440,
            align="center"
        )

        # Dibujamos el texto de "Agente AI"
        self.print(
            typeFont=TypeFont.TITTLE_LARGE,
            text="Agente AI",
            areaX=710,
            areaY=440,
            align="center"
        )

        # Contador de Victorias del Usuario
        self.print(
            typeFont=TypeFont.TITTLE_LARGE,
            text=f"{self.numberWinUser}",
            areaX=435,
            areaY=480,
            align="center"
        )

        self.print(
            typeFont=TypeFont.TITTLE_LARGE,
            text=f"{self.numberWinAgentAi}",
            areaX=710,
            areaY=480,
            align="center"
        )

        self.print(
            typeFont=TypeFont.TITTLE_MEDIUM,
            text="Reiniciar Juego",
            areaX=self.widht * 0.5,
            areaY=615,
            align="center",
            color=(100, 100,100)
        )
        
        titulo = ""
        if (self.turno_n + 1) % 11 == 0:
            titulo = "Empate"
        elif self.existWinner == PLAYER:
            titulo = "¡Ha ganado el jugador!"
        elif self.existWinner == IA:
            titulo = "¡Ha ganado el agente AI!"

        self.drawTitleCard(
            typeFont=TypeFont.HEADLINE,
            text=titulo,
            coordinates=(self.widht // 2, 83 + 20),
            align="center"
        )
        """
        self.drawTitleCard(
            typeFont=TypeFont.HEADLINE,
            text="Turno: Usuario" if self.turn == PLAYER else "Turno: Agente AI",
            coordinates=(self.widht // 2, 83 + 20),
            align="center"
        )
        """ 
        buttonRestart = pygame.Rect(
            self.widht * 0.4,
            605,
            self.widht * 0.6 - self.widht * 0.4,
            40
        )
        pygame.draw.rect(self.display, self.colors.terciary, buttonRestart,
            width=1,
            border_radius=20
        )

        # Dibujamos las jugadas actuales del tablero
        for i in range(9):
            casilla = self.boardFront.grid_map[i]

            if self.boardState[i] == PLAYER:
                self.boardFront.agentO.drawSymbolO(
                    startX= casilla[0],
                    startY= casilla[1],
                    sizeGrid=60,
                    radius=20,
                    width=7
                )

            if self.boardState[i] == IA:
                self.boardFront.agentX.drawSymbolX(
                startX=casilla[0],
                startY=casilla[1],
                sizeGrid=60,
                widthLineSymbol=7
            )