import pygame
import time
import pygame.math
from constantes import *
from tkinter import messagebox

from typing import Tuple

from model.BoardFront import BoardFront
from model.Text import Text, TypeFont
from model.Images import Images
from model.Colors import Colors
from minimax import mejor_movimiento_IA


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
        
    def on_execute(self):
        self.on_init()
        
        self.display.fill(self.colors.background)
        
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
            text="00",
            areaX=435,
            areaY=480,
            align="center"
        )
        
        # Contador de Victorias del Agente AI
        self.print(
            typeFont=TypeFont.TITTLE_LARGE,
            text="00",
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
        
        while(self.running):  
            for event in pygame.event.get():
                self.on_event(event)
            
            self.drawTitleCard(
                typeFont=TypeFont.HEADLINE,
                text="Turno: Usuario" if self.turn == PLAYER else "Turno: Agente AI",
                coordinates=(self.widht // 2, 83 + 20),
                align="center"
            )
            pygame.display.flip()
            
    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                print(f"X = {mouse_x} - Y = {mouse_y}")                    
                
                if self.turn == PLAYER:
                    # Tablero
                    if((mouse_x > self.boardFront.left and mouse_x < self.boardFront.left + self.boardFront.width) and (mouse_y > self.boardFront.top and mouse_y < self.boardFront.top + self.boardFront.height)):        
                        # Obtenemos la cuadricula del tablero que fue marcada
                        grid = self.markGrid(areaX=mouse_x, areaY=mouse_y)
                        
                        print(self.boardFront.grid_map)
                        print("Casilla: ", grid)
                        print("Contenido Casilla: ", self.boardState[grid])
                        print("Coordenadas: ", self.boardFront.grid_map[grid])
                        
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
                                                            
                            if self.existWinner == 0:
                                self.turn *= -1
        
                    # Boton de Reiniciar Juego
                    if((mouse_x > 432 and mouse_x < 648) and (mouse_y > 605 and mouse_y < 645)):
                        cleanBoard = pygame.Rect(
                            315,
                            190,
                            180,
                            180
                        )      
                        pygame.draw.rect(self.display, self.colors.backgroundCard, cleanBoard)
                        self.resetGame()
                    
    def turnoPlayer(self, grid: int):
        self.boardState[grid] = PLAYER
        casilla = self.boardFront.grid_map[grid]
        
        self.boardFront.agentO.drawSymbolO(
            startX= casilla[0],
            startY=casilla[1],
            sizeGrid=60,
            radius=20,
            width=7
        )
        
        # Modificamos el estado del tablero en memoria con la jugada en la cuadricula realizada
                    
    def turnoIA(self):
        mejor_movimiento = mejor_movimiento_IA(self.boardState.copy(), self.turno_n)
                        
        self.boardState[mejor_movimiento] = IA
        casilla = self.boardFront.grid_map[mejor_movimiento]       
        
        
        # Dibuja en pantalla una 'X' cuando sea turno del Agente AI
        self.boardFront.agentX.drawSymbolX(
            startX=casilla[0],
            startY=casilla[1],
            sizeGrid=60,
            widthLineSymbol=7
        )
        
        return mejor_movimiento
        #    self.printSymbolX(areaX=mouse_x, areaY=mouse_y)

        # Modificamos el estado del tablero en memoria con la jugada en la cuadricula realizada
      
    def resetGame(self):
        self.existWinner = 0
        self.turn = PLAYER
        self.boardState = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        
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
            for pasos in range(cantidad_de_pasos, 0, -1):
                pygame.draw.line(
                    self.display,
                    (255,0,0),
                    (self.boardFront.left, self.boardFront.top + (row * (SIZE_GRID + WIDTH_LINE_CASILLA)) + SIZE_GRID // 2),
                    (self.boardFront.left + (self.boardFront.width //  pasos), self.boardFront.top + (row * (SIZE_GRID + WIDTH_LINE_CASILLA)) + SIZE_GRID // 2),
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
            for pasos in range(cantidad_de_pasos, 0, -1):
                pygame.draw.line(
                    self.display,
                    (255,0,0),
                    (self.boardFront.left + (column * (SIZE_GRID + WIDTH_LINE_CASILLA)) + SIZE_GRID // 2, self.boardFront.top),
                    (self.boardFront.left + (column * (SIZE_GRID + WIDTH_LINE_CASILLA)) + SIZE_GRID // 2, self.boardFront.top + (self.boardFront.height //  pasos)),
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
                pygame.draw.line(
                    self.display,
                    (255,0,0),
                    (grid_map[0][0] + 10, grid_map[0][1] + 10),
                    (grid_map[8][2] - 10, grid_map[8][3] - 10),
                    5
                )
                pygame.display.flip()
                pygame.time.delay(5)
                
    def winDiagonalRight(self) -> bool:
        return (self.boardState[2] == self.turn and self.boardState[4] == self.turn and self.boardState[6] == self.turn)
                
    def effectWinDiagonalRight(self):
        if (self.winDiagonalRight()):
            grid_map = self.boardFront.grid_map
            
            cantidad_de_pasos = 180
            for pasos in range(cantidad_de_pasos):
                pygame.draw.line(
                    self.display,
                    (255,0,0),
                    (grid_map[6][0] + 10, grid_map[6][3] - 10),
                    (grid_map[2][2] - 10, grid_map[2][3] + 10),
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