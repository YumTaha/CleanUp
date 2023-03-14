import pygame
from sys import exit
from random import randint, choice


class Trashcan(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        trashcan_close = pygame.image.load('items/trashcan_close.png').convert_alpha()
        trashcan_open = pygame.image.load('items/trashcan_open.png').convert_alpha()
        self.trashcan_ = [trashcan_close, trashcan_open]
        self.trashcan_index = 0

        self.image = self.trashcan_[self.trashcan_index]
        self.rect = self.image.get_rect(midbottom= (100, 385))
        
    def set_index(self, index):
        self.index = index
        self.image = self.trashcan_[self.index]
        
    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]: 
            self.rect.x -= 4
            if self.rect.midright[0] < 0: self.rect.x = 800
        if keys[pygame.K_RIGHT]:
            self.rect.x += 4
            if self.rect.midleft[0] > 800: self.rect.x = -40

    def update(self):
        self.player_input()

class Trash(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        paper = pygame.image.load('items/trash.png').convert_alpha()
        paper = pygame.transform.rotozoom(paper, 0, 1.5)

        self.image = paper
        self.rect = self.image.get_rect(bottomright= (randint(10, 750), randint(-70,-30)))
        
        self.collide_sound = pygame.mixer.Sound('audio/collision.wav')

    def update(self):
        self.rect.y += 2
        self.destroy()

    def destroy(self):
        global trash_missed, trash_cleaned

        if trashcan.sprite.rect.midleft <= self.rect.center <= trashcan.sprite.rect.midright and self.rect.center[1] >330:
            trash_cleaned += 1
            self.kill()
            self.collide_sound.play()

        if self.rect.y >= 360:
            trash_missed += 1
            self.kill()


def get_timer():
    current_time = (pygame.time.get_ticks() - start_time) // 1000 # convert to seconds
    minutes, seconds = divmod(current_time, 60)
    time_str = f"{minutes:02d}:{seconds:02d}" # format as "mm:ss"
    time_sur = font.render(time_str, False, (64, 64, 64))
    time_rec = time_sur.get_rect(center=(40, 30))
    screen.blit(time_sur, time_rec)

def collision_sprite():

    if pygame.sprite.spritecollide(trashcan.sprite, trash_group, False):
        trashcan.sprite.set_index(1)
    else: trashcan.sprite.set_index(0)

pygame.init()
game_active = True
trash_cleaned, trash_missed, start_time = 0, 0, 0  # initialize count

# Initialize the game
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Clean UP')
icon = pygame.image.load('background/game_icon.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/Pixeltype.ttf', 30)

# Background music
bg_music1 = pygame.mixer.Sound('audio/bg_music1.wav')
bg_music2 = pygame.mixer.Sound('audio/bg_music2.mp3')
bg_music = choice([bg_music1, bg_music2])
bg_music.set_volume(0.2)
bg_music.play(loops = -1)

# Calling classes and creating the ingame items
trashcan = pygame.sprite.GroupSingle()
trashcan.add(Trashcan())
trash_group = pygame.sprite.Group()

# Initialize the surface (background)
background_sur = pygame.image.load('background/background.jpg').convert()
score_sur = font.render('0 Cleaned - 0/10 Missed', False, (64, 64, 64))
score_rec = score_sur.get_rect(center = (390, 30))

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
            trash_group.add(Trash())

    if game_active:

        # Placing the surface we made on the original surface
        screen.blit(background_sur, (0, 0))
        screen.blit(score_sur, score_rec)
        get_timer()

        trashcan.draw(screen)
        trashcan.update()
        trash_group.draw(screen)
        trash_group.update()

        score_sur = font.render(f'{trash_cleaned} Cleaned - {trash_missed}/10 Missed', False, (64, 64, 64))
        
        # Colision detection and animation change
        collision_sprite()

        # Game Lost
        if trash_missed == 10:
            game_active = False

            # Gameover sound
            bg_music.set_volume(0)
            gameover_sound = pygame.mixer.Sound('audio/gameover.wav')
            gameover_sound.set_volume(0.1)
            gameover_sound.play()

    
    else:
        # Initialize the surface (gameover)
        gameover_sur = pygame.image.load('background/background.jpg').convert()
        font_over = pygame.font.Font('fonts/Pixeltype.ttf', 100)
        font_choices = pygame.font.Font('fonts/Pixeltype.ttf', 60)

        # game over texts
        textover_sur = font_over.render('GAME OVER', False, (64, 45, 75))
        textover_rec = textover_sur.get_rect(center = (390, 180))

        restart_sur = font_choices.render('RESTART', False, (64, 45, 75))
        restart_rec = restart_sur.get_rect(center = (390, 230))

        yes_sur = font_choices.render('YES', False, (0, 255, 0))
        yes_rec = yes_sur.get_rect(center = (330, 270))
        
        no_sur = font_choices.render('NO', False, (255, 0, 0))
        no_rec = no_sur.get_rect(center = (450, 270))
        
        # Display
        screen.blit(gameover_sur, (0, 0))
        screen.blit(textover_sur, textover_rec)
        screen.blit(restart_sur, restart_rec)
        screen.blit(yes_sur, yes_rec)
        screen.blit(no_sur, no_rec)

        if event.type == pygame.MOUSEBUTTONDOWN and yes_rec.collidepoint(event.pos):
            trash_cleaned, trash_missed = 0, 0  # initialize count
            game_active = True
            bg_music.set_volume(0.2)
            trash_group.empty()
            
            start_time = pygame.time.get_ticks()

        if event.type == pygame.MOUSEBUTTONDOWN and no_rec.collidepoint(event.pos):
            pygame.quit()
            exit()



        



    
    # Draw all our elements
    # Update everything
    pygame.display.update()
    clock.tick(60)


    