import pygame
from sys import exit
import random

pygame.init()
clean_track, notclean_track = 0, 0
# Initialize the game
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Clean UP')
icon = pygame.image.load('items/trash.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.Font('pixeltype/Pixeltype.ttf', 30)
game_active = True

# Initialize the surface (background)
background_sur = pygame.image.load('background/background.jpg').convert()
score_sur = font.render('0 Cleaned - 0 Not Cleaned', False, (64, 64, 64))
score_rec = score_sur.get_rect(center = (390, 30))

trash_sur = pygame.image.load('items/trash.png').convert_alpha()
trash_rec = trash_sur.get_rect(bottomright= (random.randint(0, 750), -30))

trashcan_sur = pygame.image.load('items/trashcan_close.png').convert_alpha()
trashcan_rec = trashcan_sur.get_rect(midbottom= (80, 385))

# The game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

    if game_active:
        # Placing the surface we made on the original surface
        screen.blit(background_sur, (0, 0))
        screen.blit(score_sur, score_rec)

        trash_rec.y += 2
        if trash_rec.bottom >= 390: 
            trash_rec.x, trash_rec.bottom = random.randint(0, 750), 0 
            notclean_track += 1 
            score_sur = font.render(f'{clean_track} Cleaned - {notclean_track} not Cleaned', False, (64, 64, 64))

        
        screen.blit(trash_sur, trash_rec)
        screen.blit(trashcan_sur, trashcan_rec)


        # Keyboard detection and trach can position change
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and trashcan_rec.midleft[0] > 0:
            trashcan_rec.x -= 4
        elif keys[pygame.K_RIGHT] and trashcan_rec.midright[0] < 800:
            trashcan_rec.x += 4


        # Colision detection and animation change
        if trashcan_rec.colliderect(trash_rec):
            trashcan_sur = pygame.image.load('items/trashcan_open.png').convert_alpha()
            if trashcan_rec.midleft[0] <= trash_rec.center[0] <= trashcan_rec.midright[0] and trash_rec.center[1] >= 335:
                clean_track += 1
                trash_rec.x, trash_rec.bottom = random.randint(0, 750), 0 
                score_sur = font.render(f'{clean_track} Cleaned - {notclean_track} not Cleaned', False, (64, 64, 64))


        else: trashcan_sur = pygame.image.load('items/trashcan_close.png').convert_alpha()
        
            

        # Game Lost
        if notclean_track == 1:
            game_active = False
    
    else:
        # Initialize the surface (gameover)
        gameover_sur = pygame.image.load('background/background.jpg').convert()
        font_over = pygame.font.Font('pixeltype/Pixeltype.ttf', 100)
        font_choices = pygame.font.Font('pixeltype/Pixeltype.ttf', 60)
        
        # game over texts
        textover_sur = font_over.render('GAME OVER', False, (64, 45, 75))
        textover_rec = textover_sur.get_rect(center = (390, 200))
        
        yes_sur = font_choices.render('YES', False, (0, 255, 0))
        yes_rec = yes_sur.get_rect(center = (330, 260))
        
        no_sur = font_choices.render('NO', False, (255, 0, 0))
        no_rec = no_sur.get_rect(center = (450, 260))
        
        # Display
        screen.blit(gameover_sur, (0, 0))
        screen.blit(textover_sur, textover_rec)
        screen.blit(yes_sur, yes_rec)
        screen.blit(no_sur, no_rec)

        if event.type == pygame.MOUSEBUTTONDOWN and yes_rec.collidepoint(event.pos):
            clean_track, notclean_track = 0, 0
            score_sur = font.render('0 Cleaned - 0 Not Cleaned', False, (64, 64, 64))
            game_active = True

        if event.type == pygame.MOUSEBUTTONDOWN and no_rec.collidepoint(event.pos):
            pygame.quit()
            exit()



        



    
    # Draw all our elements
    # Update everything
    pygame.display.update()
    clock.tick(60)


    