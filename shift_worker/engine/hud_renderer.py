import pygame
from engine.quest_data import QUEST_DATA

class HUDRenderer:
    def __init__(self, font):
        self.font = font
        self.small_font = pygame.font.SysFont(None, 18)

    def draw(self, screen, quest_mgr, inventory, game_map):
        # top-left objective panel
        current = quest_mgr.current
        data = QUEST_DATA.get(current, {"title": current, "description": ""})
        title = data["title"]
        desc = data["description"]

        # progress if applicable
        progress = ""
        if current == "collect_components" and hasattr(game_map, 'total_components'):
            progress = f" ({game_map.collected_count()}/{game_map.total_components()})"

        lines = [f"OBJECTIVE: {title}{progress}", desc]
        y = 20
        for i, line in enumerate(lines):
            txt = self.font.render(line, True, (255, 255, 255) if i == 0 else (200, 200, 200))
            panel = pygame.Surface((txt.get_width() + 20, txt.get_height() + 8), pygame.SRCALPHA)
            panel.fill((10, 10, 20, 180))
            screen.blit(panel, (15, y - 4))
            screen.blit(txt, (25, y))
            y += 28
