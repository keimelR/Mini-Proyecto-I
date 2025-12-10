from bigtree import Node
from constantes import *
# Los players son PLAYER y la IA es 1

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
                nodo_actual = Node(str(profundidad) + str(i), tablero=tablero.copy(), profundidad=profundidad, parent=nodo_padre, jugador=PLAYER)
                
                resultado = minimax(tablero, nodo_actual, IA, profundidad=profundidad + 1)
                
                tablero[i] = VACIO
                mejor_puntaje = min(mejor_puntaje, resultado)
        return mejor_puntaje
    
    elif turno == IA:
        mejor_puntaje = -float('inf')
        for i in range(9):
            if tablero[i] == VACIO:
                tablero[i] = IA
                
                nodo_actual = Node(str(profundidad) + str(i), tablero=tablero.copy(),profundidad=profundidad, parent=nodo_padre, jugador=IA)
                resultado = minimax(tablero, nodo_actual, PLAYER, profundidad + 1)
                
                tablero[i] = VACIO
                mejor_puntaje = max(mejor_puntaje, resultado)
        return mejor_puntaje
    else:
        print("Esto no deberia de pasar WTF")
        exit()

# Funcion recursiva, debe de devolver la mejor jugada que puede realizar la IA, el valor a devolver es un int
def mejor_movimiento_IA(profundidad: int, nodo_raiz: Node):
    mejor_puntaje = -float('inf')
    mejor_movimiento = -1
    
    tablero = nodo_raiz.get_attr("tablero")
    
    for i in range(9):
        if tablero[i] == VACIO:
            tablero[i] = IA
            
            nodo_actual = Node(str(profundidad) + str(i), tablero=tablero.copy(), profundidad=profundidad, parent=nodo_raiz, jugador=IA)
            
            resultado = minimax(tablero, nodo_actual, PLAYER, profundidad)
                
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