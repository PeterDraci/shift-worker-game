class Inventory:
    def __init__(self):
        self.components = 0
        self.device = False

    def add_component(self):
        self.components += 1

    def has_components(self, count):
        return self.components >= count

    def assemble_device(self, game_map=None):
        if game_map and game_map.all_components_collected():
            self.device = True
            self.components = 0
            return True
        return False

    def reset(self):
        self.components = 0
        self.device = False
