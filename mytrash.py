import pygame
from sys import exit
import random


class Trashcan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        trashcan_close = pygame.image.load('items/trashcan_close.png').convert_alpha()
        trashcan_open = pygame.image.load('items/trashcan_open.png').convert_alpha()
        self.trashcan_ = [trashcan_close, trashcan_open]
        self.trashcan_index = 0

        self.image = self.trashcan_[self.trashcan_index]
        self.rect = self.image.get_rect(midbottom= (100, 385))
        
    def set_index(self, index):
        self.trashcan_index = index
        self.image = self.trashcan_[self.trashcan_index]
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.midleft[0] > 0:
            self.rect.x -= 4
        elif keys[pygame.K_RIGHT] and self.rect.midright[0] < 800:
            self.rect.x += 4

    def update(self):
        self.player_input()

class Trash(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'paper':
            paper = pygame.image.load('items/trash.png').convert_alpha()
            paper = pygame.transform.rotozoom(paper, 0, 1.5)
            self.paper = paper

        self.image = self.paper
        self.rect = self.image.get_rect(bottomright= (random.randint(10, 750), random.randint(-70,-30)))
    
    def update(self):
        self.rect.y += 2
        self.destroy()

    def destroy(self):
        global trash_missed, clean_track

        if trashcan.sprite.rect.midleft <= self.rect.center <= trashcan.sprite.rect.midright and self.rect.center[1] >330:
            clean_track += 1
            self.kill()
        if self.rect.y >= 360:
            trash_missed += 1
            self.kill()


def get_timer():
    current_time = (pygame.time.get_ticks() - start_time) // 1000 # convert to seconds
    minutes, seconds = divmod(current_time, 60)
    time_str = f"{minutes:02d}:{seconds:02d}" # format as "mm:ss"
    time_sur = font.render(time_str, False, (64, 64, 64))
    time_rec = score_sur.get_rect(center=(110, 30))
    screen.blit(time_sur, time_rec)

def collision_sprite():
    global clean_track
    if pygame.sprite.spritecollide(trashcan.sprite, trash_group, False):
        trashcan.sprite.set_index(1)
    else: trashcan.sprite.set_index(0)

pygame.init()
game_active = True
clean_track, trash_missed, start_time = 0, 0, 0  # initialize count


# Initialize the game
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Clean UP')
icon = pygame.image.load('items/trash.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.Font('pixeltype/Pixeltype.ttf', 30)




trashcan = pygame.sprite.GroupSingle()
trashcan.add(Trashcan())

trash_group = pygame.sprite.Group()


# Initialize the surface (background)
background_sur = pygame.image.load('background/background.jpg').convert()
score_sur = font.render('0 Cleaned - 0/10 Missed', False, (64, 64, 64))
score_rec = score_sur.get_rect(center = (390, 30))

# trashes
trash_sur = pygame.image.load('items/trash.png').convert_alpha()
trash_sur = pygame.transform.rotozoom(trash_sur, 0, 1.5)


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
            trash_group.add(Trash('paper'))

    if game_active:
        # Placing the surface we made on the original surface
        screen.blit(background_sur, (0, 0))
        screen.blit(score_sur, score_rec)
        get_timer()

        #screen.blit(trashcan_sur, trashcan_rec)
        trashcan.draw(screen)
        trashcan.update()
        trash_group.draw(screen)
        trash_group.update()

        score_sur = font.render(f'{clean_track} Cleaned - {trash_missed}/10 Missed', False, (64, 64, 64))
        
        # Colision detection and animation change
        collision_sprite()

        # Game Lost
        if trash_missed == 10:
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


    