import pygame
from sys import exit
import random

def get_timer():
    current_time = (pygame.time.get_ticks() - start_time) // 1000 # convert to seconds
    minutes, seconds = divmod(current_time, 60)
    time_str = f"{minutes:02d}:{seconds:02d}" # format as "mm:ss"
    time_sur = font.render(time_str, False, (64, 64, 64))
    time_rec = score_sur.get_rect(center=(110, 30))
    screen.blit(time_sur, time_rec)

def trash_movement(trash_list, trash_missed):
    if trash_list:
        for trash_rec in trash_list:
            trash_rec.y += 2
            screen.blit(trash_sur, trash_rec)
            if trash_rec.y >= 360: trash_missed += 1

        trash_list = [trashes for trashes in trash_list if trashes.y < 360]
            
        return trash_list, trash_missed
    else:
        return [], trash_missed

def collisions(trashcan, trash):
    global trashcan_index, trashcan_sur
    if trash:
        for trash_rec in trash:
            if trashcan.colliderect(trash_rec): 
                
                trashcan_index = 1
                trashcan_sur = trashcan_[trashcan_index]

                if trashcan_rec.midleft[0] <= trash_rec.midbottom[0] <= trashcan_rec.midright[0] and trash_rec.midbottom[1] > 335:
                
                    trash_rec_list.remove(trash_rec)
                    trashcan_index = 0
                    trashcan_sur = trashcan_[trashcan_index]
                    return True
            
    return False

 

pygame.init()
clean_track, trash_missed = 0, 0  # initialize count


# Initialize the game
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Clean UP')
icon = pygame.image.load('items/trash.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.Font('pixeltype/Pixeltype.ttf', 30)
game_active = True
start_time = 0

# Initialize the surface (background)
background_sur = pygame.image.load('background/background.jpg').convert()
score_sur = font.render('0 Cleaned - 0/10 Missed', False, (64, 64, 64))
score_rec = score_sur.get_rect(center = (390, 30))

# trashes
trash_sur = pygame.image.load('items/trash.png').convert_alpha()
trash_sur = pygame.transform.rotozoom(trash_sur, 0, 1.5)

trash_rec_list = []

trashcan_close = pygame.image.load('items/trashcan_close.png').convert_alpha()
trashcan_open = pygame.image.load('items/trashcan_open.png').convert_alpha()
trashcan_ = [trashcan_close, trashcan_open]
trashcan_index = 0
trashcan_sur =trashcan_[trashcan_index]
trashcan_rec = trashcan_sur.get_rect(midbottom= (80, 385))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


# The game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        if event.type == obstacle_timer and game_active:
            trash_rec_list.append(trash_sur.get_rect(bottomright= (random.randint(10, 750), random.randint(-70,-30))))

    if game_active:
        # Placing the surface we made on the original surface
        screen.blit(background_sur, (0, 0))
        screen.blit(score_sur, score_rec)
        get_timer()
        



        screen.blit(trashcan_sur, trashcan_rec)


        # Obstacle Movement
        trash_rec_list, trash_missed = trash_movement(trash_rec_list, trash_missed)

        score_sur = font.render(f'{clean_track} Cleaned - {trash_missed}/10 Missed', False, (64, 64, 64))
        

        # Keyboard detection and trach can position change
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and trashcan_rec.midleft[0] > 0:
            trashcan_rec.x -= 4
        elif keys[pygame.K_RIGHT] and trashcan_rec.midright[0] < 800:
            trashcan_rec.x += 4

            
        # Colision detection and animation change
        coll_detector = collisions(trashcan_rec, trash_rec_list)
        if coll_detector:
            clean_track += 1
            score_sur = font.render(f'{clean_track} Cleaned - {trash_missed}/10 Missed', False, (64, 64, 64))
        

        # Game Lost
        if trash_missed == 10:
            game_active = False
    
    else:
        # Initialize the surface (gameover)
        gameover_sur = pygame.image.load('background/background.jpg').convert()
        font_over = pygame.font.Font('pixeltype/Pixeltype.ttf', 100)
        font_choices = pygame.font.Font('pixeltype/Pixeltype.ttf', 60)
        trash_rec_list.clear()

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
            clean_track, trash_missed = 0, 0  # initialize count
            score_sur = font.render('0 Cleaned - 0/10 Missed', False, (64, 64, 64))
            game_active = True
            start_time = pygame.time.get_ticks()

        if event.type == pygame.MOUSEBUTTONDOWN and no_rec.collidepoint(event.pos):
            pygame.quit()
            exit()



        



    
    # Draw all our elements
    # Update everything
    pygame.display.update()
    clock.tick(60)


    