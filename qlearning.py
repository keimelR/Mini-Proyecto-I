import numpy as np

class TicTacToeBot:
    def __init__(self, alpha=0.3, gamma=0.9, epsilon=0.1):
        self.q_table = {}   # Memoria del bot
        self.alpha = alpha   # Tasa de aprendizaje
        self.gamma = gamma   # Descuento de recompensas futuras
        self.epsilon = epsilon # Probabilidad de explorar (azar)
        
        self.last_tabla = None
        self.last_jugada = None

    def get_estado(self, board):
        # Convertimos tu lista boardState en una tupla para que sea usable como llave
        return tuple(board)

    def jugada_bot(self, board):
        state = self.get_estado(board)
        
        # Si no conocemos este estado, inicializamos sus 9 movimientos en 0.0
        if state not in self.q_table:
            self.q_table[state] = np.zeros(9)

        # Identificar casillas vacías (donde tu boardState tiene un 0)
        available_moves = [i for i, val in enumerate(board) if val == 0]

        # Decisión: ¿Explorar (azar) o Explotar (mejor movimiento)?
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice(available_moves)
        else:
            # Buscamos el valor máximo solo entre las casillas disponibles
            q_values = self.q_table[state]
            # Llenamos las casillas ocupadas con un valor muy bajo para que no las elija
            masked_q = np.full(9, -np.inf)
            for move in available_moves:
                masked_q[move] = q_values[move]
            action = np.argmax(masked_q)

        self.last_tabla = state
        self.last_jugada = action
        return action

    def learn(self, current_board, recompensa, game_over):
        """
        Ajusta la Q-Table usando la recompensa recibida.
        """
        if self.last_tabla is None:
            return

        estado = self.get_estado(current_board)
        if estado not in self.q_table:
            self.q_table[estado] = np.zeros(9)

        # Valor Q que queremos actualizar
        ultimo_q = self.q_table[self.last_tabla][self.last_jugada]
        
        # Valor máximo futuro
        if game_over:
            q_maximo_futuro = 0 # No hay más movimientos
        else:
            q_maximo_futuro = np.max(self.q_table[estado])

        # Fórmula de Q-Learning (Ecuación de Bellman)
        nuevo_q = ultimo_q + self.alpha * (recompensa + self.gamma * q_maximo_futuro - ultimo_q)
        self.q_table[self.last_tabla][self.last_jugada] = nuevo_q

class Entrenamiento:
    def entrenar_bot(self, bot: TicTacToeBot, episodes=20000):
        print(f"Entrenando al bot durante {episodes} partidas...")
        
        for i in range(episodes):
            # 1. Reiniciar tablero para nueva partida
            board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            game_over = False
            
            # Alternar quién empieza para que aprenda ambas posiciones
            current_player = 1 if i % 2 == 0 else -1 
            
            while not game_over:
                available_moves = [idx for idx, val in enumerate(board) if val == 0]
                
                if not available_moves:
                    break

                if current_player == 1:
                    # TURNO DEL BOT
                    action = bot.jugada_bot(board)
                    board[action] = 1
                    
                    # Verificar si ganó tras su movimiento
                    reward, game_over = self.check_game_status(board)
                    bot.learn(board, reward, game_over)
                else:
                    # TURNO DEL OPONENTE (Simulamos un jugador aleatorio o con estrategia)
                    # Es importante que el bot aprenda de las consecuencias de los actos del rival
                    action = np.random.choice(available_moves)
                    board[action] = -1
                    
                    # Verificar si el oponente ganó
                    reward, game_over = self.check_game_status(board)
                    # Si el rival gana, el bot recibe recompensa negativa por su acción anterior
                    if game_over:
                        bot.learn(board, reward, game_over)

                current_player *= -1 # Cambio de turno

        print("Entrenamiento finalizado.")

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
                    return -1.0, True
                    
        if 0 not in board: # Empate
            return 0.1, True # Pequeña recompensa por no perder
            
        return 0.0, False # El juego sigue