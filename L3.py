import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Spaceship Demo")
clock = pygame.time.Clock()

ship_x, ship_y = WIDTH // 2, HEIGHT // 2
ship_speed = 5
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: ship_x -= ship_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: ship_x += ship_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]: ship_y -= ship_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]: ship_y += ship_speed
    
    ship_x = max(0, min(WIDTH - 50, ship_x))
    ship_y = max(0, min(HEIGHT - 50, ship_y))
    
    screen.fill((10, 10, 30)) # Space black corner
    
    ship_points = [(ship_x + 25, ship_y), (ship_x, ship_y + 40), (ship_x + 15, ship_y + 25),
                   (ship_x + 35, ship_y + 25), (ship_x + 50, ship_y + 40)]
    pygame.draw.polygon(screen, (100, 200, 255), ship_points)
    pygame.draw.polygon(screen, (255, 255, 255), ship_points, 2)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
