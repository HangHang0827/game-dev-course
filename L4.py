import pygame
import sys
import random

# --- 1. Initialization and Constants ---
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
WIN_SCORE = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Setup Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong: Player vs AI")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("consolas", 60, bold=True)
small_font = pygame.font.SysFont("consolas", 30)

# --- 2. Game Objects ---
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 100)
        self.speed = 7

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move(self, up, down):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        if down and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - 10, HEIGHT//2 - 10, 20, 20)
        self.base_speed = 6
        self.dx = random.choice([-1, 1]) * self.base_speed
        self.dy = random.choice([-1, 1]) * self.base_speed

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        # Serve towards the player who just scored (or randomly)
        self.dx = random.choice([-1, 1]) * self.base_speed
        self.dy = random.choice([-1, 1]) * self.base_speed

# --- 3. Game Functions ---
def draw_menu(title, subtitle):
    screen.fill(BLACK)
    title_text = font.render(title, True, WHITE)
    sub_text = small_font.render(subtitle, True, GRAY)
    
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//3))
    screen.blit(sub_text, (WIDTH//2 - sub_text.get_width()//2, HEIGHT//2))
    pygame.display.flip()

def draw_game(player, ai, ball, p_score, ai_score):
    screen.fill(BLACK)
    
    # Draw center line
    pygame.draw.aaline(screen, GRAY, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    # Draw scores
    p_text = font.render(str(p_score), True, WHITE)
    ai_text = font.render(str(ai_score), True, WHITE)
    screen.blit(p_text, (WIDTH//4, 20))
    screen.blit(ai_text, (WIDTH*3//4, 20))
    
    # Draw objects
    player.draw()
    ai.draw()
    ball.draw()
    
    pygame.display.flip()

# --- 4. Main Loop ---
def main():
    player = Paddle(30, HEIGHT//2 - 50)
    ai = Paddle(WIDTH - 45, HEIGHT//2 - 50)
    ball = Ball()
    
    p_score = 0
    ai_score = 0
    
    state = "MENU" # States: MENU, PLAYING, GAME_OVER

    while True:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if state == "MENU" or state == "GAME_OVER":
                        # Reset game variables
                        p_score, ai_score = 0, 0
                        player.rect.centery = HEIGHT // 2
                        ai.rect.centery = HEIGHT // 2
                        ball.reset()
                        state = "PLAYING"

        if state == "MENU":
            draw_menu("PONG", "Press SPACE to Start")
            
        elif state == "GAME_OVER":
            winner = "Player Wins!" if p_score >= WIN_SCORE else "AI Wins!"
            draw_menu(winner, "Press SPACE to Restart")

        elif state == "PLAYING":
            # --- Input Handling ---
            keys = pygame.key.get_pressed()
            # Player movement (W/S or Up/Down)
            player_up = keys[pygame.K_w] or keys[pygame.K_UP]
            player_down = keys[pygame.K_s] or keys[pygame.K_DOWN]
            player.move(player_up, player_down)

            # --- AI Logic ---
            # AI tracks the ball's Y position but moves slightly slower to be beatable
            ai_speed = 10 
            if ai.rect.centery < ball.rect.centery and ai.rect.bottom < HEIGHT:
                ai.rect.y += ai_speed
            elif ai.rect.centery > ball.rect.centery and ai.rect.top > 0:
                ai.rect.y -= ai_speed

            # --- Physics and Movement ---
            ball.move()

            # Top and Bottom collision
            if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
                ball.dy *= -1

            # Paddle collision
            if ball.rect.colliderect(player.rect) and ball.dx < 0:
                ball.dx *= -1.1 # Increase speed slightly on bounce
                ball.rect.left = player.rect.right # Prevent glitching inside paddle
            
            if ball.rect.colliderect(ai.rect) and ball.dx > 0:
                ball.dx *= -1.1 
                ball.rect.right = ai.rect.left

            # Limit ball max speed so it doesn't clip through paddles
            ball.dx = max(min(ball.dx, 15), -15)

            # --- Scoring ---
            if ball.rect.left <= 0:
                ai_score += 1
                ball.reset()
            elif ball.rect.right >= WIDTH:
                p_score += 1
                ball.reset()

            # Win Condition
            if p_score >= WIN_SCORE or ai_score >= WIN_SCORE:
                state = "GAME_OVER"

            # Render
            draw_game(player, ai, ball, p_score, ai_score)

        clock.tick(FPS)

if __name__ == "__main__":
    main()