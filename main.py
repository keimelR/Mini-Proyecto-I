import random
import time

import numpy as np

# Asegúrate de tener minimax.py en la misma carpeta o define la función aquí
try:
    from minimax import mejor_movimiento_IA
except ImportError:
    # Si no tienes el archivo, aquí pongo un dummy para que el código corra
    def mejor_movimiento_IA(player, board):
        avail = [i for i, x in enumerate(board) if x == 0]
        return random.choice(avail) if avail else None


def get_available_moves(board):
    return [i for i, val in enumerate(board) if val == 0]


class TicTacToeBot:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=1.0):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.last_tabla = None
        self.last_jugada = None

    def get_estado(self, board):
        return tuple(board)

    def jugada_bot(self, board, explorar=True):
        state = self.get_estado(board)
        if state not in self.q_table:
            self.q_table[state] = np.zeros(9)

        available_moves = [i for i, val in enumerate(board) if val == 0]

        # Exploración (Random)
        if explorar and np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice(available_moves)
        # Explotación (Mejor Q)
        else:
            q_values = self.q_table[state]
            masked_q = np.full(9, -np.inf)
            for move in available_moves:
                masked_q[move] = q_values[move]
            action = np.argmax(masked_q)

        # Guardamos el estado y la acción para aprender MÁS TARDE
        self.last_tabla = state
        self.last_jugada = action
        return action

    def learn(self, current_board, recompensa, game_over):
        """
        Actualiza la Q-Table basándose en la última jugada realizada (self.last_tabla)
        y el estado actual del tablero (current_board).
        """
        if self.last_tabla is None:
            return

        estado_actual = self.get_estado(current_board)
        if estado_actual not in self.q_table:
            self.q_table[estado_actual] = np.zeros(9)

        # Q(S, A) actual
        ultimo_q = self.q_table[self.last_tabla][self.last_jugada]

        # Max Q(S', a')
        if game_over:
            q_maximo_futuro = 0
        else:
            q_maximo_futuro = np.max(self.q_table[estado_actual])

        # Ecuación de Bellman
        self.q_table[self.last_tabla][self.last_jugada] += self.alpha * (
            recompensa + self.gamma * q_maximo_futuro - ultimo_q
        )


class Entrenamiento:
    def check_game_status(self, board):
        """
        Retorna (recompensa, terminado)
        """
        win_conditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]

        for combo in win_conditions:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != 0:
                if board[combo[0]] == 1:
                    return 1.0, True  # Ganó el Bot
                else:
                    return -1.0, True  # Ganó Minimax

        if 0 not in board:
            return (
                0.5,
                True,
            )

        return 0.0, False

    def entrenar_bot(self, bot: TicTacToeBot, episodes=10000):
        epsilon_start = 1.0
        epsilon_end = 0.05  # Dejar un poco de exploración siempre es bueno
        decay_step = (epsilon_start - epsilon_end) / episodes

        print(f"--- INICIANDO ENTRENAMIENTO ({episodes} episodios) ---")

        for i in range(episodes):
            bot.epsilon = max(epsilon_end, bot.epsilon - decay_step)

            board = [0] * 9
            game_over = False

            while not game_over:
                # --- TURNO BOT ---
                action = bot.jugada_bot(board)
                board[action] = 1

                reward, game_over = self.check_game_status(board)

                if game_over:
                    # Si el bot gana con su movimiento, aprende y termina
                    bot.learn(board, reward, game_over)
                    break

                action_opp = mejor_movimiento_IA(-1, board)
                board[action_opp] = -1

                reward, game_over = self.check_game_status(board)

                if game_over:
                    bot.learn(board, reward, game_over)
                else:
                    bot.learn(board, 0.0, False)

            if i % 1000 == 0:
                print(
                    f"Episodio: {i}. Q-Table size: {len(bot.q_table)}. Epsilon: {bot.epsilon:.4f}"
                )

        bot.epsilon = 0
        print("--- Entrenamiento finalizado ---")


def display_board(board):
    """
    Muestra el tablero.
    Si la casilla está vacía (0), muestra su número de índice (0-8).
    Si está ocupada, muestra X (Bot) u O (Humano).
    """
    display_chars = []
    for i, val in enumerate(board):
        if val == 1:
            display_chars.append("X")  # Bot
        elif val == -1:
            display_chars.append("O")  # Humano
        else:
            display_chars.append(str(i))  # Número de guía para casilla vacía

    print(f"\n {display_chars[0]} | {display_chars[1]} | {display_chars[2]} ")
    print("---+---+---")
    print(f" {display_chars[3]} | {display_chars[4]} | {display_chars[5]} ")
    print("---+---+---")
    print(f" {display_chars[6]} | {display_chars[7]} | {display_chars[8]} \n")


def play_interactive_game(bot: TicTacToeBot):
    """Juego interactivo infinito hasta que el usuario decida salir."""
    bot.epsilon = 0  # Modo Dios (Sin explorar, usa solo lo aprendido)
    judge = Entrenamiento()  # Instancia para verificar ganadores

    print("\n=============================================")
    print("   ¡BIENVENIDO AL TIC-TAC-TOE VS IA!")
    print("=============================================")
    print(" -> Tú eres 'O'")
    print(" -> La IA es 'X'")
    print(" -> Introduce el número que ves en el tablero para mover.")

    playing = True

    while playing:
        board = [0] * 9
        game_over = False

        # Puedes cambiar esto para decidir quién empieza
        # 1 = Bot empieza, -1 = Humano empieza
        # Por defecto alternamos o dejamos fijo al Bot para probar su defensa
        current_player = 1

        print("\n--- NUEVA PARTIDA ---")
        if current_player == 1:
            print(">> Empieza la IA (X).")
        else:
            print(">> Empiezas tú (O).")

        while not game_over:
            display_board(board)

            if current_player == 1:
                # Turno del Bot
                print("Pensando...")
                time.sleep(0.5)  # Pequeña pausa para darle realismo
                action = bot.jugada_bot(board, explorar=False)
                board[action] = 1
                print(f"La IA marcó la casilla {action}")
            else:
                # Turno del Humano
                valid = False
                while not valid:
                    try:
                        user_input = input("Tu turno (elige un número disponible): ")
                        move = int(user_input)

                        if 0 <= move <= 8:
                            if board[move] == 0:
                                board[move] = -1
                                valid = True
                            else:
                                print(
                                    f"¡La casilla {move} ya está ocupada! Elige otra."
                                )
                        else:
                            print("Por favor, ingresa un número entre 0 y 8.")
                    except ValueError:
                        print("Entrada inválida. Debes ingresar un número entero.")

            # Verificar estado del juego
            reward, game_over = judge.check_game_status(board)

            if game_over:
                display_board(board)
                if reward == 1.0:
                    print("RESULTADO: ¡La IA (X) ha ganado!")
                elif reward == -1.0:
                    print("RESULTADO: ¡Felicidades! Has ganado (O).")
                else:
                    print("RESULTADO: ¡Es un Empate!")

            # Cambiar turno
            current_player *= -1

        # --- Fin de la partida actual, preguntar si repetir ---
        reponse = input("\n¿Quieres jugar otra vez? (s/n): ").lower()
        if reponse != "s" and reponse != "si" and reponse != "y":
            playing = False
            print("\n¡Gracias por jugar! Cerrando...")


if __name__ == "__main__":
    # Aumenté un poco los episodios porque Minimax es un maestro estricto
    bot = TicTacToeBot(alpha=0.5, gamma=0.7, epsilon=1.0)
    trainer = Entrenamiento()
    trainer.entrenar_bot(bot, episodes=20000)

    play_interactive_game(bot)
