from data.tiles import TILES

INTERACTABLES = {2, 3, 4, 5, 6, 8, 9}

def get_tile_name(tile_id):
    return TILES.get(tile_id, "unknown")

def is_interactable(tile_id):
    return tile_id in INTERACTABLES
