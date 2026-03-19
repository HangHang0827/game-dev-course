import pygame
import sys
import random
import json
import os
import math

# --- 1. Initialization and Constants ---
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
WIN_SCORE = 5
SCORE_FILE = "high_score.json"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 150, 255)
CYAN = (50, 255, 255)
MAGENTA = (255, 50, 255)

# Color Selection Lists
AVAILABLE_COLORS = [WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]
COLOR_NAMES = ["WHITE", "RED", "GREEN", "BLUE", "YELLOW", "CYAN", "MAGENTA"]

# Setup Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong: Ultimate Edition")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("consolas", 60, bold=True)
small_font = pygame.font.SysFont("consolas", 30)
tiny_font = pygame.font.SysFont("consolas", 20)

# --- 2. JSON Leaderboard Functions ---
def load_leaderboard():
    default_data = {"streak": [], "endless": []}
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as file:
            try:
                data = json.load(file)
                if isinstance(data.get("streak"), int): 
                    return default_data
                return data
            except json.JSONDecodeError:
                return default_data
    return default_data

def save_leaderboard(data):
    with open(SCORE_FILE, "w") as file:
        json.dump(data, file)

def is_high_score(data, mode, score):
    if score <= 0: return False
    key = "streak" if mode == "NORMAL" else "endless"
    scores = data.get(key, [])
    if len(scores) < 5: return True 
    return score > scores[-1]["score"] 

def add_score(data, mode, name, score):
    key = "streak" if mode == "NORMAL" else "endless"
    data[key].append({"name": name, "score": score})
    data[key] = sorted(data[key], key=lambda x: x["score"], reverse=True)[:5]
    save_leaderboard(data)

def get_highest(data, mode):
    key = "streak" if mode == "NORMAL" else "endless"
    scores = data.get(key, [])
    return scores[0]["score"] if scores else 0

def create_particles(x, y, colors, amount, speed, size):
    new_particles = []
    for _ in range(amount):
        color = random.choice(colors) if isinstance(colors, list) else colors
        new_particles.append(Particle(x, y, color, speed, size))
    return new_particles

# --- 3. Game UI Classes ---
class Button:
    def __init__(self, text, x, y, width, height, font_to_use=small_font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = DARK_GRAY
        self.hover_color = GRAY
        self.text_color = WHITE
        self.font = font_to_use

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, width=2, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            if self.rect.collidepoint(event.pos):
                return True
        return False

# --- 4. Game Objects ---
class Particle:
    def __init__(self, x, y, color, speed_multiplier, size):
        self.x = x
        self.y = y
        self.dx = random.uniform(-1, 1) * speed_multiplier
        self.dy = random.uniform(-1, 1) * speed_multiplier
        self.color = color
        self.radius = random.uniform(2, size)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.radius -= 0.15
        return self.radius > 0

    def draw(self, surface):
        if self.radius > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))

class Paddle:
    def __init__(self, x, y, is_player_controlled=False):
        self.rect = pygame.Rect(x, y, 15, 100)
        self.velocity = 0.0
        self.acceleration = 1.5 
        self.friction = 0.85
        self.max_speed = 12.0
        self.is_player_controlled = is_player_controlled

    def draw(self, surface, color=WHITE):
        pygame.draw.rect(surface, color, self.rect)

    def apply_physics(self):
        self.velocity *= self.friction
        if self.velocity > self.max_speed: self.velocity = self.max_speed
        elif self.velocity < -self.max_speed: self.velocity = -self.max_speed
        self.rect.y += int(self.velocity)
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def move_player(self, up, down):
        if up: self.velocity -= self.acceleration
        if down: self.velocity += self.acceleration
        self.apply_physics()

    def move_ai(self, target_y):
        deadzone = 15 
        if self.rect.centery < target_y - deadzone: self.velocity += self.acceleration * 0.7
        elif self.rect.centery > target_y + deadzone: self.velocity -= self.acceleration * 0.7
        self.apply_physics()

class Ball:
    def __init__(self, speed_multiplier=1.0):
        self.rect = pygame.Rect(WIDTH//2 - 10, HEIGHT//2 - 10, 20, 20)
        self.base_speed = 6 * speed_multiplier
        self.dx = random.choice([-1, 1]) * self.base_speed
        self.dy = random.choice([-1, 1]) * self.base_speed
        self.trail = []
        self.delay_frames = 180  # 3 seconds at 60 FPS

    def draw(self, surface):
        # Draw countdown if delayed
        if self.delay_frames > 0:
            seconds_left = (self.delay_frames // 60) + 1
            countdown_text = small_font.render(str(seconds_left), True, WHITE)
            text_rect = countdown_text.get_rect(center=(self.rect.centerx, self.rect.centery - 40))
            surface.blit(countdown_text, text_rect)
        else:
            # Draw dynamic trail
            current_speed = math.hypot(self.dx, self.dy)
            if current_speed > 10:
                trail_base_size = min(20, current_speed * 0.8)
                for i, pos in enumerate(self.trail):
                    ratio = i / len(self.trail)
                    radius = int(trail_base_size * ratio)
                    color_intensity = int(200 * ratio) + 55 
                    trail_color = (color_intensity, color_intensity, color_intensity)
                    
                    if radius > 0:
                        pygame.draw.circle(surface, trail_color, pos, radius)

        # Draw the actual ball on top
        pygame.draw.ellipse(surface, WHITE, self.rect)

    def move(self):
        # Countdown logic
        if self.delay_frames > 0:
            self.delay_frames -= 1
            return 

        self.trail.append(self.rect.center)
        
        current_speed = math.hypot(self.dx, self.dy)
        max_trail_length = min(16, int(current_speed * 0.9))
        
        while len(self.trail) > max_trail_length:
            self.trail.pop(0)

        self.rect.x += self.dx
        self.rect.y += self.dy

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.dx = random.choice([-1, 1]) * self.base_speed
        self.dy = random.choice([-1, 1]) * self.base_speed
        self.trail.clear()
        self.delay_frames = 180

# --- 5. Background Menu Match Functions ---
def create_menu_elements():
    paddle_left = Paddle(30, HEIGHT//2 - 50, is_player_controlled=False)
    paddle_right = Paddle(WIDTH - 45, HEIGHT//2 - 50, is_player_controlled=False)
    ball = Ball(speed_multiplier=0.8) 
    ball.delay_frames = 0  # Force the menu ball to start moving immediately!
    particles = []
    return paddle_left, paddle_right, ball, particles

def update_menu_elements(paddle_left, paddle_right, ball, particles):
    time_ms = pygame.time.get_ticks()

    # AI 1: "The Defender" (Left Paddle)
    if ball.dx > 0:
        target_left = HEIGHT // 2 
    else:
        target_left = ball.rect.centery + math.sin(time_ms * 0.002) * 10 
    
    paddle_left.move_ai(target_left)

    # AI 2: "The Chaser" (Right Paddle)
    offset_right = math.cos(time_ms * 0.001) * 45
    paddle_right.move_ai(ball.rect.centery + offset_right)
    
    ball.move()
    particles[:] = [p for p in particles if p.update()]

    if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
        ball.dy *= -1
        particles.extend(create_particles(ball.rect.centerx, ball.rect.centery, GRAY, 3, 1, 3))

    def check_paddle_collision(paddle, is_left):
        nonlocal particles
        if ball.rect.colliderect(paddle.rect):
            if (is_left and ball.dx < 0) or (not is_left and ball.dx > 0):
                ball.dx *= -1
                ball.dy += paddle.velocity * 0.1
                if is_left: ball.rect.left = paddle.rect.right
                else: ball.rect.right = paddle.rect.left
                p_x = ball.rect.left if is_left else ball.rect.right
                particles.extend(create_particles(p_x, ball.rect.centery, WHITE, 8, 2, 4))
                
    check_paddle_collision(paddle_left, is_left=True)
    check_paddle_collision(paddle_right, is_left=False)

    if ball.rect.left <= -50 or ball.rect.right >= WIDTH + 50:
        exit_x = 0 if ball.rect.left <= -50 else WIDTH
        particles.extend(create_particles(exit_x, ball.rect.centery, [ORANGE, RED], 15, 3, 6))
        ball.reset()
        ball.delay_frames = 0  # Keep the menu ball moving immediately after a reset!

def draw_menu_scene(surface, paddle_left, paddle_right, ball, particles):
    bg_surface = pygame.Surface((WIDTH, HEIGHT))
    bg_surface.set_colorkey(BLACK) 
    bg_surface.set_alpha(80) 

    pygame.draw.aaline(bg_surface, GRAY, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    for p in particles:
        p.draw(bg_surface)
    paddle_left.draw(bg_surface)
    paddle_right.draw(bg_surface)
    ball.draw(bg_surface)
    
    surface.blit(bg_surface, (0, 0))

# --- 6. Main Loop ---
def main():
    player = Paddle(30, HEIGHT//2 - 50, is_player_controlled=True)
    ai = Paddle(WIDTH - 45, HEIGHT//2 - 50, is_player_controlled=False) 
    ball = Ball()
    
    p_score = 0
    ai_score = 0
    current_streak = 0
    
    leaderboard_data = load_leaderboard()
    playing_particles = []
    
    menu_left, menu_right, menu_ball, menu_particles = create_menu_elements()
    
    state = "MENU"
    game_mode = "NORMAL"
    winner = ""

    # Color Selection State variables
    p1_color_idx = 2  # Default to GREEN
    p2_color_idx = 1  # Default to RED

    # Input Variables
    player_name = ""
    qualifying_score = 0
    cursor_timer = 0

    # UI setup
    btn_width, btn_height = 280, 45  
    center_x = WIDTH // 2 - btn_width // 2
    
    # Main Menu Buttons
    play_menu_btn = Button("Play Game", center_x, 220, btn_width, btn_height)
    ldr_btn = Button("Leaderboard", center_x, 290, btn_width, btn_height)
    credits_btn = Button("Credits", center_x, 360, btn_width, btn_height)
    quit_btn = Button("Quit", center_x, 430, btn_width, btn_height)

    # Mode Selection Buttons
    normal_btn = Button("1P Normal Match", center_x, 200, btn_width, btn_height)
    p2_btn = Button("2 Player Match", center_x, 270, btn_width, btn_height)
    endless_btn = Button("Endless Mode", center_x, 340, btn_width, btn_height)
    mode_back_btn = Button("Back to Menu", center_x, 430, btn_width, btn_height)
    
    # Color Selection Buttons
    p1_left_btn = Button("<", WIDTH//4 - 70, 240, 40, 40)
    p1_right_btn = Button(">", WIDTH//4 + 30, 240, 40, 40)
    p2_left_btn = Button("<", WIDTH*3//4 - 70, 240, 40, 40)
    p2_right_btn = Button(">", WIDTH*3//4 + 30, 240, 40, 40)
    start_pvp_btn = Button("Start Match!", center_x, 350, btn_width, btn_height)
    color_back_btn = Button("Back", center_x, 420, btn_width, btn_height)

    # Other Buttons
    resume_btn = Button("Resume", center_x, 250, btn_width, btn_height)
    menu_btn = Button("Main Menu", center_x, 320, btn_width, btn_height)
    replay_btn = Button("Play Again", center_x, 250, btn_width, btn_height)
    back_btn = Button("Back", center_x, 520, btn_width, btn_height)
    pause_btn = Button("Pause", WIDTH//2 - 40, 10, 80, 30, tiny_font)

    def reset_match():
        nonlocal p_score, ai_score, playing_particles
        p_score, ai_score = 0, 0
        player.rect.centery = HEIGHT // 2
        ai.rect.centery = HEIGHT // 2
        player.velocity, ai.velocity = 0, 0
        playing_particles.clear()
        ball.reset()

    while True:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and state == "PLAYING":
                    state = "PAUSED"
                elif event.key == pygame.K_ESCAPE and state == "PAUSED":
                    state = "PLAYING"

            if state == "MENU":
                if play_menu_btn.is_clicked(event):
                    state = "MODE_SELECT"
                if ldr_btn.is_clicked(event):
                    state = "LEADERBOARD"
                if credits_btn.is_clicked(event):
                    state = "CREDITS"
                if quit_btn.is_clicked(event):
                    pygame.quit()
                    sys.exit()

            elif state == "MODE_SELECT":
                if normal_btn.is_clicked(event):
                    game_mode = "NORMAL"
                    reset_match()
                    state = "PLAYING"
                if p2_btn.is_clicked(event):
                    state = "COLOR_SELECT"
                if endless_btn.is_clicked(event):
                    game_mode = "ENDLESS"
                    reset_match()
                    state = "PLAYING"
                if mode_back_btn.is_clicked(event):
                    state = "MENU"

            elif state == "COLOR_SELECT":
                # Cycle P1 colors
                if p1_left_btn.is_clicked(event):
                    p1_color_idx = (p1_color_idx - 1) % len(AVAILABLE_COLORS)
                if p1_right_btn.is_clicked(event):
                    p1_color_idx = (p1_color_idx + 1) % len(AVAILABLE_COLORS)
                # Cycle P2 colors
                if p2_left_btn.is_clicked(event):
                    p2_color_idx = (p2_color_idx - 1) % len(AVAILABLE_COLORS)
                if p2_right_btn.is_clicked(event):
                    p2_color_idx = (p2_color_idx + 1) % len(AVAILABLE_COLORS)
                
                # Start the actual match
                if start_pvp_btn.is_clicked(event):
                    game_mode = "2_PLAYER"
                    reset_match()
                    state = "PLAYING"
                if color_back_btn.is_clicked(event):
                    state = "MODE_SELECT"
                    
            elif state == "PLAYING":
                if pause_btn.is_clicked(event):
                    state = "PAUSED"

            elif state == "PAUSED":
                if resume_btn.is_clicked(event):
                    state = "PLAYING"
                if menu_btn.is_clicked(event):
                    state = "MENU"

            elif state == "INPUT_NAME":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        final_name = player_name.strip()
                        if not final_name: final_name = "ANON"
                        add_score(leaderboard_data, game_mode, final_name, qualifying_score)
                        player_name = ""
                        state = "LEADERBOARD"
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 10:
                            player_name += event.unicode

            elif state == "GAME_OVER":
                if replay_btn.is_clicked(event):
                    reset_match()
                    state = "PLAYING"
                if menu_btn.is_clicked(event):
                    state = "MENU"
                if quit_btn.is_clicked(event):
                    pygame.quit()
                    sys.exit()

            elif state == "CREDITS" or state == "LEADERBOARD":
                if back_btn.is_clicked(event):
                    state = "MENU"

        # Update Background Match in specific states
        states_with_bg_game = ["MENU", "MODE_SELECT", "COLOR_SELECT", "LEADERBOARD", "CREDITS", "PAUSED", "INPUT_NAME"]
        if state in states_with_bg_game:
            update_menu_elements(menu_left, menu_right, menu_ball, menu_particles)
        elif state == "PLAYING":
             playing_particles[:] = [p for p in playing_particles if p.update()]


        # --- RENDERING & LOGIC ---
        screen.fill(BLACK)
        
        # Draw background match
        if state in states_with_bg_game:
            draw_menu_scene(screen, menu_left, menu_right, menu_ball, menu_particles)

        # Draw playing particles
        if state == "PLAYING":
            for p in playing_particles:
                p.draw(screen)

        # --- Menu Rendering ---
        if state == "MENU":
            title_text = font.render("PONG", True, WHITE)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 60))
            
            top_streak = get_highest(leaderboard_data, "NORMAL")
            top_endless = get_highest(leaderboard_data, "ENDLESS")
            
            streak_text = tiny_font.render(f"Top Streak: {top_streak}", True, YELLOW)
            endless_text = tiny_font.render(f"Top Endless: {top_endless}", True, ORANGE)
            screen.blit(streak_text, (WIDTH//2 - streak_text.get_width()//2, 130))
            screen.blit(endless_text, (WIDTH//2 - endless_text.get_width()//2, 160))

            play_menu_btn.draw(screen)
            ldr_btn.draw(screen)
            credits_btn.draw(screen)
            quit_btn.draw(screen)

        elif state == "MODE_SELECT":
            title_text = font.render("SELECT MODE", True, WHITE)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 80))
            
            normal_btn.draw(screen)
            p2_btn.draw(screen)
            endless_btn.draw(screen)
            mode_back_btn.draw(screen)

        elif state == "COLOR_SELECT":
            title_text = font.render("CHOOSE COLORS", True, WHITE)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 70))

            # Player 1 Section
            p1_title = small_font.render("PLAYER 1", True, WHITE)
            screen.blit(p1_title, (WIDTH//4 - p1_title.get_width()//2, 180))
            
            p1_c_name = small_font.render(COLOR_NAMES[p1_color_idx], True, AVAILABLE_COLORS[p1_color_idx])
            screen.blit(p1_c_name, (WIDTH//4 - p1_c_name.get_width()//2, 290))
            
            p1_left_btn.draw(screen)
            p1_right_btn.draw(screen)

            # Player 2 Section
            p2_title = small_font.render("PLAYER 2", True, WHITE)
            screen.blit(p2_title, (WIDTH*3//4 - p2_title.get_width()//2, 180))
            
            p2_c_name = small_font.render(COLOR_NAMES[p2_color_idx], True, AVAILABLE_COLORS[p2_color_idx])
            screen.blit(p2_c_name, (WIDTH*3//4 - p2_c_name.get_width()//2, 290))
            
            p2_left_btn.draw(screen)
            p2_right_btn.draw(screen)

            start_pvp_btn.draw(screen)
            color_back_btn.draw(screen)

        elif state == "LEADERBOARD":
            title_text = font.render("LEADERBOARD", True, WHITE)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))
            
            streak_title = small_font.render("WIN STREAKS", True, YELLOW)
            screen.blit(streak_title, (150, 150))
            for i, entry in enumerate(leaderboard_data.get("streak", [])):
                entry_txt = tiny_font.render(f"{i+1}. {entry['name']} - {entry['score']}", True, WHITE)
                screen.blit(entry_txt, (150, 200 + (i * 40)))

            endless_title = small_font.render("ENDLESS MODE", True, ORANGE)
            screen.blit(endless_title, (450, 150))
            for i, entry in enumerate(leaderboard_data.get("endless", [])):
                entry_txt = tiny_font.render(f"{i+1}. {entry['name']} - {entry['score']}", True, WHITE)
                screen.blit(entry_txt, (450, 200 + (i * 40)))

            back_btn.draw(screen)

        elif state == "CREDITS":
            title_text = font.render("CREDITS", True, WHITE)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))
            dev_text = small_font.render("Developed in Python with Pygame", True, GRAY)
            thanks_text = small_font.render("Thanks for playing!", True, WHITE)
            screen.blit(dev_text, (WIDTH//2 - dev_text.get_width()//2, 250))
            screen.blit(thanks_text, (WIDTH//2 - thanks_text.get_width()//2, 320))
            back_btn.draw(screen)
            
        elif state == "INPUT_NAME":
            title_text = font.render("NEW HIGH SCORE!", True, GREEN)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 150))
            
            sub_text = small_font.render(f"Score: {qualifying_score} | Enter Name:", True, WHITE)
            screen.blit(sub_text, (WIDTH//2 - sub_text.get_width()//2, 250))
            
            cursor_timer += clock.get_time()
            cursor = "_" if cursor_timer % 1000 < 500 else " "
            
            name_text = font.render(player_name + cursor, True, YELLOW)
            screen.blit(name_text, (WIDTH//2 - name_text.get_width()//2, 320))
            
            hint_text = tiny_font.render("Press ENTER to save", True, GRAY)
            screen.blit(hint_text, (WIDTH//2 - hint_text.get_width()//2, 450))

        elif state == "GAME_OVER":
            title_text = font.render(winner, True, WHITE)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))
            
            if game_mode == "ENDLESS":
                score_text = small_font.render(f"Final Score: {p_score}", True, GRAY)
                screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 180))
            elif game_mode == "NORMAL":
                streak_txt = small_font.render(f"Win Streak: {current_streak}", True, YELLOW)
                screen.blit(streak_txt, (WIDTH//2 - streak_txt.get_width()//2, 180))

            replay_btn.draw(screen)
            menu_btn.draw(screen)
            
            quit_btn.rect.y = 390
            quit_btn.draw(screen)
            quit_btn.rect.y = 430

        elif state == "PAUSED":
            title_text = font.render("PAUSED", True, WHITE)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))
            resume_btn.draw(screen)
            menu_btn.draw(screen)

        elif state == "PLAYING":
            keys = pygame.key.get_pressed()
            
            # --- Dynamic Colors ---
            p1_color = AVAILABLE_COLORS[p1_color_idx] if game_mode == "2_PLAYER" else WHITE
            p2_color = AVAILABLE_COLORS[p2_color_idx] if game_mode == "2_PLAYER" else WHITE
            
            if game_mode == "2_PLAYER":
                player.move_player(keys[pygame.K_w], keys[pygame.K_s])
                ai.move_player(keys[pygame.K_UP], keys[pygame.K_DOWN]) 
            else:
                player.move_player(keys[pygame.K_w] or keys[pygame.K_UP], keys[pygame.K_s] or keys[pygame.K_DOWN])
                # Only let the AI move if the ball isn't paused!
                if ball.delay_frames == 0:
                    ai.move_ai(ball.rect.centery) 

            ball.move()

            # Bounces
            if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
                ball.dy *= -1
                playing_particles.extend(create_particles(ball.rect.centerx, ball.rect.centery, GRAY, 5, 2, 4))

            # Paddle collisions
            if ball.rect.colliderect(player.rect) and ball.dx < 0:
                ball.dx *= -1.1 
                ball.dy += player.velocity * 0.15 
                ball.rect.left = player.rect.right 
                playing_particles.extend(create_particles(ball.rect.left, ball.rect.centery, p1_color, 15, 4, 5))
            
            if ball.rect.colliderect(ai.rect) and ball.dx > 0:
                ball.dx *= -1.1 
                ball.dy += ai.velocity * 0.15
                ball.rect.right = ai.rect.left
                playing_particles.extend(create_particles(ball.rect.right, ball.rect.centery, p2_color, 15, 4, 5))

            ball.dx = max(min(ball.dx, 15), -15)
            ball.dy = max(min(ball.dy, 12), -12)

            # --- Scoring Logic ---
            if ball.rect.left <= 0:
                ai_score += 1
                playing_particles.extend(create_particles(0, ball.rect.centery, [YELLOW, ORANGE, RED], 60, 8, 8))
                ball.reset()
            elif ball.rect.right >= WIDTH:
                p_score += 1
                playing_particles.extend(create_particles(WIDTH, ball.rect.centery, [YELLOW, ORANGE, RED], 60, 8, 8))
                ball.reset()

            # --- Win/Loss Logic ---
            if game_mode == "NORMAL":
                if p_score >= WIN_SCORE:
                    winner = "Player Wins!"
                    current_streak += 1
                    if is_high_score(leaderboard_data, "NORMAL", current_streak):
                        qualifying_score = current_streak
                        state = "INPUT_NAME"
                    else:
                        state = "GAME_OVER"
                elif ai_score >= WIN_SCORE:
                    winner = "AI Wins!"
                    current_streak = 0
                    state = "GAME_OVER"
            
            elif game_mode == "ENDLESS":
                if ai_score >= 5:
                    winner = "Game Over!"
                    if is_high_score(leaderboard_data, "ENDLESS", p_score):
                        qualifying_score = p_score
                        state = "INPUT_NAME"
                    else:
                        state = "GAME_OVER"

            elif game_mode == "2_PLAYER":
                if p_score >= WIN_SCORE:
                    winner = "Player 1 Wins!"
                    state = "GAME_OVER"
                elif ai_score >= WIN_SCORE:
                    winner = "Player 2 Wins!"
                    state = "GAME_OVER"

            # --- Draw Game Elements ---
            pygame.draw.aaline(screen, GRAY, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
            pause_btn.draw(screen)
            
            # Draw score text with dynamic colors
            p_text = font.render(str(p_score), True, p1_color)
            if game_mode == "NORMAL" or game_mode == "2_PLAYER":
                ai_text = font.render(str(ai_score), True, p2_color)
                screen.blit(p_text, (WIDTH//4, 20))
                screen.blit(ai_text, (WIDTH*3//4, 20))
                
                if game_mode == "NORMAL":
                    streak_ind = tiny_font.render(f"Streak: {current_streak}", True, YELLOW)
                    screen.blit(streak_ind, (20, 20))
                
            elif game_mode == "ENDLESS":
                screen.blit(p_text, (WIDTH//2 - p_text.get_width()//2, 50))
                lives_text = tiny_font.render(f"Lives: {5 - ai_score}", True, RED)
                screen.blit(lives_text, (20, 20))

            # Draw the paddles and ball
            player.draw(screen, p1_color)
            ai.draw(screen, p2_color)
            ball.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()