import pygame
import os
from main_menu import main_menu

pygame.init()

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
GRAVITY = 1
VISIBILITY_RADIUS = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BROWN = (139, 69, 19)
LIGHT_GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SANDY_BROWN = (210, 180, 140)
SILVER = (192, 192, 192)
RED = (255, 0, 0)
SKY_BLUE = (135, 206, 235)
DARK_BLUE = (25, 25, 112)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Terraria Clone")

with open("map.txt", "r") as file:
    world = [list(map(int, line.strip())) for line in file if line.strip()]

world_height = len(world)
world_width = len(world[0]) if world_height > 0 else 0

player = pygame.Rect(40, 30, TILE_SIZE, TILE_SIZE)
player_color = (0, 255, 0)
player_speed = 5
player_velocity_y = 0
is_jumping = False

paused = False
current_block_type = 1

textures = {
    1: pygame.image.load(os.path.join('textures', 'dirt.png')).convert_alpha(),
    2: pygame.image.load(os.path.join('textures', 'stone.png')).convert_alpha(),
    3: pygame.image.load(os.path.join('textures', 'wood.png')).convert_alpha(),
    4: pygame.image.load(os.path.join('textures', 'grass.png')).convert_alpha(),
    5: [],  # Вода (анимация)
    6: pygame.image.load(os.path.join('textures', 'snow.png')).convert_alpha(),
    7: pygame.image.load(os.path.join('textures', 'sand.png')).convert_alpha(),
    8: pygame.image.load(os.path.join('textures', 'metal.png')).convert_alpha(),
    9: [],  # Лава (анимация)
}

# Загрузка кадров анимации для воды и лавы
water_frames = [
    pygame.image.load(os.path.join('textures', f'water_{i}.png')).convert_alpha()
    for i in range(1, 4)  # water_1.png, water_2.png, water_3.png
]
lava_frames = [
    pygame.image.load(os.path.join('textures', f'lava_{i}.png')).convert_alpha()
    for i in range(1, 4)  # lava_1.png, lava_2.png, lava_3.png
]

for key in textures:
    if key == 5:  
        textures[5] = [pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE)) for frame in water_frames]
    elif key == 9: 
        textures[9] = [pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE)) for frame in lava_frames]
    elif textures[key]:
        textures[key] = pygame.transform.scale(textures[key], (TILE_SIZE, TILE_SIZE))

# Таймер для анимации
animation_frame = 0
animation_speed = 10 

# Функция проверки коллизий
def check_collision(rect, dx, dy):
    future_rect = rect.move(dx, dy)
    for y in range(world_height):
        for x in range(world_width):
            if world[y][x] in textures and world[y][x] != 0:
                tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if future_rect.colliderect(tile_rect):
                    return True
    return False

def interpolate_color(color1, color2, factor):
    return tuple(int(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3))

def game_over_screen():
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 74)
        text = font.render("Game Over", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        font_small = pygame.font.SysFont(None, 36)
        restart_text = font_small.render("Press R to Restart", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  
                    return True

def game_loop():
    player_velocity_y = 0
    global paused, current_block_type, animation_frame

    running = True
    clock = pygame.time.Clock()
    camera_x, camera_y = 0, 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = (mouse_x + camera_x) // TILE_SIZE
                grid_y = (mouse_y + camera_y) // TILE_SIZE

                if 0 <= grid_x < world_width and 0 <= grid_y < world_height:
                    player_grid_x = player.x // TILE_SIZE
                    player_grid_y = player.y // TILE_SIZE
                    if abs(grid_x - player_grid_x) <= VISIBILITY_RADIUS and abs(grid_y - player_grid_y) <= VISIBILITY_RADIUS:
                        if event.button == 1:
                            world[grid_y][grid_x] = 0
                        elif event.button == 3:
                            if world[grid_y][grid_x] == 0:
                                world[grid_y][grid_x] = current_block_type

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                current_block_type += 1
                if current_block_type > len(textures):
                    current_block_type = 1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                current_block_type -= 1
                if current_block_type < 1:
                    current_block_type = len(textures)

        if not paused:
            keys = pygame.key.get_pressed()
            dx = 0
            dy = player_velocity_y

            if keys[pygame.K_a]:
                dx -= player_speed
            if keys[pygame.K_d]:
                dx += player_speed
            if keys[pygame.K_w] and not is_jumping:
                player_velocity_y = -15
                is_jumping = True

            if not check_collision(player, dx, 0):
                player.x += dx

            player_velocity_y += GRAVITY
            if player_velocity_y > 10:
                player_velocity_y = 10

            if not check_collision(player, 0, dy):
                player.y += dy
            else:
                if dy > 0:
                    player_velocity_y = 0
                    is_jumping = False
                elif dy < 0:
                    player_velocity_y = 0

            if player.y >= world_height * TILE_SIZE:
                if game_over_screen(): 
                    player.x, player.y = 40, 30
                    player_velocity_y = 0
                    is_jumping = False
                    continue  
                else:
                    running = False  

        animation_frame += 1
        if animation_frame >= animation_speed * len(textures[5]):
            animation_frame = 0

        camera_x = player.x - WIDTH // 2 + TILE_SIZE // 2
        camera_y = player.y - HEIGHT // 2 + TILE_SIZE // 2

        camera_x = max(0, min(camera_x, world_width * TILE_SIZE - WIDTH))
        camera_y = max(0, min(camera_y, world_height * TILE_SIZE - HEIGHT))

        height_factor = min(max(camera_y / (world_height * TILE_SIZE), 0), 1)
        background_color = interpolate_color(SKY_BLUE, DARK_BLUE, height_factor)
        screen.fill(background_color)

        start_x = max(0, camera_x // TILE_SIZE)
        end_x = min(world_width, (camera_x + WIDTH) // TILE_SIZE + 1)
        start_y = max(0, camera_y // TILE_SIZE)
        end_y = min(world_height, (camera_y + HEIGHT) // TILE_SIZE + 1)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                rect = pygame.Rect(x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y, TILE_SIZE, TILE_SIZE)
                block_type = world[y][x]
                if block_type in textures:
                    if block_type == 5:  # Вода
                        frame_index = (animation_frame // animation_speed) % len(textures[5])
                        screen.blit(textures[5][frame_index], rect.topleft)
                    elif block_type == 9:  # Лава
                        frame_index = (animation_frame // animation_speed) % len(textures[9])
                        screen.blit(textures[9][frame_index], rect.topleft)
                    else:
                        screen.blit(textures[block_type], rect.topleft)

        pygame.draw.rect(screen, player_color, player.move(-camera_x, -camera_y))

        Names = {
            0: None,
            1: 'Земля',
            2: 'Камень',
            3: 'Дерево',
            4: 'Трава',
            5: 'Вода',
            6: 'Снег',
            7: 'Песок',
            8: 'Железо',
            9: 'Лава',
        }

        font = pygame.font.SysFont('Comic Sans MS', 30)
        block_type_text = font.render(f"{Names[current_block_type]}", True, BLACK)
        screen.blit(block_type_text, (10, 10))

        if paused:
            font = pygame.font.SysFont('Comic Sans MS', 48)
            text = font.render("Paused", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    result = main_menu()
    if result == "singleplayer":
        game_loop()
    elif result == "multiplayer":
        print("Многопользовательская игра пока не реализована.")