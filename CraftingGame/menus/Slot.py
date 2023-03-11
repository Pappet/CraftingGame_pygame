import pygame
import CraftingGame.helper.color as color


class Slot:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.item = None
        self.selected = False  # add a 'selected' property
        self.hovering = False
        self.amount = 0
        # change the font to a system font that is available on your system
        self.font_size = 10
        self.font = pygame.font.SysFont("arial", self.font_size)

    def is_empty(self):
        if self.item:
            return False
        else:
            return True

    def add_item(self, item, amount):
        if self.item is None:
            self.item = item
            self.amount = amount
        else:
            if self.item.id == item.id and self.item.stackable:
                self.amount += amount
            else:
                print("this Slot is not empty and the item is not stackable!")
                return

    def remove_item(self, amount):
        item = self.item
        if item is not None:
            if item.stackable and self.amount > amount:
                self.amount -= amount
                return item
            else:
                self.item = None
                self.amount = 0
                self.selected = False
                return item
        else:
            print("this Slot is empty!")
            return None

    def is_clicked(self, pos):
        if self.x <= pos[0] < self.x + self.width and self.y <= pos[1] < self.y + self.height:
            self.selected = True
            return True
        else:
            self.selected = False
            return False

    def get_item_in_slot(self):
        return self.item

    def draw(self, surface):
        pygame.draw.rect(surface, color.dark_gray, self.rect)
        pygame.draw.rect(surface, color.white, self.rect, 1)
        if not self.is_empty():
            surface.blit(self.item.get_image(), self.rect.topleft)
            if self.item.stackable:
                amount_text = self.font.render(
                    f"{self.amount}", True, color.white)
                surface.blit(
                    amount_text, (self.x + self.width - self.font_size, self.y + self.height - self.font_size))
        # draw a selection border, if selected
        if self.selected:
            pygame.draw.rect(surface, color.gold, (self.x - 2,
                                                   self.y - 2, self.width + 4, self.height + 4), 2)
        if self.hovering:
            pygame.draw.rect(surface, color.green, (self.x - 2,
                                                    self.y - 2, self.width + 4, self.height + 4), 2)
