from menus.slot import Slot
import pygame
import helper.color as color
from .menu import Menu
from .item import Item
from .item_types import ItemType


class Inventory(Menu):
    def __init__(self, x, y, width, height, slot_size, slot_spacing, rows, cols, edge_spacing, menu_font_size, title_spacing, title, active):
        super().__init__(x=x, y=y, width=width, height=height,
                         edge_spacing=edge_spacing, menu_font_size=menu_font_size, title_spacing=title_spacing, title=title, active=active)

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
        self.active = active
        self.selected_item = None

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
        if self.active:
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

            # draw the selected item's info
            if self.selected_item is not None:
                font = pygame.font.Font(None, self.menu_font_size)
                name_text = font.render(
                    self.selected_item.name, True, color.white)
                desc_text = font.render(
                    self.selected_item.description, True, color.white)
                image_item = self.selected_item.get_image()
                surface.blit(image_item, (self.x +
                                          self.width + self.slot_spacing, self.y))
                surface.blit(name_text, (self.x +
                                         self.width + self.slot_spacing, self.y + 40))
                surface.blit(desc_text, (self.x +
                                         self.width + self.slot_spacing, self.y + 60))

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                # testing the inventory - add and remove an test item
                if event.key == pygame.K_a:
                    if self.get_free_inventory_space() > 0:
                        self.add_item(
                            Item("TEST", ItemType.RESSOURCE, "THIS IS A TEST ITEM!"))
                elif event.key == pygame.K_r:
                    if self.get_free_inventory_space() < self.get_inventory_space():
                        self.remove_item(
                            self.get_last_filled_slot().item)
            if event.key == pygame.K_x:

                self.toogle_menu()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.active:
                # check if left mouse button was pressed
                if event.button == 1:
                    selected_item_index = False
                    # Go through all slots and check if the position of the click is within in one slot
                    for slot in self.slots:
                        if slot.is_clicked(event.pos):
                            # slot was clicked. Set the helper index to true
                            selected_item_index = True
                            # set the item in slot
                            self.selected_item = slot.item_in_slot()
                        # if no slot was clicked set it to None
                        if selected_item_index is False:
                            self.selected_item = None
