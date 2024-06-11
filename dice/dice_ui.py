import random
import pygame

class DiceUI:
    def __init__(self, x_pos, y_pos, num, key, screen):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.number = num
        self.key = key
        self.active = False
        self.die = ''
        self.screen = screen

    def update_number(self, num):
        self.number = num

    def update_active(self, value):
        self.active = value

    def draw(self):
        self.die = pygame.draw.rect(self.screen, (255, 255, 255), [self.x_pos, self.y_pos, 100, 100], 0, 10)
        if self.number == 1:
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 50, self.y_pos + 50), 10)
        if self.number == 2:
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 20, self.y_pos + 20), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 80, self.y_pos + 80), 10)
        if self.number == 3:
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 50, self.y_pos + 50), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 20, self.y_pos + 20), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 80, self.y_pos + 80), 10)
        if self.number == 4:
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 20, self.y_pos + 20), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 80, self.y_pos + 80), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 20, self.y_pos + 80), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 80, self.y_pos + 20), 10)
        if self.number == 5:
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 50, self.y_pos + 50), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 20, self.y_pos + 20), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 80, self.y_pos + 80), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 20, self.y_pos + 80), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 80, self.y_pos + 20), 10)
        if self.number == 6:
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 20, self.y_pos + 50), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 80, self.y_pos + 50), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 20, self.y_pos + 20), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 80, self.y_pos + 80), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 20, self.y_pos + 80), 10)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x_pos + 80, self.y_pos + 20), 10)
        if self.active:
            pygame.draw.rect(self.screen, (20, 20, 20), [self.x_pos, self.y_pos, 100, 100], 5, 10)
