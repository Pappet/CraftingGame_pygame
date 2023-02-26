import pygame
import helper.color as color


class Slot:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.item = None

    def is_empty(self):
        return self.item is None

    def add_item(self, item):
        if self.item == None:
            self.item = item
        else:
            print("this Slot is not empty!")
            return

    def remove_item(self):
        item = self.item
        if item is not None:
            self.item = None
            return item
        else:
            print("this Slot is empty!")
            return

    def draw(self, surface):
        pygame.draw.rect(surface, color.white, self.rect, 1)
        if not self.is_empty():
            surface.blit(self.item.get_image(), self.rect.topleft)
