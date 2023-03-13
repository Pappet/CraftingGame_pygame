import pygame
import CraftingGame.helper.color as color
import CraftingGame.helper.pygame_text as text
from CraftingGame.menus.Menu import Menu


class CraftingMenu(Menu):
    def __init__(self, x, y, width, height, edge_spacing, menu_font_size, title_spacing, title, active, inventory, item_manager, message_menu):
        super().__init__(x=x, y=y, message_menu = message_menu, width=width, height=height,
                         edge_spacing=edge_spacing, menu_font_size=menu_font_size, title_spacing=title_spacing,
                         title=title, active=active)
        self.bg_color = color.gainsboro
        self.inventory = inventory
        self.item_manager = item_manager

        self.info_width = self.width - self.edge_spacing * 2
        self.info_height = 100
        self.info_x = self.x + self.edge_spacing
        self.info_y = self.height - self.info_height - self.edge_spacing
        self.info_left_x = self.info_x + self.edge_spacing
        self.info_middle_x = self.info_left_x + 80
        self.info_right_x = self.info_middle_x + 130

        self.selected_slot_rect = (self.info_x, self.info_y, self.info_width, self.info_height)

    def draw(self, surface):
        super().draw(surface)
        # draw the selected item's info
        if self.active:
            pygame.draw.rect(surface, color.gray, self.selected_slot_rect)
            if self.inventory.selected_slot is not None and self.inventory.selected_slot.get_item_in_slot():
                if self.inventory.selected_slot.get_item_in_slot().stackable:
                    stackable_str = "stackable"
                else:
                    stackable_str = "not stackable"
                image_item = self.inventory.selected_slot.get_item_in_slot().get_image()

                text.draw_text(surface, self.inventory.selected_slot.get_item_in_slot().name, int(self.menu_font_size*1.5), color.white, self.info_middle_x, self.info_y + self.edge_spacing)
                text.draw_text(surface, f"Amount: {self.inventory.selected_slot.amount}", self.menu_font_size, color.white, self.info_middle_x, self.info_y + self.edge_spacing + 20)
                text.draw_text(surface, stackable_str, self.menu_font_size, color.white, self.info_middle_x, self.info_y + self.edge_spacing + 40)
                surface.blit(image_item, (self.info_left_x, self.info_y + self.info_height//2 - image_item.get_height()//2))
                text.draw_multiline_text(surface, self.inventory.selected_slot.get_item_in_slot().description, self.menu_font_size,
                                         color.white,
                                         self.info_right_x, self.info_y + self.edge_spacing, 200)
