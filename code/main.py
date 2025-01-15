import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
GRAVITY = 1
VISIBILITY_RADIUS = 5

# TODO:
# Сделать нормальные цвета и названия материалов
# Меню главное (в конце уже)
# Сделать счетчик блоков, типо инвентарь. Сломал блок одного вида, тебе добавился в счетчик +1 этого блока
# Health Point
# Ещё подумаем...

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

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Terraria Clone")

WORLD_WIDTH = 2000
WORLD_HEIGHT = 1500

world_width = WORLD_WIDTH // TILE_SIZE
world_height = WORLD_HEIGHT // TILE_SIZE
world = [[0 for _ in range(world_width)] for _ in range(world_height)]

for x in range(world_width):
    world[world_height - 1][x] = 1

player = pygame.Rect(WIDTH // 2, HEIGHT // 2, TILE_SIZE, TILE_SIZE)
player_color = (0, 255, 0)
player_speed = 5
player_velocity_y = 0
is_jumping = False

paused = False

# UPDATE NAME'S OF MATERIAL!!!

BLOCK_TYPES = {
    0: None,
    1: BROWN,
    2: GRAY,
    3: BROWN,
    4: GREEN,
    5: BLUE,
    6: WHITE,
    7: SANDY_BROWN,
    8: SILVER,
    9: RED,
}

current_block_type = 1


def check_collision(rect, dx, dy):
    future_rect = rect.move(dx, dy)
    for y in range(world_height):
        for x in range(world_width):
            if world[y][x] in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if future_rect.colliderect(tile_rect):
                    return True
    return False


running = True
clock = pygame.time.Clock()
camera_x, camera_y = 0, 0

while running:
    screen.fill(SKY_BLUE)
    try:
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
                    if abs(grid_x - player_grid_x) <= VISIBILITY_RADIUS and abs(
                            grid_y - player_grid_y) <= VISIBILITY_RADIUS:
                        if event.button == 1:
                            world[grid_y][grid_x] = 0
                        elif event.button == 3:
                            if world[grid_y][grid_x] == 0:
                                world[grid_y][grid_x] = current_block_type

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                current_block_type += 1
                if current_block_type > len(BLOCK_TYPES) - 1:
                    current_block_type = 1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                current_block_type -= 1
                if current_block_type < 1:
                    current_block_type = len(BLOCK_TYPES) - 1
    except:
        print("")

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

    camera_x = player.x - WIDTH // 2 + TILE_SIZE // 2
    camera_y = player.y - HEIGHT // 2 + TILE_SIZE // 2

    camera_x = max(0, min(camera_x, WORLD_WIDTH - WIDTH))
    camera_y = max(0, min(camera_y, WORLD_HEIGHT - HEIGHT))

    for y in range(world_height):
        for x in range(world_width):
            rect = pygame.Rect(x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y, TILE_SIZE, TILE_SIZE)
            block_color = BLOCK_TYPES.get(world[y][x])
            if block_color is not None:
                pygame.draw.rect(screen, block_color, rect)

            player_grid_x = player.x // TILE_SIZE
            player_grid_y = player.y // TILE_SIZE
            if abs(x - player_grid_x) <= VISIBILITY_RADIUS and abs(y - player_grid_y) <= VISIBILITY_RADIUS:
                pygame.draw.rect(screen, LIGHT_GRAY, rect, 1)
            else:
                pygame.draw.rect(screen, GRAY, rect, 1)

    pygame.draw.rect(screen, player_color, player.move(-camera_x, -camera_y))

    font = pygame.font.SysFont(None, 36)
    block_type_text = font.render(f"Current Block: {current_block_type}", True, BLACK)
    screen.blit(block_type_text, (10, 10))

    if paused:
        font = pygame.font.SysFont(None, 55)
        text = font.render("Paused", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
