import pygame
import sys
from engine.renderer import render, load_map_image, DEBUG_COLORS
from engine.player import Player
from engine.map import RESTRICTED_X_MIN, RESTRICTED_Y_MAX, RESTRICTED_Y_MIN, RESTRICTED_X_MAX, Map, TILE_SIZE
from engine.quest_manager import QuestManager
from engine.inventory_system import Inventory
from engine.interaction import handle_interaction, get_nearby_interactable
from engine.ui_manager import UIManager

pygame.init()
# screen size (windowed view)
SCREEN_WIDTH, SCREEN_HEIGHT = 1536, 1024
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shift Worker")
clock = pygame.time.Clock()

# load visual map
MAP_IMG, MAP_WIDTH, MAP_HEIGHT = load_map_image()

# logical map (decoupled) - uses numeric grid from data/level.py
game_map = Map()
player = Player(130, 150)
quest_mgr = QuestManager()
inventory = Inventory()

font = pygame.font.SysFont(None, 24)
interact_font = pygame.font.SysFont(None, 20)
ui = UIManager(screen, font)
visited_triggers = set()

DEBUG_MODE = True
running = True
speed = 2
up_pressed = down_pressed = left_pressed = right_pressed = False
prev_x, prev_y = player.x, player.y
while running:
    pygame.event.pump()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if DEBUG_MODE:
                print("KEYDOWN:", event.key)
            if event.key == pygame.K_UP: up_pressed = True
            if event.key == pygame.K_DOWN: down_pressed = True
            if event.key == pygame.K_LEFT: left_pressed = True
            if event.key == pygame.K_RIGHT: right_pressed = True
            if event.key == pygame.K_e:
                msg = handle_interaction(pygame.K_e, player, game_map, quest_mgr, inventory)
                if msg:
                    ui.notify(msg)
                if DEBUG_MODE and msg:
                    print("INTERACT:", msg)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP: up_pressed = False
            if event.key == pygame.K_DOWN: down_pressed = False
            if event.key == pygame.K_LEFT: left_pressed = False
            if event.key == pygame.K_RIGHT: right_pressed = False

    # Movement using event-tracked state + map collision
    dx, dy = 0, 0
    if left_pressed: dx = -speed
    if right_pressed: dx = speed
    if up_pressed: dy = -speed
    if down_pressed: dy = speed

    if dx or dy:
        # explicit tile conversion + grid authoritative check
        new_x = player.x + dx
        new_y = player.y + dy
        tile_x = int(new_x // TILE_SIZE)
        tile_y = int(new_y // TILE_SIZE)
        if 0 <= tile_x < game_map.width and 0 <= tile_y < game_map.height:
            tile = game_map.grid[tile_y][tile_x]
            if tile != 1:
                player.x = new_x
                player.y = new_y
                if tile == 3 and DEBUG_MODE:
                    print("RESOURCE DETECTED")
        # hard bounds
        player.x = max(RESTRICTED_X_MIN, min(player.x, RESTRICTED_X_MAX - player.SIZE))
        player.y = max(RESTRICTED_Y_MIN, min(player.y, RESTRICTED_Y_MAX - player.SIZE))

    # trigger zone (tile 7) support
    tx = int(player.x // TILE_SIZE)
    ty = int(player.y // TILE_SIZE)
    if (tx, ty) not in visited_triggers:
        if 0 <= tx < game_map.width and 0 <= ty < game_map.height:
            tile = game_map.grid[ty][tx]
            if tile == 7:
                ui.notify("Entering restricted sector...")
                visited_triggers.add((tx, ty))

    if DEBUG_MODE and (player.x != prev_x or player.y != prev_y):
        print("POS CHANGED:", player.x, player.y)
    prev_x, prev_y = player.x, player.y

    ui.update()

    # Render
    cam_x = max(0, min(player.x - SCREEN_WIDTH // 2, MAP_WIDTH - SCREEN_WIDTH))
    cam_y = max(0, min(player.y - SCREEN_HEIGHT // 2, MAP_HEIGHT - SCREEN_HEIGHT))
    screen.fill((0, 0, 0))
    render(screen, (player.x, player.y), (cam_x, cam_y))

    # Debug overlay for logical grid (walls red, resources green)
    if DEBUG_MODE:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for ty in range(game_map.height):
            for tx in range(game_map.width):
                tile = game_map.grid[ty][tx]
                sx = tx * TILE_SIZE - cam_x
                sy = ty * TILE_SIZE - cam_y
                if sx + TILE_SIZE < 0 or sx > SCREEN_WIDTH or sy + TILE_SIZE < 0 or sy > SCREEN_HEIGHT:
                    continue
                if tile == 1:
                    pygame.draw.rect(overlay, (255, 0, 0, 80), (sx, sy, TILE_SIZE, TILE_SIZE))
                elif tile in DEBUG_COLORS:
                    pygame.draw.rect(overlay, (*DEBUG_COLORS[tile], 120), (sx, sy, TILE_SIZE, TILE_SIZE))
        screen.blit(overlay, (0, 0))

    hud = font.render(f"Pos: {player.x}, {player.y}", True, (255, 255, 255))
    screen.blit(hud, (10, SCREEN_HEIGHT - 30))

    # interaction prompt
    nearby = get_nearby_interactable(player, game_map)
    if nearby:
        prompt = interact_font.render("Press E to interact", True, (255, 255, 0))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 80))

    ui.draw(quest_mgr, inventory, game_map)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()