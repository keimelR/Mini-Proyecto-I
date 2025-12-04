import pygame

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
        self.usedHeight = 0
                
    def on_init(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.widht, self.height))
        self.running = True
        
    def on_execute(self):
        self.on_init()
        
        self.display.fill(self.colors.background)
        
        self.print(
            typeFont=TypeFont.HEADLINE,
            text="Bienvenido a:",
            areaX=(self.widht // 2),
            areaY=self.usedHeight + (self.height // 60),
            align="center"
        )
        
        self.print(
            typeFont=TypeFont.DISPLAY,
            text="Tic Tac Toe",
            areaX=self.widht // 2,
            areaY=self.usedHeight + (self.height // 40),
            align="center"
        )
        
        containerRect = pygame.Rect((
            self.widht // 4, 
            self.usedHeight + 20, 
            self.widht // 2, 
            self.height // 1.5
        ))
        pygame.draw.rect(self.display, self.colors.backgroundCard, containerRect, 0, 20)
        
        containerRectTitle = pygame.Rect((
            self.widht // 4, 
            self.usedHeight + 20, 
            self.widht // 2, 
            32
        ))
        pygame.draw.rect(
            self.display, 
            self.colors.backgroundHeaderCard, 
            containerRectTitle, 
            border_top_left_radius=10, 
            border_bottom_right_radius=10
        )
        
        self.print(
            typeFont=TypeFont.HEADLINE,
            text="Un Clasico Juego",
            areaX=self.widht // 2,
            areaY=self.usedHeight + 20,
            align="center"
        )
    
        self.printBoard()
    
        # Container del usuario
        containerUser = pygame.Rect((
            20 + (self.widht // 4),
            440,
            225,
            70
        ))
        
        # Container del Agente AI
        containerAgentAi = pygame.Rect(
            565,
            440,
            225,
            70
        )
                
        # Imprimir el Container del Usuario en la Pantalla
        pygame.draw.rect(
            self.display, 
            self.colors.secondary, 
            containerUser, 
            0,
            border_top_left_radius=60,
            border_bottom_left_radius=60
        )
        
        # Imprimir el Container del Agente AI en la Pantalla
        pygame.draw.rect(
            self.display, 
            self.colors.secondary, 
            containerAgentAi, 
            0,
            border_top_left_radius=60,
            border_bottom_left_radius=60
        )
        
        # Texto de Usuario
        self.print(
            typeFont=TypeFont.TITTLE_LARGE,
            text="Usuario",
            areaX=435,
            areaY=440,
            align="center"
        )
        
        # Texto de Agente AI
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
        
        # Imagen de Logo del Usuario
        self.printImage(
            image=self.images.userHumanLogo,
            areaX=20 + (self.widht // 4),
            areaY=440
        )
    
        # Imagen de Logo de Agente AI
        self.printImage(
            image=self.images.userAgentAi,
            areaX=565,
            areaY=440
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
        pygame.draw.rect(
            self.display,
            self.colors.terciary,
            buttonRestart,
            width=1,
            border_radius=20
        )
        
        while(self.running):  
            for event in pygame.event.get():
                self.on_event(event)
                
            pygame.display.flip()
            
                
    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                
                mouse_x, mouse_y = event.pos
                if(mouse_x >= 315 and mouse_x <= 495 and mouse_y >= 190 and mouse_y <= 370):
                    print(f"{mouse_x} - {mouse_y}")
                    self.printSymbolX(
                        areaX=mouse_x,
                        areaY=mouse_y
                    )
            
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
        self.usedHeight += textDisplay.get_height()
        
        print(self.usedHeight)
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
        widhtImage = transparencyImage.get_width()
        
        self.display.blit(transparencyImage, (areaX , areaY))
        
        

    def printBoard(self):
        for column in range(2):
            columnLine = pygame.Rect((
                45 + (self.widht // 4),
                self.height // 3 + (60 * column),
                180,
                10
            ))
            
            pygame.draw.rect(
                self.display, 
                self.colors.neutral, 
                columnLine, 
                border_top_left_radius=10, 
                border_bottom_right_radius=10
            )
            
        for row in range(2):
            rowLine = pygame.Rect((
                self.widht // 2 - 170 + (row * 60),
                190,
                10,
                180
            ))
            
            pygame.draw.rect(
                self.display, 
                self.colors.neutral, 
                rowLine, 
                border_top_left_radius=10, 
                border_bottom_right_radius=10
            )
            
    def printSymbolX(
        self,
        areaX: int,
        areaY: int
    ):
        areaXPos = (areaX - 315) // 60
        areaYPos = (areaY - 190) // 60
        
        areaXStart = 315 + (areaXPos * 60) + 15
        areaYStart = 190 + (areaYPos * 60) + 15
        
        print(f"El areaXStart es: {areaXStart}")
        print(f"El areaYStart es: {areaYStart}")

        if(areaXPos > 1):
            areaXStart += 5
        
        if(areaYPos > 1):
            areaYStart += 5
            
        areaXEnd = areaXStart + 60 - 30
        areaYEnd = areaYStart + 60 - 30
            
            
        pygame.draw.line(
            self.display,
            self.colors.error,
            (areaXStart, areaYStart),
            (areaXEnd, areaYEnd),
            10
        )
            
        pygame.draw.line(
            self.display,
            self.colors.error,
            (areaXEnd, areaYStart),
            (areaXStart, areaYEnd),
            10
        )  