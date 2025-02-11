import pygame
from pygame.display import set_icon

# Initialize Pygame and variables
pygame.init()
clock = pygame.time.Clock()
game_running = True
frame_clock = 0
# Display stuff
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Load assets
dust_image = pygame.image.load("assets/dust.png")
icon_image = pygame.image.load("assets/icon.png")
pre_load_overlay = pygame.image.load("assets/overlay.png")
set_icon(icon_image)
scale = (WIDTH, HEIGHT)
overlay_image = pygame.transform.scale(pre_load_overlay, scale)
overlay_mask = pygame.mask.from_surface(overlay_image)
overlay_mask.invert()

def out_of_bounds(position_x, position_y):
    if overlay_mask.get_at((position_x, position_y)):
        return False
    else:
        return True

mask_width, mask_height = 0, 0

def find_mask_width():
    current_mask_width = WIDTH
    for x in range(0, WIDTH):
       if not out_of_bounds(x, HEIGHT / 2):
           current_mask_width -= 1
    global mask_width
    mask_width = current_mask_width

def find_mask_height():
    current_mask_height = HEIGHT
    for y in range(0, HEIGHT):
        if not out_of_bounds(y, WIDTH / 2):
            current_mask_height -= 1
    global mask_height
    mask_height = current_mask_height

find_mask_width()
find_mask_height()


# Set up the display
drawing_width = WIDTH - mask_width
drawing_height = HEIGHT - mask_height
drawing_display_origin_x = mask_width / 2
drawing_display_origin_y = mask_height / 2
drawing_surface = pygame.Surface((WIDTH, HEIGHT))
dust_rectangle = pygame.Rect(drawing_display_origin_x, drawing_display_origin_y, drawing_width, drawing_height)
overlay_rectangle = pygame.Rect((0,0), (WIDTH, HEIGHT))
game_display = pygame.display.set_mode((WIDTH, HEIGHT))
player_position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)


dark_gray_color = 22, 22, 22
light_gray_color = 180, 180, 180


def draw_dust_within_mask():
    dust_scaled = pygame.transform.scale(dust_image, (drawing_width, drawing_height))
    game_display.blit(dust_scaled, dust_rectangle)


# Blit display images
def refresh_images():
    draw_dust_within_mask()
    game_display.blit(overlay_image, (0, 0), overlay_rectangle)


refresh_images()


# Draw the player's circle
def draw_circle(player_current_position):
    pygame.draw.circle(game_display, dark_gray_color, player_current_position, 3)
    pygame.draw.circle(game_display, light_gray_color, player_current_position, 1)


def key_pressed(key_press):
        if key_press[pygame.K_UP] or key_press[pygame.K_w]:
            move_up()
        if key_press[pygame.K_DOWN] or key_press[pygame.K_s]:
            move_down()
        if key_press[pygame.K_LEFT] or key_press[pygame.K_a]:
            move_left()
        if key_press[pygame.K_RIGHT] or key_press[pygame.K_d]:
            move_right()
        if key_press[pygame.K_F5] or key_press[pygame.K_ESCAPE] or key_press[pygame.K_SPACE]:
            shake_screen()


def move_up():
    if out_of_bounds(player_position.x, player_position.y - 3):
        return False
    player_position.y -= 150 * frame_clock
    draw_circle(player_position)

def move_down():
    if out_of_bounds(player_position.x, player_position.y + 3):
        return False
    player_position.y += 150 * frame_clock
    draw_circle(player_position)


def move_left():
    if out_of_bounds(player_position.x - 3, player_position.y):
        return False
    player_position.x -= 150 * frame_clock
    draw_circle(player_position)


def move_right():
    if out_of_bounds(player_position.x + 3, player_position.y):
        return False
    player_position.x += 150 * frame_clock
    draw_circle(player_position)


# Clear the lines from the screen, intentionally leaves a bit of the lines leftover. This can be fixed by setting the
# Alpha to a higher number
def shake_screen():
    shake_image = dust_image
    shake_image.set_alpha(10)
    refresh_images()


def window_shake(x_moved, y_moved):
    total_moved = x_moved + y_moved
    total_moved = total_moved / 100
    for iteration in range(int (total_moved)):
        shake_screen()


while game_running:
    for event in pygame.event.get():
        # Allows closing the game
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.WINDOWMOVED:
            window_shake(event.x, event.y)
    # Draw a circle if the player has moved
    keys = pygame.key.get_pressed()
    key_pressed(keys)
    # Display the overlay again so the player doesn't draw over it
    game_display.blit(overlay_image, (0, 0))
    pygame.display.flip()
    frame_clock = clock.tick(60) / 1000

pygame.quit()
