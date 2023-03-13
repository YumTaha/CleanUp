import pygame
from sys import exit
import random

pygame.init()
tracker = 0

# Initialize the game
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Clean UP')
icon = pygame.image.load('items/trash.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.Font('pixeltype/Pixeltype.ttf', 50)

# Initialize the surface (background)
background_sur = pygame.image.load('background/background.jpg').convert()
score_sur = font.render('0 Trash Cleaned', False, (64, 64, 64))
score_rec = score_sur.get_rect(center = (380, 50))

trash_sur = pygame.image.load('items/trash.png').convert_alpha()
trash_rec = trash_sur.get_rect(bottomright= (random.randint(0, 750), 0))

trashcan_sur = pygame.image.load('items/trashcan_close.png').convert_alpha()
trashcan_rec = trashcan_sur.get_rect(midbottom= (80, 385))

# The game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Placing the surface we made on the original surface
    screen.blit(background_sur, (0, 0))
    screen.blit(score_sur, score_rec)

    trash_rec.y += 2
    if trash_rec.bottom >= 390: trash_rec.x, trash_rec.bottom = random.randint(0, 750), 0     
    
    screen.blit(trash_sur, trash_rec)
    screen.blit(trashcan_sur, trashcan_rec)


    # Keyboard detection and trach can position change
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and trashcan_rec.midleft[0] >= -23:
        trashcan_rec.x -= 4
    elif keys[pygame.K_RIGHT] and trashcan_rec.midright[0] <=823:
        trashcan_rec.x += 4


    # Colision detection and animation change
    
    if trashcan_rec.colliderect(trash_rec):
        trashcan_sur = pygame.image.load('items/trashcan_open.png').convert_alpha()
        if trashcan_rec.midleft <= trash_rec.center <= trashcan_rec.midright:
            tracker += 1
            trash_rec.x, trash_rec.bottom = random.randint(0, 750), 0 
            score_sur = font.render(f'{tracker} Trash Cleaned', False, (64, 64, 64))


    else: trashcan_sur = pygame.image.load('items/trashcan_close.png').convert_alpha()
    
        


    # Draw all our elements
    # Update everything
    pygame.display.update()
    clock.tick(60)

    