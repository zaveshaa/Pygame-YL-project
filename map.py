import pygame
import json

pygame.init()

WIDTH, HEIGHT = 1600, 1200
TILE_SIZE = 20
BLOCK_TYPES = {
    0: None,
    1: (139, 69, 19),
    2: (100, 100, 100),
    3: (0, 255, 0),
    4: (0, 0, 255),
    5: (210, 180, 140),
    6: (192, 192, 192),
    7: (255, 0, 0),
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Map Editor")

world_width = WIDTH // TILE_SIZE
world_height = HEIGHT // TILE_SIZE

world = [[0 for _ in range(world_width)] for _ in range(world_height)]

current_block_type = 1
is_dragging = False

font = pygame.font.SysFont(None, 36)

def draw_map():
    for y in range(world_height):
        for x in range(world_width):
            block_color = BLOCK_TYPES.get(world[y][x])
            if block_color:
                pygame.draw.rect(screen, block_color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def save_map():
    with open("map.txt", "w") as file:
        for row in world:
            file.write("".join(str(cell) for cell in row) + "\n")

running = True
while running:
    screen.fill((255, 255, 255))
    draw_map()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                current_block_type += 1
                if current_block_type > len(BLOCK_TYPES) - 1:
                    current_block_type = 1

            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                ctrl_pressed = True

            if event.key == pygame.K_s and ctrl_pressed:
                save_map()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                ctrl_pressed = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // TILE_SIZE
            grid_y = mouse_y // TILE_SIZE

            if event.button == 1:
                if 0 <= grid_x < world_width and 0 <= grid_y < world_height:
                    world[grid_y][grid_x] = current_block_type
                    is_dragging = True

            if event.button == 3:
                if 0 <= grid_x < world_width and 0 <= grid_y < world_height:
                    world[grid_y][grid_x] = 0
                    is_dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            is_dragging = False

        if event.type == pygame.MOUSEMOTION and is_dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // TILE_SIZE
            grid_y = mouse_y // TILE_SIZE

            if 0 <= grid_x < world_width and 0 <= grid_y < world_height:
                world[grid_y][grid_x] = current_block_type

    block_type_text = font.render(f"Current Block: {current_block_type}", True, (0, 0, 0))
    screen.blit(block_type_text, (10, 10))

    save_text = font.render("Save (Ctrl + S)", True, (0, 0, 0))
    screen.blit(save_text, (WIDTH - 200, 10))

    pygame.display.flip()

pygame.quit()