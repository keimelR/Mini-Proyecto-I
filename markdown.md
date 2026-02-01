# Descripción del Proyecto

Este proyecto implementa un agente autónomo para el juego **Tic-Tac-Toe** (Tres en Raya) utilizando el algoritmo **Q-Learning**, un método de aprendizaje por refuerzo. El objetivo es demostrar cómo un agente puede aprender estrategias óptimas mediante la interacción con el entorno, sin conocimiento previo de las reglas lógicas del juego, basándose únicamente en recompensas y castigos.

---

# Clases Principales

### `class TicTacToeBot`
Esta clase representa el cerebro del agente, gestionando la memoria de largo plazo a través de una tabla de valores Q.

* **Atributos:**
    * `q_table`: Diccionario que mapea los estados (tuplas del tablero) a los valores estimados de cada acción.
    * `alpha` ($\alpha$): Tasa de aprendizaje establecida en **0.5**.
    * `gamma` ($\gamma$): Factor de descuento establecido en **0.9**.
    * `epsilon` ($\epsilon$): Tasa de exploración inicial fijada en **0.9**.
    * `last_tabla`: Almacena el estado previo para la actualización de Bellman.
    * `last_jugada`: Almacena la última acción ejecutada.

* **Métodos Principales:**
    * `get_estado(board)`: Convierte el tablero (lista) a una tupla inmutable para indexar la `q_table`.
    * `jugada_bot(board, explorar=True)`: Selecciona una acción usando la política **$\epsilon$-greedy**:
        * Con probabilidad $\epsilon$: Selecciona una acción aleatoria (**exploración**).
        * Con probabilidad $1-\epsilon$: Selecciona la acción con el valor Q más alto (**explotación**).
    * `learn(current_board, recompensa, game_over)`: Actualiza los valores de la tabla utilizando la **Ecuación de Bellman**:

$$Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma \max_{a'} Q(s', a') - Q(s, a)]$$



---

### `class Entrenamiento`
Gestiona el ciclo de vida del aprendizaje y las estadísticas de rendimiento.

* **Atributos de Seguimiento:**
    * `victorias_bot`: Contador de partidas ganadas por el agente.
    * `derrotas_bot`: Contador de partidas perdidas.
    * `empates`: Contador de tablas.

* **Métodos Principales:**
    * `entrenar_bot(bot, episodes=20000)`: Ejecuta el ciclo de entrenamiento. 
        * **Decaimiento de $\epsilon$**: Se aplica una reducción exponencial para pasar de la exploración total a la explotación refinada:
            $$\epsilon = \epsilon_{final} + (\epsilon_{inicial} - \epsilon_{final}) \cdot e^{-decay\_rate \cdot episodio}$$
        * **Estrategia de Oponente**: Para un aprendizaje robusto, el bot se enfrenta a una mezcla de oponente aleatorio (30%) y algoritmo Minimax (70%).
    * `check_game_status(board)`: Define el sistema de gratificación del entorno:
        * **Bot gana**: $+1.0$
        * **Oponente gana**: $-10.0$
        * **Empate**: $+0.5$
        * **Juego continúa**: $-0.01$ (penalización por tiempo para fomentar victorias rápidas).

---

# Algoritmo Q-Learning Aplicado a Tic-Tac-Toe

### Representación del Estado
El tablero de $3 \times 3$ se representa como una lista plana de 9 elementos:
* `0`: Casilla vacía.
* `1`: Ficha del Bot.
* `-1`: Ficha del Oponente.



### Espacio de Acciones
El agente puede elegir entre 9 posiciones posibles (índices 0 a 8). El algoritmo filtra legalmente las jugadas para considerar únicamente las casillas con valor `0`.

### Hiperparámetros de Configuración

| Parámetro | Descripción |
| :--- | :--- |
| **$\alpha$ (alpha)** | **Tasa de aprendizaje**: Controla cuánto afecta la nueva información a los valores Q existentes. |
| **$\gamma$ (gamma)** | **Factor de descuento**: Determina la importancia de las recompensas futuras frente a las inmediatas. |
| **$\epsilon$ inicial** | Probabilidad máxima de realizar movimientos al azar al inicio. |
| **$\epsilon$ final** | Probabilidad mínima de exploración para mantener el aprendizaje activo. |
| **Decay rate** | Velocidad a la que el agente deja de explorar y comienza a confiar en su conocimiento. |