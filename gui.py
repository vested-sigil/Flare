import pygame
from pygame.locals import *


class Window:
    def __init__(self):
        pygame.init()
        self.open = True
        self.size = (800, 600)
        self.title = "Window"
        self.controls = []
        self.ui_manager = UIManager()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)

    def add_control(self, control):
        self.controls.append(control)

    def set_size(self, width, height):
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size)

    def set_title(self, title):
        self.title = title
        pygame.display.set_caption(self.title)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        for control in self.controls:
            control.draw(self.screen)
        self.ui_manager.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.open:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.open = False
                self.ui_manager.handle_event(event)
            self.ui_manager.update()
            self.draw()

