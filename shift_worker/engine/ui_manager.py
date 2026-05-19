from engine.notification_system import NotificationSystem
from engine.hud_renderer import HUDRenderer

class UIManager:
    def __init__(self, screen, font):
        self.notifications = NotificationSystem()
        self.hud = HUDRenderer(font)
        self.screen = screen

    def update(self):
        self.notifications.update()

    def draw(self, quest_mgr, inventory, game_map):
        self.hud.draw(self.screen, quest_mgr, inventory, game_map)
        self.notifications.draw(self.screen, self.hud.font)

    def notify(self, message):
        self.notifications.show(message)
