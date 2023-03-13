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
text_sur = font.render('START', False, 'black')

trash_sur = pygame.image.load('items/trash.png').convert_alpha()
trash_rec = trash_sur.get_rect(bottomright= (random.randint(0, 750), 0))

trashcan_sur = pygame.image.load('items/trashcan_close.png').convert_alpha()
trashcan_rec = trashcan_sur.get_rect(midbottom= (80, 400))

# The game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            event.pos

    # Placing the surface we made on the original surface
    screen.blit(background_sur, (0, 0))
    screen.blit(text_sur, (350, 100))

    trash_rec.y += 2
    if trash_rec.bottom >= 390: trash_rec.x, trash_rec.bottom = random.randint(0, 750), 0     
    
    screen.blit(trash_sur, trash_rec)
    screen.blit(trashcan_sur, trashcan_rec)


    '''if trashcan_rec.colliderect(trash_rec):
        pygame.mouse'''

    mouse_pos = pygame.mouse.get_pos()
    if trashcan_rec.collidepoint(mouse_pos):
        


    # Draw all our elements
    # Update everything
    pygame.display.update()
    clock.tick(60)

    