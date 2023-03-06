from typing import Tuple, Optional

from CraftingGame.menus.slot import Slot
import pygame
import CraftingGame.helper.color as color
from CraftingGame.menus.menu import Menu


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
        self.selected_slot = None
        self.dragging_image = None
        self.max_stack_size = 99

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

    def get_slot_at_position(self, pos: Tuple[int, int]) -> Optional[Slot]:
        for i, slot in enumerate(self.slots):
            if slot.rect.collidepoint(pos):
                return slot
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
        if item.stackable:
            for slot in self.slots:
                if not slot.is_empty():
                    if slot.item.id == item.id and not None:
                        slot.add_item(item)
                        return True
                else:
                    if slot.is_empty():
                        slot.add_item(item)
                        return True
        else:
            for slot in self.slots:
                if slot.is_empty():
                    slot.add_item(item)
                    return True
        return False

    def remove_item(self, item):
        for slot in self.slots:
            if not slot.is_empty():
                if slot.item.id == item.id and item.stackable:
                    slot.remove_item()
                    return True

        return False

    def move_item(self, from_slot: Slot, to_slot: Slot) -> None:
        from_item = from_slot.item
        to_item = to_slot.item
        if from_item is not None:
            if to_slot.is_empty():
                # Move item from source slot to target slot
                to_slot.item = from_item
                from_slot.item = None
                to_slot.amount = from_slot.amount
                from_slot.amount = 0
            elif from_item.id == to_item.id and from_item.stackable:
                # Increment item count if the items are stackable and have the same id
                total_amount = from_slot.amount + to_slot.amount
                if total_amount <= self.max_stack_size:
                    to_slot.amount = total_amount
                    from_slot.item = None
                    from_slot.amount = 0
                else:
                    diff = total_amount - self.max_stack_size
                    to_slot.amount = self.max_stack_size
                    from_slot.amount = diff
            else:
                # Swap items between source slot and target slot
                to_slot.item = from_item
                to_slot.amount = from_slot.amount
                from_slot.item = to_item
                from_slot.amount = to_slot.amount

    def draw(self, surface):
        if self.active:
            self.image.fill(self.bg_color)
            bg_rect = self.image.get_rect(topleft=(self.x, self.y))
            # top-left=(self.x - self.edge_spacing, self.y - self.edge_spacing - self.title_spacing))
            pygame.draw.rect(surface, self.bg_color, bg_rect)

            title_surface = self.font.render(
                f"{self.title} ({self.get_free_inventory_space()}/{self.get_inventory_space()})", True, color.black)
            surface.blit(title_surface, (self.x - (title_surface.get_width()/2) +
                                         (self.width/2) - (self.edge_spacing/2), self.y + (self.edge_spacing/2)))

            for slot in self.slots:
                slot.draw(surface)

            # draw the selected item's info
            if self.selected_slot is not None and self.selected_slot.item_in_slot():
                font = pygame.font.Font(None, self.menu_font_size)
                name_text = font.render(
                    self.selected_slot.item_in_slot().name, True, color.white)
                desc_text = font.render(
                    self.selected_slot.item_in_slot().description, True, color.white)
                image_item = self.selected_slot.item_in_slot().get_image()
                amount_text = font.render(
                    f"Amount: {self.selected_slot.amount}", True, color.white)
                if self.selected_slot.item_in_slot().stackable:
                    stackable_str = "stackable"
                else:
                    stackable_str = "not stackable"
                stackable_text = font.render(stackable_str, True, color.white)
                surface.blit(image_item, (self.x +
                                          self.width + self.slot_spacing, self.y))
                surface.blit(name_text, (self.x +
                                         self.width + self.slot_spacing, self.y + 40))
                surface.blit(desc_text, (self.x +
                                         self.width + self.slot_spacing, self.y + 60))
                surface.blit(amount_text, (self.x + self.width +
                             self.slot_spacing, self.y + 80))
                surface.blit(stackable_text, (self.x +
                                              self.width + self.slot_spacing, self.y + 100))

            if self.dragging_image is not None:
                # Render the dragging image surface at the mouse position
                mouse_pos = pygame.mouse.get_pos()
                x, y = mouse_pos[0] - self.dragging_image.get_width() / 2, mouse_pos[
                    1] - self.dragging_image.get_height() / 2
                surface.blit(self.dragging_image, (x, y))

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                # testing the inventory - add and remove a test item
                if event.key == pygame.K_a:
                    if self.get_free_inventory_space() > 0 and not self.selected_slot.is_empty():
                        self.add_item(self.selected_slot.item)
                elif event.key == pygame.K_r:
                    if self.get_free_inventory_space() < self.get_inventory_space() and self.selected_slot:
                        if not self.selected_slot.remove_item():
                            self.selected_slot = None
            if event.key == pygame.K_x:
                self.toggle_menu()
                if not self.active:
                    if self.selected_slot:
                        self.selected_slot.selected = False
                        self.selected_slot = None

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.active:
                # check if left mouse button was pressed
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    slot_index = self.get_slot_at_position(pos)
                    if slot_index is not None:
                        self.selected_slot = slot_index
                        if not slot_index.is_empty():
                            self.dragging_image = slot_index.item_in_slot().get_image()

                    selected_slot_index = False
                    # Go through all slots and check if the position of the click is within in one slot
                    for slot in self.slots:
                        if slot.is_clicked(event.pos):
                            # slot was clicked. Set the helper index to true
                            selected_slot_index = True
                            # set the item in slot
                            self.selected_slot = slot

                        # if no slot was clicked set it to None
                        if selected_slot_index is False:
                            self.selected_slot = None
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                slot_index = self.get_slot_at_position(pos)
                if slot_index is not None and slot_index != self.selected_slot:
                    self.move_item(self.selected_slot, slot_index)
                    self.selected_slot.selected = False
                    slot_index.selected = True
                    self.selected_slot = slot_index
                    self.dragging_image = None
                if slot_index == self.selected_slot:
                    self.dragging_image = None
