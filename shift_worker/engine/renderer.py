import pygame
import os

MAP_IMG = None
MAP_WIDTH = MAP_HEIGHT = 0
WORKER_SPRITE = None
from engine.map import TILE_SIZE

def load_map_image():
    global MAP_IMG, MAP_WIDTH, MAP_HEIGHT
    if MAP_IMG is None:
        MAP_IMG = pygame.image.load(os.path.join(os.path.dirname(__file__), '../assets/img/game_map.png')).convert()
        MAP_WIDTH, MAP_HEIGHT = MAP_IMG.get_size()
    return MAP_IMG, MAP_WIDTH, MAP_HEIGHT

def load_worker_sprite():
    global WORKER_SPRITE
    if WORKER_SPRITE is None:
        path = os.path.join(os.path.dirname(__file__), '../assets/img/worker.png')
        img = pygame.image.load(path).convert_alpha()
        WORKER_SPRITE = pygame.transform.scale(img, (TILE_SIZE * 8, TILE_SIZE * 8))
    return WORKER_SPRITE

def render(screen, player_pos, camera_offset=(0, 0)):
    # draw map background
    screen.blit(MAP_IMG, (-camera_offset[0], -camera_offset[1]))

    # worker sprite
    sprite = load_worker_sprite()
    px, py = player_pos
    sw, sh = sprite.get_size()
    screen.blit(sprite, (px - camera_offset[0] - sw // 2, py - camera_offset[1] - sh // 2))