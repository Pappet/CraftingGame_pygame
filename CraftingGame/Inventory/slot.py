import pygame
import helper.color as color


class Slot:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.item = None
        self.selected = False  # add a 'selected' property

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

         # draw a selection border, if selected
        if self.selected:
            pygame.draw.rect(surface, color.gold, (self.x - 2,
                             self.y - 2, self.width + 4, self.height + 4), 2)
