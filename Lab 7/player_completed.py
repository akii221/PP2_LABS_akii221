import pygame
import os 

pygame.init()
pygame.mixer.init()
image = pygame.image.load('player1.png')
screen = pygame.display.set_mode((500,400))
songs = [
    "Track 1.mp3",
    "Track 2.mp3"
]
current_song = 0

def playsong(num):
    pygame.mixer.music.load(songs[num])
    pygame.mixer.music.play()

playsong(current_song)

x = 0
y = 0

running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))
    screen.blit(image, (x,y))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]: # dlya pause
        pygame.mixer.music.pause()
    if keys[pygame.K_w]: #dlya resume
        pygame.mixer.music.unpause()
    if keys[pygame.K_e]: #dlya next
        current_song = (current_song + 1)
        playsong(current_song)
    if keys[pygame.K_r]: # dlya previous
        current_song = (current_song -1)
        playsong(current_song)

    
    pygame.time.delay(100)
    pygame.display.flip()


pygame.quit()