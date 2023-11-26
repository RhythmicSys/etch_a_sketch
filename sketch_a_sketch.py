import pygame

# Initialize Pygame and variables
pygame.init()
clock = pygame.time.Clock()
game_running = True
frame_clock = 0
display_width, display_height = 764, 590
drawing_x, drawing_y = 92, 96
drawing_width, drawing_height = 670, 448
dark_gray_color = 22, 22, 22
light_gray_color = 180, 180, 180

# Set up the display
drawing_surface = pygame.Surface((drawing_width, drawing_height))
dust_rectangle = pygame.Rect((80, 80), (700, 448))
drawing_area = pygame.Rect((drawing_x, drawing_y), (drawing_width, drawing_height))
game_display = pygame.display.set_mode((display_width, display_height))
player_position = pygame.Vector2(game_display.get_width() / 2, game_display.get_height() / 2)

# Load assets
dust_image = pygame.image.load("assets/dust.png")
etch_a_sketch_image = pygame.image.load("assets/overlay.svg")

# Blit display images
game_display.blit(dust_image, (80, 80), dust_rectangle)
game_display.blit(etch_a_sketch_image, (0, 0))


# Draw the player's circle
def draw_circle(player_current_position):
    pygame.draw.circle(game_display, dark_gray_color, player_current_position, 3)
    pygame.draw.circle(game_display, light_gray_color, player_current_position, 1)


# Clear the lines from the screen, intentionally leaves a bit of the lines leftover. This can be fixed by setting the
# Alpha to a higher number
def shake_screen():
    shake_image = dust_image
    shake_image.set_alpha(10)
    game_display.blit(shake_image, (80, 80), dust_rectangle)
    game_display.blit(etch_a_sketch_image, (0, 0))


while game_running:
    for event in pygame.event.get():
        # Allows closing the game
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.WINDOWMOVED:
            shake_screen()
    # Draw a circle if the player has moved
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if not player_position.y <= drawing_y + 3:
            player_position.y -= 150 * frame_clock
            draw_circle(player_position)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if not player_position.y >= drawing_height - 3:
            player_position.y += 150 * frame_clock
            draw_circle(player_position)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if not player_position.x <= drawing_x + 3:
            player_position.x -= 150 * frame_clock
            draw_circle(player_position)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if not player_position.x >= drawing_width - 3:
            player_position.x += 150 * frame_clock
            draw_circle(player_position)
    if keys[pygame.K_F5] or keys[pygame.K_ESCAPE]:
        shake_screen()
    # Display the overlay again so the player doesn't draw over it
    game_display.blit(etch_a_sketch_image, (0, 0))
    pygame.display.flip()
    frame_clock = clock.tick(60) / 1000

pygame.quit()
