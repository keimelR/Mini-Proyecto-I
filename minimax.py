import math

from bigtree import Node

from constantes import *


# Los players son PLAYER y la IA es 1 (Asumiendo que IA=1 y PLAYER=-1 para Minimax)
def check_winner_minimax(board):
    wins = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),  # Horizontales
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),  # Verticales
        (0, 4, 8),
        (2, 4, 6),  # Diagonales
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] and board[a] != VACIO:
            return board[a]
    return None


def minimax(board, depth, is_maximizing, alpha, beta):
    winner = check_winner_minimax(board)

    # --- CASOS BASE ---
    if winner == 1:
        return 10 - depth  # Gana X (Preferimos ganar rápido)
    if winner == -1:
        return -10 + depth  # Gana O (Preferimos perder lento)
    if VACIO not in board:
        return 0  # Empate

    # --- RECURSIÓN CON PODA ---
    if is_maximizing:  # Turno de 1 (X)
        max_eval = -math.inf
        for i in range(9):
            if board[i] == VACIO:
                board[i] = 1
                eval = minimax(board, depth + 1, False, alpha, beta)
                board[i] = VACIO
                max_eval = max(max_eval, eval)

                # PODA ALFA
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval

    else:  # Turno de -1 (O)
        min_eval = math.inf
        for i in range(9):
            if board[i] == VACIO:
                board[i] = -1
                eval = minimax(board, depth + 1, True, alpha, beta)
                board[i] = VACIO
                min_eval = min(min_eval, eval)

                # PODA BETA
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval


def mejor_movimiento_IA(player, board):
    """
    Encuentra el mejor movimiento para 'player' usando Minimax con Poda Alfa-Beta.
    player: 1 o -1
    board: lista de 9 enteros
    """
    best_score = -math.inf if player == 1 else math.inf
    best_move = -1

    # Inicializamos alfa y beta
    alpha = -math.inf
    beta = math.inf

    # Validamos movimientos disponibles
    available_moves = [i for i, x in enumerate(board) if x == VACIO]

    # Si es el primer movimiento del juego, jugar al centro o esquina ahorra cómputo
    if len(available_moves) == 9:
        return 4  # Centro
    if len(available_moves) == 8 and board[4] == VACIO:
        return 4  # Tomar centro si está libre

    for move in available_moves:
        board[move] = player

        if player == 1:
            # Si soy 1, el siguiente turno es de -1 (Minimizing)
            score = minimax(board, 0, False, alpha, beta)
            board[move] = VACIO

            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)

        else:
            score = minimax(board, 0, True, alpha, beta)
            board[move] = VACIO

            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)

    return best_move


"""
def minimax(tablero, turno, alfa, beta):
    # 1. Comprobar estado terminal
    analisis_victoria = detectar_victoria(tablero)
    if analisis_victoria != 0:
        return analisis_victoria
    if VACIO not in tablero:
        return 0 # Empate

    if turno == IA:
        mejor_puntaje = -float('inf')
        for i in range(9):
            if tablero[i] == VACIO:
                tablero[i] = IA
                # Pasamos alfa y beta a la llamada recursiva
                resultado = minimax(tablero, PLAYER, alfa, beta)
                tablero[i] = VACIO
                mejor_puntaje = max(mejor_puntaje, resultado)
                alfa = max(alfa, mejor_puntaje)
                if beta <= alfa:
                    break # Poda
        return mejor_puntaje

    else: # Turno del PLAYER
        mejor_puntaje = float('inf')
        for i in range(9):
            if tablero[i] == VACIO:
                tablero[i] = PLAYER
                # Pasamos alfa y beta a la llamada recursiva
                resultado = minimax(tablero, IA, alfa, beta)
                tablero[i] = VACIO
                mejor_puntaje = min(mejor_puntaje, resultado)
                beta = min(beta, mejor_puntaje)
                if beta <= alfa:
                    break # Poda
        return mejor_puntaje

def mejor_movimiento_IA(profundidad, tablero):
    mejor_puntaje = -float('inf')
    mejor_movimiento = -1

    # Valores iniciales para la poda
    alfa = -float('inf')
    beta = float('inf')

    for i in range(9):
        if tablero[i] == VACIO:
            tablero[i] = IA
            # Llamada inicial con alfa y beta
            resultado = minimax(tablero, PLAYER, alfa, beta)
            tablero[i] = VACIO

            if resultado > mejor_puntaje:
                mejor_puntaje = resultado
                mejor_movimiento = i
    return mejor_movimiento
"""


def recorrer_arbol_de_nodos(nodo_raiz: Node, profundidad: int, turno: int):
    """
    Recorre el árbol, construye los nodos y asigna el valor Minimax a cada nodo.
    """
    nodo_actual = nodo_raiz
    tablero = nodo_actual.get_attr("tablero")

    analisis_victoria = detectar_victoria(tablero)

    # Caso Base: Victoria o Empate (Hoja del árbol)
    if analisis_victoria != 0 or not any(x == VACIO for x in tablero):
        # El puntaje es el resultado de la victoria/derrota/empate (0)
        score = analisis_victoria

        # Asignamos el valor Minimax al nodo hoja
        nodo_raiz.set_attrs(
            {
                "tablero": tablero.copy(),
                "profundidad": profundidad,
                "victoria": analisis_victoria,
                "minimax_value": score,  # <--- Valor asignado
            }
        )
        return score

    if turno == PLAYER:
        # Minimizador
        mejor_puntaje = float("inf")
        for i in range(9):
            if tablero[i] == VACIO:
                tablero[i] = PLAYER

                # Crear el nodo hijo
                nodo_actual = Node(
                    str(profundidad) + str(i),
                    tablero=tablero.copy(),
                    profundidad=profundidad,
                    parent=nodo_raiz,
                    jugador=PLAYER,
                )

                # Llamada recursiva (obtiene el valor Minimax del hijo)
                resultado = recorrer_arbol_de_nodos(
                    nodo_actual, profundidad=profundidad + 1, turno=IA
                )

                tablero[i] = VACIO
                mejor_puntaje = min(mejor_puntaje, resultado)

        # Asignamos el valor Minimax al nodo actual (Minimizador)
        nodo_raiz.set_attrs({"minimax_value": mejor_puntaje})  # <--- Valor asignado
        return mejor_puntaje

    elif turno == IA:
        # Maximizador
        mejor_puntaje = -float("inf")
        for i in range(9):
            if tablero[i] == VACIO:
                tablero[i] = IA

                # Crear el nodo hijo
                nodo_actual = Node(
                    str(profundidad) + str(i),
                    tablero=tablero.copy(),
                    profundidad=profundidad,
                    parent=nodo_raiz,
                    jugador=IA,
                )

                # Llamada recursiva (obtiene el valor Minimax del hijo)
                resultado = recorrer_arbol_de_nodos(
                    nodo_actual, profundidad + 1, turno=PLAYER
                )

                tablero[i] = VACIO
                mejor_puntaje = max(mejor_puntaje, resultado)

        # Asignamos el valor Minimax al nodo actual (Maximizador)
        nodo_raiz.set_attrs({"minimax_value": mejor_puntaje})  # <--- Valor asignado
        return mejor_puntaje
    else:
        print("Esto no deberia de pasar WTF")
        exit()


def cargar_arbol_de_nodos(nodo_raiz: Node, profundidad: int):
    """
    Inicia la construcción del árbol desde los hijos del nodo raíz y asigna el valor Minimax
    al nodo raíz.
    """
    mejor_puntaje = -float("inf")
    mejor_movimiento = -1

    tablero = nodo_raiz.get_attr("tablero")

    for i in range(9):
        if tablero[i] == VACIO:
            tablero[i] = PLAYER

            # Crear el nodo hijo
            nodo_actual = Node(
                str(profundidad) + str(i),
                tablero=tablero.copy(),
                profundidad=profundidad,
                parent=nodo_raiz,
                jugador=PLAYER,
            )

            # La llamada recursiva construye el subárbol y asigna valores
            resultado = recorrer_arbol_de_nodos(nodo_actual, profundidad + 1, IA)

            tablero[i] = VACIO

            if resultado > mejor_puntaje:
                mejor_movimiento = i
                mejor_puntaje = resultado

    # Asignamos el valor Minimax al nodo raíz
    nodo_raiz.set_attrs({"minimax_value": mejor_puntaje})  # <--- Valor asignado
    return mejor_movimiento


def detectar_victoria(tablero: list[int]):
    analisis_horizontal = detectar_lineas_horizontales(tablero)
    analisis_vertical = detectar_lineas_verticales(tablero)
    analisis_diagonal = detectar_lineas_diagonales(tablero)

    if (
        analisis_horizontal == PLAYER
        or analisis_vertical == PLAYER
        or analisis_diagonal == PLAYER
    ):
        return PLAYER

    if analisis_horizontal == IA or analisis_vertical == IA or analisis_diagonal == IA:
        return IA

    return VACIO


def detectar_lineas_horizontales(tablero: list[int]):
    if (
        (tablero[0] == PLAYER and tablero[1] == PLAYER and tablero[2] == PLAYER)
        or (tablero[3] == PLAYER and tablero[4] == PLAYER and tablero[5] == PLAYER)
        or (tablero[6] == PLAYER and tablero[7] == PLAYER and tablero[8] == PLAYER)
    ):
        return PLAYER

    if (
        (tablero[0] == IA and tablero[1] == IA and tablero[2] == IA)
        or (tablero[3] == IA and tablero[4] == IA and tablero[5] == IA)
        or (tablero[6] == IA and tablero[7] == IA and tablero[8] == IA)
    ):
        return IA

    return VACIO


def detectar_lineas_verticales(tablero: list[int]):
    if (
        (tablero[0] == PLAYER and tablero[3] == PLAYER and tablero[6] == PLAYER)
        or (tablero[1] == PLAYER and tablero[4] == PLAYER and tablero[7] == PLAYER)
        or (tablero[2] == PLAYER and tablero[5] == PLAYER and tablero[8] == PLAYER)
    ):
        return PLAYER

    if (
        (tablero[0] == IA and tablero[3] == IA and tablero[6] == IA)
        or (tablero[1] == IA and tablero[4] == IA and tablero[7] == IA)
        or (tablero[2] == IA and tablero[5] == IA and tablero[8] == IA)
    ):
        return IA

    return VACIO


def detectar_lineas_diagonales(tablero: list[int]):
    if (tablero[0] == PLAYER and tablero[4] == PLAYER and tablero[8] == PLAYER) or (
        tablero[2] == PLAYER and tablero[4] == PLAYER and tablero[6] == PLAYER
    ):
        return PLAYER

    if (tablero[0] == IA and tablero[4] == IA and tablero[8] == IA) or (
        tablero[2] == IA and tablero[4] == IA and tablero[6] == IA
    ):
        return IA

    return VACIO
