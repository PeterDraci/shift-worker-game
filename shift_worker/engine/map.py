import json
from data.level import level
from data.tiles import TILES

TILE_SIZE = 8
RESTRICTED_X_MIN = 80
RESTRICTED_Y_MIN = 100
RESTRICTED_X_MAX = 1440
RESTRICTED_Y_MAX = 810

class Map:
    def __init__(self):
        coarse = [row[:] for row in level]
        h = len(coarse)
        w = len(coarse[0])
        # upscale 2x for precision
        self.grid = []
        for row in coarse:
            new_row1 = []
            new_row2 = []
            for tile in row:
                new_row1.extend([tile, tile])
                new_row2.extend([tile, tile])
            self.grid.append(new_row1)
            self.grid.append(new_row2)
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.objects = {}
        self.components = {}
        self._restrict_playable_area(RESTRICTED_X_MIN, RESTRICTED_Y_MIN, RESTRICTED_X_MAX, RESTRICTED_Y_MAX)
        self.spawn_pos = self._find_spawn()
        self._detect_components()

    def _find_spawn(self):
        for ty, row in enumerate(self.grid):
            for tx, tile in enumerate(row):
                if tile == 2:
                    return (tx * TILE_SIZE + TILE_SIZE // 2, ty * TILE_SIZE + TILE_SIZE // 2)
        # fallback inside playable rect on free tile (row3,col3=0)
        return (3 * TILE_SIZE + TILE_SIZE // 2, 3 * TILE_SIZE + TILE_SIZE // 2)

    def _restrict_playable_area(self, min_px, min_py, max_px, max_py):
        min_tx = min_px // TILE_SIZE
        min_ty = min_py // TILE_SIZE
        max_tx = max_px // TILE_SIZE
        max_ty = max_py // TILE_SIZE
        for ty in range(self.height):
            for tx in range(self.width):
                if not (min_tx <= tx <= max_tx and min_ty <= ty <= max_ty):
                    self.grid[ty][tx] = 1
                # inside: keep original values (0 free, 1 wall, 2 spawn etc.)

    def is_walkable(self, x, y):
        tx = x // TILE_SIZE
        ty = y // TILE_SIZE
        if not (0 <= tx < self.width and 0 <= ty < self.height):
            return False
        tile = self.grid[ty][tx]
        return tile != 1  # walls block, everything else (0,2..9) allows per TILES

    def get_tile(self, x, y):
        tx = x // TILE_SIZE
        ty = y // TILE_SIZE
        if 0 <= tx < self.width and 0 <= ty < self.height:
            return self.grid[ty][tx]
        return 1

    def place_object(self, tx, ty, obj_type):
        if 0 <= tx < self.width and 0 <= ty < self.height:
            self.grid[ty][tx] = obj_type
            self.objects[(tx, ty)] = obj_type

    def load_from_file(self, filepath):
        with open(filepath) as f:
            data = json.load(f)
        self.width = data['width']
        self.height = data['height']
        self.grid = data['grid']
        self.objects = {tuple(k): v for k, v in data.get('objects', {}).items()}

    def _detect_components(self):
        self.components = {}
        for ty in range(self.height):
            for tx in range(self.width):
                if self.grid[ty][tx] == 4:
                    self.components[(tx, ty)] = False  # not collected

    def collect_component(self, tx, ty):
        key = (tx, ty)
        if key in self.components and not self.components[key]:
            self.components[key] = True
            self.grid[ty][tx] = 0  # remove visually
            return True
        return False

    def collected_count(self):
        return sum(1 for v in self.components.values() if v)

    def total_components(self):
        return len(self.components)

    def all_components_collected(self):
        return self.total_components() > 0 and all(self.components.values())