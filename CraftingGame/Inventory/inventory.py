from Inventory.slot import Slot
import pygame
import random
import helper.color as color


class Inventory:
    def __init__(self, x, y, slot_size, slot_spacing, rows, cols, edge_spacing, title_spacing, title):
        self.x = x
        self.y = y
        self.slot_size = slot_size
        self.slot_spacing = slot_spacing
        self.edge_spacing = edge_spacing
        self.title_spacing = title_spacing
        self.title = title
        self.rows = rows
        self.cols = cols
        self.width = self.slot_size*self.cols + \
            (self.slot_spacing*self.cols) - \
            self.slot_spacing + (edge_spacing*2)
        self.height = self.slot_size*self.rows + \
            (self.slot_spacing*self.rows) - \
            self.slot_spacing + (edge_spacing*2) + self.title_spacing
        self.slots = []
        self.create_slots()

        self.image = pygame.Surface((self.width, self.height))
        self.bg_color = color.gray
        # change the font to a system font that is available on your system
        self.font = pygame.font.SysFont("arial", self.title_spacing)

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

    def get_selected_item(self, mouse_pos):
        # convert mouse position to grid coordinates
        grid_x = (mouse_pos[0] -
                  self.x) // (self.slot_size + self.slot_spacing)
        grid_y = (mouse_pos[1] - self.y -
                  30) // (self.slot_size + self.slot_spacing)
        # check if mouse position is inside the inventory
        if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows:
            # get the selected slot
            slot = self.slots[grid_y * self.cols + grid_x]
            # select the slot
            for s in self.slots:
                s.selected = False
            slot.selected = True
            # get the item in the slot, if any
            return slot.item
        # deselect all slots if not clicked on a slot
        for s in self.slots:
            s.selected = False
        return None

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

    def get_image(self):
        return self.image

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
