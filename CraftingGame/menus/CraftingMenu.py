import pygame
from functools import partial

import CraftingGame.helper.color as color
import CraftingGame.helper.pygame_text as text
from CraftingGame.menus.Menu import Menu
from CraftingGame.menus.Button import Button


class CraftingMenu(Menu):
    def __init__(self, x, y, width, height, edge_spacing, menu_font_size, title_spacing, title, active, inventory, item_manager, message_menu, button_manager, recipe_manager):
        super().__init__(x=x, y=y, message_menu=message_menu, button_manager=button_manager, width=width, height=height,
                         edge_spacing=edge_spacing, menu_font_size=menu_font_size, title_spacing=title_spacing,
                         title=title, active=active)
        self.bg_color = color.gainsboro
        self.inventory = inventory
        self.item_manager = item_manager
        self.button_manager = button_manager
        self.recipe_manager = recipe_manager

        self.info_width = self.width - self.edge_spacing * 2
        self.info_height = 120
        self.info_x = self.x + self.edge_spacing
        self.info_y = self.height - self.info_height - self.edge_spacing
        self.info_left_x = self.info_x + self.edge_spacing
        self.info_left_upper_y = self.info_y + self.edge_spacing
        self.info_left_lower_y = self.info_y + self.info_height - 64 - self.edge_spacing
        self.info_middle_x = self.info_left_x + 80
        self.info_right_x = self.info_middle_x + 130
        self.selected_slot_rect = (self.info_x, self.info_y, self.info_width, self.info_height)

        self.crafting_width = self.width - self.edge_spacing * 2
        self.crafting_height = self.height - self.title_spacing - (self.edge_spacing * 3) - self.info_height
        self.crafting_x = self.x + self.edge_spacing
        self.crafting_y = self.y + self.title_spacing + self.edge_spacing
        self.crafting_rect = (self.crafting_x, self.crafting_y, self.crafting_width, self.crafting_height)
        self.craft_button = Button(self.crafting_x + self.edge_spacing + (self.crafting_width//2) - 30, self.crafting_y + self.edge_spacing, 60, self.title_spacing, "CRAFT", 18, color.black,
                                   color.red, color.coralred, partial(recipe_manager.craft, recipe_manager.get_recipe_by_name("Stock")))
        self.button_manager.add_button(self.craft_button)

        self.close_button = Button(self.x, self.y, self.title_spacing, self.title_spacing, "X", 18, color.black,
                                   color.red, color.coralred, self.toggle_menu)
        self.button_manager.add_button(self.close_button)

    def draw(self, surface):
        super().draw(surface)
        # draw the selected item's info
        if self.active:
            self.draw_item_info(surface)
            self.draw_crafting(surface)

    def draw_item_info(self, surface):
        pygame.draw.rect(surface, color.gray, self.selected_slot_rect)
        if self.inventory.selected_slot is not None and self.inventory.selected_slot.get_item_in_slot():
            if self.inventory.selected_slot.get_item_in_slot().stackable:
                stackable_str = "stackable"
            else:
                stackable_str = "not stackable"
            image_item = self.inventory.selected_slot.get_item_in_slot().get_image()

            text.draw_text(surface, self.inventory.selected_slot.get_item_in_slot().name,
                           int(self.menu_font_size * 1.5), color.white, self.info_left_x, self.info_left_upper_y)
            text.draw_text(surface, f"Amount: {self.inventory.selected_slot.amount}", self.menu_font_size, color.white,
                           self.info_middle_x, self.info_left_lower_y + 20 + self.edge_spacing)
            text.draw_text(surface, stackable_str, self.menu_font_size, color.white, self.info_middle_x,
                           self.info_left_lower_y + 40 + self.edge_spacing)
            surface.blit(image_item, (self.info_left_x, self.info_left_lower_y))
            text.draw_multiline_text(surface, self.inventory.selected_slot.get_item_in_slot().description,
                                     self.menu_font_size,
                                     color.white,
                                     self.info_right_x, self.info_y + self.edge_spacing, 200)

    def draw_crafting(self, surface):
        pygame.draw.rect(surface, color.gray, self.crafting_rect)