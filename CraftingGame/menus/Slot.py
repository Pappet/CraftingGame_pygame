import pygame
import CraftingGame.helper.color as color


class Slot:
    def __init__(self, x, y, width, height, font_size=10):
        self.rect = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.update_rect()
        # -------------------------------------------
        self.item = None        # is there an item in the slo?
        self.selected = False   # is the Slot selected
        self.hovering = False   # where is the mouse hovering while dragging
        self.amount = 0         # how much of the item is int the slot
        # change the font to a system font that is available on your system
        self.font_size = font_size
        self.font = pygame.font.SysFont("arial", self.font_size)

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def is_empty(self):
        return not bool(self.item)

    def add_item(self, item, amount):
        if self.item is None:
            self.item = item
            self.amount = amount
        else:
            if self.item.id == item.id and self.item.stackable:
                self.amount += amount
            else:
                print("this Slot is not empty and the item is not stackable!")

    def remove_item(self, amount):
        item = self.item
        if item is not None:
            if item.stackable and self.amount > amount:
                self.amount -= amount
                if self.amount == 0:
                    self.item = None
                    self.selected = False
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
        if self.rect.collidepoint(pos):
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
                amount_text = self.font.render(f"{self.amount}", True, color.white)
                surface.blit(amount_text, (self.x + self.width - self.font_size, self.y + self.height - self.font_size))

        border_color = None
        if self.selected:
            border_color = color.gold
        elif self.hovering:
            border_color = color.green

        if border_color:
            pygame.draw.rect(surface, border_color, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 2)
