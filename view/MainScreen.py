import pygame
import time
import pygame.math

from typing import Tuple

from model.BoardFront import BoardFront
from model.Text import Text, TypeFont
from model.Images import Images
from model.Colors import Colors

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
        
        self.leftBoard = 40 + self.widht // 4
        self.topBoard = self.height // 3
        
        self.existWinner = 0
        self.turn = -1
        self.boardState = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        self.numberWinUser = 0
        self.numberWinAgentAi = 0
        
                
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
        
        # Dibujamos el "Card" del juego
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
                text="Turno: Usuario" if self.turn == 1 else "Turno: Agente AI",
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
                
                # Tablero
                if((mouse_x > 315 and mouse_x < 495) and (mouse_y > 190 and mouse_y < 370)):        
                    # Obtenemos la cuadricula del tablero que fue marcada
                    grid = self.markGrid(areaX=mouse_x, areaY=mouse_y) - 1
                    
                    if self.boardState[grid] == 1 or self.boardState[grid] == -1:
                        # TODO. Pop-Up Anunciando que cuadricula ocupada
                        print("Cuadricula Ocupada")
                        return
                    
                    # Mientras no exista un ganador se puede jugar
                    if self.existWinner == 0:
                        
                        # Dibuja en pantalla un 'O' cuando sea turno del Usuario
                        if self.turn == 1:
                            self.boardFront.agentO.drawSymbolO(
                                areaX=mouse_x,
                                areaY=mouse_y,
                                left=self.leftBoard,
                                top=self.topBoard,
                                sizeGrid=60,
                                widhtLineBoard=10,
                                radius=20,
                                width=7
                            )
                        
                        # Dibuja en pantalla una 'X' cuando sea turno del Agente AI
                        if self.turn == -1:
                            self.boardFront.agentX.drawSymbolX(
                                areaX=mouse_x,
                                areaY=mouse_y,
                                left=self.leftBoard,
                                top=self.topBoard,
                                sizeGrid=60,
                                widhtLineBoard=10,
                                widthLineSymbol=7
                            )
                        #    self.printSymbolX(areaX=mouse_x, areaY=mouse_y)

                        # Modificamos el estado del tablero en memoria con la jugada en la cuadricula realizada
                        self.boardState[grid] = self.turn
                                                
                        if(self.winVertical() or self.winHorizontal() or self.winDiagonalLeft() or self.winDiagonalRight()):
                            # Realizamos un efecto de desplazamiento por medio de una linea en la jugada ganadora
                            self.effectWin(areaX=mouse_x, areaY=mouse_y)
                            # Almacenamos el ganador
                            self.existWinner = self.turn
                            
                            if self.existWinner == 1:
                                self.numberWinUser += 1
                            else:
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
                    
    def resetGame(self):
        self.existWinner = 0
        self.turn = -1
        self.boardState = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        self.boardFront.draw(self.leftBoard, self.topBoard, 60, 10)
     
    def print(
        self,
        typeFont: TypeFont,
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
        grid = (round(areaX - 315) // 60) + (round(areaY - 190) // 60) + 1
        if(areaY >= 250 and areaY < 310):
            grid += 2
        elif(areaY >= 310 and areaY < 370):
            grid += 4
        return grid
    
    def effectWin(self, areaX: int, areaY: int):
        row = (areaX - 315) // 60
        column = (areaY - 190) // 60
        
        self.effectWinHorizontal(column)
        self.effectWinVertical(row)
        self.effectWinDiagonalLeft()
        self.effectWinDiagonalRight()
                
    def winHorizontal(self) -> bool:            
        return ((self.boardState[0] == self.boardState[1] and self.boardState[0] == self.boardState[2]) or
            (self.boardState[3] == self.boardState[4] and self.boardState[3] == self.boardState[5]) or
            (self.boardState[6] == self.boardState[7] and self.boardState[6] == self.boardState[8])
        )
    
    def effectWinHorizontal(self, column: int):
        if self.winHorizontal():
            for row in range(180):
                pygame.draw.line(
                    self.display,
                    self.colors.terciary if self.turn == 1 else self.colors.secondary,
                    (315, 215 + (column * 60)),
                    (315 + row, 215 + (column * 60)),
                    5
                )
                pygame.display.flip()
                pygame.time.delay(5)
                
                
    def winVertical(self) -> bool:
        return ((self.boardState[0] == self.boardState[3] and self.boardState[0] == self.boardState[6]) or
            (self.boardState[1] == self.boardState[4] and self.boardState[1] == self.boardState[7]) or
            (self.boardState[2] == self.boardState[5] and self.boardState[2] == self.boardState[8])
        )
    
    def effectWinVertical(self, row: int):
        if (self.winVertical()):
            for column in range(180):
                pygame.draw.line(
                    self.display,
                    self.colors.terciary if self.turn == 1 else self.colors.secondary,
                    (315 + 30 + (row * 60), 190),
                    (315 + 30 + (row * 60), 190 + column),
                    5
                )
                pygame.display.flip()
                pygame.time.delay(5)
    
    def winDiagonalLeft(self) -> bool:
        return self.boardState[0] == self.boardState[4] and self.boardState[0] == self.boardState[8]
    
    def effectWinDiagonalLeft(self):
        if (self.winDiagonalLeft()):
            for column in range(180):
                pygame.draw.line(
                    self.display,
                    self.colors.terciary if self.turn == 1 else self.colors.secondary,
                    (315 + column, 190 + column),
                    (315 + column, 190 + column),
                    5
                )
                pygame.display.flip()
                pygame.time.delay(5)
                
    def winDiagonalRight(self) -> bool:
        return (self.boardState[2] == self.boardState[4] and self.boardState[2] == self.boardState[6])
                
    def effectWinDiagonalRight(self):
        if (self.winDiagonalRight()):
            for column in range(180):
                pygame.draw.line(
                    self.display,
                    self.colors.terciary if self.turn == 1 else self.colors.secondary,
                    (495 - column, 190 + column),
                    (495 - column, 190 + column),
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