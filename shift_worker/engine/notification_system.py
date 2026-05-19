import pygame
import time

class NotificationSystem:
    def __init__(self):
        self.queue = []
        self.current = None
        self.start_time = 0
        self.duration = 3.0  # seconds

    def show(self, message, duration=None):
        if duration:
            self.duration = duration
        self.queue.append(message)

    def update(self):
        now = time.time()
        if self.current is None and self.queue:
            self.current = self.queue.pop(0)
            self.start_time = now
        elif self.current and (now - self.start_time > self.duration):
            self.current = None

    def draw(self, screen, font):
        if self.current:
            text = font.render(self.current, True, (255, 255, 255))
            rect = text.get_rect(center=(screen.get_width() // 2, 80))
            # semi-transparent bg
            bg = pygame.Surface((rect.width + 40, rect.height + 20), pygame.SRCALPHA)
            bg.fill((20, 20, 30, 200))
            screen.blit(bg, (rect.x - 20, rect.y - 10))
            screen.blit(text, rect)
