from typing import Tuple, Optional

from CraftingGame.menus.Slot import Slot
import pygame
import CraftingGame.helper.color as color
from CraftingGame.menus.Menu import Menu
from CraftingGame.menus.Button import Button


class Inventory(Menu):
    def __init__(self, x, y, width, height, slot_size, slot_spacing, rows, cols, edge_spacing, menu_font_size,
                 title_spacing, title, active, message_menu, button_manager):
        super().__init__(x=x, y=y, message_menu=message_menu, button_manager=button_manager, width=width, height=height,
                         edge_spacing=edge_spacing, menu_font_size=menu_font_size, title_spacing=title_spacing,
                         title=title, active=active)

        self.slot_size = slot_size
        self.slot_spacing = slot_spacing
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height

        self.image = pygame.Surface((self.width, self.height))
        self.slots = []
        self.create_slots()
        self.active = active
        self.selected_slot = None
        self.hovering_slot = None
        self.dragging_image = None
        self.max_stack_size = 99

        self.close_button = Button(self.x, self.y, self.title_spacing, self.title_spacing, "X", 18, color.black,
                                   color.red, color.coralred, self.toggle_menu)
        self.button_manager.add_button(self.close_button)

    def create_slots(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x = (
                        self.x
                        + col * (self.slot_size + self.slot_spacing)
                        + self.edge_spacing
                )
                y = (
                        self.y
                        + row * (self.slot_size + self.slot_spacing)
                        + self.title_spacing
                        + self.edge_spacing
                )
                slot = Slot(x, y, self.slot_size, self.slot_size)
                self.slots.append(slot)

    def get_slot(self, index):
        return self.slots[index]

    def get_slot_index(self, slot):
        return self.slots.index(slot)

    def get_slot_at_position(self, pos: Tuple[int, int]) -> Optional[Slot]:
        for slot in self.slots:
            if slot.rect.collidepoint(pos):
                return slot
        return None

    def get_last_filled_slot(self):
        for slot in reversed(self.slots):
            if not slot.is_empty():
                return slot

    def get_free_slot(self) -> Slot:
        for slot in self.slots:
            if slot.is_empty():
                return slot

    def get_inventory_space(self):
        return len(self.slots)

    def get_free_inventory_space(self):
        return sum(1 for slot in self.slots if slot.is_empty())

    def get_items(self):
        items = {}
        for slot in self.slots:
            if not slot.is_empty():
                item_name = slot.get_item_in_slot().get_name()
                if item_name not in items:
                    items[item_name] = slot.amount
                else:
                    items[item_name] += slot.amount
        return items

    def get_item_amount(self, name):
        return self.get_items().get(name, 0)

    def get_slots_with_item(self, item):
        return [
            slot
            for slot in self.slots
            if not slot.is_empty() and slot.get_item_in_slot().id == item.id
        ]

    def add_item(self, item, amount):
        if item.stackable:
            # Check if there is an existing stack with the same item
            for slot in self.slots:
                if not slot.is_empty() and slot.item.id == item.id:
                    remaining_space = self.max_stack_size - slot.amount
                    if remaining_space >= amount:
                        slot.add_item(item, amount)
                        return True
                    else:
                        slot.add_item(item, remaining_space)
                        amount -= remaining_space

            # If there is remaining amount, try to add it to an empty slot or create new stacks
            while amount > 0:
                free_slot = self.get_free_slot()
                if free_slot is not None:
                    stack_size = min(amount, self.max_stack_size)
                    free_slot.add_item(item, stack_size)
                    amount -= stack_size
                else:
                    self.message_menu.add_message("Not enough free inventory space!")
                    return False
        else:
            if amount == 1:
                free_slot = self.get_free_slot()
                if free_slot is not None:
                    free_slot.add_item(item, 1)
                    return True
                else:
                    self.message_menu.add_message("Not enough free inventory space!")
                    return False
            else:
                if self.get_free_inventory_space() >= amount:
                    for i in range(amount):
                        free_slot = self.get_free_slot()
                        if free_slot is not None:
                            free_slot.add_item(item, 1)
                    return True
                else:
                    self.message_menu.add_message("Not enough free inventory space!")
                    return False
        return False

    def remove_item(self, item, amount):
        # Check if there are enough items in the inventory
        if self.get_item_amount(item.name) < amount:
            self.message_menu.add_message("Not enough Items in Inventory")
            return False

        # Get the list of slots containing the item
        slots_with_item = reversed(self.get_slots_with_item(item))

        # Case 1: Item is stackable
        if item.stackable:
            remaining_amount = amount
            for slot in slots_with_item:
                # Remove as many items as possible from the current slot
                if remaining_amount > slot.amount:
                    remaining_amount -= slot.amount
                    slot.remove_item(slot.amount)
                else:
                    slot.remove_item(remaining_amount)
                    return True

        # Case 2: Item is not stackable
        else:
            remaining_amount = amount
            for slot in slots_with_item:
                # Remove one item from each slot until the desired amount is removed
                if remaining_amount > 0:
                    slot.remove_item(1)
                    remaining_amount -= 1
                else:
                    break
            return True

        return False

    def move_item(self, from_slot: Slot, to_slot: Slot) -> None:
        from_item = from_slot.item
        to_item = to_slot.item

        if from_item is not None:
            # Case 1: Move item to an empty slot
            if to_slot.is_empty():
                to_slot.item = from_item
                from_slot.item = None
                to_slot.amount = from_slot.amount
                from_slot.amount = 0
                self.message_menu.add_message(f"Moved {to_slot.item.name} ({to_slot.amount}) to an empty slot.")

            # Case 2: Merge stackable items with the same id
            elif from_item.id == to_item.id and from_item.stackable:
                total_amount = from_slot.amount + to_slot.amount

                if total_amount <= self.max_stack_size:
                    to_slot.amount = total_amount
                    from_slot.item = None
                    from_slot.amount = 0
                    self.message_menu.add_message(f"Added {from_slot.amount} of {from_item.name} to the slot")
                else:
                    diff = total_amount - self.max_stack_size
                    to_slot.amount = self.max_stack_size
                    from_slot.amount = diff
                    self.message_menu.add_message(
                        f"Added {self.max_stack_size} of {from_item.name} to the slot. {diff} remaining in the other slot.")

            # Case 3: Swap items between slots
            else:
                to_slot_buffer_amount = to_slot.amount
                from_slot_buffer_amount = from_slot.amount

                to_slot.item = from_item
                to_slot.amount = from_slot_buffer_amount
                from_slot.item = to_item
                from_slot.amount = to_slot_buffer_amount
                self.message_menu.add_message(
                    f"Swapped {from_item.name} ({from_slot_buffer_amount}) with {to_item.name} ({to_slot_buffer_amount})")

    def draw(self, surface):
        if self.active:
            # Fill the background and draw it on the surface
            self.image.fill(self.bg_color)
            bg_rect = self.image.get_rect(topleft=(self.x, self.y))
            pygame.draw.rect(surface, self.bg_color, bg_rect)

            # Draw the Inventory title with additional information
            pygame.draw.rect(surface, color.gray, (self.x, self.y, self.width, self.title_spacing))
            title_text = f"{self.title} ({self.get_free_inventory_space()} / {self.get_inventory_space()})"
            title_surface = self.font.render(title_text, True, color.black)

            # Calculate title position
            title_x = self.x + (self.width - title_surface.get_width()) // 2
            title_y = self.y + (self.title_spacing - title_surface.get_height()) // 2
            surface.blit(title_surface, (title_x, title_y))

            # Draw the slots
            for slot in self.slots:
                slot.draw(surface)

            # Render the dragging image surface at the mouse position
            if self.dragging_image is not None:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                x, y = mouse_x - self.dragging_image.get_width() // 2, mouse_y - self.dragging_image.get_height() // 2
                surface.blit(self.dragging_image, (x, y))

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                # Testing the inventory - add and remove a test item
                if event.key == pygame.K_a:
                    # Add an item to the inventory if there is free space and a selected slot with an item
                    if self.get_free_inventory_space() > 0 and not self.selected_slot.is_empty():
                        self.add_item(self.selected_slot.item, 1)
                        self.message_menu.add_message(f"Added {self.selected_slot.item.name} to inventory")
                elif event.key == pygame.K_r:
                    # Remove an item from the inventory if there is an item in a selected slot
                    if self.get_free_inventory_space() < self.get_inventory_space() and self.selected_slot:
                        if not self.remove_item(self.selected_slot.get_item_in_slot(), 1):
                            self.selected_slot = None
            # Toggle the inventory menu visibility
            if event.key == pygame.K_x:
                self.toggle_menu()
                if not self.active and self.selected_slot:
                    self.selected_slot.selected = False
                    self.selected_slot = None

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.active and event.button == 1:  # Check if left mouse button was pressed
                pos = pygame.mouse.get_pos()
                clicked_slot = self.get_slot_at_position(pos)

                # Select the clicked slot and set the dragging image if the slot has an item
                if clicked_slot is not None:
                    self.selected_slot = clicked_slot
                    if not clicked_slot.is_empty():
                        self.dragging_image = clicked_slot.get_item_in_slot().get_image()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                released_slot = self.get_slot_at_position(pos)

                # Move the item from the selected slot to the released slot if they are different slots and the dragging image exists
                if released_slot is not None and released_slot != self.selected_slot and self.dragging_image:
                    self.move_item(self.selected_slot, released_slot)
                    self.selected_slot.selected = False
                    released_slot.selected = True
                    self.selected_slot = released_slot
                self.dragging_image = None

        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            hovering_slot = self.get_slot_at_position(pos)

            # Update the hovering slot status when dragging an item
            if self.dragging_image is not None:
                if self.hovering_slot is None and hovering_slot is not None:
                    self.hovering_slot = hovering_slot
                    self.hovering_slot.hovering = True
                elif self.hovering_slot != hovering_slot:
                    self.hovering_slot.hovering = False
                    self.hovering_slot = hovering_slot
            else:
                if self.hovering_slot is not None:
                    self.hovering_slot.hovering = False
                    self.hovering_slot = None

    """
    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                # testing the inventory - add and remove a test item
                if event.key == pygame.K_a:
                    if self.get_free_inventory_space() > 0 and not self.selected_slot.is_empty():
                        self.add_item(self.selected_slot.item, 1)
                        self.message_menu.add_message(f"Added {self.selected_slot.item.name} to inventory")
                elif event.key == pygame.K_r:
                    if self.get_free_inventory_space() < self.get_inventory_space() and self.selected_slot:
                        if not self.remove_item(self.selected_slot.get_item_in_slot(), 1):
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
                            self.dragging_image = slot_index.get_item_in_slot().get_image()

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
                if slot_index is not None and slot_index != self.selected_slot and self.dragging_image:
                    self.move_item(self.selected_slot, slot_index)
                    self.selected_slot.selected = False
                    slot_index.selected = True
                    self.selected_slot = slot_index
                    self.dragging_image = None
                if slot_index == self.selected_slot:
                    self.dragging_image = None
                if slot_index is None:
                    self.dragging_image = None
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_image is not None:
                pos = pygame.mouse.get_pos()
                slot_index = self.get_slot_at_position(pos)
                if self.hovering_slot is None and slot_index is not None:
                    self.hovering_slot = slot_index
                    self.hovering_slot.hovering = True
                else:
                    if self.hovering_slot != slot_index:
                        self.hovering_slot.hovering = False
                        self.hovering_slot = slot_index
            else:
                if self.hovering_slot is not None:
                    self.hovering_slot.hovering = False
                    self.hovering_slot = None
    """
