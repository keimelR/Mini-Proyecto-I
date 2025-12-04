from typing import List

class Board:
    grids: List[List[bytes]]
    numberMarks: int
    MAX_ROW = 3
    MAX_COLUMN = 3
    
    SYMBOL_X = b'\x58'
    SYMBOL_O = b'\x4f'
    
    def __init__(self):
        self.grids = [
            [b'\x31', b'\x32', b'\x33'],
            [b'\x34', b'\x35', b'\x36'],
            [b'\x37', b'\x38', b'\x39']
        ]
        self.numberMarks = 0

    def __str__(self):
        stateBoard: str = str()
        for row in self.grids:
            for column in row:
                stateBoard += column.decode(encoding='utf-8') + " "
            stateBoard += '\n'
        return stateBoard
        
    def canMarkGrid(
        self, 
        row: int, 
        column: int
    ) -> int:
        if((row or column) >= self.MAX_ROW):
            # TODO. Row o Column superior a las 3 cuadriculas (Marco una cuadricula fuera del limite).
            return -1
        elif(self.grids[row][column] == self.SYMBOL_X or self.grids[row][column] == self.SYMBOL_O):
            # TODO: Marcar una cuadricula que estaba previamente marcada con X o O.
            return -2
        else:
            return 0
        
    def markGrid(
        self,
        mark: bytes,
        row: int,
        column: int
    ) -> int:
        res: int = self.canMarkGrid(row, column)
        if(res == 0):
            self.grids[row][column] = mark
            self.numberMarks = self.numberMarks + 1
        return res