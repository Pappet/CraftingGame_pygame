from menus.slot import Slot
import pygame
import helper.color as color
from .menu import Menu


class Inventory(Menu):
    def __init__(self, x, y, width, height, slot_size, slot_spacing, rows, cols, edge_spacing, title_spacing, title):
        super().__init__(x=x, y=y, width=width, height=height,
                         edge_spacing=edge_spacing, title_spacing=title_spacing, title=title)

        self.slot_size = slot_size
        self.slot_spacing = slot_spacing
        self.rows = rows
        self.cols = cols
        self.width = self.slot_size*self.cols + \
            (self.slot_spacing*self.cols) - \
            self.slot_spacing + (self.edge_spacing*2)

        self.height = self.slot_size*self.rows + \
            (self.slot_spacing*self.rows) - self.slot_spacing + \
            (self.edge_spacing*2) + self.title_spacing

        self.image = pygame.Surface((self.width, self.height))
        self.slots = []
        self.create_slots()

    def create_slots(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.x + col * (self.slot_size +
                                    self.slot_spacing) + self.edge_spacing
                y = self.y + row * (self.slot_size +
                                    self.slot_spacing) + self.title_spacing + self.edge_spacing
                slot = Slot(x, y, self.slot_size, self.slot_size)
                self.slots.append(slot)

    def get_slot(self, index):
        return self.slots[index]

    def get_slot_index(self, slot):
        return self.slots.index(slot)

    def get_last_filled_slot(self):
        for slot in reversed(self.slots):
            if not slot.is_empty():
                return slot

    def get_inventory_space(self):
        return len(self.slots)

    def get_free_inventory_space(self):
        index = 0
        for slot in self.slots:
            if slot.is_empty():
                index += 1
        return index

    def add_item(self, item):
        for slot in self.slots:
            if slot.is_empty():
                slot.add_item(item)
                return True
        return False

    def remove_item(self, item):
        for slot in self.slots:
            if slot.item == item:
                slot.remove_item()
                return True
        return False

    def draw(self, surface):
        self.image.fill(self.bg_color)
        bg_rect = self.image.get_rect(topleft=(self.x, self.y))
        # topleft=(self.x - self.edge_spacing, self.y - self.edge_spacing - self.title_spacing))
        pygame.draw.rect(surface, self.bg_color, bg_rect)

        title_surface = self.font.render(
            f"{self.title} ({self.get_free_inventory_space()}/{self.get_inventory_space()})", True, color.black)
        surface.blit(title_surface, (self.x - (title_surface.get_width()/2) +
                     (self.width/2) - (self.edge_spacing/2), self.y + (self.edge_spacing/2)))

        for slot in self.slots:
            slot.draw(surface)
