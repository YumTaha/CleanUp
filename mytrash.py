import pygame
from sys import exit
import random

pygame.init()

# Initialize the game
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('My Trash')
clock = pygame.time.Clock()
font = pygame.font.Font('pixeltype/Pixeltype.ttf', 50)

# Initialize the surface (background)
background_sur = pygame.image.load('background/all.jpg').convert()
score_sur = font.render('SCORE', False, (64, 64, 64))
score_rec = score_sur.get_rect(center = (400, 100))

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
        '''if trashcan_rec.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            pass
        '''
    # Placing the surface we made on the original surface
    screen.blit(background_sur, (0, 0))
    screen.blit(score_sur, score_rec)

    trash_rec.y += 2
    if trash_rec.bottom >= 390: trash_rec.x, trash_rec.bottom = random.randint(0, 750), 0     
    
    screen.blit(trash_sur, trash_rec)
    screen.blit(trashcan_sur, trashcan_rec)


    '''if trashcan_rec.colliderect(trash_rec):
        pygame.mouse'''


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and trashcan_rec.midleft[0] >= -23:
        trashcan_rec.x -= 4
    elif keys[pygame.K_RIGHT] and trashcan_rec.midright[0] <=823:
        trashcan_rec.x += 4

    mouse_pos = pygame.mouse.get_pos()
    if trashcan_rec.colliderect(trash_rec):
        trashcan_sur = pygame.image.load('items/trashcan_open.png').convert_alpha()
        
    else: trashcan_sur = pygame.image.load('items/trashcan_close.png').convert_alpha()
    
        


    # Draw all our elements
    # Update everything
    pygame.display.update()
    clock.tick(60)

    