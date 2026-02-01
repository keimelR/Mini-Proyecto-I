import numpy as np

from minimax import mejor_movimiento_IA


class TicTacToeBot:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.9):  # Alpha más alto al inicio
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

        # Solo exploramos si estamos entrenando
        if explorar and np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice(available_moves)
        else:
            q_values = self.q_table[state]
            masked_q = np.full(9, -np.inf)
            for move in available_moves:
                masked_q[move] = q_values[move]
            action = np.argmax(masked_q)

        self.last_tabla = state
        self.last_jugada = action
        return action

    def learn(self, current_board, recompensa, game_over):
        if self.last_tabla is None:
            return

        estado_actual = self.get_estado(current_board)
        if estado_actual not in self.q_table:
            self.q_table[estado_actual] = np.zeros(9)

        ultimo_q = self.q_table[self.last_tabla][self.last_jugada]

        if game_over:
            q_maximo_futuro = 0
        else:
            # IMPORTANTE: Aquí buscamos el valor del SIGUIENTE estado
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

    def entrenar_bot(self, bot: TicTacToeBot, episodes=20000):
        epsilon_start = 1.0
        epsilon_end = 0.05
        decay_step = (epsilon_start - epsilon_end) / episodes

        print(f"--- INICIANDO ENTRENAMIENTO PRO ({episodes} episodios) ---")
        print("Distribución: 20% Minimax | 20% Random | 60% Self-Play")
        print("Roles: 50% Jugador 1 (X) | 50% Jugador 2 (O)")

        for i in range(episodes):
            bot.epsilon = max(epsilon_end, bot.epsilon - decay_step)

            bot_player = 1 if random.random() < 0.5 else -1
            opp_player = -1 if bot_player == 1 else 1

            # 2. Definir Tipo de Oponente
            dice = random.random()
            if dice < 0.20:
                opponent_type = "minimax"
            elif dice < 0.40:
                opponent_type = "random"
            else:
                opponent_type = "self"

            board = [0] * 9
            game_over = False
            current_player = 1  # Siempre empieza el 1 (X)

            bot.last_tabla = None
            bot.last_jugada = None

            while not game_over:
                if current_player == bot_player:
                    action = bot.jugada_bot(board)
                    board[action] = current_player

                    # Verificar resultado
                    reward_abs, game_over = self.check_game_status(board)

                    bot_reward = reward_abs * bot_player

                    if game_over:
                        bot.learn(board, bot_reward, game_over)
                        break

                else:
                    if opponent_type == "minimax":
                        # Minimax juega como 'opp_player'
                        action_opp = mejor_movimiento_IA(opp_player, board)

                    elif opponent_type == "random":
                        avail_moves = [k for k, x in enumerate(board) if x == 0]
                        action_opp = random.choice(avail_moves)

                    else:  # SELF / SOMBRA
                        avail_moves = [k for k, x in enumerate(board) if x == 0]

                        # La Sombra explora o ataca
                        if random.random() < bot.epsilon:
                            action_opp = random.choice(avail_moves)
                        else:
                            state = bot.get_estado(board)
                            if state in bot.q_table:
                                q_vals = bot.q_table[state]
                                best_val_opp = float("inf")  # Buscamos el mínimo
                                best_move_opp = random.choice(avail_moves)

                                for move in avail_moves:
                                    if q_vals[move] < best_val_opp:
                                        best_val_opp = q_vals[move]
                                        best_move_opp = move
                                action_opp = best_move_opp
                            else:
                                action_opp = random.choice(avail_moves)

                    # Ejecutar jugada oponente
                    board[action_opp] = current_player

                    # Verificar resultado
                    reward_abs, game_over = self.check_game_status(board)
                    bot_reward = reward_abs * bot_player  # Ajuste de perspectiva

                    if game_over:
                        # Si el oponente gana o empata, el bot aprende
                        bot.learn(board, bot_reward, game_over)
                    else:
                        # Si el juego sigue, el bot actualiza su predicción
                        # basándose en cómo quedó el tablero tras el ataque enemigo
                        if bot.last_tabla is not None:
                            bot.learn(board, 0.0, False)

                # Cambiar turno
                current_player *= -1

            if i % 2000 == 0:
                print(
                    f"Episodio: {i}. Q-Table: {len(bot.q_table)}. Epsilon: {bot.epsilon:.4f} "
                    f"(Role: {'P1' if bot_player == 1 else 'P2'}, Rival: {opponent_type})"
                )

        bot.epsilon = 0
        print(f"--- Entrenamiento finalizado. Q-Table: {len(bot.q_table)} ---")


"""
class Entrenamiento:
    def entrenar_bot(self, bot: TicTacToeBot, episodes=20000):
        # Configuración de Epsilon
        epsilon_start = bot.epsilon  # Empieza 100% azar
        epsilon_end = 0.01  # Termina 1% azar
        decay_rate = 0.0005  # Controla qué tan rápido baja

        print(f"Entrenando al bot durante {episodes} partidas...")

        # Definición de las probabilidades de oponente
        opponent_probabilities = {
            "self": 0.50,
            "random": 0.30,
            "minimax": 0.20,
        }

        opponent_choices = list(opponent_probabilities.keys())
        opponent_weights = list(opponent_probabilities.values())

        for i in range(episodes):
            bot.epsilon = epsilon_end + (epsilon_start - epsilon_end) * np.exp(
                -decay_rate * i
            )

            board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            game_over = False
            current_player = 1

            while not game_over:
                if current_player == 1:
                    action = bot.jugada_bot(board)

                    board[action] = 1
                    reward, game_over = self.check_game_status(board)

                    if not game_over:
                        bot.learn(board, reward, game_over)

                else:
                    opponent_type = np.random.choice(
                        opponent_choices, p=opponent_weights
                    )

                    action = -1  # Inicializar acción del oponente

                    if opponent_type == "self":
                        available_moves = [
                            idx for idx, val in enumerate(board) if val == 0
                        ]
                        if available_moves:
                            action = np.random.choice(available_moves)

                    elif opponent_type == "random":
                        available_moves = [
                            idx for idx, val in enumerate(board) if val == 0
                        ]
                        if available_moves:
                            action = np.random.choice(available_moves)

                    elif opponent_type == "minimax":
                        action = mejor_movimiento_IA(-1, board)

                    if action != -1:  # Si se eligió una acción válida
                        board[action] = -1
                        reward, game_over = self.check_game_status(board)

                        if game_over:
                            bot.learn(board, reward, game_over)
                        else:
                            pass

                current_player *= -1
            if not game_over:
                pass

            if i % 1000 == 0:
                print(f"Episode: {i}. Epsilon: {bot.epsilon:.4f}")

        bot.epsilon = 0
        print(f"Entrenamiento finalizado. Epsilon final: {bot.epsilon}")

    def check_game_status(self, board):
        # Lógica de victoria (filas, columnas, diagonales)
        win_conditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],  # Horizontales
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],  # Verticales
            [0, 4, 8],
            [2, 4, 6],  # Diagonales
        ]

        for combo in win_conditions:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != 0:
                if board[combo[0]] == 1:  # Ganó el bot (Jugador 1)
                    return 1.0, True
                else:  # Ganó el humano/rival (Jugador -1)
                    return -1, True

        if 0 not in board:  # Empate
            return 0.5, True

        return (
            0,
            False,
        )
"""
