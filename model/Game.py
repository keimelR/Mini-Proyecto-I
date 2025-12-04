from model.Player import Player
from model.Board import Board

# X = b'\x58'
# O = b'\x4f'
class Game:
    board: Board
    playerHuman: Player
    playerAgent: Player
    turnHuman: bool

    def __init__(self):
        self.board = Board()
        self.playerHuman = Player(b'\x58')
        self.playerAgent = Player(b'\x4f')
        self.turnHuman = True
        
    def hasWinner(self, symbol: bytes) -> bool:
        if(self.hasDiagonal(symbol) or self.hasHorizontal(symbol) or self.hasVertical(symbol)):
            return True
        else:
            return False
        
    def isDraw(self) -> bool:
        if(self.board.numberMarks == 9):
            return True
        else:
            return False
            
        
    def hasDiagonal(self, symbol: bytes) -> bool:
        # Diagonal desde la izquierda
        if(self.board.grids[0][0] == symbol and 
           self.board.grids[1][1] == symbol and
           self.board.grids[2][2] == symbol
        ): 
            return True
        
        # Diagonal desde la derecha
        if(self.board.grids[0][2] == symbol and 
           self.board.grids[1][1] == symbol and
           self.board.grids[2][0] == symbol
        ): 
            return True
        
        return False
    
    def hasHorizontal(self, symbol: bytes) -> bool:
        # Horizontal por la primera fila
        if(self.board.grids[0][0] == symbol and 
           self.board.grids[0][1] == symbol and 
           self.board.grids[0][2] == symbol
        ):
            return True
        
        # Horizontal por la segunda fila
        if(self.board.grids[1][0] == symbol and 
           self.board.grids[1][1] == symbol and 
           self.board.grids[1][2] == symbol
        ):
            return True
        
        # Horizontal por la tercera fila
        if(self.board.grids[2][0] == symbol and 
           self.board.grids[2][1] == symbol and 
           self.board.grids[2][2] == symbol
        ):
            return True
        
        return False
    
    def hasVertical(self, symbol: bytes) -> bool:
        # Vertical por la primera columna
        if(self.board.grids[0][0] == symbol and 
           self.board.grids[1][0] == symbol and 
           self.board.grids[2][0] == symbol
        ):
            return True
        
        # Vertical por la segunda columna
        if(self.board.grids[0][1] == symbol and 
           self.board.grids[1][1] == symbol and 
           self.board.grids[2][1] == symbol
        ):
            return True
        
        # Vertical por la tercera columna
        if(self.board.grids[0][2] == symbol and 
           self.board.grids[1][2] == symbol and 
           self.board.grids[2][2] == symbol
        ):
            return True
        
        return False
    
    def play(self, row: int, column: int) -> int:
        res: int
        if(self.turnHuman):
            res = self.board.markGrid(self.playerHuman.symbol, row, column)
        else:
            res = self.board.markGrid(self.playerAgent.symbol, row, column)
       
        if(res == 0):
            print(f"En el turno Human es: {self.turnHuman}")
            self.turnHuman = not self.turnHuman
        
        return res
    
    def minimax(self, tried: int):
        print(self.board)
        # Condiciones de Salida de Carrera
        if(self.isDraw()): # Empate/Tablas
            return 0
        if(self.hasWinner(b'\x58')): # Victoria del Agente Humano
            return -10 + tried
        if(self.hasWinner(b'\x4f')): # Victoria del Agente AI
            return 10 - tried

        res: int = 0
        for row in range(3):
            for column in range(3):
                if(self.board.canMarkGrid(row, column) == 0):
                    symbolOriginal: bytes = self.board.grids[row][column]
                    self.play(row, column)
                    res = self.minimax(tried + 1)
                    self.board.grids[row][column] = symbolOriginal
        return res
    
    def getSymbolTurn(self) -> bytes:
        if(self.turnHuman):
            return self.playerAgent.symbol
        else:
            return self.playerAgent.symbol