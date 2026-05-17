from engine.map import RESTRICTED_X_MIN, RESTRICTED_Y_MAX, RESTRICTED_Y_MIN, RESTRICTED_X_MAX

class Player:
    SPEED = 2
    SIZE = 20

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy, game_map, map_width, map_height):
        new_x = self.x + dx * self.SPEED
        new_y = self.y + dy * self.SPEED
        if game_map.is_walkable(new_x, new_y) and game_map.is_walkable(new_x + self.SIZE - 1, new_y + self.SIZE - 1):
            self.x = new_x
            self.y = new_y
        # hard pixel boundary clamp
        self.x = max(RESTRICTED_X_MIN, min(self.x, RESTRICTED_X_MAX - self.SIZE))
        self.y = max(RESTRICTED_Y_MIN, min(self.y, RESTRICTED_Y_MAX - self.SIZE))