import pygame
import helper.color as color
from menus.inventory import Inventory
from menus.item import Item
from menus.item_types import ItemType
from menus.menu import Menu
from menus.menus_manager import menus_manager

pygame.init()

# ---- Variables --------------------------------------------------------
screen_width = 1200
screen_height = 800
screen_title = "Crafting Empire"
running = True

inventory_rows = 4
inventory_cols = 5
inventory_tile = "Inventory"
inventory_slot_size = 32
menu_spacing = 10
menu_title_spacing = 24
menu_font_size = 18

# ---- various --------------------------------------------------------
clock = pygame.time.Clock()

# ---- Pygame Screen --------------------------------------------------------
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(screen_title)
window_position = screen.get_rect().center
pygame.display.window_pos = window_position

# ---- create menus and menu manager --------------------------------------------------------
menu_manager = menus_manager()
inventory = Inventory(0, 0, 100, 100, inventory_slot_size, menu_spacing, inventory_rows,
                      inventory_cols, menu_spacing, menu_font_size, menu_title_spacing, inventory_tile, True)

test_menu = Menu(300, 300, 200, 200, menu_spacing,
                 menu_font_size, menu_title_spacing, "TEST", True)
menu_manager.add_menu(inventory)
menu_manager.add_menu(test_menu)

# ---- create inventory and items --------------------------------------------------------
item1 = Item("Sword", ItemType.WEAPON, "A sharp sword for combat.")
item2 = Item("Potion", ItemType.POTION, "A magical potion that heals you.")

inventory.add_item(item1)
inventory.add_item(item2)


# ---- Haupt-Schleife --------------------------------------------------------
while running:
    # Event-Handling
    for event in pygame.event.get():
        # the close button on the window was pressed
        if event.type == pygame.QUIT:
            running = False
        menu_manager.update(event)

    # clear the screen with black
    screen.fill(color.black)
    # draw inventory
    menu_manager.draw(screen)

    pygame.display.update()
    # limit the frame rate to 60 FPS
    clock.tick(60)

# Stop the Game and close the window
pygame.quit()
quit()
