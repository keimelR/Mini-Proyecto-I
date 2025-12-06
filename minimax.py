from bigtree import Node

# Los players son PLAYER y la IA es 1

PLAYER = -1
IA = 1
VACIO = 0

#  -----------
# | 0 | 1 | 2 |
# | 3 | 4 | 5 |
# | 6 | 7 | 8 |
#  -----------
tablero_actual: list[int] = [0,0,0,0,0,0,0,0,0] # Del index 0 al 2 es la fila 1, del index 3 al 5 la fila 2 y del index 6 al 8 la 3

nodo_raiz = Node("a", tablero=tablero_actual.copy())

def minimax(tablero: list[int], nodo_padre: Node, turno: int, profundidad: int):
    analisis_victoria = detectar_victoria(tablero)
    if analisis_victoria != 0 or not any(x == VACIO for x in tablero):
        nodo_padre.set_attrs({"tablero": tablero.copy(), "profundidad": profundidad, "victoria": analisis_victoria})
        return (analisis_victoria)
    
    if turno == PLAYER:
        mejor_puntaje = float('inf')
        for i in range(9):
            if tablero[i] == VACIO:
                tablero[i] = PLAYER
                nodo_actual = Node(i, tablero=tablero.copy(), profundidad=profundidad, parent=nodo_padre)
                
                resultado = minimax(tablero, nodo_actual, IA, profundidad=profundidad + 1)
                
                tablero[i] = VACIO
                mejor_puntaje = min(mejor_puntaje, resultado)
        return mejor_puntaje
    
    elif turno == IA:
        mejor_puntaje = -float('inf')
        for i in range(9):
            if tablero[i] == VACIO:
                tablero[i] = IA
                
                nodo_actual = Node(i, tablero=tablero.copy(),profundidad=profundidad, parent=nodo_padre)
                resultado = minimax(tablero, nodo_actual, PLAYER, profundidad + 1)
                
                tablero[i] = VACIO
                mejor_puntaje = max(mejor_puntaje, resultado)
        return mejor_puntaje
    else:
        print("Esto no deberia de pasar WTF")
        exit()

# Funcion recursiva, debe de devolver la mejor jugada que puede realizar la IA, el valor a devolver es un int
def mejor_movimiento_IA(tablero: list[int]):
    mejor_puntaje = -float('inf')
    mejor_movimiento = -1
    for i in range(9):
        if tablero[i] == VACIO:
            tablero[i] = IA
            
            nodo_actual = Node(i, tablero=tablero.copy(), profundidad=0, parent=nodo_raiz)
            
            resultado = minimax(tablero, nodo_actual, PLAYER, n_turno)
                
            tablero[i] = VACIO
            
            if resultado > mejor_puntaje:
                mejor_movimiento = i
                mejor_puntaje = resultado
    return mejor_movimiento
        

def detectar_victoria(tablero: list[int]):
    analisis_horizontal = detectar_lineas_horizontales(tablero)
    analisis_vertical = detectar_lineas_verticales(tablero)
    analisis_diagonal = detectar_lineas_diagonales(tablero)
    
    if analisis_horizontal == PLAYER or analisis_vertical == PLAYER or analisis_diagonal == PLAYER:
        return PLAYER
    
    if analisis_horizontal == IA or analisis_vertical == IA or analisis_diagonal == IA:
        return IA
    
    return VACIO

def detectar_lineas_horizontales(tablero: list[int]):
    if (tablero[0] == PLAYER and tablero[1] == PLAYER and tablero[2] == PLAYER) or (tablero[3] == PLAYER and tablero[4] == PLAYER and tablero[5] == PLAYER) or (tablero[6] == PLAYER and tablero[7] == PLAYER and tablero[8] == PLAYER):
        return PLAYER
    
    if (tablero[0] == IA and tablero[1] == IA and tablero[2] == IA) or (tablero[3] == IA and tablero[4] == IA and tablero[5] == IA) or (tablero[6] == IA and tablero[7] == IA and tablero[8] == IA):
        return IA
    
    return VACIO

def detectar_lineas_verticales(tablero: list[int]):
    if (tablero[0] == PLAYER and tablero[3] == PLAYER and tablero[6] == PLAYER) or (tablero[1] == PLAYER and tablero[4] == PLAYER and tablero[7] == PLAYER) or (tablero[2] == PLAYER and tablero[5] == PLAYER and tablero[8] == PLAYER):
        return PLAYER
    
    if (tablero[0] == IA and tablero[3] == IA and tablero[6] == IA) or (tablero[1] == IA and tablero[4] == IA and tablero[7] == IA) or (tablero[2] == IA and tablero[5] == IA and tablero[8] == IA):
        return IA
    
    return VACIO

def detectar_lineas_diagonales(tablero: list[int]):
    if (tablero[0] == PLAYER and tablero[4] == PLAYER and tablero[8] == PLAYER) or (tablero[2] == PLAYER and tablero[4] == PLAYER and tablero[6] == PLAYER):
        return PLAYER
    
    if (tablero[0] == IA and tablero[4] == IA and tablero[8] == IA) or (tablero[2] == IA and tablero[4] == IA and tablero[6] == IA):
        return IA
    
    return VACIO

def imprimir_tablero(tablero: list[int]):
    for i in range(9):
        casilla = i + 1 if tablero[i] == VACIO else tablero[i]
        
        if i % 3 == 0:
            print("\n-------------")
            print(f"| ", end="")
        
        
        if i == 8:
            print(casilla, end=" |\n")
        else:
            print(casilla, end=" | ")
            
    print("-------------")

def main():
    
    global turno_actual
    turno_actual = PLAYER
    global n_turno
    n_turno = 0
    
    while True:
        victoria = detectar_victoria(tablero_actual)
        
        if not any(x == VACIO for x in tablero_actual):
            print("La partida ha terminado, no hay ganador")
            imprimir_tablero(tablero_actual)
            return
        
        if victoria != VACIO:
            imprimir_tablero(tablero_actual)
        
        if victoria == PLAYER:
            print(f"*******************************\nEl jugador ha ganado en {n_turno} turnos\n********************************")
            return
        if victoria == IA:
            print(f"*******************************\nEl ordenador ha ganado en {n_turno} turnos\n********************************")
            return
        n_turno += 1
        
        
        print(f"Turno actual: {"PLAYER" if turno_actual == PLAYER else "IA"}")
        print(f"Número de turnos: {n_turno}")
        
        if turno_actual == PLAYER:
            print("Turno del jugador")
            
            imprimir_tablero(tablero_actual)
            
            casilla = -1
            while True:
                casilla = int(input("Escriba donde quiere introducir su movimiento: "))
                
                if casilla < 1 or casilla > 9 or tablero_actual[casilla - 1] != VACIO:
                    print("El valor introducido no es válido, la casilla ya esta ocupada o no existe")
                    continue
                else:
                    break
            
            tablero_actual[casilla - 1] = PLAYER
            
        if turno_actual == IA:
            print("Turno de la IA")
            
            casilla = mejor_movimiento_IA(tablero_actual)
            nodo_raiz.show(attr_list=["tablero", "profundidad", "victoria"])
            input("")
            imprimir_tablero(tablero_actual)
            tablero_actual[casilla] = IA
        
        turno_actual = IA if turno_actual == PLAYER else PLAYER

if __name__ == "__main__":
    main()