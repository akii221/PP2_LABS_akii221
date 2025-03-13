import pygame

pygame.init()
screen = pygame.display.set_mode((500,500))
x,y = 250, 200
radius = 25

running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x - radius > 0:
        x -= 20
    if keys[pygame.K_RIGHT] and x + radius < 500:
        x += 20
    if keys[pygame.K_UP] and y - radius > 0:
        y -= 20
    if keys[pygame.K_DOWN] and y + radius < 500:
        y += 20
    screen.fill((255,255,255))

    pygame.draw.circle(screen, (255, 0, 255), (x, y), radius)
    pygame.display.flip()
    pygame.time.delay(10)
pygame.quit()

# Play, Stop, Next, Previous 