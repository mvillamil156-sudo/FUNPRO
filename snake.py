import pygame
import random
import math

#inicio
pygame.init()

#settings
WIDTH, HEIGHT = 600, 600
TILE = 25
BASE_SPEED = 10
FONT = pygame.font.SysFont("arial", 24)

#Colores 
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (200, 0, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 140, 0)

#ventana
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Evolutiva")

#obj principipales
FOOD = 1
BOOST = 2
SLOW = 3
COLOR = 4

def new_object():
    x = random.randrange(0, WIDTH // TILE) * TILE
    y = random.randrange(0, HEIGHT // TILE) * TILE
    obj_type = random.choice([FOOD, BOOST, SLOW, COLOR])
    return {"pos": (x, y), "type": obj_type}

def draw_object(obj):
    color = {FOOD: RED, BOOST: YELLOW, SLOW: BLUE, COLOR: PURPLE}[obj["type"]]
    pygame.draw.rect(win, color, (obj["pos"][0], obj["pos"][1], TILE, TILE))

#inicio del juego
snake = [(5 * TILE, 5 * TILE)]
direction = (TILE, 0)
speed = BASE_SPEED
snake_color = GREEN
level = 1
object_data = new_object()
score = 0
running = True
monster_active = False
monster_pos = [random.randint(0, WIDTH // TILE - 1) * TILE,
               random.randint(0, HEIGHT // TILE - 1) * TILE]

clock = pygame.time.Clock()

#funcion del texto
def draw_text(text, x, y, color=WHITE):
    label = FONT.render(text, True, color)
    win.blit(label, (x, y))

#funcion del monstruo
def move_monster(monster_pos, target_pos, speed=1):
    mx, my = monster_pos
    tx, ty = target_pos
    dx, dy = tx - mx, ty - my
    dist = math.hypot(dx, dy)
    if dist == 0:
        return monster_pos
    mx += speed * (dx / dist)
    my += speed * (dy / dist)
    # teletransportarse al otro lado del mapa si se sale
    mx %= WIDTH
    my %= HEIGHT
    return [mx, my]


while running:
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #controles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, TILE):
        direction = (0, -TILE)
    elif keys[pygame.K_DOWN] and direction != (0, -TILE):
        direction = (0, TILE)
    elif keys[pygame.K_LEFT] and direction != (TILE, 0):
        direction = (-TILE, 0)
    elif keys[pygame.K_RIGHT] and direction != (-TILE, 0):
        direction = (TILE, 0)

    #movimiento
    head_x, head_y = snake[0]
    new_head = ((head_x + direction[0]) % WIDTH, (head_y + direction[1]) % HEIGHT)
    snake.insert(0, new_head)

    #colision consigo misma
    if new_head in snake[1:]:
        running = False
        break

    #colision de objetos
    if new_head == object_data["pos"]:
        score += 1
        if object_data["type"] == FOOD:
            level += 1
        elif object_data["type"] == BOOST:
            speed += 2
        elif object_data["type"] == SLOW:
            speed = max(5, speed - 2)
        elif object_data["type"] == COLOR:
            snake_color = random.choice([GREEN, PURPLE, YELLOW, BLUE, WHITE, ORANGE])

        object_data = new_object()
    else:
        snake.pop()

    #nivel 10-monstruo
    if level >= 10:
        monster_active = True
        monster_pos = move_monster(monster_pos, snake[0], speed=1.2)

    #monstruo
    if monster_active:
        mx, my = monster_pos
        hx, hy = snake[0]
        if abs(mx - hx) < TILE and abs(my - hy) < TILE:
            running = False  # pierde si el monstruo lo toca
            break

    
    win.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(win, snake_color, (segment[0], segment[1], TILE, TILE))

    draw_object(object_data)

    if monster_active:
        pygame.draw.rect(win, ORANGE, (monster_pos[0], monster_pos[1], TILE, TILE))

    
    draw_text(f"Puntaje: {score}", 10, 10)
    draw_text(f"Nivel: {level}", 10, 40)
    draw_text(f"Velocidad: {speed}", 10, 70)

    pygame.display.update()

# Final
win.fill(BLACK)
draw_text("¡Perdiste!", WIDTH // 2 - 60, HEIGHT // 2 - 20, RED)
draw_text(f"Nivel alcanzado: {level}", WIDTH // 2 - 80, HEIGHT // 2 + 20, WHITE)
pygame.display.update()
pygame.time.wait(3000)
pygame.quit()

win.fill(BLACK)
for segment in snake:
    pygame.draw.rect(win, snake_color, (segment[0], segment[1], TILE, TILE))
    draw_object(object_data)

    pygame.display.update()

pygame.quit()
