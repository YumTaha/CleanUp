import pygame
pygame.font.init()
fonts = pygame.font.Font('fonts/Pixeltype.ttf', f'{tuple[100,60]}')

# Get the first value (100) from the list
first_value = fonts[0][0]
print(first_value)

# Get the second value (60) from the list
second_value = fonts[0][1]
print(second_value)
