import datetime
import random

import pygame
from datetime import date

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
game_running = True
frame_clock = 0
random_initialized = random.Random()

# Set up the display
display_width = 764
display_height = 590
game_display = pygame.display.set_mode((display_width, display_height))

drawing_x, drawing_y = 100, 110
drawing_width, drawing_height = 565, 485
dust_rectangle = pygame.Rect((80, 80), (600, 500))
drawing_rectangle = pygame.Rect((97, 103), (588, 356))

dark_gray_color = 22, 22, 22
light_gray_color = 180, 180, 180


dust_images = ("assets/dust/dust_background_1.png", "assets/dust/dust_background_2.png",
               "assets/dust/dust_background_3.png", "assets/dust/dust_background_4.png")
random_dust_image = pygame.image.load(dust_images[random_initialized.randint(0, 3)])
etch_a_sketch_image = pygame.image.load("assets/etch_a_sketch/etch_a_sketch_overlay.svg")
game_display.blit(random_dust_image, (80, 80), dust_rectangle)

game_display.blit(etch_a_sketch_image, (0, 0))

player_position = pygame.Vector2(game_display.get_width() / 2, game_display.get_height() / 2)
# pygame.draw.circle(game_display, "blue", (100, 100), 3)
# pygame.draw.circle(game_display, "blue", (660, 100), 3)
# pygame.draw.circle(game_display, "blue", (660, 445), 3)
# pygame.draw.circle(game_display, "blue", (100, 445), 3)
game_display.set_clip(drawing_rectangle)


while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
    pygame.draw.circle(game_display, dark_gray_color, player_position, 3)
    pygame.draw.circle(game_display, light_gray_color, player_position, 1)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if not player_position.y <= drawing_y:
            player_position.y -= 150 * frame_clock
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if not player_position.y >= drawing_height - (drawing_y / 2):
            player_position.y += 150 * frame_clock
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if not player_position.x <= drawing_x + 3:
            player_position.x -= 150 * frame_clock
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if not player_position.x >= drawing_width + (drawing_x - 3):
            player_position.x += 150 * frame_clock
    if keys[pygame.K_F5] or keys[pygame.K_ESCAPE]:
        image = random_dust_image
        image.set_alpha(20)
        game_display.blit(image, (80, 80), dust_rectangle)
        game_display.blit(etch_a_sketch_image, (0, 0))
    if keys[pygame.K_F2]:
        date_string = datetime.datetime.now()
        pygame.image.save(game_display, ("etch_a_sketch_" + str(date_string) + ".png"))

    pygame.display.flip()

    frame_clock = clock.tick(60) / 1000

pygame.quit()
