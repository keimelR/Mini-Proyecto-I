from model.Game import Game

class PlayerAgentAI:
    symbol: bytes
    stateGame: Game
    
    def __init__(self, symbol: bytes, stateGame: Game):
        self.symbol = symbol
        self.stateGame = stateGame
        
    def minimax(self):
        print(self.stateGame.board)
        # Condiciones de Salida de Carrera
        if(self.stateGame.isDraw()): # Empate/Tablas
            return 0
        elif(self.stateGame.hasWinner(b'\x58')): # Victoria del Agente Humano
            return -1
        elif(self.stateGame.hasWinner(b'\x4f')): # Victoria del Agente AI
            return 1
        else:
            for row in range(3):
                for column in range(3):
                    if(self.stateGame.play(row, column) == 0):
                        return self.minimax()