import noise
import random

WIDTH = 100  
HEIGHT = 100  
AIR_LAYERS = 15  
TILE_SIZE = 40  
CAVE_THRESHOLD = 0.45  
SCALE = 20.0  
OCTAVES = 8  
PERSISTENCE = 0.5  
LACUNARITY = 2.0  
SECOND_LAYER_HEIGHT = 60  

def smoothstep(x):
    return x * x * (3 - 2 * x)

def generate_map(width, height, air_layers, cave_threshold, second_layer_height, seed):
    world = [[0] * width for _ in range(height)]
    
    for y in range(air_layers):
        for x in range(width):
            world[y][x] = 0  

    for y in range(air_layers, height):
        for x in range(width):
            nx = x / SCALE
            ny = y / SCALE
            perlin_value = noise.pnoise2(
                nx, ny, octaves=OCTAVES, persistence=PERSISTENCE, lacunarity=LACUNARITY, repeatx=1024, repeaty=1024, base=seed
            )
            normalized_value = smoothstep((perlin_value + 1) / 2)

            if normalized_value < cave_threshold:
                world[y][x] = 0  
            else:
                if y >= second_layer_height:
                    world[y][x] = 2  
                else:
                    world[y][x] = 1  

    return world


seed = random.randint(0, 10000) 

world = generate_map(WIDTH, HEIGHT, AIR_LAYERS, CAVE_THRESHOLD, SECOND_LAYER_HEIGHT, seed)

with open("map.txt", "w") as file:
    for row in world:
        file.write("".join(str(cell) for cell in row) + "\n")

print(f" {seed} ")
