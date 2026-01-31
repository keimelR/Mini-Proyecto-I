import json
import pygame
import threading
import time
from qlearning import TicTacToeBot

class TrainingForm:
    def __init__(self, screen, bot, font):
        self.screen = screen
        self.bot = bot
        self.font = font
        from qlearning import Entrenamiento
        self.entrenador = Entrenamiento()
        
        self.is_open = False
        self.is_training = False 
        self.dots = ""
        self.last_dot_update = time.time()
        
        # Ajuste de tamaño para el nuevo campo
        self.form_rect = pygame.Rect(
            self.screen.get_width() // 2 - 200, 
            self.screen.get_height() // 2 - 180, 
            400, 360
        )
        
        self.background_color = (45, 45, 45)
        self.text_color = (255, 255, 255)
        self.accent_color = (0, 173, 181)
        self.input_bg = (80, 80, 80)
        
        self.input_fields = {
            "alpha": {"rect": pygame.Rect(0, 0, 140, 30), "text": str(self.bot.alpha), "active": False},
            "gamma": {"rect": pygame.Rect(0, 0, 140, 30), "text": str(self.bot.gamma), "active": False},
            "epsilon": {"rect": pygame.Rect(0, 0, 140, 30), "text": str(self.bot.epsilon), "active": False},
            "episodes": {"rect": pygame.Rect(0, 0, 140, 30), "text": "20000", "active": False}, # Nuevo
        }
        
        self.apply_button = {"rect": pygame.Rect(0, 0, 120, 40), "text": "Entrenar"}
        self.close_button = {"rect": pygame.Rect(0, 0, 100, 40), "text": "Cerrar"}
        self._setup_layout()

    def _setup_layout(self):
        y_offset = self.form_rect.top + 75
        for field in self.input_fields.values():
            field["rect"].x = self.form_rect.centerx + 10
            field["rect"].y = y_offset
            y_offset += 45
        
        self.apply_button["rect"].midtop = (self.form_rect.centerx - 70, self.form_rect.bottom - 65)
        self.close_button["rect"].midtop = (self.form_rect.centerx + 70, self.form_rect.bottom - 65)

    def guardar_conocimiento(bot: TicTacToeBot, filename="q_table.json"):
        # Convertimos las llaves (tuplas) a strings para que JSON las acepte
        data_to_save = {str(key): value.tolist() for key, value in bot.q_table.items()}
        with open(filename, "w") as f:
            json.dump(data_to_save, f, indent=4)
        print(f"Tabla Q guardada en {filename}")

    def _run_training_worker(self):
        try:
            self.bot.alpha = float(self.input_fields["alpha"]["text"])
            self.bot.gamma = float(self.input_fields["gamma"]["text"])
            self.bot.epsilon = float(self.input_fields["epsilon"]["text"])
            
            # Validación simple para episodios
            ep_text = self.input_fields["episodes"]["text"]
            num_episodes = int(ep_text) if ep_text.isdigit() else 20000
            
            self.entrenador.entrenar_bot(self.bot, episodes=num_episodes)
            
            # self.guardar_conocimiento(self.bot)
        except Exception as e:
            print(f"Error en entrenamiento: {e}")
        
        self.is_training = False
        self.is_open = False 

    def _apply_changes(self):
        if not self.is_training:
            self.is_training = True
            self.dots = "" 
            self.last_dot_update = time.time()
            threading.Thread(target=self._run_training_worker, daemon=True).start()

    def update_animation(self):
        ahora = time.time()
        if ahora - self.last_dot_update > 0.4:
            self.dots = "." * ((len(self.dots) % 3) + 1)
            self.last_dot_update = ahora

    def draw(self):
        if not self.is_open: return

        # Fondo y Borde
        pygame.draw.rect(self.screen, (20, 20, 20), self.form_rect.move(5, 5), border_radius=10) 
        pygame.draw.rect(self.screen, self.background_color, self.form_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.accent_color, self.form_rect, width=2, border_radius=10)

        titulo = self.font.render("Configuración de IA", True, self.accent_color)
        self.screen.blit(titulo, (self.form_rect.x + 20, self.form_rect.y + 20))

        if self.is_training:
            self.update_animation() 
            txt_surf = self.font.render(f"Entrenando el bot{self.dots}", True, (255, 255, 255))
            txt_rect = txt_surf.get_rect(center=(self.form_rect.centerx, self.form_rect.top + 140))
            self.screen.blit(txt_surf, txt_rect)
            
            bar_x, bar_y = self.form_rect.centerx - 100, self.form_rect.top + 180
            pygame.draw.rect(self.screen, (60, 60, 60), (bar_x, bar_y, 200, 6), border_radius=3)
            # Scanner más rápido
            progress_pos = int((time.time() * 200) % 175) 
            pygame.draw.rect(self.screen, self.accent_color, (bar_x + progress_pos, bar_y, 25, 6), border_radius=3)
        else:
            for key, field in self.input_fields.items():
                label = self.font.render(key.capitalize() + ":", True, self.text_color)
                self.screen.blit(label, (self.form_rect.x + 40, field["rect"].y + 5))
                
                bg_color = self.input_bg if not field["active"] else (110, 110, 110)
                pygame.draw.rect(self.screen, bg_color, field["rect"], border_radius=5)
                if field["active"]:
                    pygame.draw.rect(self.screen, self.accent_color, field["rect"], width=2, border_radius=5)
                
                txt_val = self.font.render(field["text"], True, (255, 255, 255))
                self.screen.blit(txt_val, (field["rect"].x + 10, field["rect"].y + 5))

            for btn in [self.apply_button, self.close_button]:
                color = self.accent_color if btn == self.apply_button else (100, 100, 100)
                pygame.draw.rect(self.screen, color, btn["rect"], border_radius=8)
                t_btn = self.font.render(btn["text"], True, (255, 255, 255))
                self.screen.blit(t_btn, t_btn.get_rect(center=btn["rect"].center))

    def handle_event(self, event):
        if not self.is_open or self.is_training: return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.apply_button["rect"].collidepoint(event.pos):
                self._apply_changes()
                return True
            if self.close_button["rect"].collidepoint(event.pos):
                self.is_open = False
                return True
            for field in self.input_fields.values():
                field["active"] = field["rect"].collidepoint(event.pos)
        if event.type == pygame.KEYDOWN:
            for field in self.input_fields.values():
                if field["active"]:
                    if event.key == pygame.K_BACKSPACE:
                        field["text"] = field["text"][:-1]
                    else:
                        char = event.unicode
                        if char.isdigit() or (char == '.' and '.' not in field["text"]):
                            if len(field["text"]) < 8:
                                field["text"] += char
                    return True
        return False