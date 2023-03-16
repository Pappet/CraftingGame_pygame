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
        self.recipe_manager = recipe_manager

        self.info = self._create_info_section()
        self.selected_slot_rect = (self.info['x'], self.info['y'], self.info['width'], self.info['height'])

        self.crafting = self._create_crafting_section()
        self.craft_button = Button(self.crafting['x'] + edge_spacing + (self.crafting['width'] // 2) - 30,
                                   self.crafting['y'] + edge_spacing, 60, title_spacing, "CRAFT", 18, color.black,
                                   color.red, color.coralred,
                                   partial(recipe_manager.craft, recipe_manager.get_recipe_by_name("Stock")))
        button_manager.add_button(self.craft_button)

        self.close_button = Button(x, y, title_spacing, title_spacing, "X", 18, color.black,
                                   color.red, color.coralred, self.toggle_menu)
        button_manager.add_button(self.close_button)

    def _create_info_section(self):
        info_x = self.x + self.edge_spacing
        info_y = self.height - 120 - self.edge_spacing
        left_x = info_x + self.edge_spacing
        left_upper_y = info_y + self.edge_spacing
        left_lower_y = info_y + 120 - 64 - self.edge_spacing
        middle_x = left_x + 80
        right_x = middle_x + 130

        info = {
            'width': self.width - self.edge_spacing * 2,
            'height': 120,
            'x': info_x,
            'y': info_y,
            'left_x': left_x,
            'left_upper_y': left_upper_y,
            'left_lower_y': left_lower_y,
            'middle_x': middle_x,
            'right_x': right_x
        }
        return info

    def _create_crafting_section(self):
        crafting_x = self.x + self.edge_spacing
        crafting_y = self.y + self.title_spacing + self.edge_spacing
        crafting_width = self.width - self.edge_spacing * 2
        crafting_height = self.height - self.title_spacing - (self.edge_spacing * 3) - self.info['height']

        crafting = {
            'x': crafting_x,
            'y': crafting_y,
            'width': crafting_width,
            'height': crafting_height,
            'rect': (crafting_x, crafting_y, crafting_width, crafting_height)
        }
        return crafting

    def draw(self, surface):
        super().draw(surface)
        # draw the selected item's info
        if self.active:
            self.draw_item_info(surface)
            self.draw_crafting(surface)

    def draw_item_info(self, surface):
        pygame.draw.rect(surface, color.gray, self.selected_slot_rect)

        selected_slot = self.inventory.selected_slot
        if selected_slot is not None and selected_slot.get_item_in_slot():
            item = selected_slot.get_item_in_slot()
            stackable_str = "stackable" if item.stackable else "not stackable"
            image_item = item.get_image()

            text.draw_text(surface, item.name, int(self.menu_font_size * 1.5), color.white, self.info["left_x"],
                           self.info["left_upper_y"])
            text.draw_text(surface, f"Amount: {selected_slot.amount}", self.menu_font_size, color.white,
                           self.info["middle_x"], self.info["left_lower_y"] + 20 + self.edge_spacing)
            text.draw_text(surface, stackable_str, self.menu_font_size, color.white, self.info["middle_x"],
                           self.info["left_lower_y"] + 40 + self.edge_spacing)
            surface.blit(image_item, (self.info["left_x"], self.info["left_lower_y"]))
            text.draw_multiline_text(surface, item.description, self.menu_font_size, color.white, self.info["right_x"],
                                     self.info["y"] + self.edge_spacing, 200)

    def draw_crafting(self, surface):
        pygame.draw.rect(surface, color.gray, self.crafting["rect"])
