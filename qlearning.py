import time
import numpy as np
from minimax import mejor_movimiento_IA

class TicTacToeBot:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.9): # Alpha más alto al inicio
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
    def entrenar_bot(self, bot: TicTacToeBot, episodes=20000):
        # Configuración de Epsilon
        epsilon_start = bot.epsilon  # Empieza 100% azar
        epsilon_end = 0.01   # Termina 1% azar
        decay_rate = 0.0005  # Controla qué tan rápido baja
        
        print(f"Entrenando al bot durante {episodes} partidas...")
        
        for i in range(episodes):
            # Aplicamos la reducción gradual (Decaimiento Exponencial)
            bot.epsilon = epsilon_end + (epsilon_start - epsilon_end) * np.exp(-decay_rate * i)
            
            board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            game_over = False
            current_player = 1 if i % 2 == 0 else -1 
            
            while not game_over:
                if current_player == 1:
                    # TURNO DEL BOT (Aprendizaje activo)
                    action = bot.jugada_bot(board)
                    board[action] = 1
                    reward, game_over = self.check_game_status(board)
                    # El bot solo debe aprender de sus consecuencias
                    bot.learn(board, reward, game_over)
                else:
                    # TURNO DEL OPONENTE (Self-Play)
                    if np.random.random() < 0.3:
                        action = np.random.choice([idx for idx, val in enumerate(board) if val == 0])
                    else:
                        action = mejor_movimiento_IA(1, board)

                    
                    board[action] = -1
                    reward, game_over = self.check_game_status(board)
                    
                    # Si el oponente gana, el bot debe aprender que su jugada anterior fue MALA
                    if game_over:
                        bot.learn(board, reward, game_over)

                current_player *= -1
            if i % 100 == 0:
                print("Episode: " + str(i))

        bot.epsilon = 0 # IA lista para competir sin errores
        print(f"Entrenamiento finalizado. Epsilon final: {bot.epsilon}")

    def check_game_status(self, board):
        """
        Función auxiliar para el entrenamiento.
        Retorna (recompensa, terminado)
        """
        # Lógica de victoria (filas, columnas, diagonales)
        win_conditions = [
            [0,1,2], [3,4,5], [6,7,8], # Horizontales
            [0,3,6], [1,4,7], [2,5,8], # Verticales
            [0,4,8], [2,4,6]           # Diagonales
        ]
        
        for combo in win_conditions:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != 0:
                if board[combo[0]] == 1: # Ganó el bot
                    return 1.0, True
                else: # Ganó el humano/rival
                    return -10.0, True
                    
        if 0 not in board: # Empate
            return 0.5, True # Pequeña recompensa por no perder
            
        return -0.01, False # El juego sigue